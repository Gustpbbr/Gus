#!/usr/bin/env python3
"""
Check de saúde diário — roda auto_diagnostico() + verifica falhas de workflows
nas últimas 24h. Envia UM único Telegram consolidado se houver qualquer problema.
Silêncio absoluto se tudo verde.

Roda via .github/workflows/check-saude.yml (cron 7h30 BRT diário).

Reusa keys já configuradas como secrets no GH Actions:
- ANTHROPIC_API_KEY, QDRANT_URL, QDRANT_API_KEY, GITHUB_TOKEN, TAVILY_API_KEY
- TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, GITHUB_REPOSITORY
"""

import asyncio
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from gus.integrations.diagnostico import auto_diagnostico

import httpx


def enviar_telegram(token: str, chat_id: str, texto: str) -> None:
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


def checar_workflows_com_falha() -> list[dict]:
    """Busca runs com falha nas últimas 24h via GitHub API."""
    token = os.environ.get("GITHUB_TOKEN", "")
    repo = os.environ.get("GITHUB_REPOSITORY", os.environ.get("GITHUB_REPO", "Gustpbbr/Gus"))
    if not token:
        return []

    since = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
    url = f"https://api.github.com/repos/{repo}/actions/runs"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    try:
        r = httpx.get(url, headers=headers, params={"status": "failure", "per_page": 30}, timeout=15)
        r.raise_for_status()
        runs = r.json().get("workflow_runs", [])
    except Exception as e:
        print(f"[warn] Falha ao checar workflows: {e}", file=sys.stderr)
        return []

    falhas = []
    for run in runs:
        created = run.get("created_at", "")
        if created < since:
            continue
        # Converte para horário BRT (-3h)
        try:
            dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            brt = dt.astimezone(timezone(timedelta(hours=-3)))
            hora_brt = brt.strftime("%d/%m %H:%M")
        except Exception:
            hora_brt = created[:16]
        falhas.append({
            "nome": run.get("name", "?"),
            "hora": hora_brt,
            "url": run.get("html_url", ""),
        })

    # Deduplica por nome (mantém a mais recente)
    vistos: set[str] = set()
    dedup = []
    for f in falhas:
        if f["nome"] not in vistos:
            vistos.add(f["nome"])
            dedup.append(f)
    return dedup


async def main() -> int:
    relatorio = await auto_diagnostico()
    print(relatorio)

    falhas_wf = checar_workflows_com_falha()
    if falhas_wf:
        linhas = "\n".join(f"• {f['nome']} — {f['hora']}" for f in falhas_wf)
        print(f"\n[info] Workflows com falha nas últimas 24h:\n{linhas}")

    tem_problema_diag = "❌" in relatorio or "⚠️" in relatorio
    tem_falha_wf = bool(falhas_wf)

    if not tem_problema_diag and not tem_falha_wf:
        print("\n[info] Tudo verde — não envia notificação.")
        return 0

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("[erro] TELEGRAM_BOT_TOKEN ou TELEGRAM_CHAT_ID ausentes.", file=sys.stderr)
        return 1

    partes = ["🚨 *Diagnóstico diário — resumo*\n"]

    if tem_problema_diag:
        partes.append(relatorio)

    if tem_falha_wf:
        linhas_wf = "\n".join(f"• {f['nome']} — {f['hora']}" for f in falhas_wf)
        repo = os.environ.get("GITHUB_REPOSITORY", "Gustpbbr/Gus")
        partes.append(
            f"\n⚠️ *Workflows com falha (últimas 24h):*\n{linhas_wf}"
            f"\n[Ver todas as runs](https://github.com/{repo}/actions)"
        )

    enviar_telegram(token, chat_id, "\n".join(partes))
    print("\n[info] Alerta enviado pro Telegram.")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
