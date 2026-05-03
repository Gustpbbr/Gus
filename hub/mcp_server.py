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
  MCP_BEARER_TOKEN    — auth header (Bearer). Funciona em Claude Desktop,
                        Claude Code, Cursor. claude.ai web NÃO suporta
                        custom headers — usar MCP_URL_SECRET pra esses casos.
  MCP_AUTH_DISABLED   — se "true", desliga AuthMiddleware (sem Bearer check).
                        Combina com MCP_URL_SECRET pra privacidade no
                        claude.ai web. Sem nenhum dos dois = público total.
  MCP_URL_SECRET      — se setado, monta o app MCP em `/{secret}` em vez de `/`.
                        Endpoint final vira `/{secret}/mcp`. "Shared secret in URL"
                        — modelo igual webhook do Slack/GitHub. Usado pra dar
                        privacidade prática no claude.ai web (que só aceita
                        OAuth, não Bearer). Ingestão fica habilitada se houver
                        ESSE secret OU Bearer ativo.
  GITHUB_TOKEN        — repo tools (opcional, sem ele tools repo retornam 503)
  GITHUB_REPO         — default "Gustpbbr/Gus"
  PORT                — default 8080 (Railway injeta automaticamente; NÃO setar manual)
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


def _is_auth_disabled() -> bool:
    """AuthMiddleware desligado via MCP_AUTH_DISABLED=true. Use junto com
    MCP_URL_SECRET pra ainda ter privacidade prática no claude.ai web."""
    return os.environ.get("MCP_AUTH_DISABLED", "").lower() == "true"


def _url_secret() -> str:
    """Segredo no path: se setado, MCP é montado em /{secret} em vez de /.
    Vazio = mount em / (modo legado / público explícito)."""
    return os.environ.get("MCP_URL_SECRET", "").strip()


def _has_access_control() -> bool:
    """True se as requests são gated por Bearer OU URL secret.
    Quando False, ingestar_fragmento é bloqueado (modo público total)."""
    if not _is_auth_disabled() and os.environ.get("MCP_BEARER_TOKEN"):
        return True
    if _url_secret():
        return True
    return False


# Brains válidos pra escrita via MCP. `gustavo` = fatos sobre Gustavo,
# `gus` = autobiografia do agente. Sem whitelist, Chat poderia salvar
# fragmento sob `user_id` arbitrário e quebrar invariante dos brains.
ALLOWED_USER_IDS = {"gustavo", "gus"}


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
    if not _has_access_control():
        return {
            "ok": False,
            "error": "Read-only mode: sem auth (Bearer) nem URL secret configurados. "
                     "Setar MCP_URL_SECRET ou MCP_BEARER_TOKEN pra reativar escrita.",
        }
    if user_id not in ALLOWED_USER_IDS:
        return {
            "ok": False,
            "error": f"user_id inválido: {user_id!r}. Aceitos: {sorted(ALLOWED_USER_IDS)}",
        }
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
    """Monta Starlette com /health público + Mount do app MCP.

    Path do mount:
      - MCP_URL_SECRET setado → `/{secret}` (endpoint final: `/{secret}/mcp`)
      - vazio → `/` (endpoint legado: `/mcp`)

    Auth:
      - MCP_AUTH_DISABLED=true → AuthMiddleware desligado
      - caso contrário → AuthMiddleware exige Bearer == MCP_BEARER_TOKEN

    IMPORTANTE: passa `lifespan=mcp_app.router.lifespan_context` pro Starlette
    wrapper. Sem isso, o session_manager do FastMCP não inicializa e qualquer
    POST /mcp explode com `RuntimeError: Task group is not initialized`.
    Esse foi o bug que impedia claude.ai Connector de conectar (29-30/04).
    """
    mcp_app = mcp.streamable_http_app()
    secret = _url_secret()
    mount_path = f"/{secret}" if secret else "/"
    routes = [
        Route("/health", health, methods=["GET"]),
        Mount(mount_path, app=mcp_app),
    ]
    # Reusa o lifespan do mcp_app — sem isso o session_manager fica órfão
    lifespan = mcp_app.router.lifespan_context

    if secret:
        # NUNCA logar o valor do secret — vaza pra logs Railway, transcripts
        # Code (via Stop hook), e qualquer pessoa com read access. Mostrar só
        # que está ativo + tamanho pra debug.
        log.info(f"MCP montado em /<URL_SECRET ({len(secret)} chars)>/mcp")
    else:
        log.info("MCP montado em /mcp (sem URL secret)")

    if _is_auth_disabled():
        if not secret:
            # Fail-closed: sem Bearer E sem URL secret = expor todo o Hub
            # publicamente (Dimagem, saúde, financeiro, identidade) pra qualquer
            # scanner que descubra o domínio Railway. Antes (V1) só logava warning
            # — agora retorna 503 em tudo (exceto /health) até alguém configurar
            # um dos dois. Setar MCP_AUTH_DISABLED=false pra reativar Bearer, OU
            # MCP_URL_SECRET pra usar shared secret no path.
            log.error("=" * 60)
            log.error("FAIL-CLOSED: MCP_AUTH_DISABLED=true sem MCP_URL_SECRET")
            log.error("Server vai retornar 503 em tudo (exceto /health).")
            log.error("Reative auth: MCP_URL_SECRET=<32+ chars> ou MCP_AUTH_DISABLED=false")
            log.error("=" * 60)
            return Starlette(
                routes=routes,
                middleware=[Middleware(AuthMiddleware, expected_header=None)],
                lifespan=lifespan,
            )
        log.info("Bearer auth desligada (MCP_AUTH_DISABLED=true) — privacidade vem do URL secret")
        return Starlette(routes=routes, middleware=[], lifespan=lifespan)

    expected_token = os.environ.get("MCP_BEARER_TOKEN")
    if not expected_token:
        log.warning("MCP_BEARER_TOKEN ausente — server vai responder 503 em todas as rotas (exceto /health)")

    expected_header = f"Bearer {expected_token}" if expected_token else None
    return Starlette(
        routes=routes,
        middleware=[Middleware(AuthMiddleware, expected_header=expected_header)],
        lifespan=lifespan,
    )


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
    if _is_auth_disabled():
        log.info("Auth: Bearer DESABILITADA (MCP_AUTH_DISABLED=true)")
    else:
        log.info(f"Auth: Bearer {'configurado' if os.environ.get('MCP_BEARER_TOKEN') else 'AUSENTE (server vai negar)'}")
    log.info(f"URL secret: {'ativo (path /<secret>/mcp)' if _url_secret() else 'sem secret (path /mcp)'}")
    log.info(f"Escrita: {'habilitada' if _has_access_control() else 'BLOQUEADA (read-only)'}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()
