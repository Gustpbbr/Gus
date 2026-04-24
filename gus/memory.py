import os
import asyncio
import logging
from mem0 import MemoryClient

logger = logging.getLogger(__name__)

# Dois "cérebros" no Mem0:
# - USER_ID_GUSTAVO: memórias sobre o Gustavo (fatos, preferências, contexto pessoal)
# - USER_ID_GUS: memórias do próprio Gus (padrões operacionais, aprendizados sobre si)
USER_ID_GUSTAVO = "gustavo"
USER_ID_GUS = "gus"
USER_ID = USER_ID_GUSTAVO  # default retrocompatível

_client = None


def _get_client() -> MemoryClient:
    global _client
    if _client is None:
        api_key = os.getenv("MEM0_API_KEY")
        if not api_key:
            raise ValueError("MEM0_API_KEY não definido")
        _client = MemoryClient(api_key=api_key)
    return _client


async def buscar_memorias(query: str, user_id: str = USER_ID_GUSTAVO) -> str:
    """Busca memórias relevantes no Mem0 para o contexto da conversa."""
    client = _get_client()
    results = await asyncio.to_thread(
        client.search, query, user_id=user_id, limit=5
    )
    if not results:
        return ""
    lines = [f"- {r['memory']}" for r in results]
    return "\n".join(lines)


async def salvar_memorias(messages: list[dict], user_id: str = USER_ID_GUSTAVO) -> None:
    """Salva o par user/assistant no Mem0 para memória futura."""
    client = _get_client()
    await asyncio.to_thread(
        client.add, messages, user_id=user_id
    )


async def buscar_memorias_detalhada(query: str, limit: int = 10, user_id: str = USER_ID_GUSTAVO) -> str:
    """Busca memórias no Mem0 com limite configurável, formatada pra retorno como tool."""
    try:
        client = _get_client()
        results = await asyncio.to_thread(
            client.search, query, user_id=user_id, limit=limit
        )
    except Exception as e:
        return f"Erro ao buscar no Mem0 (user_id={user_id}): {e}"

    if not results:
        return f"Nenhuma memória encontrada pra `{query}` no brain `{user_id}`."

    linhas = [f"Encontradas {len(results)} memória(s) em `{user_id}` pra `{query}`:"]
    for i, r in enumerate(results, 1):
        mem = (r.get("memory") or "").strip()
        if mem:
            linhas.append(f"{i}. {mem}")
    return "\n".join(linhas)


async def salvar_observacao_gus(observacao: str) -> str:
    """Salva uma observação do próprio Gus sobre si ou padrões operacionais."""
    if not observacao or not observacao.strip():
        return "Observação vazia, não salvei."
    try:
        await salvar_memorias(
            [{"role": "user", "content": observacao.strip()}],
            user_id=USER_ID_GUS,
        )
        return f"Observação salva no brain `gus` do Mem0: \"{observacao[:80]}\""
    except Exception as e:
        return f"Erro ao salvar no Mem0 (user_id=gus): {e}"


async def buscar_memorias_gus(query: str, limit: int = 10) -> str:
    """Busca nas memórias próprias do Gus (Mem0 user_id='gus')."""
    return await buscar_memorias_detalhada(query, limit=limit, user_id=USER_ID_GUS)
