#!/usr/bin/env python3
"""
Archive demandas com status: concluido + limpa loop drive→github.

Roda a cada 15min via cron. Pra cada arquivo .md em dialogos/inbox-*/ (exceto
_README.md):

1. Lê frontmatter.
2. Se status == 'concluido' (ou 'cancelado'):
   a. Se dialogos/archive/<filename> já existe: deleta o do inbox (archive
      tem versão canônica)
   b. Senão: move pra dialogos/archive/<filename>
   c. Trash arquivo no Drive em Gus-Sync/dialogos/inbox-<X>/<filename>
      (impede reimport pelo import-from-drive)
   d. Append linha em dialogos/historico/<YYYY-MM>.md (mensal)
3. Detecção de loop: se status == 'pendente' MAS dialogos/archive/<filename>
   existe com status: concluido → arquivo é fantasma reimportado. Deleta do
   inbox + Drive.
4. Outras: deixa.

Commit consolidado no fim se houver mudança.
"""

import logging
import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/drive"]
BRT = timezone(timedelta(hours=-3))

INBOXES = ["inbox-tiogu", "inbox-claude-code", "inbox-claude-chat", "inbox-custom-gpt"]
STATUS_FINAIS = {"concluido", "cancelado"}

REPO_ROOT = Path(__file__).resolve().parents[2]
DIALOGOS = REPO_ROOT / "dialogos"


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


def find_file_in_drive(drive, path, root_id):
    """Resolve path tipo 'dialogos/inbox-X/file.md' relativo a root_id.
    Retorna file_id ou None."""
    parts = [p for p in path.split("/") if p]
    if not parts:
        return None
    current = root_id
    for part in parts[:-1]:
        safe = part.replace("'", "\\'")
        q = (
            f"name = '{safe}' and '{current}' in parents "
            f"and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        )
        r = drive.files().list(q=q, fields="files(id)", pageSize=1).execute()
        files = r.get("files", [])
        if not files:
            return None
        current = files[0]["id"]

    leaf_name = parts[-1].replace("'", "\\'")
    leaf_stem = leaf_name[:-3] if leaf_name.endswith(".md") else leaf_name
    q = (
        f"('{current}' in parents) and trashed = false "
        f"and (name = '{leaf_name}' or name = '{leaf_stem}')"
    )
    r = drive.files().list(q=q, fields="files(id, name, mimeType)", pageSize=2).execute()
    files = r.get("files", [])
    return files[0]["id"] if files else None


def trash_drive_file(drive, file_id):
    drive.files().update(fileId=file_id, body={"trashed": True}).execute()


def parse_frontmatter(content):
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


def archive_already_complete(filename):
    """True se dialogos/archive/<filename> existe com status concluido/cancelado."""
    p = DIALOGOS / "archive" / filename
    if not p.exists():
        return False
    fm, _ = parse_frontmatter(p.read_text(encoding="utf-8"))
    return bool(fm) and fm.get("status") in STATUS_FINAIS


def extrair_resumo(body, max_chars=300):
    """Extrai resumo do body. Prefere seção '## Resultado'; fallback: 1ª linha não-vazia
    pós-título."""
    m = body.split("## Resultado", 1)
    if len(m) == 2:
        resumo = m[1].strip()
    else:
        linhas = [l for l in body.splitlines() if l.strip() and not l.startswith("#")]
        resumo = " ".join(linhas[:3]) if linhas else "(sem corpo)"
    resumo = " ".join(resumo.split())  # normaliza whitespace
    if len(resumo) > max_chars:
        resumo = resumo[:max_chars - 3] + "..."
    return resumo


def append_historico(fm, filename, inbox, resumo):
    """Adiciona linha em dialogos/historico/AAAA-MM.md (mensal). Cria arquivo
    com header se ainda não existe."""
    processado_em = fm.get("processado_em") or datetime.now(BRT).isoformat()
    # YAML safe_load converte ISO datetime sem aspas direto pra datetime — aceita ambos
    if isinstance(processado_em, datetime):
        dt = processado_em
    else:
        try:
            dt = datetime.fromisoformat(str(processado_em).replace("Z", "+00:00"))
        except (ValueError, AttributeError, TypeError):
            dt = datetime.now(BRT)
    yyyy_mm = dt.strftime("%Y-%m")

    historico_dir = DIALOGOS / "historico"
    historico_dir.mkdir(parents=True, exist_ok=True)
    historico_file = historico_dir / f"{yyyy_mm}.md"

    if not historico_file.exists():
        header = (
            f"# Histórico de demandas — {yyyy_mm}\n\n"
            f"Auto-gerado pelo workflow `archive-completed-demandas.yml`.\n"
            f"Cada linha é uma demanda concluída ou cancelada movida pra "
            f"`dialogos/archive/`.\n\n"
            f"| Concluída em | Origem→Destino | Status | Título | Resumo | Arquivo |\n"
            f"|---|---|---|---|---|---|\n"
        )
        historico_file.write_text(header, encoding="utf-8")

    titulo = filename.replace(".md", "")
    body_full = (DIALOGOS / "archive" / filename).read_text(encoding="utf-8") if (DIALOGOS / "archive" / filename).exists() else ""
    fm_arch, body_arch = parse_frontmatter(body_full)
    body_for_title = body_arch if fm_arch else ""
    for line in body_for_title.splitlines():
        if line.startswith("# "):
            titulo = line[2:].strip()
            break

    origem = fm.get("origem", "?")
    destino = fm.get("destino", "?")
    status = fm.get("status", "?")
    when = dt.strftime("%Y-%m-%d %H:%M")
    arquivo_link = f"archive/{filename}"

    # escape pipe in fields
    def esc(s):
        return str(s).replace("|", "\\|").replace("\n", " ")

    linha = (
        f"| {when} | {origem}→{destino} | {status} | "
        f"{esc(titulo)} | {esc(resumo)} | `{arquivo_link}` |\n"
    )
    with historico_file.open("a", encoding="utf-8") as f:
        f.write(linha)
    return historico_file


def git_run(*args):
    subprocess.run(["git", *args], check=True, cwd=REPO_ROOT)


def git_run_silent(*args):
    return subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, text=True)


def main():
    if not DIALOGOS.exists():
        log.info("dialogos/ não existe — nada a fazer")
        return

    drive_root = os.environ.get("DRIVE_ROOT_FOLDER_ID")
    drive = None
    if drive_root and os.environ.get("GOOGLE_REFRESH_TOKEN"):
        try:
            drive = get_drive()
        except Exception as e:
            log.warning(f"Drive não conectado: {e} — vai limpar só GitHub")

    archived = 0
    loop_cleaned = 0
    historicos_tocados = set()

    for inbox in INBOXES:
        inbox_dir = DIALOGOS / inbox
        if not inbox_dir.exists():
            continue
        for f in sorted(inbox_dir.glob("*.md")):
            if f.name == "_README.md":
                continue
            try:
                content = f.read_text(encoding="utf-8")
            except Exception as e:
                log.warning(f"Falha lendo {f}: {e}")
                continue
            fm, body = parse_frontmatter(content)
            if not fm:
                log.info(f"  {f.relative_to(REPO_ROOT)}: sem frontmatter, skip")
                continue
            status = (fm.get("status") or "").lower()

            # Caso 1: status final → archive
            if status in STATUS_FINAIS:
                archive_path = DIALOGOS / "archive" / f.name
                if archive_path.exists():
                    log.info(f"  {f.relative_to(REPO_ROOT)}: archive/ já tem versão. Deletando do inbox.")
                    git_run("rm", str(f.relative_to(REPO_ROOT)))
                else:
                    log.info(f"  {f.relative_to(REPO_ROOT)}: status={status}. Movendo pra archive/.")
                    git_run("mv", str(f.relative_to(REPO_ROOT)), str(archive_path.relative_to(REPO_ROOT)))

                resumo = extrair_resumo(body)
                hist = append_historico(fm, f.name, inbox, resumo)
                historicos_tocados.add(hist)

                if drive:
                    try:
                        drive_path = f"dialogos/{inbox}/{f.name}"
                        fid = find_file_in_drive(drive, drive_path, drive_root)
                        if fid:
                            trash_drive_file(drive, fid)
                            log.info(f"    Drive: trashed {drive_path}")
                    except HttpError as e:
                        log.warning(f"    Drive trash falhou: {e}")
                archived += 1
                continue

            # Caso 2: loop detection — pendente no inbox MAS archive já tem completo
            if status == "pendente" and archive_already_complete(f.name):
                log.info(f"  {f.relative_to(REPO_ROOT)}: loop detectado (archive já tem completo). Limpando.")
                git_run("rm", str(f.relative_to(REPO_ROOT)))
                if drive:
                    try:
                        drive_path = f"dialogos/{inbox}/{f.name}"
                        fid = find_file_in_drive(drive, drive_path, drive_root)
                        if fid:
                            trash_drive_file(drive, fid)
                            log.info(f"    Drive: trashed {drive_path}")
                    except HttpError as e:
                        log.warning(f"    Drive trash falhou: {e}")
                loop_cleaned += 1
                continue

    if archived == 0 and loop_cleaned == 0:
        log.info("Nada a arquivar/limpar.")
        return

    # stage historicos atualizados (commit/push fica a cargo do step do workflow)
    for h in historicos_tocados:
        git_run("add", str(h.relative_to(REPO_ROOT)))

    parts = []
    if archived:
        parts.append(f"{archived} arquivada(s)")
    if loop_cleaned:
        parts.append(f"{loop_cleaned} loop(s) limpos")
    log.info(f"Mudanças staged: {', '.join(parts)}. Workflow vai commitar+pushar no próximo step.")


if __name__ == "__main__":
    main()
