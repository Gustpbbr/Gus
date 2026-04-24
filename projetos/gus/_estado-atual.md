---
tipo: estado-atual-sessao
atualizado: 2026-04-24
---

# Estado atual — handoff entre sessões

Documento vivo. Atualizar no final de cada sessão que deixa algo no meio.

## Última sessão (2026-04-23/24)

### O que foi concluído

- **Deploy no Railway** com todas as variáveis (TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID=495256549, ANTHROPIC_API_KEY, MEM0_API_KEY, GITHUB_TOKEN, GITHUB_REPO, TAVILY_API_KEY)
- **Bot do Telegram ativo** — responde com contexto, usa Mem0, salva/lê no GitHub
- **Fix da data atual** (commit `3b8178f`) — injeta `datetime.now(BRT)` no system prompt a cada chamada
- **Tavily como busca primária** (commit `5d82769`) com DuckDuckGo como fallback — resolve rate limit de IPs cloud
- **7 MDs de documentação** em `projetos/gus/gus-01` a `gus-07` (commit `6edbec5`)
- **MCP Mem0 configurado** via `.mcp.json` na raiz (commit `3cf06e5`), pin `mem0ai==0.1.29` e auto-install (commit `f8e9089`)
- Branch `claude/initial-setup-iWTfL` e `main` sincronizadas até `5d82769`. Commits `3cf06e5` e `f8e9089` ainda só em `claude/initial-setup-iWTfL` — são mudanças de dev tooling (MCP), não afetam Railway.

### O que ficou pendente pra próxima sessão

**Testar o MCP Mem0 nesta sessão nova.** O processo do server anterior foi morto manualmente. Nova sessão deve spawnar o server com mem0ai 0.1.29 (versão pinada). Testar:

1. Chamar `mcp__mem0-gus__listar_memorias` — deve retornar memórias reais do user `gustavo`
2. Se funcionar, MCP tá validado e passo 4 da Fase 1 fica concluído
3. Se der erro de novo, investigar se a chave ainda é injetada pelo harness (check via `cat /proc/<pid>/environ`)

### Próximos passos em aberto (Fase 1)

Depois de validar MCP:

- **Passo 3 — Google Drive sync** (30min, precisa criar Service Account no Google Cloud)
- **Passo 5 — Obsidian local** (20min, fora do Claude Code)
- **Passo 6 — Claude Chat Project** (5min, fora do Claude Code)

### Bugs conhecidos em aberto

Nenhum crítico. Observações menores:

- Gus usa emojis em respostas ocasionalmente (não é proibido explícito no system prompt; decisão em aberto se vale restringir)
- DDG pode falhar quando Tavily estourar limite mensal; hoje é só fallback reativo

### Decisões pendentes (não bloqueiam)

- Qual deveria ser a ordem entre Drive sync, Obsidian, Claude Chat — Gustavo decide por uso real
- Quando começar Fase 2 (scan de dados sensíveis, backup Mem0, rate limiting) — depende de quando Gus começar a ser usado de verdade

## Como usar este arquivo

1. Próxima sessão: ler este MD primeiro, depois seguir [[gus-01-visao-geral]] se precisar de contexto mais amplo
2. Ao final da sessão: atualizar a seção "Última sessão" com data nova, concluído, pendente
3. Commit + push antes de encerrar

Relacionado: [[gus-01-visao-geral]], [[gus-02-implementado]], [[gus-03-configuracao-manual]]
