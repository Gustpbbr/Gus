---
tipo: decisao-arquitetural
data: 2026-04-26
atualizado: 2026-04-27
status: decidido (evoluído pelo ADR-001)
area: infra-memoria
proximos: gus-17-setup-ambiente.md
---

# Decisão: migração do Mem0 Cloud para self-hosted + Qdrant

> **2026-04-27 — EVOLUÇÃO:** Esta decisão (Mem0 SaaS → mem0 self-hosted +
> Qdrant Cloud) foi o **passo intermediário**. Após implementar e ver os
> trade-offs do wrapper mem0 self-hosted, o **ADR-001** (de 27/04) decidiu
> aposentar **também** o wrapper mem0 self-hosted em favor do Hub Qdrant
> direto (`hub/store.py`). Razão: o wrapper mem0 limita schema rico, o
> Hub direto permite payload completo gus-18 (tipo, camada_temporal, area,
> confiança, ciclo de vida, curador).
>
> Esta decisão (gus-15) é a **Etapa 1** da migração de memória.
> ADR-001 é a **Etapa 2** (mem0 self-hosted → Hub direto). Ambas estão
> em produção; Etapa 2 prevalece.
>
> Ver: `projetos/gus/auditorias/2026-04-27/.../ADR-001-aposentadoria-mem0.md`

## O problema

O Mem0 Cloud free tier permite 1.000 requests/mês. Em 3 dias de uso real foram
430 requests — projeção de ~4.300/mês, 4x o limite. O bot quebraria no meio do
mês todo mês.

Cada chamada a `client.search()` ou `client.add()` conta como request. Com o bot
respondendo várias mensagens por dia, o limite é insuficiente.

## Opções analisadas

| Opção | Custo | Complexidade | Controle |
|---|---|---|---|
| Mem0 Cloud pago | ~$20-50/mês | zero | nenhum |
| Self-hosted mem0 + Qdrant Cloud | ~$0-2/mês | baixa | total |
| Banco próprio do zero (SQLite) | $0 | alta | total |

## Decisão

**Self-hosted mem0 + Qdrant Cloud (free tier).**

- Qdrant Cloud free: 1 cluster, 4GiB disco, sem expiração — $0
- mem0 open source (`Memory` class) substitui `MemoryClient` com API idêntica
- Haiku faz extração (~$1-2/mês incremental, já estava implícito no Mem0 Cloud)
- Migração de código mínima: só troca a inicialização do client

## O que muda no código

Apenas `gus/memory.py`: `MemoryClient(api_key=...)` → `Memory.from_config(config)`
com Qdrant como vector store e Haiku como LLM de extração. Todas as funções
(`buscar_memorias`, `salvar_memorias`, etc.) ficam intactas.

## Caminho futuro

Self-hosted mem0 é o **passo 1**. Quando o Hub pre-AGI for construído (ver
`gus-24-hub-pre-agi-visao.md`), o Qdrant será usado diretamente — sem o wrapper
do mem0 — com payload rico e schema completo da Memória Viva. São dois projetos
sequenciais, não concorrentes.

## Trade-offs aceitos

- Startup mais lento no primeiro deploy (~30s): fastembed baixa modelo de embeddings
- Manutenção do Qdrant Cloud é nossa responsabilidade (mas free tier é estável)
- Mem0 Cloud tinha extração automática gerenciada; agora Haiku extrai localmente
