---
tipo: diagnostico
area: gus
escopo: stack memoria (Hub Qdrant + curador + fallback Mem0)
data: 2026-05-02
autor: Claude Code (sessão claude/greeting-checkin-EHt9Z)
gerado_em: 2026-05-02T22:30-03:00
fase: 0 do plano de saneamento da memória
status: parcial — 0.3 concluído, 0.1 e 0.2 pendentes Gustavo
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

## Pendências da Fase 0

### 0.1 — Volume real do Hub (pendente Gustavo)

**Tarefa:** mandar pro TioGu (Telegram):

> "Lista as memórias do brain gustavo, limit 100. Depois lista do brain gus,
> limit 100. Me dá o total e a data da mais recente de cada."

**O que esperar:**
- Se total `gustavo` < 30: confirma A1 (Hub seco entre 28/04 e 02/05)
- Se total > 100: hipótese cai, prioridade da Fase 3 baixa
- Mais recente de `gus`: deve ser timestamp 02/05 pós-fix se PR #72 produzir
  fragmentos. Se for de 27/04, brain `gus` está zerado em produção.

### 0.2 — Status migração `gus → gus_hub` (pendente Gustavo)

**Tarefa:** abrir https://github.com/Gustpbbr/Gus/actions/workflows/migrar-gus-para-hub.yml

**Reportar:**
1. Quantos runs aparecem
2. Última execução: data + status (success/failure)
3. Modo do último run: `dry-run` ou `migrar`?

**Decisão derivada:**
- Nunca rodou OU só dry-run → Fase 3.1 vira primeira execução
- Já rodou em `migrar` com sucesso → checar se 200+ fragmentos aparecem com
  `metadata.curador="haiku-migracao"` no Hub (parte de 0.1)

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

### Nada a refazer no plano original

Fases 4, 5, 6 ainda válidas como estão. Diagnóstico não invalidou
arquitetura proposta — só ajustou prioridades + revelou débito extra.

## Próximo passo

Gustavo executa 0.1 + 0.2 (5min Telegram + 1min navegador). Eu atualizo
este documento com os números. Depois disparamos Fase 1 (quick wins).

---

_Atualização ao receber dados de 0.1 e 0.2 — campo "Achados" ganha seção
A5 com volume confirmado, e A6 com status de migração._
