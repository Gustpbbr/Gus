import os
import asyncio
import logging
from mem0 import Memory

logger = logging.getLogger(__name__)

# Dois "cérebros" no Hub:
# - USER_ID_GUSTAVO: memórias sobre o Gustavo (fatos, preferências, contexto pessoal)
# - USER_ID_GUS: autobiografia do próprio Gus (padrões operacionais, história do sistema)
USER_ID_GUSTAVO = "gustavo"
USER_ID_GUS = "gus"
USER_ID = USER_ID_GUSTAVO  # default retrocompatível

# Tag de origem default — identifica qual porta gerou essa memória.
VIA_DEFAULT = os.getenv("MEM0_VIA_TAG", "telegram-claude")

_client = None


def _get_client() -> Memory:
    global _client
    if _client is None:
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_key = os.getenv("QDRANT_API_KEY")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if not qdrant_url or not qdrant_key:
            raise ValueError("QDRANT_URL e QDRANT_API_KEY não definidos")
        _client = Memory.from_config({
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "url": qdrant_url,
                    "api_key": qdrant_key,
                    "collection_name": "gus",
                }
            },
            "llm": {
                "provider": "anthropic",
                "config": {
                    "model": "claude-haiku-4-5-20251001",
                    "api_key": anthropic_key,
                }
            },
            "embedder": {
                "provider": "fastembed",
                "config": {
                    "model": "BAAI/bge-small-en-v1.5"
                }
            }
        })
    return _client


def _normalizar_results(raw) -> list:
    """Memory.search() retorna dict {"results": [...]} no self-hosted."""
    if isinstance(raw, dict):
        return raw.get("results", [])
    return raw or []


async def buscar_memorias(query: str, user_id: str = USER_ID_GUSTAVO) -> str:
    """Busca memórias relevantes para o contexto da conversa."""
    client = _get_client()
    raw = await asyncio.to_thread(
        client.search, query, user_id=user_id, limit=5
    )
    results = _normalizar_results(raw)
    if not results:
        return ""
    lines = [f"- {r['memory']}" for r in results]
    return "\n".join(lines)


async def salvar_memorias(
    messages: list[dict],
    user_id: str = USER_ID_GUSTAVO,
    via: str | None = None,
) -> None:
    """Salva o par user/assistant para memória futura com tag de origem."""
    client = _get_client()
    metadata = {"via": via or VIA_DEFAULT}
    await asyncio.to_thread(
        client.add, messages, user_id=user_id, metadata=metadata
    )


async def buscar_memorias_detalhada(query: str, limit: int = 10, user_id: str = USER_ID_GUSTAVO) -> str:
    """Busca memórias com limite configurável, incluindo ID para deleção."""
    try:
        client = _get_client()
        raw = await asyncio.to_thread(
            client.search, query, user_id=user_id, limit=limit
        )
        results = _normalizar_results(raw)
    except Exception as e:
        return f"Erro ao buscar no Mem0 (user_id={user_id}): {e}"

    if not results:
        return f"Nenhuma memória encontrada pra `{query}` no brain `{user_id}`."

    linhas = [f"Encontradas {len(results)} memória(s) em `{user_id}` pra `{query}`:"]
    for i, r in enumerate(results, 1):
        mem = (r.get("memory") or "").strip()
        mem_id = r.get("id") or "?"
        if mem:
            linhas.append(f"{i}. [{mem_id}] {mem}")
    return "\n".join(linhas)


async def deletar_memoria(memory_id: str, user_id: str = USER_ID_GUSTAVO) -> str:
    """Deleta uma memória pelo ID. IRREVERSÍVEL."""
    if not memory_id or not memory_id.strip():
        return "memory_id vazio, não dá pra deletar."
    try:
        client = _get_client()
        await asyncio.to_thread(client.delete, memory_id=memory_id.strip())
        return f"Memória `{memory_id}` deletada do brain `{user_id}`."
    except Exception as e:
        return f"Erro ao deletar memória `{memory_id}`: {e}"


async def salvar_observacao_gus(observacao: str, via: str | None = None) -> str:
    """Salva uma observação autobiográfica do Gus (brain `gus`)."""
    if not observacao or not observacao.strip():
        return "Observação vazia, não salvei."
    try:
        await salvar_memorias(
            [{"role": "user", "content": observacao.strip()}],
            user_id=USER_ID_GUS,
            via=via,
        )
        return f"Observação salva no brain `gus`: \"{observacao[:80]}\""
    except Exception as e:
        return f"Erro ao salvar no Mem0 (user_id=gus): {e}"


async def buscar_memorias_gus(query: str, limit: int = 10) -> str:
    """Busca nas memórias autobiográficas do Gus (brain `gus`)."""
    return await buscar_memorias_detalhada(query, limit=limit, user_id=USER_ID_GUS)
