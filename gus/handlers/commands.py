"""Comandos do bot (/start, /custo, /foco, /reset)."""

import asyncio
import logging

from telegram import Update
from telegram.ext import ContextTypes

from gus.logger import stats_mes_atual
from gus.memory import salvar_memorias

from gus import state
from gus.handlers.responder import _resumir_e_salvar

logger = logging.getLogger(__name__)


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    if state._autorizado(chat_id):
        await update.message.reply_text("Oi, Gus online e pronto.")
    elif not state.AUTHORIZED_CHAT_ID:
        # Primeiro uso — mostra chat_id pra configurar
        await update.message.reply_text(
            f"Seu chat\\_id é: `{chat_id}`\n\n"
            f"Configure TELEGRAM\\_CHAT\\_ID no Railway com esse número "
            f"e faça redeploy.",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("Bot privado.")


async def handle_custo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    if not state._autorizado(chat_id):
        return
    s = stats_mes_atual()
    total = s["cost_usd"]
    pct = 100 * total / state.HARD_LIMIT if state.HARD_LIMIT > 0 else 0

    # Cache hit ratio agregado do mês
    cache_total = s["cache_creation"] + s["cache_read"] + s["tokens_in"]
    hit_ratio = (s["cache_read"] / cache_total * 100) if cache_total > 0 else 0

    msg = (
        f"*Custo do mês:* US${total:.4f} de US${state.HARD_LIMIT:.2f} ({pct:.1f}%)\n"
        f"*Calls:* {s['calls']}\n"
        f"*Tokens:* {s['tokens_in']:,} in / {s['tokens_out']:,} out\n"
        f"*Cache:* {s['cache_read']:,} read + {s['cache_creation']:,} created "
        f"(hit ratio {hit_ratio:.1f}%)\n\n"
        f"_Obs: tracking reseta em redeploy se /app/data não tiver volume persistente._"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


async def _limpar_focos_antigos() -> int:
    """Deleta fragmentos com [FOCO-ATUAL] no brain `gustavo` antes de salvar
    foco novo. Sem isso, /foco empilha — busca semântica retorna múltiplos
    "foco atual" da mesma pessoa, vira ruído.

    Retorna número de fragmentos deletados (0 se nada).
    """
    try:
        from hub.store import lembrar as hub_lembrar, deletar as hub_deletar
    except Exception as e:
        logger.warning(f"Não consegui importar hub.store pra limpar focos: {e}")
        return 0

    try:
        antigos = await asyncio.to_thread(hub_lembrar, "[FOCO-ATUAL]", "gustavo", 20)
    except Exception as e:
        logger.warning(f"Falha ao buscar focos antigos: {e}")
        return 0

    deletados = 0
    for ant in antigos:
        conteudo = (ant.get("conteudo") or "")
        if "[FOCO-ATUAL]" not in conteudo:
            continue  # filtro semântico pode trazer fragmentos relacionados
        mid = ant.get("id")
        if not mid:
            continue
        try:
            await asyncio.to_thread(hub_deletar, mid, "/foco substituicao")
            deletados += 1
        except Exception as e:
            logger.warning(f"Falha ao deletar foco antigo {mid}: {e}")
    return deletados


async def handle_foco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Registra foco atual da sessão no Hub. Uso: /foco <descrição livre>

    Antes de salvar o novo, deleta FOCO-ATUAL existentes (TTL via substituição
    explícita). Sem isso, múltiplos /foco poluem busca semântica.
    """
    chat_id = str(update.effective_chat.id)
    if not state._autorizado(chat_id):
        return

    texto = update.message.text.removeprefix("/foco").strip()
    if not texto:
        await update.message.reply_text(
            "Pra definir o foco da sessão, usa: `/foco estou trabalhando em X`\n\n"
            "Isso vira uma memória prioritária no Hub e serve de contexto nas próximas sessões. "
            "Foco novo substitui o anterior.",
            parse_mode="Markdown"
        )
        return

    try:
        deletados = await _limpar_focos_antigos()
        await salvar_memorias([
            {"role": "user", "content": f"[FOCO-ATUAL] {texto}"}
        ])
        nota_subs = (
            f"\n_(substituiu {deletados} foco(s) anterior(es))_" if deletados else ""
        )
        await update.message.reply_text(
            f"Foco registrado: _{texto}_{nota_subs}\n\n"
            f"Vou priorizar esse contexto nas próximas interações.",
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.warning(f"Falha ao salvar foco: {e}")
        await update.message.reply_text("Não consegui registrar o foco agora. Tenta de novo em instantes.")


async def handle_reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    if not state._autorizado(chat_id):
        return

    # Se houve turnos desde o último resumo, salva o que acumulou antes de zerar
    turn = state.turn_counters.get(chat_id, 0)
    if turn > state.last_saved_turn.get(chat_id, 0):
        trecho = list(state.conversation_histories.get(chat_id, []))
        if trecho:
            asyncio.create_task(_resumir_e_salvar(chat_id, trecho))

    state.conversation_histories.pop(chat_id, None)
    state.turn_counters.pop(chat_id, None)
    state.last_saved_turn.pop(chat_id, None)
    state.message_timestamps.pop(chat_id, None)
    state._save_state()  # persiste o reset
    await update.message.reply_text("Histórico limpo. Começando do zero.")
