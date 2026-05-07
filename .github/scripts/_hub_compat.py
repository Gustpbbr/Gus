"""
Compat layer Hub → formato Mem0.

Os scripts em .github/scripts/ historicamente leram do Mem0 SaaS via
`mem0.MemoryClient`. Após migração (R2 da auditoria fiscal), passam a ler
do Hub Qdrant — mas no FORMATO antigo, pra evitar reescrever a lógica
inteira de cada script.

Mapeamento de campos:
    Hub              →  Mem0 compat (formato esperado pelos scripts)
    conteudo         →  memory
    criado_em        →  created_at
    id               →  id
    score (search)   →  score
    tipo/area/via/.. →  metadata.{tipo,area,via,estado,curador}

USO:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from .github.scripts._hub_compat import get_all_memorias, search_memorias

    memorias = get_all_memorias(user_id="gustavo", limit=10000)
    # → [{"id": ..., "memory": ..., "created_at": ..., "metadata": {...}}, ...]

REQUISITOS DE AMBIENTE:
    QDRANT_URL, QDRANT_API_KEY (variáveis de secret no workflow)

VARIÁVEIS REMOVIDAS (não mais necessárias):
    MEM0_API_KEY (Mem0 SaaS aposentado pelo ADR-001)
"""

import os
import sys
from pathlib import Path

# Garante que o repo root esteja no sys.path pra importar `hub.store`.
# Cada script chamador faz isso também, mas reforçar aqui é defensivo.
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def _to_mem0_format(m: dict, include_score: bool = False) -> dict:
    """Converte 1 fragmento do Hub pro formato Mem0 que os scripts esperam.

    Antes do fix de 2026-05-04, este conversor preservava só 5 campos no
    `metadata` (tipo/estado/via/area/curador), o que deixava todos os
    consumidores (`meta_relatorio_hub.py`, `auditoria_hub.py`, etc.) cegos
    pra `camada_temporal`, `prompt_version`, `confianca`, `tipo_esquecimento`,
    `hash_janela`, `janela_turnos`, `acessos`, `ultimo_acesso` — todos
    campos que o curador e os ingest paths gravam normalmente. Resultado:
    relatórios mostravam 100% `(sem)` em colunas que estavam corretamente
    populadas no Hub.

    Agora o `metadata` carrega TODO o payload exceto os campos top-level
    do formato Mem0 (`memory`, `created_at`, `id`). Backward-compat: os 5
    campos antigos continuam acessíveis por nome (estavam todos em
    `metadata` antes, continuam estando agora).
    """
    # Campos que viram top-level no formato Mem0 (não duplicar no metadata)
    promovidos = {"id", "conteudo", "criado_em", "score"}
    metadata = {k: v for k, v in m.items() if k not in promovidos}
    out = {
        "id": m.get("id"),
        "memory": m.get("conteudo", ""),
        "created_at": m.get("criado_em", ""),
        "metadata": metadata,
    }
    if include_score:
        out["score"] = m.get("score", 0)
    return out


def get_all_memorias(user_id: str = "gustavo", limit: int = 10000) -> list[dict]:
    """Retorna todas as memórias do user_id no formato Mem0 compat.

    Substitui `client.get_all(user_id=user_id)` da Mem0 SaaS. Default
    `limit=10000` cobre o volume atual (~204 memórias migradas) com folga.

    Hub `listar()` faz scroll filtrado por user_id na coleção gus_hub.
    """
    from hub.store import listar
    raw = listar(user_id=user_id, limit=limit)
    return [_to_mem0_format(m) for m in raw]


def search_memorias(query: str, user_id: str = "gustavo", limit: int = 10) -> list[dict]:
    """Busca semântica filtrada — substitui `client.search()` da Mem0 SaaS.

    Hub `lembrar()` aplica filtro user_id + estado='ativo' por padrão
    (exclui historicos/esquecidos). Retorna ordenado por score descendente.
    """
    from hub.store import lembrar
    raw = lembrar(query=query, user_id=user_id, limit=limit)
    return [_to_mem0_format(m, include_score=True) for m in raw]


def health_check() -> tuple[bool, str]:
    """Smoke test rápido da conectividade Hub. Retorna (ok, mensagem).

    Útil pra workflows novos que precisam validar o ambiente antes
    de processar.
    """
    try:
        from hub.store import stats
        s = stats()
        total = (s.get("user_id_gustavo") or 0) + (s.get("user_id_gus") or 0)
        return True, f"Hub OK — {total} fragmentos ({s.get('colecao')})"
    except Exception as e:
        return False, f"Hub indisponível: {e}"


__all__ = ["get_all_memorias", "search_memorias", "health_check"]
