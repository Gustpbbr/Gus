#!/usr/bin/env python3
"""
Cron: processa transcripts da porta Claude Code → Hub Qdrant via Curador.

Fluxo (cron 30min):
  1. Lista .jsonl em _log/transcripts-claude-code/ (skip processados/)
  2. Pra cada arquivo:
     a. Lê conteúdo bruto (já redatado pelo retro_engine.py antes de commitar)
     b. Trunca pra MAX_CHARS pra evitar custo absurdo
     c. Roda hub.curador.curar_arquivo 2x:
        - user_id="gus"      → autobiografia do agente, decisões arquiteturais
        - user_id="gustavo"  → fatos sobre Gustavo extraídos da sessão
        Ambas chamadas rodam Haiku + GPT em paralelo (curador híbrido)
     d. Move arquivo pra processados/AAAA-MM/
  3. git commit + push das mudanças (cleanup transcripts processados)

Resolve a demanda 2026-05-01-curador-bidirecional-cron: hoje a porta Claude
Code não tem captura de memória (env vars ausentes no Code on the web,
hook Stop no-op). Caminho 2 = transcript commitado pela sessão + cron com
secrets do GitHub Actions processa.

Variáveis de ambiente necessárias:
  ANTHROPIC_API_KEY  — Haiku do curador
  OPENAI_API_KEY     — GPT-4o-mini do curador
  QDRANT_URL         — Hub vector store
  QDRANT_API_KEY     — idem
  GITHUB_TOKEN       — commit + push (já configurado no Actions)
"""

import asyncio
import logging
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

BRT = timezone(timedelta(hours=-3))
TRANSCRIPTS_DIR = Path("_log/transcripts-claude-code")
PROCESSADOS_DIR = TRANSCRIPTS_DIR / "processados"

MIN_CHARS = 200
MAX_CHARS = 50_000  # cap pra evitar transcript gigante explodindo custo


def _truncar(conteudo: str) -> str:
    if len(conteudo) <= MAX_CHARS:
        return conteudo
    meio = MAX_CHARS // 2
    return conteudo[:meio] + "\n\n[…transcript truncado…]\n\n" + conteudo[-meio:]


async def processar_transcript(path: Path) -> dict:
    """Roda curador 2x (gus + gustavo) sobre o transcript. Move pra processados/."""
    from hub.curador import curar_arquivo

    conteudo = path.read_text(encoding="utf-8", errors="ignore")

    if len(conteudo) < MIN_CHARS:
        return {"file": path.name, "skip": "muito_curto"}

    conteudo = _truncar(conteudo)

    resultados: dict = {"file": path.name}
    for user_id in ("gustavo", "gus"):
        try:
            r = await curar_arquivo(
                conteudo,
                via="claude-code",
                user_id=user_id,
            )
            resultados[user_id] = {
                "salvos": r.get("salvos", 0),
                "haiku": len(r.get("haiku", [])),
                "gpt": len(r.get("gpt", [])),
                "erros": r.get("erros", []),
            }
        except Exception as e:
            resultados[user_id] = {"erro": str(e)[:200]}

    return resultados


def mover_para_processados(path: Path) -> None:
    mes = datetime.now(BRT).strftime("%Y-%m")
    destino = PROCESSADOS_DIR / mes
    destino.mkdir(parents=True, exist_ok=True)
    shutil.move(str(path), str(destino / path.name))


def commit_push(branch: str = "main") -> None:
    try:
        subprocess.run(
            ["git", "config", "user.name", "github-actions[bot]"],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            ["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            ["git", "add", "_log/transcripts-claude-code/"],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        diff = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
        )
        if diff.returncode == 0:
            log.info("Nada pra commitar.")
            return
        subprocess.run(
            ["git", "commit", "-m", "auto: processa transcripts Claude Code"],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            ["git", "push", "origin", branch],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        log.info("Commit + push feito.")
    except subprocess.CalledProcessError as e:
        log.warning(f"git falhou: {e}")


async def main() -> None:
    if not TRANSCRIPTS_DIR.is_dir():
        log.info(f"{TRANSCRIPTS_DIR} não existe — nada a fazer")
        return

    transcripts = sorted(
        p for p in TRANSCRIPTS_DIR.glob("*.jsonl") if p.is_file()
    )

    if not transcripts:
        log.info("Nenhum transcript novo.")
        return

    log.info(f"Processando {len(transcripts)} transcript(s)…")

    for path in transcripts:
        try:
            resultado = await processar_transcript(path)
            log.info(f"OK {resultado}")
            mover_para_processados(path)
        except Exception as e:
            log.error(f"FAIL {path.name}: {e}")
            # Não move — próxima rodada tenta de novo

    commit_push()


if __name__ == "__main__":
    asyncio.run(main())
