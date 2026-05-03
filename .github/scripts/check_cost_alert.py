"""
Alerta proativo de custo mensal (S4 do plano de saneamento).

Lê stats agregados via /health/cost da API pública e dispara aviso pelo
Telegram se passar do threshold (default 80% do HARD_LIMIT). Antes:
HARD_LIMIT silencioso — bot mudo até alguém mandar msg e ver. Agora:
sinal externo proativo.

Roda em cron 1h (.github/workflows/check-cost.yml). Idempotente — chamadas
repetidas no mesmo nível só repostam se voltarmos pra cima do threshold
após cair (sem dedup memory entre runs, mas threshold raro de bater).

Env vars necessárias:
  - API_PUBLIC_URL          — onde o bot tá rodando (ex: https://gus-production.up.railway.app)
  - TELEGRAM_BOT_TOKEN      — pra mandar mensagem
  - TELEGRAM_CHAT_ID        — pra quem mandar
  - COST_ALERT_THRESHOLD    — % limite (default 80)
"""

import os
import sys
import json
import urllib.request
import urllib.error


def main() -> int:
    api_url = os.getenv("API_PUBLIC_URL", "").rstrip("/")
    if not api_url:
        print("API_PUBLIC_URL ausente — pulando check.", file=sys.stderr)
        return 0  # não-bloqueante: workflow não falha

    threshold = float(os.getenv("COST_ALERT_THRESHOLD", "80"))

    url = f"{api_url}/health/cost"
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} ao consultar {url}: {e.reason}", file=sys.stderr)
        return 0
    except Exception as e:
        print(f"Falha ao consultar {url}: {e}", file=sys.stderr)
        return 0

    pct = float(data.get("percentage", 0))
    cost = float(data.get("cost_usd", 0))
    limit = float(data.get("limit_usd", 0))
    calls = int(data.get("calls", 0))

    print(f"Custo atual: US${cost:.4f} de US${limit:.2f} ({pct:.1f}%, {calls} calls)")

    if pct < threshold:
        return 0

    # Bate threshold — alerta no Telegram
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not bot_token or not chat_id:
        print("TELEGRAM_BOT_TOKEN/CHAT_ID ausentes — alerta não enviado.", file=sys.stderr)
        return 1

    if pct >= 100:
        emoji = "🛑"
        urgencia = "ATINGIU O LIMITE — bot vai parar de responder."
    elif pct >= 90:
        emoji = "⚠️"
        urgencia = "Pouco saldo restante. Considera aumentar HARD_LIMIT_USD_MONTH ou observar uso."
    else:
        emoji = "📊"
        urgencia = "Use /custo no bot pra ver detalhes."

    texto = (
        f"{emoji} *Alerta de custo Gus*\n\n"
        f"Atingiu *{pct:.1f}%* do limite mensal.\n"
        f"US${cost:.2f} de US${limit:.2f} em {calls} calls.\n\n"
        f"{urgencia}"
    )

    payload = json.dumps({
        "chat_id": chat_id,
        "text": texto,
        "parse_mode": "Markdown",
    }).encode("utf-8")

    tg_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    try:
        req = urllib.request.Request(
            tg_url,
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status != 200:
                print(f"Telegram respondeu {resp.status}", file=sys.stderr)
                return 1
    except Exception as e:
        print(f"Falha ao enviar alerta Telegram: {e}", file=sys.stderr)
        return 1

    print(f"Alerta enviado: {pct:.1f}% do limite.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
