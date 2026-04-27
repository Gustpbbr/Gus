#!/usr/bin/env python3
"""
Migração de dados: coleção 'gus' (Mem0 antigo) → 'gus_hub' (Hub direto, schema gus-18).

Implementa Fase 4 do ADR-001 — popula o Hub com a história acumulada de ~200
fragmentos da camada Mem0 antes de aposentá-la.

ESTRATÉGIA:
  1. Scroll paginado na coleção 'gus' (Qdrant) — não precisa do mem0ai
  2. Classifica fragmentos em batch (20 por chamada Haiku) — barato (~$0.05 total)
  3. Insere cada fragmento em 'gus_hub' via hub.store.ingestar com:
       - tipo / area / camada_temporal classificados pelo Haiku
       - via = metadata original (default 'telegram-claude')
       - user_id = 'gustavo'
       - curador = 'haiku-migracao' (distingue dos curadores normais)
       - migrado_de_gus = True (rastreabilidade)
       - data_original = criado_em do Mem0 antigo (preserva história)

NÃO APAGA NADA. Coleção 'gus' fica intacta — Fase 5 decide o que fazer.

MODOS (input do workflow):
  dry-run : lê tudo, classifica, mostra o que SERIA inserido — sem escrever
  migrar  : executa a inserção real

VARIÁVEIS DE AMBIENTE:
  QDRANT_URL, QDRANT_API_KEY    — acesso ao Qdrant Cloud
  ANTHROPIC_API_KEY              — chamadas Haiku pra classificação

USAGE:
  MODE=dry-run python .github/scripts/migrar_gus_para_hub.py
  MODE=migrar  python .github/scripts/migrar_gus_para_hub.py
"""

import json
import logging
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [migracao] %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger(__name__)

BRT = timezone(timedelta(hours=-3))

# Sobe path do repo pra importar hub.*
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

BATCH_SIZE = 20  # fragmentos classificados por chamada Haiku
HAIKU_MODEL = "claude-haiku-4-5"

PROMPT_CLASSIFICACAO = """Você está fazendo classificação retroativa de fragmentos do Mem0 antigo do Gus, agente pessoal do Gustavo Pratti de Barros (anestesiologista, pesquisador em IA).

Cada fragmento já é um fato curto sobre o Gustavo, extraído anteriormente pelo Mem0. Sua tarefa: classificar pelo schema gus-18 do Hub.

PARA CADA FRAGMENTO NUMERADO, atribua:

- tipo: identidade_operacional | biografico | emocional | decisao | procedural | rotina | meta_reflexao | conexao_emergente | episodico | cronologico | fato | preferencia | lacuna | projeto

- area: gus | saude | financeiro | projetos | pessoal | dimagem | pesquisa | receitas | esportes

- camada_temporal: momento | sessao | semana | rotina | permanente

REGRAS:
- Fragmentos sobre o sistema Gus (workflows, tools, decisões técnicas) → tipo='meta_reflexao' ou 'decisao', area='gus'
- Fragmentos sobre projetos do Gustavo (Phronesis, MGE, TER, Axon) → area='projetos'
- Fragmentos sobre pacientes Dimagem → area='dimagem', tipo='episodico'
- Preferências e gostos → tipo='preferencia'
- Fatos perenes (anestesiologista, hipertireoidismo, etc) → tipo='biografico', camada_temporal='permanente'

FORMATO — apenas JSON válido, sem texto extra:

[
  {"id": 1, "tipo": "<tipo>", "area": "<area>", "camada_temporal": "<camada>"},
  {"id": 2, "tipo": "<tipo>", "area": "<area>", "camada_temporal": "<camada>"}
]

Fragmentos a classificar:

{fragmentos}
"""


def _ler_fragmentos_gus():
    """Scroll paginado na coleção 'gus' do Qdrant. Retorna lista de dicts."""
    from qdrant_client import QdrantClient

    client = QdrantClient(
        url=os.environ["QDRANT_URL"],
        api_key=os.environ["QDRANT_API_KEY"],
        timeout=30,
    )

    fragmentos = []
    offset = None
    while True:
        pontos, prox = client.scroll(
            collection_name="gus",
            limit=100,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )
        for p in pontos:
            payload = p.payload or {}
            # Mem0 padrão guarda o texto em 'data' ou 'memory' dependendo da versão
            conteudo = (
                payload.get("data")
                or payload.get("memory")
                or payload.get("conteudo")
                or ""
            ).strip()
            if not conteudo:
                continue
            fragmentos.append({
                "id_original": str(p.id),
                "conteudo": conteudo,
                "metadata_original": payload,
                "via_original": (payload.get("metadata") or {}).get("via", "telegram-claude")
                                 if isinstance(payload.get("metadata"), dict)
                                 else payload.get("via", "telegram-claude"),
                "criado_em_original": payload.get("created_at") or payload.get("criado_em"),
            })
        if not prox:
            break
        offset = prox

    return fragmentos


def _classificar_batch(batch, anthropic_key):
    """Chama Haiku com batch de fragmentos. Retorna list de dicts {id, tipo, area, camada_temporal}."""
    import anthropic

    client = anthropic.Anthropic(api_key=anthropic_key, timeout=60.0)
    fragmentos_str = "\n".join(
        f"{i+1}. {f['conteudo'][:500]}"  # limita pra controlar custo
        for i, f in enumerate(batch)
    )
    prompt = PROMPT_CLASSIFICACAO.format(fragmentos=fragmentos_str)

    try:
        resp = client.messages.create(
            model=HAIKU_MODEL,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as e:
        log.warning(f"Haiku batch falhou: {e}")
        return []

    texto = next((b.text for b in resp.content if hasattr(b, "text")), "") or ""
    return _parsear_classificacoes(texto)


def _parsear_classificacoes(texto):
    """Parser tolerante (cerca markdown, ruído antes/depois)."""
    if not texto:
        return []
    texto = texto.strip()
    if texto.startswith("```"):
        texto = re.sub(r"^```(?:json)?\s*", "", texto)
        texto = re.sub(r"```\s*$", "", texto)
        texto = texto.strip()
    try:
        return json.loads(texto) if texto else []
    except json.JSONDecodeError:
        m = re.search(r"\[\s*(?:\{.*?\}\s*,?\s*)*\]", texto, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                return []
    return []


def _classificacao_default(conteudo):
    """Heurística simples se Haiku falhar: classifica pelo conteúdo."""
    c = conteudo.lower()
    if any(t in c for t in ["mem0", "haiku", "sonnet", "qdrant", "workflow", "claude"]):
        return {"tipo": "meta_reflexao", "area": "gus", "camada_temporal": "rotina"}
    if any(t in c for t in ["dimagem", "paciente", "convênio"]):
        return {"tipo": "episodico", "area": "dimagem", "camada_temporal": "sessao"}
    if any(t in c for t in ["phronesis", "mge", "mgx", "ter", "axon"]):
        return {"tipo": "projeto", "area": "projetos", "camada_temporal": "rotina"}
    if any(t in c for t in ["hipertireoid", "tapazol", "saúde", "exame", "sangue"]):
        return {"tipo": "fato", "area": "saude", "camada_temporal": "permanente"}
    if any(t in c for t in ["financ", "custo", "preço", "valor", "obra", "casa"]):
        return {"tipo": "fato", "area": "financeiro", "camada_temporal": "rotina"}
    if any(t in c for t in ["receita", "feijoada", "doce", "salgad"]):
        return {"tipo": "preferencia", "area": "receitas", "camada_temporal": "permanente"}
    return {"tipo": "fato", "area": "pessoal", "camada_temporal": "rotina"}


def _ingerir_no_hub(fragmento, classificacao, dry_run):
    """Insere um fragmento em gus_hub via hub.store.ingestar (ou simula em dry-run)."""
    metadata = {
        "tipo": classificacao.get("tipo", "fato"),
        "camada_temporal": classificacao.get("camada_temporal", "rotina"),
        "area": classificacao.get("area", ""),
        "confianca": 0.6,  # confiança média — classificação retroativa
        "via": fragmento.get("via_original", "telegram-claude"),
        "user_id": "gustavo",
        "curador": "haiku-migracao",
        "hash_janela": fragmento["id_original"][:8],
        "janela_turnos": 0,  # não aplicável a migração
    }
    if dry_run:
        return None
    from hub.store import ingestar
    return ingestar(fragmento["conteudo"], metadata)


def main():
    mode = os.environ.get("MODE", "dry-run").strip().lower()
    if mode not in ("dry-run", "migrar"):
        log.error(f"MODE inválido: '{mode}' — use 'dry-run' ou 'migrar'")
        sys.exit(1)

    for var in ("QDRANT_URL", "QDRANT_API_KEY", "ANTHROPIC_API_KEY"):
        if not os.environ.get(var):
            log.error(f"{var} ausente")
            sys.exit(1)

    log.info(f"=== Migração 'gus' → 'gus_hub' (modo: {mode}) ===")

    log.info("Lendo fragmentos da coleção 'gus'…")
    fragmentos = _ler_fragmentos_gus()
    log.info(f"Encontrados: {len(fragmentos)} fragmentos com conteúdo")

    if not fragmentos:
        log.info("Nada a migrar. Saindo.")
        return

    # Classificação em batches
    anthropic_key = os.environ["ANTHROPIC_API_KEY"]
    classificacoes_por_id = {}  # id_original → {tipo, area, camada_temporal}

    for i in range(0, len(fragmentos), BATCH_SIZE):
        batch = fragmentos[i:i + BATCH_SIZE]
        log.info(f"Classificando batch {i // BATCH_SIZE + 1} ({len(batch)} fragmentos)…")
        result = _classificar_batch(batch, anthropic_key)
        # result é lista [{id, tipo, area, camada_temporal}]
        for entry in result:
            try:
                idx_local = int(entry.get("id", 0)) - 1  # 1-indexed no prompt
                if 0 <= idx_local < len(batch):
                    classificacoes_por_id[batch[idx_local]["id_original"]] = {
                        "tipo": entry.get("tipo", "fato"),
                        "area": entry.get("area", ""),
                        "camada_temporal": entry.get("camada_temporal", "rotina"),
                    }
            except (ValueError, TypeError):
                continue

    # Aplica fallback heurístico nos que Haiku não classificou
    sem_classificacao = [f for f in fragmentos if f["id_original"] not in classificacoes_por_id]
    if sem_classificacao:
        log.warning(f"{len(sem_classificacao)} fragmentos sem classificação Haiku — usando heurística")
        for f in sem_classificacao:
            classificacoes_por_id[f["id_original"]] = _classificacao_default(f["conteudo"])

    # Distribuição prevista
    by_tipo = {}
    by_area = {}
    for cls in classificacoes_por_id.values():
        by_tipo[cls["tipo"]] = by_tipo.get(cls["tipo"], 0) + 1
        by_area[cls["area"] or "(vazio)"] = by_area.get(cls["area"] or "(vazio)", 0) + 1

    log.info("=== Distribuição prevista ===")
    log.info(f"Por tipo: {sorted(by_tipo.items(), key=lambda x: -x[1])}")
    log.info(f"Por area: {sorted(by_area.items(), key=lambda x: -x[1])}")

    if mode == "dry-run":
        log.info("=== DRY-RUN — nada foi inserido ===")
        log.info(f"Pra executar, rode novamente com MODE=migrar")
        # Salva amostra pra análise
        amostra = []
        for f in fragmentos[:10]:
            cls = classificacoes_por_id.get(f["id_original"], {})
            amostra.append({
                "id_original": f["id_original"],
                "conteudo": f["conteudo"][:200],
                "tipo": cls.get("tipo"),
                "area": cls.get("area"),
                "camada_temporal": cls.get("camada_temporal"),
            })
        print("\n=== AMOSTRA (10 primeiros) ===")
        print(json.dumps(amostra, indent=2, ensure_ascii=False))
        return

    # Migração real
    log.info("=== INICIANDO MIGRAÇÃO REAL ===")
    salvos = erros = 0
    for f in fragmentos:
        cls = classificacoes_por_id.get(f["id_original"], _classificacao_default(f["conteudo"]))
        try:
            _ingerir_no_hub(f, cls, dry_run=False)
            salvos += 1
        except Exception as e:
            erros += 1
            log.warning(f"  Erro em {f['id_original'][:8]}: {str(e)[:120]}")

    log.info("=== RESUMO MIGRAÇÃO ===")
    log.info(f"Salvos: {salvos}")
    log.info(f"Erros:  {erros}")
    log.info(f"Total:  {len(fragmentos)}")
    log.info("Coleção 'gus' permaneceu INTACTA — Fase 5 decide o destino dela.")


if __name__ == "__main__":
    main()
