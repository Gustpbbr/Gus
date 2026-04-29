---
tipo: demanda
origem: claude-chat
destino: claude-code
prioridade: alta
status: concluido
criado_em: 2026-04-29T10:20:00-03:00
processado_em: 2026-04-29T12:15:00-03:00
processado_por: claude-code
acao_sugerida: criar_novo
destino_path: Dockerfile.mcp
contexto: "Fix urgente: gus-mcp-server falhando no healthcheck. railway.toml aponta para gus.main mas Dockerfile.mcp so copia hub/. Precisa corrigir start command."
---

# Fix: gus-mcp-server healthcheck failure

## Problema

Deploy do gus-mcp-server falha no healthcheck em todos os deploys.
Diagnostico do Railway confirma:

  "Update the start command in railway.toml from python -m gus.main
  to python -m hub.mcp_server. The Docker image built from Dockerfile.mcp
  only copies the hub/ directory, so the gus module does not exist in
  the container and the app crashes immediately."

## O que precisa mudar

Opcao A (preferida): adicionar CMD explicito no Dockerfile.mcp

  No final do Dockerfile.mcp, adicionar:
  CMD ["python", "-m", "hub.mcp_server"]

Opcao B: criar railway.toml especifico para o servico MCP

  [deploy]
  startCommand = "python -m hub.mcp_server"

  Mas isso pode conflitar com o railway.toml existente do bot.

Opcao A e mais limpa -- o Dockerfile ja e especifico do MCP,
faz sentido o start command estar nele.

## Evidencia

Build logs confirmam que o build funciona (imagem buildada com sucesso).
O problema e exclusivamente no start command em runtime.

Healthcheck path: /health
Resposta esperada: {"status": "ok", "service": "gus-hub-mcp"}

## Resultado

Marcada como concluida em batch (limpeza de inbox 29/04).

Obsoleta. CMD já estava no Dockerfile.mcp desde PR #29. Problema real era cache de pip + railway.toml conflitando, resolvido nos PRs #34/#36/#37/#38/#40/#41. Server agora Active e healthcheck passa.
