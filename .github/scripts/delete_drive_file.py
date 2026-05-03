#!/usr/bin/env python3
"""
Apaga (ou move pra lixeira) arquivo no Google Drive via API.

Uso (workflow_dispatch) — passe UM dos dois:
  - file_id:   ID exato do arquivo (URL do Drive: /file/d/<id>/view)
  - file_path: caminho relativo a Gus-Sync/, ex:
               "dialogos/Demandas Gustavo/_teste_para_todas_portas.md"

  - mode: dry-run | trash | delete (default: trash)

Modos:
  - dry-run: só busca metadata e printa, não toca em nada
  - trash: marca como `trashed=true` (recuperável por 30 dias no Drive)
  - delete: remove permanentemente (irreversível!)

Default é `trash` por segurança. Se ambos file_id e file_path forem passados,
file_id tem precedência.
"""

import os
import sys

from googleapiclient.errors import HttpError

# Helper compartilhado de auth Drive (WIF preferred, SA JSON e OAuth fallback)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _drive_auth import get_drive_service


def get_drive():
    return get_drive_service()


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


def resolve_path_to_file_id(drive, root_id, path):
    """Resolve path tipo 'dialogos/Demandas Gustavo/arquivo.md' relativo a root_id.

    Retorna file_id ou levanta ValueError com motivo (não encontrado, ambíguo).
    Quoting de aspas em nomes feito explicitamente.
    """
    parts = [p for p in path.split("/") if p.strip()]
    if not parts:
        raise ValueError("path vazio depois de normalizar")

    current = root_id
    for i, part in enumerate(parts):
        is_last = (i == len(parts) - 1)
        safe = part.replace("'", "\\'")
        if is_last:
            # Último componente: arquivo (qualquer mimeType, exceto folder)
            q = (
                f"name = '{safe}' and '{current}' in parents "
                f"and trashed = false and mimeType != 'application/vnd.google-apps.folder'"
            )
        else:
            # Componente intermediário: tem que ser pasta
            q = (
                f"name = '{safe}' and '{current}' in parents "
                f"and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
            )
        r = drive.files().list(q=q, fields="files(id, name, mimeType)", pageSize=10).execute()
        files = r.get("files", [])
        if not files:
            tipo = "arquivo" if is_last else "pasta"
            caminho_ate = "/".join(parts[: i + 1])
            raise ValueError(f"{tipo} não encontrado: '{caminho_ate}'")
        if len(files) > 1:
            ids = ", ".join(f["id"] for f in files)
            raise ValueError(
                f"ambiguidade em '{part}' ({len(files)} matches: {ids}). "
                f"Use file_id explícito."
            )
        current = files[0]["id"]

    return current


def main():
    file_id = os.environ.get("FILE_ID", "").strip()
    file_path = os.environ.get("FILE_PATH", "").strip()
    mode = os.environ.get("MODE", "trash").strip().lower()

    if not file_id and not file_path:
        print("ERRO: passe file_id OU file_path (nenhum recebido)")
        sys.exit(1)

    if mode not in ("dry-run", "trash", "delete"):
        print(f"ERRO: mode inválido '{mode}', use dry-run|trash|delete")
        sys.exit(1)

    drive = get_drive()

    # Resolve path → file_id se necessário
    if not file_id and file_path:
        root_id = os.environ.get("DRIVE_ROOT_FOLDER_ID", "").strip()
        if not root_id:
            print("ERRO: DRIVE_ROOT_FOLDER_ID ausente, não dá pra resolver path")
            sys.exit(1)
        try:
            file_id = resolve_path_to_file_id(drive, root_id, file_path)
            print(f"Path '{file_path}' resolvido pra file_id={file_id}")
        except ValueError as e:
            print(f"ERRO: {e}")
            sys.exit(1)

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
