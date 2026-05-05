"""Handler de mensagens de texto. Inclui interceptação do fluxo Dimagem
(confirmação de OS pendente)."""

import logging

from telegram import Update
from telegram.ext import ContextTypes

from gus.integrations.dimagem import salvar_os_dimagem

from gus import state
from gus.handlers.responder import _responder

logger = logging.getLogger(__name__)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    if not state._autorizado(chat_id):
        logger.warning(f"Mensagem ignorada de chat_id não autorizado: {chat_id}")
        return
    if not await state._verificar_rate_limit(update, chat_id):
        return
    if not await state._verificar_limite(update):
        return

    texto = update.message.text or ""

    # Se há OS dimagem pendente de confirmação, intercepta antes do Sonnet
    pending = state.dimagem_pending.get(chat_id)
    if pending:
        if state.DIMAGEM_CONFIRMA_RE.match(texto):
            del state.dimagem_pending[chat_id]
            state._save_state()
            try:
                resultado = await salvar_os_dimagem(pending)
            except Exception as e:
                logger.error(f"Erro ao salvar OS confirmada: {e}")
                resultado = f"Erro ao salvar: {str(e)[:200]}"
            await update.message.reply_text(resultado)
            return
        if state.DIMAGEM_CANCELA_RE.match(texto):
            del state.dimagem_pending[chat_id]
            state._save_state()
            await update.message.reply_text("OS cancelada — não salvei.")
            return
        # Mensagem que não é confirmação nem cancelamento → expira o pending
        # e segue pro fluxo Sonnet (Gustavo mudou de assunto).
        del state.dimagem_pending[chat_id]
        state._save_state()
        await update.message.reply_text("(OS pendente expirada — você falou de outro assunto.)")

    content = [{"type": "text", "text": texto}]
    await _responder(update, chat_id, content, texto)
