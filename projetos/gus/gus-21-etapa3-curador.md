---
tipo: guia-implementacao
data: 2026-04-26
status: pronto-para-implementar
area: infra-hub
anterior: gus-20-etapa2-hub-qdrant.md
proximo: gus-22-etapas4-5-ego-autorelato.md
---

# Etapa 3 — Curador Haiku integrado

Após cada interação no Telegram, o Curador analisa o transcript com Haiku e
extrai fragmentos atômicos para o Hub. Roda de forma assíncrona (fire-and-forget)
— não bloqueia a resposta ao Gustavo.

## Arquivos

- `hub/curador.py` — extração de fragmentos
- `gus/bot.py` — +3 linhas de integração

## `hub/curador.py`

```python
"""
Extrai fragmentos atômicos de uma interação e ingesta no Hub.
Chamado de forma assíncrona após cada resposta do bot — não bloqueia.
"""

import os
import json
import asyncio
import logging
import anthropic

from hub.store import ingestar

logger = logging.getLogger(__name__)

PROMPT_CURADOR = """Você é um curador de memória. Analise esta interação e extraia fragmentos de conhecimento atômicos sobre o Gustavo ou sobre o funcionamento do Gus.

Regras:
- Cada fragmento = uma informação isolada e auto-suficiente
- Ignore conteúdo efêmero (perguntas simples, confirmações, small talk)
- Extraia só o que tem valor duradouro
- Máximo 5 fragmentos por interação
- Se não houver nada relevante, retorne lista vazia

Para cada fragmento, classifique:
- tipo: identidade_operacional | biografico | decisao | procedural | preferencia | meta_reflexao | episodico | rotina
- camada_temporal: momento | sessao | semana | rotina | permanente
- area: gus | saude | financeiro | projetos | pessoal | dimagem | pesquisa
- confianca: 0.0 a 1.0 (quão certo você está do fragmento)

Retorne APENAS JSON válido, sem texto extra:
[
  {
    "conteudo": "texto do fragmento",
    "tipo": "tipo",
    "camada_temporal": "camada",
    "area": "area",
    "confianca": 0.8
  }
]

Interação a analisar:
{interacao}"""


async def curar(user_msg: str, assistant_msg: str, via: str = "telegram",
                user_id: str = "gustavo") -> int:
    """Extrai fragmentos da interação e salva no Hub. Retorna quantos salvou."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return 0

    interacao = f"Usuário: {user_msg}\n\nGus: {assistant_msg}"
    client = anthropic.AsyncAnthropic(api_key=api_key)

    try:
        resp = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": PROMPT_CURADOR.format(interacao=interacao)
            }]
        )
        texto = next((b.text for b in resp.content if hasattr(b, "text")), "[]")
        fragmentos = json.loads(texto)
    except Exception as e:
        logger.warning(f"Curador: erro na extração — {e}")
        return 0

    salvos = 0
    for f in fragmentos:
        conteudo = f.get("conteudo", "").strip()
        if not conteudo:
            continue
        try:
            await asyncio.to_thread(
                ingestar,
                conteudo,
                {
                    "tipo": f.get("tipo", "episodico"),
                    "camada_temporal": f.get("camada_temporal", "sessao"),
                    "area": f.get("area", ""),
                    "confianca": f.get("confianca", 0.7),
                    "via": via,
                    "user_id": user_id,
                }
            )
            salvos += 1
        except Exception as e:
            logger.warning(f"Curador: erro ao salvar fragmento — {e}")

    logger.info(f"Curador: {salvos} fragmento(s) salvos de interação via={via}")
    return salvos
```

## Integração em `gus/bot.py`

Localizar onde o bot envia a resposta ao Telegram (após `await message.reply(resposta)`
ou equivalente) e adicionar logo após:

```python
# Fire-and-forget — curadoria não bloqueia resposta
asyncio.create_task(_curar_interacao(user_text, resposta))
```

E definir a função auxiliar no arquivo:

```python
async def _curar_interacao(user_msg: str, assistant_msg: str):
    try:
        from hub.curador import curar
        await curar(user_msg, assistant_msg, via="telegram")
    except Exception:
        pass  # curadoria nunca quebra o bot
```

## Custo estimado

- Haiku: ~$0.25/1M tokens input, ~$1.25/1M tokens output
- Cada curadoria: ~500 tokens input + ~200 tokens output
- 10 interações/dia × 30 dias = 300 curadorias/mês
- Custo: ~300 × 0.7k tokens → **~$0.05/mês**

Negligível. O custo real é 0 a 3 fragmentos por interação, Haiku é barato.

## Observações

- Fragmentos com `confianca < 0.5` são salvos mas marcados como baixa confiança
- Haiku pode às vezes retornar JSON inválido — o `try/except` em torno do
  `json.loads` descarta silenciosamente
- Para debugar, ativar `DEBUG` no logger do módulo `hub.curador`
- O Curador não duplica o que o mem0 já faz — são coleções separadas (`gus` vs `gus_hub`)
