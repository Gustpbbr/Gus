#!/usr/bin/env python3
"""
Sincroniza arquivos .md do repositório para o Google Drive.
Modo incremental: roda a cada push em main (só arquivos alterados).
Modo full sync: roda via workflow_dispatch, sobe todos os .md de conteúdo.
"""

import os
import subprocess
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]

EXCLUDE_PATHS = {
    "CLAUDE.md",
    "README.md",
    "gus/system_prompt.md",
}
EXCLUDE_PREFIXES = (
    "historico/",
    "gus/",
    ".github/",
    "sensivel/",
)
# Precedência sobre EXCLUDE_*. Os arquivos canônicos de bootstrap/identity
# foram movidos pra dialogos/_bootstrap/ (que já é sincronizada). Os stubs
# em gus/ continuam aqui pra sobrescrever no Drive a versão antiga (que
# senão ficaria stale pro Claude Chat ler).
INCLUDE_OVERRIDES = {
    "gus/gus-bootstrap.md",   # stub de redirecionamento
    "gus/gus-identity.md",    # stub de redirecionamento
}


def get_drive_service():
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


def _is_excluded(filepath):
    if filepath in INCLUDE_OVERRIDES:
        return False
    return filepath in EXCLUDE_PATHS or filepath.startswith(EXCLUDE_PREFIXES)


def get_changed_md_files():
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACM", "HEAD~1", "HEAD"],
        capture_output=True,
        text=True,
    )
    files = result.stdout.strip().split("\n")
    return [
        f for f in files
        if f.endswith(".md") and f and os.path.exists(f) and not _is_excluded(f)
    ]


def get_all_md_files():
    result = []
    for path in Path(".").rglob("*.md"):
        filepath = str(path).replace("\\", "/").lstrip("./")
        if filepath and os.path.exists(filepath) and not _is_excluded(filepath):
            result.append(filepath)
    return sorted(result)


def get_or_create_folder(service, folder_name, parent_id):
    safe_name = folder_name.replace("'", "\\'")
    query = (
        f"name = '{safe_name}' "
        f"and '{parent_id}' in parents "
        f"and mimeType = 'application/vnd.google-apps.folder' "
        f"and trashed = false"
    )
    results = service.files().list(q=query, fields="files(id, name)", pageSize=1).execute()
    files = results.get("files", [])
    if files:
        return files[0]["id"]
    folder = service.files().create(
        body={"name": folder_name, "mimeType": "application/vnd.google-apps.folder", "parents": [parent_id]},
        fields="id"
    ).execute()
    print(f"  Pasta criada: {folder_name}")
    return folder["id"]


def ensure_folder_path(service, path, root_folder_id):
    current_parent = root_folder_id
    for part in [p for p in path.split("/") if p]:
        current_parent = get_or_create_folder(service, part, current_parent)
    return current_parent


def find_existing_file(service, file_name, parent_id):
    safe_name = file_name.replace("'", "\\'")
    query = (
        f"name = '{safe_name}' "
        f"and '{parent_id}' in parents "
        f"and trashed = false"
    )
    results = service.files().list(q=query, fields="files(id, name)", pageSize=1).execute()
    files = results.get("files", [])
    return files[0]["id"] if files else None


def upsert_file(service, local_path, file_name, parent_id):
    existing_id = find_existing_file(service, file_name, parent_id)

    # Idempotência: se Drive já tem byte-idêntico, skip. Quebra loop com
    # import-from-drive (que pode trazer o mesmo arquivo de volta do Drive
    # quando dialogos/** for varrido recursivo).
    if existing_id:
        try:
            remote_bytes = service.files().get_media(fileId=existing_id).execute()
            with open(local_path, "rb") as fh:
                local_bytes = fh.read()
            if remote_bytes == local_bytes:
                print(f"  Idêntico, skip: {file_name}")
                return
        except Exception as e:
            print(f"  Comparação falhou ({e}), prossegue com update")

    media = MediaFileUpload(local_path, mimetype="text/plain", resumable=True)
    if existing_id:
        service.files().update(
            fileId=existing_id,
            media_body=media,
            fields="id, name",
        ).execute()
        print(f"  Atualizado: {file_name}")
    else:
        service.files().create(
            body={"name": file_name, "parents": [parent_id]},
            media_body=media,
            fields="id, name",
        ).execute()
        print(f"  Criado: {file_name}")


def sync_file(service, local_path, root_folder_id):
    dir_path = os.path.dirname(local_path)
    file_name = os.path.basename(local_path)
    parent_id = ensure_folder_path(service, dir_path, root_folder_id) if dir_path else root_folder_id
    upsert_file(service, local_path, file_name, parent_id)


def main():
    if not os.environ.get("GOOGLE_REFRESH_TOKEN") or not os.environ.get("DRIVE_ROOT_FOLDER_ID"):
        print("Credenciais ou DRIVE_ROOT_FOLDER_ID não configurados. Sync pulado.")
        sys.exit(0)

    root_folder_id = os.environ["DRIVE_ROOT_FOLDER_ID"]
    service = get_drive_service()
    full_sync = os.environ.get("FULL_SYNC", "").lower() == "true"

    if full_sync:
        files = get_all_md_files()
        print(f"Modo full sync: {len(files)} arquivo(s) encontrados.")
    else:
        files = get_changed_md_files()
        if not files:
            print("Nenhum .md de conteúdo alterado. Nada a sincronizar.")
            sys.exit(0)
        print(f"Sincronizando {len(files)} arquivo(s) alterado(s)...")

    for file_path in files:
        print(f"\n→ {file_path}")
        try:
            sync_file(service, file_path, root_folder_id)
        except Exception as e:
            print(f"  ERRO: {e}")

    print("\nSync completo.")


if __name__ == "__main__":
    main()
