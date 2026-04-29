---
tipo: demanda
origem: claude-chat
destino: claude-code
prioridade: alta
status: pendente
criado_em: 2026-04-29T10:40:00-03:00
processado_em: ""
processado_por: ""
acao_sugerida: criar_novo
destino_path: Dockerfile.mcp
contexto: "Fix gus-mcp-server: adicionar CMD no Dockerfile.mcp. NAO mexer no railway.toml (quebra o bot Telegram)"
---

# Fix: gus-mcp-server -- CMD no Dockerfile.mcp

## Contexto

O PR #33 tentou corrigir o start command via railway.toml mas quebrou o bot
Telegram. O PR #35 reverteu. O railway.toml eh compartilhado entre os dois
servicos -- qualquer mudanca no startCommand afeta os dois.

## Solucao correta

Adicionar CMD explicito no Dockerfile.mcp. O Dockerfile.mcp ja e especifico
do MCP server -- o start command deve estar nele, nao no railway.toml.

No final do Dockerfile.mcp, adicionar:

  CMD ["python", "-m", "hub.mcp_server"]

Isso sobrescreve qualquer startCommand do railway.toml para o container MCP.
O bot Telegram nao e afetado porque usa o Dockerfile principal (nao o .mcp).

## O que NAO fazer

NAO mexer no railway.toml -- qualquer mudanca ali afeta o bot Telegram.

## Validacao

Apos o fix e novo deploy, healthcheck em:
https://<dominio>.up.railway.app/health
Resposta esperada: {"status": "ok", "service": "gus-hub-mcp"}

## Resultado
