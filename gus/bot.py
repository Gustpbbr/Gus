"""
Re-exports dos handlers do bot Telegram.

Histórico (M1 do plano de saneamento, 2026-05-03): este arquivo era
monolítico (~650 linhas com state + 6 handlers + utilitários). Splitado em:

  - gus/state.py             — state global + load/save + validações
  - gus/handlers/responder   — _responder + curador + PII redact (compartilhado)
  - gus/handlers/text        — handle_message (+ interceptação Dimagem)
  - gus/handlers/photo       — handle_photo (+ fluxo Dimagem OCR)
  - gus/handlers/document    — handle_document (PDF/Word/Excel)
  - gus/handlers/voice       — handle_voice (Whisper)
  - gus/handlers/commands    — handle_start/custo/foco/reset

Este módulo só agrega tudo pra preservar `from gus.bot import handle_*`
em `gus/main.py` e em testes existentes.

Re-exports adicionais (compatibilidade com tests/test_bot.py):
  - state globals (conversation_histories, dimagem_pending, etc.)
  - utilidades privadas (_load_state, _save_state, _autorizado, ...)
  - regex Dimagem
"""

# Handlers públicos
from gus.handlers.commands import handle_start, handle_custo, handle_foco, handle_reset
from gus.handlers.text import handle_message
from gus.handlers.photo import handle_photo
from gus.handlers.document import handle_document
from gus.handlers.voice import handle_voice

# Compat — testes e código externo importavam direto de gus.bot
from gus.handlers.commands import _limpar_focos_antigos
from gus.handlers.responder import (
    _redigir_resposta,
    _texto_de_content,
    _query_mem0_contextual,
    _resumir_e_salvar,
    _responder,
)

# State + utilidades — re-exportados pra os testes (tests/test_bot.py acessa
# bot.conversation_histories, bot._load_state, bot._DIMAGEM_CONFIRMA_RE etc.)
from gus.state import (
    AUTHORIZED_CHAT_ID,
    HARD_LIMIT,
    MAX_HISTORY,
    TURNOS_PARA_RESUMO,
    RATE_LIMIT_MSG_PER_MINUTE,
    STATE_FILE,
    conversation_histories,
    turn_counters,
    last_saved_turn,
    message_timestamps,
    dimagem_pending,
    DIMAGEM_CONFIRMA_RE as _DIMAGEM_CONFIRMA_RE,
    DIMAGEM_CANCELA_RE as _DIMAGEM_CANCELA_RE,
    _load_state,
    _save_state,
    _autorizado,
    _verificar_limite,
    _verificar_rate_limit,
)


__all__ = [
    # Handlers
    "handle_start", "handle_custo", "handle_foco", "handle_reset",
    "handle_message", "handle_photo", "handle_document", "handle_voice",
    # Compat
    "_limpar_focos_antigos",
    "_redigir_resposta", "_texto_de_content", "_query_mem0_contextual",
    "_resumir_e_salvar", "_responder",
    "AUTHORIZED_CHAT_ID", "HARD_LIMIT", "MAX_HISTORY", "TURNOS_PARA_RESUMO",
    "RATE_LIMIT_MSG_PER_MINUTE", "STATE_FILE",
    "conversation_histories", "turn_counters", "last_saved_turn",
    "message_timestamps", "dimagem_pending",
    "_DIMAGEM_CONFIRMA_RE", "_DIMAGEM_CANCELA_RE",
    "_load_state", "_save_state",
    "_autorizado", "_verificar_limite", "_verificar_rate_limit",
]
