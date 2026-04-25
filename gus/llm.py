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
    system_prompt,  # str OU lista de blocos (pra prompt caching)
    messages: list,
    tools: list | None = None,
    max_tentativas: int = 4,
):
    """Chama Claude com backoff exponencial (1s, 2s, 4s, 8s) e fallback de modelo.

    Tenta o modelo primário até max_tentativas vezes em erros 5xx/529.
    Se esgotar, tenta o MODEL_FALLBACK (default Haiku) com mesma política.
    Re-lança a última APIStatusError se tudo falhar.

    `system_prompt` pode ser str (uso simples) ou lista de blocos
    (pra prompt caching com cache_control: ephemeral).
    """
    modelos = [model]
    fallback = os.getenv("MODEL_FALLBACK", "claude-haiku-4-5")
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
                # Beta header token-efficient-tools: comprime os schemas das tools
                # no contexto enviado ao modelo. Reduz ~30-40% dos tokens dos tools.
                # Só faz sentido quando há tools — em chamadas sem tools (resumo de
                # turnos via Haiku), o header é dispensável.
                if tools is not None:
                    kwargs["tools"] = tools
                    kwargs["extra_headers"] = {
                        "anthropic-beta": "token-efficient-tools-2025-02-19"
                    }
                return await client.messages.create(**kwargs)
            except (anthropic.APIStatusError, anthropic.APIConnectionError, anthropic.APITimeoutError) as e:
                ultima_excecao = e
                status = getattr(e, "status_code", None)
                # 4xx (exceto 429) — não adianta retry; loga detalhes antes de propagar
                if status and status < 500 and status != 429:
                    body = getattr(e, "body", None)
                    msg = str(body) if body else str(e)
                    logger.error(
                        f"Claude {modelo_atual} erro não-retryable (status={status}): {msg[:500]}"
                    )
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


def _mensagem_erro_amigavel(e: Exception) -> str:
    """Converte erro da API Anthropic em mensagem clara em português pro Gustavo."""
    status = getattr(e, "status_code", None)
    body = getattr(e, "body", None) or {}

    api_msg = ""
    error_type = ""
    if isinstance(body, dict):
        err = body.get("error", {})
        if isinstance(err, dict):
            api_msg = err.get("message", "") or ""
            error_type = err.get("type", "") or ""
    msg_lower = api_msg.lower()

    # Sem créditos — caso mais comum quando para de funcionar do nada
    if any(tok in msg_lower for tok in ["credit balance", "insufficient credit", "out of credit", "usage credits", "disabled because"]):
        return (
            "A conta Anthropic tá sem créditos. Pra voltar, o Gustavo precisa "
            "adicionar saldo em console.anthropic.com/settings/billing (ativar auto-reload "
            "evita interrupção futura)."
        )

    if status == 401 or "authentication" in error_type.lower():
        return (
            "Chave da Anthropic inválida ou expirada. Checa ANTHROPIC_API_KEY "
            "no Railway (pode ter sido rotacionada sem atualizar aqui)."
        )

    if status == 403 or "permission" in error_type.lower():
        return f"Sem permissão na API Anthropic. Detalhe: {api_msg[:200] or error_type}"

    if status == 413 or "too_large" in error_type.lower():
        return (
            "A requisição ficou grande demais (histórico longo ou anexo pesado). "
            "Manda /reset pra limpar o histórico e tenta de novo com conteúdo menor."
        )

    if status == 429:
        return "Bati limite de rate na Anthropic. Aguenta ~30s e tenta de novo."

    if status and status < 500:
        return f"Erro da API Anthropic (status {status}): {api_msg[:200] or error_type}"

    if isinstance(e, anthropic.APITimeoutError):
        return "A API da Anthropic demorou demais pra responder. Tenta de novo em 1 min."

    if isinstance(e, anthropic.APIConnectionError):
        return "Não consegui conectar na API da Anthropic. Pode ser rede ou serviço fora. Tenta em 1 min."

    return f"Problema inesperado com a API Anthropic: {str(e)[:200]}"

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
    model = os.getenv("MODEL_RESUMO", "claude-haiku-4-5")

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


def _build_system_blocks(system_estavel: str, suffix_var: str) -> list[dict]:
    """Monta system como 2 blocos: estável (cacheado) + variável (fresh).

    O bloco estável é o conteúdo do system_prompt.md — não muda entre calls,
    cacheia por 5min via cache_control: ephemeral. Em chamadas subsequentes
    o custo cai pra 10% dos tokens cacheados (input).

    O bloco variável (data/hora atual + memórias relevantes) muda a cada call,
    fica fresh.
    """
    blocks = [
        {
            "type": "text",
            "text": system_estavel,
            "cache_control": {"type": "ephemeral"},
        }
    ]
    if suffix_var:
        blocks.append({"type": "text", "text": suffix_var})
    return blocks


def _build_tools_cached(tools: list[dict]) -> list[dict]:
    """Marca o último tool com cache_control — Anthropic cacheia toda a lista
    de tools até o ponto do cache_control. Tools são estáticas no projeto,
    então cache hit é praticamente garantido entre calls."""
    if not tools:
        return tools
    cached = list(tools)
    cached[-1] = {**cached[-1], "cache_control": {"type": "ephemeral"}}
    return cached


_TOOLS_CACHED = _build_tools_cached(TOOLS)


async def gerar_resposta(messages: list[dict], memory_context: str = "") -> tuple[str, dict]:
    model = os.getenv("MODEL_DEFAULT", "claude-sonnet-4-6")
    max_tokens = int(os.getenv("MAX_TOKENS_RESPONSE", "2048"))

    system_estavel = _load_system_prompt()
    agora = datetime.now(BRT)
    dia_semana = DIAS_SEMANA[agora.weekday()]
    suffix_var = (
        f"\n\n## Data e hora atuais\n"
        f"Hoje é {dia_semana}, {agora.strftime('%d/%m/%Y')}, {agora.strftime('%H:%M')} (horário de Brasília)."
    )
    if memory_context:
        suffix_var += f"\n\n## Memórias relevantes\n{memory_context}"

    system_blocks = _build_system_blocks(system_estavel, suffix_var)

    total_in = 0
    total_out = 0
    cache_creation = 0
    cache_read = 0
    current_messages = list(messages)
    max_tool_rounds = 10

    # Loop de tool calling — continua até Claude retornar texto final
    for _ in range(max_tool_rounds):
        try:
            response = await _chamar_claude_com_retry(
                model=model,
                max_tokens=max_tokens,
                system_prompt=system_blocks,
                messages=current_messages,
                tools=_TOOLS_CACHED,
            )
        except (anthropic.APIStatusError, anthropic.APIConnectionError, anthropic.APITimeoutError) as e:
            status = getattr(e, "status_code", None)
            pricing = _get_pricing(model)
            cost_input = (
                total_in * pricing["input"]
                + cache_creation * pricing["input"] * 1.25
                + cache_read * pricing["input"] * 0.10
            )
            cost_usd = round(cost_input + total_out * pricing["output"], 6)

            # 5xx/529 — sobrecarga, mensagem padrão
            if status in _STATUS_RETRY:
                texto = (
                    f"A API da IA tá sobrecarregada agora (status {status}). "
                    "Tentei várias vezes sem sucesso. Tenta de novo em 1-2 minutos."
                )
                err_label = f"api_overload_{status}"
            else:
                # 4xx ou erro de conexão — usa classificador específico
                texto = _mensagem_erro_amigavel(e)
                err_label = f"api_error_{status or 'conn'}"

            return texto, {
                "model": model, "tokens_in": total_in,
                "tokens_out": total_out, "cost_usd": cost_usd,
                "error": err_label
            }

        total_in += response.usage.input_tokens
        total_out += response.usage.output_tokens
        # Cache stats — só presentes se prompt caching estiver ativo
        cache_creation += getattr(response.usage, "cache_creation_input_tokens", 0) or 0
        cache_read += getattr(response.usage, "cache_read_input_tokens", 0) or 0

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
            # Custo: input fresh full + cache creation 25% extra + cache read 10%.
            # response.usage.input_tokens já EXCLUI cache_read e cache_creation,
            # então somamos separado.
            cost_input = (
                total_in * pricing["input"]
                + cache_creation * pricing["input"] * 1.25
                + cache_read * pricing["input"] * 0.10
            )
            cost_usd = round(cost_input + total_out * pricing["output"], 6)
            metadata = {
                "model": model,
                "tokens_in": total_in,
                "tokens_out": total_out,
                "cache_creation": cache_creation,
                "cache_read": cache_read,
                "cost_usd": cost_usd,
            }
            return text, metadata

    # Saída de segurança se o loop de tools esgotar
    pricing = _get_pricing(model)
    cost_input = (
        total_in * pricing["input"]
        + cache_creation * pricing["input"] * 1.25
        + cache_read * pricing["input"] * 0.10
    )
    cost_usd = round(cost_input + total_out * pricing["output"], 6)
    return "Desculpa, entrei em loop interno. Tenta reformular.", {
        "model": model, "tokens_in": total_in,
        "tokens_out": total_out,
        "cache_creation": cache_creation,
        "cache_read": cache_read,
        "cost_usd": cost_usd
    }
