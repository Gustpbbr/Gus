---
tipo: meta-memoria
atualizado: 2026-05-03T07:11:40.322782-03:00
hub_total_geral: 3210
hub_total_gustavo: 1633
hub_total_gus: 1577
---

# Auditoria do Hub Qdrant

Análise automática e determinística do armazém de memórias do Gus (coleção `gus_hub`). Gerada diariamente via GitHub Action (`auditoria_hub.py`). Sem LLM — heurística baseada em keywords + similaridade Jaccard.

**Não confundir com meta-memória do Gus** (`gus/meta-memoria.md`), que é o auto-conhecimento do próprio Gus.

## Resumo multi-brain (item 1.5)
- **Brain `gustavo`** (memórias sobre o usuário): 1633 fragmentos
- **Brain `gus`** (auto-observações do agente): 1577 fragmentos
- **Total geral:** 3210

## Detalhe — brain `gustavo`

- **Total:** 1633 memórias
- **Mais antiga:** 2026-04-27 — *"1. Após merge e deploys recentes, o auto_diagnostico agora tem acesso ao Hub Qdr..."*
- **Mais recente:** 2026-05-03 — *"A coleta de fragmentos é realizada através de 3 produções simultâneas de entrada..."*

## Frescor
- **Últimas 24h:** 1614 (98.8%)
- **Últimos 7 dias:** 19 (1.2%)
- **Últimos 30 dias:** 0 (0.0%)
- **Mais de 30 dias:** 0 (0.0%)

## Densidade por área
Estimativa via keywords (uma memória pode contar em múltiplas áreas):

- **projetos:** 838 (51.3%)
- **gus:** 771 (47.2%)
- **saude:** 12 (0.7%)
- **capturado:** 7 (0.4%)
- **pessoal:** 6 (0.4%)
- **dimagem:** 5 (0.3%)
- **receitas:** 2 (0.1%)
- **pesquisa:** 1 (0.1%)

## Duplicatas suspeitas
Pares com similaridade Jaccard ≥ 0.5. Revisar manualmente — não são duplicatas garantidas, são candidatas.

### Similaridade 1.0
- **A** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*
- **B** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*

### Similaridade 1.0
- **A** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*
- **B** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*

### Similaridade 1.0
- **A** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*
- **B** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*

### Similaridade 1.0
- **A** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*
- **B** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*

### Similaridade 1.0
- **A** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*
- **B** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*

### Similaridade 1.0
- **A** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*
- **B** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*

### Similaridade 1.0
- **A** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*
- **B** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*

### Similaridade 1.0
- **A** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*
- **B** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*

### Similaridade 1.0
- **A** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*
- **B** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*

### Similaridade 1.0
- **A** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*
- **B** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*

### Similaridade 1.0
- **A** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*
- **B** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*

### Similaridade 1.0
- **A** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*
- **B** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*

### Similaridade 1.0
- **A** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*
- **B** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*

### Similaridade 1.0
- **A** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*
- **B** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*

### Similaridade 1.0
- **A** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*
- **B** (2026-05-03): *"Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`...."*

## Gaps (áreas com índice mas sem memória)

- **financeiro** — índice existe, nenhuma memória classificada nesta área

## Detalhe — brain `gus` (auto-observações)

- **Total:** 1577
- **Últimas 24h:** 1563 (99.1%)
- **Últimos 7 dias:** 14 (0.9%)
- **Últimos 30 dias:** 0 (0.0%)
- **Mais de 30 dias:** 0 (0.0%)

**Áreas (brain `gus`):**
- **projetos:** 940 (59.6%)
- **gus:** 596 (37.8%)
- **capturado:** 20 (1.3%)
- **pessoal:** 8 (0.5%)
- **saude:** 7 (0.4%)
- **dimagem:** 5 (0.3%)
- **pesquisa:** 1 (0.1%)
- **receitas:** 1 (0.1%)

## Uso
- Bot consulta este arquivo via tool `auditoria_hub()` quando o Gustavo pergunta sobre o estado das suas próprias memórias no Mem0.
- Não confundir com `meta_memoria()`, que retorna `gus/meta-memoria.md` (auto-conhecimento do Gus).
- SELF-1 (reflexão quinzenal) usa este arquivo pra contextualizar Nosis e Thymos com o estado do armazém de memórias sobre o Gustavo.
- Atualização automática — não editar manualmente.
