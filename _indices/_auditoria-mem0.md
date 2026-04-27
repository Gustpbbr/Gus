---
tipo: meta-memoria
atualizado: 2026-04-27T07:51:42.248694-03:00
mem0_total: 204
---

# Auditoria do Mem0 (memórias sobre o Gustavo)

Análise automática e determinística do estado do armazém de memórias SOBRE O GUSTAVO (Mem0). Gerada diariamente via GitHub Action (`auditoria_mem0.py`). Sem LLM — heurística baseada em keywords e similaridade Jaccard.

**Não confundir com meta-memória do Gus** (`gus/meta-memoria.md`), que é o auto-conhecimento do próprio Gus.

## Estatísticas gerais
- **Total:** 204 memórias
- **Mais antiga:** 2026-04-11 — *"User wants to edit, sign, and share PDF files from any location and is directed ..."*
- **Mais recente:** 2026-04-26 — *"Gustavo values autonomy and permanence of Gus's memories, viewing the self‑hoste..."*

## Frescor
- **Últimas 24h:** 24 (11.8%)
- **Últimos 7 dias:** 172 (84.3%)
- **Últimos 30 dias:** 8 (3.9%)
- **Mais de 30 dias:** 0 (0.0%)

## Densidade por área
Estimativa via keywords (uma memória pode contar em múltiplas áreas):

- **capturado:** 112 (54.9%)
- **projetos:** 59 (28.9%)
- **dimagem:** 30 (14.7%)
- **saude:** 10 (4.9%)
- **construcao:** 3 (1.5%)
- **receitas:** 2 (1.0%)
- **financeiro:** 2 (1.0%)

## Duplicatas suspeitas
Pares com similaridade Jaccard ≥ 0.5. Revisar manualmente — não são duplicatas garantidas, são candidatas.

### Similaridade 0.53
- **A** (2026-04-24): *"Isabela Barros de Souza has a cranial MRI at Assim São Gonçalo with fasting confirmed +8h...."*
- **B** (2026-04-24): *"Theo Silva Alvarenga has a cranial MRI at Assim São Gonçalo with fasting confirmed at 8am...."*

## Gaps (áreas com índice mas sem memória)

- Nenhum gap detectado.

## Uso
- Bot consulta este arquivo via tool `auditoria_mem0()` quando o Gustavo pergunta sobre o estado das suas próprias memórias no Mem0.
- Não confundir com `meta_memoria()`, que retorna `gus/meta-memoria.md` (auto-conhecimento do Gus).
- SELF-1 (reflexão quinzenal) usa este arquivo pra contextualizar Nosis e Thymos com o estado do armazém de memórias sobre o Gustavo.
- Atualização automática — não editar manualmente.
