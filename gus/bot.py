import os
import time
import json
import asyncio
import logging
from collections import deque
from pathlib import Path
from telegram import Update
from telegram.ext import ContextTypes
from gus.llm import gerar_resposta, gerar_resumo_turnos
from gus.logger import registrar, custo_mes_atual, stats_mes_atual
from gus.memory import buscar_memorias, salvar_memorias
from gus.media import processar_imagem, processar_pdf, processar_docx, processar_xlsx, transcrever_audio
from gus.resumo_log import append_resumo_async
from gus.dimagem import analisar_os_dimagem, salvar_os_dimagem
import re as _re_bot
import httpx as _httpx_bot

logger = logging.getLogger(__name__)

AUTHORIZED_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
HARD_LIMIT = float(os.getenv("HARD_LIMIT_USD_MONTH", "30"))
MAX_HISTORY = int(os.getenv("MAX_HISTORY_MESSAGES", "40"))  # 20 turnos
TURNOS_PARA_RESUMO = int(os.getenv("TURNOS_PARA_RESUMO", "3"))
RATE_LIMIT_MSG_PER_MINUTE = int(os.getenv("RATE_LIMIT_MSG_PER_MINUTE", "20"))

# Auto-detect volume Railway em /app/data. Se montado, persiste state entre redeploys.
_DATA_DIR = "/app/data" if os.path.isdir("/app/data") else None
STATE_FILE = os.getenv("STATE_FILE") or (f"{_DATA_DIR}/bot_state.json" if _DATA_DIR else "")

# Estado em memória por chat_id (carregado do disco se disponível, senão zerado)
conversation_histories: dict[str, list] = {}
turn_counters: dict[str, int] = {}
last_saved_turn: dict[str, int] = {}
message_timestamps: dict[str, deque] = {}

# Fluxo dimagem: OS extraídas aguardando confirmação ("sim"/"ok") do Gustavo.
# Persistido em bot_state.json pra sobreviver redeploy do Railway.
dimagem_pending: dict[str, dict] = {}

_DIMAGEM_CONFIRMA_RE = _re_bot.compile(
    r"^\s*(sim|s|ok|okay|confirma|confirme|confirmo|manda|pode|salva|salve|vai|bora|positivo|1|👍)\s*[!.]*\s*$",
    _re_bot.IGNORECASE,
)
_DIMAGEM_CANCELA_RE = _re_bot.compile(
    r"^\s*(n[ãa]o|cancela|ignora|esquece|deixa\s+pr[ao]\s+l[áa]|aborta?)",
    _re_bot.IGNORECASE,
)


def _load_state() -> None:
    """Carrega state persistido do disco (se volume Railway está montado)."""
    if not STATE_FILE or not os.path.exists(STATE_FILE):
        return
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        conversation_histories.update(data.get("conversations", {}))
        turn_counters.update(data.get("turn_counters", {}))
        last_saved_turn.update(data.get("last_saved_turn", {}))
        for chat_id, ts_list in data.get("message_timestamps", {}).items():
            message_timestamps[chat_id] = deque(ts_list)
        dimagem_pending.update(data.get("dimagem_pending", {}))
        logger.info(
            f"State carregado de {STATE_FILE}: "
            f"{len(conversation_histories)} chats, "
            f"{sum(turn_counters.values())} turnos acumulados, "
            f"{len(dimagem_pending)} OS dimagem pendentes"
        )
    except Exception as e:
        logger.warning(f"Falha ao carregar state de {STATE_FILE}: {e}")


def _save_state() -> None:
    """Persiste state no disco. Silencioso em falhas (não interrompe resposta)."""
    if not STATE_FILE:
        return
    try:
        Path(STATE_FILE).parent.mkdir(parents=True, exist_ok=True)
        data = {
            "conversations": dict(conversation_histories),
            "turn_counters": dict(turn_counters),
            "last_saved_turn": dict(last_saved_turn),
            "message_timestamps": {cid: list(ts) for cid, ts in message_timestamps.items()},
            "dimagem_pending": dict(dimagem_pending),
        }
        # Write atômico via tmp + replace pra não corromper em caso de kill
        tmp = STATE_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        os.replace(tmp, STATE_FILE)
    except Exception as e:
        logger.warning(f"Falha ao salvar state em {STATE_FILE}: {e}")


# Carrega state ao importar o módulo (startup do bot)
_load_state()


def _texto_de_content(content) -> str:
    """Extrai as partes de texto de um content (str ou list multimodal)."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        partes = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                t = block.get("text", "")
                if t:
                    partes.append(t)
        return " ".join(partes).strip()
    return ""


def _query_mem0_contextual(history: list[dict], fallback: str) -> str:
    """Monta query do Mem0 a partir das últimas 3 mensagens do Gustavo.
    Ajuda a busca semântica quando a mensagem atual é curta ou referencial."""
    textos_user = []
    for msg in reversed(history):
        if msg.get("role") != "user":
            continue
        t = _texto_de_content(msg.get("content"))
        if t:
            textos_user.append(t)
        if len(textos_user) >= 3:
            break
    textos_user.reverse()
    return " ".join(textos_user) if textos_user else fallback


async def _resumir_e_salvar(chat_id: str, trecho: list[dict]) -> None:
    """Gera resumo extrativo do trecho e salva no Mem0. Silencioso em falhas.

    Também registra cada evento (salvo/descartado/erro) no log auditável
    em _log/resumos-mem0/AAAA-MM-DD.md (Gustavo fiscaliza no Obsidian).
    """
    try:
        resumo = await gerar_resumo_turnos(trecho)
        if resumo and resumo.strip().lower() != "sem conteúdo relevante":
            await salvar_memorias([{"role": "user", "content": resumo}])
            logger.info(f"Resumo salvo no Mem0 (chat {chat_id}, {len(resumo)} chars)")
            append_resumo_async(resumo, len(trecho), "salvo")
        else:
            logger.info(f"Resumo vazio ou sem conteúdo relevante (chat {chat_id})")
            append_resumo_async("(sem conteúdo relevante)", len(trecho), "descartado")
    except Exception as e:
        logger.warning(f"Resumo falhou (chat {chat_id}): {e}")
        append_resumo_async(f"(erro: {str(e)[:120]})", len(trecho), "erro")


def _autorizado(chat_id: str) -> bool:
    if not AUTHORIZED_CHAT_ID:
        return False  # nega tudo até configurar TELEGRAM_CHAT_ID
    return chat_id == AUTHORIZED_CHAT_ID


async def _verificar_limite(update: Update) -> bool:
    custo_atual = custo_mes_atual()
    if custo_atual >= HARD_LIMIT:
        await update.message.reply_text(
            f"Atingi o limite mensal de US${HARD_LIMIT:.0f}. "
            f"Desligando chamadas até o próximo mês."
        )
        return False
    return True


async def _verificar_rate_limit(update: Update, chat_id: str) -> bool:
    """Rate limit: até RATE_LIMIT_MSG_PER_MINUTE por janela de 60s."""
    agora = time.time()
    timestamps = message_timestamps.setdefault(chat_id, deque())
    while timestamps and timestamps[0] < agora - 60:
        timestamps.popleft()
    if len(timestamps) >= RATE_LIMIT_MSG_PER_MINUTE:
        await update.message.reply_text(
            f"Tô recebendo muito rápido ({len(timestamps)}+ msgs no último minuto). "
            f"Aguenta uns segundos e manda de novo."
        )
        return False
    timestamps.append(agora)
    return True


async def _responder(update: Update, chat_id: str, content: list[dict], texto_preview: str):
    """Envia content para o Claude e responde no Telegram."""
    history = conversation_histories.setdefault(chat_id, [])
    history.append({"role": "user", "content": content})

    if len(history) > MAX_HISTORY:
        history[:] = history[-MAX_HISTORY:]

    turn = turn_counters.get(chat_id, 0) + 1
    turn_counters[chat_id] = turn

    start = time.time()

    memory_context = ""
    try:
        # Query combina últimas 3 msgs do usuário + preview atual pra melhorar recall
        query = _query_mem0_contextual(history, texto_preview or "imagem ou documento")
        memory_context = await buscar_memorias(query)
    except Exception as mem_err:
        logger.warning(f"Mem0 search falhou: {mem_err}")

    try:
        resposta, metadata = await gerar_resposta(history, memory_context)
        latency = round(time.time() - start, 2)

        history.append({"role": "assistant", "content": resposta})

        # A cada TURNOS_PARA_RESUMO (default 3) turnos do usuário, gera resumo extrativo
        # do trecho recente e salva no Mem0 como memória curada.
        if turn - last_saved_turn.get(chat_id, 0) >= TURNOS_PARA_RESUMO:
            trecho = list(history[-(TURNOS_PARA_RESUMO * 2):])
            last_saved_turn[chat_id] = turn
            asyncio.create_task(_resumir_e_salvar(chat_id, trecho))

        for i in range(0, len(resposta), 4096):
            await update.message.reply_text(resposta[i:i + 4096])

        # Tokens de cache: se cache_read > 0, prompt caching pegou e a economia
        # real foi maior que o cost_usd sugere (cost já reflete desconto).
        # cache_hit_ratio = leitura cache / (leitura cache + criação cache + input fresh)
        cache_read = metadata.get("cache_read", 0) or 0
        cache_creation = metadata.get("cache_creation", 0) or 0
        tokens_in = metadata.get("tokens_in", 0) or 0
        denom = cache_read + cache_creation + tokens_in
        cache_hit_ratio = round(cache_read / denom, 3) if denom > 0 else 0.0

        registrar(
            direction="out",
            text_preview=texto_preview[:80],
            latency_seconds=latency,
            model=metadata.get("model"),
            tokens_in=tokens_in,
            tokens_out=metadata.get("tokens_out"),
            cache_creation=cache_creation,
            cache_read=cache_read,
            cache_hit_ratio=cache_hit_ratio,
            cost_usd=metadata.get("cost_usd"),
            status="ok"
        )

        # Persiste state em disco (volume Railway /app/data/bot_state.json)
        # pra sobreviver a redeploys
        _save_state()

    except Exception as e:
        history.pop()
        logger.error(f"Erro ao processar mensagem: {e}")
        await update.message.reply_text("Tive um problema interno. Tenta de novo em instantes.")
        registrar(direction="error", text_preview=str(e)[:80], status="error")


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    if _autorizado(chat_id):
        await update.message.reply_text("Oi, Gus online e pronto.")
    elif not AUTHORIZED_CHAT_ID:
        # Primeiro uso — mostra chat_id pra configurar
        await update.message.reply_text(
            f"Seu chat\\_id é: `{chat_id}`\n\n"
            f"Configure TELEGRAM\\_CHAT\\_ID no Railway com esse número "
            f"e faça redeploy.",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("Bot privado.")


async def handle_custo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    if not _autorizado(chat_id):
        return
    s = stats_mes_atual()
    total = s["cost_usd"]
    pct = 100 * total / HARD_LIMIT if HARD_LIMIT > 0 else 0

    # Cache hit ratio agregado do mês
    cache_total = s["cache_creation"] + s["cache_read"] + s["tokens_in"]
    hit_ratio = (s["cache_read"] / cache_total * 100) if cache_total > 0 else 0

    msg = (
        f"*Custo do mês:* US${total:.4f} de US${HARD_LIMIT:.2f} ({pct:.1f}%)\n"
        f"*Calls:* {s['calls']}\n"
        f"*Tokens:* {s['tokens_in']:,} in / {s['tokens_out']:,} out\n"
        f"*Cache:* {s['cache_read']:,} read + {s['cache_creation']:,} created "
        f"(hit ratio {hit_ratio:.1f}%)\n\n"
        f"_Obs: tracking reseta em redeploy se /app/data não tiver volume persistente._"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


async def handle_foco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Registra foco atual da sessão no Mem0. Uso: /foco <descrição livre>"""
    chat_id = str(update.effective_chat.id)
    if not _autorizado(chat_id):
        return

    texto = update.message.text.removeprefix("/foco").strip()
    if not texto:
        await update.message.reply_text(
            "Pra definir o foco da sessão, usa: `/foco estou trabalhando em X`\n\n"
            "Isso vira uma memória prioritária no Mem0 e serve de contexto nas próximas sessões.",
            parse_mode="Markdown"
        )
        return

    try:
        await salvar_memorias([
            {"role": "user", "content": f"[FOCO-ATUAL] {texto}"}
        ])
        await update.message.reply_text(
            f"Foco registrado: _{texto}_\n\nVou priorizar esse contexto nas próximas interações.",
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.warning(f"Falha ao salvar foco: {e}")
        await update.message.reply_text("Não consegui registrar o foco agora. Tenta de novo em instantes.")


async def handle_reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    if not _autorizado(chat_id):
        return

    # Se houve turnos desde o último resumo, salva o que acumulou antes de zerar
    turn = turn_counters.get(chat_id, 0)
    if turn > last_saved_turn.get(chat_id, 0):
        trecho = list(conversation_histories.get(chat_id, []))
        if trecho:
            asyncio.create_task(_resumir_e_salvar(chat_id, trecho))

    conversation_histories.pop(chat_id, None)
    turn_counters.pop(chat_id, None)
    last_saved_turn.pop(chat_id, None)
    message_timestamps.pop(chat_id, None)
    _save_state()  # persiste o reset
    await update.message.reply_text("Histórico limpo. Começando do zero.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    if not _autorizado(chat_id):
        logger.warning(f"Mensagem ignorada de chat_id não autorizado: {chat_id}")
        return
    if not await _verificar_rate_limit(update, chat_id):
        return
    if not await _verificar_limite(update):
        return

    texto = update.message.text or ""

    # Se há OS dimagem pendente de confirmação, intercepta antes do Sonnet
    pending = dimagem_pending.get(chat_id)
    if pending:
        if _DIMAGEM_CONFIRMA_RE.match(texto):
            del dimagem_pending[chat_id]
            _save_state()
            try:
                resultado = await salvar_os_dimagem(pending)
            except Exception as e:
                logger.error(f"Erro ao salvar OS confirmada: {e}")
                resultado = f"Erro ao salvar: {str(e)[:200]}"
            await update.message.reply_text(resultado)
            return
        if _DIMAGEM_CANCELA_RE.match(texto):
            del dimagem_pending[chat_id]
            _save_state()
            await update.message.reply_text("OS cancelada — não salvei.")
            return
        # Mensagem que não é confirmação nem cancelamento → expira o pending
        # e segue pro fluxo Sonnet (Gustavo mudou de assunto).
        del dimagem_pending[chat_id]
        _save_state()
        await update.message.reply_text("(OS pendente expirada — você falou de outro assunto.)")

    content = [{"type": "text", "text": texto}]
    await _responder(update, chat_id, content, texto)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    if not _autorizado(chat_id):
        return
    if not await _verificar_rate_limit(update, chat_id):
        return
    if not await _verificar_limite(update):
        return

    await update.message.reply_text("Processando imagem...")

    photo = update.message.photo[-1]  # maior resolução disponível
    file = await context.bot.get_file(photo.file_id)
    caption = update.message.caption or ""

    # Fluxo dimagem (modo confirmação prévia): se foto é OS Dimagem, extrai
    # via Haiku, mostra preview com lista atual + nova linha, espera 'sim'
    # do Gustavo. Se não for OS ou extração falhar, cai no fluxo Sonnet.
    try:
        async with _httpx_bot.AsyncClient(timeout=30) as _c:
            _img_resp = await _c.get(file.file_path)
        if _img_resp.status_code == 200:
            _preview = await analisar_os_dimagem(_img_resp.content, caption)
            if _preview:
                dimagem_pending[chat_id] = _preview
                _save_state()
                await update.message.reply_text(_preview["preview_text"])
                return
    except Exception as _dim_err:
        logger.warning(f"Fluxo dimagem falhou ({_dim_err}); caindo pro Sonnet.")

    try:
        content = await processar_imagem(file.file_path, caption)
        await _responder(update, chat_id, content, caption or "[imagem]")
    except Exception as e:
        logger.error(f"Erro ao processar imagem: {e}")
        await update.message.reply_text("Não consegui processar a imagem. Tenta de novo.")


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    if not _autorizado(chat_id):
        return
    if not await _verificar_rate_limit(update, chat_id):
        return
    if not await _verificar_limite(update):
        return

    doc = update.message.document
    mime = doc.mime_type or ""
    nome = (doc.file_name or "arquivo").lower()

    # Roteador por MIME + extensão (fallback)
    if mime == "application/pdf" or nome.endswith(".pdf"):
        processador = processar_pdf
        label = "PDF"
    elif (
        "wordprocessingml" in mime
        or mime == "application/msword"
        or nome.endswith(".docx")
        or nome.endswith(".doc")
    ):
        processador = processar_docx
        label = "Word"
    elif (
        "spreadsheetml" in mime
        or mime == "application/vnd.ms-excel"
        or nome.endswith(".xlsx")
        or nome.endswith(".xls")
    ):
        processador = processar_xlsx
        label = "Excel"
    else:
        await update.message.reply_text(
            f"Formato '{mime or nome}' ainda não suportado. Formatos ativos: PDF, Word (.docx), Excel (.xlsx). "
            "Áudio e vídeo em breve."
        )
        return

    await update.message.reply_text(f"Processando {label}...")

    file = await context.bot.get_file(doc.file_id)
    caption = update.message.caption or ""

    try:
        content = await processador(file.file_path, caption)
        await _responder(update, chat_id, content, caption or f"[{label}: {doc.file_name}]")
    except Exception as e:
        logger.error(f"Erro ao processar {label}: {e}")
        await update.message.reply_text(f"Não consegui processar o {label}. Tenta de novo ou envia em outro formato.")


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recebe voice message do Telegram, transcreve via Whisper e processa como texto."""
    chat_id = str(update.effective_chat.id)
    if not _autorizado(chat_id):
        return
    if not await _verificar_rate_limit(update, chat_id):
        return
    if not await _verificar_limite(update):
        return

    voice = update.message.voice or update.message.audio
    if not voice:
        return

    duracao = getattr(voice, "duration", 0) or 0
    await update.message.reply_text(
        f"Transcrevendo áudio ({duracao}s)..." if duracao else "Transcrevendo áudio..."
    )

    try:
        file = await context.bot.get_file(voice.file_id)
        transcricao = await transcrever_audio(file.file_path)
    except Exception as e:
        logger.error(f"Erro baixando/transcrevendo áudio: {e}")
        await update.message.reply_text("Não consegui transcrever o áudio. Tenta de novo.")
        return

    if transcricao.startswith("("):
        # Prefixo "(...)" sinaliza erro da própria transcrição
        await update.message.reply_text(f"Problema na transcrição: {transcricao}")
        return

    # Responde com a transcrição + processa como texto
    await update.message.reply_text(f"Entendi: _{transcricao}_", parse_mode="Markdown")
    content = [{"type": "text", "text": transcricao}]
    await _responder(update, chat_id, content, transcricao)
