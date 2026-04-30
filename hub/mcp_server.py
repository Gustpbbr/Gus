"""
MCP Server — wrapper FastMCP em cima do Hub Qdrant.

Build cache marker: 2026-04-29T19:45  # invalida COPY layer no Railway

Expõe o Hub via Model Context Protocol pra clientes MCP-aware (Claude Chat,
Claude Code, etc.) consumirem busca semântica, ego cache, ingestão e leitura
de arquivos do GitHub em tempo real.

Hospedagem: Railway (serviço separado do bot Telegram, mesmo projeto).
Transporte: HTTP streamable (compatível com claude.ai Connectors).
Auth: Bearer token via header `Authorization`.

Tools expostas (Tier 1 — gus-28 Passo 2):

  Leitura Hub:
    - buscar_hub(query, limit, area?) — semântica
    - ego_cache_atual(user_id) — identidade + decisões recentes
    - fragmentos_recentes(horas, limit) — janela temporal
    - buscar_por_tipo(tipo, limit) — filtro por tipo
    - buscar_por_area(area, limit) — filtro por área
    - contar_fragmentos() — total + breakdown

  Escrita Hub:
    - ingestar_fragmento(conteudo, tipo, area, camada_temporal)
      — sempre via='claude-chat' (rastreabilidade)

  Repo GitHub:
    - read_repo_file(path) — conteúdo do .md
    - list_repo_dir(path) — listagem da pasta

Variáveis de ambiente:
  QDRANT_URL          — Hub
  QDRANT_API_KEY      — Hub
  MCP_BEARER_TOKEN    — auth header (Bearer)
  GITHUB_TOKEN        — repo tools (opcional, sem ele tools repo retornam 503)
  GITHUB_REPO         — default "Gustpbbr/Gus"
  PORT                — default 8080 (Railway injeta automaticamente; NÃO setar manual)

Rota /health responde 200 sem auth (pra Railway probe).
Rota /mcp é o endpoint MCP, exige Bearer.
"""

from __future__ import annotations

import hmac
import logging
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

# Adiciona repo root ao sys.path pra importar hub.store quando rodando
# como script standalone (Railway, docker)
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import httpx
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route

from hub.store import (
    contar,
    ego_cache,
    ingestar,
    lembrar,
    listar,
    stats,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

BRT = timezone(timedelta(hours=-3))

GH_REPO = os.environ.get("GITHUB_REPO", "Gustpbbr/Gus")
PORT = int(os.environ.get("PORT", "8080"))

# FastMCP server — host 0.0.0.0 pro Railway expor pública
mcp = FastMCP("gus-hub", host="0.0.0.0", port=PORT)


# ---------------------------------------------------------------------------
# Hub — leitura
# ---------------------------------------------------------------------------


@mcp.tool()
def buscar_hub(
    query: str,
    limit: int = 10,
    area: str = "",
    user_id: str = "gustavo",
) -> list[dict]:
    """Busca semântica no Hub Qdrant.

    Retorna fragmentos mais relevantes pra `query`, ordenados por score.
    Filtra por `area` (saude, dimagem, projetos, etc.) se informada;
    string vazia = sem filtro de área.
    Default `user_id='gustavo'` (memórias sobre o Gustavo); use `'gus'`
    pra brain do próprio agente (auto-observações).
    """
    # area="" → None pra _filtros (igual ao comportamento "sem filtro")
    area_filtro = area if area else None
    return lembrar(query=query, user_id=user_id, limit=limit, area=area_filtro)


@mcp.tool()
def ego_cache_atual(user_id: str = "gustavo") -> dict:
    """Retorna identidade operacional estável + decisões recentes + meta-reflexões.

    Usado no boot do Claude Chat pra carregar contexto vivo em vez do
    snapshot estático das 03h. Estrutura retornada:
      {
        "identidade": [...],         # tipo=identidade_operacional, estado=estavel
        "protegidos": [...],         # tipo=procedural, estado=estavel
        "decisoes_recentes": [...],  # últimas 3 decisões
        "meta_reflexoes": [...]      # últimas 5 meta-reflexões
      }
    """
    return ego_cache(user_id=user_id)


@mcp.tool()
def fragmentos_recentes(
    horas: int = 6,
    limit: int = 20,
    user_id: str = "gustavo",
) -> list[dict]:
    """Retorna fragmentos criados nas últimas `horas` horas, ordenados por timestamp desc.

    Útil pra Claude Chat ver o que outras portas (Telegram, Claude Code)
    aprenderam recentemente antes de responder.
    """
    todos = listar(user_id=user_id, limit=200)
    cutoff = datetime.now(BRT) - timedelta(hours=horas)
    recentes = []
    for frag in todos:
        criado = frag.get("criado_em")
        if not criado:
            continue
        try:
            dt = datetime.fromisoformat(criado)
            if dt >= cutoff:
                recentes.append(frag)
        except ValueError:
            continue
    # Ordena desc por criado_em e corta no limit
    recentes.sort(key=lambda f: f.get("criado_em", ""), reverse=True)
    return recentes[:limit]


@mcp.tool()
def buscar_por_tipo(
    tipo: str,
    limit: int = 10,
    user_id: str = "gustavo",
) -> list[dict]:
    """Lista fragmentos filtrados por `tipo` semântico.

    Tipos válidos (gus-18): biografico, fato, decisao, preferencia,
    identidade_operacional, episodico, meta_reflexao, projeto, rotina,
    procedural.
    """
    # Reusa lembrar com query genérica — Qdrant filter_by tipo, score só pesa pra ordenação
    return lembrar(query=tipo, user_id=user_id, limit=limit, tipo=tipo)


@mcp.tool()
def buscar_por_area(
    area: str,
    limit: int = 10,
    user_id: str = "gustavo",
) -> list[dict]:
    """Lista fragmentos filtrados por `area`.

    Áreas comuns: saude, dimagem, financeiro, projetos, capturado, gus,
    receitas, esportes.
    """
    return lembrar(query=area, user_id=user_id, limit=limit, area=area)


@mcp.tool()
def contar_fragmentos() -> dict:
    """Retorna estatísticas de contagem do Hub:
    - total de fragmentos por user_id (gustavo, gus)
    - status da coleção
    """
    return stats()


# ---------------------------------------------------------------------------
# Hub — escrita
# ---------------------------------------------------------------------------


@mcp.tool()
def ingestar_fragmento(
    conteudo: str,
    tipo: str = "episodico",
    area: str = "",
    camada_temporal: str = "sessao",
    user_id: str = "gustavo",
    confianca: float = 0.7,
) -> dict:
    """Salva um fragmento no Hub. SEMPRE marcado com `via='claude-chat'`
    pra rastreabilidade no curador.

    Use pra capturar decisões, preferências ou fatos importantes da
    conversa atual que outras portas precisam ver.

    Tipo (gus-18): episodico (default), decisao, preferencia, fato,
      biografico, identidade_operacional, meta_reflexao, projeto, rotina.
    Camada temporal: efemero, sessao (default), semana, rotina, permanente.
    """
    metadata = {
        "tipo": tipo,
        "area": area,
        "camada_temporal": camada_temporal,
        "user_id": user_id,
        "confianca": confianca,
        "via": "claude-chat",  # hardcoded — não aceitar override por segurança de auditoria
    }
    frag_id = ingestar(conteudo=conteudo, metadata=metadata)
    return {
        "ok": True,
        "id": frag_id,
        "via": "claude-chat",
        "tipo": tipo,
        "area": area,
    }


# ---------------------------------------------------------------------------
# GitHub — leitura do repo
# ---------------------------------------------------------------------------


def _gh_headers() -> Optional[dict]:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        return None
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


@mcp.tool()
def read_repo_file(path: str, ref: str = "main") -> dict:
    """Lê o conteúdo de um arquivo .md do repo GitHub (sem depender do Drive).

    `path` é relativo à raiz do repo (ex: 'projetos/gus/gus-28-acesso-hub-claude-chat.md').
    Retorna {ok, conteudo, sha, size, path}. Se GH_TOKEN ausente, retorna
    {ok: false, error}.
    """
    headers = _gh_headers()
    if not headers:
        return {"ok": False, "error": "GITHUB_TOKEN não configurado"}

    url = f"https://api.github.com/repos/{GH_REPO}/contents/{path}"
    params = {"ref": ref}
    try:
        with httpx.Client(timeout=15) as client:
            r = client.get(url, headers=headers, params=params)
        if r.status_code == 404:
            return {"ok": False, "error": f"arquivo não encontrado: {path}"}
        if r.status_code != 200:
            return {"ok": False, "error": f"GitHub {r.status_code}: {r.text[:200]}"}
        data = r.json()
        if data.get("encoding") != "base64":
            return {"ok": False, "error": f"encoding inesperado: {data.get('encoding')}"}
        import base64
        conteudo = base64.b64decode(data["content"]).decode("utf-8")
        return {
            "ok": True,
            "path": path,
            "sha": data.get("sha"),
            "size": data.get("size"),
            "conteudo": conteudo,
        }
    except (httpx.HTTPError, ValueError) as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}


@mcp.tool()
def list_repo_dir(path: str = "", ref: str = "main") -> dict:
    """Lista arquivos e subpastas de um diretório do repo GitHub.

    `path` vazio lista a raiz. Retorna {ok, items: [{name, type, path, size}]}.
    """
    headers = _gh_headers()
    if not headers:
        return {"ok": False, "error": "GITHUB_TOKEN não configurado"}

    url = f"https://api.github.com/repos/{GH_REPO}/contents/{path}"
    params = {"ref": ref}
    try:
        with httpx.Client(timeout=15) as client:
            r = client.get(url, headers=headers, params=params)
        if r.status_code == 404:
            return {"ok": False, "error": f"path não encontrado: {path}"}
        if r.status_code != 200:
            return {"ok": False, "error": f"GitHub {r.status_code}: {r.text[:200]}"}
        data = r.json()
        if not isinstance(data, list):
            return {"ok": False, "error": "path é arquivo, não diretório"}
        items = [
            {
                "name": item["name"],
                "type": item["type"],  # "file" | "dir"
                "path": item["path"],
                "size": item.get("size", 0),
            }
            for item in data
        ]
        return {"ok": True, "path": path or "/", "items": items}
    except (httpx.HTTPError, ValueError) as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}


# ---------------------------------------------------------------------------
# Auth middleware + health endpoint + run
# ---------------------------------------------------------------------------


async def health(request):
    """Endpoint público pra Railway healthcheck — sem auth."""
    return JSONResponse({"status": "ok", "service": "gus-hub-mcp"})


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware Starlette que exige `Authorization: Bearer <token>` em todas
    as rotas exceto /health. Se MCP_BEARER_TOKEN não estiver configurado,
    devolve 503 (fail-closed)."""

    def __init__(self, app, expected_header: Optional[str]):
        super().__init__(app)
        self.expected_header = expected_header

    async def dispatch(self, request, call_next):
        if request.url.path == "/health":
            return await call_next(request)

        if self.expected_header is None:
            return JSONResponse(
                {"error": "MCP_BEARER_TOKEN não configurado no servidor"},
                status_code=503,
            )

        received = request.headers.get("authorization", "")
        if not hmac.compare_digest(received, self.expected_header):
            return JSONResponse({"error": "unauthorized"}, status_code=401)

        return await call_next(request)


def _create_app() -> Starlette:
    """Monta Starlette com /health público + Mount do app MCP em /, com
    middleware de auth Bearer aplicado globalmente."""
    expected_token = os.environ.get("MCP_BEARER_TOKEN")
    if not expected_token:
        log.warning("MCP_BEARER_TOKEN ausente — server vai responder 503 em todas as rotas (exceto /health)")

    expected_header = f"Bearer {expected_token}" if expected_token else None

    mcp_app = mcp.streamable_http_app()

    app = Starlette(
        routes=[
            Route("/health", health, methods=["GET"]),
            Mount("/", app=mcp_app),
        ],
        middleware=[
            Middleware(AuthMiddleware, expected_header=expected_header),
        ],
    )
    return app


def main():
    """Entry point pra rodar via `python -m hub.mcp_server`."""
    log.info("=== MCP server boot — build 2026-04-29T19:45 ===")
    if not os.environ.get("QDRANT_URL") or not os.environ.get("QDRANT_API_KEY"):
        log.error("QDRANT_URL ou QDRANT_API_KEY ausentes")
        sys.exit(1)

    import uvicorn
    app = _create_app()
    log.info(f"MCP server iniciando na porta {PORT}")
    log.info(f"GH_REPO={GH_REPO}")
    log.info(f"Auth: {'configurado' if os.environ.get('MCP_BEARER_TOKEN') else 'AUSENTE (server vai negar)'}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()
