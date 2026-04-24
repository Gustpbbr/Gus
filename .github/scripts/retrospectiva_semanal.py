#!/usr/bin/env python3
"""
Retrospectiva semanal automática — roda sexta 20h BRT via GitHub Actions.

Coleta atividade da semana (Mem0, commits, índices modificados) e gera MD
estruturado em pessoal/diario/semana-AAAA-WW.md. Commit automático.

Variáveis necessárias:
- MEM0_API_KEY
- ANTHROPIC_API_KEY
- TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID (opcional — pra enviar resumo de aviso)
- GITHUB_TOKEN
"""

import os
import sys
import subprocess
import httpx
from datetime import datetime, timezone, timedelta

from mem0 import MemoryClient
from anthropic import Anthropic

USER_ID = "gustavo"
BRT = timezone(timedelta(hours=-3))
REPO = os.environ.get("GITHUB_REPOSITORY", "Gustpbbr/Gus")
MODEL = os.environ.get("MODEL_RETROSPECTIVA", "claude-sonnet-4-6")

PROMPT_RETRO = """Você é o Gus, agente pessoal do Gustavo. Hoje é {data}, fim de semana {ano_semana}.

Gere uma retrospectiva semanal em MD estruturado pra Gustavo. Tom: português brasileiro informal, direto, sem superlativos vazios, sem emoji.

Use EXATAMENTE esta estrutura:

```
---
tipo: retrospectiva-semanal
semana: {ano_semana}
gerado_em: {agora_iso}
---

# Retrospectiva — semana {ano_semana}

## Resumo executivo
(3 linhas — o mais importante que aconteceu e o clima geral)

## Atividades por área
(para cada área com atividade: projetos, saúde, dimagem, capturado, outras. Seja específico. Use wikilinks `[[nome-arquivo]]` quando referenciar MDs.)

## Decisões tomadas
(o que foi resolvido, com o porquê quando fizer sentido)

## Pendências identificadas
(o que ficou em aberto, priorizadas)

## Próxima semana
(1-2 sugestões concretas)
```

Dados da semana:

## Memórias novas no Mem0 (últimos 7 dias)
{memorias}

## Commits (últimos 7 dias)
{commits}

## Arquivos criados esta semana
{novos_arquivos}

Se algum dado estiver vazio, sinalize ("sem atividade registrada") em vez de inventar.
"""


def buscar_memorias_recentes() -> str:
    api_key = os.environ.get("MEM0_API_KEY")
    if not api_key:
        return "(sem MEM0_API_KEY)"
    try:
        client = MemoryClient(api_key=api_key)
        all_mem = client.get_all(user_id=USER_ID)
        sete_dias_atras = datetime.now(timezone.utc) - timedelta(days=7)

        recentes = []
        for m in all_mem:
            created = m.get("created_at", "")
            try:
                dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                if dt >= sete_dias_atras:
                    recentes.append(m)
            except Exception:
                continue

        if not recentes:
            return "(nenhuma memória nova nesta semana)"

        linhas = []
        for m in recentes:
            texto = (m.get("memory") or "").strip()
            data = m.get("created_at", "")[:10]
            if texto:
                linhas.append(f"- ({data}) {texto}")
        return "\n".join(linhas) if linhas else "(sem conteúdo extraído)"
    except Exception as e:
        return f"(erro Mem0: {e})"


def buscar_commits_semana() -> str:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        return "(sem GITHUB_TOKEN)"
    since = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    url = f"https://api.github.com/repos/{REPO}/commits"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    try:
        r = httpx.get(url, params={"since": since, "per_page": 100}, headers=headers, timeout=30)
        if r.status_code != 200:
            return f"(erro GitHub: {r.status_code})"
        commits = r.json()
        if not commits:
            return "(nenhum commit)"
        linhas = []
        for c in commits:
            sha = c.get("sha", "")[:7]
            msg = c.get("commit", {}).get("message", "").split("\n")[0]
            autor = c.get("commit", {}).get("author", {}).get("name", "?")
            data = c.get("commit", {}).get("author", {}).get("date", "")[:10]
            linhas.append(f"- ({data}) `{sha}` {autor}: {msg}")
        return "\n".join(linhas)
    except Exception as e:
        return f"(erro commits: {e})"


def buscar_novos_arquivos() -> str:
    """Via git log diff-filter=A na última semana."""
    try:
        since_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        resultado = subprocess.run(
            ["git", "log", f"--since={since_date}", "--diff-filter=A", "--name-only", "--pretty=format:"],
            capture_output=True, text=True, check=False
        )
        if resultado.returncode != 0:
            return "(erro git log)"
        arquivos = sorted(set(
            linha.strip() for linha in resultado.stdout.splitlines()
            if linha.strip() and not linha.startswith(".github/") and not linha.endswith(".gitkeep")
        ))
        if not arquivos:
            return "(nenhum arquivo novo)"
        return "\n".join(f"- {a}" for a in arquivos)
    except Exception as e:
        return f"(erro git: {e})"


def gerar_retrospectiva(memorias: str, commits: str, novos_arquivos: str) -> str:
    agora = datetime.now(BRT)
    ano, semana, _ = agora.isocalendar()
    ano_semana = f"{ano}-W{semana:02d}"

    prompt = PROMPT_RETRO.format(
        data=agora.strftime("%d/%m/%Y"),
        ano_semana=ano_semana,
        agora_iso=agora.isoformat(),
        memorias=memorias,
        commits=commits,
        novos_arquivos=novos_arquivos,
    )

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return "(sem ANTHROPIC_API_KEY)"

    client = Anthropic(api_key=api_key)
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
        )
        texto = next((b.text for b in response.content if hasattr(b, "text")), "")
        return texto.strip()
    except Exception as e:
        return f"(erro gerar retrospectiva: {e})"


def enviar_aviso_telegram(caminho: str) -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return
    texto = f"Retrospectiva da semana gerada: {caminho}"
    try:
        httpx.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": texto},
            timeout=30,
        )
    except Exception:
        pass


def main():
    print("Coletando dados da semana...")
    memorias = buscar_memorias_recentes()
    commits = buscar_commits_semana()
    novos_arquivos = buscar_novos_arquivos()

    print(f"  Memórias: {len(memorias)} chars")
    print(f"  Commits: {len(commits)} chars")
    print(f"  Arquivos novos: {len(novos_arquivos)} chars")

    print(f"Gerando retrospectiva com {MODEL}...")
    conteudo = gerar_retrospectiva(memorias, commits, novos_arquivos)

    if not conteudo or conteudo.startswith("(erro"):
        print(f"Falhou: {conteudo}")
        sys.exit(1)

    agora = datetime.now(BRT)
    ano, semana, _ = agora.isocalendar()
    arquivo = f"pessoal/diario/semana-{ano}-W{semana:02d}.md"
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)

    with open(arquivo, "w", encoding="utf-8") as f:
        f.write(conteudo + "\n")

    print(f"Escrito em {arquivo}")
    enviar_aviso_telegram(arquivo)


if __name__ == "__main__":
    main()
