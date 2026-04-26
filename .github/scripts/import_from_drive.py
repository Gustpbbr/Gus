#!/usr/bin/env python3
"""
Import demandas de Gus-Sync/dialogos/inbox-*/ no Drive pra dialogos/inbox-*/ no GitHub.

Fluxo por execução (cron 15min):
  1. Lista arquivos em cada pasta inbox-*/ no Drive
  2. Pra cada arquivo:
     a. Baixa conteúdo (Google Doc → exporta como text/markdown; .md → baixa direto)
     b. Valida frontmatter YAML
     c. Se válido: commita no GitHub via API + move arquivo no Drive pra processados/
     d. Se inválido: skip (deixa no Drive pro Gustavo corrigir)
     e. Se inbox-tiogu: notifica Telegram (opcional, só se secrets configurados)

Idempotência: se arquivo já existe no GitHub com mesmo path, faz update via PUT
sha. Se mesmo conteúdo, GitHub retorna 200 sem mudança real.
"""

import base64
import logging
import os
import re
import sys
from datetime import datetime, timezone, timedelta

import httpx
import yaml
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/drive"]
BRT = timezone(timedelta(hours=-3))

PORTAS_VALIDAS = {"claude-chat", "tiogu", "claude-code", "custom-gpt", "gustavo"}
INBOXES = ["inbox-tiogu", "inbox-claude-code", "inbox-claude-chat", "inbox-custom-gpt"]
PROCESSADOS_FOLDER = "processados"


def get_drive():
    creds = Credentials(
        token=None,
        refresh_token=os.environ["GOOGLE_REFRESH_TOKEN"],
        client_id=os.environ["GOOGLE_CLIENT_ID"],
        client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
        token_uri="https://oauth2.googleapis.com/token",
        scopes=SCOPES,
    )
    creds.refresh(Request())
    return build("drive", "v3", credentials=creds)


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
    """Cria ou atualiza arquivo no GitHub via Contents API."""
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {gh_token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    # Verifica se já existe
    sha = None
    with httpx.Client(timeout=30) as client:
        r = client.get(url, headers=headers)
        if r.status_code == 200:
            sha = r.json().get("sha")
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
            return True
        log.error(f"GitHub PUT {url} falhou ({r.status_code}): {r.text[:300]}")
        return False


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


def main():
    repo = os.environ["GH_REPO"]
    gh_token = os.environ["GH_TOKEN"]
    drive_root = os.environ["DRIVE_ROOT_FOLDER_ID"]
    drive = get_drive()

    # Resolve dialogos/ no Drive
    dialogos_id = find_folder_by_path(drive, "dialogos", drive_root)
    if not dialogos_id:
        log.info("Pasta dialogos/ não existe no Drive ainda — nada a importar")
        sys.exit(0)

    # Garante pasta processados/ existe
    processados_id = get_or_create_folder(drive, PROCESSADOS_FOLDER, dialogos_id)

    total_importados = 0
    total_erros = 0

    for inbox in INBOXES:
        inbox_id = find_folder_by_path(drive, inbox, dialogos_id)
        if not inbox_id:
            log.debug(f"{inbox}/ não existe no Drive (ainda)")
            continue

        # Subpasta de processados específica
        proc_inbox_id = get_or_create_folder(drive, inbox, processados_id)

        files = list_files_in_folder(drive, inbox_id)
        if not files:
            continue

        log.info(f"{inbox}: {len(files)} arquivo(s) a processar")

        for f in files:
            file_id = f["id"]
            file_name = f["name"]
            mime = f.get("mimeType", "")
            log.info(f"  → {file_name} (mime={mime})")

            try:
                content = download_content(drive, file_id, mime)
            except HttpError as e:
                log.error(f"    Falha ao baixar {file_name}: {e}")
                total_erros += 1
                continue

            fm, body = parse_frontmatter(content)
            if fm is None:
                log.warning(f"    Frontmatter ausente/inválido em {file_name} — skip")
                total_erros += 1
                continue

            erros_fm = validate_frontmatter(fm, file_name)
            if erros_fm:
                log.warning(f"    Validação falhou em {file_name}: {erros_fm}")
                total_erros += 1
                continue

            # Tudo OK — importa pro GitHub
            github_path = f"dialogos/{inbox}/{normalizar_nome_arquivo(file_name)}"
            commit_msg = f"import: {file_name} via {inbox} (origem: {fm.get('origem')})"

            ok = github_put_file(repo, github_path, content, commit_msg, gh_token)
            if not ok:
                log.error(f"    GitHub PUT falhou pra {file_name}")
                total_erros += 1
                continue

            log.info(f"    Commitado em {github_path}")

            # Move no Drive pra processados
            try:
                move_file(drive, file_id, proc_inbox_id, [inbox_id])
                log.info(f"    Movido no Drive pra processados/{inbox}/")
            except HttpError as e:
                log.warning(f"    Move falhou (importou OK, mas pode reprocessar): {e}")

            total_importados += 1

            # Notifica Telegram se for inbox-tiogu
            if inbox == "inbox-tiogu":
                titulo = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
                titulo = titulo.group(1).strip() if titulo else file_name
                msg = (
                    f"📥 Demanda nova em inbox-tiogu\n"
                    f"Origem: {fm.get('origem')} | Prioridade: {fm.get('prioridade')}\n"
                    f"\"{titulo}\""
                )
                notify_telegram(msg)

    log.info(f"Resumo: {total_importados} importado(s), {total_erros} erro(s)")


if __name__ == "__main__":
    main()
