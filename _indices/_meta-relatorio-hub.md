---
tipo: meta-relatorio
atualizado: 2026-05-05T08:08:31.041273-03:00
hub_total_geral: 10462
jaccard_duplicata: 0.6
---

# Meta-relatório do Hub Qdrant

Visibilidade analítica do estado de qualidade do Hub. Sem LLM — puramente heurístico.  Diferente de `_auditoria-hub.md` (mais narrativo), este relatório foca em **distribuições agregadas** + **duplicatas candidatas** + **razão de classificação completa**.

Gerado por `.github/scripts/meta_relatorio_hub.py` (item 1.8 do plano de saneamento, 02/05/2026).

## Resumo geral

- **Total Hub:** 10462
- **Classificação completa:** 8791 (84.0%)
- **Duplicatas suspeitas:** 0 pares (Jaccard ≥ 0.6)

## Por brain

### Brain `gustavo`

- **Total:** 5272
- **Classificação completa** (tipo≠episodico + camada≠sessao + area≠vazio): 4485 (85.1%)
- **Duplicatas suspeitas** (Jaccard ≥ 0.6): 0 pares

**Distribuições:**

- **Por tipo:**
  - `fato`: 3248 (61.6%)
  - `decisao`: 771 (14.6%)
  - `procedural`: 242 (4.6%)
  - `identidade_operacional`: 224 (4.2%)
  - `biografico`: 218 (4.1%)
  - `projeto`: 184 (3.5%)
  - `cronologico`: 131 (2.5%)
  - `meta_reflexao`: 107 (2.0%)
  - `episodico`: 79 (1.5%)
  - `preferencia`: 26 (0.5%)
- **Por camada_temporal:**
  - `permanente`: 4244 (80.5%)
  - `sessao`: 705 (13.4%)
  - `momento`: 282 (5.3%)
  - `rotina`: 25 (0.5%)
  - `semana`: 16 (0.3%)
- **Por area:**
  - `projetos`: 2848 (54.0%)
  - `gus`: 2202 (41.8%)
  - `pessoal`: 77 (1.5%)
  - `saude`: 61 (1.2%)
  - `(sem)`: 55 (1.0%)
  - `pesquisa`: 14 (0.3%)
  - `dimagem`: 9 (0.2%)
  - `financeiro`: 5 (0.1%)
  - `receitas`: 1 (0.0%)
- **Por via:**
  - `claude-code`: 5191 (98.5%)
  - `telegram-claude`: 77 (1.5%)
  - `claude-chat`: 4 (0.1%)
- **Por curador:**
  - `gpt`: 5249 (99.6%)
  - `(sem)`: 23 (0.4%)
- **Por estado:**
  - `ativo`: 5272 (100.0%)
- **Por prompt_version:**
  - `v1-2026-05-02`: 4712 (89.4%)
  - `(sem)`: 560 (10.6%)

**Top 30 tokens (sinal de assunto):**

  - `qdrant`: 777
  - `neurogus`: 718
  - `claude`: 685
  - `sistema`: 637
  - `gustavo`: 587
  - `chat`: 586
  - `curador`: 572
  - `estado`: 554
  - `fragmentos`: 511
  - `code`: 510
  - `memoria`: 493
  - `mem0`: 460
  - `atual`: 415
  - `projeto`: 414
  - `demandas`: 377
  - `inbox`: 368
  - `drive`: 341
  - `captura`: 334
  - `2026`: 322
  - `porta`: 322
  - `dialogos`: 320
  - `telegram`: 315
  - `tiogu`: 299
  - `arquivo`: 297
  - `pendentes`: 271
  - `colecao`: 265
  - `saas`: 263
  - `agente`: 257
  - `migracao`: 254
  - `deve`: 254

### Brain `gus`

- **Total:** 5190
- **Classificação completa** (tipo≠episodico + camada≠sessao + area≠vazio): 4306 (83.0%)
- **Duplicatas suspeitas** (Jaccard ≥ 0.6): 0 pares

**Distribuições:**

- **Por tipo:**
  - `fato`: 3205 (61.8%)
  - `decisao`: 756 (14.6%)
  - `identidade_operacional`: 239 (4.6%)
  - `procedural`: 233 (4.5%)
  - `biografico`: 207 (4.0%)
  - `projeto`: 188 (3.6%)
  - `meta_reflexao`: 119 (2.3%)
  - `cronologico`: 115 (2.2%)
  - `episodico`: 63 (1.2%)
  - `preferencia`: 26 (0.5%)
- **Por camada_temporal:**
  - `permanente`: 4135 (79.7%)
  - `sessao`: 827 (15.9%)
  - `momento`: 194 (3.7%)
  - `rotina`: 23 (0.4%)
  - `semana`: 11 (0.2%)
- **Por area:**
  - `projetos`: 2940 (56.6%)
  - `gus`: 2028 (39.1%)
  - `pessoal`: 82 (1.6%)
  - `saude`: 71 (1.4%)
  - `(sem)`: 47 (0.9%)
  - `dimagem`: 15 (0.3%)
  - `financeiro`: 5 (0.1%)
  - `pesquisa`: 1 (0.0%)
  - `receitas`: 1 (0.0%)
- **Por via:**
  - `claude-code`: 5174 (99.7%)
  - `telegram-claude`: 14 (0.3%)
  - `claude-chat`: 2 (0.0%)
- **Por curador:**
  - `gpt`: 5174 (99.7%)
  - `(sem)`: 16 (0.3%)
- **Por estado:**
  - `ativo`: 5190 (100.0%)
- **Por prompt_version:**
  - `v1-2026-05-02`: 4663 (89.8%)
  - `(sem)`: 527 (10.2%)

**Top 30 tokens (sinal de assunto):**

  - `qdrant`: 803
  - `neurogus`: 688
  - `claude`: 671
  - `sistema`: 635
  - `curador`: 572
  - `estado`: 570
  - `gustavo`: 557
  - `chat`: 550
  - `code`: 532
  - `fragmentos`: 496
  - `memoria`: 461
  - `atual`: 458
  - `mem0`: 448
  - `projeto`: 438
  - `demandas`: 378
  - `inbox`: 360
  - `captura`: 339
  - `2026`: 335
  - `porta`: 331
  - `drive`: 329
  - `dialogos`: 319
  - `telegram`: 305
  - `tiogu`: 290
  - `arquivo`: 282
  - `migracao`: 274
  - `pendentes`: 269
  - `agente`: 266
  - `multi`: 263
  - `saas`: 262
  - `projetos`: 260

## Como interpretar

- **Classificação completa baixa (<50%)**: muitos fragmentos entraram via caminhos sem classificação (MCP salvar_memoria sem params até item 1.4, ou _fallback_mem0 antes do item 1.6). Sinal de poluição.
- **Duplicatas suspeitas alta**: curador re-extraiu mesmo fato em janelas diferentes; precisa de dedup (item 1.7 ou Fase 5.5).
- **Por via concentrado**: porta dominante. Se `claude-chat` >> `telegram-claude`, sistema captura mais de Chat que do bot.
- **Por prompt_version**: durante migrações de prompt (Fase 5.1), deve aparecer mistura. Após estabilização, ≥95% deve estar na versão atual.
