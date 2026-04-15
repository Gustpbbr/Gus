import json
import os
from datetime import datetime
from pathlib import Path

LOG_DIR = Path(os.getenv("LOG_DIR", "logs"))
LOG_FILE = LOG_DIR / "gus_metrics.jsonl"


def registrar(**kwargs):
    LOG_DIR.mkdir(exist_ok=True)
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
