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
- ID + brain + severidade + razão
- Texto COMPLETO (sem trunc)
- Metadata completa: tipo, camada_temporal, area, via, curador,
  prompt_version, confianca, criado_em, estado, hash_janela, janela_turnos
- Para duplicatas: também mostra texto+metadata do fragmento mantido

Não deleta nada. Gustavo revisa o doc, edita pra remover candidatos que
quer manter (cria `_limpeza-hub-rejeitados.txt`), depois roda
`limpeza_hub_aplicar.py`.

Lê payload completo do Qdrant via scroll (não usa `_hub_compat` porque
esse só preserva 5 campos no metadata).

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
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

BRT = timezone(timedelta(hours=-3))
OUTPUT_PATH = "_indices/_limpeza-hub-candidatos.md"
JACCARD_DUP = float(os.environ.get("LIMPEZA_JACCARD", "0.7"))


def listar_payload_completo(user_id: str, limit: int = 10000) -> list[dict]:
    """Scroll Qdrant direto pra pegar payload completo (todos os campos).

    `_hub_compat.get_all_memorias` só preserva 5 campos no metadata
    (tipo/estado/via/area/curador). Pra revisão humana precisamos de
    camada_temporal, prompt_version, confianca, criado_em, hash_janela, etc.
    """
    from qdrant_client import QdrantClient
    from qdrant_client.models import Filter, FieldCondition, MatchValue

    client = QdrantClient(
        url=os.environ["QDRANT_URL"],
        api_key=os.environ["QDRANT_API_KEY"],
        timeout=60,
    )
    flt = Filter(must=[FieldCondition(key="user_id", match=MatchValue(value=user_id))])

    todos: list[dict] = []
    offset = None
    while True:
        pontos, prox = client.scroll(
            collection_name="gus_hub",
            scroll_filter=flt,
            limit=200,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )
        for p in pontos:
            payload = dict(p.payload or {})
            payload["id"] = str(p.id)
            todos.append(payload)
        if not prox:
            break
        offset = prox

    return todos


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


def coletar_candidatos(payloads: list[dict], user_id: str) -> list[dict]:
    """Para um brain, gera lista de candidatos com razão e severidade.

    `payloads` é a lista vinda de `listar_payload_completo` — cada item
    é o payload completo do Qdrant + campo 'id' adicionado.
    """
    candidatos: list[dict] = []

    enriched = []
    for p in payloads:
        texto = p.get("conteudo") or ""
        try:
            confianca = float(p.get("confianca", 0.7))
        except (TypeError, ValueError):
            confianca = 0.7
        enriched.append({
            "id": p.get("id"),
            "texto": texto,
            "tokens": normalizar(texto),
            "meta": p,           # payload completo
            "created_at": p.get("criado_em") or "",
            "confianca": confianca,
        })

    # 1) Meta-lixo (forte)
    for e in enriched:
        if _is_meta_lixo(e["texto"]):
            candidatos.append({
                "id": e["id"],
                "user_id": user_id,
                "texto": e["texto"],
                "meta": e["meta"],
                "razao": "META-LIXO",
                "razao_long": "fragmento descreve o próprio sistema (demandas pendentes, contagem de tools, etc.) — sem valor biográfico",
                "severidade": "forte",
                "extras": {},
            })

    # 2) Cross-brain pollution (forte)
    for e in enriched:
        if _is_cross_brain(e["texto"], user_id):
            candidatos.append({
                "id": e["id"],
                "user_id": user_id,
                "texto": e["texto"],
                "meta": e["meta"],
                "razao": "CROSS-BRAIN",
                "razao_long": "fragmento no brain `gus` mas conteúdo é fato sobre Gustavo (deveria estar em `gustavo`). Recomendado: deletar daqui — se valer recuperar, importa via Fase 5.6 (legacy-mem0-saas backup)",
                "severidade": "forte",
                "extras": {},
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
                "texto": e["texto"],
                "meta": e["meta"],
                "razao": "UNCLASSIFIED",
                "razao_long": "tipo+camada+area todos defaults (entrou sem classificação — caminho não-curador). Considerar delete OU re-classificar manualmente",
                "severidade": "medio",
                "extras": {},
            })

    # 4) Duplicatas semânticas (Jaccard ≥ JACCARD_DUP)
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
                "texto": e["texto"],
                "meta": e["meta"],
                "razao": "DUPLICATA",
                "razao_long": (
                    f"Duplicata semântica (Jaccard ≥ {JACCARD_DUP}) do "
                    f"fragmento mais antigo `{manter['id']}`. Mantém este, "
                    f"deleta os outros do grupo."
                ),
                "severidade": "forte",
                "extras": {
                    "manter_id": manter["id"],
                    "manter_texto": manter["texto"],
                    "manter_meta": manter["meta"],
                },
            })

    return candidatos


def _render_payload(meta: dict) -> list[str]:
    """Renderiza linhas de metadata legíveis pra revisão humana."""
    campos = [
        ("tipo", meta.get("tipo")),
        ("camada_temporal", meta.get("camada_temporal") or meta.get("camada")),
        ("area", meta.get("area")),
        ("via", meta.get("via")),
        ("curador", meta.get("curador")),
        ("prompt_version", meta.get("prompt_version")),
        ("confianca", meta.get("confianca")),
        ("estado", meta.get("estado")),
        ("tipo_esquecimento", meta.get("tipo_esquecimento")),
        ("criado_em", meta.get("criado_em")),
        ("ultimo_acesso", meta.get("ultimo_acesso")),
        ("acessos", meta.get("acessos")),
        ("hash_janela", meta.get("hash_janela")),
        ("janela_turnos", meta.get("janela_turnos")),
    ]
    linhas = []
    for k, v in campos:
        if v is None or v == "":
            continue
        linhas.append(f"  - **{k}:** `{v}`")
    return linhas


def main() -> None:
    if not os.environ.get("QDRANT_URL") or not os.environ.get("QDRANT_API_KEY"):
        print("QDRANT_URL/QDRANT_API_KEY ausentes. Pulado.")
        sys.exit(0)

    candidatos_total: list[dict] = []
    totais_brain: dict[str, int] = {}
    for user_id in ("gustavo", "gus"):
        print(f"\n=== Brain: {user_id} ===")
        payloads = listar_payload_completo(user_id, limit=10000)
        print(f"  Total: {len(payloads)}")
        totais_brain[user_id] = len(payloads)
        candidatos = coletar_candidatos(payloads, user_id)
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
    total_hub = sum(totais_brain.values())
    linhas = [
        "---",
        "tipo: limpeza-candidatos",
        f"gerado_em: {agora.isoformat()}",
        f"total_hub: {total_hub}",
        f"total_brain_gustavo: {totais_brain.get('gustavo', 0)}",
        f"total_brain_gus: {totais_brain.get('gus', 0)}",
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
        "1. Revise cada candidato abaixo (texto completo + metadata). Se um "
        "deve ser **mantido**, copie o ID e adicione em "
        "`_indices/_limpeza-hub-rejeitados.txt` (um ID por linha).",
        "2. Se aprova **todos**: não cria o arquivo de rejeitados (ou deixa vazio).",
        "3. Rode `limpeza-hub-aplicar.yml` workflow — deleta todos exceto rejeitados.",
        "",
        "Trilha de auditoria automática em `_log/deletar-hub/AAAA-MM-DD.jsonl` "
        "(snapshot completo de cada delete pra recovery se precisar).",
        "",
        f"## Resumo",
        f"- **Hub total:** {total_hub} fragmentos",
        f"  - brain `gustavo`: {totais_brain.get('gustavo', 0)}",
        f"  - brain `gus`: {totais_brain.get('gus', 0)}",
        f"- **Candidatos a delete:** {len(candidatos_unicos)} ({round(100*len(candidatos_unicos)/total_hub, 1) if total_hub else 0}%)",
    ]

    # Estatísticas
    by_sev: dict[str, int] = {}
    by_razao: dict[str, int] = {}
    by_brain: dict[str, int] = {}
    for c in candidatos_unicos:
        by_sev[c["severidade"]] = by_sev.get(c["severidade"], 0) + 1
        by_razao[c["razao"]] = by_razao.get(c["razao"], 0) + 1
        by_brain[c["user_id"]] = by_brain.get(c["user_id"], 0) + 1

    linhas.append(f"- **Por severidade:** " + ", ".join(f"{k}={v}" for k, v in sorted(by_sev.items())))
    linhas.append(f"- **Por razão:** " + ", ".join(f"{k}={v}" for k, v in sorted(by_razao.items())))
    linhas.append(f"- **Por brain:** " + ", ".join(f"{k}={v}" for k, v in sorted(by_brain.items())))
    linhas.append("")

    # Lista cada candidato agrupado por brain → severidade → razão
    # Ordenação interna: por created_at (mais antigos primeiro) pra revisão temporal
    by_grupo: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for c in candidatos_unicos:
        by_grupo[(c["user_id"], c["severidade"], c["razao"])].append(c)

    for (brain, sev, razao_curta), grupo in sorted(by_grupo.items()):
        # Ordena cronologicamente
        grupo.sort(key=lambda c: (c["meta"] or {}).get("criado_em", "") or "")
        linhas.append(f"## Brain `{brain}` — {sev} — {razao_curta} ({len(grupo)} candidatos)")
        linhas.append("")
        # Razão detalhada uma vez por grupo
        razao_detalhe = grupo[0].get("razao_long", "")
        if razao_detalhe:
            linhas.append(f"_{razao_detalhe}_")
            linhas.append("")

        for c in grupo:
            linhas.append(f"### `{c['id']}`")
            linhas.append("")
            linhas.append("**Texto:**")
            linhas.append("")
            linhas.append("```")
            linhas.append(c["texto"])
            linhas.append("```")
            linhas.append("")
            linhas.append("**Metadata:**")
            payload_lines = _render_payload(c.get("meta") or {})
            if payload_lines:
                linhas.extend(payload_lines)
            else:
                linhas.append("  - _(sem metadata)_")
            # Pra duplicatas, mostra o fragmento mantido
            extras = c.get("extras") or {}
            if extras.get("manter_id"):
                linhas.append("")
                linhas.append(f"**Mantém este (mais antigo do grupo):** `{extras['manter_id']}`")
                linhas.append("")
                linhas.append("```")
                linhas.append(extras.get("manter_texto", ""))
                linhas.append("```")
                linhas.append("")
                linhas.append("Metadata do mantido:")
                manter_payload = _render_payload(extras.get("manter_meta") or {})
                linhas.extend(manter_payload or ["  - _(sem metadata)_"])
            linhas.append("")

    Path(os.path.dirname(OUTPUT_PATH)).mkdir(parents=True, exist_ok=True)
    Path(OUTPUT_PATH).write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"\nEscrito: {OUTPUT_PATH}")
    print(f"Total candidatos únicos: {len(candidatos_unicos)}")


if __name__ == "__main__":
    main()
