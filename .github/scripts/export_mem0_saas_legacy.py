#!/usr/bin/env python3
"""
Export defensivo do Mem0 SaaS (api.mem0.ai) — legacy, uso único.

Contexto: Fase 0 do plano de saneamento da memória (02/05/2026) descobriu
que a coleção Qdrant `gus` está vazia, mas docs antigos mencionavam ~204
fragmentos históricos. Hipótese: estavam no Mem0 SaaS (api.mem0.ai), não
no Qdrant Cloud self-hosted. Este script verifica.

Uso:
- Workflow `export-mem0-saas-legacy.yml` (manual dispatch only)
- Lista todos os fragmentos do brain `gustavo` E `gus` no Mem0 SaaS
- Salva em `historico/mem0-saas-export-final-AAAA-MM-DD.json`
- Não modifica nada no Mem0

Após rodar:
- Se 0 fragmentos: Mem0 SaaS está vazio, decisão "apagar MEM0_API_KEY" sem perda
- Se N>0: arquivo está no repo (`historico/`), Gustavo decide se vale recuperar
  algo ou só apagar o secret

Dependências:
  mem0ai==0.1.29  (instalado inline no workflow)

Variáveis de ambiente:
  MEM0_API_KEY — chave do Mem0 SaaS
"""

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

BRT = timezone(timedelta(hours=-3))


def main() -> None:
    api_key = os.environ.get("MEM0_API_KEY")
    if not api_key:
        print("MEM0_API_KEY ausente — caminho Mem0 SaaS já está fechado.")
        print("Isso é OK: significa que o secret já foi apagado ou nunca existiu.")
        print("Decisão Opção B (apagar sem export) aplicada de facto. Sem ação adicional necessária.")
        sys.exit(0)

    try:
        from mem0 import MemoryClient
    except ImportError as e:
        print(f"mem0ai não instalado: {e}")
        sys.exit(1)

    client = MemoryClient(api_key=api_key)

    resultado = {
        "exportado_em": datetime.now(BRT).isoformat(),
        "fonte": "mem0-saas (api.mem0.ai)",
        "brains": {},
    }

    total_geral = 0
    for user_id in ("gustavo", "gus"):
        try:
            mems = client.get_all(user_id=user_id)
            if isinstance(mems, dict):
                mems = mems.get("results", []) or []
            mems = mems or []
        except Exception as e:
            print(f"  [erro] brain={user_id}: {e}")
            resultado["brains"][user_id] = {"erro": str(e), "memorias": []}
            continue

        n = len(mems)
        total_geral += n
        print(f"  brain={user_id}: {n} fragmentos")
        resultado["brains"][user_id] = {"total": n, "memorias": mems}

    resultado["total"] = total_geral

    # Sempre escreve, mesmo com 0 — registro de auditoria do estado final
    hoje = datetime.now(BRT).strftime("%Y-%m-%d")
    out_dir = Path("historico")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"mem0-saas-export-final-{hoje}.json"
    out_path.write_text(
        json.dumps(resultado, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )

    print()
    print(f"Total exportado: {total_geral} fragmentos")
    print(f"Saída: {out_path}")
    if total_geral == 0:
        print("Mem0 SaaS está VAZIO. Pode apagar MEM0_API_KEY sem perda.")
    else:
        print(f"Mem0 SaaS tem {total_geral} fragmentos. Revisar o arquivo antes de apagar secret.")


if __name__ == "__main__":
    main()
