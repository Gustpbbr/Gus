---
tipo: guia-implementacao
data: 2026-04-26
status: pronto-para-implementar
area: infra-hub
anterior: gus-21-etapa3-curador.md
proximo: gus-23-logica-qdrant-mem0.md
---

# Etapas 4 e 5 — Ego Cache dinâmico + Auto-relato narrativo

Etapa 4: o Ego Cache consulta o Hub e monta um JSON priorizado com os fragmentos
mais relevantes por tipo. Resultado entra no system prompt de qualquer porta no boot.

Etapa 5: o Auto-relato usa Haiku para transformar o Ego Cache em texto narrativo
em PT-BR. Cache de 2h — não regenera a cada mensagem.

## Arquivos

- `hub/ego_cache.py` — formata ego cache como texto injetável
- `hub/auto_relato.py` — gera narrativa com Haiku, com cache
- `gus/llm.py` — integração: system prompt base + auto-relato no boot

## `hub/ego_cache.py`

```python
"""
Formata o ego cache do Hub como bloco de texto para injeção no system prompt.
Chamado no boot de cada porta — leve, sem LLM, só leitura do Qdrant.
"""

import asyncio
from hub.store import ego_cache


def formatar_ego_cache(cache: dict) -> str:
    blocos = []

    identidade = cache.get("identidade", [])
    if identidade:
        linhas = [f"- {f['conteudo']}" for f in identidade if f.get("conteudo")]
        if linhas:
            blocos.append("## Identidade operacional\n" + "\n".join(linhas))

    protegidos = cache.get("protegidos", [])
    if protegidos:
        linhas = [f"- {f['conteudo']}" for f in protegidos if f.get("conteudo")]
        if linhas:
            blocos.append("## Políticas e procedimentos\n" + "\n".join(linhas))

    decisoes = cache.get("decisoes_recentes", [])
    if decisoes:
        linhas = [f"- {f['conteudo']}" for f in decisoes if f.get("conteudo")]
        if linhas:
            blocos.append("## Decisões recentes\n" + "\n".join(linhas))

    reflexoes = cache.get("meta_reflexoes", [])
    if reflexoes:
        linhas = [f"- {f['conteudo']}" for f in reflexoes if f.get("conteudo")]
        if linhas:
            blocos.append("## Auto-observações\n" + "\n".join(linhas))

    if not blocos:
        return ""

    return "# Contexto do Gus (ego cache)\n\n" + "\n\n".join(blocos)


async def obter_ego_cache_formatado(user_id: str = "gustavo") -> str:
    """Versão async — chama store e formata. Pronto para injeção."""
    try:
        cache = await asyncio.to_thread(ego_cache, user_id)
        return formatar_ego_cache(cache)
    except Exception:
        return ""
```

## `hub/auto_relato.py`

```python
"""
Gera texto narrativo do estado atual do Gus a partir do ego cache.
Usa Haiku para síntese. Cache em memória de 2h — não regenera a cada boot.
"""

import os
import time
import asyncio
import logging
import anthropic

from hub.store import ego_cache
from hub.ego_cache import formatar_ego_cache

logger = logging.getLogger(__name__)

CACHE_TTL = 2 * 3600  # 2 horas

_cache: dict[str, tuple[float, str]] = {}  # user_id → (timestamp, texto)

PROMPT_NARRATIVO = """Com base neste ego cache do Gus, escreva um parágrafo curto (3-5 frases) em PT-BR informal que o Gus usaria para se apresentar no início de uma sessão.

O texto deve:
- Dizer quem o Gus é e qual seu propósito
- Mencionar o contexto atual mais relevante (decisões recentes, projetos ativos)
- Indicar auto-observações operacionais relevantes
- Ser direto, sem floreios
- Estar em primeira pessoa

Ego cache:
{ego_cache}

Escreva apenas o parágrafo, sem título nem explicação."""


async def gerar_auto_relato(user_id: str = "gustavo", forcar: bool = False) -> str:
    """Retorna texto narrativo. Usa cache se fresco, regenera se expirado."""
    agora = time.time()

    if not forcar and user_id in _cache:
        ts, texto = _cache[user_id]
        if agora - ts < CACHE_TTL:
            return texto

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return ""

    try:
        cache = await asyncio.to_thread(ego_cache, user_id)
        cache_texto = formatar_ego_cache(cache)

        if not cache_texto:
            return ""

        client = anthropic.AsyncAnthropic(api_key=api_key)
        resp = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            messages=[{
                "role": "user",
                "content": PROMPT_NARRATIVO.format(ego_cache=cache_texto)
            }]
        )
        texto = next((b.text for b in resp.content if hasattr(b, "text")), "").strip()
        _cache[user_id] = (agora, texto)
        logger.info(f"auto-relato regenerado para user_id={user_id}")
        return texto

    except Exception as e:
        logger.warning(f"auto-relato: erro — {e}")
        # Retorna cache antigo se existir, mesmo que expirado
        return _cache.get(user_id, (0, ""))[1]
```

## Integração em `gus/llm.py`

Adicionar função auxiliar e chamar no momento de montar o system prompt:

```python
from hub.auto_relato import gerar_auto_relato

async def montar_system_prompt(base: str, user_id: str = "gustavo") -> str:
    """System prompt base + auto-relato narrativo do Hub no boot."""
    try:
        relato = await gerar_auto_relato(user_id)
        if relato:
            return f"{base}\n\n---\n\n## Contexto atual\n{relato}"
    except Exception:
        pass
    return base
```

Chamar `montar_system_prompt(system_prompt_base)` no lugar onde o system prompt
é montado antes de cada chamada à API do Claude.

## Por que cache de 2h

O auto-relato não precisa ser recalculado a cada mensagem — o contexto muda
devagar. 2h equilibra frescor com custo:

- 12 atualizações/dia máximo
- ~300 tokens por geração × 12 × 30 dias = 108k tokens/mês → **~$0.03/mês**

Para forçar regeneração imediata: `GET /hub/auto-relato?forcar=true`

## Comportamento quando o Hub está vazio

Se o Hub ainda não tem fragmentos (recém-instalado), `ego_cache()` retorna
dicts vazios, `formatar_ego_cache()` retorna `""`, e `gerar_auto_relato()`
retorna `""` sem chamar Haiku. O system prompt base é usado sem modificação.
O sistema degrada graciosamente.
