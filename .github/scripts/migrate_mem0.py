"""
Migra memórias do Mem0 Cloud para o self-hosted (Qdrant).
Roda UMA VEZ, localmente, antes do deploy da nova versão.

Uso:
    MEM0_API_KEY=... QDRANT_URL=... QDRANT_API_KEY=... \\
    ANTHROPIC_API_KEY=... python .github/scripts/migrate_mem0.py
"""

import os
from mem0 import MemoryClient, Memory


def get_source():
    return MemoryClient(api_key=os.environ["MEM0_API_KEY"])


def get_dest():
    return Memory.from_config({
        "vector_store": {
            "provider": "qdrant",
            "config": {
                "url": os.environ["QDRANT_URL"],
                "api_key": os.environ["QDRANT_API_KEY"],
                "collection_name": "gus",
            }
        },
        "llm": {
            "provider": "anthropic",
            "config": {
                "model": "claude-haiku-4-5-20251001",
                "api_key": os.environ["ANTHROPIC_API_KEY"],
            }
        },
        "embedder": {
            "provider": "huggingface",
            "config": {"model": "sentence-transformers/all-MiniLM-L6-v2"}
        }
    })


def migrar(user_id: str, source, dest):
    print(f"\n--- Migrando brain '{user_id}' ---")
    raw = source.get_all(user_id=user_id)
    memorias = raw.get("results", raw) if isinstance(raw, dict) else raw
    print(f"Encontradas: {len(memorias)}")

    ok = erros = 0
    for m in memorias:
        texto = m.get("memory", "")
        if not texto:
            continue
        try:
            dest.add(
                [{"role": "user", "content": texto}],
                user_id=user_id,
                metadata=m.get("metadata", {}),
            )
            ok += 1
            print(f"  ✓ [{ok}] {texto[:70]}")
        except Exception as e:
            erros += 1
            print(f"  ✗ ERRO: {e} | {texto[:40]}")

    print(f"Resultado '{user_id}': {ok} migradas, {erros} erros")
    return ok, erros


if __name__ == "__main__":
    source = get_source()
    dest = get_dest()
    ok_g, err_g = migrar("gustavo", source, dest)
    ok_u, err_u = migrar("gus", source, dest)
    print(f"\n=== TOTAL: {ok_g + ok_u} migradas, {err_g + err_u} erros ===")
