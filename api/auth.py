"""
Bearer token auth pra Custom GPT.

Token único compartilhado, configurado via env `CUSTOM_GPT_TOKEN`. O Custom
GPT no ChatGPT Builder envia em todo request:
  Authorization: Bearer <token>

Falha em 401 se header ausente, 403 se token errado, 503 se servidor não
configurou o token (config error).
"""

import os

from fastapi import Header, HTTPException


async def verify_bearer(authorization: str | None = Header(default=None)) -> None:
    expected = os.getenv("CUSTOM_GPT_TOKEN")
    if not expected:
        raise HTTPException(
            status_code=503,
            detail="CUSTOM_GPT_TOKEN não configurado no servidor.",
        )
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header ausente.",
        )
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Authorization deve ser 'Bearer <token>'.",
        )
    token = authorization[len("Bearer "):].strip()
    if token != expected:
        raise HTTPException(status_code=403, detail="Token inválido.")
