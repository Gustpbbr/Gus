---
tipo: guia-implementacao
data: 2026-04-26
status: pronto-para-implementar
area: infra-memoria
anterior: gus-17-setup-ambiente.md
proximo: gus-20-etapa2-hub-qdrant.md
---

# Etapa 1 — Mem0 self-hosted com Qdrant

Migração do `MemoryClient` (Mem0 Cloud) para `Memory` (self-hosted) com Qdrant
como vector store. API surface idêntica — zero mudança nas funções de negócio.

## Arquivos alterados

- `gus/memory.py` — troca client + normalização de resposta
- `requirements.txt` — adiciona `qdrant-client` e `fastembed`
- `.github/scripts/migrate_mem0.py` — script de migração (roda uma vez, local)

## `requirements.txt` — adicionar

```
qdrant-client
fastembed
```

## `gus/memory.py` — versão completa

```python
import os
import asyncio
import logging
from mem0 import Memory

logger = logging.getLogger(__name__)

USER_ID_GUSTAVO = "gustavo"
USER_ID_GUS = "gus"
USER_ID = USER_ID_GUSTAVO
VIA_DEFAULT = os.getenv("MEM0_VIA_TAG", "telegram-claude")

_client = None


def _get_client() -> Memory:
    global _client
    if _client is None:
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_key = os.getenv("QDRANT_API_KEY")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if not qdrant_url or not qdrant_key:
            raise ValueError("QDRANT_URL e QDRANT_API_KEY não definidos")
        _client = Memory.from_config({
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "url": qdrant_url,
                    "api_key": qdrant_key,
                    "collection_name": "gus",
                }
            },
            "llm": {
                "provider": "anthropic",
                "config": {
                    "model": "claude-haiku-4-5-20251001",
                    "api_key": anthropic_key,
                }
            },
            "embedder": {
                "provider": "fastembed",
                "config": {
                    "model": "BAAI/bge-small-en-v1.5"
                }
            }
        })
    return _client


def _normalizar_results(raw) -> list:
    """Memory.search() retorna dict {"results": [...]} no self-hosted."""
    if isinstance(raw, dict):
        return raw.get("results", [])
    return raw or []


async def buscar_memorias(query: str, user_id: str = USER_ID_GUSTAVO) -> str:
    client = _get_client()
    raw = await asyncio.to_thread(
        client.search, query, user_id=user_id, limit=5
    )
    results = _normalizar_results(raw)
    if not results:
        return ""
    lines = [f"- {r['memory']}" for r in results]
    return "\n".join(lines)


async def salvar_memorias(
    messages: list[dict],
    user_id: str = USER_ID_GUSTAVO,
    via: str | None = None,
) -> None:
    client = _get_client()
    metadata = {"via": via or VIA_DEFAULT}
    await asyncio.to_thread(
        client.add, messages, user_id=user_id, metadata=metadata
    )


async def buscar_memorias_detalhada(query: str, limit: int = 10, user_id: str = USER_ID_GUSTAVO) -> str:
    try:
        client = _get_client()
        raw = await asyncio.to_thread(
            client.search, query, user_id=user_id, limit=limit
        )
        results = _normalizar_results(raw)
    except Exception as e:
        return f"Erro ao buscar no Mem0 (user_id={user_id}): {e}"

    if not results:
        return f"Nenhuma memória encontrada pra `{query}` no brain `{user_id}`."

    linhas = [f"Encontradas {len(results)} memória(s) em `{user_id}` pra `{query}`:"]
    for i, r in enumerate(results, 1):
        mem = (r.get("memory") or "").strip()
        mem_id = r.get("id") or "?"
        if mem:
            linhas.append(f"{i}. [{mem_id}] {mem}")
    return "\n".join(linhas)


async def deletar_memoria(memory_id: str, user_id: str = USER_ID_GUSTAVO) -> str:
    if not memory_id or not memory_id.strip():
        return "memory_id vazio, não dá pra deletar."
    try:
        client = _get_client()
        await asyncio.to_thread(client.delete, memory_id=memory_id.strip())
        return f"Memória `{memory_id}` deletada do brain `{user_id}`."
    except Exception as e:
        return f"Erro ao deletar memória `{memory_id}`: {e}"


async def salvar_observacao_gus(observacao: str, via: str | None = None) -> str:
    if not observacao or not observacao.strip():
        return "Observação vazia, não salvei."
    try:
        await salvar_memorias(
            [{"role": "user", "content": observacao.strip()}],
            user_id=USER_ID_GUS,
            via=via,
        )
        return f"Observação salva no brain `gus`: \"{observacao[:80]}\""
    except Exception as e:
        return f"Erro ao salvar no Mem0 (user_id=gus): {e}"


async def buscar_memorias_gus(query: str, limit: int = 10) -> str:
    return await buscar_memorias_detalhada(query, limit=limit, user_id=USER_ID_GUS)
```

## `.github/scripts/migrate_mem0.py` — script de migração

```python
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
            "provider": "fastembed",
            "config": {"model": "BAAI/bge-small-en-v1.5"}
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
```

## Validação pós-deploy

1. Verificar log do Railway — sem erros de `QDRANT_URL` ou `MemoryClient`
2. Enviar mensagem no Telegram — bot responde normalmente
3. Perguntar algo que o Gus deveria lembrar — confirmar que busca retorna
4. No Qdrant Cloud dashboard → Collections → `gus` deve aparecer com pontos

## Rollback

Se algo quebrar: no Railway, renomear `QDRANT_URL` para `QDRANT_URL_BKP` e
reverter `gus/memory.py` para a versão com `MemoryClient`. O `MEM0_API_KEY`
ainda estará lá durante o período de transição.
