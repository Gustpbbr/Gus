"""
Fluxo determinístico de OS Dimagem — versão refinada da proposta do TioGu.

ARQUITETURA:
1. _e_os_dimagem(image_bytes, caption)   — detecta via caption + Haiku binário (cache hash)
2. _extrair_os(image_bytes)              — extrai JSON via Haiku Vision
3. _normalizar_convenio(raw, dict)       — lookup em dicionário versionado
4. _formatar_linha(dados, convenio_norm) — uma linha de tabela markdown
5. _append_linha_no_md(md, linha)        — append cirúrgico, preserva edições manuais
6. processar_os_dimagem(image_bytes, caption) — orquestra. None se não é OS / falha extração.

INTEGRAÇÃO (futura, em bot.py — NÃO ativada ainda):

    from gus.dimagem import processar_os_dimagem

    async def handle_photo(update, context):
        ...
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        async with httpx.AsyncClient(timeout=30) as c:
            img_bytes = (await c.get(file.file_path)).content

        resp = await processar_os_dimagem(img_bytes, update.message.caption or "")
        if resp:
            await update.message.reply_text(resp)
            return  # não passa pro Sonnet

        # fallback: fluxo conversacional normal
        content = await processar_imagem(file.file_path, update.message.caption or "")
        await _responder(update, chat_id, content, ...)

DEDUPLICAÇÃO:
- Por número de OS: persiste em /app/data/dimagem_os_processadas.json (volume Railway).
- Por nome dentro do MD do dia: lê o MD e checa case-insensitive.

CUSTOS:
- Detecção (Haiku binário): ~$0.001/foto.
- Extração (Haiku JSON):    ~$0.002/foto.
- Total: ~$0.003/foto. 5 fotos/dia = ~$0.45/mês.

DECISÕES vs proposta original do TioGu:
- Modelo: Haiku 4.5 (não Opus 4.5 inexistente)
- Reusa tools._read_from_github e tools._save_to_github (mantém scan sensível)
- Detecção visual real (não só caption)
- Dedup persistente em disco (não em memória global)
- Convênios em JSON versionado (não regex frágil no código)
- Append cirúrgico (não regex de tabela frágil)
- Valor extraído da própria foto (não tabela hardcoded)
- Fallback graceful: retorna None pra caller decidir cair no Sonnet
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

import httpx

from gus.tools import _read_from_github, _save_to_github

logger = logging.getLogger(__name__)

BRT = timezone(timedelta(hours=-3))
MODEL = "claude-haiku-4-5"

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
  "unidade": "Dimagem Taquara" | "Dimagem São Gonçalo" | null
}

Regras:
- numero_os: só o da OS principal, NÃO da anestesia.
- exames: lista de strings. EXCLUA qualquer item com a palavra "ANESTESIA".
- convenio: copie LITERALMENTE como impresso (ex: "ASSIM TAQUARA"). Não normalize.
- valor_brl: número inteiro se houver valor de cobrança claro (ex: "R$ 220" -> 220).
- unidade: identifique pelo cabeçalho/endereço se aparecer. Caso contrário, null.
- Campos não legíveis: null."""


# ---------------------------------------------------------------------------
# DETECÇÃO
# ---------------------------------------------------------------------------

async def _e_os_dimagem(image_bytes: bytes, caption: str) -> bool:
    """Detecta se a imagem é uma OS Dimagem.

    Ordem: caption (custo zero) -> cache de hash -> Haiku binário.
    """
    cap = (caption or "").upper()
    if any(k in cap for k in ("DIMAGEM", "ORDEM DE SERVI", " OS ", "OS:", "/OS")):
        return True

    h = hashlib.sha256(image_bytes).hexdigest()
    if h in _DETECCAO_CACHE:
        return _DETECCAO_CACHE[h]

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return False

    img_b64 = base64.b64encode(image_bytes).decode()
    payload = {
        "model": MODEL,
        "max_tokens": 8,
        "system": PROMPT_DETECCAO,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": img_b64}},
                {"type": "text", "text": "Esta imagem é uma OS Dimagem?"},
            ],
        }],
    }
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages", json=payload, headers=headers
            )
        if resp.status_code != 200:
            logger.warning(f"Detecção Haiku status {resp.status_code}: {resp.text[:200]}")
            return False
        texto = resp.json()["content"][0]["text"].strip().lower()
        eh_os = texto.startswith("sim")
        _DETECCAO_CACHE[h] = eh_os
        return eh_os
    except Exception as e:
        logger.warning(f"Detecção Haiku falhou: {e}")
        return False


# ---------------------------------------------------------------------------
# EXTRAÇÃO
# ---------------------------------------------------------------------------

async def _extrair_os(image_bytes: bytes) -> dict | None:
    """Chama Haiku Vision com prompt fixo. Retorna dict parseado ou None."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return None

    img_b64 = base64.b64encode(image_bytes).decode()
    payload = {
        "model": MODEL,
        "max_tokens": 800,
        "system": PROMPT_EXTRACAO,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": img_b64}},
                {"type": "text", "text": "Extraia."},
            ],
        }],
    }
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages", json=payload, headers=headers
            )
        if resp.status_code != 200:
            logger.error(f"Extração Haiku status {resp.status_code}: {resp.text[:300]}")
            return None
        texto = resp.json()["content"][0]["text"].strip()
        match = re.search(r"\{[\s\S]*\}", texto)
        if not match:
            logger.warning(f"Haiku não retornou JSON: {texto[:200]}")
            return None
        return json.loads(match.group())
    except json.JSONDecodeError as e:
        logger.warning(f"JSON inválido na extração: {e}")
        return None
    except Exception as e:
        logger.error(f"Erro na extração: {e}")
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
