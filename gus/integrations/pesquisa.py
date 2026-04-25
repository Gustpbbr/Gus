"""
Tools de pesquisa científica — PubMed (NCBI) e arXiv.

Ambas APIs são GRÁTIS, sem autenticação. NCBI pede `tool=` e `email=` no
query string como cortesia (e dá rate limit melhor — 10 req/seg em vez
de 3 req/seg sem identificação).

USO:
  pesquisar_pubmed(query, max_n=10, since_year=None)
  pesquisar_arxiv(query, max_n=10, categoria=None)

CUSTO:
  $0 por chamada (não usa Anthropic). Útil pra contexto factual em
  pesquisa clínica (Dimagem) e em IA (Phronesis, MGE, TER, Axon).
"""

import logging
import re
from xml.etree import ElementTree as ET

import httpx

logger = logging.getLogger(__name__)

PUBMED_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
ARXIV_BASE = "http://export.arxiv.org/api/query"

# Identificação cortesia pro NCBI (rate limit melhor)
PUBMED_TOOL_NAME = "GusBot"
PUBMED_EMAIL = "gustavopratti@gmail.com"


async def pesquisar_pubmed(
    query: str,
    max_n: int = 10,
    since_year: int | None = None,
) -> str:
    """Busca PubMed via NCBI E-utilities. Pipeline: esearch (IDs) → esummary
    (metadados). Retorna lista markdown com título, autores, journal/ano,
    PMID e link DOI quando disponível.

    Args:
        query: termos de busca (linguagem natural ou MeSH terms).
        max_n: máximo de resultados (1 a 20). Default 10.
        since_year: só artigos publicados em ou depois desse ano.

    Returns:
        Texto formatado pro Telegram, ou mensagem de erro.
    """
    try:
        max_n = max(1, min(int(max_n), 20))
    except (TypeError, ValueError):
        max_n = 10

    term = query.strip()
    if since_year:
        try:
            term = f"{term} AND ({int(since_year)}:3000[pdat])"
        except (TypeError, ValueError):
            pass

    params_search = {
        "db": "pubmed",
        "term": term,
        "retmax": max_n,
        "tool": PUBMED_TOOL_NAME,
        "email": PUBMED_EMAIL,
        "retmode": "json",
        "sort": "relevance",
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r1 = await client.get(f"{PUBMED_BASE}/esearch.fcgi", params=params_search)
    except Exception as e:
        logger.error(f"PubMed esearch network error: {e}")
        return f"Erro de rede no PubMed: {str(e)[:120]}"

    if r1.status_code != 200:
        return f"PubMed esearch falhou (status {r1.status_code})."

    try:
        data = r1.json()
    except Exception:
        return "PubMed esearch retornou resposta inválida."

    ids = (data.get("esearchresult") or {}).get("idlist", []) or []
    if not ids:
        return f"PubMed: nenhum resultado pra '{query}'."

    params_summary = {
        "db": "pubmed",
        "id": ",".join(ids),
        "retmode": "json",
        "tool": PUBMED_TOOL_NAME,
        "email": PUBMED_EMAIL,
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r2 = await client.get(f"{PUBMED_BASE}/esummary.fcgi", params=params_summary)
    except Exception as e:
        return f"Erro de rede no esummary: {str(e)[:120]}"

    if r2.status_code != 200:
        return f"PubMed esummary falhou (status {r2.status_code})."

    summary = (r2.json().get("result") or {})

    linhas = [f"**PubMed**: {len(ids)} resultados pra `{query}`\n"]
    for pmid in ids:
        item = summary.get(pmid, {}) or {}
        title = (item.get("title") or "?").rstrip(".")
        authors = item.get("authors", []) or []
        nomes = [a.get("name", "") for a in authors if a.get("name")]
        authors_str = ", ".join(nomes[:3])
        if len(nomes) > 3:
            authors_str += " et al."

        journal = item.get("fulljournalname") or item.get("source", "?")
        pubdate = item.get("pubdate") or ""
        year = pubdate.split()[0] if pubdate else "?"

        doi = ""
        for aid in item.get("articleids", []) or []:
            if aid.get("idtype") == "doi":
                doi = aid.get("value", "")
                break

        link = f"https://doi.org/{doi}" if doi else f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

        linhas.append(
            f"- **{title}**\n"
            f"  {authors_str} · {journal} ({year})\n"
            f"  PMID:{pmid} · {link}"
        )

    return "\n\n".join(linhas)


async def pesquisar_arxiv(
    query: str,
    max_n: int = 10,
    categoria: str | None = None,
) -> str:
    """Busca arXiv via Atom feed. Retorna lista markdown com título, autores,
    ano, abstract truncado e link.

    Args:
        query: termos de busca (linguagem natural).
        max_n: máximo (1 a 20). Default 10.
        categoria: filtro arXiv. Úteis pra Gustavo: 'cs.AI', 'cs.CL',
            'cs.LG', 'cs.HC', 'q-bio.NC'.

    Returns:
        Texto formatado pro Telegram, ou mensagem de erro.
    """
    try:
        max_n = max(1, min(int(max_n), 20))
    except (TypeError, ValueError):
        max_n = 10

    # arXiv suporta sintaxe: cat:X AND all:"texto"
    search_query = f'all:"{query.strip()}"'
    if categoria:
        cat = categoria.strip()
        search_query = f"cat:{cat} AND ({search_query})"

    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": max_n,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(ARXIV_BASE, params=params)
    except Exception as e:
        logger.error(f"arXiv network error: {e}")
        return f"Erro de rede no arXiv: {str(e)[:120]}"

    if r.status_code != 200:
        return f"arXiv falhou (status {r.status_code})."

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    try:
        root = ET.fromstring(r.text)
    except ET.ParseError as e:
        return f"arXiv retornou XML inválido: {str(e)[:120]}"

    entries = root.findall("atom:entry", ns)
    if not entries:
        return f"arXiv: nenhum resultado pra '{query}'."

    linhas = [f"**arXiv**: {len(entries)} resultados pra `{query}`\n"]
    for entry in entries:
        title_el = entry.find("atom:title", ns)
        title = (title_el.text or "?").strip() if title_el is not None else "?"
        title = re.sub(r"\s+", " ", title)

        authors_el = entry.findall("atom:author/atom:name", ns)
        nomes = [a.text for a in authors_el if a is not None and a.text]
        authors_str = ", ".join(nomes[:3])
        if len(nomes) > 3:
            authors_str += " et al."

        pub_el = entry.find("atom:published", ns)
        published = (pub_el.text or "")[:10] if pub_el is not None else ""
        year = published[:4]

        id_el = entry.find("atom:id", ns)
        link = id_el.text if id_el is not None else ""

        sum_el = entry.find("atom:summary", ns)
        summary = (sum_el.text or "").strip() if sum_el is not None else ""
        summary = re.sub(r"\s+", " ", summary)
        if len(summary) > 250:
            summary = summary[:247] + "..."

        linhas.append(
            f"- **{title}**\n"
            f"  {authors_str} ({year})\n"
            f"  {link}\n"
            f"  *{summary}*"
        )

    return "\n\n".join(linhas)
