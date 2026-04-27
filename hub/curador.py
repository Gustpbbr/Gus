"""
Curador híbrido — extração de fragmentos atômicos via Haiku + Sonnet em paralelo.

Implementa Fase 2 do ADR-001 (aposentar Mem0 → Qdrant direto). Roda os DOIS
modelos sobre o MESMO trecho/arquivo, ambos salvam no Hub com:
    metadata.curador     = "haiku" ou "sonnet"
    metadata.hash_janela = sha8 do input (mesmo valor pros 2 → permite parear)
    metadata.janela_turnos = quantas mensagens cobertas
    metadata.via         = porta de origem (telegram-claude, claude-chat, etc.)

Por 14 dias de coleta dual, o Gustavo pode comparar par-a-par qual curador
extrai melhor. Depois de validado, decide se mantém só um ou os dois.

Custo estimado por janela: ~$0.001 (Haiku) + ~$0.003 (Sonnet) = ~$0.004.

Referências:
    - projetos/gus/auditorias/2026-04-27/.../ADR-001-aposentadoria-mem0.md
    - projetos/gus/gus-21-etapa3-curador.md (desenho original, single-model)
    - projetos/gus/gus-18-schema-indexacao.md (schema do payload)
"""

import asyncio
import hashlib
import json
import logging
import os
import re
from typing import Optional

from gus.llm import _chamar_claude_com_retry
from hub.store import ingestar

logger = logging.getLogger(__name__)


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


def _validar_fragmento(frag: dict) -> Optional[dict]:
    """Sanitiza um fragmento. Retorna dict válido ou None se descartável."""
    if not isinstance(frag, dict):
        return None
    conteudo = (frag.get("conteudo") or "").strip()
    if not conteudo or len(conteudo) < 10:
        return None
    return {
        "conteudo": conteudo,
        "tipo": (frag.get("tipo") or "episodico").strip(),
        "camada_temporal": (frag.get("camada_temporal") or "sessao").strip(),
        "area": (frag.get("area") or "").strip(),
        "confianca": float(frag.get("confianca") or 0.7),
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


async def _extrair_via_modelo(
    input_texto: str, prompt_template: str, modelo: str, via: str, max_frags: int
) -> list[dict]:
    """Chama um modelo Claude com prompt_template. Retorna lista de fragmentos validados."""
    prompt = prompt_template.format(via=via, conversa=input_texto, conteudo=input_texto)
    try:
        response = await _chamar_claude_com_retry(
            model=modelo,
            max_tokens=2048,
            system_prompt="",
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as e:
        logger.warning(f"Curador {modelo} falhou: {e}")
        return []

    texto = next((b.text for b in response.content if hasattr(b, "text")), "") or ""
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
        dict {hash_janela, haiku: list, sonnet: list, salvos: int, erros: list, via, user_id}
    """
    if not input_texto or not input_texto.strip():
        return {
            "hash_janela": "", "haiku": [], "sonnet": [],
            "salvos": 0, "erros": ["input vazio"],
            "via": via, "user_id": user_id,
        }

    hash_j = _hash_janela(input_texto)

    modelo_haiku = os.getenv("MODEL_CURADOR_HAIKU", "claude-haiku-4-5")
    modelo_sonnet = os.getenv("MODEL_CURADOR_SONNET", "claude-sonnet-4-6")

    haiku_frags, sonnet_frags = await asyncio.gather(
        _extrair_via_modelo(input_texto, prompt_template, modelo_haiku, via, max_frags_por_modelo),
        _extrair_via_modelo(input_texto, prompt_template, modelo_sonnet, via, max_frags_por_modelo),
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
                    },
                )
                salvos += 1
            except Exception as e:
                erros.append(f"ingestar {curador}: {str(e)[:120]}")

    await asyncio.gather(
        _salvar_lista(haiku_frags, "haiku"),
        _salvar_lista(sonnet_frags, "sonnet"),
    )

    return {
        "hash_janela": hash_j,
        "haiku": haiku_frags,
        "sonnet": sonnet_frags,
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
            "hash_janela": "", "haiku": [], "sonnet": [],
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
