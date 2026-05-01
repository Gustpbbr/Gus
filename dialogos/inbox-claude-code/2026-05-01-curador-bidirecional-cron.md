---
tipo: demanda
origem: gustavo
destino: claude-code
prioridade: alta
status: pendente
criado_em: 2026-05-01T02:50:00-03:00
processado_em: ""
processado_por: ""
acao_sugerida: criar_novo
destino_path: .github/workflows/curador-claude-code.yml
contexto: "Captura de memória das portas Claude Code e Claude Chat hoje é zero. Retro Engine quebrado neste ambiente. Captura proativa via MCP falha por env vars. Caminho 2: cron GitHub Actions processa transcripts commitados pela sessão, roda curador bidirecional (gus+gustavo) com secrets do GitHub. Implementar fim-a-fim."
---

# Demanda — curador bidirecional via cron GitHub Actions (Caminho 2)

## Problema

Captura de memória da porta Claude Code está **completamente quebrada** no
Claude Code on the web:

1. Hook `Stop:retro-engine` é silent no-op (env vars `ANTHROPIC_API_KEY`,
   `QDRANT_URL`, `QDRANT_API_KEY` ausentes em `~/.claude/gus.env`)
2. Tools MCP `mcp__mem0-gus__salvar_memoria*` também falham (mesmo problema
   no MCP server local que roda como subprocess)
3. Captura proativa "Claude chama tool durante a sessão" não viável:
   - Mesmo se tools funcionassem, cada call pede autorização (UX quebra)
   - Depende do Claude lembrar — frágil

**Resultado:** zero fragmentos da porta Code no Hub. Conversas como esta
(decisão URL secret, descoberta de bugs, meta-reflexões) são perdidas
quando aba fecha. Próxima aba começa cega.

Mesma situação provavelmente vale pra Claude Chat (curador chat ingest
existe mas não tá ativo automaticamente).

## Caminho proposto: Cron GitHub Actions

```
[sessão Claude Code]
    ↓ (Stop hook)
salva transcript em _log/transcripts-claude-code/<session-id>.jsonl
    ↓ (commit + push automático)
[GitHub Actions cron — roda a cada 30min]
    ↓
1. Detecta transcripts novos (não processados)
2. Roda curador bidirecional Haiku × GPT-4o-mini paralelo
3. Extrai 2 listas por sessão:
   - autobiografia agente → user_id="gus"
   - fatos sobre Gustavo → user_id="gustavo"
4. Salva no Hub via hub.store.ingestar (com secrets QDRANT_*)
5. Move transcript pra _log/transcripts-claude-code/processados/
    ↓
[Hub Qdrant]
- ambos brains alimentados sem UX impact zero
- mesma lógica do curador TioGu (consistência arquitetural)
```

## Vantagens sobre Caminho 1 e 3

| Aspecto | Caminho 1 (env vars no hook) | Caminho 3 (proativa MCP) | **Caminho 2 (cron)** |
|---|---|---|---|
| Funciona neste ambiente | ❌ (não sabemos onde puxar vars) | ❌ (MCP falha sem QDRANT_*) | ✅ (secrets do GitHub Actions) |
| UX impact | nenhum | alto (autorização por call) | **nenhum** |
| Depende de Claude lembrar | não | sim (frágil) | **não** |
| Captura sessão completa | parcial | parcial | **completa (transcript inteiro)** |
| Bidirecional (gus + gustavo) | precisa modificar prompt | precisa Claude lembrar 2x | **trivial (curador já é genérico)** |
| Trabalho | depende do mistério das vars | tabela em CLAUDE.md (já fiz, vai reverter) | ~2-3h código |

## Componentes a implementar

### 1. Modificar `.claude/hooks/retro_engine.py`

Em vez de tentar chamar Haiku diretamente, salvar transcript em formato
canônico no repo:

```python
def main():
    # ... lê transcript_path do stdin ...
    transcript = _ler_transcript(transcript_path)
    if not transcript or len(transcript) < 200:
        return

    # NOVO: persist transcript pra cron processar depois
    session_id = uuid.uuid4().hex[:12]
    out_path = (
        REPO_ROOT / "_log" / "transcripts-claude-code"
        / f"{datetime.now(BRT).strftime('%Y-%m-%dT%H-%M')}__{session_id}.jsonl"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(transcript, encoding="utf-8")

    # Tenta extrair via Haiku se env disponível (modo legacy)
    # Caso contrário, transcript fica esperando o cron.
    try:
        fragmentos = _extrair_fragmentos(transcript)
        # ... salva como hoje ...
    except RuntimeError as e:
        log.info(f"Hook não tem env vars — transcript salvo pra cron processar: {out_path}")
        _logar_sessao(0, 0, [str(e)], f"(transcript salvo pra cron — {session_id})")
```

**Atenção PII:** transcripts vão pro repo público. Precisa filtrar/redigir
PII antes de commitar. Reusar `gus/patterns_sensiveis.py` (regex já existe).

### 2. Auto-commit do transcript

Hook precisa commit + push o transcript. Opções:
- **A:** Hook chama `git add + git commit + git push` direto (precisa SSH key
  ou gh CLI configurado — frágil)
- **B:** Hook só salva o arquivo. Outro hook (separate) ou o git-check
  hook commita junto com outras mudanças no fim da sessão. Já existe
  `~/.claude/stop-hook-git-check.sh` — pode ser estendido pra incluir
  transcripts também.
- **C:** Hook escreve em pasta gitignored + cron tem permissão GitHub
  Actions pra `git pull && process && git push` (mais limpo)

Recomendo **B** (reusa hook existente).

### 3. Script `.github/scripts/curador_claude_code.py`

```python
"""
Cron: lê _log/transcripts-claude-code/*.jsonl não processados,
roda curador bidirecional (Haiku × GPT-4o-mini paralelo),
salva fragmentos no Hub (gus + gustavo), move transcript pra processados/.
"""
import os
from pathlib import Path
from hub.curador import curar_turnos

TRANSCRIPTS_DIR = Path("_log/transcripts-claude-code")
PROCESSADOS_DIR = TRANSCRIPTS_DIR / "processados"

def processar_transcript(path: Path):
    conteudo = path.read_text(encoding="utf-8")
    if len(conteudo) < 200:
        path.rename(PROCESSADOS_DIR / path.name)
        return

    # Roda curador 2x: uma pra cada brain
    for user_id in ("gus", "gustavo"):
        await curar_turnos(
            conteudo,
            via="claude-code",
            user_id=user_id,
        )

    # Move pra processados/
    PROCESSADOS_DIR.mkdir(exist_ok=True)
    path.rename(PROCESSADOS_DIR / path.name)

def main():
    PROCESSADOS_DIR.mkdir(exist_ok=True)
    for path in sorted(TRANSCRIPTS_DIR.glob("*.jsonl")):
        if path.parent != TRANSCRIPTS_DIR:
            continue
        try:
            processar_transcript(path)
        except Exception as e:
            print(f"FAIL {path.name}: {e}")
```

**Decisão importante:** rodar `curar_turnos` 2x (uma por brain) é mais simples
mas custa 2x tokens. Alternativa: novo prompt do curador que retorna
`{"gus": [...], "gustavo": [...]}` numa só chamada Haiku/GPT. Mais eficiente
mas exige modificar `hub/curador.py:PROMPT_*`.

Default: 2x calls separadas (consistência com curador TioGu existente).

### 4. Workflow `.github/workflows/curador-claude-code.yml`

```yaml
name: Curador Claude Code (cron)

on:
  schedule:
    - cron: "*/30 * * * *"  # a cada 30 min
  workflow_dispatch:

permissions:
  contents: write  # pode commit nos transcripts/processados

jobs:
  process:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      - run: pip install -r requirements.txt -r .github/scripts/requirements.txt
      - name: Process transcripts
        env:
          QDRANT_URL: ${{ secrets.QDRANT_URL }}
          QDRANT_API_KEY: ${{ secrets.QDRANT_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: python .github/scripts/curador_claude_code.py
      - name: Commit processed transcripts
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add _log/transcripts-claude-code/
          git diff --cached --quiet || git commit -m "auto: processa transcripts Claude Code"
          git push
```

### 5. .gitignore / proteção PII

- Pasta `_log/transcripts-claude-code/` **NÃO** ignorada (precisa pro cron ler)
- Hook deve filtrar PII via `gus.patterns_sensiveis.SENSITIVE_PATTERNS` antes de salvar transcript
- Considerar criptografar transcripts em repouso (overkill talvez)

## Fases de implementação

**Fase 1 — Mínimo viável (1h):**
- Hook salva transcript no repo (sem PII filter ainda)
- Script cron processa, salva 2 brains
- Workflow cron a cada 30min
- Manual review do que é salvo nas primeiras execuções

**Fase 2 — PII (30min):**
- Adicionar filtro `patterns_sensiveis.py` no hook antes de salvar
- Adicionar tags/redação automáticas

**Fase 3 — Otimização (1h):**
- Modificar curador pra retornar `{"gus": [...], "gustavo": [...]}` numa só chamada
- Reduz custo Haiku/GPT pela metade

**Fase 4 — Estender pra Claude Chat (futuro):**
- Mesma arquitetura: Claude Chat exporta conversa pro Drive → cron processa
- Já existe parcial (`ingest_mem0_from_chat.py`) — adaptar pra bidirecional

## Critérios de sucesso

1. Após implementar, rodar `git log _log/transcripts-claude-code/` deve
   mostrar transcripts commitados após sessões reais
2. `mcp__mem0-gus__buscar_memorias(query="claude-code")` deve retornar
   fragmentos com `via=claude-code`
3. Tanto brain `gustavo` quanto `gus` devem ter fragmentos novos
4. UX: sessão Claude Code não percebe que captura tá rolando (zero atrito)

## Onde olhar

- `hub/curador.py` — função `curar_turnos` já genérica (aceita user_id)
- `gus/bot.py:152` — exemplo de call (`curar_turnos(trecho, via="telegram-claude", user_id="gustavo")`)
- `.github/scripts/ingest_mem0_from_chat.py` — exemplo de cron processing
- `.github/scripts/_hub_compat.py` — layer compat hub
- `.claude/hooks/retro_engine.py` — hook atual (a modificar)
- `~/.claude/stop-hook-git-check.sh` — hook commit existente

## Resultado esperado

PR implementando Fases 1+2 (mínimo viável + PII) numa branch só.
Pode ser pequeno (~150 linhas total). Mergear, esperar 1 ciclo do cron,
verificar no Hub que fragmentos novos apareceram com `via=claude-code`.
