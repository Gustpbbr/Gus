"""
Pydantic schemas pros endpoints da API. Cada modelo vira parte do
OpenAPI 3.0 que o Custom GPT importa no Builder.

Mantemos descrições curtas porque o GPT Builder usa elas pra entender
quando chamar cada operation.
"""

from pydantic import BaseModel, Field


# ============== Mem0 ==============


class SearchMemoryReq(BaseModel):
    query: str = Field(..., description="Pergunta em linguagem natural sobre o Gustavo.")
    limit: int = Field(10, ge=1, le=20, description="Máximo de memórias retornadas.")


class SaveMemoryReq(BaseModel):
    conteudo: str = Field(..., description="Fato sobre o Gustavo a salvar no brain `gustavo`.")


class SaveMemoryGusReq(BaseModel):
    observacao: str = Field(..., description="Auto-observação a salvar no brain `gus` (operacional).")


class SearchMemoryGusReq(BaseModel):
    query: str = Field(..., description="Query semântica nas memórias operacionais do agente.")
    limit: int = Field(10, ge=1, le=20)


class DeleteMemoryReq(BaseModel):
    memory_id: str = Field(..., description="UUID da memória a deletar (irreversível).")
    user_id: str | None = Field(None, description="`gustavo` ou `gus`. Default `gustavo`.")


# ============== GitHub ==============


class ReadGitHubReq(BaseModel):
    path: str = Field(..., description="Path do arquivo no repo, ex: 'pessoal/saude/historico.md'.")
    branch: str | None = Field(None, description="Branch. Omita pra ler do main.")


class ListGitHubReq(BaseModel):
    path: str = Field("", description="Path da pasta no repo. Vazio = raiz.")
    branch: str | None = None


class SaveGitHubReq(BaseModel):
    filename: str = Field(..., description="Nome do arquivo SEM extensão (.md adicionado).")
    content: str = Field(..., description="Conteúdo Markdown do arquivo.")
    folder: str = Field("capturado", description="Pasta destino no repo (ex: 'capturado/links').")


# ============== Web e Pesquisa ==============


class SearchWebReq(BaseModel):
    query: str = Field(..., description="Query de busca web (Tavily com fallback DDG).")


class PesquisarPubmedReq(BaseModel):
    query: str = Field(..., description="Termos de busca biomédica.")
    max_n: int = Field(10, ge=1, le=20)
    since_year: int | None = Field(None, description="Filtra a partir do ano (ex: 2020).")


class PesquisarArxivReq(BaseModel):
    query: str = Field(..., description="Termos de busca em IA/ML/CS/neuro.")
    max_n: int = Field(10, ge=1, le=20)
    categoria: str | None = Field(None, description="ex: 'cs.AI', 'cs.LG', 'q-bio.NC'.")


# ============== Wikilinks ==============


class SugerirWikilinksReq(BaseModel):
    arquivo: str = Field(..., description="Path .md do repo (extensão opcional).")
    branch: str | None = None


# ============== Resposta padrão ==============


class TextResp(BaseModel):
    result: str = Field(..., description="Resultado em texto formatado (Markdown).")
