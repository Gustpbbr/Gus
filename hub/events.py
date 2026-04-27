"""
SSE broadcast para o NeuroGus — visualização em tempo real.

Cada cliente conectado em /hub/stream recebe uma Queue.
Quando hub.store.ingestar() salva um fragmento, chama broadcast()
que empurra o evento JSON pra todas as filas ativas.

Thread-safe via asyncio (broadcast roda na thread do event loop).
"""

import asyncio
import json
from typing import AsyncIterator

_subscribers: list[asyncio.Queue] = []


def subscribe() -> asyncio.Queue:
    q: asyncio.Queue = asyncio.Queue(maxsize=100)
    _subscribers.append(q)
    return q


def unsubscribe(q: asyncio.Queue) -> None:
    try:
        _subscribers.remove(q)
    except ValueError:
        pass


def broadcast(event_data: dict) -> None:
    """Chamado de código síncrono (hub.store). Empurra pra todas as filas ativas."""
    if not _subscribers:
        return
    payload = json.dumps(event_data, ensure_ascii=False, default=str)
    dead = []
    for q in _subscribers:
        try:
            q.put_nowait(payload)
        except asyncio.QueueFull:
            dead.append(q)
    for q in dead:
        unsubscribe(q)


async def event_stream(q: asyncio.Queue) -> AsyncIterator[str]:
    """Gerador SSE pra um cliente. Heartbeat a cada 25s pra não fechar conexão idle."""
    try:
        while True:
            try:
                payload = await asyncio.wait_for(q.get(), timeout=25.0)
                yield f"data: {payload}\n\n"
            except asyncio.TimeoutError:
                yield ": heartbeat\n\n"
    finally:
        unsubscribe(q)
