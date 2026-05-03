import os
import json
import asyncio
import logging
import functools
import anthropic
from openai import AsyncOpenAI
from datetime import datetime, timezone, timedelta
from pathlib import Path
from gus.tools import TOOLS, executar_tool

logger = logging.getLogger(__name__)

BRT = timezone(timedelta(hours=-3))
DIAS_SEMANA = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]

# Erros de servidor Anthropic que valem retry
_STATUS_RETRY = {500, 502, 503, 504, 529}

# Preços por família de modelo (USD por token) — atualizado abr/2026
# Anthropic: por família (substring match no nome do modelo)
# OpenAI:    chave exata pra evitar match parcial (gpt-4o-mini é mais barato que gpt-4o)
MODEL_PRICING = {
    "opus":         {"input":  5.0  / 1_000_000, "output": 25.0 / 1_000_000},
    "sonnet":       {"input":  3.0  / 1_000_000, "output": 15.0 / 1_000_000},
    "haiku":        {"input":  0.8  / 1_000_000, "output":  4.0 / 1_000_000},
    "gpt-4o-mini":  {"input":  0.15 / 1_000_000, "output":  0.60 / 1_000_000},
    "gpt-4o":       {"input":  2.5  / 1_000_000, "output": 10.0 / 1_000_000},
}
FALLBACK_PRICING = MODEL_PRICING["sonnet"]


def _get_pricing(model: str) -> dict:
    """Retorna pricing baseado no nome do modelo. Match exato pra gpt-* (mini
    vs full diferem 16x) e substring pras famílias Anthropic."""
    model_lower = model.lower()
    # OpenAI: prefer exact match (gpt-4o-mini antes de gpt-4o)
    if model_lower in MODEL_PRICING:
        return MODEL_PRICING[model_lower]
    for family, pricing in MODEL_PRICING.items():
        if family in model_lower:
            return pricing
    return FALLBACK_PRICING

client = anthropic.AsyncAnthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    timeout=120.0,  # 2 minutos — evita ficar pendurado se a API travar
)

# OpenAI client é lazy: AsyncOpenAI explode em __init__ se OPENAI_API_KEY
# ausente, o que quebrava import de hub.curador (transitivamente importa
# gus.llm) em workflows que não usam OpenAI mas ainda assim importam o módulo.
# Inicialização sob demanda mantém imports seguros.
_openai_client: AsyncOpenAI | None = None


def _get_openai_client() -> AsyncOpenAI:
    global _openai_client
    if _openai_client is None:
        _openai_client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            timeout=120.0,
        )
    return _openai_client


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
                    "messages": messages,
                }
                # Só inclui `system` se tiver conteúdo. system="" disparou bug
                # 400 'temperature and top_p cannot both be specified' em
                # chamadas Sonnet 4.6 sem tools (curador errava 100% do dia
                # 27/04/2026). Defesa em profundidade — chamadas com system
                # bem-formado seguem normais.
                if system_prompt:
                    kwargs["system"] = system_prompt
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

# NOTA: gerar_resumo_turnos + RESUMO_SYSTEM_PROMPT removidos no item 1.6 do
# plano de saneamento (02/05/2026). Eram usados pelo `_fallback_mem0` legado
# em gus/bot.py — quando o curador híbrido falhava totalmente, gerava resumo
# bruto sem schema gus-18 e gravava no Hub. Decisão: preferir perder a janela
# (alta visibilidade via status=erro_curador_total) a poluir Hub com fragmentos
# não-classificados. Curador híbrido cross-vendor (Anthropic + OpenAI) já é
# resiliente — ambos caírem simultaneamente é cenário extremo que merece
# alerta, não fallback silencioso.


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


# Tool âncora pra cache_control. Anthropic cacheia toda a lista de tools até
# o ponto marcado — pra cachear TODAS, marcamos a última. Mas "última por
# posição" é frágil se alguém reordenar TOOLS sem perceber. Buscar por nome
# estável (anchor) é mais robusto: se anchor sumir, cai no último por fallback.
_CACHE_ANCHOR_NAME = "rotear_arquivo"


def _build_tools_cached(tools: list[dict]) -> list[dict]:
    """Marca a tool âncora (ou último por fallback) com cache_control.

    Anthropic cacheia toda a lista até a posição marcada. Como queremos
    cachear todas, marcamos a anchor que por convenção é a última. Se
    alguém reordenar e a anchor virar do meio, log warn (cache hit cai)
    e cacheia até ela — melhor que cacheamento errado silencioso.
    """
    if not tools:
        return tools
    cached = list(tools)
    anchor_idx = next(
        (i for i, t in enumerate(cached) if t.get("name") == _CACHE_ANCHOR_NAME),
        len(cached) - 1,
    )
    if anchor_idx != len(cached) - 1:
        logger.warning(
            f"_CACHE_ANCHOR '{_CACHE_ANCHOR_NAME}' não está no final da lista "
            f"(idx={anchor_idx}/{len(cached)-1}). Cache hit pode estar reduzido."
        )
    cached[anchor_idx] = {**cached[anchor_idx], "cache_control": {"type": "ephemeral"}}
    return cached


_TOOLS_CACHED = _build_tools_cached(TOOLS)


async def _gerar_resposta_anthropic(messages: list[dict], memory_context: str = "") -> tuple[str, dict]:
    """Implementação Anthropic da geração de resposta — loop tool-calling com
    prompt caching e retry/fallback. Comportamento legado pré-gus-29; agora
    chamada via dispatcher quando content tem image/document ou
    MULTIMODEL_ENABLED=false."""
    model = os.getenv("MODEL_DEFAULT", "claude-sonnet-4-6")
    max_tokens = int(os.getenv("MAX_TOKENS_RESPONSE", "2048"))

    system_estavel = _load_system_prompt()
    agora = datetime.now(BRT)
    dia_semana = DIAS_SEMANA[agora.weekday()]
    suffix_var = (
        f"\n\n## Modelo atual\n"
        f"Esta resposta está sendo gerada por **{model}** (Anthropic). "
        f"Quando perguntado qual modelo, diga isso — não invente. "
        f"O sistema rotea automaticamente entre Anthropic e OpenAI conforme o tipo de mensagem.\n\n"
        f"## Data e hora atuais\n"
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


# ---------------------------------------------------------------------------
# OpenAI path (gus-29 Fase 1) — texto/áudio via gpt-4o-mini
# ---------------------------------------------------------------------------


def _anthropic_to_openai_tools(tools: list[dict]) -> list[dict]:
    """Converte tools do formato Anthropic (`{name, description, input_schema}`)
    pro formato OpenAI (`{type: function, function: {name, description, parameters}}`).
    JSON Schema do `parameters` é o mesmo `input_schema`."""
    return [
        {
            "type": "function",
            "function": {
                "name": t["name"],
                "description": t.get("description", ""),
                "parameters": t.get("input_schema", {"type": "object", "properties": {}}),
            },
        }
        for t in tools
    ]


_TOOLS_OPENAI = _anthropic_to_openai_tools(TOOLS)


def _history_to_openai(messages: list[dict]) -> list[dict]:
    """Converte history do formato bot.py (Anthropic-style) pra OpenAI.

    bot.py mantém:
      - user: content é lista de blocos `[{type: "text", text: "..."}]` ou string
      - assistant: content é string (resposta final do turno anterior)

    OpenAI espera content como string simples nas mensagens persistidas.
    Tool calls do turno corrente NUNCA persistem em history (só o texto
    final), então não precisamos converter tool_use/tool_result aqui.
    """
    out = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if isinstance(content, list):
            partes = []
            for block in content:
                if isinstance(block, dict):
                    if block.get("type") == "text":
                        partes.append(block.get("text", ""))
                    # blocos image/document deveriam mandar pra Anthropic via
                    # dispatcher — mas se chegou aqui, ignora (descreve)
                    elif block.get("type") == "image":
                        partes.append("[imagem anexada]")
                    elif block.get("type") == "document":
                        partes.append("[documento anexado]")
            content_str = " ".join(p for p in partes if p).strip() or "[mídia sem texto]"
        else:
            content_str = str(content) if content is not None else ""
        out.append({"role": role, "content": content_str})
    return out


def _mensagem_erro_amigavel_openai(e: Exception) -> str:
    """Converte erro da API OpenAI em mensagem clara em português pro Gustavo."""
    status = getattr(e, "status_code", None) or getattr(e, "code", None)
    msg = str(e).lower()

    if "insufficient_quota" in msg or "quota" in msg or "billing" in msg:
        return (
            "A conta OpenAI tá sem créditos ou com problema de billing. "
            "Pra voltar, o Gustavo precisa adicionar saldo em platform.openai.com/account/billing."
        )
    if status == 401 or "authentication" in msg or "invalid_api_key" in msg:
        return "Chave OpenAI inválida ou expirada. Checa OPENAI_API_KEY no Railway."
    if status == 403 or "permission" in msg:
        return f"Sem permissão na API OpenAI: {str(e)[:200]}"
    if status == 429:
        return "Bati limite de rate na OpenAI. Aguenta ~30s e tenta de novo."
    if status and isinstance(status, int) and status >= 500:
        return f"Erro de servidor OpenAI (status {status}). Tenta de novo em 1 min."
    return f"Problema inesperado com a API OpenAI: {str(e)[:200]}"


async def _gerar_resposta_openai(messages: list[dict], memory_context: str = "") -> tuple[str, dict]:
    """Implementação OpenAI da geração de resposta — loop tool-calling
    espelhando o caminho Anthropic.

    Comportamento:
      - System prompt: concatena system_prompt.md + data/hora + memórias
        em string única (OpenAI faz prompt caching automático em ≥1024 tokens).
      - Tools: schema convertido pra formato OpenAI, mesma execução via
        `executar_tool(name, inputs)`.
      - Fallback: se OpenAI falhar (rate, billing, 5xx), tenta Anthropic
        Sonnet pra manter bot respondendo.

    Custo: gpt-4o-mini é ~20x mais barato que Sonnet em texto.
    """
    model = os.getenv("MODEL_OPENAI_DEFAULT", "gpt-4o-mini")
    max_tokens = int(os.getenv("MAX_TOKENS_RESPONSE", "2048"))

    # Monta system prompt como string única (OpenAI cacheia auto em ≥1024 tok)
    system_estavel = _load_system_prompt()
    agora = datetime.now(BRT)
    dia_semana = DIAS_SEMANA[agora.weekday()]
    suffix_var = (
        f"\n\n## Modelo atual\n"
        f"Esta resposta está sendo gerada por **{model}** (OpenAI). "
        f"Quando perguntado qual modelo, diga isso — não invente. "
        f"O sistema rotea automaticamente entre Anthropic e OpenAI conforme o tipo de mensagem.\n\n"
        f"## Data e hora atuais\n"
        f"Hoje é {dia_semana}, {agora.strftime('%d/%m/%Y')}, {agora.strftime('%H:%M')} (horário de Brasília)."
    )
    if memory_context:
        suffix_var += f"\n\n## Memórias relevantes\n{memory_context}"
    system_prompt = system_estavel + suffix_var

    # History em formato OpenAI
    current_messages = [{"role": "system", "content": system_prompt}] + _history_to_openai(messages)

    total_in = 0
    total_out = 0
    cached_tokens = 0
    max_tool_rounds = 10

    for _ in range(max_tool_rounds):
        try:
            response = await _get_openai_client().chat.completions.create(
                model=model,
                max_tokens=max_tokens,
                messages=current_messages,
                tools=_TOOLS_OPENAI,
                tool_choice="auto",
            )
        except Exception as e:
            logger.error(f"OpenAI erro: {e}")
            # Fallback pra Anthropic se OpenAI falhar — mantém bot respondendo
            try:
                logger.info("Fallback OpenAI → Anthropic")
                return await _gerar_resposta_anthropic(messages, memory_context)
            except Exception as e2:
                logger.error(f"Fallback Anthropic também falhou: {e2}")
                pricing = _get_pricing(model)
                cost_usd = round(total_in * pricing["input"] + total_out * pricing["output"], 6)
                # Mensagem combina origem + fallback pro Gustavo entender que
                # ambos os providers falharam (não só um).
                texto_openai = _mensagem_erro_amigavel_openai(e)
                texto_anthropic = _mensagem_erro_amigavel(e2) if isinstance(
                    e2, (anthropic.APIStatusError, anthropic.APIConnectionError, anthropic.APITimeoutError)
                ) else f"Anthropic também falhou: {str(e2)[:200]}"
                texto = (
                    f"Os dois providers falharam.\n\n"
                    f"OpenAI (primeiro): {texto_openai}\n\n"
                    f"Anthropic (fallback): {texto_anthropic}"
                )
                return texto, {
                    "model": model, "tokens_in": total_in,
                    "tokens_out": total_out, "cost_usd": cost_usd,
                    "error": "openai_failed_anthropic_failed",
                }

        usage = response.usage
        total_in += usage.prompt_tokens or 0
        total_out += usage.completion_tokens or 0
        # OpenAI prompt caching automático (≥1024 tokens) — exposto em
        # usage.prompt_tokens_details.cached_tokens. Conta separado pra
        # cost tracking (cached é 50% do preço de input fresh).
        details = getattr(usage, "prompt_tokens_details", None)
        if details:
            cached_tokens += getattr(details, "cached_tokens", 0) or 0

        choice = response.choices[0]
        msg = choice.message

        if choice.finish_reason == "tool_calls" and msg.tool_calls:
            # Adiciona assistant turn com tool_calls
            current_messages.append({
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in msg.tool_calls
                ],
            })
            # Executa tools
            for tc in msg.tool_calls:
                try:
                    inputs = json.loads(tc.function.arguments) if tc.function.arguments else {}
                except json.JSONDecodeError:
                    inputs = {}
                result = await executar_tool(tc.function.name, inputs)
                current_messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result if isinstance(result, str) else str(result),
                })
            continue

        # Resposta final em texto
        text = msg.content or ""
        pricing = _get_pricing(model)
        # Cached tokens pagam ~50% (gpt-4o-mini): $0.075/M vs $0.15/M
        fresh_in = total_in - cached_tokens
        cost_input = fresh_in * pricing["input"] + cached_tokens * pricing["input"] * 0.5
        cost_usd = round(cost_input + total_out * pricing["output"], 6)
        metadata = {
            "model": model,
            "tokens_in": total_in,
            "tokens_out": total_out,
            "cache_creation": 0,  # OpenAI não distingue cache_creation
            "cache_read": cached_tokens,
            "cost_usd": cost_usd,
            "provider": "openai",
        }
        return text, metadata

    # Loop esgotou
    pricing = _get_pricing(model)
    fresh_in = total_in - cached_tokens
    cost_input = fresh_in * pricing["input"] + cached_tokens * pricing["input"] * 0.5
    cost_usd = round(cost_input + total_out * pricing["output"], 6)
    return "Desculpa, entrei em loop interno. Tenta reformular.", {
        "model": model, "tokens_in": total_in,
        "tokens_out": total_out,
        "cache_creation": 0,
        "cache_read": cached_tokens,
        "cost_usd": cost_usd,
        "provider": "openai",
    }


# ---------------------------------------------------------------------------
# Dispatcher (gus-29) — escolhe provider baseado no content type
# ---------------------------------------------------------------------------


def _escolher_provider(messages: list[dict]) -> tuple[str, str]:
    """Escolhe provider baseado no último user message.

    - texto puro             → openai (gpt-4o-mini, ~20x mais barato)
    - imagem ou document     → anthropic (Sonnet, mantém qualidade Vision/PDF)
    - MULTIMODEL_ENABLED=false → anthropic (rollback flag)

    Retorna (provider, motivo) onde provider ∈ {'openai', 'anthropic'}
    e motivo é descrição curta pra log.
    """
    if os.getenv("MULTIMODEL_ENABLED", "true").lower() != "true":
        return "anthropic", "MULTIMODEL_ENABLED=false (rollback flag)"

    # Procura último user message no history
    for msg in reversed(messages):
        if msg.get("role") != "user":
            continue
        content = msg.get("content", "")
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict):
                    btype = block.get("type")
                    if btype == "image":
                        return "anthropic", "content: image"
                    if btype == "document":
                        return "anthropic", "content: document"
        # Achou user message text-only — para a busca
        break
    return "openai", "content: text"


async def gerar_resposta(messages: list[dict], memory_context: str = "") -> tuple[str, dict]:
    """Dispatcher do gus-29: escolhe provider conforme content type do último
    turno do user e delega pra implementação Anthropic ou OpenAI.

    Retorno é compatível entre os dois caminhos: `(text, metadata)` onde
    metadata sempre contém model/tokens_in/tokens_out/cost_usd. O campo
    `provider` é adicionado no path OpenAI (omitido no Anthropic).
    """
    provider, motivo = _escolher_provider(messages)
    if provider == "openai":
        modelo = os.getenv("MODEL_OPENAI_DEFAULT", "gpt-4o-mini")
        logger.info(f"Routing → openai ({modelo}) | {motivo}")
        return await _gerar_resposta_openai(messages, memory_context)
    modelo = os.getenv("MODEL_DEFAULT", "claude-sonnet-4-6")
    logger.info(f"Routing → anthropic ({modelo}) | {motivo}")
    return await _gerar_resposta_anthropic(messages, memory_context)
