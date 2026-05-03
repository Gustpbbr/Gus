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

    return app
