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

from hub.events import broadcast_sync

logger = logging.getLogger(__name__)

BRT = timezone(timedelta(hours=-3))

COLLECTION = "gus_hub"
EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBED_DIM = 384

_client: Optional[QdrantClient] = None
_embedder = None  # type: Optional["SentenceTransformer"] — lazy import (boot leve)


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


def _get_embedder():
    """Lazy import: sentence_transformers puxa torch (~500MB). Importar no
    top-level estouraria RAM em containers pequenos no boot, mesmo sem chamar
    nada. Importamos só quando a 1ª busca/ingest acontecer."""
    global _embedder
    if _embedder is None:
        logger.info(f"Carregando embedder {EMBED_MODEL_NAME} (primeira call do Hub)…")
        from sentence_transformers import SentenceTransformer
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
    for k in ("curador", "hash_janela", "janela_turnos", "prompt_version"):
        if k in metadata:
            payload[k] = metadata[k]

    vetor = _embed(conteudo)
    client.upsert(
        collection_name=COLLECTION,
        points=[PointStruct(id=frag_id, vector=vetor, payload=payload)],
    )

    # Pós-ingest: calcula top-K vizinhos por afinidade semântica e popula
    # 'relacionados' no payload. Usado pelo NeuroGus pra desenhar arestas
    # (gus-30.1 §1, K=3, threshold=0.6).
    try:
        vizinhos = _calcular_vizinhos(
            vetor, k=3, threshold=0.6,
            exclude_id=frag_id, user_id=payload["user_id"],
        )
        if vizinhos:
            client.set_payload(
                collection_name=COLLECTION,
                payload={"relacionados": vizinhos},
                points=[frag_id],
            )
            payload["relacionados"] = vizinhos
    except Exception:
        logger.exception("ingestar: cálculo de vizinhos falhou (não-fatal)")

    # Broadcast SSE pro NeuroGus. No-op se ninguém estiver conectado.
    try:
        broadcast_sync({
            "id": frag_id,
            "conteudo": conteudo,
            "tipo": payload["tipo"],
            "estado": payload["estado"],
            "confianca": payload["confianca"],
            "user_id": payload["user_id"],
            "via": payload["via"],
            "area": payload["area"],
            "criado_em": payload["criado_em"],
            "relacionados": payload.get("relacionados", []),
            "curador": payload.get("curador"),
        })
    except Exception:
        logger.exception("ingestar: broadcast SSE falhou (não-fatal)")

    return frag_id


def _calcular_vizinhos(vetor: list[float], k: int = 3, threshold: float = 0.6,
                       exclude_id: Optional[str] = None,
                       user_id: str = "gustavo") -> list[str]:
    """Top-K vizinhos por cosine similarity, filtrando o próprio nó.

    Usado pelo ingestar() pra popular 'relacionados' no payload — o NeuroGus
    desenha arestas entre fragmentos com afinidade semântica >= threshold
    (gus-30.1 §1).

    Retorna lista de IDs (strings). Vazia se não houver vizinhos acima
    do threshold ou se a coleção ainda for muito pequena.
    """
    client = _get_client()
    # Busca k+1 pra excluir o próprio depois (sem usar id_filter, mais
    # robusto que assumir que o próprio sempre é o top-1)
    pontos = client.query_points(
        collection_name=COLLECTION,
        query=vetor,
        query_filter=Filter(must=[
            FieldCondition(key="user_id", match=MatchValue(value=user_id)),
        ]),
        limit=k + 1,
        with_payload=False,
    ).points

    return [
        str(p.id) for p in pontos
        if p.score is not None and p.score >= threshold
        and (exclude_id is None or str(p.id) != exclude_id)
    ][:k]


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

    Retorna o **payload completo** mais um campo `id` derivado do point ID.
    Antes do fix de 2026-05-04, esta função filtrava só 7 campos
    (conteudo, tipo, estado, via, area, criado_em, curador) — o que
    deixava `meta_relatorio_hub` e `auditoria_hub` cegos pra
    `camada_temporal`, `prompt_version`, `confianca`,
    `tipo_esquecimento`, `hash_janela` e outros campos que o curador
    grava normalmente. Resultado: 100% dos relatórios mostravam esses
    campos como `(sem)` mesmo quando o Hub estava populando direito.
    """
    client = _get_client()
    pontos, _ = client.scroll(
        collection_name=COLLECTION,
        scroll_filter=_filtros(user_id),
        limit=limit,
        with_payload=True,
        with_vectors=False,
    )
    out: list[dict] = []
    for p in pontos:
        payload = dict(p.payload or {})
        payload["id"] = str(p.id)
        out.append(payload)
    return out


def deletar(memory_id: str, motivo: Optional[str] = None) -> bool:
    """Deleta um fragmento pelo ID. IRREVERSÍVEL.

    Usado pelo MCP `mem0-gus` em deletar_memoria. O caller é responsável
    por confirmar a intenção antes de chamar.

    Antes de deletar, fetcha o payload e grava trilha em
    `_log/deletar-hub/AAAA-MM-DD.jsonl` (item 1.3 do plano de saneamento).
    Se o log falhar, o delete prossegue (fail-soft) — não bloquear delete
    por problema de I/O.
    """
    import json as _json
    from pathlib import Path as _Path

    if not memory_id or not memory_id.strip():
        raise ValueError("memory_id vazio")
    mid = memory_id.strip()
    client = _get_client()

    # Fetch payload pré-delete pra trilha de auditoria
    snapshot = None
    try:
        pontos = client.retrieve(
            collection_name=COLLECTION,
            ids=[mid],
            with_payload=True,
            with_vectors=False,
        )
        if pontos:
            snapshot = dict(pontos[0].payload or {})
    except Exception as e:
        logger.warning(f"deletar: fetch pré-delete falhou (id={mid[:8]}): {e}")

    # Trilha de auditoria — fail-soft
    try:
        log_dir = _Path("_log/deletar-hub")
        log_dir.mkdir(parents=True, exist_ok=True)
        hoje = datetime.now(BRT).strftime("%Y-%m-%d")
        log_path = log_dir / f"{hoje}.jsonl"
        registro = {
            "timestamp": datetime.now(BRT).isoformat(),
            "memory_id": mid,
            "motivo": motivo or "(não informado)",
            "snapshot": snapshot,
        }
        with log_path.open("a", encoding="utf-8") as f:
            f.write(_json.dumps(registro, ensure_ascii=False, default=str) + "\n")
    except Exception as e:
        logger.warning(f"deletar: trilha de auditoria falhou (id={mid[:8]}): {e}")

    # Delete propriamente dito
    client.delete(
        collection_name=COLLECTION,
        points_selector=[mid],
    )
    return True


def esquecer(memory_id: str, tipo_esquecimento: str = "deliberado") -> bool:
    """Soft delete: marca estado='esquecido' + tipo_esquecimento.

    Reversível via re_lembrar(). Fragmento some das buscas semânticas
    (lembrar() filtra estado='ativo' por default) mas continua no Qdrant
    como substrato de retro-aprendizado (gus-30.1 §3).

    Default tipo_esquecimento='deliberado' = ação consciente do usuário
    via NeuroGus painel.
    """
    if not memory_id or not memory_id.strip():
        raise ValueError("memory_id vazio")
    if tipo_esquecimento not in ("funcional", "deliberado", "superado", "protegido"):
        raise ValueError(f"tipo_esquecimento inválido: '{tipo_esquecimento}'")
    client = _get_client()
    client.set_payload(
        collection_name=COLLECTION,
        payload={"estado": "esquecido", "tipo_esquecimento": tipo_esquecimento},
        points=[memory_id.strip()],
    )
    return True


def re_lembrar(memory_id: str) -> bool:
    """Reverte soft delete: estado='ativo', limpa tipo_esquecimento.

    Permite resgatar fragmento esquecido por engano (gus-30.1 §4.3).
    """
    if not memory_id or not memory_id.strip():
        raise ValueError("memory_id vazio")
    client = _get_client()
    client.set_payload(
        collection_name=COLLECTION,
        payload={"estado": "ativo", "tipo_esquecimento": None},
        points=[memory_id.strip()],
    )
    return True


def recentes(user_id: str = "gustavo", limit: int = 50,
             incluir_esquecidos: bool = False) -> list[dict]:
    """Lista fragmentos ordenados por criado_em desc (mais recentes primeiro).

    Usado pelo /hub/recent pra boot do grafo do NeuroGus. Por default
    omite fragmentos com estado='esquecido' (substrato de aprendizado,
    não pertence ao grafo ativo). incluir_esquecidos=True traz tudo
    pra modo "ver esquecidos" do NeuroGus (gus-30.1 §3.2).

    Retorna fragmentos com payload reduzido pro frontend, incluindo
    'relacionados' (IDs dos vizinhos por afinidade semântica).
    """
    client = _get_client()

    must = [FieldCondition(key="user_id", match=MatchValue(value=user_id))]
    must_not = []
    if not incluir_esquecidos:
        must_not.append(FieldCondition(key="estado", match=MatchValue(value="esquecido")))

    pontos, _ = client.scroll(
        collection_name=COLLECTION,
        scroll_filter=Filter(must=must, must_not=must_not),
        limit=limit,
        with_payload=True,
        with_vectors=False,
    )

    fragmentos = [
        {
            "id": str(p.id),
            "conteudo": (p.payload or {}).get("conteudo", ""),
            "tipo": (p.payload or {}).get("tipo"),
            "estado": (p.payload or {}).get("estado"),
            "confianca": (p.payload or {}).get("confianca", 0.7),
            "user_id": (p.payload or {}).get("user_id"),
            "via": (p.payload or {}).get("via"),
            "area": (p.payload or {}).get("area"),
            "criado_em": (p.payload or {}).get("criado_em"),
            "relacionados": (p.payload or {}).get("relacionados", []),
            "curador": (p.payload or {}).get("curador"),
        }
        for p in pontos
    ]

    # Ordena descendente por criado_em (Qdrant scroll não garante ordem)
    fragmentos.sort(key=lambda f: f.get("criado_em") or "", reverse=True)
    return fragmentos[:limit]


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


def _filtros_ext(
    user_id: str,
    tipo: Optional[str] = None,
    via: Optional[str] = None,
    area: Optional[str] = None,
    camada_temporal: Optional[str] = None,
    curador: Optional[str] = None,
) -> Filter:
    must = [FieldCondition(key="user_id", match=MatchValue(value=user_id))]
    for key, val in (
        ("tipo", tipo),
        ("via", via),
        ("area", area),
        ("camada_temporal", camada_temporal),
        ("curador", curador),
    ):
        if val:
            must.append(FieldCondition(key=key, match=MatchValue(value=val)))
    return Filter(must=must)


def listar_filtrado(
    user_id: str = "gustavo",
    tipo: Optional[str] = None,
    via: Optional[str] = None,
    area: Optional[str] = None,
    camada_temporal: Optional[str] = None,
    curador: Optional[str] = None,
    limit: int = 50,
) -> list[dict]:
    """Lista com filtros avançados, sem embedding. Para operações de inspeção."""
    client = _get_client()
    pontos, _ = client.scroll(
        collection_name=COLLECTION,
        scroll_filter=_filtros_ext(user_id, tipo, via, area, camada_temporal, curador),
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
            "camada_temporal": (p.payload or {}).get("camada_temporal"),
            "curador": (p.payload or {}).get("curador"),
            "confianca": (p.payload or {}).get("confianca"),
            "criado_em": (p.payload or {}).get("criado_em"),
        }
        for p in pontos
    ]


def auditar() -> dict:
    """Verifica qualidade da coleção. Retorna problemas e distribuições."""
    client = _get_client()

    def _contar_campo(campo: str, valor: str) -> int:
        return client.count(
            collection_name=COLLECTION,
            count_filter=Filter(must=[FieldCondition(key=campo, match=MatchValue(value=valor))]),
            exact=True,
        ).count

    curadores = {}
    for c in ("haiku", "sonnet", "telegram", "claude-code", "mgx", "api"):
        n = _contar_campo("curador", c)
        if n:
            curadores[c] = n

    vias = {}
    for v in ("telegram", "claude-code", "api", "github-action"):
        n = _contar_campo("via", v)
        if n:
            vias[v] = n

    todos, _ = client.scroll(
        collection_name=COLLECTION,
        limit=500,
        with_payload=True,
        with_vectors=False,
    )
    curtos = [
        {"id": str(p.id), "conteudo": (p.payload or {}).get("conteudo", "")[:80]}
        for p in todos
        if len((p.payload or {}).get("conteudo", "")) < 30
    ]
    sem_tipo = [
        {"id": str(p.id), "conteudo": (p.payload or {}).get("conteudo", "")[:80]}
        for p in todos
        if not (p.payload or {}).get("tipo")
    ]

    return {
        "total": len(todos),
        "por_curador": curadores,
        "por_via": vias,
        "fragmentos_curtos_lt30": curtos,
        "fragmentos_sem_tipo": sem_tipo,
    }
