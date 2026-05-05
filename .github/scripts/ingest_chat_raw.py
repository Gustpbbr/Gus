#!/usr/bin/env python3
"""
Ingest de memórias geradas pelo Claude Chat → Hub Qdrant (via Curador híbrido).

Fluxo (cron 30min):
  1. Lista .md em dialogos/inbox-chat-raw/ (skip processados/)
  2. Pra cada arquivo:
     a. Parse frontmatter + body
     b. Curador bidirecional roda 2x sobre o mesmo body:
          - user_id="gustavo" → fatos sobre o Gustavo
          - user_id="gus"     → autobiografia do agente
        Cada chamada é o curador híbrido (Haiku + GPT em paralelo). Total:
        4 conjuntos de fragmentos no Hub por arquivo.
     c. Move arquivo pra processados/AAAA-MM/
     d. Append linha em _log/curador/AAAA-MM-DD.md por (curador, brain)
        com mesmo hash_janela permitindo parear no Obsidian.
  3. git commit + push das mudanças

Idempotência: depois do move, arquivo não é reentrado. Se Hub falhar antes do
move, próxima rodada tenta de novo (pode duplicar — risco baixo dado o volume).

Substitui o caminho antigo via Mem0 SaaS (ADR-001 Fase 5 — Mem0 aposentado).

Variáveis de ambiente necessárias:
  ANTHROPIC_API_KEY  — Haiku/Sonnet do Curador
  OPENAI_API_KEY     — GPT do Curador (mini ou full, configurável)
  QDRANT_URL         — Hub vector store
  QDRANT_API_KEY     — idem
  GITHUB_TOKEN       — commit + push automático (já configurado no Actions)

Modelos do curador são configuráveis via MODEL_CURADOR_HAIKU / MODEL_CURADOR_GPT
(setados no workflow YAML). Default: claude-haiku-4-5 + gpt-4o-mini. Workflow
do Chat sobe pra claude-sonnet-4-6 + gpt-4o (porta de reflexão profunda).
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
INBOX = Path("dialogos/inbox-chat-raw")
PROCESSADOS = INBOX / "processados"
PROCESSADOS_ERRO = INBOX / "processados-erro"
LOG_DIR = Path("_log/curador")


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
    """Loga uma entrada no MD diário do _log/curador/.

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
            f"fonte: ingest claude-chat (Hub Curador híbrido Anthropic+OpenAI)\n"
            f"tipo: log-curador\n---\n\n# Resumos pro Hub — {hoje}\n\n",
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


def mover_pra_processados_erro(arquivo: Path, motivo: str) -> Path:
    """Move arquivo que falhou repetidamente pra processados-erro/.

    Antes (V1) arquivos com erro permanecente ficavam no inbox e eram
    reprocessados a cada 30min — loop infinito que gastava créditos sem
    resolver. Agora vão pra processados-erro/AAAA-MM/ com header explicando
    o motivo, e Gustavo decide o que fazer (corrigir, reenviar, descartar).
    """
    mes = datetime.now(BRT).strftime("%Y-%m")
    destino_dir = PROCESSADOS_ERRO / mes
    destino_dir.mkdir(parents=True, exist_ok=True)
    destino = destino_dir / arquivo.name

    # Prepende cabeçalho com motivo + timestamp pra debug futuro
    try:
        conteudo_original = arquivo.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        conteudo_original = "[falha ao ler conteúdo original]"

    cabecalho = (
        f"<!-- ERRO ao processar este arquivo -->\n"
        f"<!-- Motivo: {motivo} -->\n"
        f"<!-- Movido em: {datetime.now(BRT).isoformat()} -->\n\n"
    )
    destino.write_text(cabecalho + conteudo_original, encoding="utf-8")
    arquivo.unlink()
    return destino


def git_commit_push(mensagem: str) -> None:
    subprocess.run(["git", "config", "user.name", "gus-bot"], check=True)
    subprocess.run(["git", "config", "user.email", "gus-bot@users.noreply.github.com"], check=True)
    # -A em dialogos/inbox-chat-raw captura processados/, processados-erro/
    # e remove os arquivos movidos do inbox. Inclui _log/ pra registro auditável.
    subprocess.run(["git", "add", "-A", "dialogos/inbox-chat-raw", "_log/curador"], check=True)
    diff = subprocess.run(["git", "diff", "--staged", "--quiet"]).returncode
    if diff == 0:
        log.info("Nada pra commitar")
        return
    subprocess.run(["git", "commit", "-m", mensagem], check=True)
    # Retry exponencial (2/4/8/16s) — network blip no GH Actions runner não
    # deve descartar o commit que já entrou no Hub. Fragmentos foram salvos
    # antes do push; sem retry, próxima rodada commita de novo + duplica.
    import time as _time
    for tentativa in range(4):
        try:
            subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
            return
        except subprocess.CalledProcessError as e:
            if tentativa == 3:
                raise
            espera = 2 ** (tentativa + 1)  # 2, 4, 8, 16
            log.warning(f"git push falhou (tentativa {tentativa+1}/4), aguardando {espera}s: {e}")
            _time.sleep(espera)


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
        log.info("Nenhum arquivo novo em inbox-chat-raw/")
        return

    log.info(f"{len(arquivos)} arquivo(s) a processar")
    salvos_total = vazios = erros = 0

    for arq in arquivos:
        log.info(f"→ {arq.name}")
        try:
            content = arq.read_text(encoding="utf-8")
        except Exception as e:
            log.error(f"  read falhou: {e}")
            append_log(arq.name, "erro", None, None, 0, "", motivo=f"read falhou: {e}")
            mover_pra_processados_erro(arq, f"read falhou: {e}")
            erros += 1
            continue

        fm, body = parse_frontmatter(content)
        body_efetivo = (body or content).strip()

        if not body_efetivo:
            append_log(arq.name, "descartado", None, None, 0, "", motivo="arquivo vazio")
            mover_pra_processados(arq)
            vazios += 1
            continue

        # Curador bidirecional: roda 2x sobre o mesmo body, brains diferentes.
        #   user_id="gustavo" → fatos sobre o Gustavo (reflexões, decisões, sentimentos)
        #   user_id="gus"     → autobiografia do agente (identidade, padrões, autoself)
        # Chat é a porta de reflexão profunda — captura ambos os lados da conversa.
        falhou = False
        motivo_falha = ""
        salvos_arq_total = 0
        for user_id in ("gustavo", "gus"):
            try:
                resultado = asyncio.run(
                    curar_arquivo(body_efetivo, via="claude-chat", user_id=user_id)
                )
            except Exception as e:
                log.error(f"  Curador {user_id} falhou: {e}")
                falhou = True
                motivo_falha = f"curador {user_id} falhou: {type(e).__name__}: {str(e)[:200]}"
                break  # próxima rodada não retenta — vai pra processados-erro

            hash_j = resultado.get("hash_janela", "")
            haiku_frags = resultado.get("haiku", [])
            gpt_frags = resultado.get("gpt", [])
            salvos_arq_total += resultado.get("salvos", 0)
            erros_curador = resultado.get("erros", [])

            # Log dual por brain (uma entrada por curador, mesmo hash_janela)
            for nome, frags in (("haiku", haiku_frags), ("gpt", gpt_frags)):
                curador_label = f"{nome}/{user_id}"
                if frags:
                    preview = "; ".join(f.get("conteudo", "")[:60] for f in frags[:3])
                    append_log(arq.name, "salvo", curador_label, hash_j, len(frags), preview)
                else:
                    append_log(
                        arq.name, "descartado", curador_label, hash_j, 0, body_efetivo,
                        motivo="nenhum fragmento extraído",
                    )

            for err in erros_curador:
                log.warning(f"  Curador {user_id} erro parcial: {err}")

            log.info(
                f"  ✓ {user_id}: haiku={len(haiku_frags)} gpt={len(gpt_frags)} "
                f"salvos+={resultado.get('salvos', 0)} hash={hash_j}"
            )

        if falhou:
            # Move pra processados-erro/ pra evitar loop infinito.
            # Se a falha for transitória (Anthropic 5xx, network), Gustavo pode
            # mover de volta pro inbox manualmente. Pra erros permanentes
            # (auth, billing, key error de código nosso) vai ficar lá pra debug.
            append_log(arq.name, "erro", None, None, 0, "", motivo=motivo_falha)
            mover_pra_processados_erro(arq, motivo_falha)
            erros += 1
            continue
        mover_pra_processados(arq)
        salvos_total += salvos_arq_total

    log.info(
        f"Resumo: {salvos_total} fragmentos salvos no Hub, "
        f"{vazios} vazios, {erros} erros (movidos pra processados-erro/)"
    )

    if salvos_total or vazios or erros:
        git_commit_push(
            f"auto: ingest claude-chat → Hub ({salvos_total} fragmentos, {vazios} vazios, {erros} erros)"
        )


if __name__ == "__main__":
    main()
