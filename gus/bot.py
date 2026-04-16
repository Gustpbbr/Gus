import os
import time
import asyncio
import logging
from telegram import Update
from telegram.ext import ContextTypes
from gus.llm import gerar_resposta
from gus.logger import registrar, custo_mes_atual
from gus.memory import buscar_memorias, salvar_memorias
from gus.media import processar_imagem, processar_pdf

logger = logging.getLogger(__name__)

AUTHORIZED_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
HARD_LIMIT = float(os.getenv("HARD_LIMIT_USD_MONTH", "30"))
MAX_HISTORY = int(os.getenv("MAX_HISTORY_MESSAGES", "20"))  # 10 turnos

# Histórico em memória por chat_id (reseta no redeploy)
conversation_histories: dict[str, list] = {}


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


async def _responder(update: Update, chat_id: str, content: list[dict], texto_preview: str):
    """Envia content para o Claude e responde no Telegram."""
    history = conversation_histories.setdefault(chat_id, [])
    history.append({"role": "user", "content": content})

    if len(history) > MAX_HISTORY:
        history[:] = history[-MAX_HISTORY:]

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

        async def _salvar_com_log():
            try:
                await salvar_memorias([
                    {"role": "user", "content": texto_preview or "[mídia]"},
                    {"role": "assistant", "content": resposta}
                ])
            except Exception as e:
                logger.warning(f"Mem0 save falhou: {e}")

        asyncio.create_task(_salvar_com_log())

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


async def handle_reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    if not _autorizado(chat_id):
        return
    conversation_histories.pop(chat_id, None)
    await update.message.reply_text("Histórico limpo. Começando do zero.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    if not _autorizado(chat_id):
        logger.warning(f"Mensagem ignorada de chat_id não autorizado: {chat_id}")
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
    if not await _verificar_limite(update):
        return

    doc = update.message.document
    mime = doc.mime_type or ""

    if mime != "application/pdf":
        await update.message.reply_text("Por enquanto só processo PDFs. Áudio e outros formatos em breve.")
        return

    await update.message.reply_text("Processando PDF...")

    file = await context.bot.get_file(doc.file_id)
    caption = update.message.caption or ""

    try:
        content = await processar_pdf(file.file_path, caption)
        await _responder(update, chat_id, content, caption or f"[PDF: {doc.file_name}]")
    except Exception as e:
        logger.error(f"Erro ao processar PDF: {e}")
        await update.message.reply_text("Não consegui processar o PDF. Tenta de novo.")
