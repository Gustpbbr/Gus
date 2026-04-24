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

**Sincronia de branches:** `main` e `claude/initial-setup-iWTfL` sincronizadas no commit `1370d2e`. Commit `26fd5d0` só em `main` (é auto do bot; próxima sessão faz sync se precisar).

### O que ficou pendente pra próxima sessão

**Validar MCP Mem0** — primeira coisa pra fazer na próxima sessão. Testar chamando `mcp__mem0-gus__listar_memorias`. Resposta esperada: lista das 12 memórias do Gustavo (mesmo conteúdo que tá em `gus-memoria-export.md`). Se der erro "Invalid API Key": ler `~/.claude/mem0.key`, comparar prefixo com a chave do Railway; se estiver diferente, tem dessincronia.

### Próximos passos em aberto (Fase 1)

Depois de validar MCP:

- **Passo 3 — Google Drive sync** (30min, precisa criar Service Account no Google Cloud + secrets `GOOGLE_CREDENTIALS` e `DRIVE_ROOT_FOLDER_ID` no GitHub). Detalhes em `gus-03-configuracao-manual.md` seção 3.
- **Passo 5 — Obsidian local** (20min, fora do Claude Code)
- **Passo 6 — Claude Chat Project** (5min, fora do Claude Code)

### Bugs conhecidos em aberto

Nenhum crítico. Observações:

- Gus usa emojis em respostas ocasionalmente (não proibido no system prompt; decisão aberta).
- DDG pode falhar quando Tavily estourar limite mensal; fallback reativo apenas.
- Telegram bot silencia falhas de Mem0 (bot.py:52-55) — se chave ficar inválida, conversas seguem sem memória mas sem erro visível. Monitorar.

### Decisões pendentes (não bloqueiam)

- Ordem entre Drive sync, Obsidian, Claude Chat — Gustavo decide por uso real.
- Quando começar Fase 2 (scan de dados sensíveis, backup Mem0, rate limiting) — depende de quando Gus começar a ser usado de verdade.

## Como usar este arquivo

1. Próxima sessão: ler este MD primeiro, depois seguir [[gus-01-visao-geral]] se precisar de contexto mais amplo
2. Ao final da sessão: atualizar a seção "Última sessão" com data nova, concluído, pendente
3. Commit + push antes de encerrar

Relacionado: [[gus-01-visao-geral]], [[gus-02-implementado]], [[gus-03-configuracao-manual]]
