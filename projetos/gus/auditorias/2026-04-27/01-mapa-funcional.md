---
tipo: auditoria-fiscal
parte: 01-de-06
ordem_leitura: 2
gerado_em: 2026-04-27T09:55:00-03:00
gerado_por: claude-code
escopo: origin/main @ 2026-04-27 manhã
status: rascunho-fiscal
---

# Mapa funcional do sistema Gus

Voltar ao [[00-leia-primeiro]].

---

## 1. Identidade e propósito

**Gus é um agente pessoal multi-portal** do Gustavo. Não é um chatbot — é uma entidade única com memória persistente compartilhada, identidade canônica em `dialogos/_bootstrap/gus-identity.md`, e quatro **princípios invioláveis**:

1. Não alucinar
2. Buscar antes de afirmar (fato externo)
3. Citar fonte quando buscou
4. Verificar antes de afirmar ausência

Princípios estão duplicados consistentemente em `gus/system_prompt.md`, `gus/meta-memoria.md`, `dialogos/_bootstrap/gus-identity.md` e `CLAUDE.md` — boa engenharia de prompt.

---

## 2. Portas (canais de acesso)

| Porta | Status | Stack | Onde mora o código |
|---|---|---|---|
| **Telegram (TioGu)** | ✅ produção | python-telegram-bot polling, Sonnet 4.6 (Haiku 4.5 fallback) | `gus/main.py` + `gus/bot.py` |
| **Custom GPT API** | 🟡 produção, aguarda Builder | FastAPI + Bearer auth | `api/server.py` + `api/routes.py` |
| **Claude Chat** | ✅ produção via bootstrap manual | Drive integration nativa | só o bootstrap em `dialogos/_bootstrap/gus-bootstrap.md` |
| **Claude Code (esta porta)** | 🟡 funciona, MCPs dependem de `~/.claude/gus.env` | 2 MCP servers | `.claude/mcp/gus_server.py`, `.claude/mcp/mem0_server.py` |
| **Custom GPT mobile (voz)** | ⏳ planejado | mesma API + GPT Builder | bloqueado em "Configure Action no desktop" |
| **Alexa Skill** | ⏳ planejado | Lambda/Railway + Polly | só docs (`gus-10`, `gus-26`) |
| **S8 wake-word "Gus"** | ⏳ planejado | Termux + openWakeWord | só docs |

---

## 3. Camadas compartilhadas (o que faz "ser o mesmo Gus")

| Camada | Onde | Como cada porta acessa |
|---|---|---|
| **Memória relacional** | Qdrant Cloud (collection `gus`, dim 384), 2 brains: `user_id=gustavo` e `user_id=gus` | Bot/API: `gus/memory.py` (Mem0 self-hosted + HuggingFace embedder + Anthropic Sonnet pra extração); MCP `mem0-gus`: ⚠ ainda usa MemoryClient SaaS — ver R6 |
| **Conhecimento .md** | repo `Gustpbbr/Gus` (191 arquivos, 45 pastas) | `read/list/save_to_github` em todas as portas |
| **Espelho .md** | Google Drive `Gus-Sync/` | sync uma-via via `sync-to-drive.yml`; **bidirecional dentro de `dialogos/`** via `import-from-drive.yml` |
| **Identidade canônica** | `dialogos/_bootstrap/{gus-identity.md, gus-bootstrap.md}` | toda porta lê on-demand |
| **Demandas entre portas** | `dialogos/inbox-<porta>/` + frontmatter padrão | qualquer porta cria; destino lê e marca `status: concluido`; archive automático em ≤15min |

---

## 4. Fluxos principais (como uma mensagem viaja)

### 4.1 Mensagem texto no Telegram → resposta

```
Gustavo manda → handle_message (bot.py)
  → autorização (TELEGRAM_CHAT_ID), rate limit (20/min), hard limit ($30/mês)
  → interceptação dimagem (se houver pending: confirmação "sim"/"não")
  → buscar_memorias (Qdrant, query = últimas 3 msgs do user)
  → gerar_resposta (llm.py: loop até 10 rounds de tool use, Sonnet 4.6 + cache ephemeral)
  → tools chamadas (qualquer das 21) executadas em executar_tool
  → resposta texto → reply_text (split em 4096 chars)
  → a cada 3 turnos: gerar_resumo_turnos (Haiku) → salvar_memorias → log _log/resumos-mem0/
  → registrar (logger JSONL custos)
  → _save_state (/app/data/bot_state.json no volume Railway)
```

### 4.2 Foto OS Dimagem (fluxo dedicado)

```
handle_photo → analisar_os_dimagem (Haiku detecta cabeçalho OS)
  → se OS: dimagem_pending[chat_id] = preview, mensagem com lista atual + nova
  → próxima msg "sim" → salvar_os_dimagem (append em dimagem/dia/AAAA-MM-DD.md, dedup por nome)
  → "não" / outro assunto → expira pending
  → se NÃO for OS: cai no fluxo normal Sonnet com vision
```

### 4.3 Custom GPT (mobile) → API

```
GPT Builder Action → POST /endpoint (Bearer CUSTOM_GPT_TOKEN)
  → verify_bearer (auth.py)
  → reuso da função interna (_save_to_github, buscar_memorias_detalhada, etc.)
  → bloqueio path "dimagem/" (LGPD, 403 nesta porta)
  → tag via=custom-gpt em todas escritas Mem0/GitHub
  → response TextResp{result: "..."}
```

### 4.4 Demanda entre portas (canal `dialogos/`)

```
Origem cria arquivo .md no Drive em Gus-Sync/dialogos/inbox-<destino>/
  → (cron 15min) import-from-drive.yml puxa pro GitHub
    → valida frontmatter (tipo:demanda, origem≠destino, etc)
    → válido: commita em dialogos/inbox-<destino>/, move arquivo no Drive pra processados/
    → inválido: deixa no Drive, loga erro
    → se inbox-tiogu: notifica Telegram (se TELEGRAM_CHAT_ID secret)
  → destino lê, processa, atualiza frontmatter (status:concluido + Resultado no corpo)
  → (cron 15min) archive-completed-demandas.yml move pra dialogos/archive/
    → trash arquivo Drive, append em dialogos/historico/AAAA-MM.md
```

⚠ Limitação atual: **Claude Code Web (esta porta) escreve em branch, não em main**. As outras portas escrevem direto em main. Discussão e proposta de auto-merge em [[05-design-auto-merge]].

---

## 5. Tools — catálogo

### 5.1 Bot Telegram — 21 tools (em `gus/tools.py`)

| Categoria | Tools |
|---|---|
| GitHub | `read_from_github` · `list_github_directory` · `list_branches` · `list_commits` · `save_to_github` |
| Mem0 | `search_memory` · `meta_memoria` · `auditoria_mem0` · `salvar_memoria_gus` · `buscar_memoria_gus` · `deletar_memoria` |
| Web/Pesquisa | `search_web` (Tavily+DDG) · `pesquisar_pubmed` · `pesquisar_arxiv` · `perguntar_gpt` (GPT-5/mini/nano) |
| Operação | `criar_acao` · `disparar_workflow` · `logs_railway` · `auto_diagnostico` · `sugerir_wikilinks` |
| Implícito | processamento de imagem/PDF/Word/Excel/áudio Whisper |

### 5.2 Custom GPT API — 14 endpoints (em `api/routes.py`)

Subset das tools do bot, mais 4 atalhos (`/meta_memoria`, `/auditoria_mem0`, `/graph-data`, `/health-data`) e 2 ocultos do OpenAPI (`/analise_camera`, `/ver_ultima_captura`) prontos pra ativar quando câmera S8 entrar.

### 5.3 Claude Code — 2 MCPs

| MCP | Tools | Backend |
|---|---|---|
| `gus` | `auto_diagnostico`, `sugerir_wikilinks`, `perguntar_gpt` | reusa código `gus/integrations/*` |
| `mem0-gus` | `buscar/salvar/listar memorias` (×2 brains) + `deletar_memoria` | ⚠ MemoryClient SaaS (não Qdrant) — ver [[02-inconsistencias-criticas-altas#R6]] |

---

## 6. Automação

### 14 workflows GitHub Actions

**Crons ativos (BRT):**

| Workflow | Cron | Função |
|---|---|---|
| `import-from-drive.yml` | a cada 15min | Drive→GitHub (com notificação Telegram em inbox-tiogu) |
| `archive-completed-demandas.yml` | a cada 15min | Move concluído → archive, trash Drive, append histórico mensal |
| `ingest-mem0-from-chat.yml` | a cada 30min | Lê inbox-mem0-from-chat/, filtra Haiku, salva no Mem0 |
| `export-mem0.yml` | 03:00 diário | Snapshot Mem0 → .md/.json |
| `auditoria-mem0.yml` | 06:00 diário | Stats Mem0 → `_indices/_auditoria-mem0.md` |
| `briefing-matinal.yml` | 07:00 dias úteis | Briefing diário, Telegram |
| `check-saude.yml` | 07:30 diário | `auto_diagnostico`, alerta só se warn/error |
| `retrospectiva-semanal.yml` | sex 20:00 | Retrospectiva |
| `reflexao-quinzenal.yml` | sáb 10:00 (semanas pares) | SELF-1 (Nosis+Thymos+Síntese) |
| `sync-to-drive.yml` | push em main | GitHub→Drive (incremental) |

**Manuais (workflow_dispatch):** `sync-to-drive-full`, `delete-drive-file`, `migrate-mem0-to-qdrant` (one-shot já rodou), `fix-qdrant-dims` (one-shot já rodou).

### 15 scripts em `.github/scripts/`

`archive_completed.py`, `auditoria_mem0.py`, `briefing_matinal.py`, `check_saude.py`, `delete_drive_file.py`, `drive_inbox_to_github.gs` (Apps Script externo!), `enrich_mem0_export.py`, `export_mem0.py`, `import_from_drive.py`, `ingest_mem0_from_chat.py`, `migrate_mem0.py`, `reflexao_quinzenal.py`, `reset_qdrant_collection.py`, `retrospectiva_semanal.py`, `sync_to_drive.py`.

### 2 hooks Claude Code (`.claude/settings.json`)

- `SessionStart` → `session-start.sh` (instala mem0ai/mcp via pip --user no Claude Code Web)
- `PreToolUse Write|Edit|NotebookEdit` → `scan_sensivel.py` (bloqueia CPF/CNPJ/keys fora de `sensivel/`)

---

## 7. Conhecimento estruturado

**27 docs em `projetos/gus/`** (gus-01 a gus-26 + `_estado-atual.md`):

- **gus-01..07**: doc canônica original "1-de-7" (visão, implementado, config, segurança, portas, autonomia, descartadas)
- **gus-08..14**: extensões (plano, guia, Alexa, tools-roadmap, portas-futuras, tags-canônicas, custom-gpt-setup)
- **gus-15..26 (criados em massa em 26/04)**: roadmap "Hub pre-AGI" (decisão, schema, 5 etapas, lógica de convivência, visão, ativação, status consolidado)

**Índices vivos em `_indices/`:** `00-master.md` + dashboards por área (saude, financeiro, projetos, dimagem, receitas, capturado) + `_auditoria-mem0.md` (regenerado pelo cron).

---

## 8. Estado de produção (snapshot 27/04 manhã)

| Métrica | Valor |
|---|---|
| Mem0 — total memórias brain `gustavo` | **204** (auditoria 07:51 BRT) |
| Mem0 — frescor | 84% nos últimos 7d, 12% nas últimas 24h |
| Mem0 — densidade enviesada | 55% capturado, 29% projetos, 15% dimagem, 5% saúde |
| Bot Telegram | ✅ rodando, state em `/app/data/bot_state.json` |
| API FastAPI | ✅ `/health` 200 OK em `https://gus-production-58a7.up.railway.app` |
| Sync Drive bidirecional | ✅ ativo (15min) |
| Curadoria automática Haiku | ❌ **quebrada há ~13h** (R1) |
| Demandas pendentes em `inbox-claude-code/` | 3 (uma já resolvida, falta fechar — etapa A do plano, commit `98e8125` na branch `claude/greeting-checkin-NAcVz`) |

---

Próxima leitura: [[02-inconsistencias-criticas-altas]] · Voltar: [[00-leia-primeiro]]
