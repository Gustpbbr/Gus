"""
Endpoints internos do Hub para uso pelo Claude Code via MCP.

Auth: token no path (HUB_READ_TOKEN env var). Leitura apenas — sem
endpoints de escrita aqui. Completamente oculto do OpenAPI/Custom GPT.

Endpoints:
    GET /{token}/cc/hub/stats                         — totais + distribuições
    GET /{token}/cc/hub/list?user_id=&tipo=&via=&...  — listagem filtrada
    GET /{token}/cc/hub/audit                         — qualidade da coleção
"""

import asyncio
import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from hub.store import stats, listar_filtrado, auditar

router = APIRouter(include_in_schema=False)

_PREFIXO = "/{token}/cc/hub"


def _verificar_token(token: str) -> None:
    esperado = os.environ.get("HUB_READ_TOKEN")
    if not esperado:
        raise HTTPException(status_code=503, detail="HUB_READ_TOKEN não configurado.")
    if token != esperado:
        raise HTTPException(status_code=403, detail="Token inválido.")


@router.get(_PREFIXO + "/stats")
async def hub_cc_stats(token: str):
    """Totais de fragmentos por user_id, curador, via."""
    _verificar_token(token)
    try:
        resultado = await asyncio.to_thread(stats)
        return JSONResponse(resultado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(_PREFIXO + "/list")
async def hub_cc_list(
    token: str,
    user_id: str = "gustavo",
    tipo: str | None = None,
    via: str | None = None,
    area: str | None = None,
    camada_temporal: str | None = None,
    curador: str | None = None,
    limit: int = 50,
):
    """Listagem filtrada sem embedding. Aceita filtros opcionais como query params."""
    _verificar_token(token)
    limit = max(1, min(limit, 200))
    try:
        fragmentos = await asyncio.to_thread(
            listar_filtrado, user_id, tipo, via, area, camada_temporal, curador, limit
        )
        return JSONResponse({"total": len(fragmentos), "fragmentos": fragmentos})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(_PREFIXO + "/audit")
async def hub_cc_audit(token: str):
    """Auditoria de qualidade: fragmentos curtos, sem tipo, distribuição por curador."""
    _verificar_token(token)
    try:
        resultado = await asyncio.to_thread(auditar)
        return JSONResponse(resultado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
