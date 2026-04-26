---
tipo: guia-implementacao
data: 2026-04-26
status: pronto-para-implementar
area: infra-hub
anterior: gus-19-etapa1-mem0-selfhost.md
proximo: gus-21-etapa3-curador.md
schema: gus-18-schema-indexacao.md
---

# Etapa 2 — Hub Qdrant direto (payload rico)

Enquanto a Etapa 1 usa Qdrant via wrapper do mem0, esta etapa cria o Hub que
acessa o Qdrant diretamente — sem middleware — com payload rico conforme o schema
em `gus-18-schema-indexacao.md`.

O Hub roda no mesmo serviço Railway, como novas rotas em `/hub/*`.

## Arquivos novos

```
hub/
├── __init__.py       ← vazio
├── schemas.py        ← Pydantic schemas
├── store.py          ← Qdrant direto com fastembed
└── routes.py         ← FastAPI endpoints /hub/*
```

Alteração em `api/server.py`: registrar o router do Hub.

## `hub/__init__.py`

Arquivo vazio.

## `hub/schemas.py`

```python
from pydantic import BaseModel, Field
from typing import Optional


class IngestarReq(BaseModel):
    conteudo: str
    tipo: str = "episodico"
    camada_temporal: str = "sessao"
    via: str = "telegram"
    area: str = ""
    projeto: str = ""
    user_id: str = "gustavo"
    confianca: float = Field(0.7, ge=0.0, le=1.0)


class LembrarReq(BaseModel):
    query: str
    user_id: str = "gustavo"
    limit: int = Field(10, ge=1, le=30)
    tipo: Optional[str] = None
    estado: Optional[str] = None
    area: Optional[str] = None
```

## `hub/store.py`

```python
import os
import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, Filter, FieldCondition, MatchValue
)

BRT = timezone(timedelta(hours=-3))
COLLECTION = "gus_hub"

_client: Optional[QdrantClient] = None


def get_client() -> QdrantClient:
    global _client
    if _client is None:
        _client = QdrantClient(
            url=os.environ["QDRANT_URL"],
            api_key=os.environ["QDRANT_API_KEY"],
        )
        _ensure_collection(_client)
    return _client


def _ensure_collection(client: QdrantClient):
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION not in existing:
        # 384 dims = BAAI/bge-small-en-v1.5 via fastembed
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )


def _filtros(user_id: str, tipo=None, estado=None, area=None) -> Filter:
    conds = [FieldCondition(key="user_id", match=MatchValue(value=user_id))]
    if tipo:
        conds.append(FieldCondition(key="tipo", match=MatchValue(value=tipo)))
    if estado:
        conds.append(FieldCondition(key="estado", match=MatchValue(value=estado)))
    if area:
        conds.append(FieldCondition(key="area", match=MatchValue(value=area)))
    return Filter(must=conds)


def ingestar(conteudo: str, metadata: dict) -> str:
    client = get_client()
    now = datetime.now(BRT).isoformat()
    frag_id = str(uuid.uuid4())
    payload = {
        "conteudo": conteudo,
        "tipo": metadata.get("tipo", "episodico"),
        "estado": "ativo",
        "camada_temporal": metadata.get("camada_temporal", "sessao"),
        "tipo_esquecimento": None,
        "peso": 0.5,
        "confirmacoes": 0,
        "confianca": metadata.get("confianca", 0.7),
        "via": metadata.get("via", "telegram"),
        "area": metadata.get("area", ""),
        "projeto": metadata.get("projeto", ""),
        "user_id": metadata.get("user_id", "gustavo"),
        "criado_em": now,
        "ultimo_acesso": now,
        "acessos": 0,
    }
    # QdrantClient com fastembed: add() gera embedding automaticamente
    client.add(
        collection_name=COLLECTION,
        documents=[conteudo],
        metadata=[payload],
        ids=[frag_id],
    )
    return frag_id


def lembrar(query: str, user_id="gustavo", limit=10,
            tipo=None, estado=None, area=None) -> list:
    client = get_client()
    results = client.query(
        collection_name=COLLECTION,
        query_text=query,
        query_filter=_filtros(user_id, tipo, estado, area),
        limit=limit,
    )
    return [
        {
            "id": str(r.id),
            "conteudo": r.metadata.get("conteudo", ""),
            "score": r.score,
            "tipo": r.metadata.get("tipo"),
            "estado": r.metadata.get("estado"),
            "via": r.metadata.get("via"),
        }
        for r in results
    ]


def ego_cache(user_id="gustavo") -> dict:
    client = get_client()

    def scroll_tipo(tipo: str, limit: int = 10, estado: str = None):
        pontos, _ = client.scroll(
            collection_name=COLLECTION,
            scroll_filter=_filtros(user_id, tipo=tipo, estado=estado),
            limit=limit,
            with_payload=True,
        )
        return [p.payload for p in pontos]

    return {
        "identidade": scroll_tipo("identidade_operacional", estado="estavel"),
        "protegidos": scroll_tipo("procedural", estado="estavel"),
        "decisoes_recentes": scroll_tipo("decisao", limit=3),
        "meta_reflexoes": scroll_tipo("meta_reflexao", limit=5),
    }


def contar(user_id="gustavo") -> int:
    client = get_client()
    return client.count(
        collection_name=COLLECTION,
        count_filter=_filtros(user_id),
    ).count
```

## `hub/routes.py`

```python
import asyncio
from fastapi import APIRouter, Depends
from api.auth import verify_bearer
from hub.store import ingestar, lembrar, ego_cache, contar
from hub.schemas import IngestarReq, LembrarReq

router = APIRouter(prefix="/hub", dependencies=[Depends(verify_bearer)])


@router.post("/ingestar")
async def r_ingestar(payload: IngestarReq):
    frag_id = await asyncio.to_thread(ingestar, payload.conteudo, payload.model_dump())
    return {"id": frag_id, "status": "ok"}


@router.post("/lembrar")
async def r_lembrar(payload: LembrarReq):
    results = await asyncio.to_thread(
        lembrar, payload.query, payload.user_id, payload.limit,
        payload.tipo, payload.estado, payload.area
    )
    return {"results": results, "total": len(results)}


@router.get("/ego-cache")
async def r_ego_cache(user_id: str = "gustavo"):
    cache = await asyncio.to_thread(ego_cache, user_id)
    return cache


@router.get("/auto-relato")
async def r_auto_relato(user_id: str = "gustavo", forcar: bool = False):
    from hub.auto_relato import gerar_auto_relato
    texto = await gerar_auto_relato(user_id, forcar=forcar)
    return {"auto_relato": texto, "user_id": user_id}


@router.get("/stats")
async def r_stats(user_id: str = "gustavo"):
    total = await asyncio.to_thread(contar, user_id)
    return {"user_id": user_id, "total_fragmentos": total}
```

## Alteração em `api/server.py`

Adicionar após `app.include_router(router)`:

```python
from hub.routes import router as hub_router
app.include_router(hub_router)
```

## Coleções no Qdrant

| Coleção | Usado por | Conteúdo |
|---|---|---|
| `gus` | mem0 self-hosted (Etapa 1) | memórias extraídas pelo mem0 |
| `gus_hub` | Hub direto (Etapa 2+) | fragmentos com payload rico |

As duas coleções coexistem. Ver `gus-23-logica-qdrant-mem0.md` para regras de convivência.
