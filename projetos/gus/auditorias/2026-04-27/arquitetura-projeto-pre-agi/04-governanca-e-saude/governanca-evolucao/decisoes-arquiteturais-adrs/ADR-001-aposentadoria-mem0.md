---
tipo: adr
numero: 001
titulo: Aposentar Mem0 como camada permanente — adotar Qdrant direto
status: aceito
data: 2026-04-27
decididor: Gustavo (consulta com Claude Code)
relacionados: gus-15-decisao-migracao, gus-23-logica-qdrant-mem0, gus-18-schema-indexacao, R1, R2, R6
supersede: gus-23 (que propunha convivência indefinida)
---

# ADR-001 — Aposentar Mem0 como camada permanente

> **Architecture Decision Record** seguindo formato Michael Nygard.
> Voltar: [[../../../00-leia-primeiro/cruzamento-com-gus-real]]

---

## Status

**Aceito** em 2026-04-27 13:54 BRT.

Este ADR **supersede** parcialmente `projetos/gus/gus-23-logica-qdrant-mem0.md`, que propunha convivência indefinida entre coleção `gus` (via Mem0) e `gus_hub` (Qdrant direto). Decidimos que a convivência é **temporária** (durante migração), não permanente.

---

## Contexto

Hoje o sistema de memória do Gus tem **três caminhos para o mesmo Qdrant Cloud**, com problemas em cada um:

1. **`gus/memory.py`** — usa `Memory.from_config()` do `mem0ai` (self-hosted). Aponta pro Qdrant Cloud na coleção `gus`. Em produção pelo bot Telegram + API FastAPI desde 26/04/2026.

2. **`.claude/mcp/mem0_server.py`** — usa `MemoryClient(api_key=MEM0_API_KEY)` (Mem0 SaaS hosted). **Brain morto ou divergente** — escreve/lê de outro lugar. Risco R6.

3. **Vários scripts em `.github/scripts/`** (`auditoria_mem0.py`, `briefing_matinal.py`, `enrich_mem0_export.py`, `ingest_mem0_from_chat.py`, `retrospectiva_semanal.py`, `export_mem0.py`) — também usam `MemoryClient` SaaS. Auditorias e briefings podem estar lendo fonte desatualizada.

Bugs documentados:
- **R1** — Curador automático Haiku quebrado há 14h+ por incompatibilidade `mem0ai 0.1.29` × `qdrant-client 1.12+` (`temperature` + `top_p` em conjunção)
- **R2** — Split arquitetural Mem0 SaaS × Qdrant self-hosted; auditoria de hoje mostra 204 mems mas não dá pra confirmar de onde
- **R6** — MCP `mem0-gus` aponta pra Mem0 SaaS — pode estar acessando dados velhos ou inexistentes

E o esquema de fragmentos definido em `gus-18-schema-indexacao.md` (14 tipos, 4 estados, 5 camadas temporais, 5 tipos de esquecimento, lifecycle com `peso`/`confirmacoes`/`acessos`) **não cabe nativamente em Mem0** — Mem0 tem schema fixo e pequeno (`id`, `memory`, `metadata.via`).

A visão pre-AGI (`gus-24`) declara: *"modelo é descartável, memória é o centro"*. Logo, a infra de memória precisa ser **simples, sólida, sem camadas frágeis**.

---

## Decisão

**Aposentar Mem0 como camada permanente. Migrar para Qdrant direto, em 5 fases.**

Resultado final desejado:
- Uma única coleção viva no Qdrant Cloud: `gus_hub`, com schema rico do `gus-18`
- Código próprio (`hub/store.py`, `hub/curador.py`, `hub/ego_cache.py`, `hub/auto_relato.py`) escreve e lê direto
- Mem0 SaaS cancelado, `mem0ai` removido das dependências
- Coleção `gus` (legado) esvaziada e removida

---

## Alternativas consideradas

### Alternativa A — Migração total para Qdrant direto (escolhida)

- ✅ Schema rico (gus-18) realizável
- ✅ Sem camada intermediária frágil
- ✅ Filtros nativos por tipo/estado/área
- ✅ Resolve R1, R2, R6 de uma vez
- ❌ Curador customizado precisa ser escrito (gus-21)
- ❌ Mais código próprio para manter

### Alternativa B — Convivência indefinida (gus-23 original)

- ✅ Sem migração, sem breaking change
- ❌ Dois caminhos de leitura → dois lugares de drift
- ❌ Custo cognitivo: "qual coleção tem essa memória?"
- ❌ Mantém Mem0 como fonte de fragilidade
- ❌ Não realiza schema gus-18

### Alternativa C — Reverter para Mem0 SaaS puro

- ✅ Volta para o conhecido
- ❌ Quota free tier é insuficiente (motivo original da migração — gus-15)
- ❌ Mantém schema pobre, não cabe gus-18
- ❌ Joga fora a infra Qdrant Cloud já provisionada

---

## Consequências

### Positivas

- **Schema do Hub pre-AGI realizado em código.** Os 14 tipos + lifecycle + tipo_esquecimento `protegido` ganham efetividade.
- **Debug direto.** Sem caixa preta de extração — você vê o prompt do curador, o LLM, o custo.
- **Independência de versão.** `qdrant-client` é controlado por nós, sem depender da agenda de release de `mem0ai`.
- **Single source of truth.** Toda porta lê e escreve no mesmo `gus_hub`, com tag `via=<porta>`.
- **Custo previsível.** Curador Haiku custa ~$0.05/mês (estimativa gus-21). Mem0 já cobrava extração também — não há custo novo significativo.

### Negativas

- **Curador customizado precisa ser implementado** (`hub/curador.py` em gus-21). Hoje o Mem0 fazia automático. ~150 linhas de código.
- **Dedup precisa ser implementado.** Mem0 fazia automático via similaridade. Vai precisar de lógica própria (hash + similaridade Qdrant).
- **Migração de dados.** ~204 fragmentos da coleção `gus` precisam ser classificados (atribuir `tipo`, `area`, `camada_temporal`) e re-inseridos em `gus_hub`. Script único.
- **Re-implementar busca semântica de alto nível.** O `Memory.search()` retornava texto formatado; vai precisar de helper próprio.

### Neutras

- **MCP `mem0-gus` precisa migrar.** Substituir `MemoryClient` por chamadas a `hub/store.py`. Renomear pra `mcp/hub_server.py` faria sentido.

---

## Plano de migração — 5 fases

Cada fase é **incremental e reversível**. A Fase N só começa após a Fase N-1 estar validada por uso real.

### Fase 1 — Hub paralelo nasce (RISCO ZERO)

**Objetivo:** criar a infraestrutura Hub sem tocar em produção.

**Implementar:**
- `hub/__init__.py` (vazio)
- `hub/schemas.py` (Pydantic com `IngestarReq`, `LembrarReq` etc.)
- `hub/store.py` com:
  - `get_client()` — instancia `QdrantClient` apontando pro mesmo Qdrant Cloud
  - `_ensure_collection()` — cria `gus_hub` se não existe (vetores 384 dim, distance cosine)
  - `_filtros(user_id, tipo, estado, area)` — helper de Filter
  - `ingestar(conteudo, metadata)` — embedding via fastembed/HF, upsert com payload completo do gus-18
  - `lembrar(query, ...)` — query com filtros opcionais
  - `ego_cache(user_id)` — scroll dos tipos relevantes
  - `contar(user_id)` — count com filtro
- `hub/routes.py` — FastAPI router em `/hub/*`:
  - `POST /hub/ingestar`
  - `POST /hub/lembrar`
  - `GET /hub/ego-cache`
  - `GET /hub/auto-relato`
  - `GET /hub/stats`
- `api/server.py`: registrar `from hub.routes import router as hub_router; app.include_router(hub_router)`

**Quem faz:** Claude Code (esta porta). ~3-4h código.

**Quem ativa:** Gustavo confirma deploy + testa endpoints com curl/Postman.

**Validação:**
- `POST /hub/ingestar` com fragmento teste → retorna ID, fragmento aparece no Qdrant Cloud dashboard na coleção `gus_hub`
- `POST /hub/lembrar` com query similar → retorna o fragmento
- `GET /hub/stats` → retorna `total_fragmentos: 1`

**Risco:** zero. Mem0 e bot continuam intactos. Hub é aditivo.

---

### Fase 2 — Curador alimenta Hub em paralelo

**Objetivo:** começar a popular `gus_hub` automaticamente, sem desligar o resumo Mem0.

**Implementar:**
- `hub/curador.py`:
  - `curar(user_msg, assistant_msg, via, user_id)` — chama Haiku com prompt PROMPT_CURADOR (template em gus-21), recebe JSON com fragmentos classificados, valida, chama `ingestar()` pra cada um
  - Validação: descarta fragmento sem `conteudo`, força `tipo` em allowlist (com fallback `episodico`)
  - Try/except generoso: nunca quebra o bot
- `gus/bot.py`: adicionar fire-and-forget após cada resposta:
  ```python
  asyncio.create_task(_curar_interacao(user_text, resposta))
  ```
  com função auxiliar `_curar_interacao` em `bot.py`

**Aproveitamento:** o R1 (curador Mem0 quebrado) não precisa ser corrigido — o Curador novo substitui. Mas o resumo extrativo Mem0 continua tentando rodar (e falhando) por 14 dias até decidir desligar.

**Quem faz:** Claude Code. ~2-3h código.

**Validação (14 dias de coleta dual):**
- Após 14 dias, `gus_hub` deve ter 50-100 fragmentos curados
- Distribuição de tipos esperada: `biografico`, `preferencia`, `decisao`, `episodico`, `meta_reflexao`
- Comparar manualmente: 5 fragmentos do `gus_hub` vs 5 memórias do Mem0 do mesmo período. Qual está mais útil?

**Risco:** baixo. Curador roda em background, não bloqueia resposta. Custo: ~$0.05/mês extra.

---

### Fase 3 — Bot lê do Hub primeiro (validação operacional)

**Objetivo:** mudar a fonte de leitura do bot Telegram pra `gus_hub`, mantendo Mem0 como fallback.

**Implementar:**
- `gus/memory.py:buscar_memorias` refatorada:
  - Tenta `hub.store.lembrar(query)` primeiro
  - Se vazio (ou erro), fallback pra `Memory.search()` antigo
  - Log da decisão (`hub_hit`, `mem0_fallback`)
- Métrica adicionada ao `/custo`: `hub_hit_ratio`

**Quem faz:** Claude Code. ~1h.

**Validação (14 dias):**
- Hub respondendo bem → `hub_hit_ratio` cresce naturalmente conforme `gus_hub` enriquece
- Conversas do bot continuam fazendo sentido (Gustavo monitora subjetivamente)

**Risco:** baixo. Fallback existe. Pior caso: volta pro comportamento antigo.

---

### Fase 4 — Migração de dados `gus` → `gus_hub`

**Objetivo:** transferir os ~204 fragmentos da coleção `gus` (Mem0) pra `gus_hub` com schema rico.

**Implementar:**
- `.github/scripts/migrar_gus_para_hub.py`:
  - Lê todos fragmentos da coleção `gus` (paginado)
  - Pra cada um: chama Haiku com prompt de classificação (atribui `tipo`, `area`, `camada_temporal` baseado no texto + metadata)
  - Insere no `gus_hub` via `hub.store.ingestar()`
  - Loga: total migrado, total descartado (lixo), distribuição de tipos atribuídos
- Workflow `.github/workflows/migrar-gus-para-hub.yml` (manual, `workflow_dispatch`)

**Quem faz:** Claude Code escreve. Gustavo dispara o workflow uma vez.

**Validação:**
- `gus_hub` cresce de ~50-100 (curador) para ~250-300 (curador + migração)
- Auditoria seguinte (06h) mostra distribuição rica por tipo
- Bot busca memória antiga ("o que eu disse sobre Cleir?") e encontra → migração funcionou

**Risco:** médio. Erros de classificação podem distorcer distribuição. Mitigação: dry-run primeiro (--mode dry-run mostra classificação sem inserir).

---

### Fase 5 — Aposentadoria do Mem0 (FECHAMENTO)

**Objetivo:** remover Mem0 do sistema. Single source of truth = Qdrant + Hub.

**Implementar:**
1. **`gus/memory.py`** — apagar fallback Mem0. `buscar_memorias` agora chama só `hub.store.lembrar`.
2. **`.claude/mcp/mem0_server.py`** — renomear pra `.claude/mcp/hub_server.py`. Trocar `MemoryClient` por `hub.store`. Atualizar header doc.
3. **Scripts em `.github/scripts/`** — migrar um por um (ordem do plano D do saneamento):
   - `enrich_mem0_export.py` (mais isolado)
   - `auditoria_mem0.py` (cron diário)
   - `export_mem0.py` (decidir: migra ou arquiva?)
   - `briefing_matinal.py`
   - `retrospectiva_semanal.py`
   - `ingest_mem0_from_chat.py`
4. **Arquivar one-shots** legacy: `migrate_mem0.py`, `reset_qdrant_collection.py` + workflows correspondentes em `.github/{scripts,workflows}/_legado/`
5. **Esvaziar coleção `gus`** no Qdrant (só após confirmar Hub funcionando)
6. **Remover `mem0ai` do `requirements.txt`**
7. **Remover `MEM0_API_KEY` dos secrets do GitHub**
8. **Remover `MEM0_API_KEY` do `~/.claude/gus.env` e `.mcp.json`**
9. **Cancelar conta Mem0 SaaS** no painel mem0.ai (Gustavo executa)

**Atualizar docs:**
- `gus-15-decisao-migracao.md` → status: `executado`
- `gus-23-logica-qdrant-mem0.md` → marcar como **superseded por ADR-001**
- `CLAUDE.md` → atualizar arquitetura ("Mem0 hosted" → "Qdrant direto via Hub")

**Quem faz:** Claude Code escreve mudanças. Gustavo cancela conta SaaS.

**Validação final:**
- `grep -r "MemoryClient\|mem0ai\|from mem0 import" . | grep -v _legado/` → **zero hits**
- Bot, API, MCP, todos os 14 workflows funcionam consultando só `gus_hub`
- Auditoria diária regenera com mesmos números (consistente)
- Custo Mem0 SaaS = $0 (cancelado)

**Risco:** baixo se Fases 1-4 validadas. Cada componente migrado tem rollback (mantém branch antes de mergear).

---

## Cronograma estimado

| Fase | Tempo Claude Code | Tempo Gustavo | Observação ativa |
|---|---|---|---|
| **1** Hub paralelo | 3-4h | 30min validar | dia 1 |
| **2** Curador paralelo | 2-3h | passivo | 14 dias |
| **3** Bot lê Hub primeiro | 1h | passivo | 14 dias |
| **4** Migração de dados | 2h escrever + dispatch | 10min disparar | dia único |
| **5** Aposentadoria final | 4-6h | 30min cancelar SaaS | dia único após Fases 1-4 estáveis |

**Total ativo:** ~12-16h código + ~1h ações Gustavo. **Tempo calendário:** ~30-45 dias com observação real.

---

## Critério de sucesso global

> *"O que Gustavo falou no Telegram às 14h aparece no auto-relato do Claude Code às 16h."* (gus-24)

Após Fase 5:
- Toda escrita no Telegram, Custom GPT, Claude Chat alimenta `gus_hub`
- Toda porta lê de `gus_hub`
- Schema gus-18 está vivo em produção
- Sistema independente de Mem0

Esse é o critério que valida o ADR.

---

## Reabertura

Este ADR seria reaberto se:
- Qdrant Cloud descontinuar free tier sem aviso suficiente
- Aparecer alternativa significativamente mais barata/simples (ex: Postgres + pgvector com extensão LLM nativa)
- Volume crescer a ponto do Hub manual virar gargalo (>1M fragmentos — hoje estamos com 204)

---

## Referências

- `projetos/gus/gus-15-decisao-migracao.md` — decisão original Mem0 Cloud → self-hosted
- `projetos/gus/gus-18-schema-indexacao.md` — schema do Hub
- `projetos/gus/gus-19-etapa1-mem0-selfhost.md` — Fase 1 da migração original (já feita)
- `projetos/gus/gus-20-etapa2-hub-qdrant.md` — desenho do Hub direto (= Fase 1 deste ADR)
- `projetos/gus/gus-21-etapa3-curador.md` — desenho do Curador (= Fase 2 deste ADR)
- `projetos/gus/gus-22-etapas4-5-ego-autorelato.md` — Ego Cache + Auto-relato (= continuação pós-ADR)
- `projetos/gus/gus-23-logica-qdrant-mem0.md` — **superseded** por este ADR
- `projetos/gus/gus-24-hub-pre-agi-visao.md` — visão arquitetural completa
- `projetos/gus/gus-25-roadmap-ativacao.md` — fases pós-infra
- Auditoria-mãe: [[../../../00-leia-primeiro]]
- Cruzamento: [[../../../00-leia-primeiro/cruzamento-com-gus-real]]

---

_Aprovado por Gustavo em 2026-04-27 13:54 BRT, registrado pelo Claude Code (esta porta) na sessão de fiscalização._
