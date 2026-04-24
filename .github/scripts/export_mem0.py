#!/usr/bin/env python3
"""
Exporta todas as memórias do Mem0 para arquivo .md no repositório.
Roda via GitHub Actions cron diário.
O arquivo é sincronizado pro Google Drive pelo workflow de sync.
"""

import json
import os
import sys
from datetime import datetime, timezone, timedelta

from mem0 import MemoryClient

USER_ID = "gustavo"
BRT = timezone(timedelta(hours=-3))
OUTPUT_PATH = "gus-memoria-export.md"
OUTPUT_JSON = "gus-memoria-export.json"


def main():
    api_key = os.environ.get("MEM0_API_KEY")
    if not api_key:
        print("MEM0_API_KEY não definido.")
        sys.exit(1)

    client = MemoryClient(api_key=api_key)
    memories = client.get_all(user_id=USER_ID)

    if not memories:
        print("Nenhuma memória encontrada.")
        sys.exit(0)

    now = datetime.now(BRT)
    lines = [
        "---",
        f"exportado_em: {now.strftime('%Y-%m-%dT%H:%M:%S')}",
        f"total: {len(memories)}",
        "fonte: mem0",
        "---",
        "",
        "# Memórias do Gustavo — Export Mem0",
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
