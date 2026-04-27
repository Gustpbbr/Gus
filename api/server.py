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
from fastapi.responses import HTMLResponse

from api.routes import router


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

    app.include_router(router)

    return app
