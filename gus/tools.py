import os
import re
import asyncio
import logging
import base64
from datetime import datetime, timezone, timedelta
import httpx
from duckduckgo_search import DDGS
from gus.memory import buscar_memorias_detalhada

logger = logging.getLogger(__name__)

BRT = timezone(timedelta(hours=-3))

# Caracteres permitidos em nomes de arquivo e pastas
_SAFE_PATH_RE = re.compile(r"^[a-zA-Z0-9\-_/]+$")

# Padrões de dados sensíveis pra escaneamento antes de salvar
_PATTERNS_SENSIVEIS = {
    "CPF":              re.compile(r"\b\d{3}[.\s]?\d{3}[.\s]?\d{3}[-\s]?\d{2}\b"),
    "CNPJ":             re.compile(r"\b\d{2}[.\s]?\d{3}[.\s]?\d{3}/?\d{4}[-\s]?\d{2}\b"),
    "cartão":           re.compile(r"\b(?:\d[ -]?){13,19}\b"),
    "API key Anthropic":re.compile(r"\bsk-ant-[\w-]{20,}\b"),
    "API key OpenAI":   re.compile(r"\bsk-[A-Za-z0-9]{40,}\b"),
    "GitHub PAT":       re.compile(r"\b(?:ghp_|github_pat_)[\w]{20,}\b"),
    "Mem0 key":         re.compile(r"\bm0-[\w]{20,}\b"),
    "Tavily key":       re.compile(r"\btvly-[\w]{20,}\b"),
}


def _validar_path(path: str) -> str:
    """Valida path contra traversal e caracteres perigosos."""
    path = path.strip().lstrip("/")
    if ".." in path:
        raise ValueError(f"Path inválido (traversal): {path}")
    if not _SAFE_PATH_RE.match(path.replace(".md", "")):
        raise ValueError(f"Path contém caracteres não permitidos: {path}")
    return path


def _escanear_sensivel(content: str) -> list[str]:
    """Retorna lista dos tipos de dados sensíveis encontrados no texto."""
    encontrados = []
    for nome, padrao in _PATTERNS_SENSIVEIS.items():
        if padrao.search(content):
            encontrados.append(nome)
    return encontrados

TOOLS = [
    {
        "name": "read_from_github",
        "description": (
            "Lê o conteúdo de um arquivo Markdown do repositório do Gustavo no GitHub. "
            "Use quando precisar de contexto específico de um projeto, histórico de saúde, "
            "exames anteriores, decisões passadas, ou qualquer informação estruturada salva. "
            "Exemplos de paths: 'pessoal/saude/historico-saude.md', "
            "'phronesis-bench/semantico/phronesis-00-briefing.md', 'capturado/insight-x.md'."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Caminho completo do arquivo no repositório, incluindo extensão (ex: 'pessoal/saude/historico-saude.md')"
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "list_github_directory",
        "description": (
            "Lista o conteúdo (arquivos e subpastas) de uma pasta do repositório do Gustavo "
            "no GitHub. Use ANTES de chutar paths — quando o usuário perguntar o que existe "
            "em uma área, ou quando você não tem certeza se um arquivo específico existe. "
            "Retorna nomes de arquivos e pastas. Para listar a raiz do repo, passe path vazio "
            "ou '.'."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Caminho da pasta no repositório (ex: 'pessoal/saude', 'projetos/gus'). Vazio ou '.' para a raiz."
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "list_commits",
        "description": (
            "Lista commits recentes do repositório. Use quando o usuário perguntar sobre "
            "histórico, o que mudou, quando foi editado, quem modificou — qualquer coisa "
            "temporal ou de autoria. Pode filtrar por path (pasta ou arquivo) e por janela "
            "de dias. Retorna hash curto, data em horário de Brasília, autor e mensagem de "
            "cada commit."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path do arquivo ou pasta pra filtrar. Ex: 'projetos/gus', 'pessoal/saude/historico-saude.md'. Vazio pra commits do repo inteiro."
                },
                "limit": {
                    "type": "integer",
                    "description": "Quantidade máxima de commits a retornar (1 a 30). Default 10."
                },
                "since_days": {
                    "type": "integer",
                    "description": "Filtrar só commits dos últimos N dias. 0 ou omitido pra sem filtro temporal."
                }
            },
            "required": []
        }
    },
    {
        "name": "search_memory",
        "description": (
            "Busca memórias do Gustavo no Mem0 de forma ativa (por query específica). "
            "Use quando o usuário perguntar sobre memórias recentes, ou quando você precisar "
            "de contexto adicional além do que já foi injetado passivamente no início da "
            "conversa. Retorna as memórias mais semanticamente próximas da query."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Busca em linguagem natural (ex: 'projetos ativos', 'saúde recente', 'decisões sobre o Gus', 'construção da casa')"
                },
                "limit": {
                    "type": "integer",
                    "description": "Número máximo de memórias a retornar (1 a 20). Default 10."
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "search_web",
        "description": (
            "Busca informações atuais na web. Use quando não tiver certeza sobre fatos recentes, "
            "eventos atuais, preços, notícias, dados técnicos ou qualquer coisa que precise de "
            "fonte externa para confirmar."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Termos de busca em português ou inglês"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "save_to_github",
        "description": (
            "Salva conteúdo como arquivo Markdown no repositório do Gustavo no GitHub. "
            "Use quando o usuário pedir explicitamente pra salvar, quando houver um insight "
            "importante que mereça ser preservado, ou após analisar um documento relevante."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Nome do arquivo sem extensão (ex: 'exame-jan-2026', 'insight-phronesis')"
                },
                "content": {
                    "type": "string",
                    "description": "Conteúdo completo do arquivo em Markdown"
                },
                "folder": {
                    "type": "string",
                    "description": (
                        "Pasta no repositório. Use a mais específica possível: "
                        "'pessoal/saude' para exames, 'phronesis-bench' para Phronesis, "
                        "'mge' para MGE/MGX, 'ter' para TER, 'axon' para Axon, "
                        "'capturado' para capturas gerais sem projeto definido."
                    )
                }
            },
            "required": ["filename", "content", "folder"]
        }
    }
]


async def _read_from_github(path: str) -> str:
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

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(url, headers=headers)

    if response.status_code == 404:
        return f"Arquivo não encontrado: `{path}`"
    if response.status_code != 200:
        return f"Erro ao ler do GitHub: {response.status_code}"

    data = response.json()
    content = base64.b64decode(data["content"]).decode("utf-8")
    return content


async def _list_github_directory(path: str) -> str:
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

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(url, headers=headers)

    if response.status_code == 404:
        return f"Pasta não encontrada: `{path or '.'}`"
    if response.status_code != 200:
        return f"Erro ao listar GitHub: {response.status_code}"

    items = response.json()
    if not isinstance(items, list):
        return f"`{path}` é um arquivo, não uma pasta. Use read_from_github pra ler."

    pastas = sorted([i["name"] for i in items if i["type"] == "dir"])
    arquivos = sorted([i["name"] for i in items if i["type"] == "file"])

    linhas = [f"Conteúdo de `{path or '(raiz)'}`:"]
    if pastas:
        linhas.append("\n**Pastas:**")
        linhas.extend(f"- {p}/" for p in pastas)
    if arquivos:
        linhas.append("\n**Arquivos:**")
        linhas.extend(f"- {a}" for a in arquivos)
    if not pastas and not arquivos:
        linhas.append("(vazio)")
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


async def _search_tavily(query: str) -> str | None:
    """Busca via Tavily API. Retorna string formatada ou None se falhar."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return None

    payload = {
        "api_key": api_key,
        "query": query,
        "max_results": 5,
        "search_depth": "basic",
    }
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post("https://api.tavily.com/search", json=payload)
        if response.status_code != 200:
            logger.warning(f"Tavily retornou {response.status_code}: {response.text[:200]}")
            return None
        results = response.json().get("results", [])
    except Exception as e:
        logger.warning(f"Tavily falhou: {e}")
        return None

    if not results:
        return None

    lines = [f"**{r['title']}**\n{r['content']}\nFonte: {r['url']}" for r in results]
    return "\n\n---\n\n".join(lines)


async def _search_ddg(query: str) -> str:
    """Fallback: busca via DuckDuckGo."""
    def _run():
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=5))

    try:
        results = await asyncio.to_thread(_run)
    except Exception as e:
        logger.error(f"Falha na busca web (DDG): {e}")
        return f"Erro na busca: {e}"

    if not results:
        return "Nenhum resultado encontrado."

    lines = [f"**{r['title']}**\n{r['body']}\nFonte: {r['href']}" for r in results]
    return "\n\n---\n\n".join(lines)


async def _search_web(query: str) -> str:
    """Tenta Tavily primeiro; se falhar ou sem chave, cai pro DuckDuckGo."""
    tavily_result = await _search_tavily(query)
    if tavily_result:
        return tavily_result
    return await _search_ddg(query)


async def _save_to_github(filename: str, content: str, folder: str) -> str:
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
        f"via: telegram\n"
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


async def executar_tool(name: str, inputs: dict) -> str:
    if name == "read_from_github":
        return await _read_from_github(inputs["path"])
    elif name == "list_github_directory":
        return await _list_github_directory(inputs.get("path", ""))
    elif name == "list_commits":
        return await _list_commits(
            inputs.get("path", ""),
            inputs.get("limit", 10),
            inputs.get("since_days", 0)
        )
    elif name == "search_memory":
        try:
            limit = max(1, min(int(inputs.get("limit", 10)), 20))
        except (TypeError, ValueError):
            limit = 10
        return await buscar_memorias_detalhada(inputs["query"], limit)
    elif name == "search_web":
        return await _search_web(inputs["query"])
    elif name == "save_to_github":
        return await _save_to_github(
            inputs["filename"],
            inputs["content"],
            inputs.get("folder", "capturado")
        )
    return f"Tool desconhecida: {name}"
