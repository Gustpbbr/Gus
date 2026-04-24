---
tipo: estado-atual-sessao
atualizado: 2026-04-24
---

# Estado atual — handoff entre sessões

Documento vivo. Atualizar no final de cada sessão que deixa algo no meio.

## Última sessão (2026-04-23/24) — maratona Fase 1 + reforços

### Deploy e bot vivo
- Railway com todas as variáveis. `TELEGRAM_CHAT_ID=495256549`. Bot responde, usa Mem0, salva/lê no GitHub.
- 12 testes funcionais validados em produção via Telegram.

### Correções críticas
- **Bug 1 (data):** `datetime.now(BRT)` injetado no system prompt a cada chamada (`3b8178f`).
- **Bug 2 (busca):** Tavily primário + DuckDuckGo fallback (`5d82769`).
- **Bug 3 (repo):** nome `Gustpbbr/Gus` declarado no system prompt (`0360f80`).
- **Bug 4 (descoberta):** tool `list_github_directory` adicionada (`0360f80`).
- **Bug workflow export-mem0:** pin `mem0ai==0.1.29` (`2a3829b`) + `permissions: contents: write` (`1370d2e`). Validado, 12 memórias exportadas (`26fd5d0`).

### Features novas (8 tools no total)
- `read_from_github` (original)
- `list_github_directory` (descoberta, `0360f80`)
- `list_commits` (histórico/datas/autoria, `71e27b8`)
- `search_memory` (busca ativa Mem0, `009d25b` → `f69f71b` pós-rebase)
- `search_web` (Tavily + DDG)
- `save_to_github` com scan de dados sensíveis (`0b3a31e`)

### Infraestrutura de memória e documentação
- **7 MDs de documentação** em `projetos/gus/gus-01` a `gus-07` (`6edbec5`).
- **`gus-08-plano-proximos-passos.md`** — detalhamento técnico de 8 itens pendentes (`358cc5f`).
- **`_estado-atual.md`** — este handoff, atualizado no fim de cada sessão.
- **`_indices/`** — 7 índices MOC por área (master, saude, financeiro, projetos, dimagem, receitas, capturado) + README com regras de manutenção (`0b3a31e`).
- **`sensivel/`** — pasta excluída do Drive sync com README de regras (`0b3a31e`).
- **`system_prompt.md`** orquestra: ler `_estado-atual.md` primeiro, manter índices sincronizados, proteger dados sensíveis, quando usar cada tool.

### Mem0
- Chave rotacionada: antiga `m0-obYXul...` revogada, nova `m0-cfOtGO...` ativa em Railway + GitHub Secrets + `~/.claude/mem0.key`.
- **Resumo extrativo a cada 5 turnos** (commit `5f4ffe8`) — sistema chama Claude Haiku pra extrair só decisões/preferências/fatos novos dos últimos 10 msgs e salva curado no Mem0.
- MCP server `mem0-gus` configurado via `.mcp.json` lê chave de `~/.claude/mem0.key`. Testado nesta sessão: listar_memorias, buscar_memorias, salvar_memoria disponíveis.

### Resiliência
- Retry exponencial (1s, 2s, 4s, 8s) para erros Anthropic 5xx/529 (`0e964e0`).
- Fallback pro Haiku quando Sonnet overloaded (`0e964e0`), alias curto `claude-haiku-4-5` (`d89c7c1`).
- Logging detalhado de erros 4xx não-retryables antes de propagar.
- Mensagem amigável ao usuário quando tudo falha: *"A API tá sobrecarregada agora (status X). Tenta em 1-2 min."*

### Bloqueios e decisões
- **Drive sync:** política da organização `iam.disableServiceAccountKeyCreation` no Google Cloud barra criação de JSON keys. Alternativas: desligar policy (requer `roles/orgpolicy.policyAdmin`) ou Workload Identity Federation. Não atacado nesta sessão.
- **Obsidian:** adiado por decisão do Gustavo (Windows, único usuário, mas sem tempo).
- **Claude Chat Project:** criado, mas os 4 testes de validação falharam — provavelmente `gus-identity.md` não foi colado em Project Instructions. Precisa refazer.

### Sincronia
`main` e `claude/initial-setup-iWTfL` alinhadas no commit `358cc5f`.

## Pendente pra próxima sessão

### Combo 1 — local (recomendado começar aqui)
Itens que **não dependem de ação externa**: atualizar doc (**G** — ✅ feito agora), rate limit (**A**), backup JSON Mem0 (**B**), guia de uso (**H**), esqueleto fila ações (**F**), comando `/custo` (**E**). Ver [[gus-08-plano-proximos-passos]].

### Combo 2 — automações proativas
Briefing matinal (**C**) + retrospectiva semanal (**D**). Requer adicionar 3 secrets no GitHub: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `ANTHROPIC_API_KEY` (mesma key da Anthropic).

### Decisões pendentes de Gustavo
1. **Drive sync:** desligar policy, usar WIF, ou ficar sem? Impacta Claude Chat Project vivo.
2. **Claude Chat Project:** refazer validação com `gus-identity.md` colado corretamente.
3. **Volume Railway pra `logs/`:** sem isso, `HARD_LIMIT_USD_MONTH` pode ser burlado em redeploy e tracking de custo fica resetado.

## Bugs em aberto (não bloqueantes)
- Gus ocasionalmente usa emojis apesar do tom do system prompt.
- DDG pode falhar se Tavily estourar limite mensal (fallback reativo).
- Mem0 falhas são silenciadas no bot (`bot.py` logger.warning) — sem alerta visível se chave fica inválida.

## Como usar este arquivo

1. Próxima sessão: ler este MD primeiro, depois [[gus-08-plano-proximos-passos]] se tiver intenção clara de avançar.
2. Se precisar de contexto amplo, puxa [[gus-01-visao-geral]].
3. Ao final da sessão: atualizar seção "Última sessão" com o que rolou.
4. Commit + push antes de encerrar.

Relacionado: [[gus-01-visao-geral]], [[gus-02-implementado]], [[gus-03-configuracao-manual]], [[gus-08-plano-proximos-passos]]
