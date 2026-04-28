---
tipo: setup-porta
porta: telegram
agente: Lua
estimativa: ~2-4h
status: aguardando-decisoes
---

# Setup — Bot Telegram da Lua

Passo a passo pra colocar o bot Telegram da Lua em produção 24/7
no Railway.

> **Pré-requisito:** decisões dos blocos 1-3 do `decisoes-pendentes.md`
> resolvidas (nome do bot, repositório, conta separada, etc.).

---

## Visão geral do que vai existir

```
┌──────────────────┐                ┌─────────────────────┐
│ Telegram         │                │ Railway (24/7)      │
│ @LuaBot          │ ←─ webhook ──→ │ Bot Python rodando  │
│ (criado via      │                │ + dependências      │
│ @BotFather)      │                │ + variáveis env     │
└──────────────────┘                └──────────┬──────────┘
                                                │
                  ┌─────────────────────────────┼──────────────────────────┐
                  │                             │                          │
            ┌─────▼─────┐              ┌────────▼────────┐         ┌───────▼──────┐
            │ Anthropic │              │ Qdrant Cloud    │         │ GitHub vault │
            │ (Claude)  │              │ coleção lua_hub │         │ (Lua repo)   │
            └───────────┘              └─────────────────┘         └──────────────┘
```

---

## Etapa 1 — Criar o bot Telegram

1. **Abrir Telegram → conversar com `@BotFather`**
2. Comando `/newbot`
3. **Nome** do bot (visível pros usuários): `Lua` — ou outro
4. **Username** (precisa terminar em `bot`): `LuaBot`, `LuaPessoal_bot`,
   `MinhaLuaBot` — depende de disponibilidade
5. BotFather retorna **token** no formato `123456789:ABCdefGHI...`
6. **Anotar token em local seguro** (gerenciador de senhas). Será
   `TELEGRAM_BOT_TOKEN` na config.

7. Configurar bot:
   - `/setdescription` — descrição que aparece no perfil
   - `/setabouttext` — texto curto sobre
   - `/setuserpic` — avatar
   - `/setprivacy` → **Enable** (bot só vê mensagens diretas, não em grupos)
   - `/setjoingroups` → **Disable** (bot é pessoal)

8. Pegar o **chat_id** do dono:
   - Mandar `/start` pro novo bot
   - Abrir `https://api.telegram.org/bot<TOKEN>/getUpdates`
   - Procurar campo `"chat":{"id":NÚMERO}` — esse é o `chat_id`
   - **Anotar** chat_id. Será `TELEGRAM_CHAT_ID` na config.

---

## Etapa 2 — Criar contas externas (se ainda não tiver)

Recomendação: **conta nova/coleção nova** pra Lua, separado do agente
existente. Isso permite ver custos da Lua isolados.

| Serviço | Ação | Anotar |
|---|---|---|
| Anthropic | Login console.anthropic.com → API Keys → Create new key (label "Lua") | `ANTHROPIC_API_KEY` |
| Qdrant Cloud | Login cloud.qdrant.io → Cluster (mesmo que outro agente, ou novo) → criar coleção `lua_hub` (ver `memoria/setup-qdrant.md`) | `QDRANT_URL`, `QDRANT_API_KEY` |
| Railway | Login railway.app → New Project | (sem secret aqui ainda) |
| GitHub | Repositório novo `<seu-user>/Lua` (ou pasta dedicada em repo existente) → Settings → Generate Personal Access Token (fine-grained, só este repo) | `GITHUB_TOKEN`, `GITHUB_REPO` |
| Tavily (opcional) | Login tavily.com → API key | `TAVILY_API_KEY` |
| OpenAI (opcional pra Whisper) | platform.openai.com → API key | `OPENAI_API_KEY` |

---

## Etapa 3 — Estrutura do código do bot

Repositório da Lua precisa de (mínimo viável):

```
Lua/                              ← repo dedicado (recomendado) ou pasta
├── lua/                          ← código Python do bot
│   ├── __init__.py
│   ├── main.py                   ← entry point, registra handlers Telegram
│   ├── bot.py                    ← handlers: texto, foto, /start, /reset, etc.
│   ├── llm.py                    ← chama Anthropic API com retry, prompt caching
│   ├── memory.py                 ← buscar/salvar/deletar via hub.store
│   ├── tools.py                  ← schema de tools + dispatcher
│   ├── media.py                  ← processa imagens, PDFs, voz (Whisper)
│   ├── logger.py                 ← log de custos e latência (JSONL)
│   ├── system_prompt.md          ← cópia do projetos/Lua/system-prompts/telegram.md
│   ├── lua-identity.md           ← cópia do projetos/Lua/identidade/lua-identity.md
│   └── principios.md             ← cópia do projetos/Lua/identidade/principios.md
│
├── hub/                          ← Hub Qdrant (lê/escreve no lua_hub)
│   ├── __init__.py
│   ├── store.py                  ← ingestar / lembrar / listar / deletar
│   └── curador.py                ← extração a cada N turnos
│
├── Dockerfile                    ← imagem pra Railway
├── railway.toml                  ← config Railway
├── requirements.txt              ← dependências Python
├── .env.example                  ← template de variáveis
├── .gitignore                    ← protege .env, secrets
└── README.md                     ← doc do repo
```

**Implementação real:** copiar do agente existente (mesmo dono já
tem implementação madura), trocar nome de pacote `gus` → `lua` e
ajustar identidade.

> Esta cópia será feita pela IA implementadora durante implementação.
> Quando chegar a hora, abrir sessão dedicada com Claude Code e pedir
> "implementa o bot da Lua copiando estrutura do agente atual".

---

## Etapa 4 — Variáveis de ambiente no Railway

Configurar no Railway → Project → Variables:

```
ANTHROPIC_API_KEY=sk-ant-...          # Etapa 2
TELEGRAM_BOT_TOKEN=123456789:ABC...   # Etapa 1
TELEGRAM_CHAT_ID=12345678             # Etapa 1
QDRANT_URL=https://xyz.qdrant.io      # Etapa 2
QDRANT_API_KEY=abc...                 # Etapa 2
GITHUB_TOKEN=ghp_...                  # Etapa 2
GITHUB_REPO=usuario/Lua               # Etapa 2

# Opcionais
TAVILY_API_KEY=tvly-...               # busca web
OPENAI_API_KEY=sk-...                 # Whisper transcrição
HARD_LIMIT_USD_MONTH=15               # corta chamadas Anthropic se passar (ajustar)
TURNOS_PARA_RESUMO=3                  # frequência do curador
RATE_LIMIT_MSG_PER_MINUTE=20          # rate limit do bot
```

**NUNCA** colocar essas vars no código ou em arquivos commitados. Só
no painel Railway.

---

## Etapa 5 — Volume persistente Railway

No Railway → Project → Volumes → Create:
- Mount path: `/app/data`
- Tamanho: 1GB inicial (pode crescer)

Esse volume guarda `bot_state.json` (histórico de turnos pra sobreviver
redeploy) e `dimagem_pending.json` (se Lua tiver fluxo OS médica)
ou outros estados.

---

## Etapa 6 — Deploy inicial

1. **Push** do código pro GitHub (`main`)
2. **Conectar** GitHub ao Railway → New Service → Deploy from Repo
3. Railway detecta `Dockerfile` e faz build
4. Quando subir, **conferir logs**: deve aparecer "Bot iniciado..."
5. **Teste**: mandar `/start` no `@LuaBot` (Telegram)
6. Bot deve responder com mensagem de boas-vindas
7. Mandar mensagem qualquer ("oi"). Bot deve responder usando o
   system_prompt da Lua

Se bot não responder:
- Logs Railway mostram erro?
- Token Telegram correto?
- chat_id corresponde ao seu Telegram?
- Anthropic key válida (saldo)?

---

## Etapa 7 — Memória (Hub Qdrant)

Conferir `memoria/setup-qdrant.md`. Resumo:

1. Criar coleção `lua_hub` com 384 dimensões (sentence-transformers
   `all-MiniLM-L6-v2`)
2. Bot lê/escreve nela via `hub.store`
3. Curador automático extrai fragmentos a cada N turnos

Validar: conversar com bot por 6+ mensagens. Curador roda em background
(ver logs). Depois: `search_memory("o que conversamos")` deve trazer
fragmentos.

---

## Etapa 8 — GitHub Actions (cron)

Workflows opcionais (cobertos em `04-governanca-e-saude/`):

- Export diário (3h BRT) — exporta memórias pra `.md` no repo
- Auditoria diária (6h BRT) — gera estatísticas
- Briefing matinal (7h dias úteis) — manda resumo no Telegram
- Health check (7:30h) — alerta se algo quebrou
- Retrospectiva semanal (sex 20h) — sumário da semana
- Reflexão quinzenal (sáb 10h) — auto-questionamento

**Não obrigatório no V1** — adicionar conforme uso real demonstrar
necessidade.

---

## Custos esperados

Operação típica (~50 mensagens/dia + curador a cada 3 turnos):

| Item | Custo/mês |
|---|---|
| Anthropic (Sonnet 4.6 + Haiku 4.5 do curador) | ~US$10–25 |
| Railway runtime | ~US$5 |
| Qdrant Cloud (free tier) | US$0 |
| Telegram Bot API | US$0 |
| **Total** | **~US$15–30/mês** |

Pra reduzir: usar só Haiku no bot (sem Sonnet 4.6), limitar
processamento de imagem, reduzir N turnos do curador.

---

## Pitfalls comuns

### 1. Bot recebe mensagem mas não responde

Causas possíveis:
- Sem créditos Anthropic — verificar console
- Rate limit ativo — aguardar 30s
- `TELEGRAM_CHAT_ID` errado (bot só responde pro chat_id configurado)
- Imagem corrompida — testar com mensagem texto pura

### 2. Memória vazia mesmo após várias conversas

- Curador desabilitado? Conferir env `TURNOS_PARA_RESUMO`
- Erro 400 no curador? Conferir logs (`_log/resumos-mem0/...`)
- Coleção Qdrant errada? Conferir `QDRANT_URL`

### 3. Custos descontrolados

- Configurar `HARD_LIMIT_USD_MONTH` (corta chamadas)
- Conferir `/custo` periodicamente

### 4. `@LuaBot` já existe (alguém pegou o nome)

- Tentar `@LuaBot_pessoal`, `@MinhaLuaBot`, etc.

---

## Versão

| Versão | Data | Mudança |
|---|---|---|
| 0.1-rascunho | 2026-04-28 | Setup inicial baseado em estrutura conhecida do agente irmão |
