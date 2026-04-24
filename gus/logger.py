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
    if not LOG_FILE.exists():
        return 0.0
    now = datetime.now()
    total = 0.0
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
                ts = datetime.fromisoformat(entry["timestamp"])
                if ts.year == now.year and ts.month == now.month:
                    total += entry.get("cost_usd", 0.0)
            except Exception:
                continue
    return round(total, 4)
