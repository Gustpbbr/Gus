"""
Auto-diagnóstico do Gus — health check paralelo de todos os componentes externos.

Cada check retorna dict {name, status, detail} com status em "ok"|"warn"|"error".
Tudo roda em paralelo via asyncio.gather pra latência total ~ check mais lento.

CHECKS ATIVOS (6):
  1. GitHub PAT          — GET /user, valida escopo
  2. Mem0                — get_all + calcula frescor da memória mais recente
  3. Anthropic           — Haiku ping (1 token, ~$0.000004)
  4. Tavily              — search com max_results=1
  5. Volume Railway      — /app/data writable?
  6. Workflows GH        — últimos 5 runs e conclusões

CHECKS NÃO INCLUÍDOS (decisão pendente):
  - Whisper: precisaria arquivo dummy
  - DuckDuckGo: só fallback do Tavily
  - Mem0 write real: indexação assíncrona (latência minutos), o frescor já cobre

USO:
  await auto_diagnostico()  → tabela markdown pro Telegram
"""

import asyncio
import logging
import os
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx

logger = logging.getLogger(__name__)
BRT = timezone(timedelta(hours=-3))

# Threshold em horas: se a memória mais recente do Mem0 for mais antiga que
# isso, levanta WARNING. 12h é razoável — pega o silêncio de 13h de hoje.
MEM0_FRESH_HOURS = 12

_EMOJI = {"ok": "✅", "warn": "⚠️", "error": "❌"}


# ---------------------------------------------------------------------------
# CHECKS individuais
# ---------------------------------------------------------------------------

async def _check_github_pat() -> dict:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return {"name": "GitHub PAT", "status": "error", "detail": "GITHUB_TOKEN ausente"}
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get("https://api.github.com/user", headers=headers)
        if r.status_code != 200:
            return {
                "name": "GitHub PAT",
                "status": "error",
                "detail": f"status {r.status_code}",
            }
        scopes = r.headers.get("x-oauth-scopes", "?")
        return {
            "name": "GitHub PAT",
            "status": "ok",
            "detail": f"escopos: {scopes or 'fine-grained'}",
        }
    except Exception as e:
        return {"name": "GitHub PAT", "status": "error", "detail": str(e)[:80]}


async def _check_mem0() -> dict:
    """Lê memórias do brain `gustavo` e calcula frescor da mais recente."""
    api_key = os.getenv("MEM0_API_KEY")
    if not api_key:
        return {"name": "Mem0", "status": "error", "detail": "MEM0_API_KEY ausente"}

    try:
        from mem0 import MemoryClient
        client = MemoryClient(api_key=api_key)
    except Exception as e:
        return {"name": "Mem0", "status": "error", "detail": f"client init: {str(e)[:60]}"}

    try:
        result = await asyncio.to_thread(
            client.get_all, user_id="gustavo", page=1, page_size=20
        )
    except Exception as e:
        return {"name": "Mem0", "status": "error", "detail": f"get_all: {str(e)[:60]}"}

    # SDK varia — normaliza pra lista
    if isinstance(result, dict):
        mems = result.get("memories") or result.get("results") or []
    elif isinstance(result, list):
        mems = result
    else:
        mems = []

    if not mems:
        return {
            "name": "Mem0",
            "status": "warn",
            "detail": "0 memórias no brain gustavo",
        }

    latest = None
    for m in mems:
        c = m.get("created_at") if isinstance(m, dict) else None
        if not c:
            continue
        try:
            dt = datetime.fromisoformat(c.replace("Z", "+00:00"))
            if latest is None or dt > latest:
                latest = dt
        except Exception:
            pass

    total = len(mems)
    if latest is None:
        return {
            "name": "Mem0",
            "status": "warn",
            "detail": f"{total} mems mas sem timestamp parseável",
        }

    delta_h = (datetime.now(timezone.utc) - latest).total_seconds() / 3600
    fresca_brt = latest.astimezone(BRT).strftime("%d/%m %H:%M")

    if delta_h > MEM0_FRESH_HOURS:
        return {
            "name": "Mem0",
            "status": "warn",
            "detail": f"{total} mems, última há {delta_h:.1f}h ({fresca_brt} BRT) — possível silêncio",
        }
    return {
        "name": "Mem0",
        "status": "ok",
        "detail": f"{total} mems, última há {delta_h:.1f}h ({fresca_brt} BRT)",
    }


async def _check_anthropic() -> dict:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return {"name": "Anthropic", "status": "error", "detail": "ANTHROPIC_API_KEY ausente"}

    payload = {
        "model": "claude-haiku-4-5",
        "max_tokens": 8,
        "messages": [{"role": "user", "content": "ping"}],
    }
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    t0 = time.time()
    try:
        async with httpx.AsyncClient(timeout=20) as c:
            r = await c.post(
                "https://api.anthropic.com/v1/messages", json=payload, headers=headers
            )
        latency = round(time.time() - t0, 2)
        if r.status_code == 200:
            return {"name": "Anthropic", "status": "ok", "detail": f"Haiku ok em {latency}s"}
        body = r.json() if "json" in r.headers.get("content-type", "") else {}
        msg = (body.get("error", {}) or {}).get("message", "") or r.text[:80]
        msg_low = msg.lower()
        if any(t in msg_low for t in ["credit", "balance", "insufficient"]):
            return {"name": "Anthropic", "status": "error", "detail": "sem créditos"}
        if r.status_code == 401:
            return {"name": "Anthropic", "status": "error", "detail": "key inválida"}
        if r.status_code == 429:
            return {"name": "Anthropic", "status": "warn", "detail": "rate limit"}
        return {"name": "Anthropic", "status": "error", "detail": f"{r.status_code}: {msg[:60]}"}
    except Exception as e:
        return {"name": "Anthropic", "status": "error", "detail": str(e)[:80]}


async def _check_tavily() -> dict:
    key = os.getenv("TAVILY_API_KEY")
    if not key:
        return {
            "name": "Tavily",
            "status": "warn",
            "detail": "TAVILY_API_KEY ausente (DDG vira primário)",
        }

    payload = {"api_key": key, "query": "ping", "max_results": 1}
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.post("https://api.tavily.com/search", json=payload)
        if r.status_code == 200:
            return {"name": "Tavily", "status": "ok", "detail": "search OK"}
        if r.status_code == 401:
            return {"name": "Tavily", "status": "error", "detail": "key inválida"}
        if r.status_code == 429:
            return {"name": "Tavily", "status": "warn", "detail": "rate/quota"}
        return {"name": "Tavily", "status": "error", "detail": f"status {r.status_code}"}
    except Exception as e:
        return {"name": "Tavily", "status": "error", "detail": str(e)[:80]}


def _check_volume_sync() -> dict:
    data_dir = Path("/app/data")
    if not data_dir.exists():
        return {
            "name": "Volume Railway",
            "status": "warn",
            "detail": "/app/data inexistente (rodando fora do Railway?)",
        }
    test_file = data_dir / ".diagnostic_test"
    try:
        test_file.write_text("ping", encoding="utf-8")
        contents = test_file.read_text(encoding="utf-8")
        test_file.unlink()
        if contents != "ping":
            return {"name": "Volume Railway", "status": "error", "detail": "ler!=escrever"}
        return {"name": "Volume Railway", "status": "ok", "detail": "/app/data writable"}
    except Exception as e:
        return {"name": "Volume Railway", "status": "error", "detail": str(e)[:80]}


async def _check_volume() -> dict:
    return await asyncio.to_thread(_check_volume_sync)


async def _check_workflows() -> dict:
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPO", "Gustpbbr/Gus")
    if not token:
        return {"name": "Workflows GH", "status": "error", "detail": "GITHUB_TOKEN ausente"}

    url = f"https://api.github.com/repos/{repo}/actions/runs"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(url, headers=headers, params={"per_page": 5})
        if r.status_code != 200:
            return {
                "name": "Workflows GH",
                "status": "error",
                "detail": f"status {r.status_code}",
            }
        runs = r.json().get("workflow_runs", [])
        if not runs:
            return {"name": "Workflows GH", "status": "warn", "detail": "nenhum run recente"}
        falhas = [run for run in runs if run.get("conclusion") == "failure"]
        if falhas:
            nomes = ", ".join({run.get("name", "?") for run in falhas})
            return {
                "name": "Workflows GH",
                "status": "warn",
                "detail": f"{len(falhas)}/{len(runs)} falhas: {nomes[:60]}",
            }
        return {
            "name": "Workflows GH",
            "status": "ok",
            "detail": f"{len(runs)} runs recentes, todos OK",
        }
    except Exception as e:
        return {"name": "Workflows GH", "status": "error", "detail": str(e)[:80]}


# ---------------------------------------------------------------------------
# ORQUESTRAÇÃO
# ---------------------------------------------------------------------------

async def auto_diagnostico() -> str:
    """Roda todos os checks em paralelo e retorna tabela markdown."""
    inicio = time.time()
    resultados = await asyncio.gather(
        _check_github_pat(),
        _check_mem0(),
        _check_anthropic(),
        _check_tavily(),
        _check_volume(),
        _check_workflows(),
        return_exceptions=True,
    )

    linhas = ["| Check | Status | Detalhe |", "|---|---|---|"]
    erros = 0
    warns = 0

    for r in resultados:
        if isinstance(r, Exception):
            linhas.append(f"| (exceção) | ❌ | {str(r)[:80]} |")
            erros += 1
            continue
        emoji = _EMOJI.get(r["status"], "❓")
        if r["status"] == "error":
            erros += 1
        elif r["status"] == "warn":
            warns += 1
        linhas.append(f"| {r['name']} | {emoji} | {r['detail']} |")

    elapsed = round(time.time() - inicio, 1)

    if erros:
        cabecalho = f"❌ Diagnóstico — {erros} erro(s), {warns} aviso(s) em {elapsed}s"
    elif warns:
        cabecalho = f"⚠️ Diagnóstico — {warns} aviso(s) em {elapsed}s"
    else:
        cabecalho = f"✅ Diagnóstico — tudo ok em {elapsed}s"

    return f"{cabecalho}\n\n" + "\n".join(linhas)
