---
tipo: estado-atual-sessao
atualizado: 2026-05-02T01:36-03:00
---

# Estado atual — handoff entre sessões

Documento vivo. Atualizar no fim de cada sessão Code que deixa algo no meio.

## Últimas sessões (ambas em 02/05/2026 madrugada)

Duas sessões Code paralelas no mesmo dia. **Sessão A** = saneamento do
TioGu (testes, PII, byte budget). **Sessão B** = auditoria da porta
Claude Chat + hardening MCP/curador. Independentes em escopo, mergeáveis
em qualquer ordem.

### Sessão A — Fase 1 saneamento TioGu (commits `55c1de8` + `d8ee949`, PR #73)

Sessão de hygiene/manutenção do bot Telegram. Plano completo no chat
`claude/project-discussion-fkfA8`. Sessões 1 e 2 da Fase 1 concluídas.

**Resumo executivo:** análise técnica imparcial do TioGu listou pontos
severos / médios / cosméticos por categoria. Fase 1 = rede de segurança
via testes + tapar vazamentos críticos. **163 testes verdes**, suite
roda em ~3.5s.

**O que foi feito:**

Sessão 1 — Testes do caminho crítico (commit `55c1de8`):
- Suite `tests/` com 142 testes em 6 arquivos
- Cobertura: `_chamar_claude_com_retry` (system="" omitido — bug
  histórico do curador 27/04 agora coberto), `salvar_memorias`
  (Hub-first com Mem0 fallback), `_load_state`/`_save_state`
  round-trip, `_validar_path` (traversal), `_extrair_json` (markdown
  fence), `escanear`/`redact` (PII), regex Dimagem
- Mocks: `anthropic.AsyncAnthropic`, `hub.store.ingestar/lembrar`
- Workflow `.github/workflows/tests.yml` em PR + push main
- `pyproject.toml` config pytest (asyncio_mode=auto)
- `requirements-dev.txt`
- Hook `scan_sensivel.py` ganhou `tests/` na ALLOW_PREFIXES

Sessão 2 — PII output + byte budget + cleanup (commit `d8ee949`):
- **S2 PII no output:** `_redigir_resposta()` em `gus/bot.py` reusa
  `redact()` de `patterns_sensiveis`. Aplicado em `_responder` antes
  do `reply_text`. Anexa nota visível ao Gustavo listando tipos
  redatados.
- **S5 byte budget cache mídia:** `_CACHE_MAX` (count) → `_CACHE_MAX_ITEMS=50`
  + `_CACHE_MAX_BYTES=200MB`. Ejeção LRU por count OU bytes.
- **C1** `gus/logger.py`: 3 linhas mortas removidas
- **C4** `gus/memory.py`: `VIA_DEFAULT` virou `_via_default()` lazy
- **C5** `gus/llm.py`: `_build_tools_cached` com anchor por nome estável
- **C6** `gus/llm.py`: fallback openai→anthropic concatena ambas exceções
- +21 testes (TestRedigirResposta, TestContentBytes, TestCachePut*)

Validação: suite local **163 passed in 3.54s**. CI verde após push.

### Sessão B — Auditoria do Chat + hardening (commits `e9d4046` + `5fa805f`, PR #72)

Auditoria multi-especialista da porta Claude Chat (todas as superfícies:
bootstrap, MCP, Drive sync, curador, ingest pipeline). Identificou 31
achados (3 críticos + 9 altos + 13 médios + 6 baixos). Branch
`claude/audit-chat-fixes` resolveu **12 itens**; resto pendente em
`projetos/gus/auditorias/2026-05-02-chat.md`.

**Resumo executivo:**

- **Curador estava errando 100%** desde 30/04 — `prompt_template.format()`
  encontrava `{` literais do exemplo JSON dos templates e dava
  `KeyError('\n    "conteudo"')`. Bug reproduzido 1:1 com snippet mínimo.
  Fix: substituir `format()` por `replace()`. Afeta tanto Telegram quanto
  upload do Chat. Hub não recebia nada via curadoria há 3 dias.
- **MCP server tinha fail-open** quando `MCP_AUTH_DISABLED=true && sem MCP_URL_SECRET`.
  Agora retorna 503 em tudo (exceto /health) até alguém configurar um dos dois.
- **Whitelist user_id** em `ingestar_fragmento` aceita só {gustavo, gus}.
- **Validação fragmentos**: tipo/camada/area validados contra enum gus-18,
  confiança clamped pra [0,1].
- **Retry git push** no `ingest_mem0_from_chat` (2/4/8/16s).
- **processados-erro/** ativo: arquivo que faz curador errar agora vai pra
  `inbox-mem0-from-chat/processados-erro/AAAA-MM/` em vez de loop infinito.
- **Bootstrap atualizado**: aviso de Drive stale + recomendação `read_repo_file`
  MCP > Drive enquanto OAuth não voltar.
- **gus-28-passo2-mcp-server.md reorganizado**: Etapa 1 = `MCP_URL_SECRET`,
  Bearer migra pra anexo.

## PRs/branches recentes (28/04 → 02/05)

| PR | Descrição | Estado |
|---|---|---|
| #57 | fix MCP lifespan (Connector cadastrava direito) | mergeado |
| #58 | fix MCP lifespan (cherry/related) | mergeado |
| #60 | `MCP_URL_SECRET` no path pra privacidade no claude.ai web | mergeado |
| #61 | demandas captura multiporta + Drive sync OAuth | mergeado |
| #62 | captura proativa MCP (revertido depois) | mergeado |
| #63 | arquiva 2 demandas MCP resolvidas | mergeado |
| #64 | captura transcripts Claude Code via cron | mergeado |
| #67 | curador-chat bidirecional + modelos top-tier | mergeado |
| #70 | demanda consolidada pendências Claude Chat | mergeado |
| #72 | auditoria Chat — 12 itens (Sessão B) | aberto |
| #73 | Fase 1 saneamento TioGu (Sessão A) | mergeado |

## Estado das demandas pendentes em `inbox-claude-code/`

1. `2026-05-01-captura-multiporta-curador.md` — decidir A/B/C, requer Gustavo
2. `2026-05-01-drive-sync-oauth-fix.md` — decidir 1/2/3, requer Gustavo
3. `2026-05-02-pendencias-claude-chat-consolidacao.md` — guarda-chuva 6 fronts

## Pendente pra próxima sessão

### Da Sessão A (Fase 1 TioGu)

**Fase 2A — Reconciliação docs estáticas (~2h):**

1. **M8/M10** ✅ — `scripts/gerar_lista_tools.py` + workflow `sync-docs.yml`
2. **P9** ✅ — `_estado-atual.md` + `gus-26-status-consolidado.md` atualizados
3. **P10** decidir `gus-08-plano-proximos-passos.md` (24/04 obsoleto):
   mover pra `historico/`

**Fase 2B — System prompt (~2h, dedicada, risco alto):**

- **S3** reescrever `gus/system_prompt.md` (794 linhas → ~500): conta de
  tools real (21, vai virar `len(TOOLS)`), unificar Dimagem, remover
  seções pré-migração ADR-001. Diff explícito antes do commit.

**Fase 3 — Operacional (~3h):**

- **S4** alerta proativo HARD_LIMIT (cron check-cost.yml + 2º canal)
- **M5** cache `auto_diagnostico` 5min
- **M7** `/foco` deleta FOCO-ATUAL antigo antes de salvar novo

**Fase 4 — Refator estrutural (~6h, depende Fase 1 done ✅):**

- **M1** split `gus/bot.py` em `gus/handlers/{text,photo,document,voice,commands}.py`
  + `gus/state.py`
- **M2** promover `_chamar_claude_com_retry` → público
- **C3** split `gus/tools.py` (1140 linhas)
- **C2** threadsafe `_get_openai_client`
- **C7** mover `dimagem.py` (D4 = A já decidido)

### Da Sessão B (Auditoria Chat — PR #72)

**Prioridade 1 — operacional Gustavo (~30min no celular):**

- **Setar `MCP_URL_SECRET` no Railway** (32+ chars hex). Destrava privacidade
  + escrita do Chat. Hoje MCP roda público.
- **Recadastrar Connector claude.ai** com URL `/<secret>/mcp`.
- **Decidir Drive sync** (1/2/3 da demanda). Recomendação: Service Account.

**Prioridade 2 — decisões arquiteturais (Gustavo + Code):**

- Hierarquia de canais de escrita do Chat (real-time MCP vs upload curado vs
  demanda inbox). Bootstrap precisa orientar o Chat.
- Refinar bidirecional curador (gustavo+gus). Mesmo prompt rodando 2× sem
  distinção — pode duplicar fragmentos cross-brain.
- Aprovar Opção A (captura tempo real Chat via prompt no bootstrap).

**Prioridade 3 — NeuroGus (gus-30) bloqueado:**

- §11.1: confirmar K=3, threshold=0.6
- §11.2: localizar mock HTML 28/04 ou recriar
- §11.3-11.5: 3 decisões UX
- Fase 1 backend SSE: `hub/events.py`, `broadcast()`, `/hub/recent`,
  `/hub/stream`. Branch `claude/neurogus-fase1-backend-sse`.

### Fase 5 — Decisões pendentes Gustavo (paralelo)

Tratado em aba separada do Claude Chat:
- **P1** captura Claude Chat (A/B/C) — coberto por Sessão B P2
- **P2** Drive sync OAuth (1/2/3) — coberto por Sessão B P1
- **P3** NeuroGus (decisões 11.1-11.7) — coberto por Sessão B P3

Pendente do Gustavo aqui:
- **P7** Custom GPT desktop — configurar Action no Builder
- **P8** limpar 4+ memórias poluídas no brain `gustavo`

### Fase 6 — Aposentar Mem0 (bloqueado até 12/05)

- Coleta dual Anthropic × OpenAI termina **12/05/2026**
- Após: Gustavo escolhe modelo, Code limpa fallback, remove `mem0ai`,
  remove secret `MEM0_API_KEY`, upgrade `anthropic` SDK 0.40 → 0.50+

### Fase 7 — NeuroGus (sprint dedicado, depende decisão P3)

~145 LOC: `hub/events.py` + `broadcast()` + 2 endpoints SSE +
`api/neurogus.py` (PWA). Plano em `gus-30-neurogus-roadmap.md`.

## Decisões importantes tomadas (acumulado)

### Tomadas em 2026-05-02 (Sessão A — Fase 1 TioGu)

- **D3 = C** — `drop_pending_updates=True` mantido + aviso ao Gustavo
  no boot se houver msgs pendentes
- **D4 = A** — mover `gus/dimagem.py` → `gus/integrations/dimagem.py`
- **Testes obrigatórios pré-merge** — qualquer mudança em `gus/` precisa
  de teste cobrindo o caminho. Suite verde = porta de entrada pra main.

### Tomadas em 2026-05-02 (Sessão B — Auditoria Chat)

- **Bug curador `format()` vs `replace()`** — não usar str.format() em
  templates com JSON example literal. Replace com placeholders nomeados
  é mais robusto.
- **Fail-closed default** no MCP server — segurança não-opcional.
- **Whitelist user_id** — invariante dos brains (`gustavo`, `gus`) é hard
  constraint. Outros brains exigem schema novo + revisão privacidade.
- **processados-erro** — loop infinito no ingest é pior que move + alerta
  manual.

### Tomadas em 2026-04-27

- **ADR-001: aposentar Mem0** — wrapper mem0 self-hosted limita schema rico,
  Hub direto permite payload completo gus-18. Caminho:
  Fase 1 (Hub criado) → Fase 2 (curador) → Fase 3 (bot lê Hub) → Fase 4
  (migrar dados) → Fase 5 (aposentar Mem0)
- **Curador híbrido** Haiku × Sonnet em paralelo (mudou pra Haiku × GPT-4o-mini
  em 29/04 via gus-29 Fase 3 — resiliência cross-vendor + custo 10× menor)
- **Patterns sensíveis em fonte única** (`gus/patterns_sensiveis.py`)
- **OCR confiança gate** — schema do Haiku Vision auto-avalia confiança em
  3 níveis. Baixa bloqueia save.

### Tomadas antes (2026-04-25 e anteriores, ainda válidas)

- **Alexa não é o destino final** — porta complementar. Conversa fluida =
  mobile (Custom GPT + Claude voice).
- **Câmera no Echo Show inviável via Skill** — caminho real é câmera IP separada.
- **Wake word "Gus" no S8** = Termux + openWakeWord, pós-Alexa.
- **Conector GitHub nativo do ChatGPT recusado** — bypass de LGPD. Custom
  GPT acessa GitHub APENAS via Action REST nossa.
- **Claude Chat tem write no Drive** — habilita loop assíncrono real (mas
  sync OAuth atualmente quebrado).
- **Canal unificado `dialogos/` por destinatário** — evita explosão N×N.
- **Auto-execução desabilitada V1** — Gustavo no loop pra revisar antes.

## Branches ativas

- `claude/audit-chat-fixes` — PR #72 aberto (Sessão B)
- `claude/project-discussion-fkfA8` — PR #73 mergeado (Sessão A, Fase 1)

## Bugs em aberto (não bloqueantes)

- DDG fallback ativa quando Tavily esgota cota (esperado, sem ação)
- 4+ memórias poluídas no brain `gustavo` aguardando limpeza manual via
  MCP (P8, deletar_memoria)
- Drive sync GitHub→Drive quebrado desde 01/05 14:38Z (refresh token expirado).
  Demanda em `inbox-claude-code/2026-05-01-drive-sync-oauth-fix.md`.
- Hub Qdrant pode ficar ocioso por horas em janela noturna (sem ação)

## Mudanças no projeto desde o último estado-atual (27/04)

PRs entre 27/04 e 02/05:
- **#57/#58/#60** MCP server público no Railway com URL secret no path
- **#63** arquiva 2 demandas MCP resolvidas
- **#64** captura transcripts Claude Code via cron
- **#67** curador-chat bidirecional (gustavo + gus) com Sonnet 4.6 + GPT-4o
- **#70** demanda consolidada pendências Chat (6 fronts)
- **#72** auditoria Chat — 12 itens (aberto, Sessão B)
- **#73** Fase 1 saneamento TioGu (Sessão A)

## Como usar este arquivo

1. Próxima sessão Code: ler ANTES de outras coisas. Pega o fio dos PRs
   recentes, do plano em curso, das decisões já tomadas.
2. Ao fim da sessão: atualizar "Última sessão" + "Pendente" com o que
   ficou no meio. Commit + push antes de encerrar.

Relacionado: [[gus-01-visao-geral]], [[gus-10-caminho-alexa]],
[[gus-15-decisao-migracao]], [[gus-23-logica-qdrant-mem0]],
[[gus-26-status-consolidado]], [[gus-28-acesso-hub-claude-chat]],
[[gus-30-neurogus-roadmap]], [[auditorias/2026-05-02-chat]]

---

## Histórico (sessões anteriores resumidas)

### 2026-04-27 — maratona Claude Code (ADR-001 Fases 3+4 + fixes)

Resolução de **5 demandas do inbox** + R2/R6/R7 da auditoria fiscal +
**bug 400 do curador** (causa antiga: `system=""` ativava defaults
conflitantes; corrigido movendo prompt pra `system_prompt` canônico) +
finalização da migração Mem0 → Hub Qdrant.

PRs #8, #9, #10. Bugs críticos resolvidos:
1. Curador 400 `temperature and top_p` (system="" no Sonnet 4.6).
2. TioGu reportando "Mem0 silêncio 25h" — `_check_mem0` → `_check_hub`.
3. OCR Dimagem com nome trocado em prontuário (gate de confiança no Vision).

### 2026-04-29 a 2026-05-01 — sequência MCP + curador-chat

- gus-29 Fase 3: troca Sonnet → GPT-4o-mini no curador
- PR #57/#58: fix lifespan MCP
- PR #60: `MCP_URL_SECRET` no path
- PR #61: 2 demandas (captura multiporta + Drive sync OAuth)
- PR #64: captura transcripts Claude Code via cron
- PR #67: curador-chat bidirecional + modelos top-tier
- PR #70: demanda consolidada pendências Claude Chat
