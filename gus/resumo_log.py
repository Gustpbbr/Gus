"""
Log auditável dos resumos extrativos que vão pro Mem0.

A cada 3 turnos, bot.py:_resumir_e_salvar gera um resumo via Haiku
(gus/llm.py:gerar_resumo_turnos) e salva no Mem0. Esse módulo registra
TODOS os eventos (sucesso, descarte, erro) num MD diário no repo, pra
o Gustavo auditar no Obsidian.

PATH: _log/resumos-mem0/AAAA-MM-DD.md

FORMATO:
---
data: AAAA-MM-DD
fonte: bot Telegram (Haiku 4.5)
---

# Resumos pro Mem0 — DD/MM/AAAA

## HH:MM:SS BRT — <status>
**Turnos:** N (mensagens do trecho)
**Resumo:**
> texto do resumo, ou "(sem conteúdo relevante)", ou "(erro: ...)"

POR QUE: o Gustavo precisa fiscalizar se o Haiku está extraindo memórias
sensatas. Mem0 cloud não tem visualização nativa, e perder memórias por
erro silencioso (como aconteceu 24/04) é caro.

CUSTO: o write é pelo save_to_github (1 commit por resumo). Em pico de uso
intenso (10 resumos/dia) = 10 commits/dia. Aceitável — git aguenta.
"""

import asyncio
import logging
from datetime import datetime, timedelta, timezone

from gus.tools import _read_from_github, _save_to_github

logger = logging.getLogger(__name__)
BRT = timezone(timedelta(hours=-3))

PASTA = "_log/resumos-mem0"


def _formatar_entrada(resumo: str, num_turnos: int, status: str) -> str:
    """Bloco de uma entrada no log."""
    agora = datetime.now(BRT).strftime("%H:%M:%S")
    # Indenta resumo como blockquote markdown
    linhas_resumo = (resumo or "").splitlines() or ["(vazio)"]
    quoted = "\n".join(f"> {l}" for l in linhas_resumo)
    return (
        f"\n## {agora} BRT — {status}\n"
        f"**Turnos:** {num_turnos}\n"
        f"**Resumo:**\n{quoted}\n"
    )


def _frontmatter_inicial(data_iso: str) -> str:
    data_br = datetime.strptime(data_iso, "%Y-%m-%d").strftime("%d/%m/%Y")
    return (
        f"---\n"
        f"data: {data_iso}\n"
        f"fonte: bot Telegram (Haiku 4.5)\n"
        f"tipo: log-resumos-mem0\n"
        f"---\n\n"
        f"# Resumos pro Mem0 — {data_br}\n"
    )


async def append_resumo(resumo: str, num_turnos: int, status: str = "salvo") -> None:
    """Adiciona entrada no MD do dia. Silencioso em falha (não interrompe bot).

    Args:
        resumo: texto bruto do resumo do Haiku, ou mensagem de erro/descarte
        num_turnos: quantos turnos do trecho original foram resumidos
        status: 'salvo' | 'descartado' | 'erro' (livre, vai literal no MD)
    """
    try:
        hoje_iso = datetime.now(BRT).strftime("%Y-%m-%d")
        path = f"{PASTA}/{hoje_iso}.md"

        existente = await _read_from_github(path)
        nova_entrada = _formatar_entrada(resumo, num_turnos, status)

        if existente and not existente.startswith("Arquivo não encontrado"):
            conteudo = existente.rstrip() + "\n" + nova_entrada
        else:
            conteudo = _frontmatter_inicial(hoje_iso) + nova_entrada

        # _save_to_github salva sempre na main, com scan sensível
        resultado = await _save_to_github(hoje_iso, conteudo, PASTA)
        if "ATENÇÃO" in resultado or "Erro" in resultado:
            logger.warning(f"Falha ao logar resumo: {resultado[:200]}")
    except Exception as e:
        logger.warning(f"append_resumo falhou: {e}")


def append_resumo_async(resumo: str, num_turnos: int, status: str = "salvo") -> None:
    """Wrapper que dispara append_resumo em background — não bloqueia bot."""
    try:
        asyncio.create_task(append_resumo(resumo, num_turnos, status))
    except Exception as e:
        logger.warning(f"append_resumo_async falhou: {e}")
