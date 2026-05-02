---
tipo: demanda
origem: gustavo
destino: claude-code
prioridade: alta
status: pendente
criado_em: 2026-05-02T00:50:00-03:00
processado_em: ""
processado_por: ""
acao_sugerida: criar_novo
destino_path: multiplo
contexto: "Consolida pendências relacionadas à porta Claude Chat discutidas na sessão Code de 30/04-02/05. Inclui ativação de URL secret no MCP, recadastro de Connector, decisões da Fase 2 NeuroGus, captura em tempo real (Opção A) e sync Drive. Cobre 6 fronts; cada um com seção própria + leituras necessárias + critério de resolução."
---

# Demanda — Pendências Claude Chat (consolidação)

## TL;DR

Esta demanda agrupa **6 pendências distintas** relacionadas à porta Claude
Chat, todas discutidas em sessões Code recentes (30/04 a 02/05/2026).
Próxima aba pode atacar em qualquer ordem — são **independentes**, mas
algumas dependem de **decisão do Gustavo antes** de codar.

| # | Pendência | Bloqueio | Quem decide / faz |
|---|---|---|---|
| 1 | Ativar `MCP_URL_SECRET` no Railway | Hub MCP atualmente público | **Gustavo** (operacional Railway) |
| 2 | Recadastrar Connector claude.ai com URL nova `/<secret>/mcp` | Depende do #1 | **Gustavo** (UI claude.ai) |
| 3 | Localizar mock HTML NeuroGus no Drive Claude Chat 28/04 | Bloqueia Fase 2 frontend | **Gustavo** (10min — abrir sessão Chat antiga) |
| 4 | Decidir `?token=` URL, auto-orbit, reconnect SSE (§11.3-11.5) | Bloqueia Fase 2 frontend | **Gustavo** (decisões de design) |
| 5 | Captura em tempo real Claude Chat (Opção A da multi-porta) | Captura depende de upload manual de .md hoje | **Code** implementa após Gustavo aprovar |
| 6 | Drive sync OAuth → Service Account | Bootstrap stale no Chat | **Gustavo** + **Code** (ver demanda separada) |

---

## Contexto: estado atual da porta Claude Chat

| Capacidade | Status |
|---|---|
| Connector MCP gus-hub conectado | ✅ funciona em modo público temporário (`MCP_AUTH_DISABLED=true`, sem URL secret) |
| 9 tools MCP listadas + invocáveis | ✅ confirmado por Gustavo (teste `contar_fragmentos`) |
| Captura via .md upload (curador chat ingest) | ✅ **bidirecional + top-tier** desde PR #67 (Sonnet 4.6 + GPT-4o, brain `gustavo` + `gus`) |
| Captura em tempo real durante conversa | ❌ não existe — só após upload manual |
| Ler do Drive (`gus-bootstrap.md`, `gus-estado-atual.md`) | ⚠️ **stale** — sync OAuth quebrado há semanas |

Já resolvidos antes (não rediscutir):
- PR #57 — lifespan do Starlette wrapper (impedia Connector cadastrar)
- PR #60 — `MCP_URL_SECRET` no path (substitui Bearer que claude.ai web não suporta)
- PR #67 — curador chat bidirecional + bug fix `resultado["sonnet"]`

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

## Pendência 5 — Captura em tempo real Claude Chat (Opção A)

**Por quê:** PR #67 fez o curador chat bidirecional, **mas só processa
.md uploadados manualmente**. Captura em tempo real durante a conversa
(quando você fala algo importante e quer que o Hub veja na hora) **não
existe**.

**Opção A** da demanda `2026-05-01-captura-multiporta-curador.md`: adicionar
seção em `dialogos/_bootstrap/gus-bootstrap.md` instruindo Claude Chat a
chamar `mcp__gus-hub__ingestar_fragmento` quando detectar decisão /
preferência / fato relevante durante a conversa.

**Trade-offs:**
- ✅ Funciona já (MCP gus-hub conectado, tool disponível)
- ✅ Captura em tempo real, sem upload manual
- ⚠️ Qualidade depende do prompt — pode salvar lixo ou ignorar coisa importante
- ⚠️ Sem comparação Haiku × GPT como o curador post-hoc tem

**Quem decide:** Gustavo (vale o esforço dado que PR #67 já cobre 80% via
upload manual?).

**Quem implementa:** Code (~30 linhas no bootstrap).

**Como resolver (se Gustavo aprovar):**

1. Adicionar seção em `dialogos/_bootstrap/gus-bootstrap.md` com:
   - Tabela de tipos (gus-18) e quando salvar cada
   - Sintaxe da tool `mcp__gus-hub__ingestar_fragmento`
   - Cadência sugerida + quando NÃO salvar
2. Pedir confirmação: cobre 2 brains (`gustavo` + `gus`) — bidirecional
3. Mirror automático pro Drive via workflow existente
4. Validar em conversa nova: "salva no hub que..." → confere fragmento criado

**Leituras:**
- `dialogos/inbox-claude-code/2026-05-01-captura-multiporta-curador.md` (demanda original)
- `CLAUDE.md` § "AVISO IMPORTANTE — Captura de memória da porta Code quebrada" (analogia: captura proativa via MCP **falha** no Code por env vars; no Chat funciona porque o MCP gus-hub roda em servidor separado com env vars)
- `hub/mcp_server.py` — tool `ingestar_fragmento` (linha ~211)
- `dialogos/_bootstrap/gus-bootstrap.md` — onde inserir a nova seção

**Critério de sucesso:**
- Bootstrap atualizado, mirror Drive sincroniza
- Conversa nova Chat: pedir explicitamente "salva no hub..." → fragmento criado com `via=claude-chat` no Hub
- 1 semana depois: revisar fragmentos `via=claude-chat` no Hub — qualidade aceitável?

---

## Pendência 6 — Drive sync OAuth → Service Account

**Por quê:** workflow `sync-to-drive.yml` parou de empurrar GitHub→Drive.
Hipótese: refresh token Google OAuth expirado (apps "Testing" expiram em
7 dias). Resultado: Claude Chat lê Drive **stale** — bootstrap, estado-atual
todos desatualizados.

**Demanda separada já criada:** `dialogos/inbox-claude-code/2026-05-01-drive-sync-oauth-fix.md`.

**Resumo das opções:**
- **Opção 1:** reset OAuth — paliativo, expira de novo em 7 dias
- **Opção 2:** Service Account — definitivo, não expira (recomendado)
- **Opção 3:** aposentar Drive sync, Chat lê tudo via MCP (`read_repo_file`)

**Quem decide:** Gustavo. **Quem implementa:** Code (Opção 2 = ~30min código + Gustavo cria SA no Google Console).

**Leituras:**
- `dialogos/inbox-claude-code/2026-05-01-drive-sync-oauth-fix.md`
- `.github/scripts/sync_to_drive.py`
- `.github/workflows/sync-to-drive.yml`

---

## Como esta demanda deve ser processada

Sequência sugerida (mas independentes — pode pular):

1. **Pendências 1+2 (URL secret + Connector)** → faça **agora**, é operacional simples e destrava privacidade. ~10min de Gustavo.
2. **Pendência 6 (Drive sync)** → curto código, destrava bootstrap atualizado pro Chat. Code implementa após Gustavo decidir Opção 1/2/3.
3. **Pendência 3 (mock HTML)** → 10min de Gustavo procurar; se não achar, parte pra Pendência 4.
4. **Pendência 4 (decisões Fase 2)** → Gustavo responde 3 perguntas. Code atualiza gus-30.1.
5. **Pendência 5 (Opção A captura tempo real)** → Gustavo decide se vale; Code implementa em ~30 linhas.

Após cada uma:
- Atualizar frontmatter desta demanda (ou marcar individual no checklist abaixo)
- Mover pra `dialogos/archive/` quando todas as 6 estiverem resolvidas
- Se alguma virar PR, referenciar nesta demanda

---

## Checklist de resolução

- [ ] **#1** — `MCP_URL_SECRET` ativado no Railway (Gustavo)
- [ ] **#2** — Connector recadastrado no claude.ai com URL nova (Gustavo)
- [ ] **#3** — Mock HTML localizado OU decidido recriar (Gustavo)
- [ ] **#4** — Decisões §11.3-11.5 respondidas, gus-30.1 atualizado (Gustavo + Code)
- [ ] **#5** — Decidida Opção A; se sim, bootstrap atualizado (Gustavo + Code)
- [ ] **#6** — Drive sync OAuth → Service Account migrado (Gustavo + Code)

---

## Resultado esperado

Quando todas as 6 estiverem ✅:
- Hub privado (URL secret ativo)
- Claude Chat lê Drive sempre atualizado
- Frontend NeuroGus pronto pra Fase 2 (mock disponível, decisões fechadas)
- Captura Claude Chat em tempo real funcionando (se Opção A aprovada)

Próxima fase: **Fase 2 NeuroGus frontend** (depende de #3 + #4 resolvidos).
