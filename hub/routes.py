"""
Endpoints REST do Hub Qdrant direto.

Todos sob /hub/*, com Bearer auth herdado de api/auth.py:verify_bearer.
Registrado em api/server.py via app.include_router(hub_router).

Endpoints expostos no OpenAPI (Custom GPT pode consumir):
    POST /hub/ingestar        — insere fragmento
    POST /hub/lembrar         — busca semântica filtrada

Endpoints internos (ocultos do OpenAPI):
    GET  /hub/ego-cache       — bloco pra injeção em system prompt
    GET  /hub/stats           — contagem por user_id

Referências:
    - hub/store.py (lógica)
    - hub/schemas.py (Pydantic)
    - projetos/gus/auditorias/2026-04-27/.../ADR-001-aposentadoria-mem0.md (decisão)
"""

import asyncio
import logging

from fastapi import APIRouter, Depends, HTTPException

from api.auth import verify_bearer
from hub.schemas import IngestarReq, IngestarResp, LembrarReq, LembrarResp
from hub.store import ingestar, lembrar, ego_cache, contar, stats

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/hub", tags=["hub"], dependencies=[Depends(verify_bearer)])


@router.post("/ingestar", operation_id="hub_ingestar", response_model=IngestarResp)
async def r_ingestar(payload: IngestarReq):
    """Insere um fragmento no Hub Qdrant (coleção `gus_hub`)."""
    try:
        frag_id = await asyncio.to_thread(
            ingestar, payload.conteudo, payload.model_dump()
        )
        return IngestarResp(id=frag_id, status="ok")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("hub.ingestar falhou")
        raise HTTPException(status_code=500, detail=f"hub.ingestar: {e}")


@router.post("/lembrar", operation_id="hub_lembrar", response_model=LembrarResp)
async def r_lembrar(payload: LembrarReq):
    """Busca semântica no Hub. Filtros opcionais por tipo/estado/area."""
    try:
        resultados = await asyncio.to_thread(
            lembrar,
            payload.query,
            payload.user_id,
            payload.limit,
            payload.tipo,
            payload.estado or None,
            payload.area,
        )
        return LembrarResp(results=resultados, total=len(resultados))
    except Exception as e:
        logger.exception("hub.lembrar falhou")
        raise HTTPException(status_code=500, detail=f"hub.lembrar: {e}")


@router.get("/ego-cache", operation_id="hub_ego_cache", include_in_schema=False)
async def r_ego_cache(user_id: str = "gustavo"):
    """Retorna fragmentos priorizados pra injeção em system prompt (Fase 4 do roadmap)."""
    try:
        cache = await asyncio.to_thread(ego_cache, user_id)
        return cache
    except Exception as e:
        logger.exception("hub.ego_cache falhou")
        raise HTTPException(status_code=500, detail=f"hub.ego_cache: {e}")


@router.get("/stats", operation_id="hub_stats", include_in_schema=False)
async def r_stats():
    """Retorna stats da coleção gus_hub (contagem por user_id, status, etc)."""
    try:
        s = await asyncio.to_thread(stats)
        return s
    except Exception as e:
        logger.exception("hub.stats falhou")
        raise HTTPException(status_code=500, detail=f"hub.stats: {e}")


@router.get("/contar", operation_id="hub_contar", include_in_schema=False)
async def r_contar(user_id: str = "gustavo"):
    """Atalho pra contagem de um user_id específico."""
    try:
        total = await asyncio.to_thread(contar, user_id)
        return {"user_id": user_id, "total_fragmentos": total, "colecao": "gus_hub"}
    except Exception as e:
        logger.exception("hub.contar falhou")
        raise HTTPException(status_code=500, detail=f"hub.contar: {e}")
