import os
import asyncio
import logging
from mem0 import Memory
from qdrant_client.models import PayloadSchemaType

logger = logging.getLogger(__name__)

# Dois "cérebros" no Hub:
# - USER_ID_GUSTAVO: memórias sobre o Gustavo (fatos, preferências, contexto pessoal)
# - USER_ID_GUS: autobiografia do próprio Gus (padrões operacionais, história do sistema)
USER_ID_GUSTAVO = "gustavo"
USER_ID_GUS = "gus"
USER_ID = USER_ID_GUSTAVO  # default retrocompatível

# Tag de origem default — identifica qual porta gerou essa memória.
# Lê env em cada call (em vez de cachear no import) — facilita testes e
# permite mudança runtime sem restart do processo.
def _via_default() -> str:
    return os.getenv("MEM0_VIA_TAG", "telegram-claude")


# Mantido como atributo do módulo pra compatibilidade com testes/imports
# que faziam `from gus.memory import VIA_DEFAULT`. Hoje resolvido via
# property-like — mas mantemos o nome legacy.
VIA_DEFAULT = _via_default()

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
                    "model": "claude-sonnet-4-6",
                    "api_key": anthropic_key,
                }
            },
            "embedder": {
                "provider": "huggingface",
                "config": {
                    "model": "sentence-transformers/all-MiniLM-L6-v2"
                }
            }
        })
        _ensure_indexes(_client)
    return _client


def _ensure_indexes(memory: Memory) -> None:
    """Cria índices de payload no Qdrant para os campos de filtro do mem0."""
    try:
        qdrant = memory.vector_store.client
        for field in ("user_id", "agent_id", "run_id"):
            try:
                qdrant.create_payload_index(
                    collection_name="gus",
                    field_name=field,
                    field_schema=PayloadSchemaType.KEYWORD,
                )
            except Exception:
                pass  # já existe — idempotente
    except Exception as e:
        logger.warning(f"Não foi possível criar índices Qdrant: {e}")


def _normalizar_results(raw) -> list:
    """Memory.search() retorna dict {"results": [...]} no self-hosted."""
    if isinstance(raw, dict):
        return raw.get("results", [])
    return raw or []


async def buscar_memorias(query: str, user_id: str = USER_ID_GUSTAVO) -> str:
    """Busca memórias relevantes para o contexto da conversa.

    ADR-001 Fase 3: tenta o Hub Qdrant ('gus_hub', schema rico) PRIMEIRO.
    Se o Hub não retornar nada útil ou der erro, fallback para a coleção
    Mem0 antiga ('gus' via mem0ai). Mantém comportamento atual como rede
    de segurança durante a transição.

    Após Fase 5 (aposentadoria do Mem0), o fallback é removido.
    """
    # 1) Tenta Hub Qdrant direto (rico, com filtros)
    try:
        from hub.store import lembrar as hub_lembrar
        hub_results = await asyncio.to_thread(
            hub_lembrar, query, user_id, 5
        )
        if hub_results:
            linhas = [f"- {r['conteudo']}" for r in hub_results if r.get("conteudo")]
            if linhas:
                logger.info(f"Memória servida pelo Hub ({len(linhas)} fragmentos)")
                return "\n".join(linhas)
    except Exception as e:
        logger.warning(f"Hub.lembrar falhou (cai pro fallback Mem0): {e}")

    # 2) Fallback: Mem0 wrapper antigo (coleção 'gus')
    try:
        client = _get_client()
        raw = await asyncio.to_thread(
            client.search, query, user_id=user_id, limit=5
        )
        results = _normalizar_results(raw)
        if not results:
            return ""
        lines = [f"- {r['memory']}" for r in results]
        logger.info(f"Memória servida pelo Mem0 (fallback, {len(lines)} fragmentos)")
        return "\n".join(lines)
    except Exception as e:
        logger.warning(f"Mem0 fallback também falhou: {e}")
        return ""


async def salvar_memorias(
    messages: list[dict],
    user_id: str = USER_ID_GUSTAVO,
    via: str | None = None,
) -> None:
    """Salva fragmentos no Hub Qdrant (gus_hub) com tag de origem.

    ADR-001 Fase 3: Hub primeiro. Antes escrevia no Mem0 SaaS via client.add,
    agora escreve direto no Hub via hub.store.ingestar — uma chamada por
    message não-vazia. Cada message vira um fragmento atômico.

    Sem fallback Mem0: o Mem0 SaaS está aposentado pelo ADR-001 e novas
    escritas iriam pra coleção morta (não retornaria erro mas o registro
    nunca seria lido por mais ninguém).

    Casos de uso:
    - /foco no Telegram (gus/bot.py:handle_foco) — salva [FOCO-ATUAL] ...
    - Fallback do _resumir_e_salvar quando curador híbrido falha
    - salvar_observacao_gus (brain user_id=gus)

    Args:
        messages: lista de {role, content} — só "content" string é aproveitado.
                  Para content como lista (multimodal), só blocos type=text contam.
        user_id: 'gustavo' (default) ou 'gus' (auto-observações).
        via: tag de origem ('telegram', 'claude-code', etc).
    """
    from hub.store import ingestar

    via_tag = via or _via_default()
    metadata = {
        "user_id": user_id,
        "via": via_tag,
        # Sem classificação automática (tipo/area/camada) — quem chama essa
        # função (handle_foco, fallback) não tem o LLM curador no caminho.
        # Default tipo=episodico, camada=sessao no schema do Hub.
    }

    for msg in messages:
        content = msg.get("content")
        if isinstance(content, str):
            texto = content.strip()
        elif isinstance(content, list):
            partes = [
                c.get("text", "")
                for c in content
                if isinstance(c, dict) and c.get("type") == "text"
            ]
            texto = " ".join(p for p in partes if p).strip()
        else:
            texto = ""

        if not texto:
            continue

        try:
            await asyncio.to_thread(ingestar, texto, metadata)
        except Exception as e:
            logger.warning(f"Hub.ingestar falhou em salvar_memorias (user_id={user_id}): {e}")


async def buscar_memorias_detalhada(query: str, limit: int = 10, user_id: str = USER_ID_GUSTAVO) -> str:
    """Busca memórias com limite configurável, incluindo ID para deleção.

    ADR-001 Fase 3: Hub Qdrant (gus_hub) primeiro. Fallback Mem0 só se Hub
    falhar (rede/auth). Após Fase 5, fallback removido.
    """
    # 1) Tenta Hub Qdrant
    try:
        from hub.store import lembrar as hub_lembrar
        hub_results = await asyncio.to_thread(
            hub_lembrar, query, user_id, limit
        )
        if hub_results:
            linhas = [f"Encontradas {len(hub_results)} memória(s) em `{user_id}` (Hub) pra `{query}`:"]
            for i, r in enumerate(hub_results, 1):
                conteudo = (r.get("conteudo") or "").strip()
                mem_id = r.get("id") or "?"
                tipo = r.get("tipo") or "?"
                area = r.get("area") or "-"
                if conteudo:
                    linhas.append(f"{i}. [{mem_id}] [{tipo}/{area}] {conteudo}")
            return "\n".join(linhas)
    except Exception as e:
        logger.warning(f"Hub.lembrar (detalhada) falhou — fallback Mem0: {e}")

    # 2) Fallback Mem0
    try:
        client = _get_client()
        raw = await asyncio.to_thread(
            client.search, query, user_id=user_id, limit=limit
        )
        results = _normalizar_results(raw)
    except Exception as e:
        return f"Erro ao buscar (Hub+Mem0) (user_id={user_id}): {e}"

    if not results:
        return f"Nenhuma memória encontrada pra `{query}` no brain `{user_id}`."

    linhas = [f"Encontradas {len(results)} memória(s) em `{user_id}` (Mem0 fallback) pra `{query}`:"]
    for i, r in enumerate(results, 1):
        mem = (r.get("memory") or "").strip()
        mem_id = r.get("id") or "?"
        if mem:
            linhas.append(f"{i}. [{mem_id}] {mem}")
    return "\n".join(linhas)


async def deletar_memoria(memory_id: str, user_id: str = USER_ID_GUSTAVO) -> str:
    """Deleta uma memória pelo ID. IRREVERSÍVEL.

    ADR-001 Fase 3: tenta Hub primeiro (UUID do gus_hub). Se ID não casar
    com formato Hub OU der erro, fallback Mem0 (formato próprio do SaaS).
    Cobre IDs históricos que ainda não foram migrados pro Hub.

    Args:
        memory_id: UUID (Hub) ou ID Mem0.
        user_id: 'gustavo' ou 'gus' — usado só pra mensagem amigável; Hub
                 e Mem0 deletam por ID, não filtram por user_id.
    """
    if not memory_id or not memory_id.strip():
        return "memory_id vazio, não dá pra deletar."
    mid = memory_id.strip()

    # 1) Tenta Hub Qdrant
    try:
        from hub.store import deletar as hub_deletar
        motivo = f"gus.memory.deletar_memoria user_id={user_id}"
        await asyncio.to_thread(hub_deletar, mid, motivo)
        return f"Memória `{mid}` deletada do Hub (user_id=`{user_id}`)."
    except Exception as e_hub:
        logger.warning(f"Hub.deletar falhou em '{mid}': {e_hub}. Tentando Mem0 fallback…")

    # 2) Fallback Mem0 (IDs históricos pré-migração)
    try:
        client = _get_client()
        await asyncio.to_thread(client.delete, memory_id=mid)
        return f"Memória `{mid}` deletada do Mem0 (fallback, user_id=`{user_id}`)."
    except Exception as e_mem0:
        return f"Erro ao deletar memória `{mid}` (Hub+Mem0): {e_mem0}"


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
        return f"Erro ao salvar (user_id=gus): {e}"


async def buscar_memorias_gus(query: str, limit: int = 10) -> str:
    """Busca nas memórias autobiográficas do Gus (brain `gus`)."""
    return await buscar_memorias_detalhada(query, limit=limit, user_id=USER_ID_GUS)
