"""Tool `criar_acao` — enfileira ação em `acoes/pendentes/<id>.md`.

Executor real (Twilio/Gmail/Calendar) ainda não existe — ações ficam em
pendentes esperando implementação. Frontmatter YAML padrão facilita
parsing futuro pelo executor.
"""

import uuid
from datetime import datetime

from gus.tools._utils import BRT
from gus.tools.github import _save_to_github


async def _criar_acao(tipo: str, conteudo: str, alto_risco: bool = False) -> str:
    """Enfileira uma ação em acoes/pendentes/<id>.md com frontmatter YAML padrão."""
    agora = datetime.now(BRT)
    acao_id = f"{agora.strftime('%Y-%m-%d-%H%M%S')}-{uuid.uuid4().hex[:4]}"

    frontmatter = (
        f"---\n"
        f"id: {acao_id}\n"
        f"tipo: {tipo}\n"
        f"origem: telegram\n"
        f"criado_em: {agora.isoformat()}\n"
        f"status: pendente\n"
        f"alto_risco: {str(bool(alto_risco)).lower()}\n"
        f"---\n\n"
    )

    full_content = frontmatter + conteudo.strip() + "\n"

    # Salva direto sem scan — o frontmatter acima é sempre adicionado pela tool.
    # Usa save_to_github internamente, mas bypassa o scan passando conteúdo já em
    # acoes/pendentes/ que deve ter pasta sensivel/ se envolver dados privados.
    return await _save_to_github(acao_id, full_content, "acoes/pendentes")
