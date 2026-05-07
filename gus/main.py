import asyncio
import logging
import os

import uvicorn
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from api.server import create_app
from gus.bot import (
    handle_custo,
    handle_document,
    handle_foco,
    handle_message,
    handle_photo,
    handle_reset,
    handle_start,
    handle_voice,
)

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def run_bot() -> None:
    logger.info("=== Bot boot — build 2026-04-29T19:45 ===")
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN não definido.")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(CommandHandler("reset", handle_reset))
    app.add_handler(CommandHandler("custo", handle_custo))
    app.add_handler(CommandHandler("foco", handle_foco))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_voice))

    await app.initialize()
    await app.start()

    # Detecta updates pendentes ANTES de droppar (drop_pending_updates=True
    # descarta msgs em flight durante deploy sem deixar trace). Se houver,
    # avisa o Gustavo que algo pode ter sido perdido (D3=C decisão).
    pending_count = 0
    try:
        # peek no fim da fila — não confirma, só verifica se há algo
        peek = await app.bot.get_updates(offset=-1, limit=1, timeout=0)
        if peek:
            pending_count = peek[0].update_id  # heurística: ID alto = backlog real
            # Recolhe todas pendentes pra contar (até 100)
            todas = await app.bot.get_updates(offset=0, limit=100, timeout=0)
            pending_count = len(todas)
    except Exception as e:
        logger.warning(f"Não foi possível checar updates pendentes: {e}")

    await app.updater.start_polling(drop_pending_updates=True)
    logger.info(f"Bot Telegram iniciado. Pending dropped: {pending_count}")

    # Avisa o Gustavo que voltou online (e quantas msgs foram dropadas)
    chat_id_gustavo = os.getenv("TELEGRAM_CHAT_ID")
    if pending_count > 0 and chat_id_gustavo:
        try:
            plural = "msg" if pending_count == 1 else "msgs"
            await app.bot.send_message(
                chat_id=chat_id_gustavo,
                text=(
                    f"🔄 Voltei online após redeploy. "
                    f"{pending_count} {plural} durante o downtime "
                    f"foram descartadas — reenvia se foi importante."
                ),
            )
        except Exception as e:
            logger.warning(f"Falha ao avisar Gustavo do redeploy: {e}")

    # Mantém vivo até cancelamento externo (uvicorn ou SIGTERM).
    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        logger.info("Bot recebeu cancelamento — desligando…")
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


async def run_api() -> None:
    port = int(os.getenv("PORT", "8000"))
    api_app = create_app()
    config = uvicorn.Config(
        api_app,
        host="0.0.0.0",
        port=port,
        log_level="info",
        access_log=False,
    )
    server = uvicorn.Server(config)
    logger.info(f"API FastAPI iniciada em :{port}")
    await server.serve()


async def main_async() -> None:
    bot_task = asyncio.create_task(run_bot(), name="bot")
    api_task = asyncio.create_task(run_api(), name="api")

    done, pending = await asyncio.wait(
        {bot_task, api_task},
        return_when=asyncio.FIRST_EXCEPTION,
    )

    for task in pending:
        task.cancel()
    for task in pending:
        try:
            await task
        except asyncio.CancelledError:
            pass

    for task in done:
        if task.exception():
            raise task.exception()


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
