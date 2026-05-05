#!/usr/bin/env python3
"""
Reflexão quinzenal do Gus — camada SELF-1 (Nosis + Thymos + Síntese).

Roda sábado 10h BRT via GitHub Actions (a cada 2 semanas na prática,
script verifica semana par/ímpar pra decidir se roda).

- Nosis (Haiku): camada cognitiva — padrões, contradições, vieses, gaps
- Thymos (Haiku): camada volitiva — drift de foco, projetos estagnados, intenções
- Síntese (Sonnet): integra os dois e gera 1 recomendação concreta

Saída: projetos/gus/reflexoes/AAAA-WW-reflexao.md

Variáveis necessárias:
- QDRANT_URL, QDRANT_API_KEY (Hub Qdrant — antes era MEM0_API_KEY)
- ANTHROPIC_API_KEY
- GITHUB_TOKEN (automático)
- TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID (opcional, aviso)
"""

import os
import sys
import subprocess
import httpx
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Migrado em R2 (2026-04-27): lê do Hub Qdrant via _hub_compat (Mem0 aposentado).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _hub_compat import get_all_memorias

from anthropic import Anthropic

USER_ID = "gustavo"
BRT = timezone(timedelta(hours=-3))
REPO = os.environ.get("GITHUB_REPOSITORY", "Gustpbbr/Gus")
MODEL_OBS = os.environ.get("MODEL_REFLEXAO_OBS", "claude-haiku-4-5")
MODEL_SINTESE = os.environ.get("MODEL_REFLEXAO_SINTESE", "claude-sonnet-4-6")
DIAS_JANELA = 14

NOSIS_PROMPT = """Você é Nosis — a camada cognitiva reflexiva do Gus (agente pessoal do Gustavo). Sua função é **observar** o pensamento recente do Gustavo e apontar padrões.

Analise os dados abaixo (memórias recentes + commits + arquivos novos + meta-memória dos últimos 14 dias) e produza observações em 4 categorias:

**Importante — uso da meta-memória:** a seção "Meta-memória" descreve o estado estrutural do Mem0 (duplicatas suspeitas, gaps, densidade por área). Use essa informação pra filtrar: padrões que aparecem apenas em memórias flagadas como duplicatas não são "recorrências reais". Lacunas listadas em "Gaps" devem ser citadas quando fizerem sentido.

**Padrões recorrentes:** temas, decisões ou perguntas que voltam
**Contradições:** coisas ditas/decididas em pontos diferentes que não se sustentam juntas
**Vieses identificáveis:** excesso de confiança, ancoragem, aversão a perda, confirmação, etc
**Gaps:** áreas ativas onde a informação está insuficiente pra decisão

Regras:
- Observação neutra, não julgamento. Sem "você deveria..."
- Saída: máximo 8 bullets no total (distribuídos entre as 4 categorias conforme o que apareceu)
- Cada bullet: 1-2 linhas, específico, com âncora no dado ("baseado em [memória X]" ou "visto em [commit Y]")
- Se uma categoria não tem nada relevante, **não invente** — pule
- Português BR informal, direto

Se não houver material suficiente pra observação (dados escassos), responda apenas: "Dados insuficientes nesta janela para observação cognitiva."
"""

THYMOS_PROMPT = """Você é Thymos — a camada volitiva (vontade/intenção) reflexiva do Gus. Sua função é **observar** o que o Gustavo disse que ia fazer e comparar com o que foi feito.

Analise os dados abaixo (memórias + commits + arquivos + meta-memória dos últimos 14 dias) e produza observações em 4 categorias:

**Importante — uso da meta-memória:** a seção "Meta-memória" mostra quais áreas têm volume de memória e quais estão em gap estrutural. Projetos declarados sem memórias associadas são sinal forte de "declarado vs realizado" em desequilíbrio. Áreas com densidade alta indicam onde a energia real foi.

**Declarado vs realizado:** metas ou intenções expressas que avançaram, emperraram ou foram abandonadas
**Drift de foco:** projetos declarados como prioridade vs tempo/energia real investidos
**Pausas sem retomada:** coisas pausadas com promessa de voltar, que ainda não voltaram
**Energia emergente:** projetos ou temas que ganharam tração orgânica (mais atividade que o planejado)

Regras:
- Direto, sem moralizar. Não é coach, é observador.
- Saída: máximo 8 bullets no total
- Cada bullet: 1-2 linhas, específico, com âncora no dado
- Se não houver sinal numa categoria, pule
- Português BR informal

Se não houver material suficiente, responda apenas: "Dados insuficientes nesta janela para observação volitiva."
"""

SINTESE_PROMPT = """Você é o Gus em modo reflexivo — não o assistente Telegram, mas a camada de auto-observação do sistema.

Você recebeu duas análises feitas sobre os últimos 14 dias do Gustavo:

**Nosis (cognição):**
{nosis_output}

**Thymos (vontade):**
{thymos_output}

Sua tarefa: **integrar** os dois e produzir **uma única recomendação concreta** pra próxima quinzena. Não faça resumo — faça síntese. A recomendação deve:

- Ser executável na próxima quinzena
- Atacar simultaneamente um padrão cognitivo (Nosis) e um drift volitivo (Thymos) — a convergência é onde está o sinal
- Se os dois não convergem (falam de coisas diferentes), escolha o mais forte e explique por quê
- Ser honesta: se Gustavo está dispersado e a recomendação é "pausar projetos", diga isso

Estrutura da saída (300 palavras no máximo):

## Convergência observada
(1 parágrafo — o que Nosis e Thymos estão apontando juntos, ou por que divergem)

## Recomendação pra próxima quinzena
(1 ação concreta, específica, com porquê)

## Alerta opcional
(1 linha se houver algo urgente/grave — ex: saúde, finanças, projeto com deadline. Senão, omite.)

Português BR informal, direto, sem superlativos vazios. Sem "incrível", "fantástico", sem emoji.
"""


def skip_se_falta_secret() -> None:
    essenciais = ["ANTHROPIC_API_KEY", "QDRANT_URL", "QDRANT_API_KEY"]
    faltando = [k for k in essenciais if not os.environ.get(k)]
    if faltando:
        print(f"Secrets faltando: {', '.join(faltando)}. Reflexão pulada.")
        sys.exit(0)


def buscar_memorias_janela() -> str:
    """Memórias criadas nos últimos DIAS_JANELA dias."""
    try:
        todas = get_all_memorias(user_id=USER_ID, limit=10000)
        limite = datetime.now(timezone.utc) - timedelta(days=DIAS_JANELA)

        recentes = []
        for m in todas:
            created = m.get("created_at", "")
            try:
                dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                if dt >= limite:
                    recentes.append(m)
            except Exception:
                continue

        if not recentes:
            return "(nenhuma memória nova nos últimos 14 dias)"

        linhas = []
        for m in recentes:
            texto = (m.get("memory") or "").strip()
            data = m.get("created_at", "")[:10]
            if texto:
                linhas.append(f"- ({data}) {texto}")
        return "\n".join(linhas) or "(sem conteúdo extraído)"
    except Exception as e:
        return f"(erro Hub: {e})"


def buscar_commits_janela() -> str:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        return "(sem GITHUB_TOKEN)"
    since = (datetime.now(timezone.utc) - timedelta(days=DIAS_JANELA)).strftime("%Y-%m-%dT%H:%M:%SZ")
    url = f"https://api.github.com/repos/{REPO}/commits"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    try:
        r = httpx.get(url, params={"since": since, "per_page": 100}, headers=headers, timeout=30)
        if r.status_code != 200:
            return f"(erro GitHub: {r.status_code})"
        commits = r.json()
        if not commits:
            return "(nenhum commit na janela)"
        linhas = []
        for c in commits:
            msg = c.get("commit", {}).get("message", "").split("\n")[0]
            data = c.get("commit", {}).get("author", {}).get("date", "")[:10]
            linhas.append(f"- ({data}) {msg}")
        return "\n".join(linhas)
    except Exception as e:
        return f"(erro commits: {e})"


def buscar_arquivos_novos() -> str:
    try:
        since_date = (datetime.now() - timedelta(days=DIAS_JANELA)).strftime("%Y-%m-%d")
        resultado = subprocess.run(
            ["git", "log", f"--since={since_date}", "--diff-filter=A",
             "--name-only", "--pretty=format:"],
            capture_output=True, text=True, check=False
        )
        if resultado.returncode != 0:
            return "(erro git log)"
        arquivos = sorted(set(
            linha.strip() for linha in resultado.stdout.splitlines()
            if linha.strip() and not linha.startswith((".github/", "gus/"))
            and not linha.endswith(".gitkeep")
        ))
        if not arquivos:
            return "(nenhum arquivo novo na janela)"
        return "\n".join(f"- {a}" for a in arquivos)
    except Exception as e:
        return f"(erro git: {e})"


def carregar_meta_memoria() -> str:
    """Lê _indices/_auditoria-hub.md se existir. Contexto pra Nosis/Thymos
    distinguir padrões reais de duplicatas e gaps reais de lacunas de classificação."""
    caminho = "_indices/_auditoria-hub.md"
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "(meta-memória ainda não gerada — SELF-1 rodando sem contexto estrutural)"
    except Exception as e:
        return f"(erro ao ler meta-memória: {e})"


def chamar_claude(client: Anthropic, model: str, system: str, user_content: str, max_tokens: int = 2048) -> str:
    try:
        r = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user_content}],
        )
        return next((b.text for b in r.content if hasattr(b, "text")), "").strip()
    except Exception as e:
        return f"(erro chamada Claude {model}: {e})"


def notificar_telegram(caminho: str) -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return
    texto = f"Reflexão quinzenal gerada: {caminho}\n\nAbre no repo pra ler Nosis + Thymos + síntese."
    try:
        httpx.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": texto},
            timeout=30,
        )
    except Exception:
        pass


def main():
    skip_se_falta_secret()

    agora = datetime.now(BRT)
    ano, semana, _ = agora.isocalendar()

    # Roda apenas em semanas pares (aproxima quinzena) pra não duplicar
    # com retrospectiva semanal que já roda sexta
    if semana % 2 != 0 and not os.environ.get("FORCE_RUN"):
        print(f"Semana {semana} é ímpar — pula (só roda em pares pra ritmo quinzenal)")
        sys.exit(0)

    print(f"Coletando dados dos últimos {DIAS_JANELA} dias...")
    memorias = buscar_memorias_janela()
    commits = buscar_commits_janela()
    arquivos_novos = buscar_arquivos_novos()
    meta_mem = carregar_meta_memoria()

    dados_base = (
        f"## Memórias (Mem0)\n{memorias}\n\n"
        f"## Commits\n{commits}\n\n"
        f"## Arquivos novos\n{arquivos_novos}\n\n"
        f"## Meta-memória (estado estrutural do Mem0)\n{meta_mem}"
    )

    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    print(f"Rodando Nosis ({MODEL_OBS})...")
    nosis_out = chamar_claude(client, MODEL_OBS, NOSIS_PROMPT, dados_base, 1024)
    print(f"  Nosis: {len(nosis_out)} chars")

    print(f"Rodando Thymos ({MODEL_OBS})...")
    thymos_out = chamar_claude(client, MODEL_OBS, THYMOS_PROMPT, dados_base, 1024)
    print(f"  Thymos: {len(thymos_out)} chars")

    print(f"Rodando Síntese ({MODEL_SINTESE})...")
    sintese_system = SINTESE_PROMPT.format(
        nosis_output=nosis_out, thymos_output=thymos_out
    )
    sintese_out = chamar_claude(
        client, MODEL_SINTESE, sintese_system,
        "Produza a reflexão integrada conforme a estrutura.", 1024
    )
    print(f"  Síntese: {len(sintese_out)} chars")

    # Monta MD final
    conteudo = (
        f"---\n"
        f"tipo: reflexao-self1\n"
        f"semana: {ano}-W{semana:02d}\n"
        f"gerado_em: {agora.isoformat()}\n"
        f"modelos: nosis={MODEL_OBS}, thymos={MODEL_OBS}, sintese={MODEL_SINTESE}\n"
        f"---\n\n"
        f"# Reflexão — semana {ano}-W{semana:02d}\n\n"
        f"## Nosis (camada cognitiva)\n\n{nosis_out}\n\n"
        f"## Thymos (camada volitiva)\n\n{thymos_out}\n\n"
        f"## Síntese (CEX-leve)\n\n{sintese_out}\n"
    )

    arquivo = f"projetos/gus/reflexoes/{ano}-W{semana:02d}-reflexao.md"
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)
    with open(arquivo, "w", encoding="utf-8") as f:
        f.write(conteudo)

    print(f"Escrito em {arquivo}")
    notificar_telegram(arquivo)


if __name__ == "__main__":
    main()
