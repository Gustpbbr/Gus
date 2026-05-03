#!/usr/bin/env python3
"""
Limpeza ativa do Hub — APLICAR (item 1.7 do plano de saneamento).

IRREVERSÍVEL. Lê o relatório dryrun (`_indices/_limpeza-hub-candidatos.md`)
extraindo os IDs candidatos, exclui os listados em
`_indices/_limpeza-hub-rejeitados.txt` (1 ID por linha) e deleta o resto.

Cada delete grava trilha em `_log/deletar-hub/AAAA-MM-DD.jsonl` (item 1.3
do plano), com snapshot completo do payload pra recovery.

Fluxo:
  1. Dry-run (`limpeza_hub_dryrun.py`) gera lista
  2. Gustavo revisa MD, opcionalmente cria `_limpeza-hub-rejeitados.txt`
     com IDs que quer manter
  3. Este script é disparado manualmente via workflow
  4. Após aplicação, sobe arquivo `_log/limpeza-hub-aplicado-AAAA-MM-DD.md`
     com sumário do que foi deletado

Variáveis de ambiente:
  QDRANT_URL, QDRANT_API_KEY
  LIMPEZA_DRYRUN=1  → loga o que faria mas não deleta (default 0)

Usage:
  Workflow `limpeza-hub-aplicar.yml` (manual dispatch).
"""

import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

BRT = timezone(timedelta(hours=-3))
INPUT_MD = "_indices/_limpeza-hub-candidatos.md"
INPUT_REJEITADOS = "_indices/_limpeza-hub-rejeitados.txt"
OUTPUT_LOG_DIR = "_log/limpeza-hub"

# Regex pra capturar ID nas headings tipo `### \`<uuid>\`` no MD do dryrun
ID_HEADING_RE = re.compile(r"^###\s+`([0-9a-f-]{32,40})`\s*$", re.MULTILINE)


def _ler_ids_candidatos(md_path: str) -> list[str]:
    if not Path(md_path).exists():
        print(f"ERRO: {md_path} não encontrado. Rode `limpeza_hub_dryrun.py` antes.")
        sys.exit(1)
    conteudo = Path(md_path).read_text(encoding="utf-8")
    ids = ID_HEADING_RE.findall(conteudo)
    print(f"  Lidos {len(ids)} IDs candidatos de {md_path}")
    return ids


def _ler_ids_rejeitados(rej_path: str) -> set[str]:
    p = Path(rej_path)
    if not p.exists():
        print(f"  Sem rejeições — todos os candidatos serão deletados ({rej_path} não existe).")
        return set()
    linhas = [
        l.strip() for l in p.read_text(encoding="utf-8").splitlines()
        if l.strip() and not l.strip().startswith("#")
    ]
    print(f"  {len(linhas)} IDs rejeitados em {rej_path}")
    return set(linhas)


def main() -> None:
    if not os.environ.get("QDRANT_URL") or not os.environ.get("QDRANT_API_KEY"):
        print("QDRANT_URL/QDRANT_API_KEY ausentes. Pulado.")
        sys.exit(0)

    dryrun_flag = os.environ.get("LIMPEZA_DRYRUN", "0") == "1"

    print(f"=== Limpeza Hub — APLICAR ({'DRYRUN' if dryrun_flag else 'EXECUTANDO'}) ===")
    candidatos = _ler_ids_candidatos(INPUT_MD)
    rejeitados = _ler_ids_rejeitados(INPUT_REJEITADOS)

    a_deletar = [i for i in candidatos if i not in rejeitados]
    print(f"  A deletar: {len(a_deletar)} ({len(candidatos)} candidatos − {len(rejeitados)} rejeitados)")

    if not a_deletar:
        print("Nada a fazer.")
        sys.exit(0)

    from hub.store import deletar as hub_deletar

    sucesso = 0
    erros: list[tuple[str, str]] = []
    for mid in a_deletar:
        if dryrun_flag:
            print(f"  [DRYRUN] deletar {mid}")
            sucesso += 1
            continue
        try:
            hub_deletar(mid, motivo=f"limpeza_hub_aplicar (item 1.7)")
            sucesso += 1
            print(f"  OK delete {mid}")
        except Exception as e:
            erros.append((mid, str(e)[:200]))
            print(f"  ERRO delete {mid}: {e}")

    # Sumário em _log/limpeza-hub/AAAA-MM-DD.md
    hoje = datetime.now(BRT).strftime("%Y-%m-%d")
    Path(OUTPUT_LOG_DIR).mkdir(parents=True, exist_ok=True)
    out_path = Path(OUTPUT_LOG_DIR) / f"{hoje}.md"
    linhas = [
        "---",
        f"data: {hoje}",
        f"executado_em: {datetime.now(BRT).isoformat()}",
        f"modo: {'dryrun' if dryrun_flag else 'aplicar'}",
        f"candidatos_total: {len(candidatos)}",
        f"rejeitados_total: {len(rejeitados)}",
        f"deletados_sucesso: {sucesso}",
        f"deletados_erro: {len(erros)}",
        "---",
        "",
        f"# Limpeza Hub — execução {hoje}",
        "",
        f"Modo: {'**DRYRUN** (nada foi deletado)' if dryrun_flag else 'aplicação real'}",
        "",
        f"- **Candidatos lidos:** {len(candidatos)}",
        f"- **Rejeitados (mantidos):** {len(rejeitados)}",
        f"- **Deletados com sucesso:** {sucesso}",
        f"- **Erros:** {len(erros)}",
        "",
    ]
    if erros:
        linhas.append("## Erros")
        linhas.append("")
        for mid, err in erros:
            linhas.append(f"- `{mid}`: {err}")
        linhas.append("")
    linhas.append("Trilha completa de cada delete (com snapshot do payload "
                  "pré-delete) em `_log/deletar-hub/AAAA-MM-DD.jsonl`.")
    out_path.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"\nSumário escrito: {out_path}")


if __name__ == "__main__":
    main()
