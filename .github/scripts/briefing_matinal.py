#!/usr/bin/env python3
"""
Briefing matinal automático — roda toda manhã (7h BRT dias úteis) via GitHub Actions.

Agente com tool use: decide o que buscar antes de gerar o briefing, em vez
de seguir um template fixo. O Claude coleta contexto (Hub, commits, arquivos
MD) quantas vezes precisar, depois chama enviar_briefing quando estiver pronto.

Variáveis necessárias:
- QDRANT_URL, QDRANT_API_KEY
- ANTHROPIC_API_KEY
- TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
- GITHUB_TOKEN (automático no Actions)
"""

import os
import sys
import json
import httpx
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _hub_compat import search_memorias

from anthropic import Anthropic

USER_ID = "gustavo"
BRT = timezone(timedelta(hours=-3))
REPO = os.environ.get("GITHUB_REPOSITORY", "Gustpbbr/Gus")
MODEL = os.environ.get("MODEL_BRIEFING", "claude-haiku-4-5")

DIAS_SEMANA = [
    "segunda-feira", "terça-feira", "quarta-feira",
    "quinta-feira", "sexta-feira", "sábado", "domingo",
]

TOOLS_BRIEFING = [
    {
        "name": "buscar_hub",
        "description": (
            "Busca memórias no Hub Qdrant sobre o Gustavo. "
            "Use para encontrar pendências abertas, projetos ativos, decisões recentes, contexto de saúde ou finanças."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Texto de busca semântica (ex: 'pendências projetos semana').",
                },
                "limit": {
                    "type": "integer",
                    "description": "Número de resultados (padrão 10, máx 20).",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "buscar_commits",
        "description": "Lista commits recentes do repositório GitHub.",
        "input_schema": {
            "type": "object",
            "properties": {
                "horas": {
                    "type": "integer",
                    "description": "Quantas horas para trás buscar (padrão 24).",
                }
            },
        },
    },
    {
        "name": "ler_arquivo",
        "description": (
            "Lê um arquivo MD específico do repositório GitHub. "
            "Útil para ler estado-atual.md, índices de projetos, etc."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Caminho do arquivo no repositório (ex: projetos/gus/_estado-atual.md).",
                }
            },
            "required": ["path"],
        },
    },
    {
        "name": "enviar_briefing",
        "description": (
            "Envia o briefing gerado para o Gustavo no Telegram. "
            "Chame quando tiver coletado contexto suficiente. "
            "Máximo 5 linhas, português informal, sem markdown, sem emoji."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "texto": {
                    "type": "string",
                    "description": "Texto do briefing.",
                }
            },
            "required": ["texto"],
        },
    },
]


def _tool_buscar_hub(query: str, limit: int = 10) -> str:
    if not os.environ.get("QDRANT_URL") or not os.environ.get("QDRANT_API_KEY"):
        return "(sem QDRANT_URL/QDRANT_API_KEY)"
    try:
        results = search_memorias(query, user_id=USER_ID, limit=min(limit, 20))
        if not results:
            return "(nenhuma memória encontrada)"
        return "\n".join(f"- {r.get('memory', '')}" for r in results)
    except Exception as e:
        return f"(erro Hub: {e})"


def _tool_buscar_commits(horas: int = 24) -> str:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        return "(sem GITHUB_TOKEN)"
    since = (datetime.now(BRT) - timedelta(hours=horas)).astimezone(timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    url = f"https://api.github.com/repos/{REPO}/commits"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    try:
        r = httpx.get(url, params={"since": since, "per_page": 20}, headers=headers, timeout=30)
        if r.status_code != 200:
            return f"(erro GitHub: {r.status_code})"
        commits = r.json()
        if not commits:
            return f"(nenhum commit nas últimas {horas}h)"
        linhas = []
        for c in commits:
            msg = c.get("commit", {}).get("message", "").split("\n")[0]
            autor = c.get("commit", {}).get("author", {}).get("name", "?")
            linhas.append(f"- {autor}: {msg}")
        return "\n".join(linhas)
    except Exception as e:
        return f"(erro commits: {e})"


def _tool_ler_arquivo(path: str) -> str:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        return "(sem GITHUB_TOKEN)"
    # Sanitiza path
    path = path.lstrip("/").replace("..", "")
    url = f"https://api.github.com/repos/{REPO}/contents/{path}"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    try:
        r = httpx.get(url, headers=headers, timeout=30)
        if r.status_code == 404:
            return f"(arquivo não encontrado: {path})"
        if r.status_code != 200:
            return f"(erro GitHub: {r.status_code})"
        data = r.json()
        import base64
        conteudo = base64.b64decode(data.get("content", "")).decode("utf-8", errors="ignore")
        # Limita a 3000 chars
        if len(conteudo) > 3000:
            conteudo = conteudo[:3000] + "\n[…truncado…]"
        return conteudo
    except Exception as e:
        return f"(erro ler arquivo: {e})"


def _tool_enviar_telegram(texto: str) -> bool:
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


def _executar_tool(nome: str, args: dict) -> str:
    if nome == "buscar_hub":
        return _tool_buscar_hub(args.get("query", ""), args.get("limit", 10))
    if nome == "buscar_commits":
        return _tool_buscar_commits(args.get("horas", 24))
    if nome == "ler_arquivo":
        return _tool_ler_arquivo(args.get("path", ""))
    return f"(tool desconhecida: {nome})"


def rodar_agente_briefing() -> str | None:
    """Loop de tool use: Claude decide o que buscar e gera o briefing."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None

    agora = datetime.now(BRT)
    dia_semana = DIAS_SEMANA[agora.weekday()]
    data = agora.strftime("%d/%m/%Y")

    system = (
        f"Você é o Gus, agente pessoal do Gustavo Pratti de Barros. "
        f"Hoje é {dia_semana}, {data}. "
        "Sua tarefa: gerar um briefing matinal curto para o Gustavo. "
        "Use as ferramentas para coletar o contexto que precisar — pendências, commits recentes, projetos em andamento. "
        "Depois chame enviar_briefing com o texto final (máximo 5 linhas, português informal, sem markdown, sem emoji)."
    )

    client = Anthropic(api_key=api_key)
    messages: list[dict] = [{"role": "user", "content": "Gere o briefing matinal de hoje."}]

    for rnd in range(10):
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=1024,
                system=system,
                tools=TOOLS_BRIEFING,
                messages=messages,
            )
        except Exception as e:
            print(f"Erro agente round {rnd}: {e}")
            return None

        tool_calls = [b for b in response.content if hasattr(b, "type") and b.type == "tool_use"]

        if not tool_calls or response.stop_reason == "end_turn":
            print("Agente encerrou sem chamar enviar_briefing.")
            break

        tool_results = []
        briefing_enviado = None

        for tc in tool_calls:
            print(f"  tool: {tc.name}({json.dumps(tc.input)[:80]})")
            if tc.name == "enviar_briefing":
                texto = tc.input.get("texto", "")
                print(f"\nBriefing gerado:\n{texto}\n")
                sucesso = _tool_enviar_telegram(texto)
                if sucesso:
                    briefing_enviado = texto
                result = "enviado com sucesso" if sucesso else "falha no envio"
            else:
                result = _executar_tool(tc.name, tc.input)
                print(f"  → {result[:120]}")

            tool_results.append({"type": "tool_result", "tool_use_id": tc.id, "content": result})

        # Serializa para mensagem seguinte
        content_dicts = []
        for b in response.content:
            if b.type == "text":
                content_dicts.append({"type": "text", "text": b.text})
            elif b.type == "tool_use":
                content_dicts.append({"type": "tool_use", "id": b.id, "name": b.name, "input": b.input})

        messages.append({"role": "assistant", "content": content_dicts})
        messages.append({"role": "user", "content": tool_results})

        if briefing_enviado is not None:
            return briefing_enviado

    return None


def main():
    essenciais = ["ANTHROPIC_API_KEY", "QDRANT_URL", "QDRANT_API_KEY", "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"]
    faltando = [k for k in essenciais if not os.environ.get(k)]
    if faltando:
        print(f"Secrets faltando: {', '.join(faltando)}. Briefing pulado.")
        sys.exit(0)

    print("Iniciando agente de briefing...")
    resultado = rodar_agente_briefing()

    if resultado:
        print("Briefing enviado com sucesso.")
    else:
        print("Agente não gerou briefing.")
        sys.exit(1)


if __name__ == "__main__":
    main()
