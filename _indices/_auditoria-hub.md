---
tipo: meta-memoria
atualizado: 2026-05-04T08:10:22.131234-03:00
hub_total_geral: 8709
hub_total_gustavo: 4396
hub_total_gus: 4313
---

# Auditoria do Hub Qdrant

Análise automática e determinística do armazém de memórias do Gus (coleção `gus_hub`). Gerada diariamente via GitHub Action (`auditoria_hub.py`). Sem LLM — heurística baseada em keywords + similaridade Jaccard.

**Não confundir com meta-memória do Gus** (`gus/meta-memoria.md`), que é o auto-conhecimento do próprio Gus.

## Resumo multi-brain (item 1.5)
- **Brain `gustavo`** (memórias sobre o usuário): 4396 fragmentos
- **Brain `gus`** (auto-observações do agente): 4313 fragmentos
- **Total geral:** 8709

## Detalhe — brain `gustavo`

- **Total:** 4396 memórias
- **Mais antiga:** 2026-04-27 — *"1. Após merge e deploys recentes, o auto_diagnostico agora tem acesso ao Hub Qdr..."*
- **Mais recente:** 2026-05-04 — *"A manutenção do bot inclui a atualização periódica das dependências e a facilita..."*

## Frescor
- **Últimas 24h:** 2408 (54.8%)
- **Últimos 7 dias:** 1988 (45.2%)
- **Últimos 30 dias:** 0 (0.0%)
- **Mais de 30 dias:** 0 (0.0%)

## Densidade por área
Estimativa via keywords (uma memória pode contar em múltiplas áreas):

- **gus:** 2146 (48.8%)
- **projetos:** 2062 (46.9%)
- **pessoal:** 76 (1.7%)
- **saude:** 65 (1.5%)
- **capturado:** 23 (0.5%)
- **pesquisa:** 14 (0.3%)
- **dimagem:** 13 (0.3%)
- **financeiro:** 4 (0.1%)
- **receitas:** 2 (0.0%)

## Duplicatas suspeitas
Pares com similaridade Jaccard ≥ 0.5. Revisar manualmente — não são duplicatas garantidas, são candidatas.

### Similaridade 1.0
- **A** (2026-05-03): *"O Hub Qdrant é a memória central do sistema...."*
- **B** (2026-05-03): *"Hub Qdrant é a memória central do sistema...."*

### Similaridade 1.0
- **A** (2026-05-03): *"O Hub Qdrant é a memória central do sistema...."*
- **B** (2026-05-03): *"O Hub Qdrant é a memória central do sistema...."*

### Similaridade 1.0
- **A** (2026-05-03): *"O Hub Qdrant é a memória central do sistema...."*
- **B** (2026-05-03): *"O Hub Qdrant é a memória central do sistema...."*

### Similaridade 1.0
- **A** (2026-05-03): *"A coleta dual de modelos no curador (Haiku × GPT-4o-mini) terminará em 12/05/2026...."*
- **B** (2026-05-03): *"A coleta dual de modelos no curador (Haiku × GPT-4o-mini) terminará em 12/05/2026...."*

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

- Nenhum gap detectado.

## Detalhe — brain `gus` (auto-observações)

- **Total:** 4313
- **Últimas 24h:** 2383 (55.3%)
- **Últimos 7 dias:** 1930 (44.7%)
- **Últimos 30 dias:** 0 (0.0%)
- **Mais de 30 dias:** 0 (0.0%)

**Áreas (brain `gus`):**
- **projetos:** 2141 (49.6%)
- **gus:** 1966 (45.6%)
- **pessoal:** 82 (1.9%)
- **saude:** 71 (1.6%)
- **capturado:** 32 (0.7%)
- **dimagem:** 15 (0.3%)
- **financeiro:** 5 (0.1%)
- **pesquisa:** 1 (0.0%)
- **receitas:** 1 (0.0%)

## Uso
- Bot consulta este arquivo via tool `auditoria_hub()` quando o Gustavo pergunta sobre o estado das suas próprias memórias no Mem0.
- Não confundir com `meta_memoria()`, que retorna `gus/meta-memoria.md` (auto-conhecimento do Gus).
- SELF-1 (reflexão quinzenal) usa este arquivo pra contextualizar Nosis e Thymos com o estado do armazém de memórias sobre o Gustavo.
- Atualização automática — não editar manualmente.
