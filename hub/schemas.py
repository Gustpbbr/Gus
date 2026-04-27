"""
Pydantic schemas para os endpoints /hub/*.

Schema completo do fragmento segue projetos/gus/gus-18-schema-indexacao.md.
Esses Pydantic models cobrem só os campos que o cliente externo (Custom GPT,
Claude Code, Curador) deve fornecer — campos de lifecycle (estado, peso,
acessos, criado_em, ultimo_acesso) são preenchidos automaticamente em
hub.store:ingestar.

Validação `via` (Item 5 do plano):
- Vias canônicas listadas em VIAS_CANONICAS
- Aceita também prefixos:
    - 'workflow-*' (workflows automáticos: briefing, retrospectiva, etc.)
    - 'emergente:*' (vias novas em validação)
- Qualquer outro valor → 422 Unprocessable Entity
"""

from typing import Optional

from pydantic import BaseModel, Field, field_validator


# Tipos canônicos definidos em gus-18 (lista aberta — prefixo 'emergente:' aceito)
TIPOS_CANONICOS = {
    "identidade_operacional", "biografico", "emocional", "decisao",
    "procedural", "rotina", "meta_reflexao", "conexao_emergente",
    "episodico", "cronologico", "fato", "preferencia", "lacuna", "projeto",
}

CAMADAS_TEMPORAIS = {"momento", "sessao", "semana", "rotina", "permanente"}

TIPOS_ESQUECIMENTO = {None, "funcional", "deliberado", "superado", "protegido"}

AREAS_CANONICAS = {
    "gus", "saude", "financeiro", "projetos", "pessoal",
    "dimagem", "pesquisa", "receitas", "esportes",
}

# Vias canônicas (Item 5). Aceita também prefixos workflow-* e emergente:*.
VIAS_CANONICAS = {
    # Portas humanas (interação direta com Gustavo)
    "telegram-claude", "telegram-gpt",
    "claude-code", "claude-chat",
    "custom-gpt", "alexa", "carro-audio",
    # Casos especiais
    "manual",     # entrada manual via Obsidian/CLI
    "curador",    # quando o próprio curador atribui
    "api",        # cliente API genérico (default IngestarReq)
}


def _via_valida(v: str) -> bool:
    if v in VIAS_CANONICAS:
        return True
    if v.startswith("workflow-") and len(v) > len("workflow-"):
        return True
    if v.startswith("emergente:") and len(v) > len("emergente:"):
        return True
    return False


class IngestarReq(BaseModel):
    """Payload para inserir fragmento no Hub."""
    conteudo: str = Field(..., min_length=1, description="Texto do fragmento — auto-suficiente, sem 'ele'/'isso' sem nomear.")
    tipo: str = Field("episodico", description="Tipo do fragmento (gus-18). Aceita 'emergente:<nome>' para tipos não canônicos.")
    camada_temporal: str = Field("sessao", description="momento | sessao | semana | rotina | permanente")
    tipo_esquecimento: Optional[str] = Field(None, description="null (default) | funcional | deliberado | superado | protegido")
    via: str = Field("api", description="Origem: telegram-claude | claude-code | claude-chat | custom-gpt | curador | manual | workflow-<nome> | emergente:<nome>")
    area: str = Field("", description="Área canônica (gus-18) ou 'emergente:<nome>'.")
    projeto: str = Field("", description="Slug do projeto, se aplicável.")
    user_id: str = Field("gustavo", description="'gustavo' (sobre o usuário) | 'gus' (sobre o agente).")
    confianca: float = Field(0.7, ge=0.0, le=1.0, description="Certeza do extrator/curador.")

    @field_validator("via")
    @classmethod
    def _v_via(cls, v: str) -> str:
        if not _via_valida(v):
            raise ValueError(
                f"via inválida: '{v}'. Aceitas: {sorted(VIAS_CANONICAS)} ou prefixos 'workflow-' / 'emergente:'."
            )
        return v

    @field_validator("user_id")
    @classmethod
    def _v_user_id(cls, v: str) -> str:
        if v not in ("gustavo", "gus"):
            raise ValueError(f"user_id deve ser 'gustavo' ou 'gus' — recebido: '{v}'")
        return v

    @field_validator("camada_temporal")
    @classmethod
    def _v_camada(cls, v: str) -> str:
        if v not in CAMADAS_TEMPORAIS:
            raise ValueError(f"camada_temporal inválida: '{v}'. Aceitas: {sorted(CAMADAS_TEMPORAIS)}")
        return v

    @field_validator("tipo_esquecimento")
    @classmethod
    def _v_esq(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in {"funcional", "deliberado", "superado", "protegido"}:
            raise ValueError(f"tipo_esquecimento inválido: '{v}'")
        return v


class IngestarResp(BaseModel):
    id: str
    status: str = "ok"


class LembrarReq(BaseModel):
    """Payload para buscar fragmentos no Hub."""
    query: str = Field(..., min_length=1)
    user_id: str = Field("gustavo")
    limit: int = Field(10, ge=1, le=30)
    tipo: Optional[str] = Field(None, description="Filtra por tipo exato. Omita para todos.")
    estado: Optional[str] = Field("ativo", description="Default 'ativo'. Passe null/vazio para incluir todos.")
    area: Optional[str] = Field(None, description="Filtra por área. Omita para todas.")

    @field_validator("user_id")
    @classmethod
    def _v_user_id(cls, v: str) -> str:
        if v not in ("gustavo", "gus"):
            raise ValueError(f"user_id deve ser 'gustavo' ou 'gus'")
        return v


class LembrarResp(BaseModel):
    results: list
    total: int

