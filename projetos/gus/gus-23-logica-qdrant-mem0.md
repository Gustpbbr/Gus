---
tipo: decisao-arquitetural
data: 2026-04-26
status: vigente
area: infra-memoria
---

# Lógica de convivência Qdrant × Mem0

Durante a transição e a longo prazo, existem duas coleções no mesmo Qdrant Cloud:

| Coleção | Gerenciada por | Propósito |
|---|---|---|
| `gus` | mem0 self-hosted (Etapa 1) | Memórias extraídas automaticamente pelo mem0 |
| `gus_hub` | Hub direto (Etapa 2+) | Fragmentos com payload rico, ciclo de vida completo |

## Quando usar cada uma

**Coleção `gus` (via mem0):**
- Busca semântica rápida de fatos sobre o Gustavo
- Usado pelo bot Telegram para contexto de conversa
- Salvo automaticamente após cada interação
- Schema simples: `id`, `memory`, `metadata.via`

**Coleção `gus_hub` (via Hub direto):**
- Fragmentos tipados com ciclo de vida completo
- Ego Cache e Auto-relato
- Análises temporais, padrões, meta-reflexões
- Schema rico conforme `gus-18-schema-indexacao.md`

## Período de transição (Etapas 1 → 2)

Entre a Etapa 1 (mem0 self-hosted) e a Etapa 2 (Hub ativo com curador):

- `gus` cresce normalmente com cada interação
- `gus_hub` começa vazio e cresce com o Curador (Etapa 3) ativo
- As duas coleções não se sincronizam automaticamente — são independentes
- O bot usa `gus` para memória de conversa; Hub é camada adicional, não substituta

## Migração futura (longo prazo)

Quando o Hub estiver maduro (>500 fragmentos, curador calibrado), avaliar:

1. Migrar memórias da coleção `gus` para `gus_hub` com tipo `biografico/fato`
2. Bot passa a usar Hub como fonte principal
3. Coleção `gus` fica como legado e é descontinuada

Não é urgente. As duas coleções podem coexistir indefinidamente sem conflito.

## Rollback da Etapa 1

Se o mem0 self-hosted apresentar problema após deploy:

1. Railway → Variables → renomear `QDRANT_URL` para `QDRANT_URL_BKP`
2. Reverter `gus/memory.py` para versão com `MemoryClient`
3. `MEM0_API_KEY` ainda está presente — bot volta a usar Mem0 Cloud
4. As memórias no Qdrant ficam preservadas para quando for retomado

## Rollback da Etapa 2 (Hub)

O Hub é aditivo — não substitui nada na Etapa 2. Para desativar:

1. Remover `from hub.routes import hub_router` e `app.include_router(hub_router)` de `api/server.py`
2. Remover `asyncio.create_task(_curar_interacao(...))` de `gus/bot.py`
3. Coleção `gus_hub` permanece no Qdrant mas para de receber dados

## Custo consolidado

| Componente | Custo |
|---|---|
| Qdrant Cloud (ambas as coleções) | $0 (free tier) |
| mem0 extração (Haiku) | ~$1-2/mês |
| Curador Haiku (Etapa 3) | ~$0.05/mês |
| Auto-relato Haiku (Etapa 5) | ~$0.03/mês |
| **Total incremental** | **~$1-2/mês** |
