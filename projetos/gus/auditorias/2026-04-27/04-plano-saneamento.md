---
tipo: auditoria-fiscal
parte: 04-de-06
ordem_leitura: 5
gerado_em: 2026-04-27T09:55:00-03:00
gerado_por: claude-code
escopo: origin/main @ 2026-04-27 manhã
status: rascunho-fiscal
---

# Plano de saneamento — etapas A–I

Voltar: [[00-leia-primeiro]] · Anterior: [[03-inconsistencias-medias-baixas]] · Próximo: [[05-design-auto-merge]]

---

## Visão geral (ordem e dependências)

```
[ Triagem rápida (1h) ]
  └─ A. Fechar demanda fix-qdrant já resolvida (R4)  ✅ FEITA — commit 98e8125

[ Crítico 1 — Estancar hemorragia (1-2h) ]
  └─ B. Curadoria automática quebrada (R1)
      ⚠ Resolver ANTES de tudo
      ⚠ Decisão Gustavo: HÍBRIDO Haiku + Sonnet com assinatura via metadata.curador

[ Crítico 2 — Alinhar arquitetura Mem0 (2-4h) ]
  ├─ C. Decisão Qdrant vs SaaS (R2)  ✅ DECIDIDA: C1 (Qdrant é destino único)
  └─ D. Migrar MCP mem0-gus + scripts não-migrados (R6 ⊂ R2)

[ Crítico 3 — LGPD (1-2h) ]
  ├─ E. Quarentena memórias de pacientes (R3, urgente)
  └─ F. Política preventiva no curador (R3, depende de B)

[ Altos — fortalecer (2-3h) ]
  ├─ G. Fonte única de patterns sensíveis (R7)
  └─ H. Decidir caminho Drive→GitHub (R8)

[ Cosmético controlado (1h, por último) ]
  └─ I. Atualizar docs mestre (R5)
       ⚠ Só DEPOIS de B, C, D estabilizados ≥48h
```

**Total estimado restante (sem A já feita):** 7-12h de Claude Code + decisões pontuais suas.

---

## A — Fechar demanda já resolvida (R4) ✅

**Status:** FEITA em 2026-04-27 09:12 BRT.

**Commit:** `98e8125 fix(dialogos): fechar demanda fix-qdrant-search-bug` na branch `claude/greeting-checkin-NAcVz`.

**Para ativar archive workflow:** mergear esta branch pra `main`. Após merge, `archive-completed-demandas.yml` move o arquivo em ≤15min, demanda some de `inbox-claude-code/` e aparece em `archive/` + `historico/2026-04.md`.

---

## B — Curadoria híbrida Haiku + Sonnet com assinatura

### Princípio

A cada janela de 3 turnos do Telegram, **dois resumos são gerados (Haiku e Sonnet) em paralelo**, **cada um vira uma memória independente** no Qdrant com `metadata.curador="haiku"` ou `"sonnet"`. Você não escolhe qual entra — ambos entram, com etiqueta. Daí depois você compara.

### B.0 — Pré-investigação (15min)

1. Pegar o erro 400 inteiro (log corta em "`temperature` and `top_p` can[…]")
2. Conferir onde os params são montados (`_chamar_claude_com_retry` ou config externa)
3. Decidir prompt do Sonnet: **B.0.a** mesmo do Haiku (variar 1 coisa por vez) ou **B.0.b** mais seletivo. Recomendação: **B.0.a primeiro**

### B.1 — Schema da memória

```yaml
memory: "<texto do resumo>"
metadata:
  via: "telegram-claude"
  curador: "haiku"           # NOVO — "haiku" | "sonnet"
  janela_turnos: 6           # NOVO
  hash_janela: "<sha8>"      # NOVO — pareia haiku↔sonnet do mesmo trecho
```

### B.2 — Refator `gerar_resumo_turnos` (gus/llm.py)

- Trocar retorno de `str` pra `list[tuple[str, str]]` = `[(modelo, resumo), ...]`
- Rodar Haiku + Sonnet em paralelo (`asyncio.gather`)
- Se um falhar, retorna apenas a tupla do que funcionou
- Cada call passa SÓ `temperature` (ou nenhum) — fix do bug 400 incluso

### B.3 — Refator `_resumir_e_salvar` (gus/bot.py)

- Recebe lista de tuplas
- Computa `hash_janela = sha256(joined_texts)[:8]`
- Pra cada `(modelo, resumo)`: salva memória com `metadata_extra={"curador": modelo, "hash_janela": hash}`
- Loga ambos no `_log/resumos-mem0/AAAA-MM-DD.md`

### B.4 — `gus/memory.py` aceita metadata extra

```python
async def salvar_memorias(messages, user_id="gustavo", via=None, metadata_extra=None):
    metadata = {"via": via or VIA_DEFAULT, **(metadata_extra or {})}
```

### B.5 — Log auditável

Atualizar formato pra incluir `curador` e `hash_janela`:

```
## 17:58:41 BRT — salvo (curador: haiku, janela: a3f29b1c)
## 17:58:41 BRT — salvo (curador: sonnet, janela: a3f29b1c)
```

### B.6 — Validação

1. Mandar 4 mensagens no Telegram (3 turnos + 1)
2. Conferir log ganha 2 entradas (haiku + sonnet) com mesmo hash
3. Conferir Qdrant via MCP (depois do C1) lista ambas
4. Custo: estimativa rude $1/mês a mais (aceitável)

### B.7 — Avaliação posterior (não é fix, é uso)

Após 7-14 dias: comparar pares hash_janela, densidade por área, falsos positivos LGPD, custo. Decidir: só Sonnet, só Haiku, ou híbrido permanente.

### B.8 — Fechar a demanda

Marcar `2026-04-27T06-16__curadoria-mem0-sonnet-nao-haiku.md` como concluído com `## Resultado` apontando o commit + decisão híbrida.

---

## C — Decisão Qdrant vs SaaS ✅ DECIDIDA

**Decisão:** C1 — Qdrant é destino único.

Implicações:
- Migrar TUDO pra Qdrant
- Cancelar conta Mem0 SaaS depois
- Atualizar docs (refs a "Mem0 hosted") na etapa I

---

## D — Migração arquivo a arquivo

### D.0 — Inventário (45min)

```bash
grep -rn "MemoryClient\|from mem0 import\|MEM0_API_KEY" \
  .claude/ .github/ gus/ api/ \
  | grep -v "^Binary" \
  > /tmp/mem0_refs.txt
```

Classificar cada hit em **MIGRAR**, **ARQUIVAR** ou **DELETAR**.

Confirmar paridade Qdrant ↔ SaaS antes de seguir (ambos devem ter ~204 mems).

### D.1 — Helper compartilhado em `gus/memory.py`

Extrair config Qdrant pra função pública `build_qdrant_memory()`. Todos os scripts/MCP usam essa função em vez de instanciar Memory por conta própria.

### D.2 — Migrar MCP `mem0-gus`

- Trocar `from mem0 import MemoryClient` por `from gus.memory import build_qdrant_memory`
- Verificar API: `Memory` (self-hosted) vs `MemoryClient` (SaaS) — assinaturas iguais? especialmente `get_all` paginação
- Atualizar header doc + `.mcp.json` (tirar fallback `~/.claude/mem0.key`)

### D.3 — Migrar scripts (ordem por blast radius, baixo→alto)

1. `enrich_mem0_export.py` (sem cron, isolado)
2. `auditoria_mem0.py` (cron 06h diário)
3. `export_mem0.py` (cron 03h diário) — decidir: migra ou arquiva?
4. `briefing_matinal.py` (cron 07h dias úteis) — visível
5. `retrospectiva_semanal.py` (cron sex 20h)
6. `ingest_mem0_from_chat.py` (cron 30min) — mais frequente, por último

Pra cada: trocar `MemoryClient` por `build_qdrant_memory()`, atualizar workflow secrets, rodar `workflow_dispatch` antes de deixar pro cron, comparar saída antes vs depois.

### D.4 — Arquivar one-shots

Mover pra `.github/{scripts,workflows}/_legado/`:
- `migrate_mem0.py`, `migrate-mem0-to-qdrant.yml`
- `reset_qdrant_collection.py`, `fix-qdrant-dims.yml`

### D.5 — Atualizar secrets do GitHub

Garantir `QDRANT_URL`, `QDRANT_API_KEY`, `ANTHROPIC_API_KEY` em todos os workflows migrados. **Não remover `MEM0_API_KEY` ainda** — só após D.6.

### D.6 — Limpeza final (depois de 7 dias estável)

1. Re-grep `MemoryClient` — zero hits (exceto em `_legado/`)
2. Remover `MEM0_API_KEY` dos secrets do GitHub
3. Cancelar conta Mem0 SaaS no painel (você executa)
4. Tirar `MEM0_API_KEY` do `~/.claude/gus.env` e `.mcp.json`

### D.7 — Validação consolidada

- MCP daqui retorna ~204 (igual auditoria)
- Bot Telegram + API + auditoria amanhã + briefing amanhã: todos consistentes
- Curadoria híbrida (B): ambas memórias aparecem

### D.8 — Atualização cosmética

Atualizar `gus-15-decisao-migracao.md` (status: decidido → executado) e `gus-23-logica-qdrant-mem0.md` (deixou de ser "convivência" → só Qdrant).

---

## E — Quarentena LGPD (urgente)

### E.0 — Pré-investigação (15min)

Buscar memórias de pacientes:

```python
mcp__mem0-gus__buscar_memorias("MRI Assim São Gonçalo", limit=30)
mcp__mem0-gus__buscar_memorias("paciente", limit=30)
mcp__mem0-gus__buscar_memorias("Intermédica", limit=20)
mcp__mem0-gus__buscar_memorias("propofol sedação", limit=20)
```

Pra cada: dado de paciente (apagar) ou discussão clínica genérica (manter)?

⚠ Se C+D ainda não foi feito: rodar quarentena nas DUAS fontes (SaaS + Qdrant), porque o MCP atual aponta pra SaaS.

### E.1 — Execução

- `mcp__mem0-gus__deletar_memoria(memory_id, user_id="gustavo")` pra cada
- Confirmar via `listar_memorias`
- Auditoria seguinte deve mostrar densidade `dimagem` reduzida

---

## F — Política preventiva (depende de B resolvido)

### F.1 — Atualizar `RESUMO_SYSTEM_PROMPT` (gus/llm.py)

Adicionar regra explícita:

```
NUNCA inclua nomes de pacientes do Dimagem, números de OS,
convênios específicos vinculados a indivíduos. Se a conversa
tratou de paciente, resuma como "Gustavo discutiu sedação de
paciente [pediátrico/adulto]" — sem nome.
```

### F.2 — Scan determinístico pós-resumo

Antes de salvar no Mem0, rodar regex pra padrões "Nome Sobrenome … MRI/exame". Se bater, bloqueia salvamento, loga `descartado-lgpd`.

### F.3 — Validação

Mandar OS Dimagem real no Telegram + 2 outras msgs (forçar 3 turnos). Conferir que resumo não vai pro Mem0 com nome.

---

## G — Fonte única de patterns sensíveis (R7)

### G.1 — Criar `gus/patterns_sensiveis.py`

Lista canônica única. `gus/tools.py` e `.claude/hooks/scan_sensivel.py` importam dela.

### G.2 — Adicionar patterns faltantes

- `QDRANT_API_KEY` (formato a confirmar — geralmente UUID/JWT)
- `RAILWAY_API_TOKEN`
- `TELEGRAM_BOT_TOKEN` (`^\d{8,10}:[A-Za-z0-9_-]{35}$`)
- Service account Google (`"private_key": "-----BEGIN PRIVATE KEY-----`)

### G.3 — Validação

Tentar Write/save_to_github com cada pattern → ambas camadas bloqueiam.

---

## H — Drive→GitHub: dois caminhos (R8) — PENDENTE DECISÃO

Discussão adiada pra sessão futura conforme combinado em conversa de 27/04.

Opções:
- **H1.** Desativar Apps Script
- **H2.** Manter ambos com escopos disjuntos (Apps Script pra `Inbox/`, Action pra `dialogos/`)
- **H3.** Migrar Apps Script pra Action (unificar)

Ver [[06-perguntas-abertas]] pra detalhes.

---

## I — Atualizar docs mestre (R5) — POR ÚLTIMO

⚠ **Só fazer DEPOIS de B, C, D estabilizados em produção por ≥48h.**

### I.1 — `CLAUDE.md`
- "3 tools" → "21 tools no bot, 14 endpoints na API, 10 tools nos MCPs"
- "Mem0 hosted" → "Qdrant Cloud self-hosted via Mem0 OSS"
- "Deploy pendente" → "Em produção"
- Adicionar `dialogos/`, `_indices/`, `_log/`, `api/`, `gus/integrations/`

### I.2 — `_estado-atual.md`
Reescrever com fatos pós-saneamento. Ou consolidar com `gus-26` (decidir se mantém os dois).

### I.3 — `gus-01-visao-geral.md`
- Corrigir "Mem0 hosted API"
- Tirar ou ajustar `parte: 1-de-7` (série tem 27 partes)

### I.4 — `gus-26-status-consolidado.md`
- Atualizar pós-migração (204 mems, curadoria Sonnet, etc.)

---

## Quadro-resumo

| Item | Risco | Esforço | Bloqueia? | Status |
|---|---|---|---|---|
| **A** | R4 | 30min | não | ✅ feita |
| **B** | R1 + demanda | 1-2h | F, I | 🟢 próxima |
| **C** | R2 | só decisão | D, E | ✅ decidida (C1) |
| **D** | R6 | 3-5h | E (idealmente), I | depois de B |
| **E** | R3 | 1h | F | depois de D ideal |
| **F** | R3 | 1-2h | I | depois de B+E |
| **G** | R7 | 1h | não | qualquer hora |
| **H** | R8 | varia | não | aguarda decisão |
| **I** | R5 | 2-3h | — | último, +48h após B+C+D |

**Mínimo viável pra dormir tranquilo:** A + B + E. **Mínimo pra arquitetura honesta:** + C + D. **Saneamento completo:** todos.

---

Próxima leitura: [[05-design-auto-merge]] · Voltar: [[03-inconsistencias-medias-baixas]]
