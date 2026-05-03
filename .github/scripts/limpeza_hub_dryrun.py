#!/usr/bin/env python3
"""
Limpeza ativa do Hub — DRYRUN. Gera lista de candidatos a delete pra Gustavo aprovar.

Item 1.7 do plano de saneamento (02/05/2026). Diagnóstico A1+A5+A6 mostrou
que ~70% do conteúdo do Hub atual é lixo (duplicatas semânticas + cross-brain
pollution + meta-conversa de bot). Antes de tocar no curador (Fase 5),
limpa Hub atual pra estabelecer baseline limpo.

Tipos de candidatos identificados:

1. **Duplicatas semânticas (Jaccard ≥ 0.7)** — fragmentos quase iguais.
   Mantém o mais antigo + maior `confianca`, marca os outros como
   candidatos a delete.

2. **Cross-brain pollution** — fragmentos no brain `gus` cujo conteúdo
   é claramente sobre o Gustavo (não auto-observação do agente).
   Detectado por padrão "Nasci em..." / "Gustavo é..." / etc.

3. **Meta-lixo de bot** — fragmentos cujo conteúdo é só meta-conversa
   sobre o sistema ("X demandas pendentes", "bot tem N tools",
   "auditoria identificou..."). Sem valor biográfico.

4. **Tipo+camada padrão sem area** — `tipo=episodico, camada=sessao,
   area=""` em todos os 3 campos = entrou via caminho sem classificação
   (MCP antigo, fallback antigo). Sinal forte de poluição.

Output: `_indices/_limpeza-hub-candidatos.md` com cada candidato:
- ID
- Brain (gustavo / gus)
- Razão proposta
- Texto do fragmento (até 200 chars)
- Severidade da recomendação (forte / médio / fraco)

Não deleta nada. Gustavo revisa o doc, edita pra remover candidatos que
quer manter, depois roda `limpeza_hub_aplicar.py`.

Variáveis de ambiente:
  QDRANT_URL, QDRANT_API_KEY
"""

import os
import re
import sys
import unicodedata
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _hub_compat import get_all_memorias

BRT = timezone(timedelta(hours=-3))
OUTPUT_PATH = "_indices/_limpeza-hub-candidatos.md"
JACCARD_DUP = float(os.environ.get("LIMPEZA_JACCARD", "0.7"))


# Padrões de meta-lixo de bot — frags cujo conteúdo só descreve o sistema
META_LIXO_PATTERNS = [
    r"\b\d+\s*(demandas?|pendênc|paradas?)\b.*\binbox-claude-code\b",
    r"\bbot\s+(do\s+)?telegram\b.*\b(possui|tem)\s+~?\d+\s+(tools|ferramentas)\b",
    r"\btiogu\b.*\b~?\d+\s+(tools|ferramentas)\b",
    r"\bauditoria\s+(do\s+)?chat\b.*\b(envolve|conclu|identif)",
    r"\bretro-?engine\b.*\b(no-op|anthropic_missing)\b",
    r"\blog\s+do\s+retro-engine\b",
    r"\bworkflows?\s+(disponíve|configurad|operacional)",
    r"\bjsons?\s+estruturad",
]

# Padrões de cross-brain pollution — fragmentos no brain `gus` que falam
# sobre o Gustavo (deveriam ser brain `gustavo`).
CROSS_BRAIN_PATTERNS = [
    r"\bnasci(do)?\s+em\b",        # 'Nasci em Vitória' (fato biográfico)
    r"^gustavo\s+(é|tem|gosta|prefere|mora|trabalha|faz|usa|nasceu)",
    r"\buser\s+(wants?|prefers?|likes|asserts?|requests?|clarified|instructs|says)\b",  # EN biographical
    r"\b(insurance|patient|exam|mri)\b",  # Dimagem clínico — não é auto-observação do agente
]


def normalizar(texto: str) -> set[str]:
    if not texto:
        return set()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^a-z0-9\s]", " ", texto.lower())
    return {t for t in texto.split() if len(t) > 3}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def _is_meta_lixo(texto: str) -> bool:
    if not texto:
        return False
    txt_low = texto.lower()
    return any(re.search(p, txt_low) for p in META_LIXO_PATTERNS)


def _is_cross_brain(texto: str, user_id: str) -> bool:
    """True se fragmento está no brain `gus` mas conteúdo é fato sobre Gustavo."""
    if user_id != "gus":
        return False
    if not texto:
        return False
    txt_low = texto.lower()
    return any(re.search(p, txt_low) for p in CROSS_BRAIN_PATTERNS)


def _is_unclassified(meta: dict) -> bool:
    """True se tipo + camada + area todos defaults (entrou sem classificação)."""
    tipo = (meta or {}).get("tipo")
    camada = (meta or {}).get("camada_temporal") or (meta or {}).get("camada")
    area = (meta or {}).get("area")
    return (tipo == "episodico" or not tipo) and \
           (camada == "sessao" or not camada) and \
           (not area)


def coletar_candidatos(brain_data: dict, user_id: str) -> list[dict]:
    """Para um brain, gera lista de candidatos com razão e severidade."""
    candidatos: list[dict] = []
    mems = brain_data.get("memorias", [])

    enriched = []
    for m in mems:
        meta = m.get("metadata") or {}
        texto = m.get("memory") or ""
        enriched.append({
            "id": m.get("id"),
            "texto": texto,
            "tokens": normalizar(texto),
            "meta": meta,
            "created_at": m.get("created_at") or "",
            "confianca": float(meta.get("confianca", 0.7)) if isinstance(meta, dict) else 0.7,
        })

    # 1) Meta-lixo (forte)
    for e in enriched:
        if _is_meta_lixo(e["texto"]):
            candidatos.append({
                "id": e["id"],
                "user_id": user_id,
                "texto": e["texto"][:200],
                "razao": "META-LIXO: fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico",
                "severidade": "forte",
            })

    # 2) Cross-brain pollution (forte)
    for e in enriched:
        if _is_cross_brain(e["texto"], user_id):
            candidatos.append({
                "id": e["id"],
                "user_id": user_id,
                "texto": e["texto"][:200],
                "razao": "CROSS-BRAIN: fragmento no brain `gus` mas conteúdo é fato sobre Gustavo (deveria estar em `gustavo`). Recomendado: deletar daqui — se valer recuperar, importa via Fase 5.6 (legacy-mem0-saas backup)",
                "severidade": "forte",
            })

    # 3) Unclassified (médio — pode ser conteúdo bom mas mal classificado)
    ids_ja_marcados = {c["id"] for c in candidatos}
    for e in enriched:
        if e["id"] in ids_ja_marcados:
            continue
        if _is_unclassified(e["meta"]):
            candidatos.append({
                "id": e["id"],
                "user_id": user_id,
                "texto": e["texto"][:200],
                "razao": "UNCLASSIFIED: tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente",
                "severidade": "medio",
            })

    # 4) Duplicatas semânticas (Jaccard ≥ JACCARD_DUP)
    # Agrupa por similaridade transitiva. Mantém o "melhor" (mais antigo + maior confiança)
    # e marca os outros.
    grupos: list[list[int]] = []
    visitado = [False] * len(enriched)
    for i in range(len(enriched)):
        if visitado[i]:
            continue
        grupo = [i]
        visitado[i] = True
        for j in range(i + 1, len(enriched)):
            if visitado[j]:
                continue
            sim = jaccard(enriched[i]["tokens"], enriched[j]["tokens"])
            if sim >= JACCARD_DUP:
                grupo.append(j)
                visitado[j] = True
        if len(grupo) > 1:
            grupos.append(grupo)

    ids_ja_marcados = {c["id"] for c in candidatos}
    for grupo in grupos:
        # Escolhe o mantido: mais antigo (proxy de "primeira ocorrência") +
        # maior confianca em desempate
        ordenado = sorted(
            grupo,
            key=lambda idx: (enriched[idx]["created_at"], -enriched[idx]["confianca"]),
        )
        manter_idx = ordenado[0]
        manter = enriched[manter_idx]
        for idx in ordenado[1:]:
            e = enriched[idx]
            if e["id"] in ids_ja_marcados:
                continue
            candidatos.append({
                "id": e["id"],
                "user_id": user_id,
                "texto": e["texto"][:200],
                "razao": (
                    f"DUPLICATA semântica do fragmento mais antigo "
                    f"`{manter['id']}` (Jaccard ≥ {JACCARD_DUP}). "
                    f"Manter '{manter['texto'][:80]}...'"
                ),
                "severidade": "forte",
            })

    return candidatos


def main() -> None:
    if not os.environ.get("QDRANT_URL") or not os.environ.get("QDRANT_API_KEY"):
        print("QDRANT_URL/QDRANT_API_KEY ausentes. Pulado.")
        sys.exit(0)

    candidatos_total: list[dict] = []
    for user_id in ("gustavo", "gus"):
        print(f"\n=== Brain: {user_id} ===")
        mems = get_all_memorias(user_id=user_id, limit=10000)
        print(f"  Total: {len(mems)}")
        candidatos = coletar_candidatos({"memorias": mems}, user_id)
        print(f"  Candidatos: {len(candidatos)}")
        candidatos_total.extend(candidatos)

    # Dedup candidatos (frag pode bater 2 razões — mantém só a 1ª)
    visto: set[str] = set()
    candidatos_unicos: list[dict] = []
    for c in candidatos_total:
        if c["id"] in visto:
            continue
        visto.add(c["id"])
        candidatos_unicos.append(c)

    # Renderiza MD
    agora = datetime.now(BRT)
    linhas = [
        "---",
        "tipo: limpeza-candidatos",
        f"gerado_em: {agora.isoformat()}",
        f"total_candidatos: {len(candidatos_unicos)}",
        f"jaccard_threshold: {JACCARD_DUP}",
        "---",
        "",
        "# Limpeza Hub — candidatos a delete",
        "",
        f"Gerado por `.github/scripts/limpeza_hub_dryrun.py` em "
        f"{agora.strftime('%d/%m/%Y às %H:%M BRT')}. **Nada foi deletado** — "
        f"este é o relatório dryrun pra Gustavo aprovar.",
        "",
        "## Como aprovar",
        "",
        "1. Revise cada candidato abaixo. Se um deve ser **mantido** (não "
        "deletar), copie o ID e adicione em "
        "`_indices/_limpeza-hub-rejeitados.txt` (um ID por linha).",
        "2. Se aprova **todos** os candidatos: deixe `_limpeza-hub-rejeitados.txt` vazio "
        "(ou inexistente).",
        "3. Rode `limpeza_hub_aplicar.py` (workflow `limpeza-hub-aplicar.yml`) — "
        "deleta todos os candidatos *exceto* os listados em rejeitados.",
        "",
        "Trilha de auditoria automática em `_log/deletar-hub/AAAA-MM-DD.jsonl` "
        "(item 1.3 do plano). Snapshot completo de cada delete pra recovery "
        "se precisar.",
        "",
        f"## Resumo",
        f"- **Total de candidatos:** {len(candidatos_unicos)}",
    ]

    # Estatísticas por severidade e razão-prefix
    by_sev: dict[str, int] = {}
    by_razao_prefix: dict[str, int] = {}
    by_brain: dict[str, int] = {}
    for c in candidatos_unicos:
        by_sev[c["severidade"]] = by_sev.get(c["severidade"], 0) + 1
        prefix = c["razao"].split(":")[0]
        by_razao_prefix[prefix] = by_razao_prefix.get(prefix, 0) + 1
        by_brain[c["user_id"]] = by_brain.get(c["user_id"], 0) + 1

    linhas.append(f"- **Por severidade:** " + ", ".join(f"{k}={v}" for k, v in sorted(by_sev.items())))
    linhas.append(f"- **Por razão:** " + ", ".join(f"{k}={v}" for k, v in sorted(by_razao_prefix.items())))
    linhas.append(f"- **Por brain:** " + ", ".join(f"{k}={v}" for k, v in sorted(by_brain.items())))
    linhas.append("")

    # Lista cada candidato agrupado por brain → severidade
    by_brain_sev: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for c in candidatos_unicos:
        by_brain_sev[(c["user_id"], c["severidade"])].append(c)

    for (brain, sev), grupo in sorted(by_brain_sev.items()):
        linhas.append(f"## Brain `{brain}` — severidade {sev} ({len(grupo)} candidatos)")
        linhas.append("")
        for c in grupo:
            linhas.append(f"### `{c['id']}`")
            linhas.append(f"- **Razão:** {c['razao']}")
            linhas.append(f"- **Texto:** {c['texto']}")
            linhas.append("")

    Path(os.path.dirname(OUTPUT_PATH)).mkdir(parents=True, exist_ok=True)
    Path(OUTPUT_PATH).write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"\nEscrito: {OUTPUT_PATH}")
    print(f"Total candidatos únicos: {len(candidatos_unicos)}")


if __name__ == "__main__":
    main()
