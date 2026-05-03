---
tipo: meta-relatorio
atualizado: 2026-05-03T07:42:27.782155-03:00
hub_total_geral: 3441
jaccard_duplicata: 0.6
---

# Meta-relatório do Hub Qdrant

Visibilidade analítica do estado de qualidade do Hub. Sem LLM — puramente heurístico.  Diferente de `_auditoria-hub.md` (mais narrativo), este relatório foca em **distribuições agregadas** + **duplicatas candidatas** + **razão de classificação completa**.

Gerado por `.github/scripts/meta_relatorio_hub.py` (item 1.8 do plano de saneamento, 02/05/2026).

## Resumo geral

- **Total Hub:** 3441
- **Classificação completa:** 0 (0.0%)
- **Duplicatas suspeitas:** 0 pares (Jaccard ≥ 0.6)

## Por brain

### Brain `gustavo`

- **Total:** 1749
- **Classificação completa** (tipo≠episodico + camada≠sessao + area≠vazio): 0 (0.0%)
- **Duplicatas suspeitas** (Jaccard ≥ 0.6): 0 pares

**Distribuições:**

- **Por tipo:**
  - `fato`: 1134 (64.8%)
  - `decisao`: 217 (12.4%)
  - `identidade_operacional`: 89 (5.1%)
  - `procedural`: 71 (4.1%)
  - `cronologico`: 55 (3.1%)
  - `biografico`: 47 (2.7%)
  - `episodico`: 37 (2.1%)
  - `meta_reflexao`: 35 (2.0%)
  - `projeto`: 33 (1.9%)
  - `preferencia`: 15 (0.9%)
- **Por camada_temporal:**
  - `(sem)`: 1749 (100.0%)
- **Por area:**
  - `projetos`: 889 (50.8%)
  - `gus`: 820 (46.9%)
  - `(sem)`: 24 (1.4%)
  - `saude`: 7 (0.4%)
  - `pessoal`: 6 (0.3%)
  - `pesquisa`: 1 (0.1%)
  - `receitas`: 1 (0.1%)
  - `dimagem`: 1 (0.1%)
- **Por via:**
  - `claude-code`: 1684 (96.3%)
  - `telegram-claude`: 62 (3.5%)
  - `claude-chat`: 3 (0.2%)
- **Por curador:**
  - `gpt`: 1727 (98.7%)
  - `(sem)`: 22 (1.3%)
- **Por estado:**
  - `ativo`: 1749 (100.0%)
- **Por prompt_version:**
  - `(sem)`: 1749 (100.0%)

**Top 30 tokens (sinal de assunto):**

  - `claude`: 285
  - `qdrant`: 251
  - `curador`: 237
  - `code`: 229
  - `estado`: 216
  - `sistema`: 213
  - `chat`: 207
  - `demandas`: 181
  - `gustavo`: 168
  - `fragmentos`: 166
  - `mem0`: 160
  - `2026`: 157
  - `dialogos`: 157
  - `atual`: 151
  - `drive`: 150
  - `inbox`: 148
  - `memoria`: 141
  - `captura`: 140
  - `telegram`: 128
  - `porta`: 127
  - `tiogu`: 126
  - `pendentes`: 112
  - `sync`: 107
  - `migracao`: 107
  - `projeto`: 104
  - `saas`: 104
  - `deve`: 100
  - `multi`: 94
  - `nova`: 89
  - `multiporta`: 88

### Brain `gus`

- **Total:** 1692
- **Classificação completa** (tipo≠episodico + camada≠sessao + area≠vazio): 0 (0.0%)
- **Duplicatas suspeitas** (Jaccard ≥ 0.6): 0 pares

**Distribuições:**

- **Por tipo:**
  - `fato`: 1122 (66.3%)
  - `decisao`: 203 (12.0%)
  - `identidade_operacional`: 96 (5.7%)
  - `procedural`: 73 (4.3%)
  - `cronologico`: 47 (2.8%)
  - `biografico`: 37 (2.2%)
  - `projeto`: 35 (2.1%)
  - `meta_reflexao`: 28 (1.7%)
  - `episodico`: 21 (1.2%)
  - `preferencia`: 14 (0.8%)
- **Por camada_temporal:**
  - `(sem)`: 1692 (100.0%)
- **Por area:**
  - `projetos`: 990 (58.5%)
  - `gus`: 655 (38.7%)
  - `(sem)`: 26 (1.5%)
  - `pessoal`: 8 (0.5%)
  - `saude`: 6 (0.4%)
  - `dimagem`: 5 (0.3%)
  - `pesquisa`: 1 (0.1%)
  - `receitas`: 1 (0.1%)
- **Por via:**
  - `claude-code`: 1677 (99.1%)
  - `telegram-claude`: 14 (0.8%)
  - `claude-chat`: 1 (0.1%)
- **Por curador:**
  - `gpt`: 1677 (99.1%)
  - `(sem)`: 15 (0.9%)
- **Por estado:**
  - `ativo`: 1692 (100.0%)
- **Por prompt_version:**
  - `(sem)`: 1692 (100.0%)

**Top 30 tokens (sinal de assunto):**

  - `claude`: 303
  - `qdrant`: 260
  - `curador`: 252
  - `code`: 241
  - `estado`: 228
  - `sistema`: 228
  - `chat`: 199
  - `demandas`: 186
  - `atual`: 176
  - `mem0`: 168
  - `captura`: 154
  - `dialogos`: 154
  - `fragmentos`: 153
  - `drive`: 150
  - `inbox`: 148
  - `2026`: 147
  - `memoria`: 142
  - `gustavo`: 137
  - `porta`: 131
  - `migracao`: 129
  - `pendentes`: 127
  - `telegram`: 123
  - `saas`: 120
  - `projeto`: 118
  - `sync`: 117
  - `tiogu`: 112
  - `multi`: 108
  - `multiporta`: 102
  - `oauth`: 101
  - `central`: 90

## Como interpretar

- **Classificação completa baixa (<50%)**: muitos fragmentos entraram via caminhos sem classificação (MCP salvar_memoria sem params até item 1.4, ou _fallback_mem0 antes do item 1.6). Sinal de poluição.
- **Duplicatas suspeitas alta**: curador re-extraiu mesmo fato em janelas diferentes; precisa de dedup (item 1.7 ou Fase 5.5).
- **Por via concentrado**: porta dominante. Se `claude-chat` >> `telegram-claude`, sistema captura mais de Chat que do bot.
- **Por prompt_version**: durante migrações de prompt (Fase 5.1), deve aparecer mistura. Após estabilização, ≥95% deve estar na versão atual.
