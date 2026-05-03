#!/usr/bin/env python3
"""
Import recursivo de Gus-Sync/dialogos/ no Drive pra dialogos/ no GitHub.

Fluxo por execução (cron 15min):
  1. Varre Gus-Sync/dialogos/ recursivo no Drive (skip processados/)
  2. Pra cada arquivo de texto encontrado:
     a. Baixa conteúdo (Google Doc → exporta markdown; .md/text → baixa direto)
     b. Decide modo pelo path relativo:
        - Profundidade 1 dentro de inbox-*/  →  modo demanda:
            valida frontmatter, commita, move arquivo no Drive pra processados/
        - Qualquer outro caminho dentro de dialogos/  →  modo mirror:
            commita raw no GitHub no path correspondente, idempotente
            (não move, não valida, não notifica)
     c. Se inbox-tiogu (modo demanda): notifica Telegram

Idempotência (modo mirror): antes de cada PUT, compara com conteúdo já no GitHub.
Se idêntico, skip — quebra o loop com sync-to-drive (que mirrora o caminho oposto).
"""

import base64
import logging
import os
import re
import sys
from datetime import datetime, timezone, timedelta

import httpx
import yaml
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

# Helper compartilhado de auth Drive (WIF preferred, SA JSON e OAuth fallback)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _drive_auth import get_drive_service

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

BRT = timezone(timedelta(hours=-3))

PORTAS_VALIDAS = {"claude-chat", "tiogu", "claude-code", "custom-gpt", "gustavo"}
# Inboxes que recebem demandas com frontmatter formal (validado).
INBOXES = ["inbox-tiogu", "inbox-claude-code", "inbox-claude-chat", "inbox-custom-gpt"]
# Inboxes que recebem qualquer .md (sem frontmatter), usadas pra captura
# bruta. Não validam, mas movem pra processados/ pra não reprocessar.
# Conteúdo é processado por outro cron downstream (ex: ingest-chat-raw).
INBOXES_RAW = ["inbox-chat-raw"]
PROCESSADOS_FOLDER = "processados"
PROCESSADOS_ERRO_FOLDER = "processados-erro"

# Mimes considerados texto pra mirror raw. Outros tipos (imagens, binários) são
# ignorados com warning — Drive pode ter qualquer coisa, repo só aceita texto.
TEXT_MIMES_PREFIX = ("text/",)
TEXT_MIMES_EXTRA = {"application/vnd.google-apps.document"}


def get_drive():
    return get_drive_service()


def get_or_create_folder(drive, name, parent_id):
    safe = name.replace("'", "\\'")
    q = (
        f"name = '{safe}' and '{parent_id}' in parents "
        f"and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    )
    r = drive.files().list(q=q, fields="files(id, name)", pageSize=1).execute()
    files = r.get("files", [])
    if files:
        return files[0]["id"]
    folder = drive.files().create(
        body={"name": name, "mimeType": "application/vnd.google-apps.folder", "parents": [parent_id]},
        fields="id",
    ).execute()
    log.info(f"Pasta criada no Drive: {name}")
    return folder["id"]


def find_folder_by_path(drive, path, root_id):
    """Resolve path tipo 'dialogos/inbox-tiogu' relativo a root_id."""
    parts = [p for p in path.split("/") if p]
    current = root_id
    for part in parts:
        safe = part.replace("'", "\\'")
        q = (
            f"name = '{safe}' and '{current}' in parents "
            f"and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        )
        r = drive.files().list(q=q, fields="files(id, name)", pageSize=1).execute()
        files = r.get("files", [])
        if not files:
            return None
        current = files[0]["id"]
    return current


def list_files_in_folder(drive, folder_id):
    """Lista arquivos (não-folders) na pasta."""
    q = f"'{folder_id}' in parents and trashed = false and mimeType != 'application/vnd.google-apps.folder'"
    fields = "files(id, name, mimeType, modifiedTime)"
    r = drive.files().list(q=q, fields=fields, pageSize=200).execute()
    return r.get("files", [])


def walk_drive_recursive(drive, folder_id, prefix=""):
    """Yield (file_dict, prefix) pra todos os arquivos sob folder_id, recursivo.

    `prefix` é o path relativo (com `/` final, ou string vazia na raiz). Pula
    as subpastas `processados/` e `processados-erro/` na raiz pra não
    reimportar arquivos já archivados (sucesso ou falha).
    """
    q = f"'{folder_id}' in parents and trashed = false"
    fields = "nextPageToken, files(id, name, mimeType, modifiedTime)"
    page_token = None
    while True:
        kwargs = {"q": q, "fields": fields, "pageSize": 200}
        if page_token:
            kwargs["pageToken"] = page_token
        r = drive.files().list(**kwargs).execute()
        for f in r.get("files", []):
            if f["mimeType"] == "application/vnd.google-apps.folder":
                if prefix == "" and f["name"] in (PROCESSADOS_FOLDER, PROCESSADOS_ERRO_FOLDER):
                    continue
                yield from walk_drive_recursive(drive, f["id"], prefix + f["name"] + "/")
            else:
                yield f, prefix
        page_token = r.get("nextPageToken")
        if not page_token:
            break


def is_text_mime(mime):
    if mime in TEXT_MIMES_EXTRA:
        return True
    return any(mime.startswith(p) for p in TEXT_MIMES_PREFIX)


def download_content(drive, file_id, mime_type):
    """Retorna conteúdo como str. Google Doc → exporta markdown. .md → baixa raw."""
    if mime_type == "application/vnd.google-apps.document":
        # Exporta como text/markdown (suportado desde 2024 pelo Drive API)
        r = drive.files().export(fileId=file_id, mimeType="text/markdown").execute()
        return r.decode("utf-8") if isinstance(r, bytes) else r
    else:
        # Texto plano / markdown direto
        r = drive.files().get_media(fileId=file_id).execute()
        return r.decode("utf-8") if isinstance(r, bytes) else r


def move_file(drive, file_id, new_parent_id, current_parents):
    """Move arquivo no Drive pra outra pasta (remove de parents atuais, adiciona no novo)."""
    drive.files().update(
        fileId=file_id,
        addParents=new_parent_id,
        removeParents=",".join(current_parents),
        fields="id, parents",
    ).execute()


def parse_frontmatter(content):
    """Extrai frontmatter YAML do início do .md. Retorna (dict, body) ou (None, content_inteiro)."""
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
    except yaml.YAMLError as e:
        log.warning(f"Frontmatter YAML inválido: {e}")
        return None, content


def validate_frontmatter(fm, file_name):
    """Retorna lista de erros (vazia se OK)."""
    erros = []
    obrig = ["tipo", "origem", "destino", "prioridade", "status", "criado_em"]
    for k in obrig:
        if k not in fm:
            erros.append(f"campo obrigatório ausente: {k}")
    if erros:
        return erros

    if fm.get("tipo") != "demanda":
        erros.append(f"tipo deve ser 'demanda', recebeu '{fm.get('tipo')}'")

    if fm.get("origem") not in PORTAS_VALIDAS:
        erros.append(f"origem inválida: {fm.get('origem')} (válidas: {sorted(PORTAS_VALIDAS)})")

    if fm.get("destino") not in PORTAS_VALIDAS:
        erros.append(f"destino inválido: {fm.get('destino')} (válidas: {sorted(PORTAS_VALIDAS)})")

    if fm.get("origem") == fm.get("destino"):
        erros.append(f"origem == destino ({fm.get('origem')}) — sem sentido enfileirar pra si mesma")

    return erros


def github_put_file(repo, path, content_str, commit_message, gh_token):
    """Cria ou atualiza arquivo no GitHub via Contents API.

    Idempotente: se o arquivo já existe e o conteúdo é byte-idêntico ao que
    seria escrito, retorna ("unchanged", True) sem PUT — evita commit no-op
    e quebra loop com sync-to-drive.
    Retorna ("created"|"updated"|"unchanged", success_bool).
    """
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {gh_token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    sha = None
    with httpx.Client(timeout=30) as client:
        r = client.get(url, headers=headers)
        if r.status_code == 200:
            data = r.json()
            sha = data.get("sha")
            if data.get("encoding") == "base64":
                try:
                    existing = base64.b64decode(data["content"]).decode("utf-8")
                    if existing == content_str:
                        return "unchanged", True
                except (ValueError, UnicodeDecodeError):
                    pass
        elif r.status_code != 404:
            log.warning(f"GET {url} retornou {r.status_code}: {r.text[:200]}")

    body = {
        "message": commit_message,
        "content": base64.b64encode(content_str.encode("utf-8")).decode("ascii"),
    }
    if sha:
        body["sha"] = sha

    with httpx.Client(timeout=30) as client:
        r = client.put(url, headers=headers, json=body)
        if r.status_code in (200, 201):
            return ("updated" if sha else "created"), True
        log.error(f"GitHub PUT {url} falhou ({r.status_code}): {r.text[:300]}")
        return "error", False


def notify_telegram(message):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        log.info("Telegram secrets ausentes, notificação pulada")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        with httpx.Client(timeout=10) as client:
            r = client.post(url, json={"chat_id": chat_id, "text": message})
            if r.status_code != 200:
                log.warning(f"Telegram falhou ({r.status_code}): {r.text[:200]}")
    except Exception as e:
        log.warning(f"Telegram erro: {e}")


def normalizar_nome_arquivo(name):
    """Drive pode salvar arquivo sem .md (Google Doc nativo). Garante .md no GitHub."""
    if name.endswith(".md"):
        return name
    return name + ".md"


def processar_demanda_inbox(drive, repo, gh_token, f, inbox, processados_id, processados_erro_id):
    """Modo demanda: arquivo direto em inbox-*/ — valida frontmatter, commita, move.
    Inválidos vão pra processados-erro/<inbox>/ pra não ciclar a cada 15min.
    Retorna 'imported' | 'invalid' | 'error'."""
    file_id = f["id"]
    file_name = f["name"]
    mime = f.get("mimeType", "")

    def _mover_para_erro(motivo):
        try:
            proc_erro_inbox_id = get_or_create_folder(drive, inbox, processados_erro_id)
            move_file(drive, file_id, proc_erro_inbox_id, find_parents(drive, file_id))
            log.info(f"    Movido pra processados-erro/{inbox}/ ({motivo})")
        except HttpError as e:
            log.warning(f"    Move pra erro falhou: {e} — vai reprocessar no próximo ciclo")

    try:
        content = download_content(drive, file_id, mime)
    except HttpError as e:
        log.error(f"    Falha ao baixar {file_name}: {e}")
        return "error"
    except UnicodeDecodeError as e:
        log.warning(f"    {file_name} não é UTF-8 válido: byte {hex(e.object[e.start])} pos {e.start}")
        _mover_para_erro(f"conteúdo não-UTF-8 (byte {hex(e.object[e.start])})")
        return "invalid"

    fm, body = parse_frontmatter(content)
    if fm is None:
        log.warning(f"    Frontmatter ausente/inválido em {file_name} — skip")
        _mover_para_erro("frontmatter ausente/inválido")
        return "invalid"

    erros_fm = validate_frontmatter(fm, file_name)
    if erros_fm:
        log.warning(f"    Validação falhou em {file_name}: {erros_fm}")
        _mover_para_erro(f"validação: {erros_fm}")
        return "invalid"

    github_path = f"dialogos/{inbox}/{normalizar_nome_arquivo(file_name)}"
    commit_msg = f"import: {file_name} via {inbox} (origem: {fm.get('origem')})"

    status, ok = github_put_file(repo, github_path, content, commit_msg, gh_token)
    if not ok:
        log.error(f"    GitHub PUT falhou pra {file_name}")
        return "error"

    log.info(f"    [{status}] {github_path}")

    # Move no Drive pra processados/<inbox>/
    proc_inbox_id = get_or_create_folder(drive, inbox, processados_id)
    try:
        move_file(drive, file_id, proc_inbox_id, find_parents(drive, file_id))
        log.info(f"    Movido no Drive pra processados/{inbox}/")
    except HttpError as e:
        log.warning(f"    Move falhou (importou OK, pode reprocessar): {e}")

    if inbox == "inbox-tiogu":
        titulo = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        titulo = titulo.group(1).strip() if titulo else file_name
        msg = (
            f"📥 Demanda nova em inbox-tiogu\n"
            f"Origem: {fm.get('origem')} | Prioridade: {fm.get('prioridade')}\n"
            f"\"{titulo}\""
        )
        notify_telegram(msg)

    return "imported"


def processar_inbox_raw(drive, repo, gh_token, f, inbox, processados_id):
    """Modo inbox raw: arquivo em inbox_RAW/ (ex: inbox-chat-raw) — não tem
    frontmatter formal, mas precisa ser movido pra processados/ pra não
    reprocessar. Cron downstream (ex: ingest-chat-raw) processa o conteúdo.
    Retorna 'imported' | 'skipped' | 'error'."""
    file_id = f["id"]
    file_name = f["name"]
    mime = f.get("mimeType", "")

    if not is_text_mime(mime):
        log.info(f"    {inbox}/{file_name} ({mime}) não é texto, skip")
        return "skipped"

    try:
        content = download_content(drive, file_id, mime)
    except HttpError as e:
        log.error(f"    Falha ao baixar {file_name}: {e}")
        return "error"
    except UnicodeDecodeError as e:
        log.error(f"    {file_name} não-UTF-8 (byte {hex(e.object[e.start])}) — pulando")
        return "error"

    github_path = f"dialogos/{inbox}/{normalizar_nome_arquivo(file_name)}"
    commit_msg = f"import-raw: {file_name} via {inbox}"

    status, ok = github_put_file(repo, github_path, content, commit_msg, gh_token)
    if not ok:
        return "error"

    log.info(f"    [{status}] {github_path}")

    proc_inbox_id = get_or_create_folder(drive, inbox, processados_id)
    try:
        move_file(drive, file_id, proc_inbox_id, find_parents(drive, file_id))
        log.info(f"    Movido no Drive pra processados/{inbox}/")
    except HttpError as e:
        log.warning(f"    Move falhou (importou OK, pode reprocessar): {e}")

    return "imported"


def processar_mirror_raw(drive, repo, gh_token, f, prefix):
    """Modo mirror: cópia raw pro GitHub, idempotente. Não move, não valida.
    Retorna 'updated' | 'created' | 'unchanged' | 'skipped' | 'error'."""
    file_id = f["id"]
    file_name = f["name"]
    mime = f.get("mimeType", "")

    if not is_text_mime(mime):
        log.info(f"    {prefix}{file_name} ({mime}) não é texto, skip")
        return "skipped"

    try:
        content = download_content(drive, file_id, mime)
    except HttpError as e:
        log.error(f"    Falha ao baixar {prefix}{file_name}: {e}")
        return "error"
    except UnicodeDecodeError as e:
        log.error(f"    {prefix}{file_name} não é UTF-8 válido (byte {hex(e.object[e.start])} pos {e.start}) — pulando")
        return "error"

    github_path = f"dialogos/{prefix}{normalizar_nome_arquivo(file_name)}"
    commit_msg = f"mirror: {file_name} de Drive dialogos/{prefix}"

    status, ok = github_put_file(repo, github_path, content, commit_msg, gh_token)
    if not ok:
        return "error"
    return status


def find_parents(drive, file_id):
    """Pega lista de parents atuais (necessário pra move)."""
    r = drive.files().get(fileId=file_id, fields="parents").execute()
    return r.get("parents", [])


def main():
    repo = os.environ["GH_REPO"]
    gh_token = os.environ["GH_TOKEN"]
    drive_root = os.environ["DRIVE_ROOT_FOLDER_ID"]
    drive = get_drive()

    dialogos_id = find_folder_by_path(drive, "dialogos", drive_root)
    if not dialogos_id:
        log.info("Pasta dialogos/ não existe no Drive ainda — nada a importar")
        sys.exit(0)

    processados_id = get_or_create_folder(drive, PROCESSADOS_FOLDER, dialogos_id)
    processados_erro_id = get_or_create_folder(drive, PROCESSADOS_ERRO_FOLDER, dialogos_id)

    counts = {"imported": 0, "invalid": 0, "updated": 0, "created": 0,
              "unchanged": 0, "skipped": 0, "error": 0}

    for f, prefix in walk_drive_recursive(drive, dialogos_id):
        file_name = f["name"]
        mime = f.get("mimeType", "")

        # Path relativo a dialogos/. Ex: ""  -> arquivo direto em dialogos/
        #                                "inbox-tiogu/" -> direto em inbox
        #                                "streams/2026/" -> aninhado
        # Arquivos com prefixo `_` (ex: _README.md, _frontmatter-referencia.md)
        # são docs/referência — modo mirror, não demanda.
        parts = [p for p in prefix.split("/") if p]
        is_inbox_top = (
            len(parts) == 1
            and parts[0] in INBOXES
            and not file_name.startswith("_")
        )
        is_inbox_raw = (
            len(parts) == 1
            and parts[0] in INBOXES_RAW
            and not file_name.startswith("_")
        )

        log.info(f"  → {prefix}{file_name} (mime={mime})")

        if is_inbox_top:
            result = processar_demanda_inbox(drive, repo, gh_token, f, parts[0], processados_id, processados_erro_id)
        elif is_inbox_raw:
            result = processar_inbox_raw(drive, repo, gh_token, f, parts[0], processados_id)
        else:
            result = processar_mirror_raw(drive, repo, gh_token, f, prefix)

        counts[result] = counts.get(result, 0) + 1

    log.info(
        f"Resumo: {counts['imported']} demanda(s), "
        f"{counts['created']}/{counts['updated']}/{counts['unchanged']} mirror "
        f"(novos/atualizados/sem mudança), {counts['invalid']} inválida(s), "
        f"{counts['skipped']} ignorada(s), {counts['error']} erro(s)"
    )


if __name__ == "__main__":
    main()
