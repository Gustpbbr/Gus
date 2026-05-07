Exibir painel de status do sistema Gus. Execute os seguintes passos em paralelo e apresente um resumo compacto:

1. **Git log:** `git log --oneline -10` — últimos commits
2. **Inbox Claude Code:** `ls dialogos/inbox-claude-code/` — demandas pendentes (exclua arquivos que começam com `_`)
3. **Inbox TioGu:** `ls dialogos/inbox-tiogu/ 2>/dev/null` — demandas para o Telegram
4. **Branch atual:** `git branch --show-current` e `git status --short`
5. **Semana atual:** ler `dialogos/streams/semana-2026-05-05.md` se existir, senão listar `dialogos/streams/`

Apresente o resultado neste formato:

```
=== STATUS GUS — <data/hora BRT> ===

Branch: <branch> | <N> arquivo(s) modificado(s)

INBOX CLAUDE CODE (<N> demandas):
  - <arquivo1> [<prioridade se visível>]
  - ...

INBOX TIOGU (<N> demandas):
  - <arquivo1>
  - ...

ÚLTIMOS COMMITS:
  <hash> <mensagem>
  ...

STREAM DA SEMANA: <primeira linha do MD ou "não encontrado">
```

Se o Hub Qdrant não estiver acessível (HUB_READ_TOKEN ausente), indique "(Hub: sem acesso neste ambiente)" sem tentar as tools MCP.
