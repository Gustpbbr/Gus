"""
Fixtures e setup compartilhado da suite de testes.

Importante: env vars fake setadas ANTES de qualquer import de gus.* — vários
módulos instanciam clients no top-level (gus/llm.py:client = AsyncAnthropic).
"""

import os
import sys
from pathlib import Path

# repo root no sys.path pra `from gus...` e `from hub...` funcionarem
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Env vars fake — necessárias pra import top-level não quebrar.
os.environ.setdefault("ANTHROPIC_API_KEY", "fake-test-key")
os.environ.setdefault("OPENAI_API_KEY", "fake-test-key")
os.environ.setdefault("QDRANT_URL", "http://fake.local")
os.environ.setdefault("QDRANT_API_KEY", "fake-test-key")
os.environ.setdefault("TELEGRAM_BOT_TOKEN", "fake-test-token")
os.environ.setdefault("TELEGRAM_CHAT_ID", "12345")
os.environ.setdefault("GITHUB_TOKEN", "fake-test-token")

import pytest


@pytest.fixture
def tmp_state_file(tmp_path, monkeypatch):
    """Path temporário para STATE_FILE do bot.py."""
    state = tmp_path / "bot_state.json"
    monkeypatch.setenv("STATE_FILE", str(state))
    return state


@pytest.fixture
def tmp_log_dir(tmp_path, monkeypatch):
    """Path temporário para LOG_DIR do logger.py."""
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    monkeypatch.setenv("LOG_DIR", str(log_dir))
    return log_dir
