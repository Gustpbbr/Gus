"""Utilidades compartilhadas pelas tools (validação, scan PII)."""

import re
from datetime import timezone, timedelta

from gus.patterns_sensiveis import PATTERNS_SENSIVEIS as _PATTERNS_SENSIVEIS

BRT = timezone(timedelta(hours=-3))

# Caracteres permitidos em nomes de arquivo e pastas.
# Ponto permitido pra pastas hidden legítimas (.github/, .claude/, .env.example).
# Traversal (..) bloqueado explicitamente em _validar_path.
_SAFE_PATH_RE = re.compile(r"^[a-zA-Z0-9\-_./]+$")


def _validar_path(path: str) -> str:
    """Valida path contra traversal e caracteres perigosos."""
    path = path.strip().lstrip("/")
    if ".." in path:
        raise ValueError(f"Path inválido (traversal): {path}")
    if not _SAFE_PATH_RE.match(path.replace(".md", "")):
        raise ValueError(f"Path contém caracteres não permitidos: {path}")
    return path


def _escanear_sensivel(content: str) -> list[str]:
    """Retorna lista dos tipos de dados sensíveis encontrados no texto.

    Padrões em fonte única `gus/patterns_sensiveis.py` (R7) — mesma lista
    usada pelo hook PreToolUse em `.claude/hooks/scan_sensivel.py`.
    """
    encontrados = []
    for nome, padrao in _PATTERNS_SENSIVEIS.items():
        if padrao.search(content):
            encontrados.append(nome)
    return encontrados
