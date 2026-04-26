#!/usr/bin/env python3
"""
Apaga (ou move pra lixeira) arquivo no Google Drive via API.

Uso (workflow_dispatch):
  - file_id: ID do arquivo no Drive (obrigatório)
  - mode: dry-run | trash | delete (default: trash)

Modos:
  - dry-run: só busca metadata e printa, não toca em nada
  - trash: marca como `trashed=true` (recuperável por 30 dias no Drive)
  - delete: remove permanentemente (irreversível!)

Default é `trash` por segurança.
"""

import os
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/drive"]


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


def get_metadata(drive, file_id):
    fields = "id, name, mimeType, modifiedTime, parents, size, trashed, webViewLink"
    return drive.files().get(fileId=file_id, fields=fields).execute()


def resolve_parent_path(drive, parent_id):
    """Sobe a hierarquia até root pra mostrar path legível."""
    parts = []
    current = parent_id
    for _ in range(10):  # limite de profundidade
        try:
            f = drive.files().get(fileId=current, fields="id, name, parents").execute()
        except HttpError:
            break
        parts.append(f["name"])
        if not f.get("parents"):
            break
        current = f["parents"][0]
    return "/".join(reversed(parts))


def main():
    file_id = os.environ.get("FILE_ID", "").strip()
    mode = os.environ.get("MODE", "trash").strip().lower()

    if not file_id:
        print("ERRO: FILE_ID vazio")
        sys.exit(1)

    if mode not in ("dry-run", "trash", "delete"):
        print(f"ERRO: mode inválido '{mode}', use dry-run|trash|delete")
        sys.exit(1)

    drive = get_drive()

    try:
        meta = get_metadata(drive, file_id)
    except HttpError as e:
        if e.resp.status == 404:
            print(f"ERRO: arquivo {file_id} não existe (404)")
            sys.exit(1)
        print(f"ERRO ao buscar metadata: {e}")
        sys.exit(1)

    print("===== METADATA =====")
    print(f"  ID:            {meta['id']}")
    print(f"  Nome:          {meta['name']}")
    print(f"  Mime:          {meta.get('mimeType', '?')}")
    print(f"  Modificado:    {meta.get('modifiedTime', '?')}")
    print(f"  Tamanho:       {meta.get('size', 'n/a')} bytes")
    print(f"  Já na lixeira: {meta.get('trashed', False)}")
    if meta.get("parents"):
        path = resolve_parent_path(drive, meta["parents"][0])
        print(f"  Pasta pai:     {path}")
    print(f"  Web link:      {meta.get('webViewLink', '?')}")
    print()

    if mode == "dry-run":
        print("MODO dry-run — nada foi alterado.")
        return

    if mode == "trash":
        if meta.get("trashed"):
            print("Arquivo JÁ está na lixeira. Nada a fazer.")
            return
        drive.files().update(fileId=file_id, body={"trashed": True}).execute()
        print(f"✅ Movido pra lixeira do Drive (recuperável por 30 dias).")
        return

    if mode == "delete":
        drive.files().delete(fileId=file_id).execute()
        print(f"✅ Apagado permanentemente do Drive (irreversível).")
        return


if __name__ == "__main__":
    main()
