"""Handler de fotos. Inclui fluxo Dimagem (extração de OS via Haiku Vision
com gate de confiança no OCR)."""

import logging

import httpx
from telegram import Update
from telegram.ext import ContextTypes

from gus.media import processar_imagem
from gus.integrations.dimagem import analisar_os_dimagem

from gus import state
from gus.handlers.responder import _responder

logger = logging.getLogger(__name__)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    if not state._autorizado(chat_id):
        return
    if not await state._verificar_rate_limit(update, chat_id):
        return
    if not await state._verificar_limite(update):
        return

    await update.message.reply_text("Processando imagem...")

    photo = update.message.photo[-1]  # maior resolução disponível
    file = await context.bot.get_file(photo.file_id)
    caption = update.message.caption or ""

    # Fluxo dimagem (modo confirmação prévia): se foto é OS Dimagem, extrai
    # via Haiku, mostra preview com lista atual + nova linha, espera 'sim'
    # do Gustavo. Se não for OS ou extração falhar, cai no fluxo Sonnet.
    try:
        async with httpx.AsyncClient(timeout=30) as _c:
            _img_resp = await _c.get(file.file_path)
        if _img_resp.status_code == 200:
            _preview = await analisar_os_dimagem(_img_resp.content, caption)
            if _preview:
                # Confiança baixa do OCR -> não cria pending, só pede reenvio.
                # Sem state = sem chance de confirmar por engano nome trocado.
                if _preview.get("pedir_reenvio"):
                    await update.message.reply_text(_preview["preview_text"])
                    return
                state.dimagem_pending[chat_id] = _preview
                state._save_state()
                await update.message.reply_text(_preview["preview_text"])
                return
    except Exception as _dim_err:
        logger.warning(f"Fluxo dimagem falhou ({_dim_err}); caindo pro Sonnet.")

    try:
        content = await processar_imagem(file.file_path, caption)
        await _responder(update, chat_id, content, caption or "[imagem]")
    except Exception as e:
        logger.error(f"Erro ao processar imagem: {e}")
        await update.message.reply_text("Não consegui processar a imagem. Tenta de novo.")
