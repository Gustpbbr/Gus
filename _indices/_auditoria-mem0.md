---
tipo: meta-memoria
atualizado: 2026-04-26T11:41:18.914586-03:00
mem0_total: 190
---

# Auditoria do Mem0 (memórias sobre o Gustavo)

Análise automática e determinística do estado do armazém de memórias SOBRE O GUSTAVO (Mem0). Gerada diariamente via GitHub Action (`auditoria_mem0.py`). Sem LLM — heurística baseada em keywords e similaridade Jaccard.

**Não confundir com meta-memória do Gus** (`gus/meta-memoria.md`), que é o auto-conhecimento do próprio Gus.

## Estatísticas gerais
- **Total:** 190 memórias
- **Mais antiga:** 2026-04-11 — *"User wants to edit, sign, and share PDF files from any location and is directed ..."*
- **Mais recente:** 2026-04-26 — *"The Tavily API Key is not configured in Railway's environment variables, so sear..."*

## Frescor
- **Últimas 24h:** 73 (38.4%)
- **Últimos 7 dias:** 109 (57.4%)
- **Últimos 30 dias:** 8 (4.2%)
- **Mais de 30 dias:** 0 (0.0%)

## Densidade por área
Estimativa via keywords (uma memória pode contar em múltiplas áreas):

- **capturado:** 106 (55.8%)
- **projetos:** 52 (27.4%)
- **dimagem:** 30 (15.8%)
- **saude:** 9 (4.7%)
- **construcao:** 3 (1.6%)
- **receitas:** 2 (1.1%)
- **financeiro:** 2 (1.1%)

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
