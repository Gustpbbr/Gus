#!/usr/bin/env python3
"""
Gera `dialogos/_bootstrap/gus-estado-atual.md` lendo do Hub Qdrant.

Resolve o lag de 21h do Claude Chat (que antes só via snapshot das 03h
gerado pelo `export_mem0.py`). Cron a cada 15min mantém esse arquivo
fresco.

Conteúdo gerado:
  - Header com timestamp BRT
  - Ego cache (identidade, decisões recentes, meta-reflexões) via
    `hub.store.ego_cache(user_id="gustavo")`
  - Fragmentos das últimas 6h (filtro por `criado_em` em `listar`)
  - Resumo numérico (total no brain, frequência por tipo)

Tamanho-alvo: 500-1500 tokens. Nunca verbose — Claude Chat tem janela
de 200k mas o objetivo é entregar contexto digerível, não dump.

Idempotência:
  - Sempre escreve o arquivo. O workflow no GH Actions só commita
    se houve diff real (git diff --staged --quiet).

Pré-requisito: variáveis de ambiente QDRANT_URL e QDRANT_API_KEY.
"""

import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Adiciona repo root ao sys.path pra importar hub.store
_REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO_ROOT))

from hub.store import ego_cache, listar, contar  # noqa: E402

USER_ID = "gustavo"
BRT = timezone(timedelta(hours=-3))
JANELA_HORAS = 6
MAX_FRAGMENTOS_RECENTES = 20
OUTPUT_PATH = _REPO_ROOT / "dialogos" / "_bootstrap" / "gus-estado-atual.md"

# Tipos prioritários — ordenados por valor pro Claude Chat saber estado
TIPOS_PRIORITARIOS = [
    "decisao",
    "preferencia",
    "biografico",
    "episodico",
    "meta_reflexao",
    "fato",
    "projeto",
    "rotina",
]
TIPOS_EXCLUIR = ["lacuna"]  # pendências, não fatos


def _agora_brt_iso() -> str:
    return datetime.now(BRT).strftime("%Y-%m-%dT%H:%M:%S%z")


def _agora_brt_legivel() -> str:
    return datetime.now(BRT).strftime("%d/%m/%Y às %H:%M")


def _eh_recente(criado_em: str | None, horas: int = JANELA_HORAS) -> bool:
    """True se `criado_em` (ISO) é dentro das últimas N horas (BRT-aware)."""
    if not criado_em:
        return False
    try:
        # Aceita "2026-04-28T19:00:00-03:00" ou variações com Z
        dt = datetime.fromisoformat(criado_em.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=BRT)
        agora = datetime.now(BRT).astimezone(timezone.utc)
        return (agora - dt.astimezone(timezone.utc)) <= timedelta(hours=horas)
    except (ValueError, TypeError):
        return False


def _formatar_fragmento_curto(frag: dict) -> str:
    """Linha de 1 fragmento em formato '- [tipo/area] conteudo (via)'."""
    tipo = frag.get("tipo") or "?"
    area = frag.get("area") or "-"
    conteudo = (frag.get("conteudo") or "").strip()
    via = frag.get("via") or "?"
    # Trunca conteúdo longo pra manter densidade alta
    if len(conteudo) > 200:
        conteudo = conteudo[:197] + "..."
    return f"- [{tipo}/{area}] {conteudo} _(via {via})_"


def _bloco_ego_cache(ego: dict) -> list[str]:
    linhas = []

    identidade = ego.get("identidade", [])
    if identidade:
        linhas.append("## Ego cache — identidade operacional estável")
        linhas.append("")
        for frag in identidade[:8]:
            linhas.append(_formatar_fragmento_curto(frag))
        linhas.append("")

    protegidos = ego.get("protegidos", [])
    if protegidos:
        linhas.append("## Procedural protegido (estável)")
        linhas.append("")
        for frag in protegidos[:5]:
            linhas.append(_formatar_fragmento_curto(frag))
        linhas.append("")

    decisoes = ego.get("decisoes_recentes", [])
    if decisoes:
        linhas.append("## Decisões recentes")
        linhas.append("")
        for frag in decisoes[:5]:
            linhas.append(_formatar_fragmento_curto(frag))
        linhas.append("")

    meta = ego.get("meta_reflexoes", [])
    if meta:
        linhas.append("## Meta-reflexões ativas")
        linhas.append("")
        for frag in meta[:5]:
            linhas.append(_formatar_fragmento_curto(frag))
        linhas.append("")

    return linhas


def _bloco_recentes(frags: list[dict]) -> list[str]:
    """Fragmentos das últimas JANELA_HORAS, filtrados por tipo."""
    recentes = [
        f for f in frags
        if _eh_recente(f.get("criado_em"))
        and (f.get("tipo") in TIPOS_PRIORITARIOS or f.get("tipo") not in TIPOS_EXCLUIR)
    ]

    # Ordena por criado_em descendente (mais novo primeiro)
    recentes.sort(key=lambda f: f.get("criado_em") or "", reverse=True)
    recentes = recentes[:MAX_FRAGMENTOS_RECENTES]

    if not recentes:
        return [
            f"## Fragmentos das últimas {JANELA_HORAS}h",
            "",
            "_(nenhum fragmento novo nesta janela — sistema ocioso ou curador parado)_",
            "",
        ]

    linhas = [
        f"## Fragmentos das últimas {JANELA_HORAS}h ({len(recentes)} de {len(frags)} no brain)",
        "",
    ]
    for frag in recentes:
        linhas.append(_formatar_fragmento_curto(frag))
    linhas.append("")
    return linhas


def _bloco_resumo_numerico(total: int, frags: list[dict]) -> list[str]:
    """Distribuição por tipo — útil pra Claude Chat ter noção do balanço."""
    contagem = {}
    for f in frags:
        t = f.get("tipo") or "?"
        contagem[t] = contagem.get(t, 0) + 1

    linhas = [
        "## Resumo numérico",
        "",
        f"- **Total no brain `{USER_ID}`**: {total} fragmentos",
        f"- **Amostra carregada**: {len(frags)} mais recentes (limite do listar)",
        "",
        "### Distribuição por tipo (na amostra)",
        "",
    ]
    for tipo, n in sorted(contagem.items(), key=lambda kv: kv[1], reverse=True):
        linhas.append(f"- `{tipo}`: {n}")
    linhas.append("")
    return linhas


def gerar_conteudo() -> str:
    """Monta o markdown completo do estado atual."""
    cabecalho = [
        "---",
        "tipo: estado-atual-vivo",
        f"gerado_em: {_agora_brt_iso()}",
        f"fonte: hub-qdrant (gus_hub, user_id={USER_ID})",
        f"janela_recentes_horas: {JANELA_HORAS}",
        "atualizacao: cron 15min",
        "---",
        "",
        f"# Estado atual do Gus — {_agora_brt_legivel()} BRT",
        "",
        "> Documento gerado automaticamente a cada 15 minutos lendo o Hub",
        "> Qdrant. Substitui o snapshot estático das 03h pra Claude Chat ter",
        "> contexto fresco do que o sistema sabe agora. NÃO editar manualmente —",
        "> próxima execução do cron sobrescreve.",
        "",
        "**Como o Claude Chat usa este arquivo:** lê no boot do modo Gus pra",
        "complementar a identidade canônica em `gus-bootstrap.md` com o estado",
        "dinâmico. Sem este arquivo, Claude Chat opera com lag de 21h.",
        "",
    ]

    try:
        ego = ego_cache(USER_ID)
    except Exception as e:
        ego = {}
        ego_erro = str(e)[:200]
    else:
        ego_erro = None

    try:
        frags = listar(USER_ID, limit=50)
    except Exception as e:
        frags = []
        listar_erro = str(e)[:200]
    else:
        listar_erro = None

    try:
        total = contar(USER_ID)
    except Exception as e:
        total = -1
        contar_erro = str(e)[:200]
    else:
        contar_erro = None

    blocos = list(cabecalho)

    if ego_erro or listar_erro or contar_erro:
        blocos.append("## ⚠️ Erros ao consultar Hub")
        blocos.append("")
        if ego_erro:
            blocos.append(f"- `ego_cache`: {ego_erro}")
        if listar_erro:
            blocos.append(f"- `listar`: {listar_erro}")
        if contar_erro:
            blocos.append(f"- `contar`: {contar_erro}")
        blocos.append("")
        blocos.append("Conteúdo abaixo pode estar incompleto.")
        blocos.append("")

    blocos.extend(_bloco_ego_cache(ego))
    blocos.extend(_bloco_recentes(frags))
    blocos.extend(_bloco_resumo_numerico(total if total >= 0 else len(frags), frags))

    blocos.append("---")
    blocos.append("")
    blocos.append("_Última atualização automática. Próxima em ≤15min._")

    return "\n".join(blocos) + "\n"


def main() -> int:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    conteudo = gerar_conteudo()
    OUTPUT_PATH.write_text(conteudo, encoding="utf-8")
    print(f"Escrito: {OUTPUT_PATH} ({len(conteudo)} chars, ~{len(conteudo) // 4} tokens)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
