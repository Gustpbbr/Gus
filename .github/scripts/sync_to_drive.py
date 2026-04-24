#!/usr/bin/env python3
"""
Sincroniza arquivos .md do repositório para o Google Drive,
convertendo para Google Docs e preservando estrutura de pastas.

Roda via GitHub Actions a cada push em main.
Só sincroniza arquivos de conteúdo (exclui código e docs do projeto).
"""

import json
import os
import subprocess
import sys

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]

EXCLUDE_PATHS = {
    "CLAUDE.md",
    "README.md",
    "gus/system_prompt.md",
}
EXCLUDE_PREFIXES = (
    "docs/",
    "gus/",
    ".github/",
    "sensivel/",
)


def get_drive_service():
    creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
    credentials = service_account.Credentials.from_service_account_info(
        creds_dict, scopes=SCOPES
    )
    return build("drive", "v3", credentials=credentials)


def get_changed_md_files():
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACM", "HEAD~1", "HEAD"],
        capture_output=True,
        text=True,
    )
    files = result.stdout.strip().split("\n")
    return [
        f
        for f in files
        if f.endswith(".md")
        and f
        and os.path.exists(f)
        and f not in EXCLUDE_PATHS
        and not f.startswith(EXCLUDE_PREFIXES)
    ]


def get_or_create_folder(service, folder_name, parent_id):
    safe_name = folder_name.replace("'", "\\'")
    query = (
        f"name = '{safe_name}' "
        f"and '{parent_id}' in parents "
        f"and mimeType = 'application/vnd.google-apps.folder' "
        f"and trashed = false"
    )
    results = service.files().list(
        q=query, fields="files(id, name)", pageSize=1
    ).execute()
    files = results.get("files", [])

    if files:
        return files[0]["id"]

    folder_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }
    folder = service.files().create(
        body=folder_metadata, fields="id"
    ).execute()
    print(f"  Pasta criada: {folder_name}")
    return folder["id"]


def ensure_folder_path(service, path, root_folder_id):
    current_parent = root_folder_id
    parts = [p for p in path.split("/") if p]
    for part in parts:
        current_parent = get_or_create_folder(service, part, current_parent)
    return current_parent


def find_existing_file(service, file_name, parent_id):
    safe_name = file_name.replace("'", "\\'")
    query = (
        f"name = '{safe_name}' "
        f"and '{parent_id}' in parents "
        f"and trashed = false"
    )
    results = service.files().list(
        q=query, fields="files(id, name)", pageSize=1
    ).execute()
    files = results.get("files", [])
    return files[0]["id"] if files else None


def upsert_file(service, local_path, file_name, parent_id):
    media = MediaFileUpload(local_path, mimetype="text/markdown", resumable=True)

    existing_id = find_existing_file(service, file_name, parent_id)

    if existing_id:
        updated = service.files().update(
            fileId=existing_id,
            media_body=media,
            fields="id, name, modifiedTime",
        ).execute()
        print(f"  Atualizado: {file_name}")
        return updated

    file_metadata = {
        "name": file_name,
        "mimeType": "application/vnd.google-apps.document",
        "parents": [parent_id],
    }
    created = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, name",
    ).execute()
    print(f"  Criado: {file_name}")
    return created


def sync_file(service, local_path, root_folder_id):
    dir_path = os.path.dirname(local_path)
    file_name = os.path.basename(local_path)

    if dir_path:
        parent_id = ensure_folder_path(service, dir_path, root_folder_id)
    else:
        parent_id = root_folder_id

    upsert_file(service, local_path, file_name, parent_id)


def main():
    root_folder_id = os.environ["DRIVE_ROOT_FOLDER_ID"]
    service = get_drive_service()

    changed_files = get_changed_md_files()

    if not changed_files:
        print("Nenhum .md de conteúdo alterado. Nada a sincronizar.")
        sys.exit(0)

    print(f"Sincronizando {len(changed_files)} arquivo(s)...")
    for file_path in changed_files:
        print(f"\n→ {file_path}")
        sync_file(service, file_path, root_folder_id)

    print("\nSync completo.")


if __name__ == "__main__":
    main()
