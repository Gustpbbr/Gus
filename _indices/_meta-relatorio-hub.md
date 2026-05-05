---
tipo: meta-relatorio
atualizado: 2026-05-04T21:12:21.065383-03:00
hub_total_geral: 8709
jaccard_duplicata: 0.6
---

# Meta-relatório do Hub Qdrant

Visibilidade analítica do estado de qualidade do Hub. Sem LLM — puramente heurístico.  Diferente de `_auditoria-hub.md` (mais narrativo), este relatório foca em **distribuições agregadas** + **duplicatas candidatas** + **razão de classificação completa**.

Gerado por `.github/scripts/meta_relatorio_hub.py` (item 1.8 do plano de saneamento, 02/05/2026).

## Resumo geral

- **Total Hub:** 8709
- **Classificação completa:** 0 (0.0%)
- **Duplicatas suspeitas:** 0 pares (Jaccard ≥ 0.6)

## Por brain

### Brain `gustavo`

- **Total:** 4396
- **Classificação completa** (tipo≠episodico + camada≠sessao + area≠vazio): 0 (0.0%)
- **Duplicatas suspeitas** (Jaccard ≥ 0.6): 0 pares

**Distribuições:**

- **Por tipo:**
  - `fato`: 2755 (62.7%)
  - `decisao`: 559 (12.7%)
  - `identidade_operacional`: 219 (5.0%)
  - `biografico`: 218 (5.0%)
  - `procedural`: 204 (4.6%)
  - `cronologico`: 127 (2.9%)
  - `projeto`: 102 (2.3%)
  - `meta_reflexao`: 88 (2.0%)
  - `episodico`: 64 (1.5%)
  - `preferencia`: 23 (0.5%)
- **Por camada_temporal:**
  - `(sem)`: 4396 (100.0%)
- **Por area:**
  - `gus`: 2146 (48.8%)
  - `projetos`: 2035 (46.3%)
  - `pessoal`: 76 (1.7%)
  - `saude`: 60 (1.4%)
  - `(sem)`: 51 (1.2%)
  - `pesquisa`: 14 (0.3%)
  - `dimagem`: 9 (0.2%)
  - `financeiro`: 4 (0.1%)
  - `receitas`: 1 (0.0%)
- **Por via:**
  - `claude-code`: 4315 (98.2%)
  - `telegram-claude`: 77 (1.8%)
  - `claude-chat`: 4 (0.1%)
- **Por curador:**
  - `gpt`: 4373 (99.5%)
  - `(sem)`: 23 (0.5%)
- **Por estado:**
  - `ativo`: 4396 (100.0%)
- **Por prompt_version:**
  - `(sem)`: 4396 (100.0%)

**Top 30 tokens (sinal de assunto):**

  - `qdrant`: 644
  - `claude`: 640
  - `sistema`: 623
  - `chat`: 570
  - `curador`: 532
  - `gustavo`: 526
  - `code`: 500
  - `estado`: 495
  - `mem0`: 448
  - `fragmentos`: 444
  - `memoria`: 370
  - `demandas`: 366
  - `atual`: 351
  - `captura`: 331
  - `drive`: 328
  - `2026`: 318
  - `inbox`: 313
  - `dialogos`: 312
  - `telegram`: 312
  - `porta`: 309
  - `saas`: 261
  - `pendentes`: 257
  - `bootstrap`: 253
  - `agente`: 252
  - `arquivo`: 252
  - `projeto`: 250
  - `sync`: 250
  - `tiogu`: 249
  - `multi`: 243
  - `arquivos`: 240

### Brain `gus`

- **Total:** 4313
- **Classificação completa** (tipo≠episodico + camada≠sessao + area≠vazio): 0 (0.0%)
- **Duplicatas suspeitas** (Jaccard ≥ 0.6): 0 pares

**Distribuições:**

- **Por tipo:**
  - `fato`: 2676 (62.0%)
  - `decisao`: 548 (12.7%)
  - `identidade_operacional`: 236 (5.5%)
  - `biografico`: 206 (4.8%)
  - `procedural`: 206 (4.8%)
  - `cronologico`: 112 (2.6%)
  - `projeto`: 109 (2.5%)
  - `meta_reflexao`: 102 (2.4%)
  - `episodico`: 60 (1.4%)
  - `preferencia`: 26 (0.6%)
- **Por camada_temporal:**
  - `(sem)`: 4313 (100.0%)
- **Por area:**
  - `projetos`: 2130 (49.4%)
  - `gus`: 1966 (45.6%)
  - `pessoal`: 82 (1.9%)
  - `saude`: 70 (1.6%)
  - `(sem)`: 44 (1.0%)
  - `dimagem`: 14 (0.3%)
  - `financeiro`: 5 (0.1%)
  - `pesquisa`: 1 (0.0%)
  - `receitas`: 1 (0.0%)
- **Por via:**
  - `claude-code`: 4297 (99.6%)
  - `telegram-claude`: 14 (0.3%)
  - `claude-chat`: 2 (0.0%)
- **Por curador:**
  - `gpt`: 4297 (99.6%)
  - `(sem)`: 16 (0.4%)
- **Por estado:**
  - `ativo`: 4313 (100.0%)
- **Por prompt_version:**
  - `(sem)`: 4313 (100.0%)

**Top 30 tokens (sinal de assunto):**

  - `qdrant`: 656
  - `claude`: 627
  - `sistema`: 615
  - `curador`: 533
  - `chat`: 532
  - `code`: 522
  - `estado`: 507
  - `gustavo`: 496
  - `mem0`: 433
  - `fragmentos`: 430
  - `atual`: 383
  - `demandas`: 370
  - `memoria`: 343
  - `captura`: 337
  - `2026`: 330
  - `drive`: 321
  - `porta`: 320
  - `inbox`: 308
  - `dialogos`: 304
  - `telegram`: 300
  - `projeto`: 267
  - `multi`: 263
  - `pendentes`: 262
  - `saas`: 261
  - `agente`: 261
  - `migracao`: 256
  - `bootstrap`: 254
  - `arquivo`: 250
  - `tiogu`: 241
  - `arquivos`: 241

## Como interpretar

- **Classificação completa baixa (<50%)**: muitos fragmentos entraram via caminhos sem classificação (MCP salvar_memoria sem params até item 1.4, ou _fallback_mem0 antes do item 1.6). Sinal de poluição.
- **Duplicatas suspeitas alta**: curador re-extraiu mesmo fato em janelas diferentes; precisa de dedup (item 1.7 ou Fase 5.5).
- **Por via concentrado**: porta dominante. Se `claude-chat` >> `telegram-claude`, sistema captura mais de Chat que do bot.
- **Por prompt_version**: durante migrações de prompt (Fase 5.1), deve aparecer mistura. Após estabilização, ≥95% deve estar na versão atual.
