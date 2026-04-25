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

    app.include_router(router)

    return app
