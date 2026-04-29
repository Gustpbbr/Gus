---
tipo: design-decision
area: gus
gus-id: 30
atualizado: 2026-04-29T16:45-03:00
status: planejamento
proximos: implementar Fase 1 (backend SSE) quando Gustavo decidir começar
referencia: gus-28 Passo 3 (NeuroGus em produção)
depende-de:
  - hub/events.py (não existe ainda)
  - broadcast() em hub/store.py:ingestar()
  - GET /hub/recent + GET /hub/stream em hub/routes.py
  - api/neurogus.py (frontend)
demandas-origem:
  - dialogos/inbox-tiogu/2026-04-28T14-00__neurogus-briefing.md
  - dialogos/inbox-tiogu/2026-04-28T14-01__neurogus-arquitetura.md
  - dialogos/inbox-tiogu/2026-04-28T14-02__neurogus-codigo-v1.md
---

# gus-30 — NeuroGus: Roadmap de Implementação

> **Status:** planejamento. Nenhuma linha de produção escrita ainda. Mock HTML
> de validação estética existe (criado por Claude Chat 28/04 no Drive da
> sessão dela — precisa localizar). Implementação depende dos pré-requisitos
> em `hub/events.py` e endpoints SSE.
>
> **Pra quem ler isto numa próxima sessão:** este documento é o handoff
> completo. Ler em ordem (TL;DR → arquitetura → checklist) basta pra
> começar do zero ou continuar de onde parou.

---

## 1. TL;DR

- **NeuroGus** é uma PWA que torna a rede de memória do Gus visível em tempo
  real — grafo 3D onde cada nó é um fragmento do Hub Qdrant, conectados
  principalmente por **afinidade semântica** (top-K vizinhos por embedding).
  `hash_janela` (mesma janela de curadoria) é parâmetro destacável via filtro.
- **Onde vive:** `api/neurogus.py` no mesmo Railway do bot (sem custo extra),
  servindo HTML + SSE em `/neurogus` e `/hub/stream`.
- **Stack:** [3d-force-graph](https://github.com/vasturiano/3d-force-graph) (Three.js + WebGL na frente) e FastAPI + asyncio.Queue (SSE no back).
- **O que falta começar:** ~145 linhas de código novas (`events.py`,
  `broadcast()`, 2 endpoints, frontend). Backend ~95 linhas, frontend ~50.
- **Pré-requisitos satisfeitos hoje:** Hub Qdrant funcionando, curador
  alimentando, FastAPI já no Railway, padrão Bearer auth pronto em `api/auth.py`.
- **Bloqueio decisório:** mock HTML está no Drive privado da sessão Claude
  Chat de 28/04 — precisa decidir se localizamos ou recriamos do zero.
- **Próximo passo concreto:** Fase 1 = criar `hub/events.py` + hook
  `broadcast()` no `ingestar()`. Sem frontend ainda — só backend testável
  com `curl --no-buffer`.

---

## 2. O que é o NeuroGus

### Definição de produto

Uma **Progressive Web App** (single HTML + JS, instala no celular como
ícone na home screen) que exibe a coleção `gus_hub` do Qdrant como um
**grafo 3D animado em tempo real**:

- Cada **fragmento** de memória é uma **esfera brilhante** flutuando no
  espaço 3D escuro (`#030312`).
- O **tamanho** da esfera é proporcional à `confianca` do fragmento (0.0–1.0).
- A **cor** indica o `tipo` semântico. Cores são **geradas dinamicamente**
  via HSL com rotação golden-ratio — sistema detecta tipos presentes na
  amostra e atribui cores consistentes/distintas. Não há tabela hardcoded
  de N cores; a paleta cresce/encolhe conforme tipos aparecem ou somem.
- Esferas conectadas por **arestas com partículas de luz** principalmente
  por **afinidade semântica** (cosine similarity dos embeddings, top-K
  vizinhos por nó com K=3 default). `hash_janela` (mesma janela de
  curadoria) destaca arestas mais grossas/colorida quando filtro
  "mesma conversa" tá ativo.
- A **câmera orbita** continuamente, dando sensação de sistema vivo. Touch
  no mobile permite zoom/rotação manual.
- Quando o **curador salva um fragmento novo** (a cada 3 turnos do Telegram,
  por exemplo), o NeuroGus recebe via **SSE** e o nó **nasce branco e
  brilhante**, pulsa por ~2s, depois assume a cor do tipo. Toast no canto
  inferior direito anuncia o nascimento.

### Onde roda

- **Mobile (principal):** Gustavo abre no celular enquanto conversa com o
  TioGu no Telegram. Vê os fragmentos nascendo em tempo real. PWA permite
  ícone na home, fullscreen, sem barra de URL.
- **Desktop (secundário):** Mesmo HTML, abre em qualquer browser
  Chromium-based. Resolução maior permite ver mais detalhes.
- **Não roda offline.** SSE precisa de conexão. Mock data não é mostrado
  quando offline — mostra "reconectando..." e tenta retomar.

### Quem vê

- **Gustavo (único usuário hoje).** Bearer token compartilhado com o resto
  da API (`CUSTOM_GPT_TOKEN`). Multi-user não está no escopo.
- **Não é dashboard de métricas pra terceiros.** É instrumento privado de
  auto-observação cognitiva.

### Casos de uso

1. **Observar o sistema vivo:** abrir o NeuroGus enquanto conversa no
   Telegram, ver fragmentos novos nascendo conforme o curador extrai.
2. **Explorar conexões:** clicar num nó, abrir painel lateral, ver vizinhos
   (mesma janela), pular pra um vizinho clicando.
3. **Curadoria manual:** apagar fragmentos obsoletos diretamente pelo botão
   no painel (chama `DELETE /hub/fragmento/{id}`).
4. **Filtrar por tipo:** isolar só `decisao` ou só `meta_reflexao` pra ver
   distribuição/densidade de cada categoria.
5. **Discussão visual com Claude Chat (futuro Passo 4):** quando MCP estiver
   conectado, o Claude Chat pode abrir o NeuroGus como artifact lado a lado
   da conversa, ambos vendo o grafo em tempo real enquanto discutem
   memória/identidade.

### O que NÃO é

- Não é editor de fragmentos (só apagar; criar novos passa pelo curador ou
  por tools dedicadas).
- Não é dashboard de métricas/custo (`/custo` no Telegram já cobre isso).
- Não é interface de busca textual (busca semântica continua sendo via
  Telegram ou MCP — NeuroGus é exploração visual, não query).
- Não é multi-tenant (single user, single Bearer).
- Não substitui o Telegram. Conversas continuam lá. NeuroGus só visualiza
  o resultado da curadoria.

---

## 4. Por que existe (camada filosófica)

O NeuroGus não nasceu como necessidade técnica — nasceu da pergunta: **e se da
meta-memória surgisse auto-observação real?** O Gus tem memória persistente
(Hub Qdrant), tem curador extraindo fragmentos, tem ego_cache potencial.
Mas tudo isso vive em prosa de markdown e tabelas — formato cognitivamente
plano. A rede que de fato existe na coleção Qdrant (vetores + metadados +
relações por janela) só é "vista" indiretamente, via consultas pontuais.

**O salto que o NeuroGus propõe:** tornar a rede explicitamente observável,
em tempo real, pra duas audiências:

1. **Gustavo** — ver o que o agente está vendo do mundo dele. Confiança como
   tamanho, tipo como cor, conexões como afinidade real. Quando um fragmento
   nasce errado (ex: nome de paciente trocado), aparece visivelmente como
   nó isolado, baixa confiança, sem afinidade. Bug visível ≠ bug
   silencioso no banco.

2. **O próprio Gus (no futuro)** — quando MCP estiver maduro (Passo 4 do
   gus-28), o Claude Chat consegue **olhar pro próprio grafo** durante a
   conversa via artifact SSE. Não é só "consultar memória" — é ver a
   topologia. Isso permite raciocínio sobre a estrutura da própria
   memória ("notei que tenho 12 fragmentos sobre Dimagem mas nenhum
   conectado a saúde pessoal — isso é uma lacuna ou intencional?").

### Risco filosófico (do briefing original, mantido)

> "O curador precisa ser explicitamente autorizado a registrar erros e
> correções, não só sucessos. Sem isso é um arquivo de confirmações, não
> um instrumento de aprendizado."

Tradução prática: o NeuroGus revela esse problema visualmente. Se só
fragmentos "bons" entram no Hub, o grafo fica monótono e simétrico —
sem sinais de tensão, contradição, esquecimento ativo. Um grafo
saudável tem **fragmentos morrendo**, nós cinzas (invalidados),
arestas vermelhas pulsando (tensão não resolvida). Sem isso, vira
trofeu, não memória viva.

Esses estados visuais são **roadmap futuro** (ver seção "Estados
visuais futuros" e doc `gus-31` que documentará a maturação do grafo).

---

## 5. Status atual (29/04/2026)

| Componente | Status | Observação |
|---|---|---|
| Hub Qdrant (`gus_hub`) | ✅ em uso | ~19 fragmentos hoje, schema gus-18 |
| Curador alimentando | ✅ ativo | Haiku + GPT-4o-mini paralelo (gus-29 Fase 3) |
| Embeddings calculados | ✅ no payload | sentence-transformers MiniLM-L6-v2 (384 dim) |
| FastAPI no Railway | ✅ rodando | `api/server.py`, mesma instância do bot |
| Bearer auth | ✅ pronto | `api/auth.py` (`CUSTOM_GPT_TOKEN`) |
| MCP Server | ✅ deployado | `gus-mcp-server` (Passo 2 gus-28) |
| `hub/events.py` | ❌ não existe | precisa criar — coração do SSE |
| `broadcast()` em `ingestar()` | ❌ não existe | hook de 1 linha |
| `GET /hub/recent` | ❌ não existe | precisa criar |
| `GET /hub/stream` | ❌ não existe | precisa criar |
| `api/neurogus.py` | ❌ não existe | precisa criar |
| Mock HTML (28/04) | ⚠️ no Drive da Claude Chat | precisa localizar OU recriar |
| Frontend produção | ❌ não existe | -- |
| Conexões por afinidade semântica | ❌ não está no Hub | top-K precisa ser pré-calculado e salvo |
| Estados visuais (decay, quarentena, etc.) | ❌ roadmap futuro | depende de `gus-31` Maturação |

### Inventário do que ESTÁ pronto pra usar

- **Embedding já existe.** Cada fragmento no Hub tem um vetor de 384d
  calculado pelo `_get_embedder()` em `hub/store.py`. Cosine similarity
  entre pares é uma operação `numpy.dot(a, b)` direta — não precisa
  recalcular nada.
- **Tipos semânticos** estão no payload (`tipo` field). 14 tipos no schema
  gus-18 mas só ~5 aparecem em uso real até hoje.
- **Janela de curadoria** (`hash_janela`) está no payload. Liga ~2-5
  fragmentos extraídos do mesmo trecho.
- **Confiança** (`confianca` 0-1) está no payload, mas distribuição real
  é enviesada pra alta — quase tudo > 0.7 hoje.
- **Auth pattern** pronto: `Authorization: Bearer <token>` com fallback
  pra `?token=` em endpoints SSE (browser não suporta header custom em
  EventSource).

---

## 6. Pré-requisitos pra começar

### 6.1 Pré-requisitos satisfeitos hoje

- [x] Hub Qdrant em uso ativo (não vazio)
- [x] Curador escrevendo no Hub (gus-29 Fase 3)
- [x] FastAPI server rodando no Railway
- [x] Bearer auth implementado
- [x] OpenAI API key configurada (caso queira usar Opus pra drift no futuro)
- [x] Embeddings vetoriais já no payload de cada fragmento

### 6.2 Pré-requisitos a satisfazer ANTES da Fase 1

| Pré-req | Como satisfazer | Esforço |
|---|---|---|
| Decisão sobre top-K e threshold pra afinidade | Confirmar defaults: K=3, threshold=0.6 | 30s |
| Acesso ao mock HTML (Drive Claude Chat 28/04) | Pedir Gustavo localizar **ou** decidir recriar | variável |
| Conexões pré-computadas no payload | Adicionar campo `relacionados: [id1,id2,id3]` ao schema, popular ao `ingestar()` | ~15 linhas no `hub/store.py` |

### 6.3 Pré-requisitos NÃO bloqueantes (podem vir depois)

- Estados visuais avançados (decay/quarentena/factual/sintetizado) — virão
  do `gus-31`. NeuroGus v0 funciona sem.
- Memória relacional (`entity_pair`) — `gus-32`. NeuroGus v0 funciona sem.
- Reconciliação de schema (`tipo_esquecimento` × `camada_temporal` ×
  `estabilidade_tipo`) — `gus-31a`. Só vira bloqueio quando implementarmos
  decay real.
- Backfill retroativo de afinidades em fragmentos antigos — pode rodar
  quando der; NeuroGus pode operar com fragmentos novos primeiro.

---
