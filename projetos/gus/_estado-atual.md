---
tipo: estado-atual-sessao
atualizado: 2026-04-24
---

# Estado atual — handoff entre sessões

Documento vivo. Atualizar no final de cada sessão que deixa algo no meio.

## Última sessão (2026-04-23/24)

### O que foi concluído

**Deploy e bot vivo:**
- Railway com todas as variáveis. `TELEGRAM_CHAT_ID=495256549`. Bot responde, usa Mem0, salva/lê no GitHub.

**Correções críticas após testes reais:**
- Data correta no system prompt (commit `3b8178f`) — `datetime.now(BRT)` a cada chamada.
- Tavily como busca primária (commit `5d82769`) com DuckDuckGo como fallback — resolve rate limit de DDG em IPs cloud.

**Documentação estruturada:**
- 7 MDs em `projetos/gus/gus-01` a `gus-07` (commit `6edbec5`).
- Este `_estado-atual.md` pra handoff entre sessões.

**Chave Mem0 rotacionada:**
- Antiga (`m0-obYXul...`) revogada.
- Nova (`m0-cfOtGO...`) ativa em: Railway (bot), GitHub Secrets (Action export), `~/.claude/mem0.key` (MCP local).

**Workflow `export-mem0` validado:**
- Pin de `mem0ai==0.1.29` (commit `2a3829b`) — mesmo bug de versão que bateu no MCP local.
- `permissions: contents: write` (commit `1370d2e`) — sem isso, git push em Action falha com exit 128.
- Última run verde em 2026-04-24, exportou 12 memórias do Gustavo → `gus-memoria-export.md` em `main` (commit `26fd5d0`).

**MCP Mem0 configurado (não testado nesta sessão):**
- `.mcp.json` lê chave de `~/.claude/mem0.key` (commit `47ee86f`).
- `mem0ai==0.1.29` pinado em `.claude/mcp/requirements.txt`.
- Harness desta sessão cacheou a config antiga no boot — mudanças no `.mcp.json` durante a sessão só surtem efeito na próxima.

**Bot descobre arquivos e sabe o nome do repo (commit `0360f80`):**
- Adicionado tool `list_github_directory(path)` — bot pode explorar o repo em vez de chutar paths.
- `system_prompt.md` atualizado com: nome explícito `Gustpbbr/Gus`, instrução pra ler `_estado-atual.md` antes de responder sobre estado do projeto, índice dos 7 MDs de documentação.
- Validado em conversa real: bot listou os 8 arquivos em `projetos/gus/`, confirmou repo e deu resumo correto do estado.

**Tentativa de Drive sync abortada nesta sessão:**
- Política da organização `iam.disableServiceAccountKeyCreation` bloqueia criação de JSON keys no Google Cloud (security-by-default pro org `gustavo-pratti-org`).
- Não tentamos Workload Identity Federation (overkill por agora).
- Drive sync fica **parado** até Gustavo desligar a política OU migrar pra WIF.

**Obsidian adiado:**
- Conceitualmente aceito, mas Gustavo prefere não instalar no PC por agora.
- Volta em outra sessão quando quiser visualização local.

**Claude Chat Project parcialmente feito:**
- Criado Project "Gus" em `claude.ai`.
- Os 4 testes de validação (projetos ativos, estilo de comunicação, ferramentas, o que é o Gus) **falharam** — possivelmente o conteúdo do `gus-identity.md` não foi colado corretamente no campo **Project instructions**. Precisa refazer.
- Integração Drive no Project depende de Drive sync estar vivo (bloqueado acima).

**Sincronia de branches:** `main` e `claude/initial-setup-iWTfL` sincronizadas no commit `0360f80`.

### O que ficou pendente pra próxima sessão

Em ordem de desbloqueio:

1. **Validar MCP Mem0 no Claude Code** (teste rápido) — chamar `mcp__mem0-gus__listar_memorias`, deve retornar 12+ memórias.
2. **Refazer Claude Chat Project** — garantir que `gus/gus-identity.md` foi colado no campo **Project instructions** (não como anexo), rodar os 4 testes novamente.
3. **Decidir destino do Drive sync** — desligar política org, tentar WIF, ou ficar sem Drive (e sem Projeto integrado com arquivos vivos).

### Ideias em discussão (não implementadas)

- **Índices MOC** (Map of Content) em `_indices/` — um `.md` por área (saúde, financeiro, projetos, etc) funcionando como dashboard vivo com estado atual + timeline + wikilinks pros arquivos detalhados. Pressupõe o bot atualizar esses índices automaticamente quando salvar algo novo. Discutido nesta sessão; **não criado ainda**. Requer Drive sync funcionando pra fazer sentido pro Claude Chat.

### Próximos passos em aberto (Fase 1)

- ✅ Passo 4 (MCP Claude Code) — configurado; falta teste em nova sessão.
- 🚧 Passo 3 (Drive sync) — bloqueado por política Google.
- ⏸️ Passo 5 (Obsidian) — adiado por decisão.
- 🚧 Passo 6 (Claude Chat Project) — config parcial, retestar.

### Bugs fechados nesta sessão

- ✅ Bug 1: data atual alucinada → fix injetando `datetime.now(BRT)` no system prompt (commit `3b8178f`).
- ✅ Bug 2: DuckDuckGo rate-limited em IPs cloud → Tavily primário (commit `5d82769`).
- ✅ Bug 3: bot não sabia o nome do repo → declarado no system prompt (commit `0360f80`).
- ✅ Bug 4: bot não conseguia descobrir arquivos → novo tool `list_github_directory` (commit `0360f80`).
- ✅ Bug workflow `export-mem0`: pin mem0ai (`2a3829b`) + permissions write (`1370d2e`). Validado com 12 memórias exportadas.

### Bugs conhecidos em aberto

Nenhum crítico. Observações:

- Gus usa emojis em respostas ocasionalmente (não proibido no system prompt; decisão aberta).
- DDG pode falhar quando Tavily estourar limite mensal; fallback reativo apenas.
- Telegram bot silencia falhas de Mem0 (`bot.py:52-55`) — se chave ficar inválida, conversas seguem sem memória mas sem erro visível. Monitorar.
- Bot não conhece histórico de commits (não há tool `list_commits` ainda). Se perguntado "o que mudou essa semana" ele não tem resposta precisa sem consultar múltiplos arquivos.

### Decisões pendentes (não bloqueiam)

- Ordem entre Drive sync, Obsidian, Claude Chat — Gustavo decide por uso real.
- Quando começar Fase 2 (scan de dados sensíveis, backup Mem0, rate limiting) — depende de quando Gus começar a ser usado de verdade.

## Como usar este arquivo

1. Próxima sessão: ler este MD primeiro, depois seguir [[gus-01-visao-geral]] se precisar de contexto mais amplo
2. Ao final da sessão: atualizar a seção "Última sessão" com data nova, concluído, pendente
3. Commit + push antes de encerrar

Relacionado: [[gus-01-visao-geral]], [[gus-02-implementado]], [[gus-03-configuracao-manual]]
