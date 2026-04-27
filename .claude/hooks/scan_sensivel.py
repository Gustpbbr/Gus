#!/usr/bin/env python3
"""
PreToolUse hook — bloqueia escrita de dados sensíveis fora de sensivel/.

Importa patterns de `gus.patterns_sensiveis` (fonte única — R7).
A mesma lista é usada pelo bot Telegram em `gus/tools.py:_PATTERNS_SENSIVEIS`.

COMO FUNCIONA:
  1. Recebe via stdin um JSON com {tool_name, tool_input, ...}
  2. Se tool não for Write/Edit/NotebookEdit -> exit 0 (permite)
  3. Se path comeca com 'sensivel/' -> exit 0 (permite -- pasta dedicada)
  4. Senao escaneia o conteudo. Se achar PII/credenciais -> exit 2
     com mensagem em stderr (Claude ve e ajusta)

CONTORNO PROPOSITAL:
  Se realmente precisa salvar em path nao-sensivel (ex: documentar formato
  num exemplo), o hook nao detecta intent. Solucao pratica: salvar em
  sensivel/ ou usar exemplos com placeholder (XXX.XXX.XXX-XX em vez de
  numeros que casam com regex).
"""

import json
import sys
from pathlib import Path

# Adiciona repo root ao sys.path pra importar gus.patterns_sensiveis
_REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO_ROOT))

try:
    from gus.patterns_sensiveis import PATTERNS_SENSIVEIS as PATTERNS
except ImportError:
    # Fallback defensivo: se import falhar, hook degrada gracioso
    # (nao trava o Claude Code, mas avisa em stderr)
    print("[scan_sensivel] ATENCAO: gus.patterns_sensiveis indisponivel - hook degradado", file=sys.stderr)
    PATTERNS = {}

TOOLS_ALVO = ("Write", "Edit", "NotebookEdit")

# Allowlist: paths que podem conter dados sensiveis sem alarme
ALLOW_PREFIXES = (
    "sensivel/",
    "/sensivel/",
)


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        # Sem stdin parseavel - nao atrapalha, deixa passar
        return 0

    tool_name = data.get("tool_name") or ""
    tool_input = data.get("tool_input") or {}

    if tool_name not in TOOLS_ALVO:
        return 0

    file_path = (tool_input.get("file_path") or "").strip()
    # Normaliza pra busca de prefixo: tira /home/user/Gus/ se vier absoluto
    rel_path = file_path
    for marker in ("/Gus/", "/home/user/Gus/"):
        idx = rel_path.find(marker)
        if idx >= 0:
            rel_path = rel_path[idx + len(marker):]
            break

    if any(rel_path.startswith(p) for p in ALLOW_PREFIXES):
        return 0

    # Conteudo a escanear depende da tool
    if tool_name == "Write":
        content = tool_input.get("content", "") or ""
    elif tool_name == "Edit":
        content = tool_input.get("new_string", "") or ""
    elif tool_name == "NotebookEdit":
        content = tool_input.get("new_source", "") or ""
    else:
        content = ""

    if not content:
        return 0

    encontrados = []
    for nome, padrao in PATTERNS.items():
        if padrao.search(content):
            encontrados.append(nome)

    if not encontrados:
        return 0

    # Bloqueia. stderr vai pro contexto do Claude.
    msg = (
        f"[scan_sensivel] BLOQUEADO em '{file_path}': "
        f"detectado {', '.join(encontrados)}.\n"
        "Mova pra 'sensivel/<subpasta>/' (nao vai pro Drive sync), "
        "ou peca confirmacao explicita ao usuario antes de salvar no path original."
    )
    print(msg, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
