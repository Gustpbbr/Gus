"""
FastAPI app pro Custom GPT no ChatGPT consumir.

Servida no mesmo processo do bot Telegram via `gus/main.py` rodando ambos
em paralelo (asyncio). Importada no GPT Builder via OpenAPI (`/openapi.json`).

Endpoints:
  - GET  /health                — sem auth, healthcheck do Railway
  - todos os outros             — Bearer token (CUSTOM_GPT_TOKEN)
"""

import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from api.routes import router
from api.gpt_inbox import router as gpt_inbox_router
from hub.routes import router as hub_router


def create_app() -> FastAPI:
    base_url = os.getenv("API_PUBLIC_URL", "")

    app = FastAPI(
        title="Gus — Custom GPT API",
        version="1.0.0",
        description=(
            "API HTTP do Gus pro Custom GPT do Gustavo. Espelha subset das "
            "tools do bot Telegram. Path `dimagem/` bloqueado nesta porta "
            "por LGPD. Toda escrita carrega tag `via=custom-gpt` no Mem0."
        ),
        servers=[{"url": base_url}] if base_url else None,
    )

    @app.get("/health", include_in_schema=False)
    async def health():
        return {"status": "ok", "service": "gus-api"}

    # Stat operacional pro alerta proativo de custo (item S4 do plano de
    # saneamento). Sem auth porque é só agregado mensal — cron GH Actions
    # consulta sem precisar carregar Bearer.
    @app.get("/health/cost", include_in_schema=False)
    async def health_cost():
        from gus.logger import stats_mes_atual
        s = stats_mes_atual()
        limit = float(os.getenv("HARD_LIMIT_USD_MONTH", "30"))
        pct = (s["cost_usd"] / limit * 100.0) if limit > 0 else 0.0
        return {
            "cost_usd": s["cost_usd"],
            "limit_usd": limit,
            "percentage": round(pct, 2),
            "calls": s["calls"],
            "tokens_in": s["tokens_in"],
            "tokens_out": s["tokens_out"],
        }

    # PROJETO FUTURO — PWA da câmera do S8.
    # Sem auth (é só uma página HTML). O token é inserido pelo usuário na
    # primeira abertura e salvo em localStorage. Os endpoints que a PWA
    # consome (/analise_camera) requerem Bearer token normalmente.
    @app.get("/dashboard", include_in_schema=False, response_class=HTMLResponse)
    async def dashboard():
        from api.dashboard import DASHBOARD_HTML
        return HTMLResponse(content=DASHBOARD_HTML)

    @app.get("/camera", include_in_schema=False, response_class=HTMLResponse)
    async def camera_pwa():
        from api.camera import CAMERA_PWA_HTML
        return HTMLResponse(content=CAMERA_PWA_HTML)

    # NeuroGus — PWA grafo 3D do Hub Qdrant (gus-30, gus-30.1).
    # Sem auth na rota: HTML é estático na Parte 1A. Parte 1B (próxima)
    # vai validar ?token= antes de retornar dados via fetch /hub/recent
    # e EventSource /hub/stream — auth dos dados, não do HTML.
    @app.get("/neurogus", include_in_schema=False, response_class=HTMLResponse)
    async def neurogus():
        from api.neurogus import NEUROGUS_HTML
        return HTMLResponse(content=NEUROGUS_HTML)

    @app.get("/neurogus/manifest.json", include_in_schema=False)
    async def neurogus_manifest():
        from api.neurogus import MANIFEST
        return JSONResponse(content=MANIFEST)

    app.include_router(router)
    app.include_router(hub_router)  # Hub Qdrant direto — ADR-001 Fase 1
    app.include_router(gpt_inbox_router)  # Inbox determinístico — GPT Chat

    return app
