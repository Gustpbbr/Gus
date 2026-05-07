"""Endpoints para as portas GPT Chat e Custom GPT.

GET /{secret}/gpt/inbox/{porta}    — inbox de uma porta
GET /{secret}/gpt/contexto         — inbox gpt-chat + hub stats
GET /{secret}/gpt/hub/search       — busca semântica no Hub
GET /{secret}/gpt/hub/list         — listagem filtrada do Hub
GET /{secret}/gpt/hub/recent       — fragmentos mais recentes
GET /{secret}/gpt/hub/ego-cache    — identidade + decisões + meta-reflexões
GET /{secret}/gpt/hub/audit        — qualidade da coleção

Requer GPT_INBOX_SECRET no Railway. Credenciais Qdrant ficam internas — nunca
saem para o cliente.
"""
import asyncio
import os
import re

import httpx
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

_PORTAS_VALIDAS = frozenset({"gpt-chat", "tiogu", "claude-code", "claude-chat", "custom-gpt"})
_PRIORIDADE_ORDEM = {"alta": 0, "media": 1, "baixa": 2}


def _secret() -> str:
    s = os.environ.get("GPT_INBOX_SECRET", "")
    if not s:
        raise RuntimeError("GPT_INBOX_SECRET não configurado")
    return s


def _gh_headers() -> dict:
    return {
        "Authorization": f"token {os.getenv('GITHUB_TOKEN', '')}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _parse_frontmatter(content: str) -> dict:
    """Extrai frontmatter YAML simples via regex — sem dependência yaml."""
    m = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not m:
        return {}
    result = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip().lower()
        val = val.strip().strip('"').strip("'")
        if val and val not in ('""', "''"):
            result[key] = val
    return result


async def _gh_list(folder: str) -> list[dict]:
    repo = os.getenv("GITHUB_REPO", "Gustpbbr/Gus")
    url = f"https://api.github.com/repos/{repo}/contents/{folder}"
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, headers=_gh_headers())
        r.raise_for_status()
        data = r.json()
        return data if isinstance(data, list) else []


async def _gh_list_recursive(folder: str) -> list[dict]:
    """Lista arquivos recursivamente incluindo subpastas."""
    items = await _gh_list(folder)
    result = []
    for item in items:
        if item["type"] == "file":
            result.append(item)
        elif item["type"] == "dir":
            result.extend(await _gh_list_recursive(item["path"]))
    return result


async def _gh_read(download_url: str) -> str:
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(download_url)
        r.raise_for_status()
        return r.text


async def _listar_inbox(porta: str) -> dict:
    """Lógica central do inbox, sem autenticação — chamável internamente."""
    folder = f"dialogos/inbox-{porta}"
    try:
        items = await _gh_list_recursive(folder)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return {"porta": porta, "modo": "deterministico", "total": 0, "arquivos": [],
                    "aviso": f"Pasta {folder} ainda não existe"}
        raise HTTPException(status_code=503, detail="GitHub inacessível")
    except Exception:
        raise HTTPException(status_code=503, detail="Erro ao acessar GitHub")

    arquivos = []
    for item in items:
        name = item.get("name", "")
        if not name.endswith(".md") or name.startswith("_"):
            continue
        try:
            content = await _gh_read(item["download_url"])
        except Exception:
            continue
        fm = _parse_frontmatter(content)
        status = fm.get("status", "pendente").lower()
        if status in ("concluido", "arquivado", "cancelado"):
            continue
        title_m = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        titulo = title_m.group(1).strip() if title_m else name.removesuffix(".md")
        body = re.sub(r"^---.*?---\s*", "", content, flags=re.DOTALL).strip()
        resumo = (body.split("\n\n")[0] if body else "")[:200]
        arquivos.append({"path": f"{folder}/{name}", "nome": name,
                         "frontmatter": fm, "titulo": titulo, "resumo": resumo})

    arquivos.sort(key=lambda x: _PRIORIDADE_ORDEM.get(
        str(x["frontmatter"].get("prioridade", "")).lower(), 3))
    return {"porta": porta, "modo": "deterministico", "total": len(arquivos), "arquivos": arquivos}


async def _hub_stats_interno() -> dict | None:
    """Chama hub.store.stats() internamente — HUB_READ_TOKEN não sai da API."""
    try:
        from hub.store import stats
        return await asyncio.to_thread(stats)
    except Exception as e:
        return {"erro": str(e)[:120]}


def _verificar_secret(secret: str) -> None:
    try:
        expected = _secret()
    except RuntimeError:
        raise HTTPException(status_code=503, detail="GPT_INBOX_SECRET não configurado no Railway")
    if secret != expected:
        raise HTTPException(status_code=404)


@router.get("/{secret}/gpt/inbox/{porta}")
async def gpt_inbox(secret: str, porta: str):
    """Listagem determinística do inbox de uma porta — para uso pelo GPT Chat."""
    _verificar_secret(secret)
    if porta not in _PORTAS_VALIDAS:
        raise HTTPException(status_code=400, detail=f"Porta inválida: {porta}")
    return await _listar_inbox(porta)


@router.get("/{secret}/gpt/contexto")
async def gpt_contexto(secret: str):
    """Contexto agregado: inbox gpt-chat + hub stats.

    GPT Chat usa este endpoint com apenas GPT_INBOX_SECRET.
    HUB_READ_TOKEN e credenciais Qdrant ficam internas ao Railway — nunca
    saem para o cliente.
    """
    _verificar_secret(secret)
    inbox, hub = await asyncio.gather(
        _listar_inbox("gpt-chat"),
        _hub_stats_interno(),
    )
    return {
        "porta": "gpt-chat",
        "modo": "deterministico",
        "inbox": inbox,
        "hub": hub,
    }


# ── Hub endpoints (busca, listagem, recentes, ego-cache, auditoria) ──────────
# Credenciais Qdrant ficam internas. Único segredo externo: GPT_INBOX_SECRET.

@router.get("/{secret}/gpt/hub/search")
async def gpt_hub_search(
    secret: str,
    q: str = Query(..., description="Consulta em linguagem natural"),
    user_id: str = Query("gustavo", description="Brain alvo: gustavo ou gus"),
    limit: int = Query(20, ge=1, le=100),
    tipo: Optional[str] = Query(None),
    area: Optional[str] = Query(None),
    estado: Optional[str] = Query("ativo"),
):
    """Busca semântica no Hub Qdrant. Retorna fragmentos mais relevantes para a query."""
    _verificar_secret(secret)
    try:
        from hub.store import lembrar
        fragmentos = await asyncio.to_thread(lembrar, q, user_id, limit, tipo, estado, area)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Hub inacessível: {str(e)[:120]}")
    return {"modo": "semantico", "query": q, "user_id": user_id, "total": len(fragmentos), "fragmentos": fragmentos}


@router.get("/{secret}/gpt/hub/list")
async def gpt_hub_list(
    secret: str,
    user_id: str = Query("gustavo"),
    tipo: Optional[str] = Query(None),
    via: Optional[str] = Query(None),
    area: Optional[str] = Query(None),
    camada_temporal: Optional[str] = Query(None),
    curador: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
):
    """Listagem filtrada do Hub — sem busca semântica. Filtra por tipo, área, via, curador etc."""
    _verificar_secret(secret)
    try:
        from hub.store import listar_filtrado
        fragmentos = await asyncio.to_thread(
            listar_filtrado, user_id, tipo, via, area, camada_temporal, curador, limit
        )
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Hub inacessível: {str(e)[:120]}")
    return {"modo": "filtrado", "user_id": user_id, "total": len(fragmentos), "fragmentos": fragmentos}


@router.get("/{secret}/gpt/hub/recent")
async def gpt_hub_recent(
    secret: str,
    user_id: str = Query("gustavo"),
    limit: int = Query(50, ge=1, le=200),
    incluir_esquecidos: bool = Query(False),
):
    """Fragmentos mais recentes do Hub, ordenados por criado_em desc."""
    _verificar_secret(secret)
    try:
        from hub.store import recentes
        fragmentos = await asyncio.to_thread(recentes, user_id, limit, incluir_esquecidos)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Hub inacessível: {str(e)[:120]}")
    return {"modo": "recentes", "user_id": user_id, "total": len(fragmentos), "fragmentos": fragmentos}


@router.get("/{secret}/gpt/hub/ego-cache")
async def gpt_hub_ego_cache(
    secret: str,
    user_id: str = Query("gustavo"),
):
    """Ego cache: identidade operacional, procedurais estáveis, decisões recentes, meta-reflexões.

    Use no boot do Custom GPT para contexto essencial do Gus sem busca semântica.
    """
    _verificar_secret(secret)
    try:
        from hub.store import ego_cache
        cache = await asyncio.to_thread(ego_cache, user_id)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Hub inacessível: {str(e)[:120]}")
    return {"modo": "ego_cache", "user_id": user_id, "cache": cache}


@router.get("/{secret}/gpt/hub/audit")
async def gpt_hub_audit(secret: str):
    """Auditoria de qualidade da coleção Hub: fragmentos curtos, sem tipo, distribuição por curador/via."""
    _verificar_secret(secret)
    try:
        from hub.store import auditar
        resultado = await asyncio.to_thread(auditar)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Hub inacessível: {str(e)[:120]}")
    return {"modo": "auditoria", "resultado": resultado}
