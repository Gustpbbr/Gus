---
tipo: cruzamento-fiscal
parte: cruzamento-com-gus-real
gerado_em: 2026-04-27T14:01:00-03:00
gerado_por: claude-code
escopo: origin/main snapshot 2026-04-27 manhã/tarde
status: rascunho-fiscal
---

# Cruzamento — Mapa canônico × estado real do Gus

> Aplica os 10 blocos funcionais + 8 transversais do mapa pre-AGI ao estado real do repositório `Gustpbbr/Gus` em `origin/main`. Pra cada subcomponente: status, onde está hoje, lacuna.

Voltar: `../README.md` (estrutura geral) · Auditoria-mãe: `../../00-leia-primeiro.md`

---

## Legenda

| Símbolo | Significado |
|---|---|
| ✅ | Existe e funciona |
| 🟡 | Existe mas parcial / desatualizado / problemas |
| 📦 | Existe mas em local errado / duplicado |
| ⏳ | Planejado em doc, não implementado |
| ❌ | Não existe nem em doc |

---

## Branches checadas

- **Referência:** `origin/main` (estado oficial em produção)
- **Branch desta sessão:** `claude/greeting-checkin-NAcVz` (3 commits ahead — A do plano + auditoria + esqueleto)
- **Outras branches `claude/*` com trabalho não-mergeado** (achado novo a registrar):
  - `research-tools-capabilities-PmKIo` — 114 commits
  - `initial-setup-t7xP7` — 81 commits
  - `initial-setup-iWTfL` — 80 commits
  - `portuguese-greeting-ZBMFU` — 8 commits
  - `review-project-structure-esL3J` — 1 commit
  - 3 outras com 0 commits ahead

→ Reforça [[../05-design-auto-merge|R11/auto-merge]]: trabalho órfão de sessões antigas espalhado.

---

## 🟦 BLOCO 1 — Conteúdo do usuário

### 1.A Domínio pessoal

| Subcomponente | Status | Onde está hoje | Observação |
|---|---|---|---|
| `pessoal/` (raiz) | ✅ | `pessoal/` | guarda-chuva. Nome confunde com "área `pessoal` do gus-18" |
| `pessoal/saude/` + `historico-saude.md` | ❌ | — | declarado em `system_prompt.md`, `gus-09`. **Reflexão SELF-1 W17 já apontou** |
| `pessoal/financeiro/overview.md` | 🟡 | existe | rascunho com gaps a preencher |
| `pessoal/financeiro/resumo-financeiro.md` | ❌ | — | declarado mestre, **não criado lá** |
| `resumo-financeiro.md` (raiz) | 📦 | raiz do repo | arquivo **vazio** (0 bytes), localização errada |
| `pessoal/diario/` | ✅ | `semana-2026-W17.md` | retrospectiva auto-gerada |
| `agenda/` | 🟡 | 8 stubs mensais | provável placeholder |
| `receitas/` | ✅ | `doces/` + `salgadas/` | 2 receitas reais |
| `capturado/links/`, `ideias/`, `misc/` | ❌ | — | declarados em `gus-09`, **nenhum existe** |
| `capturado/visual/` | ✅ | `_ultimo.md` | placeholder pro projeto câmera S8 |
| `acoes/pendentes/`, `acoes/concluidas/` | 🟡 | só `.gitkeep` | estrutura existe, executor não |
| `acoes/lembretes-ativos.md` | ✅ | existe | sem cron consumindo ainda |
| `sensivel/` | ✅ | `README.md` + `identidade/teste-cpf.md` | em produção, vazio real |
| `esportes/treinos/`, `evolucao.md` | ❌ | — | **declarado, NUNCA criado** |
| `leituras/livros/`, `papers/` | ❌ | — | declarado em `gus-01` |
| `contatos/mapa.md` | ❌ | — | declarado em `gus-06` |
| `casa/` | ❌ | — | obra Paty do Alferes começa em maio sem registro |
| `familia/` | ❌ | — | proposta nova do Gustavo |

**Síntese 1.A:** das 18 áreas previstas, **9 não existem** (50%). A proposta `gustavo/` resolve naming mas precisa criar várias subpastas.

### 1.B Domínio profissional Dimagem

| Subcomponente | Status | Onde está | Observação |
|---|---|---|---|
| `dimagem/dia/` (operacional/contábil) | ✅ | 2 arquivos | **schema inconsistente** entre os 2 |
| `dimagem/convenios.json` | ✅ | raiz da pasta | bom modelo de canonical mapping |
| `dimagem/casos/` (clínico/didático) | ❌ | — | declarado, nunca populado |
| `dimagem/protocolos/` | ❌ | — | declarado, vazio |
| `dimagem/admin/` | ❌ | — | declarado, vazio |
| `dimagem/fechamento/`, `ordens-servico/` | ❌ (correto) | — | já foram limpas em 25/04 |

---

## 🟩 BLOCO 2 — Identidade e Memória

### 2.1 Identidade canônica

| Subcomponente | Status | Onde está | Observação |
|---|---|---|---|
| `dialogos/_bootstrap/gus-identity.md` | ✅ | 2493 bytes | identidade compartilhada — fonte de verdade |
| `dialogos/_bootstrap/gus-bootstrap.md` | ✅ | 12641 bytes | ativador Claude Chat |
| `gus/gus-identity.md` | 🟡 | 320 bytes (placeholder "MOVIDO") | redirect file |
| `gus/gus-bootstrap.md` | 🟡 | 587 bytes (placeholder "MOVIDO") | redirect file |
| `gus/system_prompt.md` | 🟡 | 42100 bytes (~700 linhas) | **monolítico**, só Telegram. Diretriz `gus-12` ("system prompt em camadas") nunca implementada |
| `gus/meta-memoria.md` | ✅ | 10721 bytes | autobiografia narrativa |
| `principios.md` (separado, referenciável) | ❌ | — | princípios **duplicados** em 3 arquivos hoje |
| `portas/<X>.md` (system prompt por porta) | ⏳ | espalhado em CLAUDE.md, gus-bootstrap, Instructions V2 | a estruturar |

### 2.2 Memória persistente

| Subcomponente | Status | Onde está | Observação |
|---|---|---|---|
| `gus/memory.py` (Mem0 self-hosted → Qdrant) | 🟡 | bot Telegram + API | **a aposentar** (ADR-001) |
| `.claude/mcp/mem0_server.py` | 📦 | aponta pra Mem0 SaaS | **brain morto** — R6 |
| `.claude/mcp/gus_server.py` | ✅ | 3 tools (auto_diag, wikilinks, gpt) | OK |
| `hub/store.py` | ⏳ | — | **a implementar (gus-20)** |
| `hub/curador.py` | ⏳ | — | a implementar (gus-21) — bate com demanda pendente |
| `hub/ego_cache.py` | ⏳ | — | a implementar (gus-22) |
| `hub/auto_relato.py` | ⏳ | — | a implementar (gus-22) |
| Coleção Qdrant `gus` (Mem0) | 🟡 | ~204 mems | a esvaziar/migrar pra `gus_hub` |
| Coleção Qdrant `gus_hub` (Hub direto) | ❌ | — | a criar |
| `_indices/_auditoria-mem0.md` | ✅ | regenera 06h | OK, mas script lê de Mem0 |
| `gus-memoria-export.{md,json}` | ✅ | raiz | OK, mesmo caveat |
| `_log/resumos-mem0/` | 🟡 | logs diários | mostra **R1 ativo**: erros 400 |
| Retro Engine (auto-observação fim de sessão) | ❌ | — | gus-25 Fase 5, futuro |

---

## 🟨 BLOCO 3 — Interface e Operação

### 3.1 Portas (canais I/O)

| Porta | Status | Onde está | Observação |
|---|---|---|---|
| Telegram (TioGu) | ✅ | `gus/main.py` + `bot.py` | em produção, 21 tools |
| Custom GPT API | ✅ | `api/server.py` + `routes.py` | API rodando, **aguarda Builder** |
| Claude Chat (via bootstrap) | ✅ | bootstrap em `dialogos/_bootstrap/` | funcional |
| Claude Code (esta porta) | 🟡 | 2 MCPs em `.claude/mcp/` | depende de `~/.claude/gus.env` |
| Custom GPT mobile (voz) | ⏳ | — | bloqueado em "configurar Action no desktop" |
| Alexa Skill | ❌ | — | só docs (`gus-10`) |
| S8 wake-word | ❌ | — | só docs |
| Plugin de carro | ❌ | — | só citação em `gus-12` |

### 3.2 Capacidades / tools

| Subcomponente | Status | Onde está | Observação |
|---|---|---|---|
| Catálogo declarativo | ✅ | `gus/tools.py` (TOOLS list) | 21 tools |
| Dispatcher | ✅ | `gus/tools.py:executar_tool` | OK |
| Categorias de tools | 🟡 | implícitas no código | `gus-11` lista 8 categorias |
| Validação de path | ✅ | `_SAFE_PATH_RE` | OK |
| Scan PII | 🟡 | duplicado em 2 lugares | R7 |
| Bloqueio LGPD `dimagem/` | ✅ | `api/routes.py` | bloqueado na API |
| Rate limit | ✅ | `bot.py` (20/min) | OK |
| Hard limit USD | ✅ | `bot.py` ($30/mês) | OK |
| Trust scores | ❌ | — | gus-25 Fase 3 |

### 3.3 Canal de comunicação interna (`dialogos/`)

| Subcomponente | Status | Onde está | Observação |
|---|---|---|---|
| `inbox-tiogu/` | 🟡 | 5 arquivos pendentes | acumula respostas (R10) |
| `inbox-claude-code/` | 🟡 | 3 demandas; 1 fix-qdrant em fechamento | R4 |
| `inbox-claude-chat/` | ✅ | 2 arquivos | OK |
| `inbox-custom-gpt/` | ✅ (vazia) | só `_README.md` | esperado |
| `archive/` | ✅ | 5 demandas concluídas | OK |
| `historico/2026-04.md` | ✅ | 1 entrada | nascente, OK |
| `streams/` (legado) | 🟡 | 2 arquivos | hook do Claude Code Web ainda aponta pra streams |
| `processados-erro/` | ✅ (vazia) | só `_README.md` | OK |
| `_bootstrap/` | ✅ | identity + bootstrap | OK |
| `Demandas Gustavo /` | 🟡 | pasta com espaço/maiúscula | mantida (decisão Gustavo) |
| `inbox-mem0-from-chat/` | ❌ | declarado em gus-bootstrap | **não existe** apesar de promised by `ingest-mem0-from-chat.yml` |
| Frontmatter padronizado (doc) | ✅ | `dialogos/README.md` | OK |
| Workflow `import-from-drive` | ✅ | cron 15min | OK |
| Workflow `archive-completed-demandas` | ✅ | cron 15min | OK |

---

## 🟥 BLOCO 4 — Governança e Saúde

### 4.1 Automação / ciclos vitais

| Ciclo | Componente | Status | Cron |
|---|---|---|---|
| **Turno** | resumo extrativo a cada 3 turnos | 🟡 quebrado há 14h+ (R1) | a cada 3 msgs |
| **15min** | import Drive→GitHub | ✅ | */15 |
| **15min** | archive demandas concluídas | ✅ | */15 |
| **30min** | ingest Mem0 from Chat | 🟡 | */30 — script aponta pra Mem0 SaaS |
| **Diário 03h** | export Mem0 | ✅ | OK |
| **Diário 06h** | auditoria Mem0 | ✅ | OK |
| **Diário 07h** | briefing matinal (dias úteis) | ✅ | OK |
| **Diário 07:30** | check de saúde | ✅ | OK |
| **Semanal sex 20h** | retrospectiva | ✅ | OK |
| **Quinzenal sáb 10h** | reflexão SELF-1 | 🟡 | rodou só 1× |
| **Profundo (>30d)** | arqueologia | ❌ | gus-24, futuro |
| **One-shot legacy** | `migrate-mem0-to-qdrant` | 📦 | já rodou, arquivar |
| **One-shot legacy** | `fix-qdrant-dims` | 📦 | já rodou, arquivar |

### 4.2 Observabilidade

| Subcomponente | Status | Onde está | Observação |
|---|---|---|---|
| Logs estruturados (JSONL) | ✅ | `gus/logger.py` → `logs/gus_metrics.jsonl` | path `logs/` **vs** `_log/` (inconsistência) |
| `_log/resumos-mem0/` | ✅ | log auditável de curadoria | mostra R1 ativo |
| Métricas (cache, custo, latência) | ✅ | `gus/logger.py` + `/custo` | OK |
| Auditoria automática Mem0 | ✅ | `_indices/_auditoria-mem0.md` | regenera diário |
| Health checks | ✅ | `auto_diagnostico` + `check-saude.yml` | OK |
| Dashboard humano-legível | 🟡 | `api/dashboard.py` (642 linhas) | PROJETO FUTURO, não exposto no OpenAPI |
| Alertas | ✅ | check-saude → Telegram | OK |
| `_indices/<area>.md` | ✅ | 6 dashboards MOC + master | várias seed-stage |

### 4.3 Governança e evolução

| Subcomponente | Status | Onde está | Observação |
|---|---|---|---|
| ADRs | 🟡 | `gus-15`, `gus-23` | dispersos como `gus-XX`, sem categoria própria |
| Decisões descartadas | 🟡 | `gus-07-decisoes-descartadas.md` | conteúdo **contradiz `gus-15`** (R5) |
| Roadmap vivo | 🟡 | `gus-25` + `gus-26` | 2 roadmaps com numerações inconsistentes |
| Reflexão periódica (SELF-1) | 🟡 | `reflexoes/2026-W17-reflexao.md` | rodou 1× |
| Trust scores | ❌ | — | gus-25 Fase 3 |
| Handoff entre sessões | 🟡 | `_estado-atual.md` | desatualizado em 2 dias (R5) |
| Doc canônica do projeto | 🟡 | 26 arquivos `gus-XX` | **2 modelos coexistem** (gus-01..14 antigo, gus-15..26 novo) |

---

## 🟪 TRANSVERSAIS T1–T8

| # | Transversal | Status | Onde está | Observação |
|---|---|---|---|---|
| **T1** | Configs e segredos | 🟡 | `.env.example`, `.gitignore`, `.mcp.json`, `get_token.py` | **`get_token.py` foi commitado** (deveria estar gitignored) |
| **T2** | Deploy e runtime | ✅ | `Dockerfile`, `railway.toml`, `requirements.txt` | OK |
| **T3** | Sync com Drive | 🟡 | 3 workflows + 3 scripts | **2 caminhos coexistem** (Apps Script + Action) — R8 |
| **T4** | Versionamento e history | 🟡 | git nativo + 9 branches `claude/*` | **6 branches com trabalho não-mergeado** |
| **T5** | Segurança em profundidade | 🟡 | `scan_sensivel.py` + `tools.py` | patterns duplicados, faltam keys (R7) |
| **T6** | Documentação humana | 🟡 | `CLAUDE.md` + 7 docs em `docs/` | CLAUDE.md desatualizado (R5); `docs/*` mistura vivo (drive-setup) com obsoleto (briefing-opus, entrevista) |
| **T7** | Custos e quotas | 🟡 | `gus/logger.py` + `/custo` | tracking existe, **path `logs/` ≠ `_log/`**; sem alerta de quota Qdrant |
| **T8** | Teste e staging | ❌ | só `scripts/test_railway_logs.py` | **sem `tests/`, sem ambiente staging** |
| (extra) | Obsidian config | ✅ | `.obsidian/` | versionado |
| (extra) | `README.md` raiz | ❌ | — | **não existe** README pra novato |

---

## Síntese final — números

| Camada | ✅ OK | 🟡 parcial | 📦 lugar errado | ⏳ planejado | ❌ falta |
|---|---|---|---|---|---|
| **A — Conteúdo** | 11 | 4 | 1 | — | 12 |
| **B — Identidade/Memória** | 8 | 6 | 1 | 6 | 1 |
| **C — Interface/Operação** | 18 | 4 | — | 4 | 4 |
| **D — Governança/Saúde** | 11 | 8 | 2 | 4 | 2 |
| **Transversais T1–T8** | 1 | 6 | — | — | 1 |
| **TOTAL** | **49** | **28** | **4** | **14** | **20** |

Lendo:
- **49 elementos OK** → infra forte
- **28 parciais** → maior categoria; sintoma "muito desenhado, pouco executado"
- **20 ausências reais** → 12 só em conteúdo do usuário (saúde, esportes, leituras, contatos, casa, família — confirma diagnóstico SELF-1 W17)
- **14 planejados não implementados** → quase todos do Hub pre-AGI (5 do Hub) + portas e capacidades futuras

---

## Top 5 ações de migração que essa tabela aponta

1. **Implementar `hub/`** (5 arquivos novos) → resolve B.2 + ADR-001
2. **Migrar scripts SaaS pra Qdrant direto** (5 scripts em `.github/scripts/`) → resolve R2/R6
3. **Aposentar `gus/memory.py` (camada Mem0)** + atualizar MCP → fechamento da decisão
4. **Criar pastas faltantes do conteúdo do usuário** (`pessoal/saude/`, `esportes/`, `leituras/`, `contatos/`, `casa/`, `familia/`) com READMEs explicando regra
5. **Refatorar identidade em camadas** (`base.md` + `principios.md` + `portas/<X>.md`) → resolve diretriz `gus-12` nunca implementada

---

## Próximas etapas

- **ADR-001** (Aposentadoria Mem0) registrado em `../04-governanca-e-saude/governanca-evolucao/decisoes-arquiteturais-adrs/ADR-001-aposentadoria-mem0.md`
- **Implementação do Hub** detalhada em ADR-001 §"Plano de migração"

Voltar: [[../00-leia-primeiro]] · ADR-001: [[../04-governanca-e-saude/governanca-evolucao/decisoes-arquiteturais-adrs/ADR-001-aposentadoria-mem0]]
