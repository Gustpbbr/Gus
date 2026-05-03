"""
State global do bot Telegram + utilidades de validação.

Separado de gus/bot.py em 2026-05-03 (item M1 do plano de saneamento) pra
permitir testes isolados e split de handlers em arquivos próprios.

State é PROCESS-LOCAL (por chat_id) com persistência opcional em volume
Railway (`/app/data/bot_state.json`). Sobrevive a redeploys quando o volume
está montado; reseta quando container roda fora de Railway sem volume.

Fluxo:
  - Import do módulo dispara `_load_state()` automaticamente
  - Handlers atualizam dicts globais e chamam `_save_state()` em pontos
    críticos (após resposta, após reset, após dimagem confirma/cancela)
  - Write atômico via tmp+replace evita corrupção em kill mid-write
"""

import os
import json
import time
import logging
import re
from collections import deque
from pathlib import Path
from typing import Optional

from telegram import Update

from gus.logger import custo_mes_atual

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuração via env vars
# ---------------------------------------------------------------------------

AUTHORIZED_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
HARD_LIMIT = float(os.getenv("HARD_LIMIT_USD_MONTH", "30"))
MAX_HISTORY = int(os.getenv("MAX_HISTORY_MESSAGES", "40"))  # 20 turnos
TURNOS_PARA_RESUMO = int(os.getenv("TURNOS_PARA_RESUMO", "3"))
RATE_LIMIT_MSG_PER_MINUTE = int(os.getenv("RATE_LIMIT_MSG_PER_MINUTE", "20"))

# Auto-detect volume Railway em /app/data. Se montado, persiste state entre
# redeploys.
_DATA_DIR = "/app/data" if os.path.isdir("/app/data") else None
STATE_FILE = os.getenv("STATE_FILE") or (
    f"{_DATA_DIR}/bot_state.json" if _DATA_DIR else ""
)


# ---------------------------------------------------------------------------
# State em memória por chat_id (carregado do disco se disponível)
# ---------------------------------------------------------------------------

conversation_histories: dict[str, list] = {}
turn_counters: dict[str, int] = {}
last_saved_turn: dict[str, int] = {}
message_timestamps: dict[str, deque] = {}

# Fluxo dimagem: OS extraídas aguardando confirmação ("sim"/"ok") do Gustavo.
# Persistido em bot_state.json pra sobreviver redeploy do Railway.
dimagem_pending: dict[str, dict] = {}


# ---------------------------------------------------------------------------
# Regex pré-compilados (fluxo dimagem)
# ---------------------------------------------------------------------------

DIMAGEM_CONFIRMA_RE = re.compile(
    r"^\s*(sim|s|ok|okay|confirma|confirme|confirmo|manda|pode|salva|salve|vai|bora|positivo|1|👍)\s*[!.]*\s*$",
    re.IGNORECASE,
)
DIMAGEM_CANCELA_RE = re.compile(
    r"^\s*(n[ãa]o|cancela|ignora|esquece|deixa\s+pr[ao]\s+l[áa]|aborta?)",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Persistência (volume Railway)
# ---------------------------------------------------------------------------

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
            "message_timestamps": {
                cid: list(ts) for cid, ts in message_timestamps.items()
            },
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


# ---------------------------------------------------------------------------
# Validações de chat / rate / custo
# ---------------------------------------------------------------------------

def _autorizado(chat_id: str) -> bool:
    if not AUTHORIZED_CHAT_ID:
        return False  # nega tudo até configurar TELEGRAM_CHAT_ID
    return chat_id == AUTHORIZED_CHAT_ID


async def _verificar_limite(update: Update) -> bool:
    """HARD_LIMIT mensal — atingido, recusa novos turnos."""
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
