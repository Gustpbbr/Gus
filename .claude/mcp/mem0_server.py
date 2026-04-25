#!/usr/bin/env python3
"""
MCP server que expõe Mem0 como ferramenta do Claude Code.

Paridade com as tools do bot Telegram (TioGu) — toda sessão de Claude Code
no repo Gus enxerga as mesmas memórias e tem as mesmas ações disponíveis.

7 tools expostas:
  Brain `gustavo` (fatos sobre o Gustavo):
    - buscar_memorias(query, limit=10)        — search semântico, retorna IDs
    - salvar_memoria(conteudo)                 — adiciona memória
    - listar_memorias(limit=50)                — get_all com IDs

  Brain `gus` (auto-observações do agente):
    - buscar_memorias_gus(query, limit=10)     — search semântico no brain gus
    - salvar_memoria_gus(observacao)           — adiciona ao brain gus
    - listar_memorias_gus(limit=50)            — get_all do brain gus

  Geral:
    - deletar_memoria(memory_id, user_id?)     — IRREVERSÍVEL, exige ID exato

Todos os retornos de busca/lista trazem `[uuid] texto` pra facilitar uso
encadeado com deletar_memoria.

CONFIGURAÇÃO:
  Variável de ambiente MEM0_API_KEY obrigatória. O .mcp.json atual injeta via
  `cat ~/.claude/mem0.key` — o Gustavo precisa criar esse arquivo manualmente
  com a chave (uma vez, fora do repo).
"""

import asyncio
import os
import sys

from mem0 import MemoryClient
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

USER_GUSTAVO = "gustavo"
USER_GUS = "gus"

# Tag de origem — identifica que esta porta gerou a memória.
# Default 'claude-code' porque este MCP roda dentro do Claude Code.
# Pode ser sobrescrito via MEM0_VIA_TAG no env (ex: 'claude-code-web' vs
# 'claude-code-local' se quiser distinguir). Veja gus-12-portas-futuras.md.
VIA_TAG = os.environ.get("MEM0_VIA_TAG", "claude-code")

server = Server("mem0-gus")
_client = None


def get_client() -> MemoryClient:
    global _client
    if _client is None:
        api_key = os.environ.get("MEM0_API_KEY")
        if not api_key:
            raise ValueError(
                "MEM0_API_KEY não definido. Crie ~/.claude/mem0.key com a chave "
                "ou exporte a variável de ambiente."
            )
        _client = MemoryClient(api_key=api_key)
    return _client


def _normalize_results(results) -> list[dict]:
    """SDK do Mem0 às vezes retorna list, às vezes dict com 'memories'/'results'.
    Normaliza pra list[dict] sempre."""
    if isinstance(results, dict):
        return results.get("memories") or results.get("results") or []
    if isinstance(results, list):
        return results
    return []


def _fmt_lista(mems: list[dict], header: str) -> str:
    if not mems:
        return f"{header}: nenhuma memória encontrada."
    linhas = [f"{header}: {len(mems)} memórias\n"]
    for r in mems:
        if not isinstance(r, dict):
            continue
        mem = (r.get("memory") or "").strip()
        mem_id = r.get("id") or "?"
        if mem:
            linhas.append(f"- [{mem_id}] {mem}")
    return "\n".join(linhas)


@server.list_tools()
async def list_tools():
    return [
        # ============= BRAIN GUSTAVO =============
        Tool(
            name="buscar_memorias",
            description=(
                "Busca memórias do Gustavo no Mem0 (brain `gustavo`). Use pra obter "
                "contexto pessoal, preferências, histórico de decisões, projetos ativos. "
                "Retorna até `limit` memórias com seus IDs no formato `[uuid] texto` — o "
                "ID é necessário pra `deletar_memoria` se algo precisar ser removido."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Busca em linguagem natural (ex: 'projetos ativos', 'saúde recente', 'preferências de comunicação')",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Número máximo de memórias (1 a 30). Default 10.",
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="salvar_memoria",
            description=(
                "Salva uma observação sobre o Gustavo no brain `gustavo`. Use quando "
                "aprender algo novo sobre preferências, decisões, contexto pessoal "
                "que deveria persistir entre sessões."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "conteudo": {
                        "type": "string",
                        "description": "Observação a salvar (ex: 'Gustavo prefere crítica direta, não suaviza problemas')",
                    }
                },
                "required": ["conteudo"],
            },
        ),
        Tool(
            name="listar_memorias",
            description=(
                "Lista todas as memórias do brain `gustavo` (até `limit`) com IDs. Use "
                "pra ter visão geral do que o Mem0 sabe sobre o Gustavo, ou pra "
                "encontrar IDs candidatos a deletar."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Máximo de memórias (1 a 100). Default 50.",
                    }
                },
            },
        ),
        # ============= BRAIN GUS =============
        Tool(
            name="buscar_memorias_gus",
            description=(
                "Busca nas memórias OPERACIONAIS do próprio Gus (brain `gus`). Esse "
                "brain guarda padrões observados pelo agente sobre o Gustavo, "
                "aprendizados táticos, princípios emergidos. Diferente de "
                "`buscar_memorias` (que é fatos sobre o Gustavo)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Query semântica (ex: 'como agir com Gustavo', 'padrões observados', 'caveats de tools')",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Máximo (1 a 30). Default 10.",
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="salvar_memoria_gus",
            description=(
                "Salva no brain `gus` (auto-observação do agente). Use com moderação: "
                "padrões operacionais sobre o Gustavo que afetam como agir, "
                "aprendizados sobre tools, princípios emergidos. NÃO usar pra fatos "
                "sobre o Gustavo (esses vão em `salvar_memoria`)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "observacao": {
                        "type": "string",
                        "description": "Observação operacional (ex: 'tool X tem caveat Y', 'Gustavo descarta superlativos')",
                    }
                },
                "required": ["observacao"],
            },
        ),
        Tool(
            name="listar_memorias_gus",
            description=(
                "Lista memórias do brain `gus` (auto-observações). Útil pra revisar o "
                "que o agente acumulou sobre si mesmo e seus padrões."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Máximo (1 a 100). Default 50.",
                    }
                },
            },
        ),
        # ============= DELETE =============
        Tool(
            name="deletar_memoria",
            description=(
                "DELETA uma memória do Mem0 pelo ID. AÇÃO IRREVERSÍVEL. Use SOMENTE "
                "após o Gustavo confirmar explicitamente qual memória deletar. Fluxo "
                "recomendado: (1) `buscar_memorias` ou `listar_memorias` retornam IDs "
                "no formato `[uuid] texto`; (2) mostre ao Gustavo e pergunte qual; "
                "(3) só após resposta clara, chame com o `memory_id` exato. NUNCA "
                "chame em loop sem perguntar entre cada exclusão."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "memory_id": {
                        "type": "string",
                        "description": "UUID exato da memória (retornado entre colchetes pelas tools de busca/listagem).",
                    },
                    "user_id": {
                        "type": "string",
                        "description": "Brain alvo: 'gustavo' (default) ou 'gus'. Use 'gus' só se o pedido for explicitamente sobre apagar do brain de auto-observação.",
                    },
                },
                "required": ["memory_id"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        client = get_client()
    except ValueError as e:
        return [TextContent(type="text", text=str(e))]

    # ============= BRAIN GUSTAVO =============
    if name == "buscar_memorias":
        query = arguments["query"]
        limit = max(1, min(int(arguments.get("limit", 10)), 30))
        results = await asyncio.to_thread(
            client.search, query, user_id=USER_GUSTAVO, limit=limit
        )
        mems = _normalize_results(results)
        return [TextContent(type="text", text=_fmt_lista(mems, f"Brain `gustavo` — query='{query}'"))]

    if name == "salvar_memoria":
        conteudo = arguments["conteudo"]
        await asyncio.to_thread(
            client.add,
            [{"role": "user", "content": conteudo}],
            user_id=USER_GUSTAVO,
            metadata={"via": VIA_TAG},
        )
        return [TextContent(type="text", text=f"Salvo no brain `gustavo` (via={VIA_TAG}): {conteudo[:120]}")]

    if name == "listar_memorias":
        limit = max(1, min(int(arguments.get("limit", 50)), 100))
        results = await asyncio.to_thread(
            client.get_all, user_id=USER_GUSTAVO, page=1, page_size=limit
        )
        mems = _normalize_results(results)
        return [TextContent(type="text", text=_fmt_lista(mems, "Brain `gustavo`"))]

    # ============= BRAIN GUS =============
    if name == "buscar_memorias_gus":
        query = arguments["query"]
        limit = max(1, min(int(arguments.get("limit", 10)), 30))
        results = await asyncio.to_thread(
            client.search, query, user_id=USER_GUS, limit=limit
        )
        mems = _normalize_results(results)
        return [TextContent(type="text", text=_fmt_lista(mems, f"Brain `gus` — query='{query}'"))]

    if name == "salvar_memoria_gus":
        observacao = arguments["observacao"]
        await asyncio.to_thread(
            client.add,
            [{"role": "user", "content": observacao}],
            user_id=USER_GUS,
            metadata={"via": VIA_TAG},
        )
        return [TextContent(type="text", text=f"Salvo no brain `gus` (via={VIA_TAG}): {observacao[:120]}")]

    if name == "listar_memorias_gus":
        limit = max(1, min(int(arguments.get("limit", 50)), 100))
        results = await asyncio.to_thread(
            client.get_all, user_id=USER_GUS, page=1, page_size=limit
        )
        mems = _normalize_results(results)
        return [TextContent(type="text", text=_fmt_lista(mems, "Brain `gus`"))]

    # ============= DELETE =============
    if name == "deletar_memoria":
        memory_id = (arguments.get("memory_id") or "").strip()
        user_id = arguments.get("user_id", USER_GUSTAVO)
        if not memory_id:
            return [TextContent(type="text", text="memory_id vazio.")]
        try:
            await asyncio.to_thread(client.delete, memory_id=memory_id)
            return [TextContent(type="text", text=f"Deletada: `{memory_id}` (brain `{user_id}`)")]
        except Exception as e:
            return [TextContent(type="text", text=f"Erro ao deletar `{memory_id}`: {e}")]

    return [TextContent(type="text", text=f"Tool desconhecida: {name}")]


async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
