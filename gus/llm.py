import os
import asyncio
import logging
import functools
import anthropic
from datetime import datetime, timezone, timedelta
from pathlib import Path
from gus.tools import TOOLS, executar_tool

logger = logging.getLogger(__name__)

BRT = timezone(timedelta(hours=-3))
DIAS_SEMANA = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]

# Erros de servidor Anthropic que valem retry
_STATUS_RETRY = {500, 502, 503, 504, 529}

# Preços por família de modelo (USD por token) — atualizado abr/2026
MODEL_PRICING = {
    "opus":   {"input":  5.0 / 1_000_000, "output": 25.0 / 1_000_000},
    "sonnet": {"input":  3.0 / 1_000_000, "output": 15.0 / 1_000_000},
    "haiku":  {"input":  0.8 / 1_000_000, "output":  4.0 / 1_000_000},
}
FALLBACK_PRICING = MODEL_PRICING["sonnet"]


def _get_pricing(model: str) -> dict:
    """Retorna pricing baseado no nome do modelo."""
    model_lower = model.lower()
    for family, pricing in MODEL_PRICING.items():
        if family in model_lower:
            return pricing
    return FALLBACK_PRICING

client = anthropic.AsyncAnthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    timeout=120.0,  # 2 minutos — evita ficar pendurado se a API travar
)


async def _chamar_claude_com_retry(
    model: str,
    max_tokens: int,
    system_prompt: str,
    messages: list,
    tools: list | None = None,
    max_tentativas: int = 4,
):
    """Chama Claude com backoff exponencial (1s, 2s, 4s, 8s) e fallback de modelo.

    Tenta o modelo primário até max_tentativas vezes em erros 5xx/529.
    Se esgotar, tenta o MODEL_FALLBACK (default Haiku) com mesma política.
    Re-lança a última APIStatusError se tudo falhar.
    """
    modelos = [model]
    fallback = os.getenv("MODEL_FALLBACK", "claude-haiku-4-5-20251001")
    if fallback and fallback != model:
        modelos.append(fallback)

    ultima_excecao: Exception | None = None
    for modelo_atual in modelos:
        for tentativa in range(max_tentativas):
            try:
                kwargs: dict = {
                    "model": modelo_atual,
                    "max_tokens": max_tokens,
                    "system": system_prompt,
                    "messages": messages,
                }
                if tools is not None:
                    kwargs["tools"] = tools
                return await client.messages.create(**kwargs)
            except (anthropic.APIStatusError, anthropic.APIConnectionError, anthropic.APITimeoutError) as e:
                ultima_excecao = e
                status = getattr(e, "status_code", None)
                # 4xx (exceto 429) — não adianta retry
                if status and status < 500 and status != 429:
                    raise
                if tentativa < max_tentativas - 1:
                    espera = 2 ** tentativa  # 1, 2, 4, 8
                    logger.warning(
                        f"Claude {modelo_atual} falhou (status={status}, "
                        f"tentativa {tentativa+1}/{max_tentativas}), aguardando {espera}s"
                    )
                    await asyncio.sleep(espera)
        logger.warning(f"Desistindo de {modelo_atual} após {max_tentativas} tentativas")

    raise ultima_excecao if ultima_excecao else RuntimeError("Claude indisponível")

RESUMO_SYSTEM_PROMPT = """Você analisa um trecho de conversa entre Gustavo e o Gus (seu agente pessoal) e extrai o que vale ser gravado no Mem0 como memória de longo prazo.

Extraia APENAS:
- Decisões tomadas e o porquê
- Preferências reveladas (comunicação, hábitos, gostos)
- Fatos novos sobre Gustavo (saúde, projetos, pessoas, rotina, compromissos)
- Ações prometidas ou combinadas
- Contexto técnico relevante pra futuras conversas (arquitetura, bugs resolvidos, caminhos)

Ignore:
- Saudações e confirmações curtas
- Conversa pequena sem conteúdo
- Informação genérica que qualquer um saberia
- Repetição do que já é óbvio pelo system prompt

Formato: lista numerada. Cada item um fato curto e direto, em português. Se não houver nada relevante, responde exatamente: sem conteúdo relevante.
"""


async def gerar_resumo_turnos(messages: list[dict]) -> str:
    """Gera resumo extrativo dos turnos pra salvar no Mem0."""
    linhas = []
    for msg in messages:
        role = "Gustavo" if msg["role"] == "user" else "Gus"
        content = msg["content"]
        if isinstance(content, list):
            partes = [c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"]
            content = " ".join(p for p in partes if p).strip() or "[mídia]"
        linhas.append(f"{role}: {content}")

    conversa = "\n\n".join(linhas)
    model = os.getenv("MODEL_RESUMO", "claude-haiku-4-5-20251001")

    response = await _chamar_claude_com_retry(
        model=model,
        max_tokens=1024,
        system_prompt=RESUMO_SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"Trecho de conversa pra analisar:\n\n{conversa}\n\nExtraia o que vale gravar como memória:"
        }],
    )
    texto = next((b.text for b in response.content if hasattr(b, "text")), "")
    return texto.strip()


@functools.lru_cache(maxsize=1)
def _load_system_prompt() -> str:
    path = Path(__file__).parent / "system_prompt.md"
    return path.read_text(encoding="utf-8")


async def gerar_resposta(messages: list[dict], memory_context: str = "") -> tuple[str, dict]:
    model = os.getenv("MODEL_DEFAULT", "claude-sonnet-4-6")
    max_tokens = int(os.getenv("MAX_TOKENS_RESPONSE", "2048"))

    system_prompt = _load_system_prompt()
    agora = datetime.now(BRT)
    dia_semana = DIAS_SEMANA[agora.weekday()]
    system_prompt += (
        f"\n\n## Data e hora atuais\n"
        f"Hoje é {dia_semana}, {agora.strftime('%d/%m/%Y')}, {agora.strftime('%H:%M')} (horário de Brasília)."
    )
    if memory_context:
        system_prompt += f"\n\n## Memórias relevantes\n{memory_context}"

    total_in = 0
    total_out = 0
    current_messages = list(messages)
    max_tool_rounds = 10

    # Loop de tool calling — continua até Claude retornar texto final
    for _ in range(max_tool_rounds):
        try:
            response = await _chamar_claude_com_retry(
                model=model,
                max_tokens=max_tokens,
                system_prompt=system_prompt,
                messages=current_messages,
                tools=TOOLS,
            )
        except anthropic.APIStatusError as e:
            status = getattr(e, "status_code", None)
            if status in _STATUS_RETRY:
                pricing = _get_pricing(model)
                cost_usd = round((total_in * pricing["input"]) + (total_out * pricing["output"]), 6)
                return (
                    "A API da IA tá sobrecarregada agora (status {}). Tentei várias vezes sem sucesso. "
                    "Tenta de novo em 1-2 minutos.".format(status)
                ), {
                    "model": model, "tokens_in": total_in,
                    "tokens_out": total_out, "cost_usd": cost_usd,
                    "error": f"api_overload_{status}"
                }
            raise

        total_in += response.usage.input_tokens
        total_out += response.usage.output_tokens

        if response.stop_reason == "tool_use":
            # Executa as tools e continua o loop
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = await executar_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            current_messages = current_messages + [
                {"role": "assistant", "content": response.content},
                {"role": "user", "content": tool_results}
            ]
        else:
            # Resposta final em texto
            text = next(
                (b.text for b in response.content if hasattr(b, "text")),
                ""
            )
            pricing = _get_pricing(model)
            cost_usd = round((total_in * pricing["input"]) + (total_out * pricing["output"]), 6)
            metadata = {
                "model": model,
                "tokens_in": total_in,
                "tokens_out": total_out,
                "cost_usd": cost_usd
            }
            return text, metadata

    # Saída de segurança se o loop de tools esgotar
    pricing = _get_pricing(model)
    cost_usd = round((total_in * pricing["input"]) + (total_out * pricing["output"]), 6)
    return "Desculpa, entrei em loop interno. Tenta reformular.", {
        "model": model, "tokens_in": total_in,
        "tokens_out": total_out, "cost_usd": cost_usd
    }
