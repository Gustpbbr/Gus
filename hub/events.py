"""
Fila SSE pra broadcast de eventos do Hub Qdrant em tempo real.

Cada listener (cliente conectado em GET /hub/stream) tem sua própria
asyncio.Queue. broadcast(fragmento) empurra pra todas as filas; cada
listener consome a sua via subscribe(). Usado pelo NeuroGus pra ver
fragmentos novos nascerem no grafo em tempo real (gus-30, gus-30.1).

Fluxo:
    hub.store.ingestar() (thread sync via to_thread)
        └── broadcast_sync(payload)              ← thread-safe wrapper
                └── run_coroutine_threadsafe
                        └── broadcast(payload)   ← async, no loop principal
                                └── put_nowait em cada Queue
                                        └── subscribe() yield no /hub/stream

Decisões (gus-30 §7.5, gus-30.1 §4):
- Uma Queue por listener (não compartilhada) — listener lento não atrasa
  os outros. QueueFull descarta evento pra ele apenas.
- maxsize=100 — suficiente pra latência de UI (~1s/evento ≫ 100 eventos
  acumulados sem render).
- _loop_ref capturado lazy na 1ª subscribe — evita acoplamento com
  startup do FastAPI.
- Eventos perdidos se ninguém estiver conectado: ok, /hub/recent recarrega
  estado quando cliente conecta.
"""

import asyncio
import json
import logging
from typing import AsyncIterator

logger = logging.getLogger(__name__)

# Lista global de listeners. Cada um tem fila própria.
_listeners: list[asyncio.Queue] = []

# Referência ao event loop principal do FastAPI, capturada na 1ª subscribe.
# Usada por broadcast_sync (chamado de thread sync) pra agendar broadcast()
# coroutine no loop certo via run_coroutine_threadsafe.
_loop_ref: asyncio.AbstractEventLoop | None = None


async def broadcast(payload: dict) -> None:
    """Empurra payload pra todos os listeners conectados.

    Não-bloqueante por listener (put_nowait). Listener com fila cheia
    perde o evento; outros recebem normal.
    """
    if not _listeners:
        return

    serialized = json.dumps(payload, ensure_ascii=False, default=str)
    descartados = 0
    for q in list(_listeners):  # copy pra tolerar mutação durante iter
        try:
            q.put_nowait(serialized)
        except asyncio.QueueFull:
            descartados += 1

    if descartados:
        logger.warning(
            f"broadcast: {descartados}/{len(_listeners)} listener(s) "
            "com fila cheia — evento descartado pra eles"
        )


def broadcast_sync(payload: dict) -> None:
    """Versão sync de broadcast() — chamável de thread fora do loop.

    Usado por hub.store.ingestar (sync, rodado em to_thread). Se não
    houver listener ou o loop ainda não foi capturado, no-op silencioso.
    """
    if not _listeners or _loop_ref is None:
        return
    try:
        asyncio.run_coroutine_threadsafe(broadcast(payload), _loop_ref)
    except Exception:
        logger.exception("broadcast_sync: falha ao agendar broadcast")


async def subscribe() -> AsyncIterator[str]:
    """Inscreve um novo listener. Yield strings JSON conforme chegam.

    Usado por GET /hub/stream:

        async def stream():
            async for evento in subscribe():
                yield f"data: {evento}\\n\\n"

    Captura o event loop atual na 1ª chamada (assume rodando no loop
    principal do FastAPI). Limpa a fila ao desconectar.
    """
    global _loop_ref
    if _loop_ref is None:
        _loop_ref = asyncio.get_running_loop()

    q: asyncio.Queue = asyncio.Queue(maxsize=100)
    _listeners.append(q)
    logger.info(f"subscribe: novo listener (total: {len(_listeners)})")
    try:
        while True:
            payload = await q.get()
            yield payload
    finally:
        try:
            _listeners.remove(q)
        except ValueError:
            pass
        logger.info(f"subscribe: listener desconectado (restantes: {len(_listeners)})")


def listeners_count() -> int:
    """Helper de debug — quantos listeners conectados."""
    return len(_listeners)
