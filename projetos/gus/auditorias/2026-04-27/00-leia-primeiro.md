---
tipo: auditoria-fiscal
parte: 00-de-06
ordem_leitura: 1
gerado_em: 2026-04-27T09:55:00-03:00
gerado_por: claude-code
escopo: origin/main @ 2026-04-27 manhã (snapshot)
status: rascunho-fiscal
---

# Auditoria fiscal — 2026-04-27 manhã

> Documento gerado pela porta **Claude Code** numa sessão dedicada de fiscalização imparcial, não-implementadora. Não toca código de produção. Lê, mapeia, aponta. Decisões e implementações ficam pra sessões seguintes.

---

## Escopo

Mapeamento completo do sistema Gus a partir desta porta:

- Repo `Gustpbbr/Gus` em `origin/main` (191 arquivos, 45 pastas, snapshot de 27/04 manhã)
- Estado vivo via `_log/`, `_indices/_auditoria-mem0.md`, `gus-memoria-export.md`
- Mem0 acessível via MCP `mem0-gus` (com a ressalva crítica do R6)

**Fora do escopo:** Railway runtime real, Drive direct read, Telegram histórico, Qdrant collection direta, conta Mem0 SaaS.

---

## Cobertura — o que foi lido com atenção

**Lido completo:**
- `gus-01-visao-geral.md`, `gus-26-status-consolidado.md`, `_estado-atual.md`
- `dialogos/_bootstrap/{gus-identity,gus-bootstrap}.md`, `dialogos/README.md`
- `CLAUDE.md`, `gus/system_prompt.md`, `gus/meta-memoria.md`
- Código: `gus/main.py`, `gus/llm.py`, `gus/memory.py`, `gus/bot.py`, `gus/tools.py` (TOOLS+dispatcher), `api/server.py`, `api/routes.py`, `api/auth.py`, `api/schemas.py`, `.claude/mcp/{gus_server,mem0_server}.py`
- Workflows: triggers + descrição de cada um (14 arquivos)
- Scripts: docstring/header de cada um (15 arquivos)
- Hooks: `.claude/hooks/{session-start.sh, scan_sensivel.py}`, `.claude/settings.json`, `.mcp.json`
- `_log/resumos-mem0/{2026-04-25, 2026-04-26, 2026-04-27}.md`
- `_indices/_auditoria-mem0.md`, `gus-memoria-export.md` (head)
- Inboxes em `dialogos/` (estado completo)

**Lido parcial (só título + frontmatter + 1ª linha):**
- `gus-02..gus-25` (24 docs)
- Implementação completa de `gus/tools.py` (li só primeiras 250 linhas + nomes de funções)
- `gus/integrations/*` (não li)
- `gus/dimagem.py`, `gus/media.py`, `gus/logger.py`, `gus/resumo_log.py` (não li)
- `api/dashboard.py`, `api/camera.py` (não li)

**Não lido:**
- Roadmap "Hub pre-AGI" detalhado em `gus-15..gus-25`
- `gus-08-plano-proximos-passos.md` (plano técnico A-H)
- `gus-09-guia-uso-diario.md`
- `projetos/gus/reflexoes/2026-W17-reflexao.md`
- `dimagem/dia/*`, `pessoal/*`, `receitas/*`, `capturado/visual/_ultimo.md`

→ **Implicação:** as opiniões sobre arquitetura "Hub pre-AGI" e SELF-1 nesta auditoria são provisionais. Pra opinião informada, preciso ler `gus-15..gus-25` em sessão dedicada.

---

## Ordem de leitura sugerida

1. **Este arquivo** — escopo, cobertura, resumo 60s
2. [[01-mapa-funcional]] — o que o sistema faz, como, em que ordem
3. [[02-inconsistencias-criticas-altas]] — R1 a R8 (o que precisa atenção)
4. [[03-inconsistencias-medias-baixas]] — R9 a R16 (o que vale apontar)
5. [[04-plano-saneamento]] — etapas A-I com ordem e dependências
6. [[05-design-auto-merge]] — discussão sobre auto-merge condicional pra fechar o gap entre porta Claude Code e main
7. [[06-perguntas-abertas]] — decisões que dependem de você

Pode ler na ordem. Ou pular pra `02` direto se quiser ir aos riscos.

---

## Limitações da análise

Coisas que **não consigo verificar** desta porta:

- **Logs reais do Railway** (sem token aqui, sem volume montado) — só leio o que foi commitado em `_log/`
- **Estado real do Qdrant Cloud** — vejo o código que conecta, não o conteúdo
- **Estado real do Mem0 SaaS** — MCP `mem0-gus` aponta pra lá mas não confirmo se ele tá vivo (R6)
- **Drive direto** — vejo scripts, não conteúdo
- **Telegram histórico** — só código do bot
- **Conta Anthropic billing** — vejo pricing, não consumo

O que faço quando não sei: digo que não sei. Princípio fundamental do Gus.

---

## Resumo de uma página (60 segundos)

**O que o Gus é hoje:** sistema multi-portal com Telegram em produção, API Custom GPT pronta aguardando Builder, Claude Chat operando via bootstrap, Claude Code (esta porta) operando via MCPs. Compartilha memória em Qdrant Cloud (204 mems), arquivo .md no GitHub (191 arquivos), espelho no Drive bidirecional dentro de `dialogos/`. 27 docs canônicos cobrindo desde visão até plano "Hub pre-AGI" e Alexa.

**O que está errado agora:**

1. **Curadoria automática do Mem0 quebrada há ~13h** (param `temperature`+`top_p` no Haiku). Conversas do Telegram não viram memória persistente desde 26/04 noite. *Bate com a demanda `2026-04-27T06-16__curadoria-mem0-sonnet-nao-haiku`.*
2. **Split arquitetural** entre Mem0 SaaS (MCP, scripts antigos) e Qdrant self-hosted (bot, API) — risco de auditorias e exports olharem fonte morta.
3. **Pacientes Dimagem vazaram pro Mem0 do Gustavo** (LGPD).
4. **CLAUDE.md e `_estado-atual.md` desatualizados** — sessão nova lê fatos obsoletos.

**O que está certo:** infra sólida (Railway 24/7, Qdrant Cloud, sync bidirecional Drive↔GitHub via `dialogos/`, prompt caching, retry+fallback Sonnet→Haiku, scan PII em duas camadas, hard limit financeiro, brain duplo gus/gustavo, identidade canônica única em `dialogos/_bootstrap/`).

**O que recomendo:** estabilizar (corrigir os 4 críticos, alinhar docs com código) antes de implementar Hub pre-AGI etapas 2-5 ou abrir novas portas. Plano detalhado em [[04-plano-saneamento]].

---

## Ações imediatas recomendadas

1. **Ativar plano [[04-plano-saneamento]]** começando por etapa B (curadoria híbrida — resolve R1 + atende demanda do TioGu).
2. **Mergear o commit `98e8125`** da branch `claude/greeting-checkin-NAcVz` pra ativar archive da demanda `fix-qdrant-search-bug` (etapa A do plano, já feita técnicamente).
3. **Decidir se quer auto-merge condicional** ([[05-design-auto-merge]]) pra resolver de vez o gap "Claude Code escreve em branch, info fica perdida".

---

## Próximos passos pra mim (Claude Code)

Quando você der ordem:

- Se for **B (curadoria híbrida)**: investigo o erro 400 exato + projeto refator + implementação
- Se for **D (migração Qdrant)**: inventário completo `grep MemoryClient` + plano de migração arquivo a arquivo
- Se for **leitura completa do Hub pre-AGI**: leio `gus-15..gus-25` com calma e atualizo esta auditoria com opinião informada
- Se for **estrutura final do projeto**: preciso primeiro ler todos os MDs que faltam (gus-02..gus-25, gus-08, gus-09, integrations/, dimagem.py, etc) antes de propor

---

Relacionado: [[01-mapa-funcional]] · [[02-inconsistencias-criticas-altas]] · [[03-inconsistencias-medias-baixas]] · [[04-plano-saneamento]] · [[05-design-auto-merge]] · [[06-perguntas-abertas]]
