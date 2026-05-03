"""Handler de documentos (PDF, Word, Excel). Roteia por MIME + extensão."""

import logging

from telegram import Update
from telegram.ext import ContextTypes

from gus.media import processar_pdf, processar_docx, processar_xlsx

from gus import state
from gus.handlers.responder import _responder

logger = logging.getLogger(__name__)


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    if not state._autorizado(chat_id):
        return
    if not await state._verificar_rate_limit(update, chat_id):
        return
    if not await state._verificar_limite(update):
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
            f"Formato '{mime or nome}' ainda não suportado. "
            "Documentos ativos: PDF, Word (.docx), Excel (.xlsx). "
            "Mensagem de voz e arquivo de áudio funcionam direto. "
            "Vídeo ainda não tem handler."
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
