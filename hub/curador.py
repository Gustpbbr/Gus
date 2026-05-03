"""
Curador híbrido — extração de fragmentos atômicos via Haiku + GPT-4o-mini em paralelo.

Implementa Fase 2 do ADR-001 (aposentar Mem0 → Qdrant direto). Roda os DOIS
modelos sobre o MESMO trecho/arquivo, ambos salvam no Hub com:
    metadata.curador     = "haiku" (Anthropic) ou "gpt" (OpenAI)
    metadata.hash_janela = sha8 do input (mesmo valor pros 2 → permite parear)
    metadata.janela_turnos = quantas mensagens cobertas
    metadata.via         = porta de origem (telegram-claude, claude-chat, etc.)

Histórico:
- 27/04 → 29/04: A/B Haiku × Sonnet (mesma família Anthropic).
- 29/04 (gus-29 Fase 3): Sonnet substituído por GPT-4o-mini.
  Motivações: (1) resiliência — quando crédito Anthropic zera, GPT continua
  salvando memórias; (2) custo menor (~10x); (3) A/B mais informativo entre
  famílias diferentes.

Fragmentos antigos com `metadata.curador="sonnet"` permanecem históricos.
Novos fragmentos têm `metadata.curador="gpt"`.

Custo estimado por janela: ~$0.001 (Haiku) + ~$0.0001 (GPT-4o-mini).

Referências:
    - projetos/gus/auditorias/2026-04-27/.../ADR-001-aposentadoria-mem0.md
    - projetos/gus/gus-21-etapa3-curador.md (desenho original, single-model)
    - projetos/gus/gus-18-schema-indexacao.md (schema do payload)
    - projetos/gus/gus-29-roteamento-multimodelo-tiogu.md (mudança Sonnet → GPT)
"""

import asyncio
import hashlib
import json
import logging
import os
import re
from typing import Optional

from openai import AsyncOpenAI

from gus.llm import _chamar_claude_com_retry
from hub.store import ingestar

logger = logging.getLogger(__name__)

# Versão dos prompts do curador. Sobe quando PROMPT_CURADOR ou
# PROMPT_CURADOR_ARQUIVO mudar de forma que afete extração — permite
# distinguir fragmentos de gerações diferentes no Hub via
# `metadata.prompt_version`. Ex: comparar qualidade de extração antes/depois
# de uma reformulação do prompt sem precisar reler logs.
PROMPT_VERSION = "v1-2026-05-02"

_openai_client: Optional[AsyncOpenAI] = None


def _get_openai() -> AsyncOpenAI:
    """Lazy-init do client OpenAI (compartilhado entre chamadas)."""
    global _openai_client
    if _openai_client is None:
        _openai_client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            timeout=120.0,
        )
    return _openai_client


PROMPT_CURADOR = """Você é o Curador de memória do Gus, agente pessoal do Gustavo Pratti de Barros (anestesiologista, pesquisador em IA brasileiro).

Sua tarefa: analisar este trecho de interação e extrair fragmentos atômicos de informação útil que valem virar memória persistente no grafo do Gus.

REGRAS DE EXTRAÇÃO:

1. Cada fragmento = uma informação isolada e auto-suficiente. Sem "ele", "isso", "aquele projeto" sem nomear. Quem ler a memória sozinha (sem contexto) deve entender.

2. Ignore: saudações, confirmações curtas, "ok"/"valeu", small talk sem conteúdo, repetição óbvia.

3. PROTEÇÃO LGPD — Dimagem: se a janela contiver dados de paciente, extraia APENAS:
   - Nome do paciente
   - Data do procedimento
   - Convênio
   NUNCA inclua: tipo de exame, achados clínicos, observações médicas, intercorrências, doses, peso, jejum, status. Esses ficam nos arquivos `dimagem/casos/` com pseudônimo, não no Mem0.

4. Máximo 5 fragmentos por janela.

5. Se nada relevante: retorne lista vazia `[]`.

CLASSIFIQUE cada fragmento:

- tipo (escolha um):
  identidade_operacional | biografico | emocional | decisao | procedural |
  rotina | meta_reflexao | conexao_emergente | episodico | cronologico |
  fato | preferencia | lacuna | projeto

- camada_temporal:
  momento | sessao | semana | rotina | permanente

- area:
  gus | saude | financeiro | projetos | pessoal | dimagem | pesquisa |
  receitas | esportes

- confianca: 0.0 (especulativo) a 1.0 (cristal claro)

FORMATO DE SAÍDA — apenas JSON válido, sem texto extra antes ou depois:

[
  {
    "conteudo": "texto do fragmento auto-suficiente em pt-BR",
    "tipo": "<tipo>",
    "camada_temporal": "<camada>",
    "area": "<area>",
    "confianca": 0.0
  }
]

Trecho a analisar (porta de origem: {via}):

{conversa}
"""


def _hash_janela(texto: str) -> str:
    """Hash curto (sha8) pra parear fragmentos do mesmo input."""
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:8]


def _texto_de_message(msg: dict) -> str:
    """Extrai texto de uma message Anthropic (str ou list de blocos)."""
    role = "Gustavo" if msg.get("role") == "user" else "Gus"
    content = msg.get("content")
    if isinstance(content, str):
        return f"{role}: {content}"
    if isinstance(content, list):
        partes = [
            c.get("text", "")
            for c in content
            if isinstance(c, dict) and c.get("type") == "text"
        ]
        texto = " ".join(p for p in partes if p).strip() or "[mídia]"
        return f"{role}: {texto}"
    return f"{role}: [conteúdo não-texto]"


def _serializar_trecho(messages: list[dict]) -> str:
    """Serializa lista de messages num bloco de texto pra o curador analisar."""
    return "\n\n".join(_texto_de_message(m) for m in messages)


def _extrair_json(texto: str) -> list[dict]:
    """
    Extrai array JSON da resposta do modelo. Tolerante a texto antes/depois
    e cercas de código markdown (```json ... ```).
    """
    if not texto:
        return []

    # Tira cerca de código markdown se vier
    texto = texto.strip()
    if texto.startswith("```"):
        texto = re.sub(r"^```(?:json)?\s*", "", texto)
        texto = re.sub(r"```\s*$", "", texto)
        texto = texto.strip()

    # Tenta parsear direto
    try:
        parsed = json.loads(texto)
        return parsed if isinstance(parsed, list) else []
    except json.JSONDecodeError:
        pass

    # Fallback: extrai primeiro array via regex (greedy)
    match = re.search(r"\[\s*(?:\{.*?\}\s*,?\s*)*\]", texto, re.DOTALL)
    if match:
        try:
            parsed = json.loads(match.group(0))
            return parsed if isinstance(parsed, list) else []
        except json.JSONDecodeError:
            return []

    return []


# Enums canônicos importados do módulo único `hub.vocabularios` (item 1.1
# do plano de saneamento — antes havia listas duplicadas que dessincronizavam).
from hub.vocabularios import (
    TIPOS_CANONICOS as TIPOS_VALIDOS,
    CAMADAS_TEMPORAIS as CAMADAS_VALIDAS,
    AREAS_CANONICAS as AREAS_VALIDAS,
)


def _validar_fragmento(frag: dict) -> Optional[dict]:
    """Sanitiza um fragmento. Retorna dict válido ou None se descartável.

    Valida tipo/camada/area contra enums gus-18 — valores inválidos viram
    default em vez de poluir o vocabulário. Confiança é clamped pra [0,1]
    pra não quebrar sort/threshold do NeuroGus depois.
    """
    if not isinstance(frag, dict):
        return None
    conteudo = (frag.get("conteudo") or "").strip()
    if not conteudo or len(conteudo) < 10:
        return None

    tipo = (frag.get("tipo") or "episodico").strip()
    if tipo not in TIPOS_VALIDOS:
        logger.warning(f"Curador devolveu tipo inválido {tipo!r}, usando 'episodico'")
        tipo = "episodico"

    camada = (frag.get("camada_temporal") or "sessao").strip()
    if camada not in CAMADAS_VALIDAS:
        logger.warning(f"Curador devolveu camada inválida {camada!r}, usando 'sessao'")
        camada = "sessao"

    area = (frag.get("area") or "").strip()
    if area and area not in AREAS_VALIDAS:
        logger.warning(f"Curador devolveu area inválida {area!r}, descartando area")
        area = ""

    try:
        confianca = float(frag.get("confianca") or 0.7)
    except (TypeError, ValueError):
        confianca = 0.7
    confianca = max(0.0, min(1.0, confianca))  # clamp [0,1]

    return {
        "conteudo": conteudo,
        "tipo": tipo,
        "camada_temporal": camada,
        "area": area,
        "confianca": confianca,
    }


PROMPT_CURADOR_ARQUIVO = """Você é o Curador de memória do Gus, agente pessoal do Gustavo Pratti de Barros.

Este é um arquivo de memória escrito por uma instância do Claude Chat (claude.ai)
em uma sessão recente com o Gustavo. O arquivo já é uma curadoria preliminar
feita pelo próprio Chat — sua tarefa é REFINAR e CLASSIFICAR (não recriar do zero).

Sua tarefa:
1. Identificar fragmentos atômicos auto-suficientes dentro do arquivo.
2. Classificar cada um pelo schema gus-18 (tipo / camada / area / confiança).
3. Descartar lixo óbvio (saudação, "ok", teste, repetição do óbvio).

REGRAS DE EXTRAÇÃO:

1. Cada fragmento = uma informação isolada e auto-suficiente. Sem "ele", "isso", "aquele projeto" sem nomear. Quem ler a memória sozinha (sem contexto) deve entender.

2. PROTEÇÃO LGPD — Dimagem: se o arquivo contiver dados de paciente, extraia APENAS:
   - Nome do paciente
   - Data do procedimento
   - Convênio
   NUNCA: tipo de exame, achados clínicos, observações médicas, intercorrências, doses, peso, jejum, status.

3. Máximo 8 fragmentos por arquivo (arquivos do Chat costumam ser mais ricos que janelas Telegram).

4. Se o arquivo for trivial / de teste / só saudação: retorne `[]`.

CLASSIFIQUE cada fragmento:

- tipo: identidade_operacional | biografico | emocional | decisao | procedural | rotina | meta_reflexao | conexao_emergente | episodico | cronologico | fato | preferencia | lacuna | projeto

- camada_temporal: momento | sessao | semana | rotina | permanente

- area: gus | saude | financeiro | projetos | pessoal | dimagem | pesquisa | receitas | esportes

- confianca: 0.0 (especulativo) a 1.0 (cristal claro)

FORMATO — apenas JSON válido, sem texto extra:

[
  {
    "conteudo": "texto auto-suficiente em pt-BR",
    "tipo": "<tipo>",
    "camada_temporal": "<camada>",
    "area": "<area>",
    "confianca": 0.0
  }
]

Arquivo a analisar (porta de origem: {via}):

{conteudo}
"""


def _render_prompt(template: str, via: str, input_texto: str) -> str:
    """Renderiza o prompt template substituindo placeholders sem usar str.format.

    str.format() interpreta `{` e `}` como placeholders — e os templates do
    curador contêm um exemplo JSON com `{` `}` literais ("conteudo": "..."}).
    Format() pega o trecho entre o primeiro `{` e o próximo `}` e tenta usar
    como chave (`\\n    "conteudo"`), explodindo com KeyError. Esse bug fez o
    curador errar 100% das chamadas a partir de 30/04/2026 (todos logs em
    `_log/curador/AAAA-MM-DD.md` mostram só `status: erro`).

    Replace() é robusto contra braces JSON literais.
    """
    return (
        template
        .replace("{via}", via)
        .replace("{conversa}", input_texto)
        .replace("{conteudo}", input_texto)
    )


async def _extrair_via_modelo(
    input_texto: str, prompt_template: str, modelo: str, via: str, max_frags: int
) -> list[dict]:
    """Chama um modelo Claude com prompt_template. Retorna lista de fragmentos validados.

    Bug fix 2026-04-27: prompt template vai como `system_prompt` em vez de
    `messages[0].content`. Sonnet 4.6 com system="" (vazio) estava devolvendo
    400 'temperature and top_p cannot both be specified' nas chamadas SEM
    tools — o curador errava 100% do dia, Hub ficava vazio. Mover o prompt
    pro system (canônico) resolve sem mexer no SDK.
    """
    prompt = _render_prompt(prompt_template, via, input_texto)
    try:
        response = await _chamar_claude_com_retry(
            model=modelo,
            max_tokens=2048,
            system_prompt=prompt,
            messages=[{"role": "user", "content": "Extraia agora os fragmentos conforme as regras."}],
        )
    except Exception as e:
        logger.warning(f"Curador {modelo} falhou: {e}")
        return []

    texto = next((b.text for b in response.content if hasattr(b, "text")), "") or ""
    crus = _extrair_json(texto)
    validos = [v for v in (_validar_fragmento(f) for f in crus) if v]
    return validos[:max_frags]


async def _extrair_via_openai(
    input_texto: str, prompt_template: str, modelo: str, via: str, max_frags: int
) -> list[dict]:
    """Variante OpenAI de `_extrair_via_modelo`. Mesmo prompt, mesma extração JSON.

    Adicionado em gus-29 Fase 3 (29/04/2026). Substitui Sonnet no slot
    secundário do curador híbrido. Resiliente a crédito Anthropic — se
    Anthropic ficar offline, GPT-4o-mini continua salvando memórias.
    """
    prompt = _render_prompt(prompt_template, via, input_texto)
    try:
        oai = _get_openai()
        response = await oai.chat.completions.create(
            model=modelo,
            max_tokens=2048,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Extraia agora os fragmentos conforme as regras."},
            ],
        )
    except Exception as e:
        logger.warning(f"Curador {modelo} (OpenAI) falhou: {e}")
        return []

    texto = response.choices[0].message.content or ""
    crus = _extrair_json(texto)
    validos = [v for v in (_validar_fragmento(f) for f in crus) if v]
    return validos[:max_frags]


async def _curar_input_hibrido(
    input_texto: str,
    prompt_template: str,
    via: str,
    user_id: str,
    janela_turnos: int,
    max_frags_por_modelo: int = 5,
) -> dict:
    """
    Lógica comum: roda Haiku + Sonnet em paralelo sobre o mesmo input_texto,
    ambos salvam no Hub com metadata.curador distinta + mesmo hash_janela.

    Reusada por curar_turnos (input = trecho de mensagens) e curar_arquivo
    (input = body de arquivo Markdown).

    Returns:
        dict {hash_janela, haiku: list, gpt: list, salvos: int, erros: list, via, user_id}
    """
    if not input_texto or not input_texto.strip():
        return {
            "hash_janela": "", "haiku": [], "gpt": [],
            "salvos": 0, "erros": ["input vazio"],
            "via": via, "user_id": user_id,
        }

    hash_j = _hash_janela(input_texto)

    # Vars novas: MODEL_CURADOR_ANTHROPIC / MODEL_CURADOR_OPENAI (slot semântico,
    # não amarra a modelo específico). Aceita os nomes antigos como fallback
    # pra não quebrar deploys existentes — workflow Chat ainda passa
    # MODEL_CURADOR_HAIKU=claude-sonnet-4-6, que confundia (nome sugere família,
    # mas valor é outra). Após próximo deploy, vars antigas podem sair.
    modelo_anthropic = os.getenv("MODEL_CURADOR_ANTHROPIC") or os.getenv("MODEL_CURADOR_HAIKU", "claude-haiku-4-5")
    modelo_openai = os.getenv("MODEL_CURADOR_OPENAI") or os.getenv("MODEL_CURADOR_GPT", "gpt-4o-mini")

    haiku_frags, gpt_frags = await asyncio.gather(
        _extrair_via_modelo(input_texto, prompt_template, modelo_anthropic, via, max_frags_por_modelo),
        _extrair_via_openai(input_texto, prompt_template, modelo_openai, via, max_frags_por_modelo),
        return_exceptions=False,
    )

    erros: list[str] = []
    salvos = 0

    async def _salvar_lista(frags: list[dict], curador: str):
        nonlocal salvos
        for f in frags:
            try:
                await asyncio.to_thread(
                    ingestar,
                    f["conteudo"],
                    {
                        "tipo": f["tipo"],
                        "camada_temporal": f["camada_temporal"],
                        "area": f["area"],
                        "confianca": f["confianca"],
                        "via": via,
                        "user_id": user_id,
                        "curador": curador,
                        "hash_janela": hash_j,
                        "janela_turnos": janela_turnos,
                        "prompt_version": PROMPT_VERSION,
                    },
                )
                salvos += 1
            except Exception as e:
                erros.append(f"ingestar {curador}: {str(e)[:120]}")

    await asyncio.gather(
        _salvar_lista(haiku_frags, "haiku"),
        _salvar_lista(gpt_frags, "gpt"),
    )

    return {
        "hash_janela": hash_j,
        "haiku": haiku_frags,
        "gpt": gpt_frags,
        "salvos": salvos,
        "erros": erros,
        "via": via,
        "user_id": user_id,
    }


async def curar_turnos(
    messages: list[dict],
    via: str = "telegram-claude",
    user_id: str = "gustavo",
) -> dict:
    """
    Curadoria híbrida sobre uma janela de mensagens (Telegram, etc.).

    Args:
        messages: lista de mensagens [{role, content}, ...] da janela.
        via: porta de origem (telegram-claude, etc.).
        user_id: brain alvo ('gustavo' ou 'gus').
    """
    if not messages:
        return {
            "hash_janela": "", "haiku": [], "gpt": [],
            "salvos": 0, "erros": ["sem messages"],
            "via": via, "user_id": user_id,
        }

    conversa = _serializar_trecho(messages)
    return await _curar_input_hibrido(
        input_texto=conversa,
        prompt_template=PROMPT_CURADOR,
        via=via,
        user_id=user_id,
        janela_turnos=len(messages),
        max_frags_por_modelo=5,
    )


async def curar_arquivo(
    body: str,
    via: str = "claude-chat",
    user_id: str = "gustavo",
) -> dict:
    """
    Curadoria híbrida sobre um arquivo de memória (Claude Chat ingest).

    Mesmo padrão de curar_turnos, mas com prompt específico pra arquivo
    pré-curado (não trecho de turnos crus).

    Args:
        body: corpo do arquivo (sem frontmatter).
        via: porta de origem (default 'claude-chat').
        user_id: brain alvo ('gustavo' ou 'gus').
    """
    return await _curar_input_hibrido(
        input_texto=(body or "").strip(),
        prompt_template=PROMPT_CURADOR_ARQUIVO,
        via=via,
        user_id=user_id,
        janela_turnos=1,  # arquivo = 1 unidade de input
        max_frags_por_modelo=8,
    )
