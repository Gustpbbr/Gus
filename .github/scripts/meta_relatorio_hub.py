#!/usr/bin/env python3
"""
Meta-relatório recorrente do Hub Qdrant — visibilidade contínua de qualidade.

Item 1.8 do plano de saneamento (02/05/2026). Diferente da `auditoria_hub.py`
(que é diária e gera doc Markdown legível), este roda de forma mais analítica:

- Distribuição de assunto via top-shingles (sem LLM, determinístico)
- Cluster de duplicatas por similaridade Jaccard (revisar manualmente)
- Razão fragmentos com classificação completa (tipo+camada+area todos preenchidos)
  vs fragmentos default (poluição silenciosa via _resumir_e_salvar antigo,
  ou MCP salvar_memoria sem params até item 1.4)
- Distribuição por curador (haiku / gpt / haiku-migracao / outros)
- Distribuição por via (telegram-claude / claude-chat / claude-code / etc)
- Distribuição por prompt_version (item 1.2 — separação de gerações)

Output: `_indices/_meta-relatorio-hub.md` (sobrescreve a cada run).

Roda via cron diário OU dispatch manual quando precisar inspecionar.
Sem LLM — heurística pura.

Variáveis de ambiente:
  QDRANT_URL, QDRANT_API_KEY
"""

import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Adiciona repo root ao sys.path pra importar hub.store via _hub_compat
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _hub_compat import get_all_memorias

BRT = timezone(timedelta(hours=-3))
OUTPUT_PATH = "_indices/_meta-relatorio-hub.md"

# Threshold de similaridade pra agrupar duplicatas. Mais alto = só candidatos
# fortes; mais baixo = mais ruído. 0.6 é compromisso razoável.
JACCARD_DUPLICATA = float(os.environ.get("META_RELATORIO_JACCARD", "0.6"))

# Top-K de tokens / shingles a mostrar
TOP_K_TOKENS = 30
TOP_K_DUPLICATAS = 25


STOPWORDS_PT = {
    "de", "do", "da", "dos", "das", "e", "ou", "que", "com", "por", "para",
    "em", "no", "na", "nos", "nas", "um", "uma", "uns", "umas", "ser", "ter",
    "estar", "fazer", "tem", "sobre", "mais", "como", "seu", "sua", "seus",
    "suas", "ele", "ela", "eles", "elas", "nao", "sim", "muito", "esse",
    "essa", "isso", "este", "esta", "isto", "aquele", "aquela", "aquilo",
    "ja", "ainda", "tambem", "so", "apenas", "sempre", "nunca", "todo",
    "toda", "todos", "todas", "qualquer", "outro", "outra",
}
STOPWORDS_EN = {
    "the", "and", "or", "of", "a", "an", "to", "in", "is", "it", "for", "on",
    "with", "as", "by", "at", "that", "this", "be", "are", "was", "were",
    "user", "wants", "has", "have", "said", "says", "will", "should", "would",
}
STOPWORDS = STOPWORDS_PT | STOPWORDS_EN


def normalizar(texto: str) -> set[str]:
    if not texto:
        return set()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^a-z0-9\s]", " ", texto.lower())
    return {t for t in texto.split() if len(t) > 3 and t not in STOPWORDS}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def _bucket_camada(meta: dict) -> str:
    return (meta or {}).get("camada_temporal") or "(sem)"


def _classificacao_completa(payload: dict) -> bool:
    """Fragmento bem classificado tem tipo + camada_temporal + area todos preenchidos."""
    tipo = payload.get("tipo")
    camada = payload.get("camada_temporal")
    area = payload.get("area")
    if not tipo or tipo == "episodico":
        # 'episodico' é o default do hub.store quando ninguém classifica — sinal fraco
        return False
    if not camada or camada == "sessao":
        # 'sessao' é o default
        return False
    if not area:
        return False
    return True


def relatar_brain(user_id: str) -> dict:
    """Coleta stats analíticos de um brain."""
    print(f"\n=== Brain: {user_id} ===")
    mems = get_all_memorias(user_id=user_id, limit=10000)
    print(f"  Total: {len(mems)} fragmentos")

    if not mems:
        return {"user_id": user_id, "total": 0}

    # Para cada fragmento: payload completo (em compat layer vem em "metadata")
    enriched = []
    for m in mems:
        # _hub_compat preserva tipo/area/via/curador em metadata
        meta = m.get("metadata") or {}
        texto = m.get("memory") or ""
        enriched.append({
            "id": m.get("id"),
            "texto": texto,
            "tokens": normalizar(texto),
            "tipo": meta.get("tipo"),
            "camada": meta.get("camada_temporal") or meta.get("camada"),
            "area": meta.get("area"),
            "via": meta.get("via"),
            "curador": meta.get("curador"),
            "estado": meta.get("estado"),
            "prompt_version": meta.get("prompt_version"),
            "created_at": m.get("created_at"),
        })

    total = len(enriched)

    # Distribuições
    por_tipo = Counter(e["tipo"] or "(sem)" for e in enriched)
    por_camada = Counter(e["camada"] or "(sem)" for e in enriched)
    por_area = Counter(e["area"] or "(sem)" for e in enriched)
    por_via = Counter(e["via"] or "(sem)" for e in enriched)
    por_curador = Counter(e["curador"] or "(sem)" for e in enriched)
    por_estado = Counter(e["estado"] or "(sem)" for e in enriched)
    por_prompt_v = Counter(e["prompt_version"] or "(sem)" for e in enriched)

    # Razão classificação completa
    classificados = sum(1 for e in enriched if _classificacao_completa({
        "tipo": e["tipo"], "camada_temporal": e["camada"], "area": e["area"],
    }))
    pct_classif = round(100 * classificados / total, 1) if total else 0

    # Top tokens (sinal de assunto dominante)
    tokens_globais = Counter()
    for e in enriched:
        tokens_globais.update(e["tokens"])
    top_tokens = tokens_globais.most_common(TOP_K_TOKENS)

    # Duplicatas suspeitas (Jaccard cap O(N²) — aceitável em <500 frags;
    # acima disso, amostragem deveria entrar)
    duplicatas = []
    if total <= 500:
        for i in range(total):
            for j in range(i + 1, total):
                sim = jaccard(enriched[i]["tokens"], enriched[j]["tokens"])
                if sim >= JACCARD_DUPLICATA:
                    duplicatas.append({
                        "a_id": enriched[i]["id"],
                        "a_texto": enriched[i]["texto"][:140],
                        "b_id": enriched[j]["id"],
                        "b_texto": enriched[j]["texto"][:140],
                        "sim": round(sim, 2),
                    })
    duplicatas.sort(key=lambda d: d["sim"], reverse=True)

    return {
        "user_id": user_id,
        "total": total,
        "por_tipo": por_tipo,
        "por_camada": por_camada,
        "por_area": por_area,
        "por_via": por_via,
        "por_curador": por_curador,
        "por_estado": por_estado,
        "por_prompt_v": por_prompt_v,
        "classificados": classificados,
        "pct_classif": pct_classif,
        "top_tokens": top_tokens,
        "duplicatas": duplicatas[:TOP_K_DUPLICATAS],
        "duplicatas_total": len(duplicatas),
    }


def render_secao_brain(rel: dict) -> list[str]:
    """Renderiza uma seção Markdown pra um brain."""
    if rel.get("total", 0) == 0:
        return [
            f"### Brain `{rel['user_id']}`",
            "",
            "_Sem fragmentos._",
            "",
        ]

    linhas = [
        f"### Brain `{rel['user_id']}`",
        "",
        f"- **Total:** {rel['total']}",
        f"- **Classificação completa** (tipo≠episodico + camada≠sessao + area≠vazio): {rel['classificados']} ({rel['pct_classif']}%)",
        f"- **Duplicatas suspeitas** (Jaccard ≥ {JACCARD_DUPLICATA}): {rel['duplicatas_total']} pares",
        "",
        "**Distribuições:**",
        "",
    ]

    def render_dist(titulo: str, counter: Counter, top: int = 10):
        linhas.append(f"- **{titulo}:**")
        for k, n in counter.most_common(top):
            pct = round(100 * n / rel["total"], 1)
            linhas.append(f"  - `{k}`: {n} ({pct}%)")

    render_dist("Por tipo", rel["por_tipo"])
    render_dist("Por camada_temporal", rel["por_camada"])
    render_dist("Por area", rel["por_area"])
    render_dist("Por via", rel["por_via"])
    render_dist("Por curador", rel["por_curador"])
    render_dist("Por estado", rel["por_estado"])
    render_dist("Por prompt_version", rel["por_prompt_v"])

    linhas += ["", f"**Top {TOP_K_TOKENS} tokens (sinal de assunto):**", ""]
    for tok, n in rel["top_tokens"]:
        linhas.append(f"  - `{tok}`: {n}")

    if rel["duplicatas"]:
        linhas += ["", f"**Top {TOP_K_DUPLICATAS} duplicatas suspeitas:**", ""]
        for i, d in enumerate(rel["duplicatas"], 1):
            linhas.append(f"{i}. **sim={d['sim']}**")
            linhas.append(f"   - `{d['a_id']}`: {d['a_texto']}")
            linhas.append(f"   - `{d['b_id']}`: {d['b_texto']}")

    linhas.append("")
    return linhas


def main() -> None:
    if not os.environ.get("QDRANT_URL") or not os.environ.get("QDRANT_API_KEY"):
        print("QDRANT_URL/QDRANT_API_KEY ausentes. Pulado.")
        sys.exit(0)

    relatorios = [relatar_brain(uid) for uid in ("gustavo", "gus")]

    total_geral = sum(r.get("total", 0) for r in relatorios)
    duplicatas_total = sum(r.get("duplicatas_total", 0) for r in relatorios)
    classif_total = sum(r.get("classificados", 0) for r in relatorios)
    pct_classif_geral = round(100 * classif_total / total_geral, 1) if total_geral else 0

    linhas = [
        "---",
        "tipo: meta-relatorio",
        f"atualizado: {datetime.now(BRT).isoformat()}",
        f"hub_total_geral: {total_geral}",
        f"jaccard_duplicata: {JACCARD_DUPLICATA}",
        "---",
        "",
        "# Meta-relatório do Hub Qdrant",
        "",
        "Visibilidade analítica do estado de qualidade do Hub. Sem LLM — "
        "puramente heurístico.  Diferente de `_auditoria-hub.md` (mais "
        "narrativo), este relatório foca em **distribuições agregadas** + "
        "**duplicatas candidatas** + **razão de classificação completa**.",
        "",
        "Gerado por `.github/scripts/meta_relatorio_hub.py` (item 1.8 do plano "
        "de saneamento, 02/05/2026).",
        "",
        "## Resumo geral",
        "",
        f"- **Total Hub:** {total_geral}",
        f"- **Classificação completa:** {classif_total} ({pct_classif_geral}%)",
        f"- **Duplicatas suspeitas:** {duplicatas_total} pares (Jaccard ≥ {JACCARD_DUPLICATA})",
        "",
        "## Por brain",
        "",
    ]

    for rel in relatorios:
        linhas.extend(render_secao_brain(rel))

    linhas += [
        "## Como interpretar",
        "",
        "- **Classificação completa baixa (<50%)**: muitos fragmentos entraram "
        "via caminhos sem classificação (MCP salvar_memoria sem params até item "
        "1.4, ou _fallback_mem0 antes do item 1.6). Sinal de poluição.",
        "- **Duplicatas suspeitas alta**: curador re-extraiu mesmo fato em "
        "janelas diferentes; precisa de dedup (item 1.7 ou Fase 5.5).",
        "- **Por via concentrado**: porta dominante. Se `claude-chat` >> "
        "`telegram-claude`, sistema captura mais de Chat que do bot.",
        "- **Por prompt_version**: durante migrações de prompt (Fase 5.1), "
        "deve aparecer mistura. Após estabilização, ≥95% deve estar na versão atual.",
    ]

    Path(os.path.dirname(OUTPUT_PATH)).mkdir(parents=True, exist_ok=True)
    Path(OUTPUT_PATH).write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"\nEscrito: {OUTPUT_PATH}")
    print(f"Total geral: {total_geral} | classif: {pct_classif_geral}% | dupes: {duplicatas_total}")


if __name__ == "__main__":
    main()
