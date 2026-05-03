"""Dispatcher central de tools — `executar_tool(name, inputs)`.

Recebe nome da tool + dict de inputs e roteia pra implementação real.
Usado pelo loop tool-calling em `gus.llm.gerar_resposta`.

Nomes precisam casar com `name` em `gus.tools.schemas.TOOLS` (sem isso
o LLM chama uma tool e o dispatcher devolve "Tool desconhecida").
"""

from gus.memory import (
    buscar_memorias_detalhada,
    salvar_observacao_gus,
    buscar_memorias_gus,
    deletar_memoria as _deletar_memoria,
)
from gus.integrations.railway import logs_railway as _logs_railway
from gus.integrations.diagnostico import auto_diagnostico as _auto_diagnostico
from gus.integrations.wikilinks import sugerir_wikilinks as _sugerir_wikilinks
from gus.integrations.pesquisa import (
    pesquisar_pubmed as _pesquisar_pubmed,
    pesquisar_arxiv as _pesquisar_arxiv,
)
from gus.integrations.openai_chat import perguntar_gpt as _perguntar_gpt

from gus.tools.github import (
    _read_from_github,
    _list_github_directory,
    _list_branches,
    _list_commits,
    _save_to_github,
    _disparar_workflow,
)
from gus.tools.web import _search_web
from gus.tools.acoes import _criar_acao


async def executar_tool(name: str, inputs: dict) -> str:
    if name == "read_from_github":
        return await _read_from_github(inputs["path"], inputs.get("branch"))
    elif name == "list_github_directory":
        return await _list_github_directory(inputs.get("path", ""), inputs.get("branch"))
    elif name == "list_branches":
        return await _list_branches()
    elif name == "list_commits":
        return await _list_commits(
            inputs.get("path", ""),
            inputs.get("limit", 10),
            inputs.get("since_days", 0)
        )
    elif name == "search_memory":
        try:
            limit = max(1, min(int(inputs.get("limit", 10)), 20))
        except (TypeError, ValueError):
            limit = 10
        return await buscar_memorias_detalhada(inputs["query"], limit)
    elif name == "search_web":
        return await _search_web(inputs["query"])
    elif name == "pesquisar_pubmed":
        return await _pesquisar_pubmed(
            inputs["query"],
            inputs.get("max_n", 10),
            inputs.get("since_year"),
        )
    elif name == "pesquisar_arxiv":
        return await _pesquisar_arxiv(
            inputs["query"],
            inputs.get("max_n", 10),
            inputs.get("categoria"),
        )
    elif name == "perguntar_gpt":
        return await _perguntar_gpt(
            inputs["query"],
            inputs.get("modelo", "gpt-5-mini"),
        )
    elif name == "save_to_github":
        return await _save_to_github(
            inputs["filename"],
            inputs["content"],
            inputs.get("folder", "capturado")
        )
    elif name == "criar_acao":
        return await _criar_acao(
            inputs["tipo"],
            inputs["conteudo"],
            bool(inputs.get("alto_risco", False))
        )
    elif name == "meta_memoria":
        return await _read_from_github("gus/meta-memoria.md")
    elif name == "auditoria_hub":
        return await _read_from_github("_indices/_auditoria-hub.md")
    elif name == "salvar_memoria_gus":
        return await salvar_observacao_gus(inputs["observacao"])
    elif name == "buscar_memoria_gus":
        try:
            limit = max(1, min(int(inputs.get("limit", 10)), 20))
        except (TypeError, ValueError):
            limit = 10
        return await buscar_memorias_gus(inputs["query"], limit)
    elif name == "deletar_memoria":
        return await _deletar_memoria(
            inputs["memory_id"],
            inputs.get("user_id", "gustavo"),
        )
    elif name == "disparar_workflow":
        return await _disparar_workflow(
            inputs["workflow_name"],
            inputs.get("branch", "main")
        )
    elif name == "logs_railway":
        return await _logs_railway(
            inputs.get("linhas", 50),
            inputs.get("filtro"),
            inputs.get("since_min"),
        )
    elif name == "auto_diagnostico":
        return await _auto_diagnostico()
    elif name == "sugerir_wikilinks":
        return await _sugerir_wikilinks(
            inputs["arquivo"],
            inputs.get("branch"),
        )
    elif name == "rotear_arquivo":
        from gus.roteador import rotear_arquivo as _rotear
        return await _rotear(
            inputs["source_path"],
            inputs["destino_path"],
            inputs["acao"],
        )
    return f"Tool desconhecida: {name}"
