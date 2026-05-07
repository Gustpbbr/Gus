"""Handler de mensagens de voz/áudio. Transcreve via Whisper e processa
como texto."""

import logging

from telegram import Update
from telegram.ext import ContextTypes

from gus.media import transcrever_audio

from gus import state
from gus.handlers.responder import _responder

logger = logging.getLogger(__name__)


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recebe voice message do Telegram, transcreve via Whisper e processa como texto."""
    chat_id = str(update.effective_chat.id)
    if not state._autorizado(chat_id):
        return
    if not await state._verificar_rate_limit(update, chat_id):
        return
    if not await state._verificar_limite(update):
        return

    voice = update.message.voice or update.message.audio
    if not voice:
        return

    duracao = getattr(voice, "duration", 0) or 0
    await update.message.reply_text(
        f"Transcrevendo áudio ({duracao}s)..." if duracao else "Transcrevendo áudio..."
    )

    try:
        file = await context.bot.get_file(voice.file_id)
        transcricao = await transcrever_audio(file.file_path)
    except Exception as e:
        logger.error(f"Erro baixando/transcrevendo áudio: {e}")
        await update.message.reply_text("Não consegui transcrever o áudio. Tenta de novo.")
        return

    if transcricao.startswith("("):
        # Prefixo "(...)" sinaliza erro da própria transcrição
        await update.message.reply_text(f"Problema na transcrição: {transcricao}")
        return

    # Responde com a transcrição + processa como texto
    await update.message.reply_text(f"Entendi: _{transcricao}_", parse_mode="Markdown")
    content = [{"type": "text", "text": transcricao}]
    await _responder(update, chat_id, content, transcricao)
