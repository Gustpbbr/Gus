"""
Roteador de demandas — Estágio 1 do plano de roteamento.

Move/cria/anexa conteúdo de arquivos de `dialogos/inbox-tiogu/` pra paths
finais no repo, sob aprovação explícita do Gustavo via Telegram.

3 ações suportadas:

  - criar_novo: cria arquivo NOVO em destino_path (file path completo).
                Ex: ideia → capturado/ideias/<tema>.md
  - append:    lê destino_path existente, anexa o corpo do source no fim
                com separador (heading com data BRT). Ex: resumo de chat →
                pessoal/diario/2026-04.md
  - mover:     copia source completo (com frontmatter da demanda) pra
                <destino_path>/<nome_arquivo>. Ex: caso clínico didático →
                dimagem/casos/<nome>.md (preserva contexto)

Após qualquer ação:
  - Source em dialogos/inbox-tiogu/ é atualizado: status → "concluido",
    processado_em e processado_por preenchidos, seção `## Resultado`
    adicionada ao corpo descrevendo o que foi feito
  - Workflow archive-completed-demandas.yml move source pra archive/
    em até 15min (cron próprio)

Não duplica trabalho: se source já tem status: concluido, recusa com erro.
Não vaza dados sensíveis: usa o mesmo scan de patterns_sensiveis ao salvar
em paths fora de sensivel/.
"""

import base64
import logging
import os
import re
from datetime import datetime, timedelta, timezone

import httpx
import yaml

from gus.patterns_sensiveis import escanear

logger = logging.getLogger(__name__)
BRT = timezone(timedelta(hours=-3))

ACOES_VALIDAS = {"criar_novo", "append", "mover"}

# Source path precisa estar em uma das inboxes (não restringe a tiogu —
# Estágio 2 pode usar pra outras inboxes).
INBOX_PREFIXES = (
    "dialogos/inbox-tiogu/",
    "dialogos/inbox-claude-code/",
    "dialogos/inbox-claude-chat/",
    "dialogos/inbox-custom-gpt/",
)


# ---------------------------------------------------------------------------
# FRONTMATTER
# ---------------------------------------------------------------------------

def parse_frontmatter(content: str) -> tuple[dict | None, str]:
    """Extrai frontmatter YAML do início. Retorna (dict|None, body)."""
    if not content.startswith("---"):
        return None, content
    end = content.find("\n---", 3)
    if end == -1:
        return None, content
    fm_str = content[3:end].strip()
    body = content[end + 4:].lstrip("\n")
    try:
        fm = yaml.safe_load(fm_str)
        if not isinstance(fm, dict):
            return None, content
        return fm, body
    except yaml.YAMLError:
        return None, content


def serializar_frontmatter(fm: dict) -> str:
    """Serializa dict de volta pra string YAML entre `---`."""
    yaml_str = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False).rstrip()
    return f"---\n{yaml_str}\n---\n\n"


# ---------------------------------------------------------------------------
# GITHUB API helpers
# ---------------------------------------------------------------------------

async def _gh_headers() -> dict:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN não configurado")
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


async def _gh_get(path: str) -> tuple[str | None, str | None]:
    """Lê arquivo do GitHub. Retorna (content_str, sha) ou (None, None) se 404."""
    repo = os.getenv("GITHUB_REPO", "Gustpbbr/Gus")
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = await _gh_headers()
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.get(url, headers=headers)
    if r.status_code == 404:
        return None, None
    if r.status_code != 200:
        raise RuntimeError(f"GET {path} retornou {r.status_code}: {r.text[:200]}")
    data = r.json()
    if data.get("encoding") != "base64":
        raise RuntimeError(f"GET {path} encoding inesperado: {data.get('encoding')}")
    content = base64.b64decode(data["content"]).decode("utf-8")
    return content, data.get("sha")


async def _gh_put(path: str, content: str, commit_msg: str, sha: str | None = None) -> str:
    """Cria ou atualiza arquivo. Retorna commit sha."""
    repo = os.getenv("GITHUB_REPO", "Gustpbbr/Gus")
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = await _gh_headers()
    body = {
        "message": commit_msg,
        "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
        "branch": "main",
    }
    if sha:
        body["sha"] = sha
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.put(url, headers=headers, json=body)
    if r.status_code not in (200, 201):
        raise RuntimeError(f"PUT {path} retornou {r.status_code}: {r.text[:200]}")
    return r.json().get("commit", {}).get("sha", "")


# ---------------------------------------------------------------------------
# VALIDAÇÕES
# ---------------------------------------------------------------------------

_SAFE_PATH_RE = re.compile(r"^[a-zA-Z0-9\-_./]+$")


def _validar_path(path: str) -> str:
    """Valida path — sem traversal, sem caracteres estranhos. Retorna normalizado."""
    if not path:
        raise ValueError("path vazio")
    if ".." in path:
        raise ValueError(f"traversal proibido: {path}")
    if not _SAFE_PATH_RE.match(path):
        raise ValueError(f"caracteres inválidos no path: {path}")
    return path.strip("/")


def _validar_source(source_path: str) -> None:
    """Source precisa estar em alguma inbox de dialogos/."""
    if not any(source_path.startswith(p) for p in INBOX_PREFIXES):
        raise ValueError(
            f"source deve estar em uma inbox ({', '.join(INBOX_PREFIXES)}), "
            f"recebido: {source_path}"
        )
    if not source_path.endswith(".md"):
        raise ValueError(f"source deve ser .md, recebido: {source_path}")


def _validar_destino(destino_path: str, acao: str) -> None:
    """Destino: pra criar_novo/append precisa ser file (.md). Pra mover, dir (sem .md)."""
    if acao in ("criar_novo", "append"):
        if not destino_path.endswith(".md"):
            raise ValueError(
                f"acao={acao} requer destino_path terminando em .md, recebido: {destino_path}"
            )
    elif acao == "mover":
        if destino_path.endswith(".md"):
            raise ValueError(
                f"acao=mover requer destino_path como diretório (sem .md), "
                f"recebido: {destino_path}"
            )


# ---------------------------------------------------------------------------
# AÇÕES
# ---------------------------------------------------------------------------

def _frontmatter_minimo_destino(via: str = "tiogu") -> dict:
    """Frontmatter pra arquivos novos criados pelo roteador (não-demanda)."""
    return {
        "capturado_em": datetime.now(BRT).strftime("%Y-%m-%dT%H:%M:%S"),
        "via": via,
    }


async def _acao_criar_novo(source_body: str, destino_path: str) -> tuple[str, str]:
    """Cria arquivo novo em destino_path com corpo do source (sem frontmatter de demanda).
    Retorna (commit_sha, mensagem)."""
    existente, sha = await _gh_get(destino_path)
    if existente is not None:
        raise RuntimeError(
            f"destino_path '{destino_path}' já existe — use acao=append ou outro destino"
        )

    fm_destino = _frontmatter_minimo_destino()
    conteudo = serializar_frontmatter(fm_destino) + source_body.strip() + "\n"

    folder = "/".join(destino_path.split("/")[:-1])
    if not folder.startswith("sensivel"):
        flags = escanear(conteudo)
        if flags:
            raise RuntimeError(
                f"dados sensíveis detectados ({', '.join(flags)}) — não criou em "
                f"'{destino_path}'. Mova pra sensivel/ ou peça forçar."
            )

    commit_sha = await _gh_put(
        destino_path, conteudo,
        commit_msg=f"rotear: criar_novo via tiogu em {destino_path}",
    )
    return commit_sha, f"criado novo arquivo em `{destino_path}` (commit `{commit_sha[:7]}`)"


async def _acao_append(source_body: str, destino_path: str) -> tuple[str, str]:
    """Anexa corpo do source no fim do destino_path. Retorna (commit_sha, mensagem)."""
    existente, sha = await _gh_get(destino_path)
    if existente is None:
        raise RuntimeError(
            f"destino_path '{destino_path}' não existe — use acao=criar_novo"
        )

    agora = datetime.now(BRT).strftime("%Y-%m-%d %H:%M BRT")
    separador = f"\n\n---\n\n## {agora} — apêndice via tiogu\n\n"
    novo_conteudo = existente.rstrip() + separador + source_body.strip() + "\n"

    folder = "/".join(destino_path.split("/")[:-1])
    if not folder.startswith("sensivel"):
        flags = escanear(novo_conteudo)
        if flags:
            raise RuntimeError(
                f"dados sensíveis detectados após append ({', '.join(flags)}) — "
                f"não atualizou '{destino_path}'."
            )

    commit_sha = await _gh_put(
        destino_path, novo_conteudo,
        commit_msg=f"rotear: append via tiogu em {destino_path}",
        sha=sha,
    )
    return commit_sha, f"anexado em `{destino_path}` (commit `{commit_sha[:7]}`)"


async def _acao_mover(source_path: str, source_content: str, destino_dir: str) -> tuple[str, str]:
    """Copia source completo (com frontmatter de demanda) pra <destino_dir>/<nome>.
    Retorna (commit_sha, mensagem)."""
    nome_arquivo = source_path.split("/")[-1]
    destino_path = f"{destino_dir.rstrip('/')}/{nome_arquivo}"

    existente, _ = await _gh_get(destino_path)
    if existente is not None:
        raise RuntimeError(
            f"destino '{destino_path}' já existe — escolha outro destino_path"
        )

    if not destino_dir.startswith("sensivel"):
        flags = escanear(source_content)
        if flags:
            raise RuntimeError(
                f"dados sensíveis detectados ({', '.join(flags)}) — não copiou pra "
                f"'{destino_path}'."
            )

    commit_sha = await _gh_put(
        destino_path, source_content,
        commit_msg=f"rotear: mover via tiogu pra {destino_path}",
    )
    return commit_sha, f"movido pra `{destino_path}` (commit `{commit_sha[:7]}`)"


# ---------------------------------------------------------------------------
# MARCA SOURCE COMO CONCLUÍDO
# ---------------------------------------------------------------------------

async def _marcar_source_concluido(
    source_path: str,
    source_fm: dict,
    source_body: str,
    source_sha: str,
    acao: str,
    destino_path: str,
    resultado_commit: str,
) -> str:
    """Atualiza source com status: concluido + adiciona ## Resultado. Retorna commit sha."""
    agora = datetime.now(BRT).strftime("%Y-%m-%dT%H:%M:%S")

    fm_atualizado = dict(source_fm)
    fm_atualizado["status"] = "concluido"
    fm_atualizado["processado_em"] = agora
    fm_atualizado["processado_por"] = "tiogu"

    # Remove seção `## Resultado` antiga se existir, pra não duplicar
    body_limpo = re.sub(r"\n## Resultado\b.*", "", source_body, flags=re.DOTALL).rstrip()

    bloco_resultado = (
        f"\n\n## Resultado\n\n"
        f"Roteado via tool `rotear_arquivo` em {agora} BRT.\n\n"
        f"- Ação: `{acao}`\n"
        f"- Destino: `{destino_path}`\n"
        f"- Commit: `{resultado_commit[:7] if resultado_commit else '(sem sha)'}`\n"
    )

    novo_conteudo = serializar_frontmatter(fm_atualizado) + body_limpo + bloco_resultado + "\n"

    return await _gh_put(
        source_path, novo_conteudo,
        commit_msg=f"rotear: marca {source_path} como concluido",
        sha=source_sha,
    )


# ---------------------------------------------------------------------------
# ORQUESTRAÇÃO
# ---------------------------------------------------------------------------

async def rotear_arquivo(source_path: str, destino_path: str, acao: str) -> str:
    """Roteia um arquivo de inbox-*/ pro destino_path conforme acao.

    Returns: mensagem amigável pra Gustavo (sucesso ou erro).
    """
    # Validações de input
    try:
        source_path = _validar_path(source_path)
        destino_path = _validar_path(destino_path)
        _validar_source(source_path)
    except ValueError as e:
        return f"Erro de input: {e}"

    if acao not in ACOES_VALIDAS:
        return f"Erro: acao inválida '{acao}'. Válidas: {sorted(ACOES_VALIDAS)}"

    try:
        _validar_destino(destino_path, acao)
    except ValueError as e:
        return f"Erro de input: {e}"

    # Lê source
    try:
        source_content, source_sha = await _gh_get(source_path)
    except RuntimeError as e:
        return f"Erro ao ler source: {e}"

    if source_content is None:
        return f"Erro: source '{source_path}' não encontrado"

    fm, body = parse_frontmatter(source_content)
    if fm is None:
        return (
            f"Erro: source '{source_path}' sem frontmatter — não dá pra marcar "
            f"como concluído. Edita o arquivo manualmente."
        )

    if fm.get("status") == "concluido":
        return (
            f"Source já está concluído (processado em {fm.get('processado_em', '?')}). "
            f"Nada a fazer."
        )

    # Executa ação
    try:
        if acao == "criar_novo":
            commit_sha, msg_acao = await _acao_criar_novo(body, destino_path)
        elif acao == "append":
            commit_sha, msg_acao = await _acao_append(body, destino_path)
        else:  # mover
            commit_sha, msg_acao = await _acao_mover(source_path, source_content, destino_path)
    except RuntimeError as e:
        return f"Erro ao executar acao={acao}: {e}"

    # Marca source como concluído
    try:
        await _marcar_source_concluido(
            source_path, fm, body, source_sha, acao,
            destino_path if acao != "mover" else f"{destino_path}/{source_path.split('/')[-1]}",
            commit_sha,
        )
    except RuntimeError as e:
        # Sucesso parcial: ação executou, mas marcação falhou. Reporta ambos.
        return (
            f"Parcial — {msg_acao}, mas falhou ao marcar source como concluído: {e}. "
            f"Edita o frontmatter de '{source_path}' manualmente pro archive funcionar."
        )

    return (
        f"OK. {msg_acao}. Source `{source_path}` marcado como concluído — "
        f"workflow archive-completed-demandas vai mover pra archive/ em ≤15min."
    )
