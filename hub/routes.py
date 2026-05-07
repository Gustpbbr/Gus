"""
Endpoints REST do Hub Qdrant direto.

Todos sob /hub/*, com Bearer auth via header OU query (verify_bearer_flex).
Registrado em api/server.py via app.include_router(hub_router).

Endpoints expostos no OpenAPI (Custom GPT pode consumir):
    POST /hub/ingestar        — insere fragmento
    POST /hub/lembrar         — busca semântica filtrada

Endpoints internos (ocultos do OpenAPI):
    GET  /hub/ego-cache       — bloco pra injeção em system prompt
    GET  /hub/stats           — contagem por user_id

NeuroGus (gus-30.1):
    GET    /hub/recent                         — boot do grafo
    GET    /hub/stream                         — SSE em tempo real
    DELETE /hub/fragmento/{id}                 — hard delete
    PATCH  /hub/fragmento/{id}/esquecer        — soft delete (reversível)
    PATCH  /hub/fragmento/{id}/lembrar         — reverte soft delete

Referências:
    - hub/store.py (lógica)
    - hub/events.py (broadcast SSE)
    - hub/schemas.py (Pydantic)
    - projetos/gus/gus-30.1-neurogus-decisoes-v0.md (escopo Fase 1)
    - projetos/gus/auditorias/2026-04-27/.../ADR-001-aposentadoria-mem0.md
"""

import asyncio
import json
import logging
import os

from fastapi import APIRouter, Depends, HTTPException, Header, Query
from fastapi.responses import StreamingResponse

from hub.events import subscribe
from hub.schemas import IngestarReq, IngestarResp, LembrarReq, LembrarResp
from hub.store import (
    ingestar, lembrar, ego_cache, contar, stats,
    deletar, esquecer, re_lembrar, recentes,
)

logger = logging.getLogger(__name__)


async def verify_bearer_flex(
    authorization: str | None = Header(default=None),
    token: str | None = Query(default=None),
) -> None:
    """Aceita Bearer no Authorization header OU ?token= na URL.

    EventSource (SSE) não suporta header customizado, então o /hub/stream
    do NeuroGus passa o token via query. Outros endpoints continuam
    usando header (Custom GPT, MCP, claude-code) — comportamento inalterado
    porque header tem prioridade quando ambos vierem.
    """
    expected = os.getenv("CUSTOM_GPT_TOKEN")
    if not expected:
        raise HTTPException(
            status_code=503,
            detail="CUSTOM_GPT_TOKEN não configurado no servidor.",
        )

    if authorization:
        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail="Authorization deve ser 'Bearer <token>'.",
            )
        provided = authorization[len("Bearer "):].strip()
    elif token:
        provided = token.strip()
    else:
        raise HTTPException(
            status_code=401,
            detail="Authorization header ou ?token= ausente.",
        )

    if provided != expected:
        raise HTTPException(status_code=403, detail="Token inválido.")


router = APIRouter(prefix="/hub", tags=["hub"], dependencies=[Depends(verify_bearer_flex)])


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


# ────────────────────────────────────────────────────────────────────
# NeuroGus — Fase 1 (gus-30.1)
# ────────────────────────────────────────────────────────────────────

@router.get("/recent", operation_id="hub_recent", include_in_schema=False)
async def r_recent(
    user_id: str = "gustavo",
    limit: int = 50,
    incluir_esquecidos: bool = False,
):
    """Lista fragmentos recentes pro boot do grafo NeuroGus.

    Por default exclui fragmentos com estado='esquecido'. Para ver
    o substrato de retro-aprendizado, passa incluir_esquecidos=true.
    """
    try:
        fragmentos = await asyncio.to_thread(
            recentes, user_id, limit, incluir_esquecidos
        )
        return {"fragmentos": fragmentos, "total": len(fragmentos)}
    except Exception as e:
        logger.exception("hub.recent falhou")
        raise HTTPException(status_code=500, detail=f"hub.recent: {e}")


@router.get("/stream", include_in_schema=False)
async def r_stream():
    """Server-Sent Events stream de fragmentos novos em tempo real.

    Conexão persistente: cada evento `data: {json}\\n\\n` representa um
    fragmento ingerido no Hub depois do cliente conectar. Pra estado
    inicial do grafo, cliente chama GET /hub/recent primeiro.

    Auth via ?token= na query (EventSource não suporta header custom).
    Headers obrigatórios pra SSE estável atrás de proxies (Nginx/Railway):
        Cache-Control: no-cache
        X-Accel-Buffering: no
    """
    async def event_stream():
        # Comentário inicial: força flush do header e começa stream
        yield ": neurogus stream conectado\n\n"
        async for payload in subscribe():
            yield f"data: {payload}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@router.delete("/fragmento/{frag_id}", include_in_schema=False)
async def r_delete_fragmento(frag_id: str):
    """Hard delete: apaga fragmento do Qdrant. IRREVERSÍVEL.

    Use só pra dados sensíveis salvos por engano (LGPD) ou lixo
    sem valor histórico. Pra remoção reversível, use /esquecer.
    """
    try:
        await asyncio.to_thread(deletar, frag_id)
        return {"id": frag_id, "status": "deletado"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("hub.deletar falhou")
        raise HTTPException(status_code=500, detail=f"hub.deletar: {e}")


@router.patch("/fragmento/{frag_id}/esquecer", include_in_schema=False)
async def r_esquecer_fragmento(frag_id: str, tipo_esquecimento: str = "deliberado"):
    """Soft delete: marca fragmento como 'esquecido' (reversível via /lembrar).

    Fragmento some das buscas semânticas mas continua no Qdrant como
    substrato de retro-aprendizado (gus-30.1 §3).
    """
    try:
        await asyncio.to_thread(esquecer, frag_id, tipo_esquecimento)
        return {"id": frag_id, "status": "esquecido", "tipo_esquecimento": tipo_esquecimento}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("hub.esquecer falhou")
        raise HTTPException(status_code=500, detail=f"hub.esquecer: {e}")


@router.patch("/fragmento/{frag_id}/lembrar", include_in_schema=False)
async def r_re_lembrar_fragmento(frag_id: str):
    """Reverte soft delete: estado='ativo', limpa tipo_esquecimento."""
    try:
        await asyncio.to_thread(re_lembrar, frag_id)
        return {"id": frag_id, "status": "ativo"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("hub.re_lembrar falhou")
        raise HTTPException(status_code=500, detail=f"hub.re_lembrar: {e}")
