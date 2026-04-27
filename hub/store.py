"""
Hub Qdrant direto — store layer.

Implementa o schema rico definido em projetos/gus/gus-18-schema-indexacao.md
sem passar pelo wrapper Mem0. Embeddings gerados localmente via
sentence-transformers (mesma família 'all-MiniLM-L6-v2', dim=384, que
o mem0 self-hosted já usa — mantém compatibilidade futura para migração
de dados da coleção 'gus' para 'gus_hub').

Coleção: 'gus_hub' (paralela a 'gus' gerida pelo mem0).

Variáveis de ambiente:
    QDRANT_URL        — endpoint do cluster Qdrant Cloud
    QDRANT_API_KEY    — chave do cluster

Referências:
    - projetos/gus/gus-18-schema-indexacao.md (schema do payload)
    - projetos/gus/gus-20-etapa2-hub-qdrant.md (desenho desta etapa)
    - ADR-001 (decisão de aposentar Mem0)
"""

import os
import uuid
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, Filter, FieldCondition, MatchValue,
    PayloadSchemaType, PointStruct,
)
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

BRT = timezone(timedelta(hours=-3))

COLLECTION = "gus_hub"
EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBED_DIM = 384

_client: Optional[QdrantClient] = None
_embedder: Optional[SentenceTransformer] = None


def _get_client() -> QdrantClient:
    global _client
    if _client is None:
        url = os.environ.get("QDRANT_URL")
        key = os.environ.get("QDRANT_API_KEY")
        if not url or not key:
            raise ValueError("QDRANT_URL e QDRANT_API_KEY são obrigatórias para o Hub")
        _client = QdrantClient(url=url, api_key=key, timeout=30)
        _ensure_collection(_client)
        _ensure_indexes(_client)
    return _client


def _get_embedder() -> SentenceTransformer:
    global _embedder
    if _embedder is None:
        logger.info(f"Carregando embedder {EMBED_MODEL_NAME} (primeira call do Hub)…")
        _embedder = SentenceTransformer(EMBED_MODEL_NAME)
    return _embedder


def _ensure_collection(client: QdrantClient) -> None:
    """Cria a coleção gus_hub se não existir. Idempotente."""
    nomes = [c.name for c in client.get_collections().collections]
    if COLLECTION not in nomes:
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE),
        )
        logger.info(f"Coleção '{COLLECTION}' criada (dim={EMBED_DIM}, distance=cosine).")


def _ensure_indexes(client: QdrantClient) -> None:
    """Cria índices de payload nos campos usados em filtro. Idempotente."""
    campos = (
        "user_id", "tipo", "estado", "area", "via", "projeto",
        "tipo_esquecimento", "camada_temporal", "curador",
    )
    for field in campos:
        try:
            client.create_payload_index(
                collection_name=COLLECTION,
                field_name=field,
                field_schema=PayloadSchemaType.KEYWORD,
            )
        except Exception:
            pass  # já existe — silencioso


def _embed(texto: str) -> list[float]:
    return _get_embedder().encode(texto, convert_to_numpy=True).tolist()


def _filtros(user_id: str, tipo: Optional[str] = None,
             estado: Optional[str] = None, area: Optional[str] = None) -> Filter:
    must = [FieldCondition(key="user_id", match=MatchValue(value=user_id))]
    if tipo:
        must.append(FieldCondition(key="tipo", match=MatchValue(value=tipo)))
    if estado:
        must.append(FieldCondition(key="estado", match=MatchValue(value=estado)))
    if area:
        must.append(FieldCondition(key="area", match=MatchValue(value=area)))
    return Filter(must=must)


def ingestar(conteudo: str, metadata: dict) -> str:
    """
    Insere um fragmento no Hub. Retorna o UUID do fragmento.

    `metadata` aceita os campos de IngestarReq + extras opcionais que o
    Curador (Fase 2) preenche pra comparação Haiku × Sonnet:
      - curador:        'haiku' | 'sonnet'
      - hash_janela:    sha8 dos turnos/arquivo extraído
      - janela_turnos:  int — quantos turnos cobertos
    """
    if not conteudo or not conteudo.strip():
        raise ValueError("conteudo vazio")

    client = _get_client()
    now = datetime.now(BRT).isoformat()
    frag_id = str(uuid.uuid4())

    payload = {
        # Conteúdo + classificação (gus-18)
        "conteudo": conteudo,
        "tipo": metadata.get("tipo", "episodico"),
        "estado": "ativo",  # default no nascimento
        "camada_temporal": metadata.get("camada_temporal", "sessao"),
        "tipo_esquecimento": metadata.get("tipo_esquecimento"),
        # Lifecycle
        "peso": 0.5,
        "confirmacoes": 0,
        "confianca": float(metadata.get("confianca", 0.7)),
        "acessos": 0,
        # Origem e contexto
        "via": metadata.get("via", "api"),
        "area": metadata.get("area", ""),
        "projeto": metadata.get("projeto", ""),
        "user_id": metadata.get("user_id", "gustavo"),
        # Timestamps
        "criado_em": now,
        "ultimo_acesso": now,
    }

    # Campos extras do curador (preservados se vierem)
    for k in ("curador", "hash_janela", "janela_turnos"):
        if k in metadata:
            payload[k] = metadata[k]

    vetor = _embed(conteudo)
    client.upsert(
        collection_name=COLLECTION,
        points=[PointStruct(id=frag_id, vector=vetor, payload=payload)],
    )
    return frag_id


def lembrar(query: str, user_id: str = "gustavo", limit: int = 10,
            tipo: Optional[str] = None, estado: Optional[str] = "ativo",
            area: Optional[str] = None) -> list[dict]:
    """
    Busca semântica filtrada no Hub.

    Default `estado='ativo'` exclui fragmentos historicos/esquecidos.
    Passe `estado=None` para incluir todos.
    """
    client = _get_client()
    vetor = _embed(query)

    resultado = client.query_points(
        collection_name=COLLECTION,
        query=vetor,
        query_filter=_filtros(user_id, tipo, estado, area),
        limit=limit,
        with_payload=True,
    )

    return [
        {
            "id": str(p.id),
            "conteudo": (p.payload or {}).get("conteudo", ""),
            "score": p.score,
            "tipo": (p.payload or {}).get("tipo"),
            "estado": (p.payload or {}).get("estado"),
            "via": (p.payload or {}).get("via"),
            "area": (p.payload or {}).get("area"),
            "criado_em": (p.payload or {}).get("criado_em"),
            "curador": (p.payload or {}).get("curador"),
        }
        for p in resultado.points
    ]


def ego_cache(user_id: str = "gustavo") -> dict:
    """
    Retorna fragmentos prioritários para injeção em system prompt.

    Implementa parcialmente gus-22 (Etapa 4 — Ego Cache). Auto-relato
    narrativo (Etapa 5) fica para sessão futura.
    """
    client = _get_client()

    def _scroll(tipo: str, estado: Optional[str] = None, limit: int = 10) -> list[dict]:
        flt = _filtros(user_id, tipo=tipo, estado=estado)
        pontos, _ = client.scroll(
            collection_name=COLLECTION,
            scroll_filter=flt,
            limit=limit,
            with_payload=True,
        )
        return [(p.payload or {}) for p in pontos]

    return {
        "identidade": _scroll("identidade_operacional", estado="estavel"),
        "protegidos": _scroll("procedural", estado="estavel"),
        "decisoes_recentes": _scroll("decisao", limit=3),
        "meta_reflexoes": _scroll("meta_reflexao", limit=5),
    }


def contar(user_id: str = "gustavo") -> int:
    """Conta fragmentos do user_id."""
    client = _get_client()
    return client.count(
        collection_name=COLLECTION,
        count_filter=_filtros(user_id),
    ).count


def listar(user_id: str = "gustavo", limit: int = 50) -> list[dict]:
    """Lista fragmentos do user_id (sem busca semântica). Retorna até `limit`.

    Usado pelo MCP `mem0-gus` em listar_memorias / listar_memorias_gus
    quando o usuário quer ver tudo (não fazer query específica).
    """
    client = _get_client()
    pontos, _ = client.scroll(
        collection_name=COLLECTION,
        scroll_filter=_filtros(user_id),
        limit=limit,
        with_payload=True,
        with_vectors=False,
    )
    return [
        {
            "id": str(p.id),
            "conteudo": (p.payload or {}).get("conteudo", ""),
            "tipo": (p.payload or {}).get("tipo"),
            "estado": (p.payload or {}).get("estado"),
            "via": (p.payload or {}).get("via"),
            "area": (p.payload or {}).get("area"),
            "criado_em": (p.payload or {}).get("criado_em"),
            "curador": (p.payload or {}).get("curador"),
        }
        for p in pontos
    ]


def deletar(memory_id: str) -> bool:
    """Deleta um fragmento pelo ID. IRREVERSÍVEL.

    Usado pelo MCP `mem0-gus` em deletar_memoria. O caller é responsável
    por confirmar a intenção antes de chamar.
    """
    if not memory_id or not memory_id.strip():
        raise ValueError("memory_id vazio")
    client = _get_client()
    client.delete(
        collection_name=COLLECTION,
        points_selector=[memory_id.strip()],
    )
    return True


def stats() -> dict:
    """Stats agregados da coleção. Útil pra dashboard / debug."""
    client = _get_client()
    info = client.get_collection(collection_name=COLLECTION)
    total_gustavo = contar("gustavo")
    total_gus = contar("gus")
    return {
        "colecao": COLLECTION,
        "vectors_count": info.vectors_count,
        "points_count": info.points_count,
        "status": info.status,
        "user_id_gustavo": total_gustavo,
        "user_id_gus": total_gus,
    }
