---
tipo: diagnostico
area: gus
escopo: stack memoria (Hub Qdrant + curador + fallback Mem0)
data: 2026-05-02
autor: Claude Code (sessão claude/greeting-checkin-EHt9Z)
gerado_em: 2026-05-02T22:30-03:00
fase: 0 do plano de saneamento da memória
status: concluído — 0.1, 0.2, 0.3 todos fechados
---

# Diagnóstico da stack de memória — Fase 0

Diagnóstico factual antes de mudar código. Valida 3 hipóteses da auditoria
de 02/05 (`2026-05-02-chat.md`) com dados reais. Já encontrou achados
**adicionais** que a auditoria não pegou.

## Achados principais

### A1 · O bug não foi a única falha — sistema estava degradado desde 28/04

A auditoria de 02/05 disse "curador errando 100% desde 30/04". **Realidade
é pior:**

| Data | Status do curador | Entradas | Padrão |
|---|---|---|---|
| 25/04 | OK | ~30+ | majoritariamente `salvo` |
| 26-27/04 | OK com instabilidade | ~30 | mix de `salvo`, `erro`, `fallback-mem0` |
| **28/04** | **Degradado silencioso** | 18 | **TODAS `fallback-mem0`** — curador híbrido nunca foi acionado, sistema gravou no Mem0 SaaS antigo |
| 29/04 | Bug KeyError | 9 | 9 erros (`'\n    "conteudo"'`) |
| 30/04 | Bug KeyError | 3 | 3 erros |
| 01/05 | Bug KeyError | 1 | 1 erro |
| **02/05** pós-PR #72 | Inconsistente | 5 | **1 salvo (gpt) + 4 descartados (haiku)** |

Implicações:

1. **PR #74 (testes regressão) é insuficiente.** Cobre só o `format()`/KeyError
   que apareceu em 29/04. Não pega o `fallback-mem0` silencioso de 28/04 nem
   a divergência massiva Haiku×GPT pós-fix.

2. **Os 19 fragmentos no Hub `gustavo`** (snapshot `gus-estado-atual.md`)
   provavelmente vieram de testes manuais 27-28/04 + Custom GPT/Code +
   pouquíssimo bot Telegram. Hub ficou efetivamente seco entre 28/04 e
   02/05 — não 30/04 e 02/05 como auditoria disse.

3. **Tudo que entrou no Telegram em 28/04** caiu no Mem0 antigo (18 entradas
   marcadas `fallback-mem0`). Esse conteúdo está na coleção `gus`, fora do
   Hub novo. Soma à dívida da migração `gus → gus_hub` (Fase 3.1).

### A2 · Haiku 4.5 está descartando 100% pós-fix — divergência massiva

Em 5 amostras pós-PR #72 em 02/05:

| Janela | Haiku | GPT | Status |
|---|---|---|---|
| 6cd140fc | 0 | (não logado) | descartado |
| 3a815571 | (não logado) | 5 | salvo |
| 075c8df4 | 0 | (não logado) | descartado |
| 8fcb6c9e | 0 | (não logado) | descartado |
| 3cb5d5af | 0 | (não logado) | descartado |

**Padrão:** quando Haiku roda, devolve `[]`. Quando GPT roda, extrai 5.
O curador híbrido roda os 2 em paralelo, mas o **log atual só registra 1
por entrada** — o "vencedor" (ou só um deles entra no log porque o outro
zera). Isso esconde o sinal mais importante da coleta dual.

**Hipóteses pra Haiku zerar:**
- Janelas curtas/triviais que GPT extrai com mão leve, Haiku rejeita
- Prompt do curador (mesmo pra ambos) é menos eficaz em Haiku 4.5
- Bug residual no `_render_prompt` — algo no template Haiku ainda quebra
- Haiku 4.5 mais conservador por temperature/system defaults

**Confirma item M-MED-6 da auditoria como urgente (não preventivo).** Sem
script comparativo (Fase 2.1), decisão de 12/05 vai ser cega.

### A3 · MCP Hub não acessível desta porta (esperado)

`mcp__mem0-gus__listar_memorias` falhou com `QDRANT_URL e QDRANT_API_KEY
são obrigatórias`. Confirma diagnóstico do CLAUDE.md sobre o ambiente
Code on the web. Volume real do Hub precisa ser checado **via TioGu** ou
Custom GPT (que têm credenciais em produção).

## Achado A5 · Volume confirmado, qualidade catastrófica (passo 0.1)

Gustavo executou via TioGu em 02/05 22:40 BRT. Total **40 fragmentos no Hub**:
20 em `gustavo`, 20 em `gus`.

### Distribuição de conteúdo — brain `gustavo`

| Categoria | Quantidade | % |
|---|---|---|
| Variações de "X demandas pendentes em inbox-claude-code" | 10 | 50% |
| Variações de "Bot Telegram tem ~21 tools" | 8 | 40% |
| Outros (auditoria, JSONs) | 2 | 10% |
| **Fatos biográficos reais sobre o Gustavo** | **0** | **0%** |

### Distribuição — brain `gus`

| Categoria | Quantidade | % |
|---|---|---|
| Demandas inbox (duplicado do `gustavo`) | 11 | 55% |
| Auditoria Chat / retro-engine | 6 | 30% |
| Bot Telegram (deveria ser brain gustavo) | 2 | 10% |
| **"Nasci em Vitória" (fato do Gustavo)** | **2** | **10%** — cross-brain pollution + duplicata |

### Implicações

1. **M-CRIT-1 confirmado em produção.** "Nasci em Vitória" no brain `gus`
   é exemplo concreto de pollution. O brain do agente está absorvendo
   fatos biográficos do humano.

2. **Duplicatas semânticas em escala dramática.** Mesmo fato em 6+ fragmentos
   com palavras ligeiramente diferentes. `hash_janela` não detecta porque
   são janelas distintas; falta dedup por similaridade de conteúdo.

3. **Prompt do curador é o gargalo principal.** Ele extrai qualquer afirmação
   como fragmento. Não tem filtro de relevância biográfica. Resultado:
   conversa operacional sobre o próprio sistema vira "memória sobre o Gustavo".

4. **Brain `gustavo` é inútil hoje.** 100% lixo meta-sistema. Buscar
   "preferências do Gustavo" ou "saúde" retorna `[]` — não há nada.

## Pendências da Fase 0

### 0.1 — Volume real do Hub ✅ Concluído (Gustavo via TioGu, 02/05 22:40)

**Tarefa:** mandar pro TioGu (Telegram):

> "Lista as memórias do brain gustavo, limit 100. Depois lista do brain gus,
> limit 100. Me dá o total e a data da mais recente de cada."

**Resultado:** 20 + 20 = 40 fragmentos. Confirma A1 (Hub seco) E
descobre A5 (qualidade catastrófica) — ver seção acima.

### 0.2 — Status migração `gus → gus_hub` ✅ Concluído (Gustavo dispatch, 02/05 22:48)

Workflow rodou em modo **dry-run**. Conexão Qdrant OK. Resultado:

```
[migracao] Encontrados: 0 fragmentos com conteúdo
[migracao] Nada a migrar. Saindo.
```

**Coleção `gus` (Mem0 self-hosted) está vazia.** Ver Achado A8 abaixo.

## Achado A8 · Coleção legada `gus` está vazia

Múltiplos docs do projeto afirmam que há ~204 fragmentos históricos lá.
**Não há.** Hipóteses:

1. **Sempre estiveram no Mem0 SaaS** (`api.mem0.ai`), não no Qdrant Cloud
   self-hosted. Nome "gus" como coleção Qdrant nunca foi populado.
2. **Foram apagados** em algum reset (`reset_qdrant_collection.py` existe).
3. Estavam lá sem campo `data`/`memory` válido — improvável.

## Achado A9 · 18 entradas `fallback-mem0` de 28/04 não estão acessíveis

Se a coleção `gus` está vazia, as 18 entradas marcadas `fallback-mem0` em
28/04 **não foram pra lá**. Provavelmente caíram no Mem0 SaaS via
`gus/memory.py` antigo. Vetor de perda silenciosa que continua aberto se
o caminho `fallback-mem0` ainda existe (Achado A4).

## Achado A10 · Hub novo (`gus_hub`) é todo o histórico que existe

40 fragmentos (20+20) é tudo. Não há legacy a recuperar. Decisão
arquitetural: **tratar Hub atual como ponto zero** e focar em qualidade
da captura daqui pra frente.

## Achado adicional fora do escopo planejado

### A4 · Status `fallback-mem0` não está documentado em lugar nenhum

A auditoria não mencionou esse caminho. Vasculhei `gus/bot.py` (não revi
nessa sessão) — provavelmente vem do `_resumir_e_salvar` quando o
curador híbrido lança exception. O fallback grava no Mem0 antigo (coleção
`gus`) com mensagem de resumo, sem schema gus-18.

**Implicação:** mesmo após Fase 3.2 (remover fallback Mem0 em
`gus/memory.py`), pode ter outro caminho de fallback ainda gravando na
coleção velha. Investigar `gus/bot.py:_resumir_e_salvar` antes da Fase 3.

## Refinamento do plano de saneamento

### Mudanças propostas

| Item | Refinamento | Por quê |
|---|---|---|
| Fase 1.5 (auditoria multi-brain) | **Subir prioridade** — hoje a gente nem consegue saber o estado do Hub `gus` | A1 mostrou que brain `gus` pode estar zerado em produção |
| Fase 2.1 (comparar curadores) | **Adicionar registro de divergência ZERADA** (quando 1 dos 2 retorna `[]`) | A2 mostrou que essa é a divergência mais comum hoje, e log atual esconde |
| **NOVO Fase 1.6** | Investigar `_resumir_e_salvar` no bot.py + remover caminho `fallback-mem0` que grava no Mem0 antigo | A4 — débito não-mapeado |
| Fase 3.1 (migração) | **Adicionar passo de re-ingestar fragmentos `fallback-mem0` de 28/04** com `metadata.via="telegram-claude"` + `metadata.curador="recuperacao-fallback"` | A1 — 18 entradas perdidas no Mem0 antigo |
| **NOVO Fase 1.7** | Limpeza ativa do Hub: deletar duplicatas semânticas + cross-brain pollution antes de qualquer treinamento ou comparativo | A5 — Hub atual é ~70% lixo |
| **NOVO Fase 1.8** | Script `meta_relatorio_hub.py` com distribuição por assunto + Jaccard local (sem LLM) — relatório recorrente | A5 — sem visibilidade contínua, lixo volta a acumular |
| Fase 5.1 (prompt brain `gus`) | **Subir pra antes de 12/05** + adicionar **filtro de relevância biográfica** ao prompt do brain `gustavo` (não só ao do `gus`) | A7 — comparar Haiku × GPT em prompt ruim é trocar 6 por meia dúzia |

### Nada a refazer no plano original

Fases 4, 5, 6 ainda válidas como estão. Diagnóstico não invalidou
arquitetura proposta — só ajustou prioridades + revelou débito extra.

## Próximo passo

Fase 0 concluída. Próximo: **Fase 1 (quick wins) com refinamentos** dos
achados A1-A10. Plano original ganha:

- **NOVO 1.7** Limpeza ativa do Hub (deletar duplicatas + cross-brain)
- **NOVO 1.8** `meta_relatorio_hub.py` recorrente
- **NOVO 1.6** Investigar e matar caminho `fallback-mem0` em bot.py
- **NOVO 1.9** Verificar se Mem0 SaaS ainda tem conteúdo histórico
  (decisão Gustavo: recuperar ou descartar)
- **CANCELADA Fase 3.1** (migração) — coleção vazia confirmada
- **MOVIDA Fase 3.2** (remover fallback Mem0 do código) pra dentro de Fase 1

Total Fase 1 estimado: ~7-8h Code + 1 chamada API Gustavo.
