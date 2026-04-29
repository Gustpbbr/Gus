#!/usr/bin/env python3
"""
Ingest de memórias geradas pelo Claude Chat → Hub Qdrant (via Curador híbrido).

Fluxo (cron 30min):
  1. Lista .md em dialogos/inbox-mem0-from-chat/ (skip processados/)
  2. Pra cada arquivo:
     a. Parse frontmatter + body
     b. Curador híbrido (Haiku + Sonnet em paralelo) extrai e classifica
        fragmentos do body. Cada modelo salva no Hub Qdrant (gus_hub) com
        metadata.curador distinta + mesmo hash_janela.
     c. Move arquivo pra processados/AAAA-MM/
     d. Append linha em _log/resumos-mem0/AAAA-MM-DD.md (uma linha por curador
        com mesmo hash, igual ao bot Telegram)
  3. git commit + push das mudanças

Idempotência: depois do move, arquivo não é reentrado. Se Hub falhar antes do
move, próxima rodada tenta de novo (pode duplicar — risco baixo dado o volume).

Substitui o caminho antigo via Mem0 SaaS (ADR-001 Fase 5 — Mem0 aposentado).

Variáveis de ambiente necessárias:
  ANTHROPIC_API_KEY  — chamadas Haiku + Sonnet do Curador
  QDRANT_URL         — Hub vector store
  QDRANT_API_KEY     — idem
  GITHUB_TOKEN       — commit + push automático (já configurado no Actions)
"""

import logging
import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

# Adiciona repo root ao sys.path pra importar hub.curador
# (mesmo pattern de gerar_estado_atual_chat.py e _hub_compat.py)
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

BRT = timezone(timedelta(hours=-3))
INBOX = Path("dialogos/inbox-mem0-from-chat")
PROCESSADOS = INBOX / "processados"
LOG_DIR = Path("_log/resumos-mem0")


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


def append_log(
    arquivo_nome: str,
    status: str,
    curador: str | None,
    hash_janela: str | None,
    num_fragmentos: int,
    body_preview: str,
    motivo: str = "",
) -> None:
    """Loga uma entrada no MD diário do _log/resumos-mem0/.

    Formato compatível com o bot Telegram pós-Fase 2 (uma entrada por curador
    com mesmo hash_janela permite parear no Obsidian).
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    hoje = datetime.now(BRT).strftime("%Y-%m-%d")
    log_path = LOG_DIR / f"{hoje}.md"
    agora = datetime.now(BRT).strftime("%H:%M:%S")

    if not log_path.exists():
        log_path.write_text(
            f"---\ndata: {hoje}\n"
            f"fonte: ingest claude-chat (Hub Curador híbrido Haiku+Sonnet)\n"
            f"tipo: log-resumos-mem0\n---\n\n# Resumos pro Hub — {hoje}\n\n",
            encoding="utf-8",
        )

    if curador and hash_janela:
        header = f"## {agora} BRT — {status} (curador: {curador}, janela: {hash_janela})"
    elif curador:
        header = f"## {agora} BRT — {status} (curador: {curador})"
    else:
        header = f"## {agora} BRT — {status}"

    preview = body_preview.replace("\n", " ")[:280]
    linhas = [
        header,
        f"**Origem:** claude-chat",
        f"**Arquivo:** `{arquivo_nome}`",
        f"**Fragmentos:** {num_fragmentos}",
    ]
    if motivo:
        linhas.append(f"**Motivo:** {motivo}")
    linhas.append(f"**Preview:** {preview}")
    entrada = "\n".join(linhas) + "\n\n"

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
    # Vars necessárias pro Curador + Hub
    if not os.environ.get("ANTHROPIC_API_KEY"):
        log.error("ANTHROPIC_API_KEY ausente")
        sys.exit(1)
    if not os.environ.get("QDRANT_URL") or not os.environ.get("QDRANT_API_KEY"):
        log.error("QDRANT_URL ou QDRANT_API_KEY ausentes")
        sys.exit(1)

    # Import lazy — ambiente do workflow precisa ter qdrant-client + sentence-transformers
    # (já em requirements.txt desde a Fase 1)
    import asyncio
    from hub.curador import curar_arquivo

    if not INBOX.exists():
        log.info(f"{INBOX}/ não existe ainda — nada a ingerir")
        return

    arquivos = sorted(
        f for f in INBOX.glob("*.md")
        if f.is_file() and PROCESSADOS not in f.parents and not f.name.startswith("_README")
    )
    if not arquivos:
        log.info("Nenhum arquivo novo em inbox-mem0-from-chat/")
        return

    log.info(f"{len(arquivos)} arquivo(s) a processar")
    salvos_total = vazios = erros = 0

    for arq in arquivos:
        log.info(f"→ {arq.name}")
        try:
            content = arq.read_text(encoding="utf-8")
        except Exception as e:
            log.error(f"  read falhou: {e}")
            erros += 1
            continue

        fm, body = parse_frontmatter(content)
        body_efetivo = (body or content).strip()

        if not body_efetivo:
            append_log(arq.name, "descartado", None, None, 0, "", motivo="arquivo vazio")
            mover_pra_processados(arq)
            vazios += 1
            continue

        # Roda Curador híbrido sobre o body
        try:
            resultado = asyncio.run(
                curar_arquivo(body_efetivo, via="claude-chat", user_id="gustavo")
            )
        except Exception as e:
            log.error(f"  Curador falhou (não move arquivo, próxima rodada tenta): {e}")
            erros += 1
            continue  # NÃO move — próxima rodada tenta de novo

        hash_j = resultado.get("hash_janela", "")
        haiku_frags = resultado.get("haiku", [])
        sonnet_frags = resultado.get("sonnet", [])
        salvos_arq = resultado.get("salvos", 0)
        erros_curador = resultado.get("erros", [])

        # Log dual (uma entrada por curador, mesmo hash_janela)
        for nome, frags in (("haiku", haiku_frags), ("sonnet", sonnet_frags)):
            if frags:
                preview = "; ".join(f.get("conteudo", "")[:60] for f in frags[:3])
                append_log(arq.name, "salvo", nome, hash_j, len(frags), preview)
            else:
                append_log(arq.name, "descartado", nome, hash_j, 0, body_efetivo, motivo="nenhum fragmento extraído")

        for err in erros_curador:
            log.warning(f"  Curador erro parcial: {err}")

        log.info(
            f"  ✓ haiku={len(haiku_frags)} sonnet={len(sonnet_frags)} "
            f"salvos={salvos_arq} hash={hash_j}"
        )
        mover_pra_processados(arq)
        salvos_total += salvos_arq

    log.info(f"Resumo: {salvos_total} fragmentos salvos no Hub, {vazios} vazios, {erros} erros")

    if salvos_total or vazios:
        git_commit_push(
            f"auto: ingest claude-chat → Hub ({salvos_total} fragmentos, {vazios} vazios)"
        )


if __name__ == "__main__":
    main()
