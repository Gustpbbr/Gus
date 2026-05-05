"""
Endpoints REST que o Custom GPT consome via Actions.

Cada endpoint:
  - protegido por Bearer token (`verify_bearer` global no router)
  - retorna `{"result": "<texto>"}` (TextResp)
  - reusa a função interna do bot (não duplica lógica)

PROTEÇÕES ESPECÍFICAS desta porta:
  - Path `dimagem/` BLOQUEADO em read/list/save (LGPD: dados de paciente
    não passam pela OpenAI). Bot Telegram continua acessando normalmente.
  - PII scan herdado do `_save_to_github` (CPF/CNPJ/cartão/keys → bloqueia).
  - Frontmatter de arquivos salvos por aqui leva `via: custom-gpt`.
  - Wikilinks: cada chamada salva sugestões em fila pendente
    (`acoes/wikilinks-pendentes/`) pra Claude/TioGu curar depois.
"""

from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends, HTTPException

from api.auth import verify_bearer
from api.schemas import (
    CameraAnalyseReq,
    DeleteMemoryReq,
    ListGitHubReq,
    PesquisarArxivReq,
    PesquisarPubmedReq,
    ReadGitHubReq,
    SaveGitHubReq,
    SaveMemoryGusReq,
    SaveMemoryReq,
    SearchMemoryGusReq,
    SearchMemoryReq,
    SearchWebReq,
    SugerirWikilinksReq,
    TextResp,
)
from gus.memory import (
    buscar_memorias_detalhada,
    buscar_memorias_gus,
    deletar_memoria,
    salvar_memorias,
    salvar_observacao_gus,
)
from api.dashboard import fetch_graph_data, fetch_health_data
from gus.integrations.pesquisa import pesquisar_arxiv, pesquisar_pubmed
from gus.integrations.wikilinks import sugerir_wikilinks
from api.camera import analisar_imagem, salvar_captura
from gus.tools import (
    _list_github_directory,
    _read_from_github,
    _save_to_github,
    _search_web,
)


BRT = timezone(timedelta(hours=-3))
VIA_TAG = "custom-gpt"

# Paths bloqueados nesta porta. Bloqueio aplicado a read/list/save.
PATHS_BLOQUEADOS = ("dimagem/", "dimagem")


def _path_bloqueado(path: str) -> bool:
    p = (path or "").strip().lstrip("/").lower()
    if not p:
        return False
    return p == "dimagem" or p.startswith("dimagem/")


router = APIRouter(dependencies=[Depends(verify_bearer)])


# ====================== Mem0 — brain `gustavo` ======================


@router.post("/search_memory", operation_id="search_memory", response_model=TextResp)
async def r_search_memory(payload: SearchMemoryReq):
    """Busca semântica nas memórias do Gustavo (brain `gustavo`)."""
    result = await buscar_memorias_detalhada(payload.query, payload.limit)
    return TextResp(result=result)


@router.post("/salvar_memoria", operation_id="salvar_memoria", response_model=TextResp)
async def r_salvar_memoria(payload: SaveMemoryReq):
    """Salva fato sobre o Gustavo no brain `gustavo` (tag via=custom-gpt)."""
    await salvar_memorias(
        [{"role": "user", "content": payload.conteudo}],
        via=VIA_TAG,
    )
    return TextResp(result=f"Salvo no brain `gustavo` (via={VIA_TAG}): {payload.conteudo[:120]}")


# ====================== Mem0 — brain `gus` ======================


@router.post("/buscar_memoria_gus", operation_id="buscar_memoria_gus", response_model=TextResp)
async def r_buscar_memoria_gus(payload: SearchMemoryGusReq):
    """Busca nas auto-observações do agente (brain `gus` compartilhado)."""
    result = await buscar_memorias_gus(payload.query, payload.limit)
    return TextResp(result=result)


@router.post("/salvar_memoria_gus", operation_id="salvar_memoria_gus", response_model=TextResp)
async def r_salvar_memoria_gus(payload: SaveMemoryGusReq):
    """Salva auto-observação no brain `gus` (operacional, tag via=custom-gpt)."""
    await salvar_observacao_gus(payload.observacao, via=VIA_TAG)
    return TextResp(result=f"Salvo no brain `gus` (via={VIA_TAG}): {payload.observacao[:120]}")


# ====================== Mem0 — delete ======================


@router.post("/deletar_memoria", operation_id="deletar_memoria", response_model=TextResp)
async def r_deletar_memoria(payload: DeleteMemoryReq):
    """Deleta memória do Mem0 (IRREVERSÍVEL)."""
    user_id = payload.user_id or "gustavo"
    if user_id not in ("gustavo", "gus"):
        raise HTTPException(status_code=400, detail="user_id deve ser 'gustavo' ou 'gus'.")
    result = await deletar_memoria(payload.memory_id, user_id)
    return TextResp(result=result)


# ====================== GitHub ======================


@router.post("/read_from_github", operation_id="read_from_github", response_model=TextResp)
async def r_read_from_github(payload: ReadGitHubReq):
    """Lê arquivo .md do repo. Path `dimagem/` BLOQUEADO nesta porta."""
    if _path_bloqueado(payload.path):
        raise HTTPException(
            status_code=403,
            detail="Path `dimagem/` bloqueado nesta porta (LGPD). Use Telegram.",
        )
    result = await _read_from_github(payload.path, payload.branch)
    return TextResp(result=result)


@router.post("/list_github_directory", operation_id="list_github_directory", response_model=TextResp)
async def r_list_github_directory(payload: ListGitHubReq):
    """Lista pasta do repo. Path `dimagem/` BLOQUEADO nesta porta."""
    if _path_bloqueado(payload.path):
        raise HTTPException(
            status_code=403,
            detail="Path `dimagem/` bloqueado nesta porta (LGPD). Use Telegram.",
        )
    result = await _list_github_directory(payload.path, payload.branch)
    return TextResp(result=result)


@router.post("/save_to_github", operation_id="save_to_github", response_model=TextResp)
async def r_save_to_github(payload: SaveGitHubReq):
    """Salva .md no repo. Bloqueia path `dimagem/` e PII (CPF/cartão/keys)."""
    if _path_bloqueado(payload.folder):
        raise HTTPException(
            status_code=403,
            detail="Path `dimagem/` bloqueado nesta porta (LGPD). Use Telegram.",
        )
    result = await _save_to_github(payload.filename, payload.content, payload.folder, via=VIA_TAG)
    return TextResp(result=result)


# ====================== Web e Pesquisa ======================


@router.post("/search_web", operation_id="search_web", response_model=TextResp)
async def r_search_web(payload: SearchWebReq):
    """Busca web (Tavily primário, DuckDuckGo fallback)."""
    result = await _search_web(payload.query)
    return TextResp(result=result)


@router.post("/pesquisar_pubmed", operation_id="pesquisar_pubmed", response_model=TextResp)
async def r_pesquisar_pubmed(payload: PesquisarPubmedReq):
    """Busca artigos no PubMed (NCBI). Sem custo."""
    result = await pesquisar_pubmed(payload.query, payload.max_n, payload.since_year)
    return TextResp(result=result)


@router.post("/pesquisar_arxiv", operation_id="pesquisar_arxiv", response_model=TextResp)
async def r_pesquisar_arxiv(payload: PesquisarArxivReq):
    """Busca preprints no arXiv. Sem custo."""
    result = await pesquisar_arxiv(payload.query, payload.max_n, payload.categoria)
    return TextResp(result=result)


# ====================== Atalhos de leitura fixa ======================


@router.get("/meta_memoria", operation_id="meta_memoria", response_model=TextResp)
async def r_meta_memoria():
    """Lê `gus/meta-memoria.md` (biografia narrativa do Gus)."""
    result = await _read_from_github("gus/meta-memoria.md")
    return TextResp(result=result)


@router.get("/auditoria_hub", operation_id="auditoria_hub", response_model=TextResp)
async def r_auditoria_hub():
    """Lê `_indices/_auditoria-hub.md` (stats da última auditoria)."""
    result = await _read_from_github("_indices/_auditoria-hub.md")
    return TextResp(result=result)


# ====================== Wikilinks (com fila de curadoria) ======================


@router.post("/sugerir_wikilinks", operation_id="sugerir_wikilinks", response_model=TextResp)
async def r_sugerir_wikilinks(payload: SugerirWikilinksReq):
    """Sugere wikilinks pra um arquivo. Sugestões salvas em fila pendente
    pra revisão posterior pelo Claude/TioGu — não aplica direto."""
    if _path_bloqueado(payload.arquivo):
        raise HTTPException(status_code=403, detail="Path `dimagem/` bloqueado.")

    sugestoes = await sugerir_wikilinks(payload.arquivo, payload.branch)

    # Salva fila pendente
    now = datetime.now(BRT)
    timestamp = now.strftime("%Y-%m-%dT%H-%M-%S")
    nome_base = payload.arquivo.replace("/", "_").replace(".md", "")
    filename_pendente = f"{timestamp}__{nome_base}"

    conteudo_pendente = (
        f"# Wikilinks pendentes — {payload.arquivo}\n\n"
        f"**Origem:** Custom GPT  \n"
        f"**Quando:** {now.isoformat()}  \n"
        f"**Status:** aguardando curadoria do Claude/TioGu\n\n"
        f"---\n\n"
        f"{sugestoes}\n"
    )

    await _save_to_github(
        filename_pendente,
        conteudo_pendente,
        "acoes/wikilinks-pendentes",
        via=VIA_TAG,
    )

    return TextResp(
        result=(
            f"{sugestoes}\n\n"
            f"---\n\n"
            f"_Sugestões também salvas em `acoes/wikilinks-pendentes/{filename_pendente}.md` pra curadoria do Claude/TioGu._"
        )
    )


# ====================== Dashboard ======================


@router.get("/graph-data", operation_id="graph_data", include_in_schema=False)
async def r_graph_data():
    """Retorna nós do grafo de memórias (Qdrant) pro dashboard."""
    return await fetch_graph_data()


@router.get("/health-data", operation_id="health_data", include_in_schema=False)
async def r_health_data():
    """Retorna métricas de saúde do sistema pro dashboard."""
    return await fetch_health_data()


# ====================== Câmera / Visão (PROJETO FUTURO) ======================
#
# Endpoints para integração com câmera do S8 via PWA.
# Fluxo: S8 (PWA /camera) → POST /analise_camera → Claude Vision → GitHub
#        Custom GPT → GET /ver_ultima_captura → lê _ultimo.md
#
# Status atual: implementado e funcional, mas NÃO exposto no OpenAPI do Custom
# GPT (include_in_schema=False em ambos). Será ativado quando o Custom GPT
# estiver funcionando com Actions configuradas e o S8 estiver como terminal fixo.
#
# Para ativar no Custom GPT: remover include_in_schema=False dos dois endpoints
# e fazer redeploy no Railway.


@router.post(
    "/analise_camera",
    operation_id="analise_camera",
    response_model=TextResp,
    include_in_schema=False,  # FUTURO — oculto do OpenAPI/Custom GPT por ora
)
async def r_analise_camera(payload: CameraAnalyseReq):
    """Analisa imagem com Claude Vision, salva JPG + MD em capturado/visual/.

    Recebido pela PWA do S8 a cada 30s (modo auto) ou sob demanda.
    A análise fica disponível em /ver_ultima_captura pra o Custom GPT ler.
    """
    timestamp = datetime.now(BRT).strftime("%Y-%m-%d-%H%M%S")

    b64 = payload.image_base64
    if "," in b64:
        b64 = b64.split(",", 1)[1]

    analise = await analisar_imagem(b64, payload.contexto)
    salvos = await salvar_captura(b64, analise, timestamp)

    paths = [p for p in [salvos.get("img_path"), salvos.get("md_path")] if p]
    status = f"Salvo em: {', '.join(paths)}" if paths else "Análise feita, erro ao salvar no GitHub"
    return TextResp(result=f"{analise}\n\n---\n_{status}_")


@router.get(
    "/ver_ultima_captura",
    operation_id="ver_ultima_captura",
    response_model=TextResp,
    include_in_schema=False,  # FUTURO — oculto do OpenAPI/Custom GPT por ora
)
async def r_ver_ultima_captura():
    """Lê a última captura visual registrada pela câmera do S8.

    Custom GPT chama este endpoint quando o Gustavo perguntar
    'o que você está vendo?', 'o que eu estava fazendo?', etc.
    Retorna o conteúdo de capturado/visual/_ultimo.md.
    """
    result = await _read_from_github("capturado/visual/_ultimo.md")
    return TextResp(result=result)
