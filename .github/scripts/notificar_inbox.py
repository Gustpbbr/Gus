#!/usr/bin/env python3
"""
Notifica Telegram quando demanda nova chega em dialogos/inbox-tiogu/.

Estágio 0 do roteamento de demandas (notificação-only, custo zero).

INPUT (env):
  ARQUIVOS_NOVOS  — paths separados por newline, vindos de
                    git diff --diff-filter=A no workflow
  TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID — secrets

OUTPUT:
  Pra cada arquivo: 1 mensagem no Telegram com preview, frontmatter,
  e sugestão de ação. Não move nada, não rotea, só avisa.

GANHA:
  - Validação de que trigger funciona em produção
  - Visibilidade imediata pro Gustavo quando algo chega
  - Sinal pra avançar pro Estágio 1 (TioGu como roteador)

NÃO FAZ:
  - Roteamento automático (Estágio 1)
  - Decisão por agente (Estágio 2)
  - Mover/apagar arquivo
"""

import os
import sys
from pathlib import Path

import httpx
import yaml


def parse_frontmatter(content: str):
    """Extrai frontmatter YAML do início do .md. Retorna (dict|None, body)."""
    if not content.startswith("---"):
        return None, content
    end = content.find("\n---", 3)
    if end == -1:
        return None, content
    fm_str = content[3:end].strip()
    body = content[end + 4:].lstrip("\n")
    try:
        fm = yaml.safe_load(fm_str)
        if not isinstance(fm, dict):
            return None, content
        return fm, body
    except yaml.YAMLError:
        return None, content


def primeiro_titulo(body: str) -> str:
    """Pega primeira linha começando com '# '. Fallback: primeira linha não-vazia."""
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("# "):
            return s[2:].strip()
    for line in body.splitlines():
        s = line.strip()
        if s and not s.startswith("---"):
            return s[:80]
    return "(sem título)"


def montar_mensagem(arquivo: str, fm: dict | None, body: str) -> str:
    """Monta mensagem legível pro Telegram."""
    titulo = primeiro_titulo(body)
    nome_arquivo = Path(arquivo).name

    if fm is None:
        return (
            f"Novo no inbox-tiogu (sem frontmatter)\n\n"
            f'"{titulo}"\n\n'
            f"Caminho: {arquivo}\n"
            f"Aviso: arquivo sem frontmatter — pode ser conteúdo bruto."
        )

    origem = fm.get("origem", "?")
    prioridade = fm.get("prioridade", "?")
    tipo = fm.get("tipo", "?")
    status = fm.get("status", "?")

    # Campos opcionais novos (pra roteamento — Estágio 1+)
    acao = fm.get("acao_sugerida")
    destino_path = fm.get("destino_path")
    contexto = fm.get("contexto")

    linhas = [
        f"Novo no inbox-tiogu (origem: {origem})",
        "",
        f'"{titulo}"',
        "",
        f"tipo: {tipo} | prioridade: {prioridade} | status: {status}",
    ]

    if acao or destino_path:
        linhas.append("")
        linhas.append("Roteamento sugerido pelo origem:")
        if acao:
            linhas.append(f"  ação: {acao}")
        if destino_path:
            linhas.append(f"  destino: {destino_path}")

    if contexto:
        linhas.append("")
        linhas.append(f"Contexto: {contexto[:200]}")

    linhas.append("")
    linhas.append(f"Caminho no repo: {arquivo}")

    if status != "pendente":
        linhas.append("")
        linhas.append(f"(status atual: {status} — provavelmente já tratada)")

    return "\n".join(linhas)


def notificar(mensagem: str) -> bool:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print(f"[skip] TELEGRAM_BOT_TOKEN/CHAT_ID ausentes — não notifico", file=sys.stderr)
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        with httpx.Client(timeout=15) as c:
            r = c.post(url, json={"chat_id": chat_id, "text": mensagem})
        if r.status_code != 200:
            print(f"[erro] Telegram {r.status_code}: {r.text[:200]}", file=sys.stderr)
            return False
        return True
    except Exception as e:
        print(f"[erro] Telegram exception: {e}", file=sys.stderr)
        return False


def main():
    arquivos_raw = os.environ.get("ARQUIVOS_NOVOS", "").strip()
    if not arquivos_raw:
        print("Nenhum arquivo novo em dialogos/inbox-tiogu/ neste push.")
        sys.exit(0)

    arquivos = [a.strip() for a in arquivos_raw.splitlines() if a.strip()]
    arquivos = [a for a in arquivos if a.endswith(".md") and "_README" not in a]

    if not arquivos:
        print("Nenhum .md relevante (todos eram _README ou não-md).")
        sys.exit(0)

    print(f"Detectados {len(arquivos)} arquivo(s) novo(s) em inbox-tiogu:")
    for a in arquivos:
        print(f"  - {a}")

    notificados = 0
    erros = 0

    for arquivo in arquivos:
        path = Path(arquivo)
        if not path.exists():
            print(f"[skip] {arquivo} não existe (pode ter sido movido logo após push)")
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"[erro] Falha ao ler {arquivo}: {e}", file=sys.stderr)
            erros += 1
            continue

        fm, body = parse_frontmatter(content)
        msg = montar_mensagem(arquivo, fm, body)

        ok = notificar(msg)
        if ok:
            notificados += 1
            print(f"  [ok] notificado: {arquivo}")
        else:
            erros += 1

    print(f"\nResumo: {notificados} notificado(s), {erros} erro(s)")


if __name__ == "__main__":
    main()
