---
tipo: resumo-sessao-claude-code
data: 2026-04-27
duracao_aprox: ~6h (manhã + tarde + noite)
ambiente: Claude Code on the web
prs_abertos: 4 (#7, #8, #9, #10)
prs_mergeados: 4
demandas_resolvidas: 5/5 (inbox vazio ao fim)
---

# Sessão 27/04/2026 — Resumo executivo

> **TL;DR:** Migração Mem0 → Hub Qdrant fechada. Bot Telegram parou de
> reportar "Mem0 silêncio" e passou a salvar fragmentos via curador
> híbrido (Haiku × Sonnet em paralelo). 5 demandas do inbox resolvidas
> em sequência. 4 PRs sequenciais mergeados em produção.

## O que rolou

A sessão começou de manhã com **5 demandas pendentes** no inbox e
**4 itens da auditoria fiscal** (R2, R5, R6, R7). Acabou ao fim do
dia com **inbox vazio**, **auditoria fiscal 100% endereçada**, e
**3 bugs operacionais** descobertos e corrigidos no caminho:

1. Bug do **OCR Dimagem** — foto deitada gerava nome trocado em
   prontuário (risco clínico real)
2. Bug das **tools de busca do TioGu** — 3 funções não migradas pra
   Hub continuavam reportando "Mem0 silêncio 25h"
3. Bug do **curador 400 'temperature and top_p'** — fazia o Hub ficar
   vazio mesmo após migração

Cada bug virou commit dedicado, todos com defesa em profundidade
(múltiplas camadas de proteção, não um "patch e segue").

## PRs mergeados (em ordem)

| PR | Descrição | Bot Telegram afetado? |
|---|---|---|
| **#7** | Fase 4 (migração de dados) + Fase 3 (bot lê Hub) | ✅ Sim — bot passou a ler Hub |
| **#8** | R2/R6/R7 + #4 OCR + fix tools TioGu | ✅ Sim — auto_diagnostico melhorou, OCR seguro |
| **#9** | Fix curador 400 + memory.py Hub-first + bloco-âncora system_prompt | ✅ Sim — Hub começou a receber dados |
| **#10** | R5 documentação + cleanup R2 leftovers | ❌ Não — só documentação + renames |

## Demandas resolvidas (todas as 5)

| # | Demanda original | Como resolvida |
|---|---|---|
| 1 | `fix-qdrant-search-bug` | Já estava feita (sessão anterior), só faltava arquivar |
| 2 | `curadoria-mem0-sonnet-nao-haiku` | **Superada**: implementado curador **híbrido** (Haiku **e** Sonnet em paralelo, coleta dual de 14 dias pra decidir por evidência em vez de palpite) |
| 3 | `schema-hub-qdrant-salvar-memoria` | Resolvida: schema gus-18 completo (tipo / camada_temporal / area / confiança) implementado em todas as portas de entrada do Hub |
| 4 | `ocr-confianca-baixa-nao-salvar` | Implementada nesta sessão: gate de confiança no `analisar_os_dimagem` bloqueia preview se confiança baixa |
| 5 | `configurar-railway-api-token` | Gustavo configurou `Railway_diagnostic` no Railway → `logs_railway` ativo |

## Auditoria fiscal — itens endereçados

| Item | Descrição | Status |
|---|---|---|
| **R2** | 5 scripts cron migrados de Mem0 SaaS pra Hub Qdrant | ✅ |
| **R5** | Documentação atualizada pós-migração (CLAUDE.md, system_prompt, gus-15, gus-23, _estado-atual) | ✅ |
| **R6** | MCP Claude Code lendo direto do Hub (sem MemoryClient SaaS) | ✅ |
| **R7** | Patterns sensíveis em fonte única + 5 patterns novos | ✅ |

## Estado pós-sessão (validado pelo Gustavo no Telegram)

```
| Check | Status | Detalhe |
|---|---|---|
| GitHub Token | ✅ | auth OK (fine-grained PAT) |
| Hub Qdrant | ✅ | 2+ frags, mais recente há 0.0h (27/04 21:13 BRT) |
| Anthropic | ✅ | Haiku ok em 0.46s |
| Tavily | ✅ | search OK |
| Volume Railway | ✅ | /app/data writable |
| Workflows GH | ✅ | 5 runs recentes, todos OK |
```

**Tudo verde.** Curador finalmente salvando, Hub recebendo dados em
tempo real. Era a primeira vez que o `auto_diagnostico` mostrou Hub com
fragmentos desde a migração.

## Conquistas qualitativas

- **Inbox zero pela primeira vez** — passou de 5 demandas pendentes pra 0
- **3 bugs com risco real corrigidos** (OCR clínico, tools quebradas, curador morto)
- **Documentação reflete realidade** — CLAUDE.md e system_prompt vão guiar próximas sessões sem confusão sobre Mem0 vs Hub
- **Coleta dual rolando** — Haiku × Sonnet escrevendo em paralelo no mesmo trecho, decisão de modelo final em 12/05/2026 baseada em evidência

## Ver também

- `02-detalhes-tecnicos.md` — bugs em profundidade, mudanças de código por arquivo
- `03-pendencias-e-proximos-passos.md` — o que ficou pra próxima sessão
- `projetos/gus/_estado-atual.md` — handoff entre sessões (atualizado nesta)
- `projetos/gus/auditorias/2026-04-27/.../ADR-001-aposentadoria-mem0.md` — decisão arquitetural raiz

Relacionado: [[gus-15-decisao-migracao]], [[gus-23-logica-qdrant-mem0]], [[_estado-atual]]
