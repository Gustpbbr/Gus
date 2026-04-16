import os
import re
import asyncio
import logging
import base64
import httpx
from duckduckgo_search import DDGS

logger = logging.getLogger(__name__)

# Caracteres permitidos em nomes de arquivo e pastas
_SAFE_PATH_RE = re.compile(r"^[a-zA-Z0-9\-_/]+$")


def _validar_path(path: str) -> str:
    """Valida path contra traversal e caracteres perigosos."""
    path = path.strip().lstrip("/")
    if ".." in path:
        raise ValueError(f"Path inválido (traversal): {path}")
    if not _SAFE_PATH_RE.match(path.replace(".md", "")):
        raise ValueError(f"Path contém caracteres não permitidos: {path}")
    return path

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


async def _search_web(query: str) -> str:
    def _run():
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=5))

    try:
        results = await asyncio.to_thread(_run)
    except Exception as e:
        logger.error(f"Falha na busca web: {e}")
        return f"Erro na busca: {e}"

    if not results:
        return "Nenhum resultado encontrado."

    lines = []
    for r in results:
        lines.append(f"**{r['title']}**\n{r['body']}\nFonte: {r['href']}")
    return "\n\n---\n\n".join(lines)


async def _save_to_github(filename: str, content: str, folder: str) -> str:
    if "/" in filename or ".." in filename:
        return f"Nome de arquivo inválido: {filename}"

    try:
        folder = _validar_path(folder)
    except ValueError as e:
        return str(e)

    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPO", "Gustpbbr/Gus")

    if not token:
        return "GITHUB_TOKEN não configurado. Adicione a variável no Railway."

    path = f"{folder}/{filename}.md"
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
    elif name == "search_web":
        return await _search_web(inputs["query"])
    elif name == "save_to_github":
        return await _save_to_github(
            inputs["filename"],
            inputs["content"],
            inputs.get("folder", "capturado")
        )
    return f"Tool desconhecida: {name}"
