---
tipo: demanda
origem: gustavo
destino: claude-code
prioridade: alta
status: parcial
criado_em: 2026-05-02T00:50:00-03:00
processado_em: 2026-05-03T20:15:00-03:00
processado_por: claude-code
acao_sugerida: criar_novo
destino_path: multiplo
contexto: "Consolida pendências relacionadas à porta Claude Chat discutidas na sessão Code de 30/04-02/05. Inclui ativação de URL secret no MCP, recadastro de Connector, decisões da Fase 2 NeuroGus, captura em tempo real (Opção A) e sync Drive. Cobre 6 fronts; cada um com seção própria + leituras necessárias + critério de resolução."
status_parcial:
  - "#1 (URL secret) ✅ feito 02/05/2026"
  - "#2 (Recadastrar Connector) ✅ feito 02/05/2026"
  - "#3 (mock HTML NeuroGus) — pendente Gustavo"
  - "#4 (decisões §11.3-11.5 NeuroGus) — pendente Gustavo"
---

# Demanda — Pendências Claude Chat (consolidação)

## TL;DR

Esta demanda agrupa **4 pendências distintas** relacionadas à porta Claude
Chat (originalmente 6 — itens 5 e 6 resolvidos por outras frentes em
03/05). Próxima aba pode atacar em qualquer ordem — são **independentes**,
mas todas dependem de **decisão do Gustavo antes** de codar.

| # | Pendência | Bloqueio | Quem decide / faz | Estado |
|---|---|---|---|---|
| 1 | Ativar `MCP_URL_SECRET` no Railway | Hub MCP atualmente público | **Gustavo** (operacional Railway) | ✅ feito 02/05/2026 |
| 2 | Recadastrar Connector claude.ai com URL nova `/<secret>/mcp` | Depende do #1 | **Gustavo** (UI claude.ai) | ✅ feito 02/05/2026 |
| 3 | Localizar mock HTML NeuroGus no Drive Claude Chat 28/04 | Bloqueia Fase 2 frontend | **Gustavo** (10min — abrir sessão Chat antiga) | ⏳ pendente |
| 4 | Decidir `?token=` URL, auto-orbit, reconnect SSE (§11.3-11.5) | Bloqueia Fase 2 frontend | **Gustavo** (decisões de design) | ⏳ pendente |

---

## Contexto: estado atual da porta Claude Chat

| Capacidade | Status |
|---|---|
| Connector MCP gus-hub conectado | ✅ funciona em modo público temporário (`MCP_AUTH_DISABLED=true`, sem URL secret) |
| 9 tools MCP listadas + invocáveis | ✅ confirmado por Gustavo (teste `contar_fragmentos`) |
| Captura via .md upload (curador chat ingest) | ✅ **bidirecional + top-tier** desde PR #67 (Sonnet 4.6 + GPT-4o, brain `gustavo` + `gus`) |
| Captura via Drive (Chat → arquivo .md/.gdoc → cron 30min) | ✅ **resolvido em 03/05** (PRs #76 + #79 — WIF + inbox-gustavo/chat) |
| Ler do Drive (`gus-bootstrap.md`, `gus-estado-atual.md`) | ✅ **resolvido em 03/05** (PR #76 — WIF substitui OAuth expirado) |

Já resolvidos antes (não rediscutir):
- PR #57 — lifespan do Starlette wrapper (impedia Connector cadastrar)
- PR #60 — `MCP_URL_SECRET` no path (substitui Bearer que claude.ai web não suporta)
- PR #67 — curador chat bidirecional + bug fix `resultado["sonnet"]`
- PR #76 — Workload Identity Federation (resolve item 6 original) + inbox-chat-raw
- PR #79 — `inbox-gustavo/<porta>/` com auto-frontmatter (resolve item 5 original)

---

## Pendência 1 — Ativar `MCP_URL_SECRET` no Railway

**Por quê:** o MCP server hoje está com `MCP_AUTH_DISABLED=true` e sem URL
secret. Resultado: **qualquer um que descobrir a URL Railway pode ler todo
o Hub** (escrita está bloqueada por código). É vetor oportunista — scanners
varrem `*.up.railway.app`.

**Quem faz:** Gustavo (UI Railway).

**Passos pra Gustavo (Code só guia):**

1. Gerar segredo 32+ chars hex:
   - Celular: https://www.uuidgenerator.net/ → 2 UUIDs → cola sem hífen
   - Terminal: `openssl rand -hex 32`

2. No Railway → projeto Gus → serviço `gus-mcp-server` → **Variables**:
   - **Adicionar** `MCP_URL_SECRET=<segredo>`
   - **Manter** `MCP_AUTH_DISABLED=true` (claude.ai web não suporta Bearer)
   - **Manter** `MCP_BEARER_TOKEN` (não atrapalha — fica latente pra Claude Desktop futuro)

3. Salvar — Railway redeploya em ~2-3min.

**Validação:**
- `https://gus-mcp-server-production.up.railway.app/health` → `{"status":"ok"}`
- `https://.../mcp` → 404 (esperado — agora exige path com secret)
- `https://.../<segredo>/mcp` → resposta MCP (testar via claude.ai depois)

**Leituras pra próxima aba:**
- `projetos/gus/gus-28-passo2-mcp-server.md` — guia setup atualizado
- `hub/mcp_server.py` — `_url_secret()` e `_create_app()`

---

## Pendência 2 — Recadastrar Connector claude.ai

**Por quê:** Connector atual aponta pra `/mcp`. Após ativar URL secret, esse
path retorna 404. Cadastro de Connector no claude.ai web **não é editável**
— precisa deletar e recriar.

**Quem faz:** Gustavo (UI claude.ai).

**Passos pra Gustavo:**

1. claude.ai → **Settings → Connectors**
2. Achar **Gus Hub** → **Remove**
3. **Add custom connector**:
   - Name: `Gus Hub`
   - URL: `https://gus-mcp-server-production.up.railway.app/<MCP_URL_SECRET>/mcp` (substitui `<MCP_URL_SECRET>`)
   - Auth: deixa em branco (claude.ai web não suporta Bearer mesmo)
4. Salva → status verde + 9 tools listadas

**Validação:**
- Conversa nova: "Quantos fragmentos eu tenho no Hub?" → deve chamar `contar_fragmentos()` e retornar número real
- "Salva no hub que eu testei o URL secret hoje" → deve chamar `ingestar_fragmento()` (escrita agora desbloqueada porque há access control via URL secret)

**Leituras:**
- `projetos/gus/gus-28-passo2-mcp-server.md` § Etapa 6

---

## Pendência 3 — Localizar mock HTML NeuroGus

**Por quê:** decisão §11.2 do gus-30. A Claude Chat criou um mock HTML
de validação estética em sessão de 28/04/2026 dentro do Drive privado
dela. Localizar economiza ~2-3h de UI work na Fase 2.

**Quem faz:** Gustavo.

**Passos pra Gustavo:**

1. Abre claude.ai
2. Vai em conversas antigas → procura sessão de 28/04 sobre NeuroGus
3. Pede pro Claude Chat o HTML que ele criou (provavelmente em artifact)
4. Baixa e comita em `projetos/gus/neurogus-mock-2604.html`

**Se não localizar:** Code recria do zero seguindo gus-30 §8 + decisões fechadas em gus-30.1. **Trabalho extra: 2-3h.**

**Critério de decisão:** se Gustavo gastar mais de 15min procurando, abandonar e recriar.

**Leituras pra próxima aba:**
- `projetos/gus/gus-30-neurogus-roadmap.md` § 8 (design visual completo)
- `projetos/gus/gus-30.1-neurogus-decisoes-v0.md` (na branch `claude/neurogus-fase1-backend-sse`)

---

## Pendência 4 — Decisões §11.3, §11.4, §11.5 da Fase 2

**Por quê:** bloqueia frontend NeuroGus (Fase 2). Code não pode codar
sem essas decisões.

**Quem decide:** Gustavo.

**Decisões:**

| ID | Pergunta | Recomendação Code |
|---|---|---|
| §11.3 | `?token=X` na URL aceitável v0? Ou cookie HttpOnly? | **`?token=X`** (você é único user) |
| §11.4 | Auto-orbit ON ou OFF default? | **ON** com pause-on-interaction |
| §11.5 | Reconnect SSE: retoma do Last-Event-ID ou reload completo? | **Reload** (simplicidade) |

Detalhes de tradução em texto comum estão no transcript da sessão Code
de 01/05 — provavelmente já capturado pelo cron e disponível como
fragmento. Se não, releitura recomendada do gus-30 §11.

**Como resolver:**

Gustavo responde 3 perguntas. Code captura em `gus-30.1` (atualizar) ou
nova `gus-30.2`.

**Leituras:**
- `projetos/gus/gus-30-neurogus-roadmap.md` §11.3-11.5
- `projetos/gus/gus-30.1-neurogus-decisoes-v0.md` (branch `claude/neurogus-fase1-backend-sse`)

---

## Pendências 5 e 6 — RESOLVIDAS em 03/05

**5 (Captura em tempo real):** resolvido via PR #79 (`inbox-gustavo/chat/`) +
PR #76 (WIF + cron 15min). Tu salva Google Doc no Drive na pasta certa,
em até 45min (15min import + 30min curador) vira fragmento no Hub.

**6 (Drive sync OAuth → SA):** resolvido via PR #76 (Workload Identity
Federation, mais seguro que SA JSON). Não expira nunca.

---

## Como esta demanda deve ser processada

Sequência sugerida (mas independentes — pode pular):

1. **Pendências 1+2 (URL secret + Connector)** → faça **agora**, é operacional simples e destrava privacidade. ~10min de Gustavo.
2. **Pendência 3 (mock HTML)** → 10min de Gustavo procurar; se não achar, parte pra Pendência 4.
3. **Pendência 4 (decisões Fase 2)** → Gustavo responde 3 perguntas. Code atualiza gus-30.1.

Após cada uma:
- Atualizar frontmatter desta demanda (ou marcar individual no checklist abaixo)
- Mover pra `dialogos/archive/` quando todas as 4 estiverem resolvidas
- Se alguma virar PR, referenciar nesta demanda

---

## Checklist de resolução

- [x] **#1** — `MCP_URL_SECRET` ativado no Railway (validado 03/05 — Connector retornou 1081 fragmentos via `contar_fragmentos`)
- [x] **#2** — Connector recadastrado no claude.ai com URL nova (validado junto com #1)
- [ ] **#3** — Mock HTML localizado OU decidido recriar (Gustavo)
- [ ] **#4** — Decisões §11.3-11.5 respondidas, gus-30.1 atualizado (Gustavo + Code)
- [x] **#5** — Captura tempo real (resolvido via PR #79 — `inbox-gustavo/chat/`)
- [x] **#6** — Drive sync (resolvido via PR #76 — WIF)

---

## Resultado esperado

Quando todas as 4 restantes estiverem ✅:
- Hub privado (URL secret ativo)
- Claude Chat lê Drive sempre atualizado (já resolvido via WIF)
- Frontend NeuroGus pronto pra Fase 2 (mock disponível, decisões fechadas)
- Captura Claude Chat em tempo real funcionando (já resolvido via inbox-gustavo)

Próxima fase: **Fase 2 NeuroGus frontend** (depende de #3 + #4 resolvidos).
