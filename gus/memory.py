import os
import asyncio
import logging
from mem0 import MemoryClient

logger = logging.getLogger(__name__)

USER_ID = "gustavo"
_client = None


def _get_client() -> MemoryClient:
    global _client
    if _client is None:
        api_key = os.getenv("MEM0_API_KEY")
        if not api_key:
            raise ValueError("MEM0_API_KEY não definido")
        _client = MemoryClient(api_key=api_key)
    return _client


async def buscar_memorias(query: str) -> str:
    """Busca memórias relevantes no Mem0 para o contexto da conversa."""
    client = _get_client()
    results = await asyncio.to_thread(
        client.search, query, user_id=USER_ID, limit=5
    )
    if not results:
        return ""
    lines = [f"- {r['memory']}" for r in results]
    return "\n".join(lines)


async def salvar_memorias(messages: list[dict]) -> None:
    """Salva o par user/assistant no Mem0 para memória futura."""
    client = _get_client()
    await asyncio.to_thread(
        client.add, messages, user_id=USER_ID
    )


async def buscar_memorias_detalhada(query: str, limit: int = 10) -> str:
    """Busca memórias no Mem0 com limite configurável, formatada pra retorno como tool."""
    try:
        client = _get_client()
        results = await asyncio.to_thread(
            client.search, query, user_id=USER_ID, limit=limit
        )
    except Exception as e:
        return f"Erro ao buscar no Mem0: {e}"

    if not results:
        return f"Nenhuma memória encontrada pra: `{query}`"

    linhas = [f"Encontradas {len(results)} memória(s) relevante(s) pra `{query}`:"]
    for i, r in enumerate(results, 1):
        mem = (r.get("memory") or "").strip()
        if mem:
            linhas.append(f"{i}. {mem}")
    return "\n".join(linhas)
