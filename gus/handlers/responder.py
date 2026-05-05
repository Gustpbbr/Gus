"""
Lógica compartilhada de resposta — usada pelos handlers de texto, foto,
documento e voz.

`_responder` é o coração: monta history, busca memórias, chama o dispatcher
LLM (Anthropic/OpenAI), aplica scan PII no output, persiste state, dispara
curador a cada N turnos.

`_resumir_e_salvar` é fire-and-forget — chamado via asyncio.create_task pelo
`_responder`. Roda Haiku + GPT em paralelo via hub.curador, ambos salvam no
Hub Qdrant com mesmo hash_janela pra parear no Obsidian.
"""

import time
import asyncio
import logging

from telegram import Update

from gus.llm import gerar_resposta
from gus.logger import registrar
from gus.memory import buscar_memorias
from gus.resumo_log import append_resumo_async
from gus.patterns_sensiveis import redact as _redact_pii

from gus import state

logger = logging.getLogger(__name__)


def _redigir_resposta(resposta: str) -> tuple[str, list[str]]:
    """Aplica scan PII na resposta antes de mandar pro Telegram.

    Defesa em profundidade vs vazamento — o Sonnet/GPT pode incluir CPF,
    cartão, key etc. resumindo OS Dimagem ou processando arquivo. O
    `save_to_github` já tinha scan, mas a saída direta do bot não.

    Comportamento:
      - Substitui matches por `[REDIGIDO-<tipo>]`
      - Se houve redação, anexa nota visível ao Gustavo (transparência)
      - Logger já loga via warning no caller

    Retorna (resposta_redatada, lista_de_tipos_redatados).
    Se nada for redatado, resposta volta inalterada.
    """
    if not resposta:
        return resposta, []
    redatada, redatados = _redact_pii(resposta)
    if not redatados:
        return resposta, []
    tipos_unicos = sorted(set(redatados))
    nota = (
        f"\n\n_⚠️ {len(redatados)} dado(s) sensível(eis) redatado(s) "
        f"da resposta: {', '.join(tipos_unicos)}_"
    )
    return redatada + nota, redatados


def _texto_de_content(content) -> str:
    """Extrai as partes de texto de um content (str ou list multimodal)."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        partes = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                t = block.get("text", "")
                if t:
                    partes.append(t)
        return " ".join(partes).strip()
    return ""


def _query_mem0_contextual(history: list[dict], fallback: str) -> str:
    """Monta query do Mem0 a partir das últimas 3 mensagens do Gustavo.
    Ajuda a busca semântica quando a mensagem atual é curta ou referencial."""
    textos_user = []
    for msg in reversed(history):
        if msg.get("role") != "user":
            continue
        t = _texto_de_content(msg.get("content"))
        if t:
            textos_user.append(t)
        if len(textos_user) >= 3:
            break
    textos_user.reverse()
    return " ".join(textos_user) if textos_user else fallback


async def _resumir_e_salvar(chat_id: str, trecho: list[dict]) -> None:
    """Curadoria híbrida via Hub (Haiku + GPT em paralelo). Silencioso em falhas.

    Fluxo (Fase 2 do ADR-001):
      1. Tenta hub.curador.curar_turnos → roda Haiku e GPT em paralelo
         sobre o MESMO trecho. Cada modelo extrai fragmentos atômicos
         classificados (tipo, area, camada_temporal). Ambos salvam no
         Hub Qdrant (gus_hub) com metadata.curador distinta + mesmo
         hash_janela (permite parear pra comparação de qualidade).
      2. Loga UMA entrada por curador no _log/curador/AAAA-MM-DD.md
         (mesmo hash_janela visível no Obsidian → comparação lado a lado).
      3. Se hub.curador falhar globalmente (import error ou exceção fora
         do gather interno — i.e., AMBOS Anthropic e OpenAI offline ao
         mesmo tempo), loga `erro_curador_total` e segue. Item 1.6 do
         plano de saneamento removeu o `_fallback_mem0` antigo: gravar
         resumo bruto sem schema gus-18 polui o Hub mais do que
         resolve. Memória perdida em janela isolada vs. Hub
         contaminado: preferimos perder janela.

    Curador é fire-and-forget — chamado via asyncio.create_task em
    _responder. Nunca bloqueia resposta do bot.
    """
    try:
        from hub.curador import curar_turnos
        resultado = await curar_turnos(trecho, via="telegram-claude", user_id="gustavo")
    except Exception as e:
        # Falha total do curador — loga alto e segue. Janela perdida.
        logger.error(
            f"Curador (Hub) FALHA TOTAL (chat {chat_id}): {e}. "
            f"Janela de {len(trecho)} turnos perdida — sem fallback (item 1.6)."
        )
        append_resumo_async(
            f"(curador falhou totalmente: {str(e)[:120]})",
            len(trecho),
            status="erro_curador_total",
        )
        return

    hash_j = resultado.get("hash_janela", "")
    haiku_frags = resultado.get("haiku", [])
    gpt_frags = resultado.get("gpt", [])
    salvos = resultado.get("salvos", 0)
    erros = resultado.get("erros", [])

    # Loga 1 entrada por curador (mesmo hash → permite parear no Obsidian)
    for nome, frags in (("haiku", haiku_frags), ("gpt", gpt_frags)):
        if frags:
            texto = "\n".join(
                f"{i+1}. [{f.get('tipo', '?')}/{f.get('area', '-')}] {f.get('conteudo', '')}"
                for i, f in enumerate(frags)
            )
            append_resumo_async(
                texto, len(trecho), status="salvo",
                curador=nome, hash_janela=hash_j, num_fragmentos=len(frags),
            )
        else:
            append_resumo_async(
                "(sem fragmentos relevantes)", len(trecho), status="descartado",
                curador=nome, hash_janela=hash_j, num_fragmentos=0,
            )

    for err in erros:
        logger.warning(f"Curador erro parcial (chat {chat_id}): {err}")

    logger.info(
        f"Curador (chat {chat_id}): salvos={salvos} "
        f"haiku={len(haiku_frags)} gpt={len(gpt_frags)} hash={hash_j}"
    )


async def _responder(update: Update, chat_id: str, content: list[dict], texto_preview: str):
    """Envia content para o Claude e responde no Telegram."""
    history = state.conversation_histories.setdefault(chat_id, [])
    history.append({"role": "user", "content": content})

    if len(history) > state.MAX_HISTORY:
        history[:] = history[-state.MAX_HISTORY:]

    turn = state.turn_counters.get(chat_id, 0) + 1
    state.turn_counters[chat_id] = turn

    start = time.time()

    memory_context = ""
    try:
        # Query combina últimas 3 msgs do usuário + preview atual pra melhorar recall
        query = _query_mem0_contextual(history, texto_preview or "imagem ou documento")
        memory_context = await buscar_memorias(query)
    except Exception as mem_err:
        logger.warning(f"Mem0 search falhou: {mem_err}")

    try:
        resposta, metadata = await gerar_resposta(history, memory_context)
        latency = round(time.time() - start, 2)

        history.append({"role": "assistant", "content": resposta})

        # A cada TURNOS_PARA_RESUMO (default 3) turnos do usuário, gera resumo extrativo
        # do trecho recente e salva no Mem0 como memória curada.
        if turn - state.last_saved_turn.get(chat_id, 0) >= state.TURNOS_PARA_RESUMO:
            trecho = list(history[-(state.TURNOS_PARA_RESUMO * 2):])
            state.last_saved_turn[chat_id] = turn
            asyncio.create_task(_resumir_e_salvar(chat_id, trecho))

        # Scan PII no output antes de enviar — defesa em profundidade.
        resposta_envio, redatados = _redigir_resposta(resposta)
        if redatados:
            logger.warning(
                f"[PII-OUT] chat={chat_id} {len(redatados)} dado(s) "
                f"redatado(s): {sorted(set(redatados))}"
            )

        for i in range(0, len(resposta_envio), 4096):
            await update.message.reply_text(resposta_envio[i:i + 4096])

        # Tokens de cache: se cache_read > 0, prompt caching pegou e a economia
        # real foi maior que o cost_usd sugere (cost já reflete desconto).
        # cache_hit_ratio = leitura cache / (leitura cache + criação cache + input fresh)
        cache_read = metadata.get("cache_read", 0) or 0
        cache_creation = metadata.get("cache_creation", 0) or 0
        tokens_in = metadata.get("tokens_in", 0) or 0
        denom = cache_read + cache_creation + tokens_in
        cache_hit_ratio = round(cache_read / denom, 3) if denom > 0 else 0.0

        registrar(
            direction="out",
            text_preview=texto_preview[:80],
            latency_seconds=latency,
            model=metadata.get("model"),
            tokens_in=tokens_in,
            tokens_out=metadata.get("tokens_out"),
            cache_creation=cache_creation,
            cache_read=cache_read,
            cache_hit_ratio=cache_hit_ratio,
            cost_usd=metadata.get("cost_usd"),
            status="ok"
        )

        # Persiste state em disco (volume Railway /app/data/bot_state.json)
        # pra sobreviver a redeploys
        state._save_state()

    except Exception as e:
        history.pop()
        logger.error(f"Erro ao processar mensagem: {e}")
        await update.message.reply_text("Tive um problema interno. Tenta de novo em instantes.")
        registrar(direction="error", text_preview=str(e)[:80], status="error")
