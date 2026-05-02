---
tipo: estado-atual-sessao
atualizado: 2026-05-02T01:30-03:00
---

# Estado atual — handoff entre sessões

Documento vivo. Atualizar no fim de cada sessão Code que deixa algo no meio.

## Última sessão (2026-05-02 — Fase 1 do plano de saneamento do TioGu)

Sessão de hygiene/manutenção do bot Telegram. Plano completo no chat
`claude/project-discussion-fkfA8`. Sessões 1 e 2 da Fase 1 concluídas.

### Resumo executivo

Após análise técnica imparcial do TioGu, listamos pontos severos /
médios / cosméticos por categoria. Fase 1 = rede de segurança via
testes + tapar vazamentos críticos. **163 testes verdes**, suite
roda em ~3.5s.

### O que foi feito hoje

**Sessão 1 — Testes do caminho crítico (commit `55c1de8`):**
- Suite `tests/` com 142 testes em 6 arquivos
- Cobertura: `_chamar_claude_com_retry` (system="" omitido — bug
  histórico do curador 27/04 agora coberto), `salvar_memorias`
  (Hub-first com Mem0 fallback), `_load_state`/`_save_state`
  round-trip, `_validar_path` (traversal), `_extrair_json` (markdown
  fence), `escanear`/`redact` (PII), regex Dimagem
- Mocks: `anthropic.AsyncAnthropic`, `hub.store.ingestar/lembrar`
- Workflow `.github/workflows/tests.yml` em PR + push main
- `pyproject.toml` config pytest (asyncio_mode=auto)
- `requirements-dev.txt`
- Hook `scan_sensivel.py` ganhou `tests/` na ALLOW_PREFIXES (fixtures
  sintéticas precisam parecer PII pra testar o detector)

**Sessão 2 — PII output + byte budget + cleanup (commit `d8ee949`):**
- **S2 PII no output:** `_redigir_resposta()` em `gus/bot.py` reusa
  `redact()` de `patterns_sensiveis`. Aplicado em `_responder` antes
  do `reply_text`. Anexa nota visível ao Gustavo listando tipos
  redatados. Fecha a brecha — antes scan só rodava no save, agora
  cobre saída direta do bot tb (defesa em layers).
- **S5 byte budget cache mídia:** `_CACHE_MAX` (count) → `_CACHE_MAX_ITEMS=50`
  + `_CACHE_MAX_BYTES=200MB`. Ejeção LRU por count OU bytes. Item único
  maior que budget aceito (PDF max 32MB cabe folgado). Container
  Railway pequeno protegido contra OOM.
- **C1** `gus/logger.py`: 3 linhas mortas removidas
- **C4** `gus/memory.py`: `VIA_DEFAULT` virou `_via_default()` lazy
- **C5** `gus/llm.py`: `_build_tools_cached` com anchor por nome
  estável (`rotear_arquivo`); fallback pro último + warn no log se
  anchor sumir. Reorder acidental detectável.
- **C6** `gus/llm.py`: fallback openai→anthropic concatena ambas
  exceções na resposta. Antes só mostrava erro do OpenAI mesmo quando
  Anthropic também falhava.
- +21 testes (TestRedigirResposta, TestContentBytes, TestCachePut*)

### Validação

Suite local: **163 passed in 3.54s**. CI verde após push.

## Pendente pra próxima sessão

### Fase 2A — Reconciliação docs estáticas (próxima sessão, ~2h)

1. **M8/M10** ✅ FEITO HOJE — `scripts/gerar_lista_tools.py` lê
   `gus/tools.py:TOOLS` e gera `projetos/gus/_tools-inventario.md` auto.
   Workflow `sync-docs.yml` cron 04h BRT + push em mudanças.
   Confirmou **21 tools reais** (system_prompt mente em "22").
2. **P9** ✅ FEITO HOJE — `_estado-atual.md` (este arquivo) +
   `gus-26-status-consolidado.md` atualizados pra 02/05.
3. **P10** decidir `gus-08-plano-proximos-passos.md` (24/04 obsoleto):
   mover pra `historico/` é o plano (itens A-H foram quase todos feitos).

### Fase 2B — System prompt (próxima sessão dedicada, ~2h)

**Risco alto** — bot lê isso em produção. Vai isolada.

- **S3** reescrever `gus/system_prompt.md` (794 linhas → ~500):
  - Conta de tools real (21, vai virar `len(TOOLS)`)
  - Unificar fluxo Dimagem (documentado 2x hoje)
  - Remover seções pré-migração ADR-001 (Mem0 silêncio, Mem0 fallback
    histórico, etc.)
  - Diff explícito mostrado pra Gustavo aprovar antes do commit

### Fase 3 — Operacional (~3h)

- **S4** alerta proativo HARD_LIMIT (cron check-cost.yml + 2º canal)
- **M5** cache `auto_diagnostico` 5min
- **M7** `/foco` deleta FOCO-ATUAL antigo antes de salvar novo

### Fase 4 — Refator estrutural (~6h, depende Fase 1 done ✅)

Decisões já tomadas:
- **D3 = C** — `drop_pending_updates=True` mantido + aviso ao Gustavo
  no boot se houver msgs pendentes
- **D4 = A** — mover `gus/dimagem.py` → `gus/integrations/dimagem.py`

Tarefas:
- **M1** split `gus/bot.py` em `gus/handlers/{text,photo,document,voice,commands}.py`
  + `gus/state.py`
- **M2** promover `_chamar_claude_com_retry` → público (curador
  importa privada, frágil)
- **C3** split `gus/tools.py` (1140 linhas)
- **C2** threadsafe `_get_openai_client`
- **C7** ✅ planejado mover `dimagem.py` na Fase 4

### Fase 5 — Decisões pendentes Gustavo (paralelo)

Tratado em aba separada da Claude Chat:
- **P1** captura Claude Chat (A/B/C)
- **P2** Drive sync OAuth (1/2/3)
- **P3** NeuroGus (decisões 11.1-11.7)

Pendente do Gustavo aqui:
- **P7** Custom GPT desktop — configurar Action no Builder
- **P8** limpar 4+ memórias poluídas no brain `gustavo`

### Fase 6 — Aposentar Mem0 (bloqueado até 12/05)

- Coleta dual Haiku × GPT termina **12/05/2026**
- Após: Gustavo escolhe modelo, Code limpa fallback, remove `mem0ai`,
  remove secret `MEM0_API_KEY`, upgrade `anthropic` SDK 0.40 → 0.50+

### Fase 7 — NeuroGus (sprint dedicado, depende decisão P3)

~145 LOC: `hub/events.py` + `broadcast()` + 2 endpoints SSE +
`api/neurogus.py` (PWA). Plano completo em `gus-30-neurogus-roadmap.md`.

## Branch atual

`claude/project-discussion-fkfA8` — onde está rolando o plano de
saneamento. Commits Fase 1 já mergeáveis pra main.

## Bugs em aberto (não bloqueantes)

- 4+ memórias poluídas no brain `gustavo` aguardando limpeza manual
  via MCP (P8)
- DDG fallback ativa quando Tavily esgota cota (esperado, sem ação)
- Hub Qdrant pode ficar ocioso por horas em janela noturna (sem ação)

## Mudanças no projeto desde o último estado-atual (27/04)

PRs entre 27/04 e 02/05:
- **#57/#58/#60** MCP server público no Railway com URL secret no
  path — Claude Chat web acessa Hub via MCP
- **#63** arquiva 2 demandas MCP resolvidas
- **#64** captura transcripts Claude Code via cron — Stop hook salva
  transcript redatado, cron */30min processa via curador. Resolve
  problema de captura no Code web (env vars ausentes)
- **#67** curador-chat bidirecional (gustavo + gus) com Sonnet 4.6 +
  GPT-4o top-tier. Bug fix `resultado["sonnet"]` → `["gpt"]` (logs
  estavam mentindo havia semanas)

## Como usar este arquivo

1. Próxima sessão Code: ler ANTES de outras coisas. Pega o fio dos PRs
   recentes, do plano em curso, das decisões já tomadas.
2. Ao fim da sessão: atualizar "Última sessão" + "Pendente" com o que
   ficou no meio. Commit + push antes de encerrar.

Relacionado: [[gus-01-visao-geral]], [[gus-15-decisao-migracao]],
[[gus-26-status-consolidado]], [[gus-30-neurogus-roadmap]]
