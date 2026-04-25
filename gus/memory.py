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

# Tag de origem default — identifica que porta gerou essa memória.
# Outras portas usam: 'telegram-gpt', 'claude-code', 'alexa', 'custom-gpt',
# 'carro-audio'. Permite filtrar por origem em search se quiser comparar
# perspectivas, mas search default vê TUDO (visibilidade cruzada).
# Veja projetos/gus/gus-12-portas-futuras.md.
VIA_DEFAULT = os.getenv("MEM0_VIA_TAG", "telegram-claude")

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


async def salvar_memorias(
    messages: list[dict],
    user_id: str = USER_ID_GUSTAVO,
    via: str | None = None,
) -> None:
    """Salva o par user/assistant no Mem0 para memória futura.

    Adiciona metadata `via` em cada memória pra rastrear qual porta gerou
    (telegram-claude, telegram-gpt, claude-code, alexa, etc.). Search
    default ignora o filtro — todas as portas veem todas as memórias.
    """
    client = _get_client()
    metadata = {"via": via or VIA_DEFAULT}
    await asyncio.to_thread(
        client.add, messages, user_id=user_id, metadata=metadata
    )


async def buscar_memorias_detalhada(query: str, limit: int = 10, user_id: str = USER_ID_GUSTAVO) -> str:
    """Busca memórias no Mem0 com limite configurável, formatada pra retorno como tool.

    Inclui o `id` de cada memória pra facilitar uso de `deletar_memoria` em
    seguida (Gustavo escolhe qual ID confirmar).
    """
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
        mem_id = r.get("id") or "?"
        if mem:
            linhas.append(f"{i}. [{mem_id}] {mem}")
    return "\n".join(linhas)


async def deletar_memoria(memory_id: str, user_id: str = USER_ID_GUSTAVO) -> str:
    """Deleta uma memória do Mem0 pelo ID. IRREVERSÍVEL.

    Use só após confirmação explícita do Gustavo. O ID vem do
    `buscar_memorias_detalhada` (formatado como `[id] texto`).
    """
    if not memory_id or not memory_id.strip():
        return "memory_id vazio, não dá pra deletar."

    try:
        client = _get_client()
        await asyncio.to_thread(client.delete, memory_id=memory_id.strip())
        return f"Memória `{memory_id}` deletada do brain `{user_id}`."
    except Exception as e:
        return f"Erro ao deletar memória `{memory_id}`: {e}"


async def salvar_observacao_gus(observacao: str, via: str | None = None) -> str:
    """Salva uma observação do próprio Gus sobre si ou padrões operacionais."""
    if not observacao or not observacao.strip():
        return "Observação vazia, não salvei."
    try:
        await salvar_memorias(
            [{"role": "user", "content": observacao.strip()}],
            user_id=USER_ID_GUS,
            via=via,
        )
        return f"Observação salva no brain `gus` do Mem0: \"{observacao[:80]}\""
    except Exception as e:
        return f"Erro ao salvar no Mem0 (user_id=gus): {e}"


async def buscar_memorias_gus(query: str, limit: int = 10) -> str:
    """Busca nas memórias próprias do Gus (Mem0 user_id='gus')."""
    return await buscar_memorias_detalhada(query, limit=limit, user_id=USER_ID_GUS)
