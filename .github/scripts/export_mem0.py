#!/usr/bin/env python3
"""
Exporta todas as memórias do Hub Qdrant (gus_hub) para arquivo .md no repositório.
Roda via GitHub Actions cron diário.
O arquivo é sincronizado pro Google Drive pelo workflow de sync.

Migrado em R2 (2026-04-27): antes lia do Mem0 SaaS, agora lê direto do Hub.
"""

import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Adiciona repo root ao sys.path pra importar hub.store via _hub_compat
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _hub_compat import get_all_memorias

USER_ID = "gustavo"
BRT = timezone(timedelta(hours=-3))
OUTPUT_PATH = "gus-memoria-export.md"
OUTPUT_JSON = "gus-memoria-export.json"


def main():
    if not os.environ.get("QDRANT_URL") or not os.environ.get("QDRANT_API_KEY"):
        print("QDRANT_URL/QDRANT_API_KEY ausentes — Hub indisponível.")
        sys.exit(1)

    memories = get_all_memorias(user_id=USER_ID, limit=10000)

    if not memories:
        print("Nenhuma memória encontrada.")
        sys.exit(0)

    now = datetime.now(BRT)
    lines = [
        "---",
        f"exportado_em: {now.strftime('%Y-%m-%dT%H:%M:%S')}",
        f"total: {len(memories)}",
        "fonte: hub-qdrant",
        "---",
        "",
        "# Memórias do Gustavo — Export Hub Qdrant",
        "",
        f"*Última atualização: {now.strftime('%d/%m/%Y às %H:%M')}*",
        "",
    ]

    for i, mem in enumerate(memories, 1):
        memory_text = mem.get("memory", "")
        created = mem.get("created_at", "")
        lines.append(f"{i}. {memory_text}")
        if created:
            lines.append(f"   *({created[:10]})*")
        lines.append("")

    content = "\n".join(lines)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    # Backup estruturado — preserva IDs, metadata e timestamps pra restore
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(memories, f, ensure_ascii=False, indent=2, default=str)

    print(f"Exportado: {len(memories)} memórias → {OUTPUT_PATH} + {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
