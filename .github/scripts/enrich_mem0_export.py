#!/usr/bin/env python3
"""
Enriquece o export do Mem0 com wikilinks para arquivos existentes no repo.

Lê gus-memoria-export.json, lista .md de conteúdo no vault, e para cada
memória chama Haiku (em batch) para propor wikilinks relevantes. Reescreve
gus-memoria-export.md com "Relacionado: [[x]], [[y]]" abaixo de cada item.

Objetivo: fazer o grafo implícito do Mem0 atravessar a ponte pro Obsidian —
o graph view passa a ver cada memória conectada aos arquivos de conteúdo.

Idempotente: rodar duas vezes produz o mesmo resultado (wikilinks não duplicam).
Custo estimado: ~$0.02 por run com 40-50 memórias e 60-100 arquivos.

Dependências: ANTHROPIC_API_KEY no env. `mem0` NÃO é necessário aqui — esse
script lê o JSON já exportado.
"""

import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

from anthropic import Anthropic

BRT = timezone(timedelta(hours=-3))

# Pastas de conteúdo real. Exclui _indices (metadados), projetos/gus (metadoc
# do sistema), sensivel (não deve cruzar com Mem0 export), dialogos-tiogu-claude
# (protocolo interno), agenda (pode entrar se quiser — avaliar).
PASTAS_CONTEUDO = [
    "pessoal", "dimagem", "projetos", "receitas", "esportes",
    "leituras", "capturado", "agenda", "gus",
]
EXCLUIR_PREFIXOS = (
    "projetos/gus/",                  # metadoc do próprio sistema
    "gus/meta-memoria",               # meta-reflexão, não conteúdo
    "dialogos/_bootstrap/",           # identidade + bootstrap (não memória)
)

BATCH_SIZE = 10
MODEL = "claude-haiku-4-5"
MAX_TOKENS_RESPOSTA = 2048

PROMPT_SISTEMA = """Você recebe:
1. Uma lista de arquivos .md existentes no vault pessoal do Gustavo (path + nome curto)
2. Um batch de memórias do Mem0 (agente pessoal dele)

Para cada memória, identifique quais arquivos ela realmente toca (máximo 3).

Critério rigoroso: só liste um arquivo se o tema da memória conecta de forma
substantiva ao tema do arquivo. Na dúvida, não liste. Silêncio é melhor que ruído.

Responda EXCLUSIVAMENTE em JSON estrito, sem markdown, sem prosa:
{
  "conexoes": [
    {"memoria_idx": 1, "wikilinks": ["historico-saude", "exame-sangue-abr-2026"]},
    {"memoria_idx": 2, "wikilinks": []}
  ]
}

Use o NOME do arquivo sem extensão e sem path (ex: "historico-saude", não
"pessoal/saude/historico-saude.md"). O memoria_idx é 1-based dentro do batch.
"""


def listar_mds_conteudo(repo_root: Path) -> list[tuple[str, str]]:
    """Retorna lista de (path_relativo, nome_sem_extensao) dos .md de conteúdo."""
    mds = []
    for pasta in PASTAS_CONTEUDO:
        base = repo_root / pasta
        if not base.exists():
            continue
        for md in base.rglob("*.md"):
            rel = md.relative_to(repo_root).as_posix()
            if any(rel.startswith(p) for p in EXCLUIR_PREFIXOS):
                continue
            mds.append((rel, md.stem))
    # Dedup por nome — se dois .md têm mesmo stem, wikilink fica ambíguo.
    # Mantém o primeiro; loga o conflito. (Obsidian resolve por proximidade.)
    visto = {}
    for path, stem in mds:
        visto.setdefault(stem, path)
    return [(visto[stem], stem) for stem in sorted(visto)]


def chamar_haiku_batch(
    client: Anthropic,
    mds: list[tuple[str, str]],
    batch: list[dict],
) -> list[dict]:
    """Chama Haiku com um batch de memórias. Retorna lista de conexões."""
    mds_fmt = "\n".join(f"- {path}  (nome: {stem})" for path, stem in mds)
    mems_fmt = "\n".join(
        f"{i + 1}. {m.get('memory', '').strip()}"
        for i, m in enumerate(batch)
    )
    user_msg = (
        f"## Arquivos disponíveis no vault ({len(mds)}):\n{mds_fmt}\n\n"
        f"## Memórias a analisar ({len(batch)}):\n{mems_fmt}\n\n"
        f"Retorne o JSON com conexões pra cada memória (memoria_idx 1 a {len(batch)})."
    )

    resposta = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS_RESPOSTA,
        system=PROMPT_SISTEMA,
        messages=[{"role": "user", "content": user_msg}],
    )
    texto = "".join(
        b.text for b in resposta.content if hasattr(b, "text")
    ).strip()

    # Haiku pode embrulhar em ```json ... ``` — extrai o primeiro objeto JSON
    match = re.search(r"\{[\s\S]*\}", texto)
    if not match:
        print(f"  [warn] Haiku não retornou JSON parseável: {texto[:200]}")
        return []
    try:
        data = json.loads(match.group())
    except json.JSONDecodeError as e:
        print(f"  [warn] JSON inválido: {e}. Texto: {texto[:200]}")
        return []
    return data.get("conexoes", [])


def gerar_md(memorias: list[dict], conexoes: dict[int, list[str]], timestamp: str) -> str:
    """Reconstrói o gus-memoria-export.md com wikilinks inline."""
    total = len(memorias)
    linhas = [
        "---",
        f"exportado_em: {timestamp}",
        f"total: {total}",
        "fonte: mem0",
        "enriquecido: true",
        "---",
        "",
        "# Memórias do Gustavo — Export Mem0 (enriquecido)",
        "",
        f"*Export original: {timestamp}. Wikilinks adicionados via Haiku.*",
        "",
    ]
    for i, mem in enumerate(memorias, 1):
        texto = (mem.get("memory") or "").strip()
        criado = (mem.get("created_at") or "")[:10]
        linhas.append(f"{i}. {texto}")
        if criado:
            linhas.append(f"   *({criado})*")
        wikilinks = conexoes.get(i, [])
        if wikilinks:
            links_str = ", ".join(f"[[{w}]]" for w in wikilinks)
            linhas.append(f"   Relacionado: {links_str}")
        linhas.append("")
    return "\n".join(linhas)


def preservar_timestamp_original(export_md: Path) -> str:
    """Lê o frontmatter do .md existente pra não dar aparência de novo export."""
    if not export_md.exists():
        return datetime.now(BRT).strftime("%Y-%m-%dT%H:%M:%S")
    cabecalho = export_md.read_text(encoding="utf-8")[:500]
    match = re.search(r"exportado_em:\s*([^\n]+)", cabecalho)
    if match:
        return match.group(1).strip()
    return datetime.now(BRT).strftime("%Y-%m-%dT%H:%M:%S")


def main() -> int:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY não definido.", file=sys.stderr)
        return 1

    repo_root = Path(__file__).resolve().parents[2]
    export_json = repo_root / "gus-memoria-export.json"
    export_md = repo_root / "gus-memoria-export.md"

    if not export_json.exists():
        print(
            f"gus-memoria-export.json não existe em {export_json}. "
            "Rode export_mem0.py antes.",
            file=sys.stderr,
        )
        return 1

    memorias = json.loads(export_json.read_text(encoding="utf-8"))
    if not memorias:
        print("Export vazio, nada a enriquecer.")
        return 0

    mds = listar_mds_conteudo(repo_root)
    if not mds:
        print("Nenhum .md de conteúdo encontrado nas pastas alvo.", file=sys.stderr)
        return 1

    print(f"Encontradas {len(memorias)} memórias e {len(mds)} arquivos de conteúdo.")

    client = Anthropic(api_key=api_key)
    nomes_validos = {stem for _, stem in mds}
    conexoes_por_idx: dict[int, list[str]] = {}

    for inicio in range(0, len(memorias), BATCH_SIZE):
        batch = memorias[inicio:inicio + BATCH_SIZE]
        print(
            f"Processando batch {inicio // BATCH_SIZE + 1} "
            f"(memórias {inicio + 1}-{inicio + len(batch)})..."
        )
        try:
            conexoes = chamar_haiku_batch(client, mds, batch)
        except Exception as e:
            print(f"  [erro] Haiku falhou nesse batch: {e}. Pulando.", file=sys.stderr)
            continue

        for c in conexoes:
            idx_local = c.get("memoria_idx", 0)
            if not (1 <= idx_local <= len(batch)):
                continue
            idx_global = inicio + idx_local
            wikilinks_propostos = c.get("wikilinks") or []
            # Filtro: só aceita wikilinks que mapeiam pra .md real
            validos = [w for w in wikilinks_propostos if w in nomes_validos]
            if validos:
                # Dedup preservando ordem
                conexoes_por_idx[idx_global] = list(dict.fromkeys(validos))

    timestamp = preservar_timestamp_original(export_md)
    novo_md = gerar_md(memorias, conexoes_por_idx, timestamp)
    export_md.write_text(novo_md, encoding="utf-8")

    enriquecidas = len(conexoes_por_idx)
    links_totais = sum(len(v) for v in conexoes_por_idx.values())
    print(
        f"\nEnriquecimento concluído: {enriquecidas}/{len(memorias)} memórias "
        f"ganharam wikilinks ({links_totais} links no total)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
