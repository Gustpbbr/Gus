---
tipo: status-consolidado
projeto: gus
parte: 17-status-consolidado
atualizado: 2026-04-26T01:15-03:00
---

# Gus — Status consolidado e roadmap

Documento de visão única: o que está feito, o que falta (e quem faz),
e o caminho pra cada objetivo final.

> Substitui consultas separadas a `_estado-atual.md`, `gus-10-caminho-alexa.md`,
> `gus-11-tools-roadmap.md` etc. Esses continuam fonte detalhada — este aqui é
> o overview operacional.

---

## 🟢 Pronto e em produção

### Bot Telegram (TioGu)
- 21 tools ativas (memória Mem0, GitHub, web/PubMed/arXiv, save/read, workflows, autodiagnóstico, wikilinks, perguntar GPT-5)
- Multimídia: imagens, PDF, Word, Excel, áudio (Whisper)
- Personalidade Gus completa
- Prompt caching ativo (~70% economia em janelas de 5min)
- Protocolo `dialogos/` integrado no system prompt (TioGu cria demandas com frontmatter correto)

### Custom GPT API (FastAPI no Railway)
- 14 endpoints REST em produção: `https://gus-production-58a7.up.railway.app`
- Healthcheck `/health` OK
- Bearer auth (`CUSTOM_GPT_TOKEN`)
- Proteções LGPD: path `dimagem/` bloqueado, PII scan herdado
- Tag `via=custom-gpt` em toda escrita
- ⏳ Aguarda configuração no GPT Builder (precisa desktop)

### Claude Chat (claude.ai)
- Bootstrap funcional: `Lê Gus-Sync/gus/gus-bootstrap.md e segue como Gus`
- Drive integration: lê/cria/lista arquivos em `Gus-Sync/`
- Capabilities adicionais: Calendar, Gmail, Spotify, Figma, artifacts (descobertas no teste real)
- Sem Project necessário — funciona em qualquer aba claude.ai
- Validado em produção (criou arquivo de teste, leu inbox, respondeu como Gus)

### Canal unificado `dialogos/`
- Estrutura: `inbox-tiogu/`, `inbox-claude-code/`, `inbox-claude-chat/`, `inbox-custom-gpt/`, `archive/`, `processados-erro/`, `streams/` (legado)
- Workflow `import-from-drive.yml` cron 15min: Drive → GitHub
- Frontmatter padrão validado pelo workflow
- Notificação Telegram automática quando demanda chega em `inbox-tiogu/`
- Validado bidirecional: Claude Chat → TioGu e TioGu → Claude Chat

### SessionStart hook do Claude Code
- Lê `dialogos/inbox-claude-code/` no início de cada sessão Claude Code Web
- Injeta lista de demandas pendentes no contexto

### Workflows GitHub Actions ativos
| Workflow | Cron / Trigger | Função |
|---|---|---|
| `sync-to-drive.yml` | push em main | GitHub → Drive (incremental) |
| `sync-to-drive-full.yml` | manual | GitHub → Drive (full) |
| `import-from-drive.yml` | cron 15min | Drive → GitHub (com notificação Telegram) |
| `auditoria-mem0.yml` | 06:40 BRT diário | Stats Mem0 → `_indices/_auditoria-mem0.md` |
| `briefing-matinal.yml` | 07:00 BRT dias úteis | Briefing diário |
| `retrospectiva-semanal.yml` | sexta 20:00 BRT | Resumo semanal |
| `reflexao-quinzenal.yml` | sábado 10:00 BRT (semanas pares) | SELF-1 reflexão |
| `export-mem0.yml` | 03:00 BRT diário | Snapshot Mem0 → MD/JSON |
| `check-saude.yml` | 07:30 BRT diário | Alerta Telegram se algo falhar |

### Memória Mem0
- Brain `gustavo`: 164 memórias (auditoria de 25/04 18h)
- Brain `gus`: ~4 memórias (auto-observações)
- Quota Retrieval API em 37% no dia 25 (monitorar)
- Tag `via` em toda escrita nova (rastreabilidade por porta)

### Documentação
- `gus/gus-bootstrap.md` — ativador Claude Chat
- `gus/gus-identity.md` — identidade compartilhada
- `dialogos/README.md` — protocolo do canal
- `projetos/gus/gus-11-tools-roadmap.md` — inventário de tools
- `projetos/gus/gus-12-portas-futuras.md` — diretriz arquitetural
- `projetos/gus/gus-13-tags-canonicas.md` — contrato de tags
- `projetos/gus/gus-14-custom-gpt-setup.md` — passo-a-passo Custom GPT
- `projetos/gus/gus-15-claude-chat-setup.md` — (a criar quando padrão estabilizar)
- `projetos/gus/gus-16-canal-unificado.md` — design rationale

---

## 🟡 Pendências imediatas — depende do Gustavo (no PC)

### Bloco 1 — destrava acesso pleno
1. **Criar `~/.claude/gus.env`** (4-5 keys: MEM0_API_KEY, ANTHROPIC_API_KEY, OPENAI_API_KEY, GITHUB_TOKEN, TAVILY_API_KEY)
   - Destrava MCP Mem0 nas sessões Claude Code Web (sem isso, MCP daqui é cego)
   - Destrava `perguntar_gpt` daqui via MCP local
   - Destrava limpeza de memórias poluídas
2. **Adicionar `Railway_diagnostic` no Railway Variables** (token Account/Project no dashboard Railway)
   - Destrava tool `logs_railway` em produção
3. **Adicionar `TELEGRAM_CHAT_ID` no GitHub Secrets** (se não existir; `TELEGRAM_BOT_TOKEN` já existe)
   - Destrava notificação Telegram do `import-from-drive.yml` se ainda faltava

### Bloco 2 — Custom GPT pleno (só desktop)
4. **Configurar Action no GPT Builder do Custom GPT**:
   - https://chatgpt.com/gpts/mine → editar Gus → Configure → Actions
   - Importar OpenAPI: `https://gus-production-58a7.up.railway.app/openapi.json`
   - Auth: API Key + Bearer + colar `CUSTOM_GPT_TOKEN`
   - Colar Instructions V2 anti-alucinação (texto pronto em `gus-14-custom-gpt-setup.md` linhas 59-114)
   - Salvar com Visibility = Only me

---

## 🟡 Pendências imediatas — Claude Code (próximas sessões)

### Quando Bloco 1 do Gustavo estiver pronto
1. **Limpar 4+ memórias poluídas no Mem0** via MCP local
   - "Gustavo has 128 memórias" (recursiva, contagem desatualizada)
   - "There is a suspected p..." (categoria health, verificar)
   - 2+ outras a identificar
2. **Investigar 3ª entity no Mem0** (esperado 2: `gustavo` e `gus`, dashboard mostra 3)
3. **Validar `logs_railway`** com `scripts/test_railway_logs.py` (cascata diagnóstica em 5 passos)

### Independente de Gustavo
4. **Site HTML de arquitetura** — `dialogos/inbox-claude-code/2026-04-26T00-43__site-arquitetura-projeto.md` (PAUSADA por timeout, retomar quando sessão fresh)
5. **Atualizar `gus/system_prompt.md`** se TioGu errar protocolo `dialogos/` em uso real
6. **Workflow Drive→GitHub mais frequente?** (5min em vez de 15min) se latência virar problema

---

## 🎯 Caminho pra **Custom GPT pleno** (porta de voz mobile fluida)

Estimativa total: **~30min Gustavo + 0 código meu** (já está tudo pronto do meu lado).

```
✅ 1. FastAPI com 14 endpoints em produção (https://gus-production-58a7.up.railway.app)
✅ 2. Variáveis CUSTOM_GPT_TOKEN e API_PUBLIC_URL no Railway
✅ 3. Healthcheck /health respondendo
✅ 4. GPT criado no Builder (mobile, identidade Gus, capabilities desmarcadas)
⏳ 5. Configurar Action (precisa DESKTOP — mobile não tem essa seção)  ← VOCÊ AQUI
⏳ 6. Colar Instructions V2 anti-alucinação (texto em gus-14-custom-gpt-setup.md)
⏳ 7. Testar com "qual seu nome e tools?" (deve listar real, sem alucinar)
⏳ 8. Testar voice mode (toca ícone de fone, fala normal)
```

**Bloqueio único:** desktop. Tudo o resto está pronto.

---

## 🎯 Caminho pra **Alexa em casa** (porta de voz fixa, complementar)

Estimativa total: **~6-8h código meu + ~1h Gustavo + Echo Dot 3 já tem**.

```
✅ Pré-requisito: Custom GPT funcionando (valida pattern HTTP+auth, Lambda reusa quase todo código)

⏳ 1. Criar conta Amazon Developer (gratuito, ~10min Gustavo)
⏳ 2. Criar Skill manifest (JSON: nome "Gus", invocation, idioma pt-BR) — ~1h meu
⏳ 3. Criar Interaction Model (intents iniciais: PerguntaIntent, LembraIntent, BriefingIntent) — ~1h meu
⏳ 4. Backend Skill — DUAS opções:
   (a) Lambda Python AWS (free tier 1M invoc/mês — sobra) — ~3h meu
   (b) HTTPS endpoint no Railway (reusa FastAPI, adiciona rota /alexa) — ~2h meu  ← RECOMENDADO
⏳ 5. Progressive Response (driblar timeout 8s) — ~1h meu
⏳ 6. Account linking (skill privada não exige) ou pareamento direto Echo Dot 3 — ~10min Gustavo
⏳ 7. Deploy + testar no console Alexa — ~30min meu
⏳ 8. Pareamento Echo Dot 3 com conta dev (se ainda não estiver) — ~10min Gustavo
⏳ 9. Testar "Alexa, abre Gus" → "qual o briefing" — ~10min validação real
```

**Decisões pendentes pra Alexa:**
- TTS: Polly default (gratuito, voz neutra) ou ElevenLabs voice clone ($5/mês + 1min gravação Gustavo)?
- Backend: Lambda (independente) ou Railway HTTPS endpoint (reusa)?
- Quais intents iniciais? (V1 sugerido: 3-4 intents básicos)

**Ordem recomendada após Custom GPT funcionar:**
1. Skill V1 com Polly + Railway endpoint + 3 intents (~6h meu)
2. Validar 1-2 semanas em casa
3. Voice clone + intents extras se quiser

---

## 🔮 Caminho pra **wake word "Gus" mãos-livres** (S8 com Termux)

Estimativa: **~5-8h código meu + 1h gravação voz Gustavo + S8 já tem**.

Aprovado pelo Gustavo como Opção B, futuro pós-Alexa.

```
⏳ 1. S8 velho com IP Webcam app rodando (já planejado pra ser câmera ambiente)
⏳ 2. Termux instalado no S8
⏳ 3. Python no Termux: openWakeWord + pyaudio + pyttsx3 (TTS local) ou ElevenLabs HTTP
⏳ 4. Treinar wake word "Gus" custom (~30min, 100 amostras de Gustavo falando)
⏳ 5. Loop: detecta "Gus" → grava 5-10s → Whisper transcrição → API Gus → TTS resposta
⏳ 6. Tasker pra auto-iniciar no boot do S8
```

**Vantagens vs Alexa:**
- Wake word "Gus" customizado (não precisa "Alexa, abre Gus")
- ElevenLabs voice clone (qualidade alta)
- Sem timeout 8s (pensa o quanto quiser)
- Tudo grátis (openWakeWord, Termux, pyaudio livres)

**Desvantagens vs Alexa:**
- Configuração inicial chata
- S8 plugado 24/7 (bateria pode inchar em 1-2 anos)
- Não é "appliance" como Echo Dot

---

## 🟣 Decisões pendentes

| # | Decisão | Quando |
|---|---|---|
| 1 | TTS Alexa: Polly vs ElevenLabs | Antes de implementar Alexa V1 |
| 2 | Backend Alexa: Lambda vs Railway endpoint | Antes de implementar Alexa V1 |
| 3 | Intents iniciais Alexa | Antes de implementar Alexa V1 |
| 4 | Sprint 3 (email/calendar/TTS) volta? | Depois de Alexa V1 ou Custom GPT pleno |
| 5 | Cron `import-from-drive.yml`: 5min ou 15min? | Avaliar com uso real |
| 6 | Auto-execução de demandas (Nível 3 do canal) | Depois de meses usando Nível 2 |
| 7 | Câmera IP dedicada (Tapo C100) ou seguir com S8? | Quando S8 falhar |

---

## 🐛 Bugs conhecidos (não bloqueantes)

- Mem0 latência indexação: alguns minutos entre `add` e `search` retornar
- DDG fallback se Tavily esgotar quota mensal
- Quota Retrieval API Mem0 em 37% no dia 25 — pode estourar mês se ritmo continuar
- 4+ memórias poluídas no brain `gustavo` aguardando limpeza via MCP local
- Custom GPT mobile não tem Actions (só desktop) — descoberto 25/04
- Conector GitHub nativo do ChatGPT bypass nossas proteções LGPD — recusado por design

---

## 📊 Visão de longo prazo

```
HOJE (26/04/2026)
├── Telegram TioGu ✅ produção
├── Custom GPT API ✅ produção, aguarda Builder
├── Claude Chat ✅ via bootstrap
├── Claude Code ✅
└── Canal dialogos/ ✅ funcionando bidirecional

PRÓXIMAS SEMANAS
├── Custom GPT pleno (1 sessão PC)
├── Memórias poluídas limpas
└── logs_railway validado

PRÓXIMO MÊS
├── Alexa Skill V1 em casa
├── S8 como câmera IP no escritório
└── Sprint 3? (email/calendar real)

PRÓXIMO TRIMESTRE
├── Wake word "Gus" no S8 (Termux + openWakeWord)
├── ElevenLabs voice clone
└── Eventual auto-execução de demandas (Nível 3)

LONGO PRAZO
├── Claude voice mode nativo (quando Anthropic liberar pt-BR)
├── Plugin de áudio do carro
└── Substituições graduais conforme tecnologia evolui
```

---

## 📋 Checklist rápido — o que Gustavo precisa fazer no próximo turno PC

```
[ ] 1. Criar ~/.claude/gus.env com 5 keys (MEM0, ANTHROPIC, OPENAI, GITHUB, TAVILY)
[ ] 2. Adicionar Railway_diagnostic no Railway Variables
[ ] 3. Confirmar TELEGRAM_CHAT_ID está em GitHub Secrets (TELEGRAM_BOT_TOKEN já está)
[ ] 4. Configurar Action do Custom GPT no Builder (Configure → Actions → Import OpenAPI)
[ ] 5. Colar Instructions V2 no Custom GPT (texto em gus-14)
[ ] 6. Testar Custom GPT com 2-3 perguntas reais
[ ] 7. Validar voice mode do Custom GPT mobile
```

Itens 1-3 destravam Claude Code daqui pra fazer manutenção autônoma.
Itens 4-7 destravam Custom GPT pleno.

---

## Documentos relacionados (fonte detalhada)

- `_estado-atual.md` — handoff entre sessões (mais técnico)
- `gus-10-caminho-alexa.md` — plano original Alexa (parcialmente desatualizado, este aqui prevalece)
- `gus-11-tools-roadmap.md` — inventário completo de tools com histórico
- `gus-12-portas-futuras.md` — diretriz arquitetural
- `gus-13-tags-canonicas.md` — contrato de tags `via`
- `gus-14-custom-gpt-setup.md` — passo-a-passo Custom GPT (com Instructions V2)
- `gus-16-canal-unificado.md` — design rationale do canal
- `gus/gus-bootstrap.md` — ativador Claude Chat
- `dialogos/README.md` — protocolo do canal

Atualizado: 2026-04-26 01:15 BRT.
