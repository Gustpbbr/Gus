---
tipo: demanda
origem: claude-chat
destino: claude-code
prioridade: alta
status: concluido
criado_em: 2026-04-30T14:15:00-03:00
processado_em: 2026-05-01T11:35:00-03:00
processado_por: claude-code
acao_sugerida: criar_novo
destino_path: hub/mcp_server.py
contexto: "Fix autenticacao MCP server: claude.ai nao suporta custom header Bearer, so OAuth. Adaptar endpoint /mcp para aceitar conexao inicial sem auth e validar Bearer apenas nas chamadas de tools."
resolucao: "Resolvido via PR #60 (MCP_URL_SECRET no path) em vez de OAuth. claude.ai web só aceita OAuth no UI do Connector (issues #112/#155/#2157 anthropics/claude-ai-mcp). OAuth completo seria overkill (~150 linhas + risco dos bugs conhecidos). Solução pragmática: shared secret in URL — modelo igual webhook Slack/GitHub. MCP_AUTH_DISABLED=true desliga AuthMiddleware, MCP_URL_SECRET monta endpoint em /<secret>/mcp. PR #57 (lifespan) também fixou bug colateral que impedia conexão."
---

# Fix: autenticacao MCP server para funcionar com claude.ai

## Problema

O claude.ai Connectors so suporta dois modos de auth para MCP customizado:
- OAuth (Client ID + Client Secret)
- Sem autenticacao (campos vazios)

Nao ha campo de custom header / Bearer token na UI.
O servidor atual exige Bearer token em TODAS as requisicoes, incluindo
o handshake inicial de descoberta -- por isso o claude.ai rejeita a conexao.

## Solucao recomendada

Separar autenticacao em dois niveis:

1. Endpoint de descoberta (/mcp GET, /.well-known/*) -- SEM autenticacao
   Claude.ai precisa fazer o handshake inicial sem token.

2. Chamadas de tools (/mcp POST) -- COM autenticacao Bearer
   Valida MCP_BEARER_TOKEN apenas quando ha body de tool call.

Isso permite que o claude.ai descubra o servidor sem credenciais
e ainda protege as tools de acesso indevido.

## Alternativa mais simples

Se a solucao acima for complexa, uma alternativa e remover completamente
a autenticacao do servidor por enquanto. O servidor ja roda numa URL
conhecida apenas por Gustavo. Seguranca por obscuridade e suficiente
para uso pessoal no curto prazo.

Depois de validar que o claude.ai conecta, podemos adicionar autenticacao
mais robusta (OAuth) numa proxima iteracao.

## Contexto adicional

Health check funcionando: https://gus-mcp-server-production.up.railway.app/health
URL do MCP: https://gus-mcp-server-production.up.railway.app/mcp
MCP_BEARER_TOKEN esta configurado no Railway como variavel de ambiente.

## Resultado
