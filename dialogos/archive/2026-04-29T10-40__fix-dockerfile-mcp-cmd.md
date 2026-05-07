---
tipo: demanda
origem: claude-chat
destino: claude-code
prioridade: alta
status: concluido
criado_em: 2026-04-29T10:40:00-03:00
processado_em: 2026-04-29T19:55:00-03:00
processado_por: claude-code
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

## Resultado

Demanda **obsoleta**. CMD `["python", "-m", "hub.mcp_server"]` ja existe no
Dockerfile.mcp desde o PR #29 (criacao inicial do arquivo). Nao havia o que
adicionar.

O problema real do MCP nao foi falta de CMD — foi sequencia de outras
questoes ja resolvidas em PRs separados:
- PR #34: `railway.mcp.toml` separado pro MCP service (vs railway.toml do bot)
- PR #36: Optional[str] → str="" em buscar_hub (FastMCP TypeError)
- PR #37: cache bust marker pra forcar rebuild
- PR #38: pin mcp==1.27.0
- PR #40: bump httpx 0.27.0 → 0.27.2
- PR #41: relaxa pydantic >=2.11

MCP server ficou Active depois disso. Marcando concluido em batch
de limpeza.
