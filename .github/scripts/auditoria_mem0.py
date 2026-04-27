#!/usr/bin/env python3
"""
Auditoria do Mem0 — gera `_indices/_auditoria-mem0.md` com visão curada do estado
da memória do Gus. Base pra SELF-1 e pra perguntas diretas do bot.

Computa:
- Estatísticas gerais (total, mais velha, mais nova)
- Frescor em buckets (24h, 7d, 30d, >30d)
- Densidade por área via matching de keywords (determinístico, sem LLM)
- Duplicatas suspeitas via similaridade Jaccard sobre tokens normalizados
- Gaps — áreas com índice ativo em _indices/ mas sem memórias associadas

Roda via GitHub Actions diariamente (cron 6h BRT, após export Mem0 das 3h).
"""

import os
import re
import sys
import unicodedata
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Migrado em R2 (2026-04-27): lê do Hub Qdrant via _hub_compat (Mem0 aposentado).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _hub_compat import get_all_memorias

USER_ID = "gustavo"
BRT = timezone(timedelta(hours=-3))
OUTPUT_PATH = "_indices/_auditoria-mem0.md"
# Nota: este arquivo NÃO é meta-memória do Gus. É auditoria do armazém de
# memórias SOBRE O GUSTAVO (Mem0). Meta-memória (do próprio Gus) mora em
# gus/meta-memoria.md.
DIAS_JANELAS = [1, 7, 30]

# Mapeamento área → keywords. Determinístico, não perfeito — o propósito é
# estimativa, não classificação rigorosa. Atualizar aqui quando padrões novos
# aparecerem no uso real.
AREA_KEYWORDS = {
    "saude": [
        "saude", "saude", "tapazol", "hipertireoidismo", "hipotireoidismo", "tsh", "t4", "t3",
        "tireoide", "tireóide", "exame", "exames", "consulta", "medico", "medico",
        "médica", "medica", "endocrinologista", "endocrino", "remedio", "remedio",
        "remédio", "medicamento", "medicamentos", "dose", "dosagem", "pressão",
        "pressao", "glicose", "colesterol", "anemia", "diabetes",
    ],
    "financeiro": [
        "financeiro", "extrato", "pagamento", "pagar", "banco", "pix", "boleto",
        "conta", "saldo", "investimento", "renda", "gasto", "gastos", "fatura",
        "cartao", "cartão", "salário", "salario", "imposto", "receita",
    ],
    "projetos": [
        "phronesis", "phronesis-bench", "mge", "mgx", "ter", "axon", "gus",
        "benchmark", "projeto", "projetos", "deadline", "milestone",
    ],
    "dimagem": [
        "dimagem", "clinica", "clínica", "anestesia", "anestesista", "plantão",
        "plantao", "paciente", "pacientes", "hospital", "cirurgia",
    ],
    "receitas": [
        "receita", "receitas", "ingrediente", "ingredientes", "preparo",
        "cozinha", "cozinhar", "assar", "fritar", "temperatura",
    ],
    "construcao": [
        "casa", "paty", "alferes", "construcao", "construção", "planta",
        "banheiro", "sala", "quarto", "cozinha", "dimensões", "dimensoes",
        "metros", "cm", "basculante", "pia",
    ],
    "pessoal": [
        "familia", "família", "mae", "mãe", "pai", "irmão", "irmao", "esposa",
        "marido", "filho", "filha", "amigo", "amiga",
    ],
}

STOPWORDS = {
    "user", "assistant", "the", "and", "or", "of", "a", "an", "to", "in", "is", "it",
    "o", "a", "os", "as", "de", "do", "da", "dos", "das", "e", "ou", "que", "com",
    "por", "para", "em", "no", "na", "nos", "nas", "um", "uma", "uns", "umas",
    "ser", "ter", "estar", "fazer", "tem", "ser", "sobre", "mais", "como", "seu",
    "sua", "seus", "suas", "ele", "ela", "eles", "elas", "não", "nao", "sim",
    "wants", "has", "said", "says", "will",
}

JACCARD_MIN = float(os.environ.get("META_JACCARD_MIN", "0.5"))


def normalizar_texto(texto: str) -> set[str]:
    """Lowercase, remove acentos e pontuação, tokeniza, remove stopwords curtas."""
    if not texto:
        return set()
    # Remove acentos
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    # Lowercase + só letras/números
    texto = re.sub(r"[^a-z0-9\s]", " ", texto.lower())
    tokens = {t for t in texto.split() if len(t) > 2 and t not in STOPWORDS}
    return tokens


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def classificar_area(tokens: set[str]) -> list[str]:
    """Retorna lista de áreas cuja keyword bateu. Pode retornar múltiplas."""
    areas_hit = []
    for area, keywords in AREA_KEYWORDS.items():
        keywords_norm = set()
        for kw in keywords:
            keywords_norm.update(normalizar_texto(kw))
        if tokens & keywords_norm:
            areas_hit.append(area)
    return areas_hit or ["capturado"]


def indices_ativos() -> list[str]:
    """Lê nomes de índices em _indices/ (exceto README e 00-master)."""
    pasta = Path("_indices")
    if not pasta.exists():
        return []
    nomes = []
    for arq in pasta.glob("*.md"):
        nome = arq.stem
        if nome.startswith("_") or nome in ("README", "00-master"):
            continue
        nomes.append(nome)
    return sorted(nomes)


def bucket_frescor(dias_atras: float) -> str:
    for d in DIAS_JANELAS:
        if dias_atras <= d:
            return f"ultimos_{d}d"
    return "mais_de_30d"


def formatar_data(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return dt.astimezone(BRT).strftime("%Y-%m-%d")
    except Exception:
        return iso[:10] if iso else "(sem data)"


def main():
    if not os.environ.get("QDRANT_URL") or not os.environ.get("QDRANT_API_KEY"):
        print("QDRANT_URL/QDRANT_API_KEY ausentes. Auditoria pulada.")
        sys.exit(0)

    print("Carregando memórias do Hub Qdrant (gus_hub)...")
    memorias = get_all_memorias(user_id=USER_ID, limit=10000)
    total = len(memorias)
    print(f"Total de memórias: {total}")

    if not memorias:
        print("Sem memórias pra auditar. Escrevendo MD vazio.")
        conteudo = (
            "---\n"
            "tipo: meta-memoria\n"
            f"atualizado: {datetime.now(BRT).isoformat()}\n"
            "mem0_total: 0\n"
            "---\n\n"
            "# Auditoria do Mem0 (memórias sobre o Gustavo)\n\n"
            "Nenhuma memória no Mem0 ainda. Capture coisas via Telegram e o bot vai alimentando.\n\n"
            "*Nota: este arquivo é auditoria do Mem0 (memórias sobre o Gustavo). "
            "Para auto-conhecimento do Gus, ver `gus/meta-memoria.md`.*\n"
        )
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        Path(OUTPUT_PATH).write_text(conteudo, encoding="utf-8")
        sys.exit(0)

    # Normaliza e classifica
    agora_utc = datetime.now(timezone.utc)
    enriched = []
    por_area: dict[str, int] = {}

    for m in memorias:
        texto = (m.get("memory") or "").strip()
        if not texto:
            continue
        mid = m.get("id", "")
        created = m.get("created_at") or m.get("createdAt") or ""
        try:
            dt_criacao = datetime.fromisoformat(created.replace("Z", "+00:00"))
        except Exception:
            dt_criacao = agora_utc
        dias_atras = (agora_utc - dt_criacao).total_seconds() / 86400
        tokens = normalizar_texto(texto)
        areas = classificar_area(tokens)
        for a in areas:
            por_area[a] = por_area.get(a, 0) + 1
        enriched.append({
            "id": mid,
            "texto": texto,
            "tokens": tokens,
            "created": created,
            "dias_atras": dias_atras,
            "areas": areas,
        })

    # Stats de frescor
    frescor = {f"ultimos_{d}d": 0 for d in DIAS_JANELAS}
    frescor["mais_de_30d"] = 0
    for e in enriched:
        bucket = bucket_frescor(e["dias_atras"])
        frescor[bucket] = frescor.get(bucket, 0) + 1

    # Memória mais velha e mais nova
    ordenadas = sorted(enriched, key=lambda x: x["dias_atras"])
    mais_nova = ordenadas[0] if ordenadas else None
    mais_velha = ordenadas[-1] if ordenadas else None

    # Duplicatas suspeitas — pares com Jaccard >= JACCARD_MIN
    duplicatas = []
    for i in range(len(enriched)):
        for j in range(i + 1, len(enriched)):
            sim = jaccard(enriched[i]["tokens"], enriched[j]["tokens"])
            if sim >= JACCARD_MIN:
                duplicatas.append({
                    "a": enriched[i],
                    "b": enriched[j],
                    "sim": round(sim, 2),
                })
    duplicatas.sort(key=lambda d: d["sim"], reverse=True)

    # Gaps — índices sem memória
    indices = set(indices_ativos())
    areas_com_memoria = set(por_area.keys())
    gaps = sorted(indices - areas_com_memoria)

    # Monta MD
    linhas = [
        "---",
        "tipo: meta-memoria",
        f"atualizado: {datetime.now(BRT).isoformat()}",
        f"mem0_total: {total}",
        "---",
        "",
        "# Auditoria do Mem0 (memórias sobre o Gustavo)",
        "",
        "Análise automática e determinística do estado do armazém de memórias "
        "SOBRE O GUSTAVO (Mem0). Gerada diariamente via GitHub Action "
        "(`auditoria_mem0.py`). Sem LLM — heurística baseada em keywords e "
        "similaridade Jaccard.",
        "",
        "**Não confundir com meta-memória do Gus** (`gus/meta-memoria.md`), "
        "que é o auto-conhecimento do próprio Gus.",
        "",
        "## Estatísticas gerais",
        f"- **Total:** {total} memórias",
    ]

    if mais_velha:
        linhas.append(f"- **Mais antiga:** {formatar_data(mais_velha['created'])} — *\"{mais_velha['texto'][:80]}...\"*")
    if mais_nova:
        linhas.append(f"- **Mais recente:** {formatar_data(mais_nova['created'])} — *\"{mais_nova['texto'][:80]}...\"*")

    linhas += [
        "",
        "## Frescor",
    ]
    for bucket, count in frescor.items():
        label = {
            "ultimos_1d": "Últimas 24h",
            "ultimos_7d": "Últimos 7 dias",
            "ultimos_30d": "Últimos 30 dias",
            "mais_de_30d": "Mais de 30 dias",
        }.get(bucket, bucket)
        pct = round(100 * count / total, 1) if total else 0
        linhas.append(f"- **{label}:** {count} ({pct}%)")

    linhas += [
        "",
        "## Densidade por área",
        "Estimativa via keywords (uma memória pode contar em múltiplas áreas):",
        "",
    ]
    if por_area:
        for area, count in sorted(por_area.items(), key=lambda x: x[1], reverse=True):
            pct = round(100 * count / total, 1) if total else 0
            linhas.append(f"- **{area}:** {count} ({pct}%)")
    else:
        linhas.append("- (nenhuma área detectada)")

    linhas += [
        "",
        "## Duplicatas suspeitas",
        f"Pares com similaridade Jaccard ≥ {JACCARD_MIN}. Revisar manualmente — "
        "não são duplicatas garantidas, são candidatas.",
        "",
    ]
    if duplicatas:
        for dup in duplicatas[:15]:  # cap em 15 pra não encher
            linhas.append(f"### Similaridade {dup['sim']}")
            linhas.append(f"- **A** ({formatar_data(dup['a']['created'])}): *\"{dup['a']['texto'][:120]}...\"*")
            linhas.append(f"- **B** ({formatar_data(dup['b']['created'])}): *\"{dup['b']['texto'][:120]}...\"*")
            linhas.append("")
    else:
        linhas.append("- Nenhuma duplicata suspeita identificada.")
        linhas.append("")

    linhas += [
        "## Gaps (áreas com índice mas sem memória)",
        "",
    ]
    if gaps:
        for g in gaps:
            linhas.append(f"- **{g}** — índice existe, nenhuma memória classificada nesta área")
    else:
        linhas.append("- Nenhum gap detectado.")

    linhas += [
        "",
        "## Uso",
        "- Bot consulta este arquivo via tool `auditoria_mem0()` quando o Gustavo pergunta sobre o estado das suas próprias memórias no Mem0.",
        "- Não confundir com `meta_memoria()`, que retorna `gus/meta-memoria.md` (auto-conhecimento do Gus).",
        "- SELF-1 (reflexão quinzenal) usa este arquivo pra contextualizar Nosis e Thymos com o estado do armazém de memórias sobre o Gustavo.",
        "- Atualização automática — não editar manualmente.",
    ]

    conteudo = "\n".join(linhas) + "\n"
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    Path(OUTPUT_PATH).write_text(conteudo, encoding="utf-8")
    print(f"Escrito: {OUTPUT_PATH} ({len(conteudo)} chars)")


if __name__ == "__main__":
    main()
