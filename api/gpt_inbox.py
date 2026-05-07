"""Endpoint determinístico de inbox para a porta GPT Chat.

GET /{secret}/gpt/inbox/{porta}    — inbox de uma porta
GET /{secret}/gpt/contexto         — inbox gpt-chat + hub stats (token único)

Requer GPT_INBOX_SECRET no Railway. HUB_READ_TOKEN fica interno — GPT Chat
nunca o vê. GPT Chat acessa via:
  https://gus-production-58a7.up.railway.app/<secret>/gpt/inbox/gpt-chat
  https://gus-production-58a7.up.railway.app/<secret>/gpt/contexto
"""
import asyncio
import os
import re

import httpx
from fastapi import APIRouter, HTTPException

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
