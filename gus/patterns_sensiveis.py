"""
Fonte única de patterns de dados sensíveis (PII, credenciais, tokens).

Importado por:
  - gus/tools.py:_PATTERNS_SENSIVEIS — scan antes de save_to_github
  - .claude/hooks/scan_sensivel.py    — scan PreToolUse no Claude Code

Adicionar pattern novo aqui é suficiente — ambos os pontos pegam a referência.

Resolve R7 da auditoria (patterns duplicados em 2 lugares).
"""

import re

# Mapeamento {nome_humano → regex compilada}
PATTERNS_SENSIVEIS: dict[str, re.Pattern] = {
    # === Documentos de identidade brasileiros ===
    "CPF": re.compile(r"\b\d{3}[.\s]?\d{3}[.\s]?\d{3}[-\s]?\d{2}\b"),
    "CNPJ": re.compile(r"\b\d{2}[.\s]?\d{3}[.\s]?\d{3}/?\d{4}[-\s]?\d{2}\b"),

    # === Cartão de crédito (Luhn não validado, regex genérico) ===
    "cartão": re.compile(r"\b(?:\d[ -]?){13,19}\b"),

    # === API keys de provedores LLM ===
    "API key Anthropic": re.compile(r"\bsk-ant-[\w-]{20,}\b"),
    "API key OpenAI": re.compile(r"\bsk-[A-Za-z0-9]{40,}\b"),

    # === Tokens GitHub ===
    "GitHub PAT": re.compile(r"\b(?:ghp_|github_pat_)[\w]{20,}\b"),

    # === Memória / vector store ===
    "Mem0 key": re.compile(r"\bm0-[\w]{20,}\b"),
    "Qdrant API key": re.compile(r"\beyJhbGciOi[\w._-]{40,}\b"),  # JWT-like (Qdrant Cloud usa JWT)

    # === Busca web ===
    "Tavily key": re.compile(r"\btvly-[\w]{20,}\b"),

    # === Telegram ===
    # Bot token: <bot_id 8-10 dígitos>:<35 chars [A-Za-z0-9_-]>
    "Telegram bot token": re.compile(r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b"),

    # === Google ===
    # Service account private key (PEM)
    "Google service account key": re.compile(r"-----BEGIN (?:RSA )?PRIVATE KEY-----"),
    # OAuth client secret (formato típico: GOCSPX-...)
    "Google OAuth client secret": re.compile(r"\bGOCSPX-[\w-]{20,}\b"),

    # === Railway ===
    # Tokens não têm prefixo público claro, mas linhas tipo
    # "RAILWAY_API_TOKEN=<valor>" são alvo claro
    "Railway token (env line)": re.compile(
        r"RAILWAY[_A-Z]*TOKEN\s*[:=]\s*['\"]?[\w-]{20,}", re.IGNORECASE
    ),
}


def escanear(content: str) -> list[str]:
    """Retorna lista dos nomes de patterns encontrados no texto.

    Args:
        content: texto a escanear

    Returns:
        lista de nomes (vazia se nada encontrado). Pode conter duplicatas
        se o mesmo tipo aparecer múltiplas vezes — o caller geralmente
        usa `set(escanear(...))` se só importa "tem ou não tem".
    """
    encontrados = []
    for nome, padrao in PATTERNS_SENSIVEIS.items():
        if padrao.search(content):
            encontrados.append(nome)
    return encontrados


__all__ = ["PATTERNS_SENSIVEIS", "escanear"]
