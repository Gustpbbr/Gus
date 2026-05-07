"""
Gerador de inventário auto das tools do TioGu.

Lê `gus/tools.py:TOOLS` (array Python estático) e escreve um MD com
nome + descrição de cada tool em `projetos/gus/_tools-inventario.md`.
Rodado pelo workflow `sync-docs.yml`.

Por que existe: drift declarado entre system_prompt.md ("22 tools"),
CLAUDE.md ("~21") e código (21 reais). Doc auto-gerado elimina o
desencontro pra leitores externos. O gus-11-tools-roadmap.md continua
sendo doc curado (status, sprint, decisões) — esse arquivo é só
inventário fiel pro que está rodando hoje.
"""

import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

# Importar TOOLS exige env vars fake (gus/llm.py instancia clients no top).
import os
os.environ.setdefault("ANTHROPIC_API_KEY", "fake")
os.environ.setdefault("OPENAI_API_KEY", "fake")
os.environ.setdefault("QDRANT_URL", "http://fake.local")
os.environ.setdefault("QDRANT_API_KEY", "fake")

from gus.tools import TOOLS  # noqa: E402

OUTPUT = ROOT / "projetos" / "gus" / "_tools-inventario.md"
BRT = timezone(timedelta(hours=-3))


def gerar() -> str:
    agora = datetime.now(BRT).strftime("%Y-%m-%d %H:%M BRT")
    linhas = [
        "---",
        "tipo: inventario-auto",
        "area: gus",
        f"atualizado: {agora}",
        "fonte: gus/tools.py:TOOLS (geração automática — não editar)",
        "---",
        "",
        "# Tools do TioGu — inventário auto-gerado",
        "",
        "> **NÃO EDITAR.** Este arquivo é regenerado pelo workflow",
        "> `sync-docs.yml` a partir de `gus/tools.py:TOOLS`. Pra mudar uma",
        "> descrição, edite o `description` no array de tools no código.",
        ">",
        "> Doc curado (status, decisões, sprint) está em",
        "> `projetos/gus/gus-11-tools-roadmap.md`.",
        "",
        f"**Total de tools ativas:** {len(TOOLS)}",
        "",
        "| # | Nome | Descrição |",
        "|---|---|---|",
    ]

    for idx, tool in enumerate(TOOLS, start=1):
        nome = tool.get("name", "?")
        desc = (tool.get("description") or "").strip()
        # Tabela markdown — escapa pipes e quebras de linha
        desc_esc = desc.replace("|", "\\|").replace("\n", " ")
        # Trunca pra primeira sentença (ou 200 chars), legível
        if "." in desc_esc:
            primeira = desc_esc.split(".")[0] + "."
            if len(primeira) < 200:
                desc_curta = primeira
            else:
                desc_curta = desc_esc[:200] + "…"
        else:
            desc_curta = desc_esc[:200] + ("…" if len(desc_esc) > 200 else "")
        linhas.append(f"| {idx} | `{nome}` | {desc_curta} |")

    linhas.extend([
        "",
        "## Schemas completos",
        "",
        "Schema de input de cada tool (parâmetros aceitos):",
        "",
    ])

    for tool in TOOLS:
        nome = tool.get("name", "?")
        schema = tool.get("input_schema", {})
        props = schema.get("properties", {}) or {}
        required = set(schema.get("required", []) or [])

        linhas.append(f"### `{nome}`")
        linhas.append("")
        if not props:
            linhas.append("_Sem parâmetros._")
            linhas.append("")
            continue

        linhas.append("| Parâmetro | Tipo | Obrigatório | Descrição |")
        linhas.append("|---|---|---|---|")
        for pname, pdef in props.items():
            ptype = pdef.get("type", "?")
            obrigatorio = "✓" if pname in required else "—"
            pdesc = (pdef.get("description") or "").strip()
            pdesc_esc = pdesc.replace("|", "\\|").replace("\n", " ")
            if len(pdesc_esc) > 150:
                pdesc_esc = pdesc_esc[:150] + "…"
            linhas.append(f"| `{pname}` | {ptype} | {obrigatorio} | {pdesc_esc} |")
        linhas.append("")

    linhas.append("---")
    linhas.append("")
    linhas.append(f"_Auto-gerado em {agora} por `.github/scripts/gerar_lista_tools.py`._")
    linhas.append("")

    return "\n".join(linhas)


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    novo = gerar()
    atual = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
    if novo == atual:
        print(f"OK — {OUTPUT.relative_to(ROOT)} já está atualizado.")
        return 0
    OUTPUT.write_text(novo, encoding="utf-8")
    print(f"OK — {OUTPUT.relative_to(ROOT)} regenerado ({len(TOOLS)} tools).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
