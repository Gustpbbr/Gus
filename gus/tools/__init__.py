"""
Pacote `gus.tools` — tools expostas ao LLM (Anthropic e OpenAI).

Splittado em 2026-05-03 (item C3 do plano de saneamento). Antes:
arquivo monolítico `gus/tools.py` (1140 linhas com schemas + 6 grupos
de funções + dispatcher). Agora:

  - schemas.py     — TOOLS (lista de schemas Anthropic-style)
  - _utils.py      — _validar_path, _escanear_sensivel, BRT
  - github.py      — read/list/save/list_branches/list_commits/disparar_workflow
  - web.py         — search_tavily/ddg/web (Tavily primário + fallback)
  - acoes.py       — criar_acao (fila acoes/pendentes/)
  - dispatcher.py  — executar_tool (roteia name → função)

Re-exports preservam API antiga (`from gus.tools import TOOLS`,
`from gus.tools import _read_from_github`, etc.) — não quebra nenhum
caller existente:
  - .github/scripts/gerar_lista_tools.py
  - api/routes.py
  - gus/llm.py
  - gus/resumo_log.py
  - gus/integrations/dimagem.py
  - tests/test_tools.py
"""

# Schemas (TOOLS list pra Anthropic + OpenAI tool calling)
from gus.tools.schemas import TOOLS

# Dispatcher
from gus.tools.dispatcher import executar_tool

# Utilitários (testes acessam diretamente)
from gus.tools._utils import (
    BRT,
    _validar_path,
    _escanear_sensivel,
)

# GitHub functions (api/routes, resumo_log, dimagem importam direto)
from gus.tools.github import (
    _read_from_github,
    _list_github_directory,
    _list_branches,
    _list_commits,
    _save_to_github,
    _disparar_workflow,
)

# Web functions (api/routes importa _search_web)
from gus.tools.web import (
    _search_tavily,
    _search_ddg,
    _search_web,
)

# Ações
from gus.tools.acoes import _criar_acao

# Compat: PATTERNS_SENSIVEIS era acessível como `gus.tools._PATTERNS_SENSIVEIS`
# antes do split — mantemos o re-export pra não quebrar callers.
from gus.patterns_sensiveis import PATTERNS_SENSIVEIS as _PATTERNS_SENSIVEIS


__all__ = [
    # Public API principal
    "TOOLS", "executar_tool",
    # Utilitários
    "BRT", "_validar_path", "_escanear_sensivel",
    "_PATTERNS_SENSIVEIS",
    # GitHub
    "_read_from_github", "_list_github_directory", "_list_branches",
    "_list_commits", "_save_to_github", "_disparar_workflow",
    # Web
    "_search_tavily", "_search_ddg", "_search_web",
    # Ações
    "_criar_acao",
]
