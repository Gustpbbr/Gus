#!/usr/bin/env python3
"""
MCP server que expõe Mem0 como ferramenta do Claude Code.
Permite que sessões do Claude Code acessem a mesma memória do Gus.
"""

import asyncio
import json
import os
import sys

from mem0 import MemoryClient
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

USER_ID = "gustavo"

server = Server("mem0-gus")
_client = None


def get_client():
    global _client
    if _client is None:
        api_key = os.environ.get("MEM0_API_KEY")
        if not api_key:
            raise ValueError("MEM0_API_KEY não definido")
        _client = MemoryClient(api_key=api_key)
    return _client


@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="buscar_memorias",
            description=(
                "Busca memórias do Gustavo no Mem0. Use para obter contexto pessoal, "
                "preferências, histórico de decisões, projetos ativos, e qualquer coisa "
                "que o Gus já tenha aprendido sobre o Gustavo."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Busca em linguagem natural (ex: 'projetos ativos', 'preferências de comunicação', 'saúde')"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="salvar_memoria",
            description=(
                "Salva uma observação sobre o Gustavo no Mem0. Use quando aprender algo "
                "novo sobre preferências, decisões, padrões de trabalho, ou contexto pessoal "
                "que o Gus deveria lembrar em futuras conversas."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "conteudo": {
                        "type": "string",
                        "description": "Observação a salvar (ex: 'Gustavo prefere respostas em tópicos numerados')"
                    }
                },
                "required": ["conteudo"]
            }
        ),
        Tool(
            name="listar_memorias",
            description=(
                "Lista todas as memórias armazenadas do Gustavo no Mem0. "
                "Use para ter uma visão geral do que o Gus já sabe."
            ),
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    client = get_client()

    if name == "buscar_memorias":
        query = arguments["query"]
        results = await asyncio.to_thread(
            client.search, query, user_id=USER_ID, limit=10
        )
        if not results:
            return [TextContent(type="text", text="Nenhuma memória encontrada.")]
        lines = [f"- {r['memory']}" for r in results]
        return [TextContent(type="text", text="\n".join(lines))]

    elif name == "salvar_memoria":
        conteudo = arguments["conteudo"]
        messages = [{"role": "user", "content": conteudo}]
        await asyncio.to_thread(client.add, messages, user_id=USER_ID)
        return [TextContent(type="text", text=f"Memória salva: {conteudo}")]

    elif name == "listar_memorias":
        results = await asyncio.to_thread(client.get_all, user_id=USER_ID)
        if not results:
            return [TextContent(type="text", text="Nenhuma memória armazenada.")]
        lines = [f"- {r['memory']}" for r in results]
        return [TextContent(
            type="text",
            text=f"{len(results)} memórias:\n\n" + "\n".join(lines)
        )]

    return [TextContent(type="text", text=f"Tool desconhecida: {name}")]


async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
