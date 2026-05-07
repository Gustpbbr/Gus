"""
Fluxo determinístico de OS Dimagem.

ARQUITETURA:
1. _e_os_dimagem(image_bytes, caption)   — detecta via caption + gpt-4o-mini Vision binário (cache hash)
2. _extrair_os(image_bytes)              — extrai JSON via gpt-4o-mini Vision
3. _normalizar_convenio(raw, dict)       — lookup em dicionário versionado
4. _formatar_linha(dados, convenio_norm) — uma linha de tabela markdown
5. _append_linha_no_md(md, linha)        — append cirúrgico, preserva edições manuais
6. processar_os_dimagem / analisar_os_dimagem / salvar_os_dimagem
   — orquestra. None se não é OS / falha extração.

INTEGRAÇÃO (em produção desde 28/04, no `gus/bot.py:handle_photo` via
modo confirmação prévia: `analisar_os_dimagem` extrai e devolve preview
pra Gustavo confirmar com "sim/ok/manda" antes de `salvar_os_dimagem`).

DEDUPLICAÇÃO:
- Por número de OS: persiste em /app/data/dimagem_os_processadas.json (volume Railway).
- Por nome dentro do MD do dia: lê o MD e checa case-insensitive.

CUSTOS (gus-29 Fase 2 — 29/04/2026):
- Detecção (gpt-4o-mini Vision binário): ~$0.0001/foto.
- Extração (gpt-4o-mini Vision JSON):    ~$0.0002/foto.
- Total: ~$0.0003/foto. 5 fotos/dia = ~$0.05/mês.

Histórico:
- até 28/04: Haiku Anthropic Vision (~$0.45/mês, 5 fotos/dia).
- 29/04 (gus-29 Fase 2): substituído por gpt-4o-mini Vision (~10x mais barato).
  Resiliente a crédito Anthropic — se Anthropic ficar offline, fluxo Dimagem
  continua. Gate de confiança ("alta/media/baixa" no prompt) protege caso
  clínico igual antes.

DECISÕES vs proposta original do TioGu:
- Modelo: gpt-4o-mini Vision (era Haiku 4.5 Anthropic; Sonnet 4.5/Opus 4.5 não existem)
- Detail "high" no image_url: usa mais tokens mas garante OCR de texto fino
- Reusa tools._read_from_github e tools._save_to_github (mantém scan sensível)
- Detecção visual real (não só caption)
- Dedup persistente em disco (não em memória global)
- Convênios em JSON versionado (não regex frágil no código)
- Append cirúrgico (não regex de tabela frágil)
- Valor extraído da própria foto (não tabela hardcoded)
- Fallback graceful: retorna None pra caller decidir cair no fluxo conversacional
"""

import asyncio
import base64
import hashlib
import json
import logging
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

from openai import AsyncOpenAI

from gus.tools import _read_from_github, _save_to_github

logger = logging.getLogger(__name__)

BRT = timezone(timedelta(hours=-3))
# gus-29 Fase 2 (29/04/2026): Haiku Anthropic Vision → gpt-4o-mini OpenAI Vision.
# Override via env MODEL_DIMAGEM. Custos caem ~10x e o gate de confiança
# (alta/media/baixa no prompt) protege caso clínico igual.
MODEL = os.getenv("MODEL_DIMAGEM", "gpt-4o-mini")

_openai_client: Optional[AsyncOpenAI] = None


def _get_openai() -> AsyncOpenAI:
    """Lazy-init do client OpenAI. Compartilhado entre detecção e extração."""
    global _openai_client
    if _openai_client is None:
        _openai_client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            timeout=60.0,
        )
    return _openai_client


async def _chamar_openai_vision(
    image_bytes: bytes,
    system_prompt: str,
    user_text: str,
    max_tokens: int,
) -> Optional[str]:
    """Chama gpt-4o-mini Vision com imagem + prompt. Retorna texto da resposta
    ou None em falha (sem API key, exception, status != 200).

    Detail "high" pra OS Dimagem (texto pequeno em formulário) — usa mais
    tokens mas garante OCR melhor. Default seria "auto" que pode escolher
    "low" (~85 tokens) e perder texto fino.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    img_b64 = base64.b64encode(image_bytes).decode()
    try:
        oai = _get_openai()
        response = await oai.chat.completions.create(
            model=MODEL,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_b64}",
                                "detail": "high",
                            },
                        },
                        {"type": "text", "text": user_text},
                    ],
                },
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.warning(f"OpenAI Vision falhou: {e}")
        return None

_DATA_DIR = "/app/data" if os.path.isdir("/app/data") else "."
_OS_DEDUP_FILE = Path(_DATA_DIR) / "dimagem_os_processadas.json"

# Cache de detecção em memória (hash SHA-256 da imagem -> bool)
_DETECCAO_CACHE: dict[str, bool] = {}

# Convênios — fonte de verdade em dimagem/convenios.json. Fallback embutido
# pro caso de o arquivo ainda não existir ou falhar leitura.
_CONVENIOS_PATH = "dimagem/convenios.json"
_CONVENIOS_FALLBACK = {
    "ASSIM TAQUARA": "Assim Taquara",
    "ASSIM SAO GONCALO": "Assim São Gonçalo",
    "ASSIM SÃO GONÇALO": "Assim São Gonçalo",
    "INTERMEDICA NOVA IGUACU": "Intermédica – Nova Iguaçu",
    "INTERMÉDICA NOVA IGUAÇU": "Intermédica – Nova Iguaçu",
    "INTERMEDICA N IGUACU": "Intermédica – Nova Iguaçu",
    "INTERMEDICA - NOVA IGUACU": "Intermédica – Nova Iguaçu",
    "LEVE SAUDE": "Leve Saúde",
    "LEVE SAÚDE": "Leve Saúde",
    "LEVE SAUDE OPERADORA": "Leve Saúde",
    "MEDSENIOR": "MedSenior",
    "MED SENIOR": "MedSenior",
    "UNIMED": "Unimed",
}
_convenios_cache: dict[str, str] | None = None

PROMPT_DETECCAO = """Você analisa imagens. Responda APENAS com "sim" ou "nao".

Pergunta: A imagem é uma Ordem de Serviço médica ou comprovante de agendamento de exame de imagem (RM, TC, US) emitido pelo Dimagem?

Indicadores que confirmam (qualquer um basta):
- Cabeçalho com "Dimagem"
- Tabela com paciente + exame de imagem (RM/TC/US) + convênio
- Número de OS no formato "XXXXXXX-XXX"

Resposta em uma palavra:"""

PROMPT_EXTRACAO = """Você é um extrator de dados de Ordens de Serviço médicas do Dimagem.
Analise a imagem e retorne APENAS um JSON válido. Sem markdown, sem comentários, sem prosa.

Schema obrigatório:
{
  "numero_os": "XXXXXXX-XXX" | null,
  "nome_paciente": "NOME COMPLETO" | null,
  "data_exame": "DD/MM/AAAA" | null,
  "exames": ["RM CRANIO (ENCEFALO)", "..."],
  "convenio": "string copiada literalmente" | null,
  "valor_brl": int | null,
  "unidade": "Dimagem Taquara" | "Dimagem São Gonçalo" | null,
  "confianca": "alta" | "media" | "baixa",
  "motivo_incerteza": "string curta" | null
}

Regras:
- numero_os: só o da OS principal, NÃO da anestesia.
- exames: lista de strings. EXCLUA qualquer item com a palavra "ANESTESIA".
- convenio: copie LITERALMENTE como impresso (ex: "ASSIM TAQUARA"). Não normalize.
- valor_brl: número inteiro se houver valor de cobrança claro (ex: "R$ 220" -> 220).
- unidade: identifique pelo cabeçalho/endereço se aparecer. Caso contrário, null.
- Campos não legíveis: null.

CONFIANÇA — REGRA CRÍTICA (impacta prontuário médico, não chute):
- "alta":   imagem nítida, texto reto e bem legível, NOME do paciente lido com 100% de
            certeza letra por letra. Convênio claro. Você consegue ler o documento
            inteiro como se estivesse na mão.
- "media":  algum borrão leve, parte do documento cortada mas o nome do paciente
            está claro, OU letras isoladas com leve ambiguidade que o contexto
            resolve (ex: "0" vs "O"). Aceita-se.
- "baixa":  documento rotacionado >15° (deitado, de cabeça pra baixo), texto
            embaçado/iluminação ruim que torna o NOME ambíguo, parte do nome
            cortada/coberta, ou qualquer dúvida sobre QUEM é o paciente.
            QUALQUER incerteza sobre o nome → "baixa". Falso positivo no nome
            corrompe prontuário — prefira pedir reenvio.

motivo_incerteza: se confianca for "baixa" ou "media", explique em 1 frase curta
o que está ruim (ex: "imagem rotacionada 90°", "nome parcialmente coberto",
"qualidade insuficiente para ler com certeza"). Null se confianca = "alta"."""

CONTEXTO_TEMPLATE = """

CONTEXTO ADICIONAL — pacientes já registrados no MD de hoje ({hoje_str}):
{lista_atual}

Use isso pra:
- Manter convênios consistentes com a grafia já usada no dia
- Detectar se a OS na imagem já foi registrada (nome+exame+data iguais)
- Manter padrões de unidade do dia"""


# ---------------------------------------------------------------------------
# DETECÇÃO
# ---------------------------------------------------------------------------

async def _e_os_dimagem(image_bytes: bytes, caption: str) -> bool:
    """Detecta se a imagem é uma OS Dimagem.

    Ordem: caption (custo zero) -> cache de hash -> gpt-4o-mini Vision binário.
    """
    cap = (caption or "").upper()
    if any(k in cap for k in ("DIMAGEM", "ORDEM DE SERVI", " OS ", "OS:", "/OS")):
        return True

    h = hashlib.sha256(image_bytes).hexdigest()
    if h in _DETECCAO_CACHE:
        return _DETECCAO_CACHE[h]

    texto = await _chamar_openai_vision(
        image_bytes=image_bytes,
        system_prompt=PROMPT_DETECCAO,
        user_text="Esta imagem é uma OS Dimagem?",
        max_tokens=8,
    )
    if not texto:
        return False

    eh_os = texto.strip().lower().startswith("sim")
    _DETECCAO_CACHE[h] = eh_os
    return eh_os


# ---------------------------------------------------------------------------
# EXTRAÇÃO
# ---------------------------------------------------------------------------

def _extrair_pacientes_atual(md: str) -> str:
    """Extrai linhas de paciente do MD pra usar como contexto pro Vision.
    Formato compacto: cada linha = uma row da tabela."""
    if not md:
        return ""
    linhas = []
    for line in md.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        if s.startswith("|--") or "---" in s:
            continue
        if "Nome" in s and "Exame" in s:  # cabeçalho
            continue
        if s.count("|") >= 4:
            linhas.append(s)
    return "\n".join(linhas[:25])  # limita pra 25 pacientes (custo)


async def _extrair_os(image_bytes: bytes, contexto_md: str = "") -> dict | None:
    """Chama gpt-4o-mini Vision com prompt fixo + contexto opcional do MD do dia.

    Quando `contexto_md` é passado (lista de pacientes já registrados hoje),
    o prompt ganha referência pra: manter grafia de convênio, detectar
    duplicata, e padronizar unidade.
    """
    system_prompt = PROMPT_EXTRACAO
    if contexto_md.strip():
        hoje_str = datetime.now(BRT).strftime("%d/%m/%Y")
        system_prompt += CONTEXTO_TEMPLATE.format(
            hoje_str=hoje_str,
            lista_atual=contexto_md.strip()[:1500],
        )

    texto = await _chamar_openai_vision(
        image_bytes=image_bytes,
        system_prompt=system_prompt,
        user_text="Extraia.",
        max_tokens=800,
    )
    if not texto:
        return None

    texto = texto.strip()
    match = re.search(r"\{[\s\S]*\}", texto)
    if not match:
        logger.warning(f"Vision não retornou JSON: {texto[:200]}")
        return None
    try:
        return json.loads(match.group())
    except json.JSONDecodeError as e:
        logger.warning(f"JSON inválido na extração: {e}")
        return None


# ---------------------------------------------------------------------------
# DEDUP PERSISTENTE
# ---------------------------------------------------------------------------

def _carregar_os_processadas() -> dict[str, list[str]]:
    if not _OS_DEDUP_FILE.exists():
        return {}
    try:
        return json.loads(_OS_DEDUP_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _salvar_os_processadas(data: dict[str, list[str]]) -> None:
    """Atomic write. Silencioso em falha (não interrompe fluxo)."""
    try:
        _OS_DEDUP_FILE.parent.mkdir(parents=True, exist_ok=True)
        tmp = _OS_DEDUP_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, _OS_DEDUP_FILE)
    except Exception as e:
        logger.warning(f"Falha ao salvar OS processadas: {e}")


# ---------------------------------------------------------------------------
# CONVÊNIOS
# ---------------------------------------------------------------------------

async def _carregar_convenios() -> dict[str, str]:
    """Carrega dicionário de convênios. Cache por boot do processo."""
    global _convenios_cache
    if _convenios_cache is not None:
        return _convenios_cache

    raw = await _read_from_github(_CONVENIOS_PATH)
    if raw and raw.lstrip().startswith("{"):
        try:
            _convenios_cache = json.loads(raw)
            return _convenios_cache
        except Exception:
            logger.warning(f"{_CONVENIOS_PATH} malformado — usando fallback embutido.")

    _convenios_cache = dict(_CONVENIOS_FALLBACK)
    return _convenios_cache


def _normalizar_convenio(raw: str, dicionario: dict[str, str]) -> str:
    """Lookup case-insensitive com tolerância a hífens. Fallback: title-case."""
    if not raw:
        return ""
    chave = re.sub(r"\s+", " ", raw.strip().upper())
    chave = chave.replace("–", "-").replace("—", "-")
    if chave in dicionario:
        return dicionario[chave]
    # Tenta sem hífens
    chave_simples = re.sub(r"\s+", " ", chave.replace("-", " ").strip())
    if chave_simples in dicionario:
        return dicionario[chave_simples]
    logger.info(
        f"Convênio não mapeado: '{raw}' (chave '{chave}'). "
        f"Adicione em {_CONVENIOS_PATH} pra próxima vez."
    )
    return raw.title()


# ---------------------------------------------------------------------------
# MARKDOWN
# ---------------------------------------------------------------------------

def _formatar_linha(dados: dict, convenio_norm: str) -> str:
    nome = (dados.get("nome_paciente") or "").strip()
    data_ex = (dados.get("data_exame") or "").strip()
    exames = [
        e.strip() for e in (dados.get("exames") or [])
        if e and "ANESTESIA" not in e.upper()
    ]
    exames_str = " + ".join(exames)
    valor = dados.get("valor_brl")
    valor_str = f"R$ {valor}" if isinstance(valor, (int, float)) else "—"
    return f"| {nome} | {data_ex} | {exames_str} | {convenio_norm} | {valor_str} |"


def _ja_existe_paciente(md: str, nome: str) -> bool:
    """Detecta se o nome (case-insensitive) já está em alguma linha de tabela."""
    nome_up = nome.upper().strip()
    for line in md.splitlines():
        if line.lstrip().startswith("|") and nome_up in line.upper():
            return True
    return False


def _append_linha_no_md(md_existente: str, linha_nova: str) -> str:
    """Append cirúrgico — insere depois da última linha de tabela.

    Preserva tudo que vem antes (frontmatter, cabeçalhos, prosa) e tudo que
    vem depois (observações, totais manuais, links). Se não achar tabela,
    anexa cabeçalho + linha ao final.
    """
    linhas = md_existente.splitlines()
    ultimo_pipe_idx = -1
    for i, l in enumerate(linhas):
        s = l.strip()
        if s.startswith("|") and not s.startswith("|--") and "---" not in s:
            ultimo_pipe_idx = i

    if ultimo_pipe_idx == -1:
        cabecalho = (
            "\n| Nome | Data | Exame | Plano | Valor |\n"
            "|---|---|---|---|---|\n"
        )
        return md_existente.rstrip() + cabecalho + linha_nova + "\n"

    linhas.insert(ultimo_pipe_idx + 1, linha_nova)
    return "\n".join(linhas) + ("" if md_existente.endswith("\n") else "\n")


def _criar_md_inicial(data_iso: str, data_str: str, linha: str, unidade: str) -> str:
    return (
        f"---\n"
        f"capturado_em: {data_iso}\n"
        f"via: telegram\n"
        f"tipo: dia-dimagem\n"
        f"unidade: {unidade}\n"
        f"---\n\n"
        f"# Pacientes — {data_str}\n\n"
        f"| Nome | Data | Exame | Plano | Valor |\n"
        f"|---|---|---|---|---|\n"
        f"{linha}\n"
    )


def _inferir_unidade(dados: dict, convenio_norm: str) -> str:
    explicit = (dados.get("unidade") or "").strip()
    if explicit:
        return explicit
    if "Gonçalo" in convenio_norm or "São Gonçalo" in convenio_norm:
        return "Dimagem São Gonçalo"
    if "Taquara" in convenio_norm:
        return "Dimagem Taquara"
    return "Dimagem"


# ---------------------------------------------------------------------------
# ORQUESTRAÇÃO
# ---------------------------------------------------------------------------

async def processar_os_dimagem(image_bytes: bytes, caption: str = "") -> str | None:
    """Fluxo determinístico de OS Dimagem.

    Retorno:
    - str: mensagem pra responder no Telegram (sucesso ou skip explícito de dedup).
    - None: imagem NÃO é OS Dimagem OU extração falhou. Caller cai no fluxo
      conversacional normal (Sonnet) — isso é graceful degradation.
    """
    if not await _e_os_dimagem(image_bytes, caption):
        return None

    dados = await _extrair_os(image_bytes)
    if not dados:
        return None

    nome = (dados.get("nome_paciente") or "").strip()
    exames = [
        e for e in (dados.get("exames") or [])
        if e and "ANESTESIA" not in e.upper()
    ]
    convenio_raw = (dados.get("convenio") or "").strip()
    numero_os = (dados.get("numero_os") or "").strip()

    if not nome or not exames or not convenio_raw:
        return None

    dicionario = await _carregar_convenios()
    convenio_norm = _normalizar_convenio(convenio_raw, dicionario)

    hoje_iso = datetime.now(BRT).strftime("%Y-%m-%d")
    hoje_str = datetime.now(BRT).strftime("%d/%m/%Y")

    processadas = _carregar_os_processadas()
    do_dia = set(processadas.get(hoje_iso, []))
    if numero_os and numero_os in do_dia:
        return f"OS {numero_os} ({nome}) já registrada hoje. Ignorada."

    path = f"dimagem/dia/{hoje_iso}.md"
    md_existente = await _read_from_github(path)
    arquivo_existe = md_existente and not md_existente.startswith("Arquivo não encontrado")

    if arquivo_existe:
        if _ja_existe_paciente(md_existente, nome):
            return f"{nome} já está no arquivo do dia. Ignorado."
        linha = _formatar_linha(dados, convenio_norm)
        novo_md = _append_linha_no_md(md_existente, linha)
    else:
        linha = _formatar_linha(dados, convenio_norm)
        unidade = _inferir_unidade(dados, convenio_norm)
        novo_md = _criar_md_inicial(hoje_iso, hoje_str, linha, unidade)

    resultado = await _save_to_github(hoje_iso, novo_md, "dimagem/dia")
    if "Erro" in resultado or "ATENÇÃO" in resultado:
        return resultado

    if numero_os:
        do_dia.add(numero_os)
        processadas[hoje_iso] = sorted(do_dia)
        _salvar_os_processadas(processadas)

    valor = dados.get("valor_brl")
    valor_str = f" — R$ {valor}" if isinstance(valor, (int, float)) else ""
    return (
        f"✅ {nome}: {' + '.join(exames)} ({convenio_norm}{valor_str}) "
        f"registrado em `{path}`."
    )


# ---------------------------------------------------------------------------
# MODO COM CONFIRMAÇÃO PRÉVIA (split entre analisar + salvar)
# ---------------------------------------------------------------------------

async def analisar_os_dimagem(image_bytes: bytes, caption: str = "") -> dict | None:
    """Modo PREVIEW: extrai dados, lê MD do dia, monta mensagem pro Telegram
    com (a) novo paciente extraído, (b) lista atual do dia, (c) pergunta de
    confirmação. NÃO salva — quem salva é `salvar_os_dimagem(pending)`.

    Returns:
        dict com {preview_text, dados, convenio_norm, exames, nome} pra
        guardar como state pendente, OU None se imagem não é OS Dimagem ou
        extração falhou (caller cai no fluxo Sonnet normal).
    """
    if not await _e_os_dimagem(image_bytes, caption):
        return None

    hoje_iso = datetime.now(BRT).strftime("%Y-%m-%d")
    hoje_str = datetime.now(BRT).strftime("%d/%m/%Y")
    path = f"dimagem/dia/{hoje_iso}.md"

    md_existente = await _read_from_github(path)
    arquivo_existe = bool(md_existente) and not md_existente.startswith("Arquivo não encontrado")
    contexto = _extrair_pacientes_atual(md_existente) if arquivo_existe else ""

    # Extrai com contexto (B do plano A+B)
    dados = await _extrair_os(image_bytes, contexto_md=contexto)
    if not dados:
        return None

    # Confiança da extração — gate crítico contra prontuário corrompido (#4 inbox).
    # "baixa" → bloqueia preview e pede reenvio (sem state pendente, sem chance
    # de Gustavo confirmar nome trocado por engano). Default conservador "media".
    confianca = (dados.get("confianca") or "media").strip().lower()
    motivo = (dados.get("motivo_incerteza") or "").strip()
    if confianca not in ("alta", "media", "baixa"):
        confianca = "media"

    if confianca == "baixa":
        msg = (
            "Não consegui ler essa OS com certeza"
            + (f" ({motivo})" if motivo else "")
            + ". Pode reenviar a foto na posição correta, "
            "com boa iluminação e sem borrão? Não vou registrar nada até ler com clareza."
        )
        logger.warning(
            f"OCR Dimagem confiança baixa — bloqueado. motivo='{motivo}' "
            f"nome_extraido='{(dados.get('nome_paciente') or '').strip()}'"
        )
        return {"pedir_reenvio": True, "preview_text": msg, "confianca": "baixa", "motivo": motivo}

    nome = (dados.get("nome_paciente") or "").strip()
    exames = [
        e for e in (dados.get("exames") or [])
        if e and "ANESTESIA" not in e.upper()
    ]
    convenio_raw = (dados.get("convenio") or "").strip()

    if not nome or not exames or not convenio_raw:
        return None

    dicionario = await _carregar_convenios()
    convenio_norm = _normalizar_convenio(convenio_raw, dicionario)

    valor = dados.get("valor_brl")
    valor_str = f"R$ {valor}" if isinstance(valor, (int, float)) else "—"
    exames_str = " + ".join(exames)

    # Preview (A do plano A+B). Quando confiança = "media", inclui aviso visível
    # pra Gustavo conferir o nome com mais atenção antes de confirmar.
    preview = f"OS Dimagem detectada ({hoje_str}):\n"
    preview += f"  + {nome} · {exames_str} · {convenio_norm} · {valor_str}\n\n"
    if confianca == "media":
        aviso = "⚠️ Confiança média na leitura"
        if motivo:
            aviso += f" ({motivo})"
        preview += aviso + ". Confere o nome antes de confirmar.\n\n"
    if contexto:
        n_existentes = len(contexto.splitlines())
        preview += f"Pacientes já no MD do dia ({n_existentes}):\n{contexto}\n\n"
    else:
        preview += "Primeiro paciente do dia.\n\n"
    preview += "Confirma o save? Responda: sim/ok/manda  —  ou: não/cancela."

    return {
        "preview_text": preview,
        "dados": dados,
        "convenio_norm": convenio_norm,
        "exames": exames,
        "nome": nome,
        "hoje_iso": hoje_iso,
        "hoje_str": hoje_str,
        "confianca": confianca,
    }


async def salvar_os_dimagem(pending: dict) -> str:
    """Executa o save com dados já extraídos e validados em `analisar_os_dimagem`.
    Aplica as mesmas verificações de dedup que `processar_os_dimagem`."""
    dados = pending["dados"]
    nome = pending["nome"]
    exames = pending["exames"]
    convenio_norm = pending["convenio_norm"]
    hoje_iso = pending.get("hoje_iso") or datetime.now(BRT).strftime("%Y-%m-%d")
    hoje_str = pending.get("hoje_str") or datetime.now(BRT).strftime("%d/%m/%Y")

    numero_os = (dados.get("numero_os") or "").strip()
    processadas = _carregar_os_processadas()
    do_dia = set(processadas.get(hoje_iso, []))
    if numero_os and numero_os in do_dia:
        return f"OS {numero_os} ({nome}) já registrada hoje. Ignorada."

    path = f"dimagem/dia/{hoje_iso}.md"
    md_existente = await _read_from_github(path)
    arquivo_existe = bool(md_existente) and not md_existente.startswith("Arquivo não encontrado")

    if arquivo_existe:
        if _ja_existe_paciente(md_existente, nome):
            return f"{nome} já está no arquivo do dia. Ignorado."
        linha = _formatar_linha(dados, convenio_norm)
        novo_md = _append_linha_no_md(md_existente, linha)
    else:
        linha = _formatar_linha(dados, convenio_norm)
        unidade = _inferir_unidade(dados, convenio_norm)
        novo_md = _criar_md_inicial(hoje_iso, hoje_str, linha, unidade)

    resultado = await _save_to_github(hoje_iso, novo_md, "dimagem/dia")
    if "Erro" in resultado or "ATENÇÃO" in resultado:
        return resultado

    if numero_os:
        do_dia.add(numero_os)
        processadas[hoje_iso] = sorted(do_dia)
        _salvar_os_processadas(processadas)

    valor = dados.get("valor_brl")
    valor_str = f" — R$ {valor}" if isinstance(valor, (int, float)) else ""
    return (
        f"✅ {nome}: {' + '.join(exames)} ({convenio_norm}{valor_str}) "
        f"salvo em `{path}`."
    )
