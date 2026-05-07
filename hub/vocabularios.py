"""
Vocabulários canônicos do schema gus-18 — fonte única.

Todo módulo que valida ou injeta valores nos campos `tipo`, `area`,
`camada_temporal`, `tipo_esquecimento`, `via` deve importar daqui em vez
de redefinir constantes locais. Antes desse módulo, schemas.py e
curador.py tinham listas duplicadas que dessincronizavam (item M-MED-2
da auditoria 2026-05-02-memoria-diagnostico.md).

Documento canônico: projetos/gus/gus-18-schema-indexacao.md
"""

# Tipos canônicos (lista aberta — prefixo 'emergente:' aceito em vez de inventar)
TIPOS_CANONICOS = frozenset({
    "identidade_operacional", "biografico", "emocional", "decisao",
    "procedural", "rotina", "meta_reflexao", "conexao_emergente",
    "episodico", "cronologico", "fato", "preferencia", "lacuna", "projeto",
})

CAMADAS_TEMPORAIS = frozenset({"momento", "sessao", "semana", "rotina", "permanente"})

TIPOS_ESQUECIMENTO = frozenset({"funcional", "deliberado", "superado", "protegido"})

AREAS_CANONICAS = frozenset({
    "gus", "saude", "financeiro", "projetos", "pessoal",
    "dimagem", "pesquisa", "receitas", "esportes",
})

# Vias canônicas. Aceita também prefixos `workflow-*` e `emergente:*`.
VIAS_CANONICAS = frozenset({
    # Portas humanas (interação direta com Gustavo)
    "telegram-claude", "telegram-gpt",
    "claude-code", "claude-chat",
    "custom-gpt", "alexa", "carro-audio",
    # Casos especiais
    "manual",                    # entrada manual via Obsidian/CLI
    "curador",                   # quando o próprio curador atribui
    "api",                       # cliente API genérico (default IngestarReq)
    "legacy-mem0-saas",          # importação histórica (Fase 5.6 do plano de saneamento)
})


def via_valida(v: str) -> bool:
    """Aceita valor canônico OU prefixo `workflow-<algo>` / `emergente:<algo>`."""
    if not v:
        return False
    if v in VIAS_CANONICAS:
        return True
    if v.startswith("workflow-") and len(v) > len("workflow-"):
        return True
    if v.startswith("emergente:") and len(v) > len("emergente:"):
        return True
    return False


def tipo_valido(t: str) -> bool:
    """Aceita canônico OU prefixo `emergente:<algo>`."""
    if not t:
        return False
    if t in TIPOS_CANONICOS:
        return True
    if t.startswith("emergente:") and len(t) > len("emergente:"):
        return True
    return False


def area_valida(a: str) -> bool:
    """Vazio é aceito (área desconhecida). Caso contrário, canônico ou `emergente:<algo>`."""
    if not a:
        return True
    if a in AREAS_CANONICAS:
        return True
    if a.startswith("emergente:") and len(a) > len("emergente:"):
        return True
    return False


__all__ = [
    "TIPOS_CANONICOS", "CAMADAS_TEMPORAIS", "TIPOS_ESQUECIMENTO",
    "AREAS_CANONICAS", "VIAS_CANONICAS",
    "via_valida", "tipo_valido", "area_valida",
]
