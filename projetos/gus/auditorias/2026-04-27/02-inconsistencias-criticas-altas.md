---
tipo: auditoria-fiscal
parte: 02-de-06
ordem_leitura: 3
gerado_em: 2026-04-27T09:55:00-03:00
gerado_por: claude-code
escopo: origin/main @ 2026-04-27 manhã
status: rascunho-fiscal
---

# Inconsistências críticas e altas (R1–R8)

Voltar: [[00-leia-primeiro]] · Anterior: [[01-mapa-funcional]] · Próximo: [[03-inconsistencias-medias-baixas]]

---

## 🔴 CRÍTICO

### R1. Curadoria automática do Mem0 está QUEBRADA há ~13h

Em `_log/resumos-mem0/`:

- **26/04** às 18:47, 19:21, 23:47, 23:52: 4 erros 400
- **27/04** às 06:06, 06:14, 06:21, 07:04, 07:54: **5 erros consecutivos hoje** (último ~minutos antes desta auditoria)

Erro: `Error code: 400 — '\`temperature\` and \`top_p\` cannot be used together'` (provável — log corta a mensagem).

**Significado:** a cada 3 turnos do Telegram, o Haiku está falhando ao gerar o resumo extrativo. Conversas desde 26/04 noite **não estão entrando no Mem0 via esse caminho**.

→ Bate exatamente com a demanda urgente em `inbox-claude-code/2026-04-27T06-16__curadoria-mem0-sonnet-nao-haiku.md`. Gustavo já notou e quer trocar Haiku por Sonnet. Mas o último erro é depois da demanda → **ainda não foi corrigido**.

**Plano de correção:** etapa B do [[04-plano-saneamento]] (híbrida com assinatura — ambos Haiku e Sonnet rodam paralelo, cada um assina sua memória, comparação posterior).

---

### R2. Split arquitetural Mem0 SaaS vs Qdrant self-hosted

Migração ocorreu 26/04 (commits `991e452`, `b9d8f89`, `9ff9c96`). Mas:

| Componente | Aponta pra |
|---|---|
| `gus/memory.py` (bot + API) | ✅ Qdrant self-hosted |
| `.claude/mcp/mem0_server.py` (porta Claude Code) | ❌ MemoryClient SaaS |
| `.github/scripts/export_mem0.py` | ❌ MemoryClient SaaS |
| `briefing_matinal.py`, `auditoria_mem0.py`, `retrospectiva_semanal.py`, `enrich_mem0_export.py`, `ingest_mem0_from_chat.py` | ❓ todos importam `mem0`, precisam audit individual |

→ A auditoria de hoje (`_indices/_auditoria-mem0.md`, 204 memórias) pode estar lendo do **Mem0 SaaS antigo** enquanto o bot grava no **Qdrant**. Auditoria, briefing e exports podem estar olhando uma fonte que não é mais a fonte de verdade.

**Plano:** etapas C+D do [[04-plano-saneamento]] (decisão Qdrant único + migração arquivo a arquivo). Gustavo já decidiu C1 — Qdrant é destino único.

---

### R3. Vazamento LGPD: pacientes Dimagem aparecem no Mem0 do Gustavo

A auditoria detectou 1 par de duplicatas suspeitas — e ambas são **nomes reais de pacientes**:

- *"Isabela Barros de Souza has a cranial MRI at Assim São Gonçalo with fasting confirmed +8h"*
- *"Theo Silva Alvarenga has a cranial MRI at Assim São Gonçalo with fasting confirmed at 8am"*

Isso fere o design declarado em `gus-04-seguranca-protecao` e os endpoints da API (`PATHS_BLOQUEADOS = ("dimagem/",)`). Pacientes deveriam ficar **só** em `dimagem/dia/AAAA-MM-DD.md`, **nunca** no Mem0. O resumo extrativo a cada 3 turnos (quando funcionava) não filtrou conversas sobre OS Dimagem antes de salvar.

→ Risco real: se Custom GPT chamar `search_memory` com query qualquer que dê match semântico, pode retornar nome de paciente. Idem outras portas.

**Plano:** etapas E (quarentena urgente) + F (política preventiva no curador) do [[04-plano-saneamento]].

---

### R4. 3 demandas em `inbox-claude-code/` paradas + 1 falsamente "pendente"

| Arquivo | Status real | Status no frontmatter |
|---|---|---|
| `2026-04-26T23-51__fix-qdrant-search-bug.md` | resolvido (3 commits) | ~~pendente~~ → **concluido** (etapa A já feita, commit `98e8125`) |
| `2026-04-27T06-16__curadoria-mem0-sonnet-nao-haiku.md` | pendente (R1 ainda quebrando) | pendente |
| `2026-04-27T06-16__schema-hub-qdrant-salvar-memoria.md` | pendente (Etapa 3 do Hub não implementada) | pendente |

→ Existe `2026-04-27T00-30__fix-qdrant-search-bug-concluido.md` em `inbox-tiogu/` confirmando o fix, mas ninguém atualizou o frontmatter da demanda original → archive workflow nunca move → fica eternamente pendente.

**Causa raiz:** padrão a evitar — destino tem que atualizar `status` e `processado_em` ao terminar, senão `archive-completed-demandas.yml` nunca move.

---

## 🟠 ALTO

### R5. Documentação canônica tem múltiplas verdades conflitantes

| Doc | Estado | Inconsistência |
|---|---|---|
| `gus-01-visao-geral.md` (atualizado 23/04) | "Mem0 (hosted API) — memória relacional" | Contradiz arquitetura atual (Qdrant self-hosted) |
| `gus-15..gus-26` (criados 26/04) | "Qdrant self-hosted + Mem0 self-hosted" | OK, mas conflita com gus-01 |
| `_estado-atual.md` (atualizado 25/04 23:55) | cita "164 memórias", "quota Mem0 37%" | **Antes** da migração e do crescimento pra 204 |
| `gus-26-status-consolidado.md` (atualizado 26/04 01:15) | cita 164 memórias, fala da migração como "decidida" mas não como "executada" | Defasado em 1 dia |
| `CLAUDE.md` (atualizado 25/04) | "3 tools", "7 módulos Python", "Deploy pendente" | **3 níveis de gerações atrás** da realidade (21 tools, mais módulos, em produção) |
| `gus-01..07` | rótulo `parte: 1-de-7` | Série hoje tem 27 partes, não 7 |

→ Sessão nova de Claude Code lê `_estado-atual.md` primeiro (instrução do hook) e parte de fatos obsoletos.

**Plano:** etapa I do [[04-plano-saneamento]] — **última** a executar, só DEPOIS de B+C+D estabilizados. Atualizar antes é escrever em cima do drift.

---

### R6. MCP `mem0-gus` precisa de chave que talvez não exista mais

Spec em `.claude/mcp/mem0_server.py`:
```python
from mem0 import MemoryClient
api_key = os.environ.get("MEM0_API_KEY")  # m0-...
```

O Mem0 SaaS pode estar abandonado pós-migração. Mensagem em `_estado-atual.md`: *"MCP daqui é cego"*.

- Se a chave foi cancelada: esta porta perde acesso a memória completamente
- Se ainda está ativa: escreve pra brain morto (memórias salvas daqui não chegam ao Qdrant)

Nenhum dos dois cenários é o desejado. **Esta auditoria não confirmou qual dos dois é o estado atual** — só vi código.

**Plano:** etapa D.2 do [[04-plano-saneamento]] (migrar MCP `mem0-gus` pra usar `build_qdrant_memory()` de `gus/memory.py`).

---

### R7. Hook `scan_sensivel.py` duplica patterns de `gus/tools.py`

`_PATTERNS_SENSIVEIS` está em **dois arquivos**:

- `gus/tools.py` (validação dentro do bot, antes de `save_to_github`)
- `.claude/hooks/scan_sensivel.py` (PreToolUse no Claude Code, antes de Write/Edit)

Adicionar nova chave (ex: `QDRANT_API_KEY`, Railway PAT, Telegram bot token, Google service account) exige editar nos dois — risco de drift silencioso.

Hoje o hook **não detecta**:
- `QDRANT_API_KEY` (não tem regex)
- `RAILWAY_API_TOKEN`
- `TELEGRAM_BOT_TOKEN` (formato `^\d{8,10}:[A-Za-z0-9_-]{35}$`)
- Service account Google (chave: `-----BEGIN PRIVATE KEY-----`)

**Plano:** etapa G do [[04-plano-saneamento]] — extrair pra módulo único `gus/patterns_sensiveis.py` + adicionar patterns faltantes.

---

### R8. Dois caminhos Drive→GitHub coexistem

- **Apps Script** `drive_inbox_to_github.gs` (cron 5min, externo) — modo legado pra `Gus-Sync/Inbox/`
- **GitHub Action** `import_from_drive.py` (cron 15min) — modo novo pra `Gus-Sync/dialogos/`

Não vi indicação clara de qual está ativo nem se há overlap. Se ambos rodam, podem competir por arquivos.

**Plano:** etapa H do [[04-plano-saneamento]] — investigar primeiro (você precisa confirmar o que tá deployado no Apps Script), depois decidir entre desativar / manter disjunto / unificar.

---

## Ordem de prioridade pra atacar

1. **R1** (B do plano) — bug ativo, dados sendo perdidos agora
2. **R3** (E + F) — LGPD não espera
3. **R2 + R6** (C + D) — alinhar arquitetura, corrigir confusão
4. **R4** — fechar demandas paradas (R4 da fix-qdrant já está com correção em `98e8125`)
5. **R7** — fortalecer scan
6. **R8** — investigar e decidir
7. **R5** (I) — atualizar docs **por último** (só depois de B+C+D estabilizados ≥48h)

---

Próxima leitura: [[03-inconsistencias-medias-baixas]] · Voltar: [[01-mapa-funcional]]
