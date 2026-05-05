"""Busca web — Tavily primário, DuckDuckGo fallback."""

import os
import asyncio
import logging

import httpx
from duckduckgo_search import DDGS

logger = logging.getLogger(__name__)


async def _search_tavily(query: str) -> str | None:
    """Busca via Tavily API. Retorna string formatada ou None se falhar."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return None

    payload = {
        "api_key": api_key,
        "query": query,
        "max_results": 5,
        "search_depth": "basic",
    }
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post("https://api.tavily.com/search", json=payload)
        if response.status_code != 200:
            logger.warning(f"Tavily retornou {response.status_code}: {response.text[:200]}")
            return None
        results = response.json().get("results", [])
    except Exception as e:
        logger.warning(f"Tavily falhou: {e}")
        return None

    if not results:
        return None

    lines = [f"**{r['title']}**\n{r['content']}\nFonte: {r['url']}" for r in results]
    return "\n\n---\n\n".join(lines)


async def _search_ddg(query: str) -> str:
    """Fallback: busca via DuckDuckGo."""
    def _run():
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=5))

    try:
        results = await asyncio.to_thread(_run)
    except Exception as e:
        logger.error(f"Falha na busca web (DDG): {e}")
        return f"Erro na busca: {e}"

    if not results:
        return "Nenhum resultado encontrado."

    lines = [f"**{r['title']}**\n{r['body']}\nFonte: {r['href']}" for r in results]
    return "\n\n---\n\n".join(lines)


async def _search_web(query: str) -> str:
    """Tenta Tavily primeiro; se falhar ou sem chave, cai pro DuckDuckGo."""
    tavily_result = await _search_tavily(query)
    if tavily_result:
        return tavily_result
    return await _search_ddg(query)
