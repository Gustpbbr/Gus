"""
Log auditável dos resumos / fragmentos curados que vão pro Mem0/Hub.

A cada 3 turnos, bot.py:_resumir_e_salvar dispara curadoria via
hub/curador.py:curar_turnos (Haiku + GPT-4o-mini em paralelo, ambos salvam
no Hub Qdrant com metadata.curador distinta). Item 1.6 do plano de
saneamento (02/05/2026) removeu o caminho `fallback-mem0` legado — quando
o curador inteiro falha, o status registrado agora é `erro_curador_total`
e a janela é perdida (preferível a poluir Hub com resumo bruto sem schema).

Esse módulo registra TODOS os eventos (sucesso, descarte, erro)
num MD diário no repo, pra o Gustavo auditar no Obsidian.

PATH: _log/curador/AAAA-MM-DD.md

FORMATO (atualizado Fase 2.5 — gus-29 trocou Sonnet por GPT-4o-mini):
---
data: AAAA-MM-DD
fonte: bot Telegram (Hub Curador híbrido Anthropic+OpenAI)
tipo: log-resumos-mem0
---

# Resumos pro Hub — DD/MM/AAAA

## HH:MM:SS BRT — salvo (curador: haiku, janela: a3f29b1c)
**Turnos:** 6
**Fragmentos:** 3
**Resumo:**
> 1. Gustavo decidiu adotar Qdrant direto, aposentar Mem0
> 2. ...

## HH:MM:SS BRT — salvo (curador: gpt, janela: a3f29b1c)
**Turnos:** 6
**Fragmentos:** 5
**Resumo:**
> 1. ...

(2 entradas com mesmo hash_janela permitem comparar Anthropic × OpenAI
 para o MESMO trecho de input)

POR QUE: o Gustavo precisa fiscalizar se a curadoria está extraindo
memórias sensatas. Qdrant não tem visualização nativa, e perder
memórias por erro silencioso (como aconteceu 24/04) é caro.

CUSTO: o write é pelo save_to_github (1 commit por entrada). Em pico
de uso intenso com curador híbrido = ~20 commits/dia. Aceitável.
"""

import asyncio
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

from gus.tools import _read_from_github, _save_to_github

logger = logging.getLogger(__name__)
BRT = timezone(timedelta(hours=-3))

PASTA = "_log/curador"


def _formatar_entrada(
    resumo: str,
    num_turnos: int,
    status: str,
    curador: Optional[str] = None,
    hash_janela: Optional[str] = None,
    num_fragmentos: Optional[int] = None,
) -> str:
    """Bloco de uma entrada no log.

    Args:
        resumo: texto do resumo / fragmentos extraídos / mensagem de erro
        num_turnos: quantos turnos do trecho cobertos
        status: 'salvo' | 'descartado' | 'erro' | 'erro_curador_total'
        curador: 'haiku' | 'gpt' | None (legado/fallback sem curador). 'sonnet'
                 aparece em entradas históricas pré-29/04 (gus-29 Fase 3 trocou).
        hash_janela: sha8 do input — permite parear curadores diferentes
        num_fragmentos: quantos fragmentos extraídos pelo curador
    """
    agora = datetime.now(BRT).strftime("%H:%M:%S")

    # Cabeçalho com assinatura quando aplicável
    if curador and hash_janela:
        header = f"## {agora} BRT — {status} (curador: {curador}, janela: {hash_janela})"
    elif curador:
        header = f"## {agora} BRT — {status} (curador: {curador})"
    else:
        header = f"## {agora} BRT — {status}"

    linhas = [header, f"**Turnos:** {num_turnos}"]
    if num_fragmentos is not None:
        linhas.append(f"**Fragmentos:** {num_fragmentos}")

    # Indenta resumo como blockquote markdown
    linhas_resumo = (resumo or "").splitlines() or ["(vazio)"]
    quoted = "\n".join(f"> {l}" for l in linhas_resumo)
    linhas.append("**Resumo:**")
    linhas.append(quoted)

    return "\n" + "\n".join(linhas) + "\n"


def _frontmatter_inicial(data_iso: str) -> str:
    data_br = datetime.strptime(data_iso, "%Y-%m-%d").strftime("%d/%m/%Y")
    return (
        f"---\n"
        f"data: {data_iso}\n"
        f"fonte: bot Telegram (Hub Curador híbrido Anthropic+OpenAI)\n"
        f"tipo: log-resumos-mem0\n"
        f"---\n\n"
        f"# Resumos pro Hub — {data_br}\n"
    )


async def append_resumo(
    resumo: str,
    num_turnos: int,
    status: str = "salvo",
    curador: Optional[str] = None,
    hash_janela: Optional[str] = None,
    num_fragmentos: Optional[int] = None,
) -> None:
    """Adiciona entrada no MD do dia. Silencioso em falha (não interrompe bot).

    Args:
        resumo: texto bruto do resumo / fragmentos / mensagem de erro
        num_turnos: quantos turnos do trecho original foram resumidos
        status: 'salvo' | 'descartado' | 'erro' | 'erro_curador_total'
        curador: 'haiku' | 'sonnet' | None pra entradas legadas/fallback
        hash_janela: sha8 do input pra parear curadores diferentes
        num_fragmentos: quantos fragmentos atômicos o curador extraiu
    """
    try:
        hoje_iso = datetime.now(BRT).strftime("%Y-%m-%d")
        path = f"{PASTA}/{hoje_iso}.md"

        existente = await _read_from_github(path)
        nova_entrada = _formatar_entrada(
            resumo, num_turnos, status, curador, hash_janela, num_fragmentos
        )

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


def append_resumo_async(
    resumo: str,
    num_turnos: int,
    status: str = "salvo",
    curador: Optional[str] = None,
    hash_janela: Optional[str] = None,
    num_fragmentos: Optional[int] = None,
) -> None:
    """Wrapper que dispara append_resumo em background — não bloqueia bot."""
    try:
        asyncio.create_task(
            append_resumo(resumo, num_turnos, status, curador, hash_janela, num_fragmentos)
        )
    except Exception as e:
        logger.warning(f"append_resumo_async falhou: {e}")
