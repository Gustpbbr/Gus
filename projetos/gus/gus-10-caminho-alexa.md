---
tipo: documentacao-projeto
projeto: gus
parte: 10-caminho-alexa
atualizado: 2026-04-24
---

# Gus — Caminho até a Alexa

Plano consolidado de onde estamos até o objetivo final: **skill da Alexa funcionando em casa**. Atualizado após a maratona de 23-24/abr/2026.

## Estado real (snapshot 2026-04-24)

### ✅ Feito

**Infraestrutura:**
- Bot Telegram rodando 24/7 no Railway
- 13 tools ativas no bot (`read_from_github`, `list_github_directory`, `list_commits`, `search_memory`, `meta_memoria`, `auditoria_mem0`, `salvar_memoria_gus`, `buscar_memoria_gus`, `search_web`, `save_to_github`, `criar_acao`, `disparar_workflow`, + processamento multimídia)
- 7 workflows GitHub Actions (export Mem0, auditoria Mem0, briefing matinal, retrospectiva semanal, reflexão quinzenal SELF-1, sync Drive OAuth2 ✅, full sync manual)
- Drive Inbox bidirecional: Apps Script `.gs` varrendo `Gus-Sync/Inbox/` a cada 5min → push GitHub → sync volta (Claude Projetos consegue salvar `.md` no repo sem interação direta)

**Multimídia:**
- Imagens (resize automático, formato detectado)
- PDFs (Claude nativo, OCR)
- Word (.docx) e Excel (.xlsx)
- **Áudio/voz via Whisper** (pt-BR, até 25MB) ← concluído hoje

**Memória:**
- Mem0 com **2 brains separados**: `user_id="gustavo"` (fatos sobre o Gustavo) e `user_id="gus"` (auto-observações do bot)
- Meta-memória narrativa em `gus/meta-memoria.md`
- Resumo extrativo a cada 3 turnos
- Auditoria Mem0 diária
- Export `.md` + `.json` diário (backup completo)

**Resiliência:**
- Retry exponencial + fallback Haiku em falhas Anthropic
- Mensagens de erro específicas em português
- Rate limit (20 msg/min)
- Scan de dados sensíveis
- Recovery de contexto em redeploy

**Identidade e governança:**
- 4 princípios fundamentais no topo do system prompt (não alucinar, buscar antes de afirmar, citar fonte, verificar antes de afirmar ausência)
- SELF-1 (Nosis + Thymos + Síntese) validado em produção — primeira reflexão gerou observações acionáveis reais
- Protocolo `dialogos-tiogu-claude/` ativo — bot e Claude Code conversam via commits

**Documentação estruturada:**
- `projetos/gus/gus-01` a `gus-09` (visão, implementado, config, segurança, portas, autonomia, decisões, plano, guia)
- `projetos/gus/futuro/` com 14 ideias mapeadas (fut-01 a fut-14)
- `_indices/` com 7 dashboards MOC por área

### 🟡 Pendente de ação tua

| Item | Esforço | Valor |
|------|---------|-------|
| Volume Railway (`/app/data`) | 5min | Persiste logs + histórico de conversa |
| Claude Chat Project (refazer com identity.md) | 10min | 4ª porta ativa |
| Trigger Apps Script `processInbox` (5min) | 2min | Fecha fluxo Drive Inbox → GitHub |

### 🚧 Bloqueios conhecidos

- **Google Cloud policy** bloqueia Service Account JSON keys — Drive sync **resolvido via OAuth2 com refresh token** ✅ (conta Gustavo, não SA). Calendar tool ainda bloqueado pela mesma policy se tentar SA; alternativa é mesmo padrão OAuth2.
- **Twilio WhatsApp Business** tem prazo de aprovação de número (dias) — se escolhermos WhatsApp como primeiro executor

## Caminho crítico até Alexa

```
ESTADO ATUAL (base sólida)
         ↓
 [ Custom GPT no ChatGPT ] ← PRÓXIMO PASSO, valida pattern externo
         ↓
 [ Executor de 1 ação real ] ← Twilio OU Calendar
         ↓
 [ Alexa Skill + AWS Lambda ] ← objetivo final
```

## Passos restantes — detalhado

### Passo 1 — Custom GPT (PRÓXIMO)

**Objetivo:** ensaiar o pattern "voz externa → HTTP → Mem0/GitHub" antes da Alexa. Gus com voz no ChatGPT mobile.

**Meu trabalho (~3-4h):**
1. Pasta `api/` com FastAPI
2. 7 endpoints REST espelhando tools do bot:
   - `POST /search_memory`, `POST /save_to_github`, `POST /search_web`, `POST /meta_memoria`, `POST /buscar_memoria_gus`, `POST /list_commits`, `GET /health`
3. Bearer token auth (`Authorization: Bearer <CUSTOM_GPT_TOKEN>`)
4. `main.py` passa a rodar bot + FastAPI em paralelo via asyncio
5. Dockerfile/railway.toml expõem `$PORT`
6. OpenAPI spec auto-gerado em `/openapi.json`
7. Documentar em `projetos/gus/gus-11-custom-gpt-setup.md`

**Tua ação (~20min):**
1. Gerar string aleatória forte (ex: `openssl rand -hex 32`) → adicionar `CUSTOM_GPT_TOKEN` no Railway
2. `chatgpt.com/gpts/editor` → Create a GPT:
   - Nome: `Gus`
   - Instructions: colar `gus/gus-identity.md`
   - Capabilities: só **Actions**
   - Action: importar OpenAPI via URL pública Railway
   - Auth: API Key → colar `CUSTOM_GPT_TOKEN`
3. Testar em voz no celular

**Plano a médio prazo:**
- Quando tu trocar a assinatura ChatGPT Plus pro `gustavo.pratti@gmail.com`, será possível também ativar **Google Drive nativo no ChatGPT** — camada extra de leitura via OAuth, complementando os endpoints HTTP. Por enquanto fica no Plus atual, pattern HTTP cobre o necessário.

### Passo 2 — Volume Railway (recomendado antes ou paralelo)

**Objetivo:** persistir logs/ e conversation_histories/ entre redeploys.

**Meu trabalho (~30min):**
- `bot.py` passa a salvar/carregar `conversation_histories` em JSON no disco
- `logger.py` aponta pra `/app/data/logs/`
- Leitura na inicialização

**Tua ação (~5min):**
- Railway → Settings → Volumes → New Volume → `/app/data` 1GB

### Passo 3 — Executor de fila de ações (pelo menos 1)

**Objetivo:** passar de "enfileirar ação" pra "executar ação". Pré-requisito pra Alexa fazer algo útil ("Alexa, manda msg pra mãe").

**Opções (escolher 1 pra começar):**

**Opção A — Twilio WhatsApp** (mais útil no dia-a-dia)
- **Meu trabalho (~3h):** GitHub Action cron varrendo `acoes/pendentes/*.md`, executor Twilio, move pra `concluidas/`, notifica Telegram
- **Tua ação:** conta Twilio + número + 3 secrets no GitHub + `contatos/mapa.md` populado
- **Prazo externo:** aprovação de número WhatsApp Business pode levar dias

**Opção B — Google Calendar** (mais rápido de setar)
- **Meu trabalho (~1-2h):** tool `criar_evento_calendar()` + executor
- **Tua ação:** Google Cloud Service Account (mesmo bloqueio atual) + compartilhar calendário + credentials no Railway
- **Bloqueio:** mesma policy Google Cloud

**Opção C — Email via Gmail** (alternativa simples)
- **Meu trabalho (~2-3h):** OAuth + envio
- **Tua ação:** app password do Gmail ou OAuth setup

### Passo 4 — Alexa Skill + AWS Lambda

**Objetivo final.** Voz mãos livres em casa.

**Meu trabalho (~6-8h):**
1. AWS Lambda Python reusando `memory.py`, `tools.py`, parte do `llm.py`
2. Skill handler (parse intent Alexa → chama pipeline → formata speech)
3. Pattern async pra driblar timeout 8s (progressive response + notificação assíncrona via Proactive API)
4. Skill JSON: invocation name, intents, slots
5. Deploy Lambda (guia de CLI ou upload)
6. `projetos/gus/gus-12-alexa-setup.md` com passo-a-passo

**Tua ação (~1h):**
1. Conta AWS (free tier serve pra começar)
2. Amazon Developer Console
3. Deploy Lambda (guiado)
4. Criar Skill → apontar endpoint pra Lambda ARN
5. Pairing com Echo ou simulador
6. Testar: *"Alexa, abre Gus"* → *"como tá o Phronesis?"*

## Paralelos opcionais (não bloqueiam caminho principal)

| Item | Por que | Quando |
|------|---------|--------|
| Google Drive nativo no ChatGPT | Camada extra de leitura, fallback | Depois de trocar assinatura Plus |
| Claude Chat Project revalidação | 4ª porta do Gus ativa | Quando tiver 5min |
| Health check externo | Avisa se Railway cair | Nunca bloqueante, mas útil |
| Gitleaks hook | Proteção extra contra secrets no commit | Depois |

## Estimativa total restante

| Item | Meu trabalho | Tua ação externa |
|------|--------------|-------------------|
| Volume Railway | 30min | 5min |
| Custom GPT | 3-4h | 20min + criação do GPT |
| Executor 1 ação | 2-3h | 30min + aprovações externas |
| Alexa Skill + Lambda | 6-8h | 1h |

**Total:** ~12-15h código meu + ~2h ação tua + esperas externas

**Cronograma realista:**
- Semana 1 (28/abr): Custom GPT + Volume → Gus com voz no mobile
- Semana 2 (5/mai): Executor 1 tipo + teste real
- Semana 3 (12/mai): Alexa Skill + Lambda
- Semana 4 (19/mai): Polimento, correções, testes em casa

Alternativa: diluir em 1 mês com 1 sessão por semana.

## Decisões em aberto

1. **Próxima sessão — Custom GPT?** (sim, recomendação forte)
2. **Qual executor primeiro?** (Twilio vs Calendar vs Gmail)
3. **Quando atacar volume Railway?** (antes ou junto do Custom GPT)
4. **Drive:** aguarda troca de assinatura Plus (decisão tomada hoje)

## Como usar este documento

- **Começo de cada sessão de dev:** ler aqui pra ver onde estamos no caminho
- **Final de cada sessão:** atualizar o que mudou + próximo passo concreto
- **Complementa** [[_estado-atual]] (handoff operacional) e [[gus-08-plano-proximos-passos]] (itens menores, concluído)

Relacionado: [[gus-01-visao-geral]], [[gus-05-portas-capacidades]], [[gus-06-autonomia-acoes]], [[_estado-atual]]
