#!/usr/bin/env python3
"""
Briefing matinal automático — roda toda manhã (7h BRT dias úteis) via GitHub Actions.

Lê contexto do Gustavo (memórias recentes, commits, índices), gera briefing curto
via Claude Haiku, posta no Telegram via Bot API direta.

Não depende do bot estar rodando em polling — envia mensagem unidirecional.

Variáveis necessárias:
- MEM0_API_KEY
- ANTHROPIC_API_KEY
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID
- GITHUB_TOKEN (automático no Actions)
"""

import os
import sys
import json
import httpx
from datetime import datetime, timezone, timedelta

from mem0 import MemoryClient
from anthropic import Anthropic

USER_ID = "gustavo"
BRT = timezone(timedelta(hours=-3))
REPO = os.environ.get("GITHUB_REPOSITORY", "Gustpbbr/Gus")
MODEL = os.environ.get("MODEL_BRIEFING", "claude-haiku-4-5")

DIAS_SEMANA = [
    "segunda-feira", "terça-feira", "quarta-feira",
    "quinta-feira", "sexta-feira", "sábado", "domingo"
]

PROMPT_BRIEFING = """Você é o Gus, agente pessoal do Gustavo. Hoje é {dia_semana}, {data}.

Gere um briefing matinal curto (máximo 5 linhas, tom informal português brasileiro).

Inclua:
- 1 linha conectando com o dia/clima/contexto geral se fizer sentido
- Pendências ou temas em aberto extraídos das memórias recentes
- O que rolou no repo ontem (se algo significativo)
- 1 sugestão pro dia (opcional)

Seja direto. Sem formatação markdown. Sem emoji. Sem saudação longa. Apenas o conteúdo.

Contexto:

## Memórias recentes do Mem0
{memorias}

## Commits das últimas 24h
{commits}
"""


def buscar_memorias() -> str:
    api_key = os.environ.get("MEM0_API_KEY")
    if not api_key:
        return "(sem MEM0_API_KEY configurada)"
    try:
        client = MemoryClient(api_key=api_key)
        results = client.search(
            "pendências projetos atuais decisões recentes", user_id=USER_ID, limit=15
        )
        if not results:
            return "(nenhuma memória relevante)"
        return "\n".join(f"- {r.get('memory', '')}" for r in results)
    except Exception as e:
        return f"(erro ao buscar Mem0: {e})"


def buscar_commits_24h() -> str:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        return "(sem GITHUB_TOKEN)"
    since = (datetime.now(BRT) - timedelta(days=1)).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    url = f"https://api.github.com/repos/{REPO}/commits"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    try:
        r = httpx.get(url, params={"since": since, "per_page": 20}, headers=headers, timeout=30)
        if r.status_code != 200:
            return f"(erro GitHub: {r.status_code})"
        commits = r.json()
        if not commits:
            return "(nenhum commit nas últimas 24h)"
        linhas = []
        for c in commits:
            msg = c.get("commit", {}).get("message", "").split("\n")[0]
            autor = c.get("commit", {}).get("author", {}).get("name", "?")
            linhas.append(f"- {autor}: {msg}")
        return "\n".join(linhas)
    except Exception as e:
        return f"(erro ao buscar commits: {e})"


def gerar_briefing(memorias: str, commits: str) -> str:
    agora = datetime.now(BRT)
    prompt = PROMPT_BRIEFING.format(
        dia_semana=DIAS_SEMANA[agora.weekday()],
        data=agora.strftime("%d/%m/%Y"),
        memorias=memorias,
        commits=commits,
    )

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return "(sem ANTHROPIC_API_KEY configurada)"

    client = Anthropic(api_key=api_key)
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )
        texto = next((b.text for b in response.content if hasattr(b, "text")), "")
        return texto.strip()
    except Exception as e:
        return f"(erro ao gerar briefing: {e})"


def enviar_telegram(texto: str) -> bool:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("TELEGRAM_BOT_TOKEN ou TELEGRAM_CHAT_ID não definidos.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        r = httpx.post(url, json={"chat_id": chat_id, "text": texto}, timeout=30)
        if r.status_code == 200:
            return True
        print(f"Erro Telegram: {r.status_code} {r.text[:200]}")
        return False
    except Exception as e:
        print(f"Falha ao enviar Telegram: {e}")
        return False


def main():
    # Skip silencioso se secrets essenciais estão ausentes — evita email de falha
    # no cron diário até o Gustavo configurar os 3 secrets no GitHub.
    essenciais = ["ANTHROPIC_API_KEY", "MEM0_API_KEY", "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"]
    faltando = [k for k in essenciais if not os.environ.get(k)]
    if faltando:
        print(f"Secrets faltando: {', '.join(faltando)}. Briefing pulado.")
        sys.exit(0)

    print("Coletando contexto...")
    memorias = buscar_memorias()
    commits = buscar_commits_24h()

    print(f"Memórias: {len(memorias)} chars")
    print(f"Commits: {len(commits)} chars")

    print(f"Gerando briefing com {MODEL}...")
    briefing = gerar_briefing(memorias, commits)

    if not briefing or briefing.startswith("(erro"):
        print(f"Briefing vazio ou com erro: {briefing}")
        sys.exit(1)

    print(f"Briefing ({len(briefing)} chars):\n{briefing}\n")

    print("Enviando no Telegram...")
    if enviar_telegram(briefing):
        print("Enviado com sucesso.")
    else:
        print("Falha no envio.")
        sys.exit(2)


if __name__ == "__main__":
    main()
