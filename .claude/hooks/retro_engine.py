#!/usr/bin/env python3
"""
Retro Engine — hook Stop do Claude Code.

Antecipa a Fase 5 do roadmap pre-AGI (gus-22): ao final de cada sessão Claude
Code, este hook captura o transcript completo e roda Haiku como Curador
focado em AUTOBIOGRAFIA DO AGENTE (não fatos sobre o Gustavo).

Resolve o "buraco fundo" identificado na sessão fiscal de 2026-04-27: hoje
sessões inteiras Claude Code geram insights, decisões e padrões que NÃO
viram memória persistente — ficam só em commits + chat. Próxima sessão
começa cega.

FLUXO:
  1. Recebe via stdin um JSON com transcript_path (Claude Code passa)
  2. Lê o arquivo de transcript da sessão
  3. Extrai conteúdo das mensagens em formato narrativo
  4. Chama Haiku com PROMPT_RETRO_ENGINE — focado em fragmentos
     do tipo "decisao_arquitetural", "meta_reflexao", etc.
  5. Pra cada fragmento: chama hub.store.ingestar com:
       via            = "claude-code"
       user_id        = "gus"  (autobiografia do agente, NÃO sobre Gustavo)
       tipo_esquecimento = "protegido" para tipos identitários
       camada_temporal = "permanente"
  6. Loga em _log/retro-engine-claude-code/AAAA-MM-DD.md

NUNCA bloqueia o fim da sessão. Falhar = perde uma sessão de retro,
mas não quebra nada.

VARIÁVEIS DE AMBIENTE (tipicamente carregadas de ~/.claude/gus.env):
  ANTHROPIC_API_KEY  — chamada Haiku
  QDRANT_URL         — Hub vector store
  QDRANT_API_KEY     — idem

Se as vars não estiverem disponíveis, o hook é no-op silencioso.
"""

import json
import logging
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Path do repo (pra importar hub.*) — hook roda na raiz do projeto
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [retro-engine] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

BRT = timezone(timedelta(hours=-3))
LOG_DIR = REPO_ROOT / "_log" / "retro-engine-claude-code"

# Limite defensivo — sessões muito longas viram custo caro pro Haiku
MAX_TRANSCRIPT_CHARS = 30_000


PROMPT_RETRO_ENGINE = """Você é o Retro Engine do Gus — agente pessoal do Gustavo Pratti de Barros.

Esta é a transcript de uma sessão da porta Claude Code (engenharia: editar
código, commitar, mergear). Sua tarefa: extrair fragmentos AUTOBIOGRÁFICOS
DO AGENTE GUS — não fatos sobre o Gustavo.

DIFERENÇA CRÍTICA:
- Fatos sobre o Gustavo (saúde, projetos, preferências) → vão pro `user_id="gustavo"`,
  são extraídos por OUTROS curadores (TioGu, Claude Chat). NÃO é seu trabalho aqui.
- Aprendizados sobre como o sistema Gus funciona, decisões arquiteturais
  tomadas, padrões observados pela própria instância → vão pro `user_id="gus"`.
  ISSO é seu trabalho.

TIPOS QUE VOCÊ EXTRAI:

- decisao_arquitetural — decisão técnica do sistema com contexto e raciocínio
  Ex: "Decidimos aposentar Mem0 e usar Qdrant direto porque schema fixo
  do Mem0 não comporta o gus-18"

- meta_reflexao — padrão de erro ou comportamento detectado
  Ex: "Tendo a misturar projetos distintos quando contexto da sessão fica longo"

- aprendizado_operacional — caveat de tool, padrão sobre como agir
  Ex: "Quando Gustavo diz 'pode' sem comando direto, ele está autorizando
  o último plano discutido"

- marco_evolutivo — momento em que o sistema ganhou capacidade nova
  Ex: "Primeiro deploy do Hub Qdrant em 2026-04-27"

- historia_sistema — fato sobre evolução do sistema
  Ex: "Em abril/2026 o Gus migrou de Mem0 hosted pra Qdrant self-hosted"

- procedural — protocolo ou procedimento estabelecido
  Ex: "Curador deve rodar Haiku + Sonnet em paralelo por 14 dias antes
  de decidir qual modelo manter"

REGRAS:

1. Cada fragmento = informação isolada e auto-suficiente. Sem "ele" / "isso"
   sem nomear.

2. Máximo 5 fragmentos por sessão. Sessões longas com muito ruído podem
   render só 1-2.

3. Se a sessão foi trivial (só leitura, sem decisão / aprendizado / marco),
   retorne `[]`.

4. Para tipos `decisao_arquitetural` e `marco_evolutivo`, sempre marque:
   - tipo_esquecimento: "protegido" (núcleo de identidade — nunca decai)
   - camada_temporal: "permanente"

5. Para `meta_reflexao` e `aprendizado_operacional`:
   - tipo_esquecimento: null (decai natural)
   - camada_temporal: "rotina"

FORMATO — apenas JSON válido, sem texto extra:

[
  {
    "conteudo": "texto auto-suficiente em pt-BR",
    "tipo": "<tipo>",
    "camada_temporal": "<camada>",
    "tipo_esquecimento": "<protegido|null>",
    "confianca": 0.0
  }
]

Transcript da sessão:

{transcript}
"""


def _ler_transcript(path: str) -> str:
    """Lê arquivo de transcript do Claude Code. Aceita JSONL ou texto plano."""
    p = Path(path)
    if not p.exists():
        return ""
    raw = p.read_text(encoding="utf-8", errors="ignore")

    # Se for JSONL (formato comum do Claude Code), extrai conteúdo das messages
    linhas_texto = []
    for linha in raw.splitlines():
        linha = linha.strip()
        if not linha:
            continue
        try:
            obj = json.loads(linha)
        except json.JSONDecodeError:
            linhas_texto.append(linha)
            continue
        # Tenta achar conteúdo textual em formatos comuns
        if isinstance(obj, dict):
            msg = obj.get("message") or obj.get("content") or obj
            if isinstance(msg, dict):
                role = msg.get("role", "?")
                content = msg.get("content")
                if isinstance(content, str):
                    linhas_texto.append(f"{role}: {content}")
                elif isinstance(content, list):
                    for bloco in content:
                        if isinstance(bloco, dict) and bloco.get("type") == "text":
                            linhas_texto.append(f"{role}: {bloco.get('text', '')}")
            elif isinstance(msg, str):
                linhas_texto.append(msg)

    texto = "\n".join(linhas_texto) if linhas_texto else raw
    if len(texto) > MAX_TRANSCRIPT_CHARS:
        # Mantém o início (contexto) + o fim (decisões finais)
        meio = MAX_TRANSCRIPT_CHARS // 2
        texto = texto[:meio] + "\n\n[…transcript truncado…]\n\n" + texto[-meio:]
    return texto


def _extrair_fragmentos(transcript: str) -> list[dict]:
    """Chama Haiku com PROMPT_RETRO_ENGINE. Retorna lista de fragmentos validados."""
    try:
        import anthropic
    except ImportError:
        log.warning("anthropic não disponível — hook no-op")
        return []

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        log.warning("ANTHROPIC_API_KEY ausente — hook no-op")
        return []

    client = anthropic.Anthropic(api_key=api_key, timeout=60.0)
    modelo = os.environ.get("MODEL_RETRO_ENGINE", "claude-haiku-4-5")
    prompt = PROMPT_RETRO_ENGINE.format(transcript=transcript)

    try:
        response = client.messages.create(
            model=modelo,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as e:
        log.warning(f"Haiku Retro Engine falhou: {e}")
        return []

    texto = next((b.text for b in response.content if hasattr(b, "text")), "") or ""
    return _parsear_json(texto)


def _parsear_json(texto: str) -> list[dict]:
    """Tolera cercas markdown e ruído. Retorna lista de dicts."""
    import re

    if not texto:
        return []
    texto = texto.strip()
    if texto.startswith("```"):
        texto = re.sub(r"^```(?:json)?\s*", "", texto)
        texto = re.sub(r"```\s*$", "", texto)
        texto = texto.strip()
    try:
        parsed = json.loads(texto)
        return parsed if isinstance(parsed, list) else []
    except json.JSONDecodeError:
        m = re.search(r"\[\s*(?:\{.*?\}\s*,?\s*)*\]", texto, re.DOTALL)
        if m:
            try:
                p = json.loads(m.group(0))
                return p if isinstance(p, list) else []
            except json.JSONDecodeError:
                return []
    return []


def _ingestar_no_hub(fragmentos: list[dict]) -> tuple[int, list[str]]:
    """Salva cada fragmento no Hub Qdrant via hub.store.ingestar."""
    try:
        from hub.store import ingestar
    except Exception as e:
        log.warning(f"hub.store indisponível — skipping: {e}")
        return 0, [f"hub.store import: {e}"]

    salvos = 0
    erros: list[str] = []
    for f in fragmentos:
        conteudo = (f.get("conteudo") or "").strip()
        if not conteudo or len(conteudo) < 15:
            continue
        tipo = (f.get("tipo") or "meta_reflexao").strip()
        camada = (f.get("camada_temporal") or "rotina").strip()
        esq = f.get("tipo_esquecimento")
        if esq == "null" or esq == "":
            esq = None

        try:
            ingestar(
                conteudo,
                {
                    "tipo": tipo,
                    "camada_temporal": camada,
                    "tipo_esquecimento": esq,
                    "area": "gus",
                    "confianca": float(f.get("confianca") or 0.7),
                    "via": "claude-code",
                    "user_id": "gus",  # autobiografia do agente
                    "curador": "haiku",  # sempre Haiku no Retro Engine
                },
            )
            salvos += 1
        except Exception as e:
            erros.append(f"ingestar: {str(e)[:120]}")
    return salvos, erros


def _logar_sessao(num_fragmentos: int, salvos: int, erros: list[str], resumo: str) -> None:
    """Append no MD diário pra fiscalização."""
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        hoje = datetime.now(BRT).strftime("%Y-%m-%d")
        log_path = LOG_DIR / f"{hoje}.md"
        agora = datetime.now(BRT).strftime("%H:%M:%S")

        if not log_path.exists():
            log_path.write_text(
                f"---\ndata: {hoje}\n"
                f"fonte: Retro Engine (hook Stop Claude Code)\n"
                f"tipo: log-retro-engine-claude-code\n---\n\n"
                f"# Retro Engine Claude Code — {hoje}\n\n",
                encoding="utf-8",
            )

        entrada = (
            f"## {agora} BRT — sessão encerrada\n"
            f"**Fragmentos extraídos:** {num_fragmentos}\n"
            f"**Salvos no Hub (user_id=gus):** {salvos}\n"
        )
        if erros:
            entrada += f"**Erros:** {' | '.join(erros[:3])}\n"
        if resumo:
            entrada += f"**Resumo:**\n> {resumo[:300]}\n"
        entrada += "\n"

        with log_path.open("a", encoding="utf-8") as f:
            f.write(entrada)
    except Exception as e:
        log.warning(f"_logar_sessao falhou: {e}")


def main() -> None:
    """Hook Stop — recebe JSON via stdin com info da sessão."""
    try:
        raw = sys.stdin.read()
    except Exception:
        log.info("Sem stdin — hook no-op")
        return

    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        log.info("stdin não é JSON — hook no-op")
        return

    transcript_path = (
        payload.get("transcript_path")
        or payload.get("transcript")
        or payload.get("session", {}).get("transcript_path", "")
    )

    if not transcript_path:
        log.info("Sem transcript_path no payload — hook no-op")
        return

    transcript = _ler_transcript(transcript_path)
    if not transcript or len(transcript) < 200:
        log.info(f"Transcript vazio ou trivial ({len(transcript)} chars) — no-op")
        return

    log.info(f"Processando transcript ({len(transcript)} chars)…")
    fragmentos = _extrair_fragmentos(transcript)

    if not fragmentos:
        log.info("Nenhum fragmento autobiográfico extraído — sessão trivial")
        _logar_sessao(0, 0, [], "(sessão trivial — nada extraído)")
        return

    salvos, erros = _ingestar_no_hub(fragmentos)
    log.info(f"Retro Engine: {salvos}/{len(fragmentos)} fragmentos salvos no Hub")
    if erros:
        for e in erros:
            log.warning(e)

    resumo = " | ".join(f.get("conteudo", "")[:80] for f in fragmentos[:3])
    _logar_sessao(len(fragmentos), salvos, erros, resumo)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # NUNCA quebra o fim da sessão Claude Code
        log.warning(f"Retro Engine erro inesperado: {e}")
        sys.exit(0)
