---
tipo: design-decision
area: gus
gus-id: 30.1
atualizado: 2026-05-01T15:45-03:00
status: decisões fechadas — pronto pra Fase 1
referencia: gus-30 (roadmap completo)
sessao-decisora: 2026-05-01 Claude Code (Gustavo + Gus engenharia)
---

# gus-30.1 — NeuroGus: decisões fechadas pro v0

> **Pra quem ler:** este doc atualiza o `gus-30-neurogus-roadmap.md`
> com as decisões tomadas em sessão de 2026-05-01. As §11.1–11.7
> (decisões abertas) do gus-30 ficam destravadas aqui. Onde houver
> conflito, **este doc vence**.

---

## 1. Decisões fechadas

| ID gus-30 | Decisão | Resolução |
|---|---|---|
| §11.1 | Top-K e threshold pra afinidade | **K=3, threshold=0.6 cosine.** Sweet spot da literatura, alinhado com default proposto. |
| §11.6 | Apagar fragmento: hard ou soft? | **Ambos.** Coexistem com semântica distinta (ver §3). |
| §11.7 | Coleção mostrada: só `gustavo` ou também `gus`? | **Ambos no v0.** O brain `gus` é essencial — auto-observações compõem identidade. |
| nova | Linha temporal: v0 ou v1.1? | **v0.** Inclui linha reta (default), espiral 3D e anel cíclico 24h. **Sem cometa** (decoração, abstrai topologia). |
| §12.3 | Endpoints SSE em `hub/routes.py` ou `api/routes.py`? | **`hub/routes.py`.** Confirmado em `api/server.py:54` que `app.include_router(hub_router)` está em produção. Reaproveita Bearer global e prefix `/hub`. |

### Pendentes ainda (não bloqueiam Fase 1 backend, decidir antes da Fase 2 frontend)

| ID gus-30 | Decisão | Quando decidir |
|---|---|---|
| §11.2 | Mock HTML do Drive Claude Chat — localizar ou recriar? | Antes de começar Fase 2 |
| §11.3 | Token na URL aceitável? | Antes de Fase 2 |
| §11.4 | Auto-orbit ON ou OFF default? | Antes de Fase 2 |
| §11.5 | Reconnect SSE — retoma ou reload? | Antes de Fase 2 |

---

## 2. Implicações UX (mudam vs gus-30 original)

### 2.1 Painel lateral ganha **2 botões de remoção**

```
┌─ Fragmento [uuid] ────────────────┐
│ tipo: decisao                     │
│ confiança: 0.78                   │
│ criado_em: 2026-04-29 14:32       │
│ ...                               │
│                                   │
│ [ Esquecer ]   [ Apagar de vez ]  │
│   (reversível)   (irreversível)   │
└───────────────────────────────────┘
```

- **Esquecer** (soft): marca `estado: "esquecido"` no payload. Nó vira fantasma translúcido (opacity 0.15) e some das buscas semânticas — mas continua no Qdrant pra retro-aprendizado.
- **Apagar de vez** (hard, vermelho): modal "isso é irreversível, confirma?" → `client.delete(point_id)`. Some completamente.

### 2.2 Brain `gus` distinguível visualmente

Pra não confundir com o tipo `identidade_operacional` (cor cyan no preenchimento), nós do brain `gus` ganham **anel orbital fino branco** ao redor (RingGeometry Three.js).

Filtro lateral ganha 2 toggles em vez de 1:
- "memórias do Gustavo" (ON default)
- "auto-observações do Gus" (ON default)

### 2.3 Linha temporal — 3 controles

Cluster recolhível no canto inferior esquerdo:

- **Toggle 1** — "ver linha temporal" (arestas cronológicas: 0% → 40% opacity)
- **Dropdown** — modo: `linha reta | espiral 3D | anel cíclico 24h`
- **Toggle 2** — "esticar" (override força X pra reorganizar nós no eixo temporal)

Sem cometa.

---

## 3. Semântica importante: "esquecido" não é "lixeira"

Decisão central desta versão:

> **"Esquecido" é substrato de retro-aprendizado, não lixo.**

Implicações que decorrem disso:

### 3.1 Buscas semânticas filtram `estado != "esquecido"` por default

Tools normais (`search_memory`, `lembrar`, `_calcular_vizinhos`) ignoram fragmentos esquecidos. **Eles não influenciam contexto do bot.**

### 3.2 Mas continuam acessíveis pra processos de aprendizado

Casos onde `estado="esquecido"` deve ser **incluído** explicitamente:

- **SELF-1** (reflexão quinzenal) — pode olhar o que foi esquecido pra entender padrões de erro/correção
- **Auditoria do Hub** — contar quantos esquecidos, distribuição por tipo
- **Curador retro** (futuro) — analisar pares (esquecido, correção) pra aprender o que detectar
- **NeuroGus** — toggle especial "ver esquecidos" mostra eles como fantasmas no grafo

### 3.3 Quando usar cada um

| Cenário | Ação |
|---|---|
| Memória poluída/errada (esperando correção futura) | **Esquecer** |
| Memória que vai virar contraste pra aprendizado | **Esquecer** |
| Memória trivial/duplicada sem valor histórico | **Apagar de vez** |
| Dado sensível salvo por engano (LGPD) | **Apagar de vez** |
| Nome trocado em prontuário Dimagem | **Apagar de vez** |

### 3.4 Coerência com Telegram

`deletar_memoria` no bot Telegram hoje é hard delete. **Vai ganhar comportamento dual:** parâmetro `modo: "esquecer"|"apagar"` (default `apagar` por compat). Atualização do bot fica em ticket separado, não bloqueia NeuroGus.

---

## 4. Implicações backend (Fase 1)

### 4.1 Schema gus-18 — sem mudança

O campo `estado: "ativo|estavel|historico|esquecido"` já existe. Soft delete usa o `"esquecido"` que sempre esteve previsto.

### 4.2 Filtro de buscas

Adicionar em `hub/store.py:lembrar()` e `_calcular_vizinhos()`:

```python
# pseudo
filtro = Filter(must_not=[FieldCondition(key="estado", match=MatchValue(value="esquecido"))])
```

Endpoints novos `/hub/recent` e `/hub/stream` aceitam **query param `incluir_esquecidos: bool = False`**. Pra frontend ativar o "ver esquecidos" depois.

### 4.3 Endpoints novos (delta sobre gus-30 §13.2)

| Endpoint | Verbo | Função |
|---|---|---|
| `/hub/recent` | GET | últimos N fragmentos (boot do grafo) |
| `/hub/stream` | GET | SSE com fragmentos novos |
| `/hub/fragmento/{id}` | DELETE | hard delete |
| `/hub/fragmento/{id}/esquecer` | PATCH | soft delete (marca `estado=esquecido`) |
| `/hub/fragmento/{id}/lembrar` | PATCH | reverte soft delete (`estado=ativo`) |

Bonus: o `lembrar` permite "des-esquecer" um fragmento direto pelo NeuroGus se mudar de ideia.

### 4.4 Stack final de mudanças backend

| Arquivo | Ação | LoC |
|---|---|---|
| `hub/events.py` | criar (broadcast + subscribe) | ~50 |
| `hub/store.py` | `_calcular_vizinhos()` + broadcast no `ingestar()` + filtro `estado != esquecido` em `lembrar`/vizinhos | ~30 |
| `hub/routes.py` | 5 endpoints novos | ~90 |

**Total Fase 1: ~170 linhas** (subiu ~25 vs gus-30 estimativa por causa dos 2 endpoints extras de soft delete).

---

## 5. Próximos passos imediatos

### Fase 1 — Backend SSE (sessão atual)

- [ ] Criar `hub/events.py` com `broadcast()` + `subscribe()` (asyncio.Queue por listener, `maxsize=100`)
- [ ] Em `hub/store.py`:
  - [ ] `_calcular_vizinhos(vetor, k=3, threshold=0.6, exclude_id, incluir_esquecidos=False)`
  - [ ] Hook `await broadcast(payload)` no fim de `ingestar()` via `asyncio.run_coroutine_threadsafe` (ingestar é sync hoje)
  - [ ] Atualizar `lembrar()` pra filtrar `estado != "esquecido"` por default
- [ ] Em `hub/routes.py`:
  - [ ] `GET /hub/recent?limit=N&user_id=X&incluir_esquecidos=False`
  - [ ] `GET /hub/stream?token=X` (SSE, auth via query param)
  - [ ] `DELETE /hub/fragmento/{id}` (hard)
  - [ ] `PATCH /hub/fragmento/{id}/esquecer` (soft)
  - [ ] `PATCH /hub/fragmento/{id}/lembrar` (reverte soft)
- [ ] Smoke test local com `curl --no-buffer`
- [ ] PR pra main

**Definição de pronto:** `curl /hub/stream` mantém conexão aberta indefinidamente, `POST /hub/ingestar` dispara evento que aparece no stream, e os 2 endpoints PATCH alteram `estado` corretamente.

### Fase 2 — Frontend produção (sessão futura)

Decidir §11.2–11.5 do gus-30, depois implementar:
- `api/neurogus.py` (HTML + SSE consumer)
- 3d-force-graph com nascimento animado
- Painel lateral com 2 botões de remoção
- Cluster temporal (toggle linha + dropdown modo + toggle esticar)
- Anel orbital pros nós do brain `gus`
- PWA manifest

---

## 6. Cross-references

- [[gus-30-neurogus-roadmap]] — roadmap completo (§11.1, 11.6, 11.7 destravadas aqui)
- [[gus-18-schema-indexacao]] — schema dos fragmentos (campo `estado` já existe)
- [[gus-31-maturacao-grafo]] *(futuro)* — decay automático de fragmentos esquecidos
- [[gus-22-etapas4-5-ego-autorelato]] — Ego Cache; ainda lê só ativos no v0
- [[gus-28-acesso-hub-claude-chat]] — Passo 3 será marcado completo após Fase 2

---

## Apêndice — Mudanças vs gus-30 original

| §gus-30 | Status | Onde virou |
|---|---|---|
| §11.1 K e threshold | ✅ fechada | §1 deste doc |
| §11.6 hard vs soft | ✅ fechada com twist (ambos) | §1 + §3 |
| §11.7 brains gus/gustavo | ✅ fechada (ambos) | §1 + §2.2 |
| §11.2 mock HTML | ⏳ pendente Fase 2 | — |
| §11.3 token URL | ⏳ pendente Fase 2 | — |
| §11.4 auto-orbit | ⏳ pendente Fase 2 | — |
| §11.5 reconnect SSE | ⏳ pendente Fase 2 | — |
| nova: linha temporal | ✅ v0 com 3 modos | §2.3 |
| nova: semântica esquecido | ✅ substrato aprendizado | §3 |
| §13.2 endpoints | ✅ subiu de 3 pra 5 | §4.3 |

LoC backend Fase 1 estimada: **145 → 170** (+25 pelos endpoints de soft delete).
