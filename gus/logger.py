import json
import os
from datetime import datetime
from pathlib import Path

# Auto-detect volume Railway em /app/data. Se montado, usa lá; senão, pasta local.
_DATA_DIR = "/app/data" if os.path.isdir("/app/data") else None
_DEFAULT_LOG_DIR = f"{_DATA_DIR}/logs" if _DATA_DIR else "logs"

LOG_DIR = Path(os.getenv("LOG_DIR", _DEFAULT_LOG_DIR))
LOG_FILE = LOG_DIR / "gus_metrics.jsonl"


def registrar(**kwargs):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    entry = {"timestamp": datetime.now().isoformat(), **kwargs}
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def custo_mes_atual() -> float:
    """Retrocompat: só o total. Pra detalhes (cache, tokens), use stats_mes_atual()."""
    return stats_mes_atual()["cost_usd"]


def stats_mes_atual() -> dict:
    """Retorna agregado do mês: custo, tokens, cache hits.

    Útil pra /custo (interativo) e pra dashboards futuros. Lê o jsonl,
    agrega por mês corrente.
    """
    base = {
        "cost_usd": 0.0,
        "tokens_in": 0,
        "tokens_out": 0,
        "cache_creation": 0,
        "cache_read": 0,
        "calls": 0,
    }
    if not LOG_FILE.exists():
        return base

    now = datetime.now()
    for k in ("tokens_in", "tokens_out", "cache_creation", "cache_read", "calls"):
        base[k] = 0
    base["cost_usd"] = 0.0

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
                ts = datetime.fromisoformat(entry["timestamp"])
                if ts.year != now.year or ts.month != now.month:
                    continue
                base["cost_usd"] += entry.get("cost_usd", 0.0) or 0.0
                base["tokens_in"] += entry.get("tokens_in", 0) or 0
                base["tokens_out"] += entry.get("tokens_out", 0) or 0
                base["cache_creation"] += entry.get("cache_creation", 0) or 0
                base["cache_read"] += entry.get("cache_read", 0) or 0
                base["calls"] += 1
            except Exception:
                continue

    base["cost_usd"] = round(base["cost_usd"], 4)
    return base
