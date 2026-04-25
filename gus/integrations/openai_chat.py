"""
Tool `perguntar_gpt` — consulta o GPT-5 da OpenAI pra second opinion.

Reusa `OPENAI_API_KEY` (a mesma usada pra Whisper em `gus/media.py`). Não
precisa key nova.

QUANDO USAR:
  - Decisões ambíguas onde vale segunda opinião de família de modelo
    diferente do Claude (vieses distintos).
  - NÃO usar pra busca/fato atual (use `search_web` ou Perplexity).
  - NÃO usar pra brainstorm (Sonnet sozinho basta).

CUSTO (mid-2025):
  - gpt-5-nano:  ~$0.05/M input + $0.40/M output  (default não — só pra coisas triviais)
  - gpt-5-mini:  ~$0.25/M input + $2.00/M output  (DEFAULT — bom equilíbrio)
  - gpt-5:       ~$10/M input + $30/M output      (caro — só decisões críticas)

Latência típica: 2-5s pra mini, 4-10s pra full.
"""

import logging
import os

import httpx

logger = logging.getLogger(__name__)

OPENAI_BASE = "https://api.openai.com/v1/chat/completions"
MODELOS_VALIDOS = {"gpt-5", "gpt-5-mini", "gpt-5-nano"}
MODELO_DEFAULT = "gpt-5-mini"


async def perguntar_gpt(
    query: str,
    modelo: str = MODELO_DEFAULT,
    system: str | None = None,
) -> str:
    """Pergunta ao GPT-5. Retorna resposta em texto puro ou mensagem de erro.

    Args:
        query: pergunta + contexto necessário (string única).
        modelo: 'gpt-5', 'gpt-5-mini' (default) ou 'gpt-5-nano'.
        system: system prompt opcional. Se None, usa um padrão curto
            explicando que é segunda opinião pro Gus.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "(OPENAI_API_KEY não configurada — perguntar_gpt indisponível)"

    if modelo not in MODELOS_VALIDOS:
        return f"Modelo '{modelo}' inválido. Use: {', '.join(sorted(MODELOS_VALIDOS))}."

    if not query or not query.strip():
        return "Query vazia — passe a pergunta."

    sys_default = (
        "Você é consultado pelo Gus (assistente pessoal do Gustavo, anestesiologista "
        "e pesquisador em IA) pra dar uma segunda opinião divergente de Claude Sonnet. "
        "Seja direto, em português, sem floreio. Aponte pontos cegos que Sonnet pode "
        "não ter visto. Se a pergunta for trivial, responda curto e diga isso."
    )

    payload = {
        "model": modelo,
        "messages": [
            {"role": "system", "content": system or sys_default},
            {"role": "user", "content": query.strip()},
        ],
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(OPENAI_BASE, headers=headers, json=payload)
    except httpx.TimeoutException:
        return f"GPT timeout (>60s) — modelo {modelo} não respondeu."
    except Exception as e:
        logger.error(f"OpenAI network error: {e}")
        return f"Erro de rede no OpenAI: {str(e)[:120]}"

    if r.status_code == 401:
        return "(OPENAI_API_KEY rejeitada pelo OpenAI — chave inválida ou expirada)"
    if r.status_code == 429:
        return "OpenAI rate limit (429). Tenta de novo em alguns segundos."
    if r.status_code >= 500:
        return f"OpenAI server error ({r.status_code}). Tenta de novo."
    if r.status_code != 200:
        body = (r.text or "")[:200]
        return f"OpenAI falhou (status {r.status_code}): {body}"

    try:
        data = r.json()
        texto = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, ValueError) as e:
        logger.error(f"OpenAI parse error: {e} — body: {(r.text or '')[:200]}")
        return f"OpenAI retornou resposta inválida: {str(e)[:120]}"

    usage = data.get("usage", {})
    in_tok = usage.get("prompt_tokens", 0)
    out_tok = usage.get("completion_tokens", 0)
    rodape = f"\n\n---\n*GPT-{modelo.split('-')[-1] if '-' in modelo else modelo} · {in_tok}→{out_tok} tokens*"

    return (texto or "").strip() + rodape
