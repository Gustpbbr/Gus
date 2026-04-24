import os
import time
import asyncio
import logging
from collections import deque
from telegram import Update
from telegram.ext import ContextTypes
from gus.llm import gerar_resposta, gerar_resumo_turnos
from gus.logger import registrar, custo_mes_atual
from gus.memory import buscar_memorias, salvar_memorias
from gus.media import processar_imagem, processar_pdf, processar_docx, processar_xlsx

logger = logging.getLogger(__name__)

AUTHORIZED_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
HARD_LIMIT = float(os.getenv("HARD_LIMIT_USD_MONTH", "30"))
MAX_HISTORY = int(os.getenv("MAX_HISTORY_MESSAGES", "20"))  # 10 turnos
TURNOS_PARA_RESUMO = int(os.getenv("TURNOS_PARA_RESUMO", "5"))
RATE_LIMIT_MSG_PER_MINUTE = int(os.getenv("RATE_LIMIT_MSG_PER_MINUTE", "20"))

# Estado em memória por chat_id (reseta no redeploy)
conversation_histories: dict[str, list] = {}
turn_counters: dict[str, int] = {}
last_saved_turn: dict[str, int] = {}
message_timestamps: dict[str, deque] = {}


async def _resumir_e_salvar(chat_id: str, trecho: list[dict]) -> None:
    """Gera resumo extrativo do trecho e salva no Mem0. Silencioso em falhas."""
    try:
        resumo = await gerar_resumo_turnos(trecho)
        if resumo and resumo.strip().lower() != "sem conteúdo relevante":
            await salvar_memorias([{"role": "user", "content": resumo}])
            logger.info(f"Resumo salvo no Mem0 (chat {chat_id}, {len(resumo)} chars)")
        else:
            logger.info(f"Resumo vazio ou sem conteúdo relevante (chat {chat_id})")
    except Exception as e:
        logger.warning(f"Resumo falhou (chat {chat_id}): {e}")


def _autorizado(chat_id: str) -> bool:
    if not AUTHORIZED_CHAT_ID:
        return False  # nega tudo até configurar TELEGRAM_CHAT_ID
    return chat_id == AUTHORIZED_CHAT_ID


async def _verificar_limite(update: Update) -> bool:
    custo_atual = custo_mes_atual()
    if custo_atual >= HARD_LIMIT:
        await update.message.reply_text(
            f"Atingi o limite mensal de US${HARD_LIMIT:.0f}. "
            f"Desligando chamadas até o próximo mês."
        )
        return False
    return True


async def _verificar_rate_limit(update: Update, chat_id: str) -> bool:
    """Rate limit: até RATE_LIMIT_MSG_PER_MINUTE por janela de 60s."""
    agora = time.time()
    timestamps = message_timestamps.setdefault(chat_id, deque())
    while timestamps and timestamps[0] < agora - 60:
        timestamps.popleft()
    if len(timestamps) >= RATE_LIMIT_MSG_PER_MINUTE:
        await update.message.reply_text(
            f"Tô recebendo muito rápido ({len(timestamps)}+ msgs no último minuto). "
            f"Aguenta uns segundos e manda de novo."
        )
        return False
    timestamps.append(agora)
    return True


async def _responder(update: Update, chat_id: str, content: list[dict], texto_preview: str):
    """Envia content para o Claude e responde no Telegram."""
    history = conversation_histories.setdefault(chat_id, [])
    history.append({"role": "user", "content": content})

    if len(history) > MAX_HISTORY:
        history[:] = history[-MAX_HISTORY:]

    turn = turn_counters.get(chat_id, 0) + 1
    turn_counters[chat_id] = turn

    start = time.time()

    memory_context = ""
    try:
        query = texto_preview if texto_preview else "imagem ou documento enviado"
        memory_context = await buscar_memorias(query)
    except Exception as mem_err:
        logger.warning(f"Mem0 search falhou: {mem_err}")

    try:
        resposta, metadata = await gerar_resposta(history, memory_context)
        latency = round(time.time() - start, 2)

        history.append({"role": "assistant", "content": resposta})

        # A cada TURNOS_PARA_RESUMO (default 5) turnos do usuário, gera resumo extrativo
        # do trecho recente e salva no Mem0 como memória curada.
        if turn - last_saved_turn.get(chat_id, 0) >= TURNOS_PARA_RESUMO:
            trecho = list(history[-(TURNOS_PARA_RESUMO * 2):])
            last_saved_turn[chat_id] = turn
            asyncio.create_task(_resumir_e_salvar(chat_id, trecho))

        for i in range(0, len(resposta), 4096):
            await update.message.reply_text(resposta[i:i + 4096])

        registrar(
            direction="out",
            text_preview=texto_preview[:80],
            latency_seconds=latency,
            model=metadata.get("model"),
            tokens_in=metadata.get("tokens_in"),
            tokens_out=metadata.get("tokens_out"),
            cost_usd=metadata.get("cost_usd"),
            status="ok"
        )

    except Exception as e:
        history.pop()
        logger.error(f"Erro ao processar mensagem: {e}")
        await update.message.reply_text("Tive um problema interno. Tenta de novo em instantes.")
        registrar(direction="error", text_preview=str(e)[:80], status="error")


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    if _autorizado(chat_id):
        await update.message.reply_text("Oi, Gus online e pronto.")
    elif not AUTHORIZED_CHAT_ID:
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
    if not _autorizado(chat_id):
        return
    total = custo_mes_atual()
    pct = 100 * total / HARD_LIMIT if HARD_LIMIT > 0 else 0
    await update.message.reply_text(
        f"Custo do mês atual: US${total:.4f} de US${HARD_LIMIT:.2f} ({pct:.1f}%).\n\n"
        f"Obs: tracking reseta em cada redeploy do Railway. "
        f"Pra histórico confiável precisa de volume persistente em /app/logs."
    )


async def handle_reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    if not _autorizado(chat_id):
        return

    # Se houve turnos desde o último resumo, salva o que acumulou antes de zerar
    turn = turn_counters.get(chat_id, 0)
    if turn > last_saved_turn.get(chat_id, 0):
        trecho = list(conversation_histories.get(chat_id, []))
        if trecho:
            asyncio.create_task(_resumir_e_salvar(chat_id, trecho))

    conversation_histories.pop(chat_id, None)
    turn_counters.pop(chat_id, None)
    last_saved_turn.pop(chat_id, None)
    await update.message.reply_text("Histórico limpo. Começando do zero.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    if not _autorizado(chat_id):
        logger.warning(f"Mensagem ignorada de chat_id não autorizado: {chat_id}")
        return
    if not await _verificar_rate_limit(update, chat_id):
        return
    if not await _verificar_limite(update):
        return

    texto = update.message.text
    content = [{"type": "text", "text": texto}]
    await _responder(update, chat_id, content, texto)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    if not _autorizado(chat_id):
        return
    if not await _verificar_rate_limit(update, chat_id):
        return
    if not await _verificar_limite(update):
        return

    await update.message.reply_text("Processando imagem...")

    photo = update.message.photo[-1]  # maior resolução disponível
    file = await context.bot.get_file(photo.file_id)
    caption = update.message.caption or ""

    try:
        content = await processar_imagem(file.file_path, caption)
        await _responder(update, chat_id, content, caption or "[imagem]")
    except Exception as e:
        logger.error(f"Erro ao processar imagem: {e}")
        await update.message.reply_text("Não consegui processar a imagem. Tenta de novo.")


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    if not _autorizado(chat_id):
        return
    if not await _verificar_rate_limit(update, chat_id):
        return
    if not await _verificar_limite(update):
        return

    doc = update.message.document
    mime = doc.mime_type or ""
    nome = (doc.file_name or "arquivo").lower()

    # Roteador por MIME + extensão (fallback)
    if mime == "application/pdf" or nome.endswith(".pdf"):
        processador = processar_pdf
        label = "PDF"
    elif (
        "wordprocessingml" in mime
        or mime == "application/msword"
        or nome.endswith(".docx")
        or nome.endswith(".doc")
    ):
        processador = processar_docx
        label = "Word"
    elif (
        "spreadsheetml" in mime
        or mime == "application/vnd.ms-excel"
        or nome.endswith(".xlsx")
        or nome.endswith(".xls")
    ):
        processador = processar_xlsx
        label = "Excel"
    else:
        await update.message.reply_text(
            f"Formato '{mime or nome}' ainda não suportado. Formatos ativos: PDF, Word (.docx), Excel (.xlsx). "
            "Áudio e vídeo em breve."
        )
        return

    await update.message.reply_text(f"Processando {label}...")

    file = await context.bot.get_file(doc.file_id)
    caption = update.message.caption or ""

    try:
        content = await processador(file.file_path, caption)
        await _responder(update, chat_id, content, caption or f"[{label}: {doc.file_name}]")
    except Exception as e:
        logger.error(f"Erro ao processar {label}: {e}")
        await update.message.reply_text(f"Não consegui processar o {label}. Tenta de novo ou envia em outro formato.")
