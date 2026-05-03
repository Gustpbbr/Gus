#!/usr/bin/env python3
"""
MCP server `mem0-gus` — expõe o Hub Qdrant pra Claude Code (esta porta).

NOTA HISTÓRICA: o nome do server e do arquivo é 'mem0' por razões de
retrocompatibilidade (assim Claude Code Web e .mcp.json continuam
funcionando sem mudança). Internamente, usa o Hub Qdrant direto via
hub/store.py — NÃO mais Mem0 SaaS (ADR-001 Fase 5 / R6).

Paridade com o bot Telegram: toda sessão Claude Code no repo Gus enxerga
as mesmas memórias do `gus_hub` e tem as mesmas ações disponíveis.

7 tools expostas:
  Brain `gustavo` (fatos sobre o Gustavo):
    - buscar_memorias(query, limit=10)        — busca semântica via hub.lembrar
    - salvar_memoria(conteudo)                 — adiciona via hub.ingestar
    - listar_memorias(limit=50)                — listagem direta via hub.listar

  Brain `gus` (auto-observações do agente):
    - buscar_memorias_gus(query, limit=10)     — idem, user_id='gus'
    - salvar_memoria_gus(observacao)           — idem
    - listar_memorias_gus(limit=50)            — idem

  Geral:
    - deletar_memoria(memory_id, user_id?)     — IRREVERSÍVEL, exige ID exato

Todos os retornos de busca/lista trazem `[uuid] texto` pra facilitar uso
encadeado com deletar_memoria.

CONFIGURAÇÃO:
  Variáveis de ambiente (tipicamente carregadas de ~/.claude/gus.env):
    QDRANT_URL         — endpoint do cluster Qdrant Cloud
    QDRANT_API_KEY     — chave do cluster
    ANTHROPIC_API_KEY  — só pra fallback ou debug; Hub não chama LLM em leitura

  Mais MEM0_API_KEY OPCIONAL — se presente E o Hub falhar (problema de
  conexão), pode-se ativar fallback Mem0 SaaS (não implementado por padrão
  porque ADR-001 aposenta o SaaS).
"""

import asyncio
import os
import sys
from pathlib import Path

# Adiciona repo root ao sys.path pra importar hub.*
_REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO_ROOT))

from hub.store import ingestar, lembrar, listar, deletar
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

USER_GUSTAVO = "gustavo"
USER_GUS = "gus"

# Tag de origem — toda escrita por esta porta é tagueada como 'claude-code'
VIA_TAG = os.environ.get("MEM0_VIA_TAG", "claude-code")

server = Server("mem0-gus")


def _fmt_lista(mems: list[dict], header: str) -> str:
    if not mems:
        return f"{header}: nenhuma memória encontrada."
    linhas = [f"{header}: {len(mems)} memórias\n"]
    for r in mems:
        if not isinstance(r, dict):
            continue
        mem = (r.get("conteudo") or "").strip()
        mem_id = r.get("id") or "?"
        if mem:
            # Linha com tags pra facilitar inspeção visual
            tags = []
            if r.get("tipo"):
                tags.append(r["tipo"])
            if r.get("area"):
                tags.append(r["area"])
            tag_str = f"[{'/'.join(tags)}] " if tags else ""
            linhas.append(f"- [{mem_id}] {tag_str}{mem}")
    return "\n".join(linhas)


@server.list_tools()
async def list_tools():
    return [
        # ============= BRAIN GUSTAVO =============
        Tool(
            name="buscar_memorias",
            description=(
                "Busca semântica no Hub Qdrant brain `gustavo`. Use pra obter "
                "contexto pessoal, preferências, histórico de decisões, projetos "
                "ativos sobre o Gustavo. Retorna até `limit` fragmentos com IDs "
                "no formato `[uuid] [tipo/area] texto` — o ID é necessário pra "
                "`deletar_memoria` se algo precisar ser removido."
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
                        "description": "Número máximo de fragmentos (1 a 30). Default 10.",
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="salvar_memoria",
            description=(
                "Salva fato/observação sobre o Gustavo no Hub brain `gustavo`. "
                "Use quando aprender algo novo sobre preferências, decisões, "
                "contexto pessoal que deveria persistir entre sessões. Tag "
                "automática: via='claude-code'.\n\n"
                "Classifique adequadamente via params opcionais: `tipo` "
                "(decisao | preferencia | biografico | fato | meta_reflexao | "
                "etc, default 'fato') e `camada_temporal` (permanente | rotina | "
                "semana | sessao | momento, default 'rotina'). Sem essa "
                "classificação, busca semântica e ego_cache perdem sinal."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "conteudo": {
                        "type": "string",
                        "description": "Texto auto-suficiente do fragmento (ex: 'Gustavo prefere crítica direta, não suaviza problemas')",
                    },
                    "tipo": {
                        "type": "string",
                        "description": "Tipo do fragmento (gus-18). Aceita: identidade_operacional, biografico, emocional, decisao, procedural, rotina, meta_reflexao, conexao_emergente, episodico, cronologico, fato, preferencia, lacuna, projeto. Default: 'fato'.",
                    },
                    "camada_temporal": {
                        "type": "string",
                        "description": "Permanência esperada. Aceita: momento, sessao, semana, rotina, permanente. Default: 'rotina'.",
                    },
                    "area": {
                        "type": "string",
                        "description": "Área canônica: gus, saude, financeiro, projetos, pessoal, dimagem, pesquisa, receitas, esportes. Vazio se não se aplica.",
                    },
                },
                "required": ["conteudo"],
            },
        ),
        Tool(
            name="listar_memorias",
            description=(
                "Lista fragmentos do Hub brain `gustavo` (até `limit`) com IDs. "
                "Use pra ter visão geral do que o Hub tem sobre o Gustavo, ou "
                "pra encontrar IDs candidatos a deletar. Sem busca semântica — "
                "lista por scroll."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Máximo de fragmentos (1 a 100). Default 50.",
                    }
                },
            },
        ),
        # ============= BRAIN GUS =============
        Tool(
            name="buscar_memorias_gus",
            description=(
                "Busca nas memórias OPERACIONAIS do próprio Gus (Hub brain `gus`). "
                "Esse brain guarda padrões observados pelo agente sobre o Gustavo, "
                "aprendizados táticos, princípios emergidos, decisões arquiteturais "
                "e marcos evolutivos do sistema. Diferente de `buscar_memorias` "
                "(fatos sobre o Gustavo)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Query semântica (ex: 'como agir com Gustavo', 'decisões arquiteturais', 'caveats de tools')",
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
                "Salva no Hub brain `gus` (auto-observação do agente). Use com "
                "moderação: padrões operacionais, aprendizados sobre tools, "
                "princípios emergidos, decisões arquiteturais. NÃO usar pra fatos "
                "sobre o Gustavo (esses vão em `salvar_memoria`). Tag automática: "
                "via='claude-code', area='gus'.\n\n"
                "Classifique via params opcionais: `tipo` "
                "(decisao | meta_reflexao | procedural | identidade_operacional, "
                "default 'meta_reflexao') e `camada_temporal` (permanente para "
                "princípios duros, rotina para padrões observados, default "
                "'rotina')."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "observacao": {
                        "type": "string",
                        "description": "Observação operacional auto-suficiente (ex: 'tool X tem caveat Y', 'Gustavo descarta superlativos')",
                    },
                    "tipo": {
                        "type": "string",
                        "description": "Default 'meta_reflexao'. Aceita também: decisao, procedural, identidade_operacional, conexao_emergente, lacuna.",
                    },
                    "camada_temporal": {
                        "type": "string",
                        "description": "Default 'rotina'. Use 'permanente' pra princípios estruturais.",
                    },
                },
                "required": ["observacao"],
            },
        ),
        Tool(
            name="listar_memorias_gus",
            description=(
                "Lista fragmentos do Hub brain `gus` (auto-observações). Útil pra "
                "revisar o que o agente acumulou sobre si mesmo e seus padrões."
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
                "DELETA um fragmento do Hub Qdrant pelo ID. AÇÃO IRREVERSÍVEL. "
                "Use SOMENTE após o Gustavo confirmar explicitamente qual fragmento "
                "deletar. Fluxo recomendado: (1) `buscar_memorias` ou `listar_memorias` "
                "retornam IDs no formato `[uuid] texto`; (2) mostre ao Gustavo e "
                "pergunte qual; (3) só após resposta clara, chame com o `memory_id` "
                "exato. NUNCA chame em loop sem perguntar entre cada exclusão."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "memory_id": {
                        "type": "string",
                        "description": "UUID exato do fragmento (retornado entre colchetes pelas tools de busca/listagem).",
                    },
                    "user_id": {
                        "type": "string",
                        "description": "Brain alvo: 'gustavo' (default) ou 'gus'. Usado apenas pra mensagem de retorno — Hub identifica fragmento pelo UUID único.",
                    },
                },
                "required": ["memory_id"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    # ============= BRAIN GUSTAVO =============
    if name == "buscar_memorias":
        query = arguments["query"]
        limit = max(1, min(int(arguments.get("limit", 10)), 30))
        try:
            mems = await asyncio.to_thread(lembrar, query, USER_GUSTAVO, limit)
        except Exception as e:
            return [TextContent(type="text", text=f"Erro ao buscar no Hub: {e}")]
        return [TextContent(type="text", text=_fmt_lista(mems, f"Hub `gustavo` — query='{query}'"))]

    if name == "salvar_memoria":
        conteudo = arguments["conteudo"]
        # Params opcionais (item 1.4) — caller classifica em vez de hardcode
        tipo = arguments.get("tipo") or "fato"
        camada = arguments.get("camada_temporal") or "rotina"
        area = arguments.get("area") or ""
        try:
            frag_id = await asyncio.to_thread(
                ingestar,
                conteudo,
                {
                    "tipo": tipo,
                    "camada_temporal": camada,
                    "area": area,
                    "via": VIA_TAG,
                    "user_id": USER_GUSTAVO,
                    "confianca": 0.8,
                },
            )
            tag_info = f"tipo={tipo}/camada={camada}"
            if area:
                tag_info += f"/area={area}"
            return [TextContent(type="text", text=f"Salvo no Hub `gustavo` ({tag_info}, id={frag_id[:8]}): {conteudo[:120]}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Erro ao salvar no Hub: {e}")]

    if name == "listar_memorias":
        limit = max(1, min(int(arguments.get("limit", 50)), 100))
        try:
            mems = await asyncio.to_thread(listar, USER_GUSTAVO, limit)
        except Exception as e:
            return [TextContent(type="text", text=f"Erro ao listar Hub: {e}")]
        return [TextContent(type="text", text=_fmt_lista(mems, "Hub `gustavo`"))]

    # ============= BRAIN GUS =============
    if name == "buscar_memorias_gus":
        query = arguments["query"]
        limit = max(1, min(int(arguments.get("limit", 10)), 30))
        try:
            mems = await asyncio.to_thread(lembrar, query, USER_GUS, limit)
        except Exception as e:
            return [TextContent(type="text", text=f"Erro ao buscar no Hub: {e}")]
        return [TextContent(type="text", text=_fmt_lista(mems, f"Hub `gus` — query='{query}'"))]

    if name == "salvar_memoria_gus":
        observacao = arguments["observacao"]
        # Params opcionais (item 1.4) — brain gus default 'meta_reflexao'
        tipo = arguments.get("tipo") or "meta_reflexao"
        camada = arguments.get("camada_temporal") or "rotina"
        try:
            frag_id = await asyncio.to_thread(
                ingestar,
                observacao,
                {
                    "tipo": tipo,
                    "camada_temporal": camada,
                    "area": "gus",
                    "via": VIA_TAG,
                    "user_id": USER_GUS,
                    "confianca": 0.8,
                },
            )
            return [TextContent(type="text", text=f"Salvo no Hub `gus` (tipo={tipo}/camada={camada}, id={frag_id[:8]}): {observacao[:120]}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Erro ao salvar no Hub: {e}")]

    if name == "listar_memorias_gus":
        limit = max(1, min(int(arguments.get("limit", 50)), 100))
        try:
            mems = await asyncio.to_thread(listar, USER_GUS, limit)
        except Exception as e:
            return [TextContent(type="text", text=f"Erro ao listar Hub: {e}")]
        return [TextContent(type="text", text=_fmt_lista(mems, "Hub `gus`"))]

    # ============= DELETE =============
    if name == "deletar_memoria":
        memory_id = (arguments.get("memory_id") or "").strip()
        user_id = arguments.get("user_id", USER_GUSTAVO)
        if not memory_id:
            return [TextContent(type="text", text="memory_id vazio.")]
        try:
            # Motivo automático pra trilha de auditoria (item 1.3)
            motivo = f"mcp:{VIA_TAG} user_id={user_id}"
            await asyncio.to_thread(deletar, memory_id, motivo)
            return [TextContent(type="text", text=f"Deletado do Hub: `{memory_id}` (brain `{user_id}`)")]
        except Exception as e:
            return [TextContent(type="text", text=f"Erro ao deletar `{memory_id}`: {e}")]

    return [TextContent(type="text", text=f"Tool desconhecida: {name}")]


async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
