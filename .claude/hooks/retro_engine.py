#!/usr/bin/env python3
"""
Retro Engine — hook Stop do Claude Code.

Ao final de cada sessão, filtra o transcript para extrair apenas turnos
conversacionais reais (user/assistant texto), depois roda Haiku em loop
de tool use para registrar fragmentos autobiográficos do sistema Gus.

FLUXO:
  1. Recebe via stdin JSON com transcript_path
  2. Lê e filtra o JSONL: só role user/assistant, só blocos type=text,
     ignora continuation summaries injetados
  3. Haiku loop (até 8 rounds) com 2 tools:
       registrar_fragmento — chamada uma vez por fragmento extraído
       sessao_trivial      — encerra sem fragmentos
  4. Cada fragmento vai pro Hub Qdrant (user_id="gus", autobiografia)
  5. Loga em _log/retro-engine-claude-code/AAAA-MM-DD.md

VARIÁVEIS DE AMBIENTE:
  ANTHROPIC_API_KEY, QDRANT_URL, QDRANT_API_KEY
"""

import json
import logging
import os
import subprocess
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

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
TRANSCRIPTS_DIR = REPO_ROOT / "_log" / "transcripts-claude-code"

MAX_TRANSCRIPT_CHARS = 30_000

PROMPT_RETRO_ENGINE = """Você é o Retro Engine do Gus — agente pessoal do Gustavo Pratti de Barros.

Esta é a transcript de uma sessão da porta Claude Code (engenharia: editar
código, commitar, mergear). Sua tarefa: extrair fragmentos AUTOBIOGRÁFICOS
DO AGENTE GUS — não fatos sobre o Gustavo.

DIFERENÇA CRÍTICA:
- Fatos sobre Gustavo (saúde, projetos, preferências) → NÃO é seu trabalho aqui.
- Aprendizados sobre como o sistema Gus funciona, decisões arquiteturais
  tomadas, padrões observados pela própria instância → user_id="gus".

TIPOS QUE VOCÊ EXTRAI:

- decisao_arquitetural — decisão técnica do sistema com contexto e raciocínio
- meta_reflexao — padrão de erro ou comportamento detectado
- aprendizado_operacional — caveat de tool, padrão sobre como agir
- marco_evolutivo — momento em que o sistema ganhou capacidade nova
- historia_sistema — fato sobre evolução do sistema
- procedural — protocolo ou procedimento estabelecido

REGRAS:
1. Cada fragmento = informação isolada e auto-suficiente. Sem "ele"/"isso" sem nomear.
2. Máximo 5 fragmentos por sessão.
3. Se sessão foi trivial (só leitura, sem decisão/aprendizado/marco), chame sessao_trivial.
4. Para decisao_arquitetural e marco_evolutivo: tipo_esquecimento="protegido", camada_temporal="permanente"
5. Para meta_reflexao e aprendizado_operacional: tipo_esquecimento="null", camada_temporal="rotina"

Use as ferramentas para registrar cada fragmento. Quando terminar (ou se não houver nada),
chame sessao_trivial ou simplesmente encerre.

Transcript da sessão:

{transcript}
"""

TOOLS_RETRO = [
    {
        "name": "registrar_fragmento",
        "description": (
            "Registrar um fragmento autobiográfico do sistema Gus extraído desta sessão. "
            "Chame uma vez por fragmento identificado (máximo 5)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "conteudo": {
                    "type": "string",
                    "description": "Texto auto-suficiente em pt-BR. Sem pronomes sem referência.",
                },
                "tipo": {
                    "type": "string",
                    "enum": [
                        "decisao_arquitetural",
                        "meta_reflexao",
                        "aprendizado_operacional",
                        "marco_evolutivo",
                        "historia_sistema",
                        "procedural",
                    ],
                },
                "camada_temporal": {"type": "string", "enum": ["permanente", "rotina"]},
                "tipo_esquecimento": {"type": "string", "enum": ["protegido", "null"]},
                "confianca": {
                    "type": "number",
                    "description": "0.0 a 1.0",
                },
            },
            "required": ["conteudo", "tipo", "camada_temporal", "tipo_esquecimento", "confianca"],
        },
    },
    {
        "name": "sessao_trivial",
        "description": "Marcar sessão como trivial — sem fragmentos autobiográficos para extrair.",
        "input_schema": {
            "type": "object",
            "properties": {
                "motivo": {
                    "type": "string",
                    "description": "Breve explicação de por que a sessão foi trivial.",
                }
            },
            "required": ["motivo"],
        },
    },
]

_CONTINUATION_MARKERS = (
    "This session is being continued from a previous conversation",
    "Continue from where you left off",
)


def _ler_transcript(path: str) -> str:
    """Lê JSONL do Claude Code, filtrando só turnos conversacionais reais."""
    p = Path(path)
    if not p.exists():
        return ""
    raw = p.read_text(encoding="utf-8", errors="ignore")

    linhas_texto = []
    for linha in raw.splitlines():
        linha = linha.strip()
        if not linha:
            continue
        try:
            obj = json.loads(linha)
        except json.JSONDecodeError:
            continue

        if not isinstance(obj, dict):
            continue

        tipo = obj.get("type", "")
        if tipo not in ("user", "assistant"):
            continue

        msg = obj.get("message", {})
        if not isinstance(msg, dict):
            continue

        role = msg.get("role", "")
        content = msg.get("content")

        if isinstance(content, str):
            # Ignora summaries de continuação injetados pelo sistema
            if any(m in content for m in _CONTINUATION_MARKERS):
                continue
            if content.strip():
                linhas_texto.append(f"{role}: {content.strip()}")
        elif isinstance(content, list):
            for bloco in content:
                if not isinstance(bloco, dict):
                    continue
                # Só texto real — ignora tool_use, tool_result, thinking
                if bloco.get("type") == "text":
                    texto = bloco.get("text", "").strip()
                    if texto:
                        linhas_texto.append(f"{role}: {texto}")

    texto = "\n\n".join(linhas_texto)

    if len(texto) > MAX_TRANSCRIPT_CHARS:
        # Prioriza o fim da sessão (onde ficam as decisões)
        texto = "[…início truncado…]\n\n" + texto[-MAX_TRANSCRIPT_CHARS:]

    return texto


def _extrair_fragmentos(transcript: str) -> list[dict]:
    """Loop de tool use com Haiku. Retorna lista de fragmentos coletados."""
    try:
        import anthropic
    except ImportError:
        log.warning("anthropic não disponível — hook no-op")
        return []

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        log.warning("ANTHROPIC_API_KEY ausente — hook no-op")
        return []

    client = anthropic.Anthropic(api_key=api_key, timeout=90.0)
    modelo = os.environ.get("MODEL_RETRO_ENGINE", "claude-haiku-4-5")
    prompt = PROMPT_RETRO_ENGINE.format(transcript=transcript)

    messages: list[dict] = [{"role": "user", "content": prompt}]
    fragmentos: list[dict] = []

    for rnd in range(8):
        try:
            response = client.messages.create(
                model=modelo,
                max_tokens=2048,
                tools=TOOLS_RETRO,
                messages=messages,
            )
        except Exception as e:
            log.warning(f"Haiku round {rnd} falhou: {e}")
            break

        tool_calls = [b for b in response.content if hasattr(b, "type") and b.type == "tool_use"]

        if not tool_calls or response.stop_reason == "end_turn":
            break

        tool_results = []
        encerrar = False

        for tc in tool_calls:
            if tc.name == "sessao_trivial":
                log.info(f"sessao_trivial: {tc.input.get('motivo', '')[:80]}")
                encerrar = True
                tool_results.append({"type": "tool_result", "tool_use_id": tc.id, "content": "ok"})

            elif tc.name == "registrar_fragmento":
                if len(fragmentos) < 5:
                    fragmentos.append(tc.input)
                    log.info(
                        f"fragmento [{tc.input.get('tipo')}]: "
                        f"{str(tc.input.get('conteudo', ''))[:60]}"
                    )
                tool_results.append({"type": "tool_result", "tool_use_id": tc.id, "content": "registrado"})

        # Serializa content blocks para dict (compatibilidade com API)
        content_dicts = []
        for b in response.content:
            if b.type == "text":
                content_dicts.append({"type": "text", "text": b.text})
            elif b.type == "tool_use":
                content_dicts.append({"type": "tool_use", "id": b.id, "name": b.name, "input": b.input})

        messages.append({"role": "assistant", "content": content_dicts})
        messages.append({"role": "user", "content": tool_results})

        if encerrar or len(fragmentos) >= 5:
            break

    return fragmentos


def _persist_transcript_pra_cron(transcript: str) -> tuple[Path | None, list[str]]:
    """Salva transcript redatado em _log/transcripts-claude-code/ pro cron processar.

    Aplica redação PII via gus.patterns_sensiveis.redact() antes de salvar.
    Retorna (path, lista_tipos_redatados). path=None se falhou.
    """
    try:
        from gus.patterns_sensiveis import redact
        transcript_safe, redatados = redact(transcript)
    except Exception as e:
        log.warning(f"redact() falhou — não salva transcript: {e}")
        return None, []

    try:
        TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
        session_id = uuid.uuid4().hex[:12]
        nome = f"{datetime.now(BRT).strftime('%Y-%m-%dT%H-%M')}__{session_id}.jsonl"
        out_path = TRANSCRIPTS_DIR / nome
        out_path.write_text(transcript_safe, encoding="utf-8")
        return out_path, redatados
    except Exception as e:
        log.warning(f"Não consegui escrever transcript: {e}")
        return None, []


def _commit_e_push_transcript(path: Path) -> bool:
    """git add + commit + push do transcript salvo. Fallback gracioso."""
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=REPO_ROOT, text=True, stderr=subprocess.DEVNULL,
        ).strip()
    except Exception as e:
        log.warning(f"git branch falhou: {e}")
        return False

    if not branch.startswith("claude/"):
        log.info(f"Branch '{branch}' não é claude/* — transcript fica local, não commita")
        return False

    try:
        subprocess.run(
            ["git", "add", str(path.relative_to(REPO_ROOT))],
            cwd=REPO_ROOT, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
        )
        subprocess.run(
            ["git", "commit", "-m", f"chore(transcripts): captura sessão {path.stem}"],
            cwd=REPO_ROOT, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
        )
        subprocess.run(
            ["git", "push", "origin", branch],
            cwd=REPO_ROOT, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            timeout=30,
        )
        log.info(f"Transcript pushed pra origin/{branch}")
        return True
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode("utf-8", errors="ignore") if e.stderr else ""
        log.warning(f"git falhou ({e.returncode}): {stderr[:200]}")
        return False
    except Exception as e:
        log.warning(f"git inesperado: {e}")
        return False


def _ingestar_no_hub(fragmentos: list[dict]) -> tuple[int, list[str]]:
    """Salva cada fragmento no Hub Qdrant via hub.store.ingestar."""
    try:
        from hub.store import ingestar
    except Exception as e:
        log.warning(f"hub.store indisponível: {e}")
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
        if esq in ("null", "", None):
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
                    "user_id": "gus",
                    "curador": "haiku",
                },
            )
            salvos += 1
        except Exception as e:
            erros.append(f"ingestar: {str(e)[:120]}")

    return salvos, erros


def _logar_sessao(num_fragmentos: int, salvos: int, erros: list[str], resumo: str) -> None:
    """Append no MD diário."""
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

        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(entrada)
    except Exception as e:
        log.warning(f"_logar_sessao falhou: {e}")


def main() -> None:
    """Hook Stop — recebe JSON via stdin."""
    try:
        raw = sys.stdin.read()
    except Exception:
        return

    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return

    transcript_path = (
        payload.get("transcript_path")
        or payload.get("transcript")
        or payload.get("session", {}).get("transcript_path", "")
    )

    if not transcript_path:
        log.info("Sem transcript_path — hook no-op")
        return

    transcript = _ler_transcript(transcript_path)
    if not transcript or len(transcript) < 200:
        log.info(f"Transcript vazio/trivial ({len(transcript)} chars) — no-op")
        return

    out_path, redatados = _persist_transcript_pra_cron(transcript)
    pushed = False
    if out_path:
        log.info(
            f"Transcript salvo: {out_path.name} "
            f"(PII redatada: {len(redatados)} matches)"
        )
        pushed = _commit_e_push_transcript(out_path)

    log.info(f"Processando transcript ({len(transcript)} chars)…")
    fragmentos = _extrair_fragmentos(transcript)

    if not fragmentos:
        log.info("Nenhum fragmento extraído")
        _logar_sessao(0, 0, [], "(nenhum fragmento)")
        return

    salvos, erros = _ingestar_no_hub(fragmentos)
    log.info(f"Retro Engine: {salvos}/{len(fragmentos)} fragmentos salvos")
    for e in erros:
        log.warning(e)

    resumo = " | ".join(f.get("conteudo", "")[:80] for f in fragmentos[:3])
    _logar_sessao(len(fragmentos), salvos, erros, resumo)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log.warning(f"Retro Engine erro inesperado: {e}")
        sys.exit(0)
