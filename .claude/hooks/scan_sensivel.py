#!/usr/bin/env python3
"""
PreToolUse hook — bloqueia escrita de dados sensíveis fora de sensivel/.

Espelha exatamente os padrões usados pelo bot em produção
(`gus/tools.py:_PATTERNS_SENSIVEIS`), garantindo defesa de profundidade
quando o Claude Code faz Write/Edit/NotebookEdit aqui.

COMO FUNCIONA:
  1. Recebe via stdin um JSON com {tool_name, tool_input, ...}
  2. Se tool não for Write/Edit/NotebookEdit → exit 0 (permite)
  3. Se path começar com 'sensivel/' → exit 0 (permite — pasta dedicada)
  4. Senão escaneia o conteúdo. Se achar CPF/CNPJ/cartão/key → exit 2
     com mensagem em stderr (Claude vê e ajusta)

CONTORNO PROPOSITAL:
  Se o usuário REALMENTE quer salvar em path não-sensivel (ex: documentar
  formato de CPF num exemplo), pode pedir 'use bypass' — mas o hook não
  detecta intent. Solução prática: salvar em sensivel/ ou citar valores
  fictícios (123.456.789-00, etc. — pattern bate, mas é o trade-off
  aceito; o usuário pode ajustar o exemplo pra não bater).
"""

import json
import re
import sys

PATTERNS = {
    "CPF": re.compile(r"\b\d{3}[.\s]?\d{3}[.\s]?\d{3}[-\s]?\d{2}\b"),
    "CNPJ": re.compile(r"\b\d{2}[.\s]?\d{3}[.\s]?\d{3}/?\d{4}[-\s]?\d{2}\b"),
    "cartão": re.compile(r"\b(?:\d[ -]?){13,19}\b"),
    "API key Anthropic": re.compile(r"\bsk-ant-[\w-]{20,}\b"),
    "API key OpenAI": re.compile(r"\bsk-[A-Za-z0-9]{40,}\b"),
    "GitHub PAT": re.compile(r"\b(?:ghp_|github_pat_)[\w]{20,}\b"),
    "Mem0 key": re.compile(r"\bm0-[\w]{20,}\b"),
    "Tavily key": re.compile(r"\btvly-[\w]{20,}\b"),
}

TOOLS_ALVO = ("Write", "Edit", "NotebookEdit")

# Allowlist: paths que podem conter dados sensíveis sem alarme
ALLOW_PREFIXES = (
    "sensivel/",
    "/sensivel/",
)


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        # Sem stdin parseável — não atrapalha, deixa passar
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

    # Conteúdo a escanear depende da tool
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
        "Mova pra 'sensivel/<subpasta>/' (não vai pro Drive sync), "
        "ou peça confirmação explícita ao usuário antes de salvar no path original."
    )
    print(msg, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
