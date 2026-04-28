---
tipo: decisao-arquitetural
data: 2026-04-26
atualizado: 2026-04-27
status: superado-pelo-ADR-001
area: infra-memoria
---

# Lógica de convivência Qdrant × Mem0 (HISTÓRICO)

> **2026-04-27 — ATUALIZAÇÃO:** Esta lógica de **coexistência indefinida**
> foi superada pelo **ADR-001** (`projetos/gus/auditorias/2026-04-27/ADR-001-aposentadoria-mem0.md`).
> A decisão atual é **aposentar a coleção `gus`** (mem0 self-hosted) em
> favor de `gus_hub` (Hub direto). O conteúdo abaixo descreve o estado
> de transição (vigente em 26/04 → 27/04) — ler como histórico.
>
> **Estado atual:**
> - Bot Telegram lê do Hub primeiro (Fase 3 do ADR-001 — PR #7 mergeado 27/04)
> - Curador híbrido (Haiku × Sonnet) escreve no Hub a cada 3 turnos (Fase 2)
> - Coleção `gus` está **congelada** — só recebe escrita via fallback
>   raríssimo. Workflow `Migrar gus → gus_hub` faz a migração das ~204 mems
>   históricas
> - Fase 5 do ADR-001 (após 14 dias coleta dual): aposenta `gus` totalmente

---

Durante a transição (descontinuada após ADR-001), existiam duas coleções no mesmo Qdrant Cloud:

| Coleção | Gerenciada por | Propósito (histórico) |
|---|---|---|
| `gus` | mem0 self-hosted (Etapa 1) | Memórias extraídas automaticamente pelo mem0 |
| `gus_hub` | Hub direto (Etapa 2+) | Fragmentos com payload rico, ciclo de vida completo |

## Quando usar cada uma (histórico — antes do ADR-001)

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

- `gus` cresceu com cada interação até 26/04
- `gus_hub` começou vazio em 26/04 e cresceu com o Curador
- As duas coleções não sincronizam automaticamente — são independentes
- Bot usa `gus_hub` como fonte principal a partir de 27/04 (PR #7)

## Migração das duas coleções (executando agora)

Decidida em ADR-001:

1. ✅ Hub Qdrant maduro (Fase 1–2 prontas em 26/04)
2. ✅ Curador híbrido escrevendo no Hub (Fase 2)
3. ✅ Bot lê do Hub primeiro (Fase 3 — PR #7 mergeado 27/04)
4. ⏳ Workflow `Migrar gus → gus_hub` — disparar manualmente (modo `migrar`)
   pra mover ~204 mems históricas pra `gus_hub` com tipo `biografico/fato`
5. ⏳ Fase 5: aposentar `gus` (remover fallbacks no `gus/memory.py`,
   remover `MEM0_API_KEY` dos secrets, remover `mem0ai` do requirements)

## Rollback (histórico — não vale mais)

Os procedimentos de rollback abaixo eram válidos antes do ADR-001 (quando
a coexistência das duas coleções era indefinida). Após a aposentadoria
do Mem0 (Fase 5), o rollback envolve restaurar o `gus/memory.py` antigo
do git history. Não é estratégia recomendada.

### Rollback da Etapa 1 (descontinuado)

Se o mem0 self-hosted apresentasse problema após deploy:

1. Railway → Variables → renomear `QDRANT_URL` para `QDRANT_URL_BKP`
2. Reverter `gus/memory.py` para versão com `MemoryClient`
3. `MEM0_API_KEY` ainda está presente — bot voltaria a usar Mem0 Cloud
4. As memórias no Qdrant ficavam preservadas

### Rollback da Etapa 2 — Hub (descontinuado)

O Hub era aditivo até PR #7. Após PR #7 ele virou fonte principal:

1. Reverter `gus/memory.py:buscar_memorias` pra usar Mem0 client primeiro
2. Reverter `gus/bot.py:_resumir_e_salvar` pra usar `gerar_resumo_turnos`
   sem passar pelo curador híbrido
3. Coleção `gus_hub` permanece no Qdrant mas para de receber dados

## Custo consolidado (atualizado pós-ADR-001)

| Componente | Custo |
|---|---|
| Qdrant Cloud (`gus_hub` + `gus` em transição) | $0 (free tier) |
| Curador Haiku 4.5 + Sonnet 4.6 (paralelo, Fase 2) | ~$0.15/dia max → ~$4.5/mês durante coleta dual |
| Após Fase 5 (modelo único decidido) | ~$0.05–0.10/mês (só Haiku) ou ~$1-2/mês (só Sonnet) |
| Auto-relato Haiku (Etapa 5 do gus-original, ainda não implementado) | ~$0.03/mês |
| **Total incremental durante coleta dual (até 12/05)** | **~$4.5/mês** |
| **Total incremental pós-Fase 5** | **~$0.10–2/mês** |
