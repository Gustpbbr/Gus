#!/usr/bin/env python3
"""
Check de saúde diário — roda auto_diagnostico() e avisa Telegram só se tem
warning ou erro. Silêncio absoluto se tudo verde.

Roda via .github/workflows/check-saude.yml (cron 7h30 BRT diário).

Reusa keys já configuradas como secrets no GH Actions:
- ANTHROPIC_API_KEY, QDRANT_URL, QDRANT_API_KEY, GITHUB_TOKEN, TAVILY_API_KEY
- TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

NÃO reusa o Railway_diagnostic (token vive só no Railway, não nos secrets GH —
o check de Railway logs não roda aqui, só os 6 do auto_diagnostico que usam
keys universais).

Volume Railway (/app/data) também não existe aqui no GH runner — esse
check vai sair como ⚠️ esperado. Aceitável: o objetivo é detectar problemas
nos componentes externos (Hub Qdrant, Anthropic, GitHub, Tavily, workflows GH),
não validar volume.
"""

import asyncio
import os
import sys
from pathlib import Path

# Adiciona repo root ao path pra importar gus.*
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from gus.integrations.diagnostico import auto_diagnostico

import httpx


def enviar_telegram(token: str, chat_id: str, texto: str) -> None:
    """Manda texto pro Telegram. Trunca se passar de 4096 chars."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    if len(texto) > 4096:
        texto = texto[:4090] + "\n…"
    payload = {
        "chat_id": chat_id,
        "text": texto,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }
    try:
        r = httpx.post(url, json=payload, timeout=20)
        if r.status_code != 200:
            print(f"[warn] Telegram status {r.status_code}: {r.text[:200]}", file=sys.stderr)
    except Exception as e:
        print(f"[erro] Falha ao enviar Telegram: {e}", file=sys.stderr)


async def main() -> int:
    relatorio = await auto_diagnostico()
    print(relatorio)

    # Heurística: se tem ❌ ou ⚠️ no relatório → manda alerta. Se só ✅ → silêncio.
    if "❌" not in relatorio and "⚠️" not in relatorio:
        print("\n[info] Tudo verde — não envia notificação.")
        return 0

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("[erro] TELEGRAM_BOT_TOKEN ou TELEGRAM_CHAT_ID ausentes.", file=sys.stderr)
        return 1

    cabecalho = "🚨 *Diagnóstico diário detectou problema:*\n\n"
    enviar_telegram(token, chat_id, cabecalho + relatorio)
    print("\n[info] Alerta enviado pro Telegram.")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
