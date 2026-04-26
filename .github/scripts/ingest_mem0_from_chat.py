#!/usr/bin/env python3
"""
Ingest de memórias geradas pelo Claude Chat pra dentro do Mem0.

Fluxo (cron 30min):
  1. Lista .md em dialogos/inbox-mem0-from-chat/ (skip processados/)
  2. Pra cada arquivo:
     a. Parse frontmatter + body
     b. Filtro permissivo Haiku: só descarta lixo óbvio (vazio, "ok", saudação)
     c. Se aprovado: mem0.add() com user_id=gustavo, metadata.via=claude-chat
     d. Move arquivo pra processados/AAAA-MM/ (git mv)
     e. Append linha em _log/resumos-mem0/AAAA-MM-DD.md
  3. git commit + push das mudanças

Idempotência: depois do move, arquivo não é reentrado. Se Mem0 falhar antes do
move, próxima rodada tenta de novo (não duplica). Se Mem0 sucesso e move falha,
próxima rodada vai duplicar — risco baixíssimo (git é local).
"""

import logging
import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx
import yaml

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

BRT = timezone(timedelta(hours=-3))
INBOX = Path("dialogos/inbox-mem0-from-chat")
PROCESSADOS = INBOX / "processados"
LOG_DIR = Path("_log/resumos-mem0")

HAIKU_MODEL = "claude-haiku-4-5"
FILTRO_PROMPT = (
    "Você decide se um texto vale virar memória persistente do Gustavo (no Mem0).\n\n"
    "Diga DESCARTA apenas se o texto for claramente:\n"
    "- vazio ou só whitespace\n"
    "- saudação trivial sem conteúdo (ex: 'oi', 'tudo bem', 'ok', 'beleza')\n"
    "- mensagem de teste óbvia (ex: 'teste 123', 'asdf')\n"
    "- erro/lixo de copia-cola sem sentido\n\n"
    "Em QUALQUER outro caso (mesmo se parecer fragmentado, parcial, ou de baixo "
    "valor), diga SALVA. Memória do Gustavo prefere abundância a escassez — "
    "manutenção do grafo é feita depois.\n\n"
    "Responda APENAS uma palavra: SALVA ou DESCARTA."
)


def parse_frontmatter(content: str) -> tuple[dict | None, str]:
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


def filtro_haiku(body: str, anthropic_key: str) -> tuple[bool, str]:
    """Retorna (salva?, motivo). True = salvar no Mem0."""
    payload = {
        "model": HAIKU_MODEL,
        "max_tokens": 8,
        "system": FILTRO_PROMPT,
        "messages": [{"role": "user", "content": body[:4000]}],
    }
    headers = {
        "x-api-key": anthropic_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    try:
        with httpx.Client(timeout=20) as c:
            r = c.post("https://api.anthropic.com/v1/messages", json=payload, headers=headers)
        if r.status_code != 200:
            log.warning(f"  Haiku falhou ({r.status_code}), salvando por segurança")
            return True, f"haiku-erro-{r.status_code}"
        data = r.json()
        text = (data.get("content", [{}])[0] or {}).get("text", "").strip().upper()
        if text.startswith("DESCARTA"):
            return False, "filtro descartou (lixo óbvio)"
        return True, "filtro aprovou"
    except Exception as e:
        log.warning(f"  Haiku exception ({e}), salvando por segurança")
        return True, f"haiku-exception-{str(e)[:40]}"


def salvar_no_mem0(body: str, fm: dict, mem0_key: str) -> tuple[bool, str]:
    """Chama mem0.add via cliente nativo. Retorna (ok, msg)."""
    try:
        from mem0 import MemoryClient
    except Exception as e:
        return False, f"mem0 import: {e}"

    try:
        client = MemoryClient(api_key=mem0_key)
        contexto = (fm.get("contexto") or "").strip()
        msg_user = body if not contexto else f"[contexto: {contexto}]\n\n{body}"
        client.add(
            [{"role": "user", "content": msg_user[:8000]}],
            user_id="gustavo",
            metadata={"via": "claude-chat"},
        )
        return True, "ok"
    except Exception as e:
        return False, f"mem0 add: {str(e)[:120]}"


def append_log(arquivo_nome: str, status: str, motivo: str, body_preview: str) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    hoje = datetime.now(BRT).strftime("%Y-%m-%d")
    log_path = LOG_DIR / f"{hoje}.md"
    agora = datetime.now(BRT).strftime("%H:%M:%S")

    if not log_path.exists():
        log_path.write_text(
            f"---\ndata: {hoje}\nfonte: ingest claude-chat (Haiku filtro)\n"
            f"tipo: log-resumos-mem0\n---\n\n# Resumos pro Mem0 — {hoje}\n\n",
            encoding="utf-8",
        )

    preview = body_preview.replace("\n", " ")[:280]
    entrada = (
        f"## {agora} BRT — {status} (claude-chat)\n"
        f"**Arquivo:** `{arquivo_nome}`\n"
        f"**Motivo:** {motivo}\n"
        f"**Preview:** {preview}\n\n"
    )
    with log_path.open("a", encoding="utf-8") as f:
        f.write(entrada)


def mover_pra_processados(arquivo: Path) -> Path:
    mes = datetime.now(BRT).strftime("%Y-%m")
    destino_dir = PROCESSADOS / mes
    destino_dir.mkdir(parents=True, exist_ok=True)
    destino = destino_dir / arquivo.name
    shutil.move(str(arquivo), str(destino))
    return destino


def git_commit_push(mensagem: str) -> None:
    subprocess.run(["git", "config", "user.name", "gus-bot"], check=True)
    subprocess.run(["git", "config", "user.email", "gus-bot@users.noreply.github.com"], check=True)
    subprocess.run(["git", "add", "-A", "dialogos/inbox-mem0-from-chat", "_log/resumos-mem0"], check=True)
    diff = subprocess.run(["git", "diff", "--staged", "--quiet"]).returncode
    if diff == 0:
        log.info("Nada pra commitar")
        return
    subprocess.run(["git", "commit", "-m", mensagem], check=True)
    subprocess.run(["git", "push"], check=True)


def main() -> None:
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    mem0_key = os.environ.get("MEM0_API_KEY")
    if not anthropic_key or not mem0_key:
        log.error("ANTHROPIC_API_KEY ou MEM0_API_KEY ausentes")
        sys.exit(1)

    if not INBOX.exists():
        log.info(f"{INBOX}/ não existe ainda — nada a ingerir")
        return

    arquivos = sorted(
        f for f in INBOX.glob("*.md")
        if f.is_file() and PROCESSADOS not in f.parents
    )
    if not arquivos:
        log.info("Nenhum arquivo novo em inbox-mem0-from-chat/")
        return

    log.info(f"{len(arquivos)} arquivo(s) a processar")
    salvos = descartados = erros = 0

    for arq in arquivos:
        log.info(f"→ {arq.name}")
        try:
            content = arq.read_text(encoding="utf-8")
        except Exception as e:
            log.error(f"  read falhou: {e}")
            erros += 1
            continue

        fm, body = parse_frontmatter(content)
        body_efetivo = body.strip() if body else content.strip()

        if not body_efetivo:
            append_log(arq.name, "descartado", "arquivo vazio", "")
            mover_pra_processados(arq)
            descartados += 1
            continue

        salva, motivo = filtro_haiku(body_efetivo, anthropic_key)
        if not salva:
            log.info(f"  DESCARTA: {motivo}")
            append_log(arq.name, "descartado", motivo, body_efetivo)
            mover_pra_processados(arq)
            descartados += 1
            continue

        ok, msg = salvar_no_mem0(body_efetivo, fm or {}, mem0_key)
        if not ok:
            log.error(f"  Mem0 falhou: {msg}")
            erros += 1
            continue  # NÃO move — próxima rodada tenta de novo

        log.info(f"  SALVO ({motivo})")
        append_log(arq.name, "salvo", motivo, body_efetivo)
        mover_pra_processados(arq)
        salvos += 1

    log.info(f"Resumo: {salvos} salvo(s), {descartados} descartado(s), {erros} erro(s)")

    if salvos or descartados:
        git_commit_push(
            f"auto: ingest mem0 claude-chat ({salvos} salvos, {descartados} descartados)"
        )


if __name__ == "__main__":
    main()
