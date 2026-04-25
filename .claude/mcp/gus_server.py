#!/usr/bin/env python3
"""
MCP server `gus` — expõe tools de alto nível do bot pro Claude Code.

Reusa exatamente os módulos que o bot Telegram usa em produção
(`gus.integrations.diagnostico`, `gus.integrations.wikilinks`), garantindo
que toda sessão de Claude Code aberta no repo enxergue o mesmo "estado"
do TioGu.

2 tools expostas inicialmente:
  - auto_diagnostico() — health check de 6 componentes
  - sugerir_wikilinks(arquivo, branch?) — Sonnet propõe wikilinks

CONFIGURAÇÃO:
  As tools precisam de várias env vars. O .mcp.json injeta a partir do
  arquivo ~/.claude/gus.env (formato KEY=VALUE, uma por linha):

    MEM0_API_KEY=m0-...
    ANTHROPIC_API_KEY=sk-ant-...
    GITHUB_TOKEN=ghp_...
    TAVILY_API_KEY=tvly-...           # opcional
    GITHUB_REPO=Gustpbbr/Gus          # opcional, default Gustpbbr/Gus

  Se uma key faltar, a tool retorna erro descritivo (não trava o servidor).

LIMITAÇÕES NO SANDBOX WEB:
  Algumas APIs podem estar bloqueadas no allowlist de hosts do Claude Code
  Web (vimos isso com Railway). Se uma chamada falhar com 'Host not in
  allowlist', a tool vira inerte aqui mas continua funcionando no PC local.
"""

import asyncio
import sys
from pathlib import Path

# Adiciona repo root ao sys.path pra importar gus.*
_REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO_ROOT))

from gus.integrations.diagnostico import auto_diagnostico
from gus.integrations.wikilinks import sugerir_wikilinks

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("gus")


@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="auto_diagnostico",
            description=(
                "Roda health check paralelo dos componentes externos do Gus: "
                "GitHub PAT, Mem0 (com frescor da última memória), Anthropic API, "
                "Tavily, volume Railway, workflows GH. Retorna tabela markdown "
                "com OK/WARN/ERROR por linha. Use quando quiser saber 'tá tudo "
                "funcionando?' antes de operações sensíveis. Sem inputs."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="sugerir_wikilinks",
            description=(
                "Lê um arquivo .md do repo e sugere wikilinks pra outros arquivos "
                "relacionados via Sonnet. NÃO modifica o arquivo — só retorna "
                "sugestões pro Gustavo aprovar. Critério rigoroso: só conexões "
                "temáticas substantivas, ignora proximidade temporal/pasta. "
                "Custo ~$0.017 por chamada."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "arquivo": {
                        "type": "string",
                        "description": "Path do arquivo no repo (ex: 'dimagem/dia/2026-04-25.md', 'pessoal/saude/historico-saude.md'). Pode omitir extensão .md.",
                    },
                    "branch": {
                        "type": "string",
                        "description": "Nome do branch. Omita pra ler do main.",
                    },
                },
                "required": ["arquivo"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "auto_diagnostico":
        try:
            resultado = await auto_diagnostico()
            return [TextContent(type="text", text=resultado)]
        except Exception as e:
            return [TextContent(type="text", text=f"Erro em auto_diagnostico: {e}")]

    if name == "sugerir_wikilinks":
        arquivo = arguments.get("arquivo", "").strip()
        branch = arguments.get("branch")
        if not arquivo:
            return [TextContent(type="text", text="argumento `arquivo` vazio.")]
        try:
            resultado = await sugerir_wikilinks(arquivo, branch)
            return [TextContent(type="text", text=resultado)]
        except Exception as e:
            return [TextContent(type="text", text=f"Erro em sugerir_wikilinks: {e}")]

    return [TextContent(type="text", text=f"Tool desconhecida: {name}")]


async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
