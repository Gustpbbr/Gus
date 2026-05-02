---
tipo: status-consolidado
projeto: gus
parte: 26-status-consolidado
atualizado: 2026-05-02T01:30-03:00
---

# Gus — Status consolidado e roadmap

Documento de visão única: o que está pronto, o que falta (e quem faz),
e o caminho pra cada objetivo.

> Este é o overview operacional. Detalhe técnico fica em `_estado-atual.md`
> (handoff sessão a sessão), `gus-15-decisao-migracao.md` (ADR-001),
> `gus-30-neurogus-roadmap.md` (NeuroGus).

---

## 🟢 Pronto e em produção

### Bot Telegram (TioGu)
- **21 tools ativas** (não 22 — system_prompt tem drift, será corrigido na
  Fase 2B). Inventário fiel auto-gerado em `_tools-inventario.md` pelo
  workflow `sync-docs.yml`.
- Multimídia: imagens (Vision), PDF nativo, Word (.docx), Excel (.xlsx),
  áudio/voz (Whisper)
- Personalidade Gus em `gus/system_prompt.md` (794 linhas — pendente
  reescrita Fase 2B)
- Prompt caching ativo (Anthropic ephemeral + OpenAI auto ≥1024 tok)
- Roteamento multi-modelo (gus-29): texto puro → OpenAI gpt-4o-mini;
  image/document → Anthropic Sonnet
- Fallback cross-provider (OpenAI ↔ Anthropic)
- Retry exponencial 5xx + classificação de erros amigável
- Rate limit 20 msg/min + HARD_LIMIT mensal
- State persistido com write atômico (`/app/data/bot_state.json`)
- **Scan PII em entrada (save) e saída (resposta)** — Sessão 2 da Fase 1
- **Cache mídia com byte budget (200MB)** — Sessão 2 da Fase 1
- Suite de unit tests (163 testes, ~3.5s) — Sessão 1 da Fase 1
- Custom GPT API rodando paralela (FastAPI) — 14 endpoints REST

### Custom GPT API (FastAPI no Railway)
- 14 endpoints em `https://gus-production-58a7.up.railway.app`
- Healthcheck `/health` OK
- Bearer auth (`CUSTOM_GPT_TOKEN`)
- Proteções LGPD (path `dimagem/` bloqueado, PII scan herdado)
- ⏳ Aguarda configuração no GPT Builder (Action — só desktop)

### MCP Server público (gus_mcp)
- Deployed no Railway com URL secret no path (PRs #57/58/60)
- Tools `mcp__mem0-gus__*` acessíveis pelo Claude Chat web
- Bearer + secret no path = privacidade

### Captura multiporta — Hub Qdrant
- **Telegram TioGu**: curador híbrido (Haiku + GPT-4o-mini) a cada 3
  turnos, ambos salvam com mesmo `hash_janela` pra parear
- **Claude Chat web**: curador bidirecional (PR #67) com top-tier
  models (Sonnet 4.6 + GPT-4o), salva no brain `gustavo` E `gus`
- **Claude Code (web)**: cron */30min processa transcripts redatados
  (PR #64). Stop hook salva transcript local, cron lê via secrets.
- Esquema gus-18 completo em todas as portas

### Canal unificado `dialogos/`
- `inbox-tiogu/`, `inbox-claude-code/`, `inbox-claude-chat/`,
  `inbox-custom-gpt/`, `archive/`, `processados-erro/`, `streams/`
- Workflow `import-from-drive.yml` cron 15min: Drive → GitHub
- Workflow `archive-completed-demandas.yml` cron 15min: arquiva concluídas
- Notificação Telegram automática quando demanda chega em `inbox-tiogu/`

### SessionStart hook do Claude Code
- Lê `dialogos/inbox-claude-code/` no início de cada sessão Web
- Injeta lista de demandas pendentes no contexto
- Estado atual: `_log/transcripts-claude-code/`, `_log/retro-engine-*/`

### Workflows GitHub Actions ativos (~21)
| Workflow | Cron / Trigger | Função |
|---|---|---|
| `tests.yml` | PR + push main | **Unit tests (163 testes)** — novo Fase 1 |
| `sync-docs.yml` | push + cron 04h BRT | **Auto-gera `_tools-inventario.md`** — novo Fase 2A |
| `test-scripts.yml` | PR em scripts/hub | Smoke import dos scripts cron |
| `sync-to-drive.yml` | push em main | GitHub → Drive (incremental) |
| `import-from-drive.yml` | cron 15min | Drive → GitHub |
| `archive-completed-demandas.yml` | cron 15min | Arquiva demandas |
| `auditoria-mem0.yml` | 06:40 BRT diário | Stats Hub → `_indices/_auditoria-mem0.md` |
| `briefing-matinal.yml` | 07:00 BRT dias úteis | Briefing diário |
| `retrospectiva-semanal.yml` | sexta 20:00 BRT | Resumo semanal |
| `reflexao-quinzenal.yml` | sábado 10:00 BRT (pares) | SELF-1 |
| `export-mem0.yml` | 03:00 BRT diário | Snapshot → MD/JSON |
| `check-saude.yml` | 07:30 BRT diário | Alerta Telegram se falha |
| `curador-claude-code.yml` | cron */30min | Captura transcripts Code |
| `ingest-mem0-from-chat.yml` | cron 30min | Captura Chat → Hub |
| `gerar-estado-claude-chat.yml` | cron 15min | Atualiza `dialogos/_bootstrap/gus-estado-atual.md` |
| `notificar-inbox-tiogu.yml` | push em inbox | Avisa TioGu via Telegram |
| `migrate-mem0-to-qdrant.yml` | manual | Migra coleção legada |

### Memória Hub Qdrant
- Brain `gustavo`: ~19 fragmentos visíveis na amostra recente
- Brain `gus`: auto-observações (cresce conforme captura Code/Chat)
- Schema gus-18 (tipo / camada_temporal / area / confiança / via)
- Curador híbrido em produção desde 27/04 (coleta dual até 12/05)

---

## 🟡 Pendências imediatas — depende do Gustavo

### Bloco 1 — Decisões pendentes (paralelo, em aba separada Chat)
- **P1** captura proativa Chat (A: prompt no bootstrap / B: stop hook /
  C: curador agnóstico)
- **P2** Drive sync OAuth (1: reset / 2: Service Account / 3: aposentar)
- **P3** NeuroGus — confirmar 11.1-11.7 decisões abertas

### Bloco 2 — Configurações (precisam acesso desktop ou conta externa)
- **P7** Custom GPT Action no Builder (mobile não tem essa seção):
  - https://chatgpt.com/gpts/mine → editar Gus → Configure → Actions
  - Importar OpenAPI: `https://gus-production-58a7.up.railway.app/openapi.json`
  - Auth: API Key + Bearer + colar `CUSTOM_GPT_TOKEN`
  - Colar Instructions V2 (texto pronto em `gus-14-custom-gpt-setup.md`)
- **P8** Limpar 4+ memórias poluídas no Hub (lista das candidatas + IDs
  via MCP, Gustavo aprova quais)

### Bloco 3 — Pós 12/05 (fim da coleta dual)
- **P4** Comparar pares Haiku × GPT no Obsidian, escolher modelo final
  (Fase 5 do ADR-001)

---

## 🟡 Pendências imediatas — Claude Code (próximas sessões)

### Próxima sessão (Fase 2A — docs estáticas, ~2h)
- ✅ M8/M10 script auto-gerar `_tools-inventario.md` — feito hoje
- ✅ P9 atualizar `_estado-atual.md` + `gus-26` — feito hoje
- P10 mover `gus-08-plano-proximos-passos.md` (24/04, obsoleto) pra
  `historico/`

### Sessão dedicada (Fase 2B — system prompt, ~2h)
- **S3** reescrever `gus/system_prompt.md` (794 linhas → ~500)
  - Diff antes/depois mostrado pra Gustavo aprovar
  - Conta tools real (21, derivada de `len(TOOLS)`)
  - Fluxo Dimagem unificado (documentado 2x hoje)
  - Remover seções pré-migração Mem0

### Fase 3 — Operacional (~3h)
- **S4** alerta proativo HARD_LIMIT (workflow check-cost.yml)
- **M5** cache `auto_diagnostico` 5min
- **M7** `/foco` deleta FOCO-ATUAL antigo antes de salvar novo

### Fase 4 — Refator estrutural (~6h, depende Fase 1 ✅ já feita)
- **M1** split `gus/bot.py` em `gus/handlers/`
- **M2** promover `_chamar_claude_com_retry` → público
- **C3** split `gus/tools.py`
- **C2** threadsafe `_get_openai_client`
- **C7** + D4=A: mover `gus/dimagem.py` → `gus/integrations/dimagem.py`
- D3=C: `drop_pending_updates=True` + aviso ao Gustavo no boot

### Fase 6 — Pós 12/05 (aposentar Mem0)
- **P5** remover `mem0ai` de requirements + fallbacks
- **M3** remover `from mem0 import` em `memory.py`
- **M4** upgrade `anthropic` SDK 0.40 → 0.50+

### Fase 7 — NeuroGus (sprint dedicado, depende P3)
- ~145 LOC: `hub/events.py` + `broadcast()` hook + 2 endpoints SSE +
  `api/neurogus.py` (PWA grafo 3D)
- Plano detalhado em `gus-30-neurogus-roadmap.md`

---

## 🎯 Caminho pra **Custom GPT pleno**

Estimativa: **~30min Gustavo + 0 código meu** (tudo pronto do meu lado).

```
✅ FastAPI 14 endpoints em produção
✅ Variáveis CUSTOM_GPT_TOKEN e API_PUBLIC_URL no Railway
✅ Healthcheck /health
✅ GPT criado no Builder (mobile)
⏳ Configurar Action — DESKTOP — VOCÊ AQUI
⏳ Colar Instructions V2 anti-alucinação
⏳ Testar "qual seu nome e tools?"
⏳ Validar voice mode mobile
```

---

## 🎯 Caminho pra **Alexa em casa** (porta complementar)

Estimativa: ~6-8h Code + ~1h Gustavo.

```
✅ Pré-requisito: Custom GPT funcionando
⏳ Conta Amazon Developer
⏳ Skill manifest + Interaction Model
⏳ Backend: Lambda OU Railway endpoint (recomendado: Railway)
⏳ Progressive Response (driblar timeout 8s)
⏳ Pareamento Echo Dot 3
```

**Decisões pendentes:** TTS (Polly grátis vs ElevenLabs $5/mês),
backend (Lambda vs Railway), intents iniciais.

---

## 🔮 Caminho pra **wake word "Gus" mãos-livres** (S8 com Termux)

~5-8h Code + 1h Gustavo. Aprovado como Opção B, futuro pós-Alexa.

---

## 🟣 Decisões pendentes (acumulado)

| # | Decisão | Status |
|---|---|---|
| D1-D5 | Fase 0 do plano (D3=C, D4=A confirmadas) | ✅ feitas |
| P1-P3 | Captura Chat, Drive sync, NeuroGus 11.x | Em aba Chat |
| P4 | Modelo curador final (Fase 5 ADR-001) | Aguarda 12/05 |
| Alexa TTS | Polly vs ElevenLabs | Antes de Skill V1 |
| Alexa backend | Lambda vs Railway | Antes de Skill V1 |
| Alexa intents iniciais | quais V1 | Antes de Skill V1 |
| Sprint 3 (email/cal/TTS) | volta? | Pós Alexa V1 |
| `import-from-drive.yml` 5min vs 15min | aval real | — |
| Auto-execução de demandas (Nível 3) | — | Pós Nível 2 maduro |

---

## 🐛 Bugs conhecidos (não bloqueantes)

- 4+ memórias poluídas no brain `gustavo` aguardando limpeza (P8)
- DDG fallback ativa quando Tavily esgota cota mensal
- Hub Qdrant pode ficar ocioso por horas em janela noturna (sem ação,
  esperado)
- ~~Mem0 latência indexação~~ — não importa mais, Hub indexa em segundos
- ~~Curador 400 'temperature and top_p'~~ — corrigido 27/04, **agora
  com teste regressão** (Fase 1)
- ~~Cache mídia OOM-prone~~ — corrigido Fase 1, byte budget 200MB
- ~~PII vaza pela resposta do bot~~ — corrigido Fase 1, scan no output

---

## 📊 Visão de longo prazo

```
HOJE (02/05/2026)
├── Telegram TioGu ✅ produção (com testes + PII output)
├── Custom GPT API ✅ produção, aguarda Builder Action
├── Claude Chat ✅ via bootstrap + MCP server
├── Claude Code ✅ + captura via cron
├── MCP server público ✅
└── Canal dialogos/ ✅ bidirecional

PRÓXIMAS SEMANAS
├── Fase 2A docs estáticas (esta sessão)
├── Fase 2B system_prompt (sessão dedicada)
├── Fase 3 operacional (cost alert, cache, foco TTL)
├── Fase 4 refator estrutural (split bot.py + tools.py)
└── Custom GPT pleno (1 sessão Gustavo PC)

PÓS 12/05
├── Fase 6: aposentar Mem0, upgrade Anthropic SDK
└── Fase 7: NeuroGus (depende P3)

PRÓXIMO MÊS+
├── Alexa Skill V1 (após Custom GPT)
├── S8 câmera IP no escritório
└── Sprint 3? (email/calendar real)

PRÓXIMO TRIMESTRE
├── Wake word "Gus" no S8 (Termux + openWakeWord)
├── ElevenLabs voice clone
└── Auto-execução de demandas (Nível 3)
```

---

## 📋 Checklist rápido — próximo turno PC do Gustavo

```
[ ] Configurar Action do Custom GPT no Builder desktop
[ ] Colar Instructions V2
[ ] Limpar memórias poluídas via MCP local (~30min com Code)
```

---

## Documentos relacionados

- `_estado-atual.md` — handoff técnico entre sessões (lê primeiro)
- `_tools-inventario.md` — auto-gerado, fonte fiel das tools
- `gus-11-tools-roadmap.md` — roadmap curado (status, decisões)
- `gus-15-decisao-migracao.md` — ADR-001 aposentar Mem0
- `gus-30-neurogus-roadmap.md` — plano completo NeuroGus
- `gus-29-roteamento-multimodelo-tiogu.md` — dispatcher OpenAI/Anthropic
- `gus-14-custom-gpt-setup.md` — passo-a-passo Builder
- `dialogos/_bootstrap/gus-bootstrap.md` — ativador Claude Chat
- `dialogos/README.md` — protocolo do canal

Atualizado: 2026-05-02 01:30 BRT.
