"""Endpoint determinístico de inbox para a porta GPT Chat.

GET /{secret}/gpt/inbox/{porta}

Retorna listagem completa com frontmatter parseado — sem depender de busca
indexada (que o conector GitHub do ChatGPT usa e que é não-determinística).

Requer GPT_INBOX_SECRET no Railway. GPT Chat acessa via:
  https://gus-production-58a7.up.railway.app/<secret>/gpt/inbox/gpt-chat
"""
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


async def _gh_read(download_url: str) -> str:
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(download_url)
        r.raise_for_status()
        return r.text


@router.get("/{secret}/gpt/inbox/{porta}")
async def gpt_inbox(secret: str, porta: str):
    """Listagem determinística do inbox de uma porta — para uso pelo GPT Chat."""
    try:
        expected = _secret()
    except RuntimeError:
        raise HTTPException(status_code=503, detail="GPT_INBOX_SECRET não configurado no Railway")

    if secret != expected:
        raise HTTPException(status_code=404)

    if porta not in _PORTAS_VALIDAS:
        raise HTTPException(status_code=400, detail=f"Porta inválida: {porta}")

    folder = f"dialogos/inbox-{porta}"

    try:
        items = await _gh_list(folder)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return {
                "porta": porta,
                "modo": "deterministico",
                "total": 0,
                "arquivos": [],
                "aviso": f"Pasta {folder} ainda não existe",
            }
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

        # Inclui pendente, parcial e sem status — exclui concluido/arquivado
        status = fm.get("status", "pendente").lower()
        if status in ("concluido", "arquivado", "cancelado"):
            continue

        title_m = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        titulo = title_m.group(1).strip() if title_m else name.removesuffix(".md")

        body = re.sub(r"^---.*?---\s*", "", content, flags=re.DOTALL).strip()
        resumo = (body.split("\n\n")[0] if body else "")[:200]

        arquivos.append({
            "path": f"{folder}/{name}",
            "nome": name,
            "frontmatter": fm,
            "titulo": titulo,
            "resumo": resumo,
        })

    arquivos.sort(key=lambda x: _PRIORIDADE_ORDEM.get(
        str(x["frontmatter"].get("prioridade", "")).lower(), 3
    ))

    return {
        "porta": porta,
        "modo": "deterministico",
        "total": len(arquivos),
        "arquivos": arquivos,
    }
