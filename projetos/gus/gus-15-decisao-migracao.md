---
tipo: decisao-arquitetural
data: 2026-04-26
status: decidido
area: infra-memoria
proximos: gus-17-setup-ambiente.md
---

# Decisão: migração do Mem0 Cloud para self-hosted + Qdrant

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
