"""Tools de interação com GitHub via REST API.

Funções:
  - _read_from_github(path, branch?)
  - _list_github_directory(path, branch?)
  - _list_branches()
  - _list_commits(path, limit, since_days)
  - _save_to_github(filename, content, folder, via?)
  - _disparar_workflow(workflow_name, branch?)

Validação de path em `_utils._validar_path` (anti-traversal). Save scan
de PII via `_utils._escanear_sensivel` quando folder não é `sensivel/*`.
"""

import os
import re
import base64
import asyncio
import logging
from datetime import datetime, timezone, timedelta

import httpx

from gus.tools._utils import BRT, _validar_path, _escanear_sensivel

logger = logging.getLogger(__name__)


async def _read_from_github(path: str, branch: str | None = None) -> str:
    try:
        path = _validar_path(path)
    except ValueError as e:
        return str(e)

    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPO", "Gustpbbr/Gus")

    if not token:
        return "GITHUB_TOKEN não configurado."

    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    params = {"ref": branch} if branch else None

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(url, headers=headers, params=params)

    if response.status_code == 404:
        ref_msg = f" (branch={branch})" if branch else ""
        return f"Arquivo não encontrado: `{path}`{ref_msg}"
    if response.status_code != 200:
        return f"Erro ao ler do GitHub: {response.status_code}"

    data = response.json()
    content = base64.b64decode(data["content"]).decode("utf-8")
    return content


async def _list_github_directory(path: str, branch: str | None = None) -> str:
    """Lista arquivos e pastas de um diretório no repositório GitHub."""
    path = (path or "").strip().strip("/")
    if path and path != ".":
        try:
            path = _validar_path(path)
        except ValueError as e:
            return str(e)
    else:
        path = ""

    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPO", "Gustpbbr/Gus")

    if not token:
        return "GITHUB_TOKEN não configurado."

    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    params = {"ref": branch} if branch else None

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(url, headers=headers, params=params)

    if response.status_code == 404:
        ref_msg = f" (branch={branch})" if branch else ""
        return f"Pasta não encontrada: `{path or '.'}`{ref_msg}"
    if response.status_code != 200:
        return f"Erro ao listar GitHub: {response.status_code}"

    items = response.json()
    if not isinstance(items, list):
        return f"`{path}` é um arquivo, não uma pasta. Use read_from_github pra ler."

    pastas = sorted([i["name"] for i in items if i["type"] == "dir"])
    arquivos = sorted([i["name"] for i in items if i["type"] == "file"])

    branch_label = f" @ `{branch}`" if branch else ""
    linhas = [f"Conteúdo de `{path or '(raiz)'}`{branch_label}:"]
    if pastas:
        linhas.append("\n**Pastas:**")
        linhas.extend(f"- {p}/" for p in pastas)
    if arquivos:
        linhas.append("\n**Arquivos:**")
        linhas.extend(f"- {a}" for a in arquivos)
    if not pastas and not arquivos:
        linhas.append("(vazio)")
    return "\n".join(linhas)


async def _list_branches() -> str:
    """Lista todas as branches do repositório com info do último commit."""
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPO", "Gustpbbr/Gus")

    if not token:
        return "GITHUB_TOKEN não configurado."

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    url_branches = f"https://api.github.com/repos/{repo}/branches"
    url_repo = f"https://api.github.com/repos/{repo}"

    async with httpx.AsyncClient(timeout=30) as client:
        resp_b, resp_r = await asyncio.gather(
            client.get(url_branches, headers=headers, params={"per_page": 100}),
            client.get(url_repo, headers=headers),
        )

    if resp_b.status_code != 200:
        return f"Erro ao listar branches: {resp_b.status_code}"

    default_branch = "main"
    if resp_r.status_code == 200:
        default_branch = resp_r.json().get("default_branch", "main")

    branches = resp_b.json()
    if not branches:
        return "Nenhuma branch encontrada."

    # Pra cada branch, busca info do último commit em paralelo
    async def _commit_info(branch_name: str) -> dict:
        url_commit = f"https://api.github.com/repos/{repo}/commits/{branch_name}"
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(url_commit, headers=headers)
        if r.status_code != 200:
            return {"branch": branch_name, "sha": "?", "autor": "?", "data": "?", "msg": "(erro)"}
        d = r.json()
        autor = d.get("commit", {}).get("author", {})
        return {
            "branch": branch_name,
            "sha": d.get("sha", "")[:7],
            "autor": autor.get("name", "?"),
            "data": (autor.get("date") or "")[:10],
            "msg": (d.get("commit", {}).get("message") or "").splitlines()[0][:60],
        }

    infos = await asyncio.gather(
        *(_commit_info(b["name"]) for b in branches),
        return_exceptions=True,
    )

    linhas = [f"**{len(branches)} branches** (default: `{default_branch}`)\n"]
    for info in infos:
        if isinstance(info, Exception):
            continue
        marker = " ⭐" if info["branch"] == default_branch else ""
        linhas.append(
            f"- `{info['branch']}`{marker} — {info['sha']} · "
            f"{info['data']} · {info['autor']} · {info['msg']}"
        )
    return "\n".join(linhas)


async def _list_commits(path: str = "", limit: int = 10, since_days: int = 0) -> str:
    """Lista commits recentes, opcionalmente filtrados por path e período."""
    path = (path or "").strip().strip("/")
    if path and path != ".":
        try:
            path = _validar_path(path)
        except ValueError as e:
            return str(e)
    else:
        path = ""

    try:
        limit = max(1, min(int(limit), 30))
    except (TypeError, ValueError):
        limit = 10

    try:
        since_days = int(since_days) if since_days else 0
    except (TypeError, ValueError):
        since_days = 0

    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPO", "Gustpbbr/Gus")

    if not token:
        return "GITHUB_TOKEN não configurado."

    params: dict = {"per_page": limit}
    if path:
        params["path"] = path
    if since_days > 0:
        since_dt = datetime.now(BRT) - timedelta(days=since_days)
        params["since"] = since_dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    url = f"https://api.github.com/repos/{repo}/commits"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(url, params=params, headers=headers)

    if response.status_code == 404:
        return f"Path não encontrado no repo: `{path}`" if path else "Repositório não encontrado."
    if response.status_code != 200:
        return f"Erro ao listar commits: {response.status_code}"

    commits = response.json()
    if not commits:
        contexto = []
        if path:
            contexto.append(f"em `{path}`")
        if since_days:
            contexto.append(f"nos últimos {since_days} dia(s)")
        return f"Nenhum commit encontrado {' '.join(contexto)}.".strip()

    cabecalho = "Últimos "
    if path and since_days:
        cabecalho = f"Commits em `{path}` nos últimos {since_days} dia(s):"
    elif path:
        cabecalho = f"Últimos {len(commits)} commits em `{path}`:"
    elif since_days:
        cabecalho = f"Commits dos últimos {since_days} dia(s):"
    else:
        cabecalho = f"Últimos {len(commits)} commits do repositório:"

    linhas = [cabecalho]
    for c in commits:
        sha_curto = c.get("sha", "")[:7]
        commit = c.get("commit", {})
        mensagem = commit.get("message", "").split("\n")[0]
        autor = commit.get("author", {}).get("name", "?")
        data_iso = commit.get("author", {}).get("date", "")
        try:
            dt_utc = datetime.fromisoformat(data_iso.replace("Z", "+00:00"))
            data_fmt = dt_utc.astimezone(BRT).strftime("%Y-%m-%d %H:%M")
        except Exception:
            data_fmt = data_iso[:16]
        linhas.append(f"- `{sha_curto}` {data_fmt} — {autor} — {mensagem}")

    return "\n".join(linhas)


async def _save_to_github(filename: str, content: str, folder: str, via: str = "telegram") -> str:
    if "/" in filename or ".." in filename:
        return f"Nome de arquivo inválido: {filename}"

    try:
        folder = _validar_path(folder)
    except ValueError as e:
        return str(e)

    # Scan de dados sensíveis — só alerta se path NÃO for sensivel/*
    if not folder.startswith("sensivel"):
        flags = _escanear_sensivel(content)
        if flags:
            return (
                f"ATENÇÃO — dados sensíveis detectados: {', '.join(flags)}.\n"
                f"Este conteúdo NÃO foi salvo. Pergunte ao Gustavo como prosseguir:\n"
                f"  (a) salvar em 'sensivel/{folder}/' ou subpasta de 'sensivel/' (não espelha no Drive)\n"
                f"  (b) forçar o save no path original '{folder}/' mesmo com dados sensíveis\n"
                f"  (c) cancelar\n"
                f"Se (a) ou (b), chamar save_to_github de novo com o folder ajustado. "
                f"Se vier nova confirmação explícita, pode salvar."
            )

    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPO", "Gustpbbr/Gus")

    if not token:
        return "GITHUB_TOKEN não configurado. Adicione a variável no Railway."

    path = f"{folder}/{filename}.md"

    now = datetime.now(BRT)
    frontmatter = (
        f"---\n"
        f"capturado_em: {now.strftime('%Y-%m-%dT%H:%M:%S')}\n"
        f"via: {via}\n"
        f"---\n\n"
    )
    if not content.startswith("---\n"):
        content = frontmatter + content

    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    encoded = base64.b64encode(content.encode()).decode()

    async with httpx.AsyncClient(timeout=30) as client:
        # Verifica se arquivo já existe (pega sha para update)
        sha = None
        check = await client.get(url, headers=headers)
        if check.status_code == 200:
            sha = check.json().get("sha")

        payload = {
            "message": f"capture: {filename} via Gus",
            "content": encoded,
            "branch": "main"
        }
        if sha:
            payload["sha"] = sha

        response = await client.put(url, json=payload, headers=headers)

    if response.status_code in (200, 201):
        action = "Atualizado" if sha else "Salvo"
        return f"{action} em `{path}` no repositório."
    else:
        logger.error(f"GitHub API error: {response.status_code} {response.text[:300]}")
        return f"Erro ao salvar no GitHub: {response.status_code}"


async def _disparar_workflow(workflow_name: str, branch: str = "main") -> str:
    """Dispara um workflow via GitHub Actions API (workflow_dispatch)."""
    if not re.match(r"^[a-z0-9\-]+\.ya?ml$", workflow_name):
        return f"Nome inválido: `{workflow_name}`. Use formato tipo 'meta-memoria.yml'."

    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPO", "Gustpbbr/Gus")
    if not token:
        return "GITHUB_TOKEN não configurado."

    url = f"https://api.github.com/repos/{repo}/actions/workflows/{workflow_name}/dispatches"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    payload = {"ref": branch or "main"}

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, json=payload, headers=headers)
    except Exception as e:
        return f"Erro de rede ao disparar workflow: {e}"

    if response.status_code == 204:
        return (
            f"Workflow `{workflow_name}` disparado em branch `{branch}`. "
            f"Acompanhe em https://github.com/{repo}/actions."
        )
    if response.status_code == 404:
        return (
            f"Workflow `{workflow_name}` não encontrado. Confirme o nome em "
            f"`.github/workflows/` via list_github_directory."
        )
    if response.status_code == 403:
        return (
            f"Sem permissão pra disparar workflow (HTTP 403). "
            f"O GITHUB_TOKEN precisa de escopo 'Actions: Read and write'. "
            f"Gustavo atualiza em github.com/settings/tokens editando o PAT existente."
        )
    if response.status_code == 422:
        return (
            f"GitHub rejeitou o dispatch (422). Normalmente significa que o workflow "
            f"não tem `workflow_dispatch:` no trigger, ou o branch `{branch}` não existe."
        )
    return f"Erro inesperado {response.status_code}: {response.text[:200]}"
