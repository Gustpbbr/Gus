"""
Pydantic schemas para os endpoints /hub/*.

Schema completo do fragmento segue projetos/gus/gus-18-schema-indexacao.md.
Esses Pydantic models cobrem só os campos que o cliente externo (Custom GPT,
Claude Code, Curador) deve fornecer — campos de lifecycle (estado, peso,
acessos, criado_em, ultimo_acesso) são preenchidos automaticamente em
hub.store:ingestar.
"""

from typing import Optional

from pydantic import BaseModel, Field


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


class IngestarReq(BaseModel):
    """Payload para inserir fragmento no Hub."""
    conteudo: str = Field(..., min_length=1, description="Texto do fragmento — auto-suficiente, sem 'ele'/'isso' sem nomear.")
    tipo: str = Field("episodico", description="Tipo do fragmento (gus-18). Aceita 'emergente:<nome>' para tipos não canônicos.")
    camada_temporal: str = Field("sessao", description="momento | sessao | semana | rotina | permanente")
    tipo_esquecimento: Optional[str] = Field(None, description="null (default) | funcional | deliberado | superado | protegido")
    via: str = Field("api", description="Origem: telegram | claude-code | claude-chat | custom-gpt | curador | manual")
    area: str = Field("", description="Área canônica (gus-18) ou 'emergente:<nome>'.")
    projeto: str = Field("", description="Slug do projeto, se aplicável.")
    user_id: str = Field("gustavo", description="'gustavo' (sobre o usuário) | 'gus' (sobre o agente).")
    confianca: float = Field(0.7, ge=0.0, le=1.0, description="Certeza do extrator/curador.")


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


class LembrarResp(BaseModel):
    results: list
    total: int
