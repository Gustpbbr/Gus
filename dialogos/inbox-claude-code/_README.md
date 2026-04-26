# Inbox — Claude Code

Demandas que **Claude Code** (web ou local no PC) deve processar.

## Quem escreve aqui

- **Claude Chat** via Drive
- **TioGu Telegram** via `save_to_github`
- **Custom GPT** via API
- **Gustavo** manual

## Quem lê aqui

- **Claude Code** — sessão lê `inbox-claude-code/` no SessionStart
  (a implementar no hook); por enquanto Gustavo aponta na conversa

## Frontmatter

Ver `dialogos/README.md`.

## Tipos típicos de demanda pra Claude Code

- Implementar feature/fix de código
- Refatorar arquivo X
- Criar workflow Y
- Editar documentação Z
- Investigar bug

## Após processar

1. `status: concluido`, `processado_em`, `processado_por: claude-code`
2. Mover pra `archive/`
3. Resultado no corpo: commit hash, branch, link do PR (se houver)
