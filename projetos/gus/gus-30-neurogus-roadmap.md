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

## 7. Arquitetura técnica

### 7.1 Stack escolhido

**Frontend:** [`3d-force-graph`](https://github.com/vasturiano/3d-force-graph)
da família vasturiano. Construído sobre Three.js. Física de forças na CPU,
renderização WebGL. API de alto nível: passa `{ nodes, links }` e
configura.

Suporta nativamente:
- Partículas direcionais nas arestas (feixes de luz com velocidade
  configurável via `linkDirectionalParticles`)
- OrbitControls (zoom/pan/rotate por touch)
- Click no nó com callback (`.onNodeClick`)
- Custom 3D objects por nó (`.nodeThreeObject`)
- HTML labels acopladas a coordenadas 3D (`.nodeLabel`)

**Limitações conhecidas:**
- Performance degrada > ~5.000 nós (simulação de forças na CPU). Pra
  janela ativa do NeuroGus (~50–500 fragmentos), irrelevante.
- Não tem post-processing de bloom nativo — `MeshPhongMaterial` +
  `emissive` + `AdditiveBlending` resolve sem shader custom.

**Backend:** FastAPI já existente em `api/server.py`. Adicionar:
- `hub/events.py` (asyncio.Queue global)
- `broadcast()` em `hub/store.py:ingestar()` (1 linha)
- 2 endpoints novos em `hub/routes.py` (`/hub/recent`, `/hub/stream`)
- 1 endpoint novo em `api/server.py` (`/neurogus`, serve HTML)

### 7.2 Stack rejeitado (com motivo)

**Cosmograph (cosmos.gl)** — engine 100% GPU via shaders WebGL.
Suporta centenas de milhares de nós em real-time. **Rejeitado** porque:
- Não tem 3D nativo (é grafo 2D)
- Não tem partículas direcionais nas arestas (perde a metáfora "feixes
  de luz")

**Reservado pra futuro:** quando coleção crescer pra ~10k+ fragmentos
ativos e a janela 3D não der conta, criar segunda view "mapa completo
2D" com Cosmograph. Botão alterna entre as duas vistas.

**WebSocket bidirecional** — rejeitado em favor de SSE porque:
- NeuroGus só consome eventos (não emite). SSE é unidirecional e
  nativo no browser via `EventSource`.
- WebSocket exigiria framework adicional (`websockets`/`fastapi.WebSocket`)
  e tratamento de reconnect manual.
- SSE tem reconnect automático com `Last-Event-ID` header, suportado
  pelo browser sem código.

### 7.3 Onde vive

**Mesmo container do bot/API no Railway.** Sem service novo, sem custo
extra, sem secrets duplicados.

```
Railway Project: Gus
├── Service: tiogu-bot (já existe)
│   └── gus/main.py roda bot Telegram + FastAPI no mesmo processo
│       (asyncio.gather)
│       └── api/server.py expõe:
│           ├── /health  (público)
│           ├── /hub/*   (Bearer auth, JSON API — já existe)
│           ├── /neurogus       (NOVO, HTML inline)
│           ├── /hub/recent     (NOVO, JSON)
│           └── /hub/stream     (NOVO, SSE)
└── Service: gus-mcp-server (já existe — Passo 2)
    └── hub/mcp_server.py
        Não precisa mexer aqui pro NeuroGus.
```

### 7.4 Fluxo end-to-end

```
Gustavo escreve no Telegram
        │
        ▼
   gus/bot.py recebe mensagem
        │
        ▼
   curador (a cada 3 turnos, fire-and-forget)
        │
        ▼
   Haiku + GPT-4o-mini extraem fragmentos
        │
        ▼
   hub/store.py:ingestar(fragmento, metadata)
        │   ┌────────────────────────────────┐
        │   │ 1. salva no Qdrant gus_hub     │
        │   │ 2. calcula top-K vizinhos       │
        │   │    (cosine similarity > 0.6)    │
        │   │ 3. atualiza payload com         │
        │   │    relacionados: [id1, id2, id3]│
        │   │ 4. await broadcast(fragmento)   │  ← NOVO
        │   └────────────────────────────────┘
        │
        ▼
   hub/events.py: enfileira em asyncio.Queue global
        │
        ▼
   GET /hub/stream (SSE) consome a fila
        │
        ▼
   Browser (EventSource) recebe `data: {...}\n\n`
        │
        ▼
   neurogus.html: novo nó nasce no grafo
                   pulsa branco 2s → assume cor do tipo
```

### 7.5 As 4 peças de implementação

#### Peça 1: `hub/events.py` (~50 linhas)

**Responsabilidade:** fila assíncrona global, broadcast pra múltiplos
listeners (caso outros clientes além do NeuroGus se conectem no futuro).

**Esqueleto:**

```python
# hub/events.py
import asyncio
import json
import logging
from typing import AsyncIterator

logger = logging.getLogger(__name__)

# Lista de filas (uma por listener conectado).
# Não é Queue compartilhada — cada listener tem a própria pra evitar
# que um listener lento atrase os outros.
_listeners: list[asyncio.Queue] = []


async def broadcast(fragmento: dict) -> None:
    """Empurra fragmento pra todos os listeners conectados.

    Não-bloqueante: se listener tem fila cheia (ex: cliente travado),
    descarta o evento pra ele em vez de bloquear o ingestar().
    """
    if not _listeners:
        return  # ninguém conectado, no-op

    payload = json.dumps(fragmento, ensure_ascii=False, default=str)
    descartados = 0
    for q in _listeners:
        try:
            q.put_nowait(payload)
        except asyncio.QueueFull:
            descartados += 1
    if descartados:
        logger.warning(f"broadcast: {descartados} listener(s) com fila cheia, evento descartado")


async def subscribe() -> AsyncIterator[str]:
    """Inscreve um novo listener. Yield events conforme chegam.

    Usado por `GET /hub/stream` no FastAPI:
        async def stream():
            async for evento in subscribe():
                yield f"data: {evento}\n\n"
    """
    q: asyncio.Queue = asyncio.Queue(maxsize=100)
    _listeners.append(q)
    try:
        while True:
            payload = await q.get()
            yield payload
    finally:
        _listeners.remove(q)
```

**Pontos de atenção:**
- Fila por listener (não compartilhada) evita head-of-line blocking
- `maxsize=100` por fila: se cliente trava, descarta após 100 eventos
  acumulados (sinal de cliente morto)
- `asyncio.Queue` é thread-safe dentro de um event loop, o que
  basta — bot+API rodam no mesmo loop

#### Peça 2: hook em `hub/store.py:ingestar()` (~5 linhas)

**Responsabilidade:** após salvar no Qdrant, disparar broadcast.

**Esqueleto da modificação:**

```python
# hub/store.py — adicionar import
from hub.events import broadcast as _broadcast

def ingestar(conteudo, metadata):
    # ... código existente que salva no Qdrant ...

    # NOVO: pré-calcular vizinhos top-K e adicionar ao payload
    vizinhos = _calcular_vizinhos(vetor, k=3, threshold=0.6, exclude_id=frag_id)
    payload["relacionados"] = vizinhos
    client.set_payload(  # update no Qdrant
        collection_name=COLLECTION,
        payload={"relacionados": vizinhos},
        points=[frag_id],
    )

    # NOVO: broadcast pro NeuroGus (fire-and-forget)
    asyncio.create_task(_broadcast({
        "id": frag_id,
        **payload,
    }))

    return frag_id
```

**Pontos de atenção:**
- `_calcular_vizinhos` é função nova — busca top-K mais próximos do
  vetor recém-salvo, exclui o próprio ID, retorna lista de IDs
- `asyncio.create_task` faz fire-and-forget. Se broadcast falhar, não
  derruba o ingestar
- `ingestar` é chamado de contexto sync (curador roda em
  `asyncio.to_thread`). Precisa adaptar pra async OU usar
  `asyncio.run_coroutine_threadsafe`. Decisão: rever ao implementar

#### Peça 3: 2 endpoints em `hub/routes.py` (~80 linhas)

**Endpoint A: `GET /hub/recent`**

Retorna últimos N fragmentos pra inicializar o grafo no boot do
frontend. Inclui `relacionados` pra montar arestas.

```python
@router.get("/recent", operation_id="hub_recent")
async def r_recent(
    limit: int = 100,
    user_id: str = "gustavo",
):
    """Retorna últimos `limit` fragmentos do user_id, ordenados por
    criado_em desc. Inclui `relacionados` pra montar arestas no grafo.
    """
    fragmentos = await asyncio.to_thread(listar, user_id=user_id, limit=limit)
    return {"fragmentos": fragmentos, "total": len(fragmentos)}
```

**Endpoint B: `GET /hub/stream`** (SSE)

```python
from fastapi.responses import StreamingResponse
from hub.events import subscribe

@router.get("/stream", include_in_schema=False)
async def r_stream(token: str):
    """SSE com fragmentos novos em tempo real.

    Auth via query param porque EventSource não suporta header custom.
    Token comparado contra CUSTOM_GPT_TOKEN (mesmo da Bearer auth).
    """
    expected = os.getenv("CUSTOM_GPT_TOKEN")
    if not expected or token != expected:
        raise HTTPException(status_code=401)

    async def event_stream():
        async for payload in subscribe():
            yield f"data: {payload}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

**Pontos de atenção:**
- Auth no SSE via `?token=` (browser não envia header custom em
  EventSource; única alternativa segura sem proxy)
- `include_in_schema=False` esconde do OpenAPI público (não vaza pro
  Custom GPT)
- StreamingResponse com `text/event-stream` é o padrão SSE
- Reconnect: SSE tem isso nativo via `Last-Event-ID` header. Se
  quisermos retomar de onde parou, precisamos enviar `id:` em cada
  evento (issue futura, não v0)

#### Peça 4: `api/neurogus.py` + frontend (~50 linhas Python + ~400 linhas HTML/JS)

```python
# api/neurogus.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
import os

router = APIRouter(prefix="/neurogus", tags=["neurogus"])

@router.get("", response_class=HTMLResponse, include_in_schema=False)
async def serve_neurogus(token: str):
    """Serve o HTML do NeuroGus. Token via query param pra simplificar
    o link compartilhado (PWA na home screen do celular).

    O HTML lê o token da própria URL e usa em `?token=` nas chamadas
    ao /hub/recent e /hub/stream.
    """
    expected = os.getenv("CUSTOM_GPT_TOKEN")
    if not expected or token != expected:
        raise HTTPException(status_code=401)

    return HTMLResponse(NEUROGUS_HTML)


NEUROGUS_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>NeuroGus</title>
  <link rel="manifest" href="/neurogus/manifest.json">
  <!-- ... -->
</head>
<body>
  <!-- 3d-force-graph + lógica em JS inline -->
</body>
</html>
"""
```

**Pontos de atenção:**
- HTML inline no Python = simples, sem precisar servir static files
- Manifest.json pra PWA: arquivo separado servido em `/neurogus/manifest.json`
- Token vem na URL: usuário acessa `https://api-gus.../neurogus?token=XXX`,
  JS extrai com `new URLSearchParams(location.search).get('token')`
- Token na URL = aparece em logs/history. Mitigação: rotação periódica
  do `CUSTOM_GPT_TOKEN` ou usar token específico de NeuroGus (ver
  riscos)

### 7.6 Auth — síntese

| Endpoint | Método auth | Razão |
|---|---|---|
| `GET /neurogus?token=X` | Query param | HTML servido direto, JS lê token da URL |
| `GET /hub/recent?token=X` | Query param | Chamado por JS do navegador |
| `GET /hub/stream?token=X` | Query param | EventSource não suporta header custom |
| `DELETE /hub/fragmento/{id}` | **Bearer** | Chamado via `fetch()` pelo JS, suporta header |
| Outros endpoints `/hub/*` | Bearer (já existe) | sem mudança |

Token compartilhado: `CUSTOM_GPT_TOKEN` (já em uso). Pra MVP basta.
Pra futuro, criar `NEUROGUS_TOKEN` separado permite revogar acesso ao
NeuroGus sem afetar Custom GPT.

---

## 8. Design visual

### 8.1 Tipografia

- **Syne 800** (Google Fonts) — logo, títulos, valores numéricos.
  Geométrica, forte, sem serifa. Carregada via `@import` no CSS.
- **Space Mono** (Google Fonts) — labels, metadados, UI chrome.
  Monospace técnico sem ser genérico (como JetBrains Mono ou IBM
  Plex Mono).

**Justificativa:** evita Inter/Roboto/Arial. NeuroGus é instrumento
pessoal com identidade própria — fonte default genérica destoa.

### 8.2 Atmosfera

- **Fundo:** `#030312` — preto puro com leve azul profundo. Cria
  sensação de espaço sideral sem virar navy. Testado: sólido em
  ambos OLED (escuro real) e LCD (sem banding).
- **Sem skybox / texturas de fundo.** O grafo é o único protagonista.

### 8.3 Cores dos nós (geração dinâmica)

Hardcoded de N cores não escala (já discutido). Implementação:

```javascript
// Algoritmo: HSL golden-ratio rotation
const GOLDEN_ANGLE = 137.508;  // graus
const corPorTipo = new Map();

function corDeTipo(tipo) {
  if (corPorTipo.has(tipo)) return corPorTipo.get(tipo);
  const idx = corPorTipo.size;
  const hue = (idx * GOLDEN_ANGLE) % 360;
  const cor = `hsl(${hue}, 70%, 60%)`;  // saturação/luminância fixas
  corPorTipo.set(tipo, cor);
  return cor;
}
```

**Propriedades:**
- Tipo recebe cor consistente (mesmo tipo → mesma cor sempre)
- Cores ficam visualmente bem distribuídas (golden ratio garante
  separação angular)
- Saturação 70% + luminância 60% = vivacidade suficiente sem cansar
- Adapta-se: se aparecer tipo 15, ele só pega a próxima cor da
  rotação, sem refatoração

**Legenda viva:** chips no canto superior direito mostram só os tipos
que existem no momento na coleção carregada. Aparece tipo novo →
chip nasce.

### 8.4 Glow + iluminação

```javascript
// Material por nó (em 3d-force-graph .nodeThreeObject)
new THREE.MeshPhongMaterial({
  color: corDoTipo,
  emissive: corDoTipo,
  emissiveIntensity: 0.5,
  transparent: true,
  opacity: 0.95,
});
```

Combinado com `AdditiveBlending` em uma esfera externa de halo
(maior, mais transparente), produz "glow" sem post-processing
shader. Funciona bem em mobile (sem Bloom Pass que é caro).

### 8.5 Animação de nascimento (corrigida)

Problema do desenho original: branco → cor em 2s pode parecer "flash"
sem easing. Refinamento:

```javascript
// Pseudocódigo
function animarNascimento(no, corFinal) {
  // Fase 1 (0 → 0.5s): pulso radial (esfera-halo expande de 1x para 2x)
  no.cor = '#ffffff';
  no.escala = 1.0;
  tween(no.haloEscala, 1.0, 2.0, 0.5, 'easeOutCubic');

  // Fase 2 (0.5 → 1.5s): halo retorna, cor transiciona
  tween(no.haloEscala, 2.0, 1.0, 1.0, 'easeInOutQuad');
  tween(no.cor, '#ffffff', corFinal, 1.0, 'easeInOutQuad');

  // Fase 3 (1.5 → 2.0s): assenta na cor final, glow normal
  // (nada — já tá lá)
}
```

**Efeito percebido:** sinapse disparando — onda radial + transição
cromática ≠ flash chamativo.

### 8.6 Câmera + interação

- **Auto-orbit:** câmera rotaciona lentamente (~5°/s) ao redor do
  centroide do grafo. Sensação de sistema vivo.
- **Pause-on-interaction:** primeira interação do usuário (touch,
  mouse drag, click em nó) **pausa** auto-orbit imediatamente. Volta
  só ao clicar num botão "retomar órbita" no canto inferior. Sem
  isso, irrita ao tentar focar num nó específico.
- **Touch nativo:** OrbitControls do 3d-force-graph já suporta
  pinch-zoom + drag-rotate no mobile. Sem código extra.

### 8.7 Painel lateral (clique no nó)

```css
.painel {
  position: fixed;
  right: 0;
  top: 0;
  width: min(380px, 90vw);
  height: 100vh;
  background: rgba(4, 4, 22, 0.95);
  backdrop-filter: blur(28px);
  border-left: 1px solid rgba(255, 255, 255, 0.08);
  transform: translateX(100%);
  transition: transform 280ms cubic-bezier(0.2, 0.8, 0.2, 1);
}
.painel.open { transform: translateX(0); }
```

**Conteúdo (em ordem):**
1. Tipo (chip colorido)
2. Conteúdo completo do fragmento (Space Mono, scroll vertical)
3. Metadados (curador, area, camada_temporal, via, criado_em)
4. Barra de confiança visual (0–1)
5. Conexões clicáveis (top-K vizinhos com nome resumido + tipo)
6. Botão "apagar" (vermelho discreto, confirma com pop-up)

**Vidro fumê** (`backdrop-filter: blur(28px)`) deixa o grafo visível
atrás. Em mobile com tela bloqueada por painel, dá pra clicar no grafo
em volta do painel sem fechá-lo (toques nas bordas).

### 8.8 Filtros (chips toggle)

Chips no topo central do viewport com label de cada tipo presente.
Comportamento:

- Estado inicial: todos visíveis (chips em cor saturada).
- Click num chip: isola só esse tipo (outros chips ficam dim, nós
  dos outros tipos viram opacidade 10%, sem clique).
- Click de novo no mesmo chip: volta tudo ao normal.
- Click em outro chip enquanto isolado: troca o filtro.

Deliberadamente **single-select**, não multi. Multi-select é
power-user feature; pra v0, single-select é mais decisivo.

### 8.9 Estados visuais futuros (roadmap, não implementar agora)

Os estados abaixo virão quando `gus-31` (Maturação do Grafo) for
implementado. NeuroGus v0 **não** representa nenhum deles — todos os
fragmentos hoje são tratados visualmente iguais. Documentar agora
serve pra:

1. Não criar conflitos de design quando o sistema crescer
2. Reservar "espaço visual" pras dimensões adicionais sem refactor

| Estado (vem do gus-31) | Como representar visualmente | Mecanismo Three.js |
|---|---|---|
| `confianca` baixando (decay) | **Opacidade reduz** (1.0 → 0.4) conforme `confianca` cai. Tamanho também encolhe levemente. | `material.opacity` |
| `staging` (em quarentena 30d) | **Borda pontilhada** ao redor da esfera. Texto "staging" no painel. | Outline shader leve OU segunda esfera wireframe transparente |
| `factual` (estabilidade_tipo) | Ícone **âncora** flutuando ao lado. Glow azul-petróleo (não confundir com cor de tipo). | Sprite 2D anexado ao nó |
| `sintetizado` (essência) | Esfera **maior** + saturação +20%. Linhas finas conectando aos N originais (que ficam menores e cinza-azulados). | `material.emissiveIntensity` + arestas com `linkOpacity` reduzido |
| `invalidated_belief` (negative memory) | Esfera **fantasma**: cor cinza-claro + opacidade 30% + sem glow. Conexão tracejada com o fragmento que invalidou. | `material.opacity = 0.3`, `emissiveIntensity = 0` |
| `tensao_nao_resolvida` (stasis prudencial) | **Pulsa vermelho/laranja** (oscilação `emissiveIntensity` 0.4–0.9). Indica conflito persistente entre sessões. | `requestAnimationFrame` loop de pulse |
| `entity_pair` (memória relacional) | Aresta **tipo "trust_signal"** entre nó "gus" e "gustavo" (entidades virtuais que aparecem como esferas-âncora separadas). | Nós especiais sempre presentes |

**Princípio unificador:** **opacidade** é o vetor visual primário do
estado interno do fragmento. Cor é tipo (semântico). Tamanho é
confiança (dinâmica). Forma é classe (esfera padrão; outline/halo
diferente sinaliza estado).

Isso permite que **tudo seja visto simultaneamente** sem o usuário
precisar trocar de "modo" — diferentes dimensões usam canais
visuais diferentes.

### 8.10 Toast de nascimento

Canto inferior direito, slide-in de baixo:

```
┌─────────────────────────────┐
│ 🌟 Novo fragmento            │
│ tipo: decisao                │
│ "Decidi implementar Passo 2  │
│  do gus-28 hoje..."          │
│ via telegram-claude          │
└─────────────────────────────┘
   (fade out após 4s)
```

Acumula até 3 simultâneos (empilha verticalmente). Quarto e além
fica em fila e aparece quando os anteriores expiram.

---

## 9. Plano de implementação por fase

Cada fase tem **definição de pronto** (DoP) e checkpoints. Branch única
por fase.

### Fase 0 — Pre-flight (~30 min)

Decisões e localização de assets antes de tocar em código.

- [ ] Decidir top-K e threshold (defaults: K=3, threshold=0.6) — confirmar
- [ ] Localizar mock HTML do Drive da Claude Chat (28/04) ou decidir
      recriar do zero
- [ ] Confirmar que `CUSTOM_GPT_TOKEN` está setada no Railway service do
      bot
- [ ] Confirmar que `OPENAI_API_KEY` está setada (já está, mas conferir)
- [ ] Backup mental: como vai testar localmente sem Qdrant Cloud
      (decisão: smoke test mocka `hub.store`, integração real só pós-merge)

**DoP:** Gustavo aprova os 3 defaults + mock HTML está acessível ou
descartado.

### Fase 1 — Backend SSE (~2h)

Criar a infraestrutura de eventos sem frontend ainda.

- [ ] Branch `claude/neurogus-fase1-backend-sse`
- [ ] Criar `hub/events.py` com `broadcast()` + `subscribe()`
      (~50 linhas, esqueleto na seção 7.5)
- [ ] Hook em `hub/store.py:ingestar()`:
      - [ ] Função `_calcular_vizinhos(vetor, k, threshold, exclude_id)`
            usa `client.search(...)` no Qdrant pra retornar top-K
      - [ ] Salva `relacionados: [id1, id2, id3]` no payload
      - [ ] Dispara `broadcast()` fire-and-forget via
            `asyncio.create_task` (ou equivalente em contexto sync)
- [ ] Adicionar 2 endpoints em `hub/routes.py`:
      - [ ] `GET /hub/recent?limit=N` (Bearer auth normal, JSON)
      - [ ] `GET /hub/stream?token=X` (StreamingResponse SSE,
            auth via query param)
- [ ] Smoke test local: import + valida que função existe e schema
      do retorno bate
- [ ] Smoke test de integração: `curl --no-buffer -H "Authorization:
      Bearer X" .../hub/stream` em uma janela; em outra janela,
      `POST /hub/ingestar` deve aparecer no SSE da primeira

**DoP:**
- Endpoint `/hub/recent` retorna últimos N fragmentos com `relacionados`
- Endpoint `/hub/stream` mantém conexão aberta e empurra evento JSON
  por `data: {...}\n\n` quando `ingestar()` é chamado
- PR mergeado, deploy automático no Railway, smoke test em produção
  passou (curl real do bot)

**Validação:** mandar mensagem no Telegram, abrir SSE em terminal local
com curl, ver fragmento aparecer ~5-10s depois (tempo do curador).

### Fase 2 — Frontend produção (~3h)

Substituir mock por dados reais. Pré-requisito: Fase 1 mergeada.

- [ ] Branch `claude/neurogus-fase2-frontend`
- [ ] Criar `api/neurogus.py` com:
      - [ ] Endpoint `GET /neurogus?token=X` que serve HTML inline
      - [ ] Endpoint `GET /neurogus/manifest.json` pro PWA install
      - [ ] (Opcional) `GET /neurogus/icon.png` pro ícone da home screen
- [ ] HTML embed:
      - [ ] CDN: Three.js r128, 3d-force-graph 1.73.3, Google Fonts
            (Syne 800 + Space Mono)
      - [ ] CSS: backdrop-filter, transitions, painel lateral
      - [ ] Lógica JS:
            - [ ] No boot: lê token da URL, fetch `/hub/recent`,
                  monta `{nodes, links}` (links via `relacionados[]`)
            - [ ] Geração dinâmica de cor por tipo (HSL golden-ratio)
            - [ ] `EventSource('/hub/stream?token=X')` pra novos
                  fragmentos
            - [ ] Animação de nascimento (3 fases: pulso, transição,
                  assenta)
            - [ ] Pause-on-interaction da auto-orbit
            - [ ] Click em nó → painel lateral
            - [ ] Botão apagar → `DELETE /hub/fragmento/{id}` (com
                  confirmação)
            - [ ] Filtros chips no topo
            - [ ] Toast de nascimento (canto inferior direito)
- [ ] Adicionar `DELETE /hub/fragmento/{id}` em `hub/routes.py`
      (Bearer normal, chama `store.deletar`)
- [ ] Registrar `api.server.app.include_router(neurogus_router)` em
      `api/server.py`

**DoP:**
- Acessar `https://api-gus.../neurogus?token=X` no navegador retorna
  grafo populado
- Abrir Telegram, mandar mensagem; ~5-10s depois novo nó nasce no
  grafo
- Touch/click funcionam no mobile
- Painel lateral abre, conexões clicáveis, botão apagar funciona

**Validação:** abrir no celular, mandar 3 mensagens no Telegram,
observar 3 nós nascendo. Apagar 1 nó, confirmar que somem do grafo
e do Qdrant.

### Fase 3 — PWA install + polish (~1h)

Ajustes pós-validação Fase 2 que fazem o NeuroGus ser "produto" e
não só "página".

- [ ] `manifest.json` completo (name, short_name, icons, theme_color,
      background_color, display: standalone, start_url)
- [ ] Service worker simples pra cache de assets estáticos
      (Three.js, fontes — não cache de dados, é tudo SSE/dinâmico)
- [ ] Meta tags pra iOS Add-to-Home-Screen (apple-touch-icon,
      apple-mobile-web-app-capable)
- [ ] Reconnect automático SSE com `Last-Event-ID` se conexão cair
      (tela bloqueada, perda de rede)
- [ ] Indicador visual de status da conexão (verde / amarelo
      "reconectando" / vermelho "offline")

**DoP:** instalável como app no Android Chrome e iOS Safari. Funciona
em background quando volta foco. Reconnect transparente.

### Fase 4 — Validação real (1-2 semanas de uso)

Sem código novo. Só observação.

- [ ] Usar 1 semana inteira: abrir NeuroGus diariamente, mandar
      mensagens no Telegram, observar grafo
- [ ] Anotar friccções:
      - Performance bate gargalo em N=?
      - Cor dinâmica fica confusa quando há > N tipos?
      - Auto-orbit é incômodo ou útil?
      - Painel lateral tem informação faltando?
- [ ] Decisão pós-validação: continuar polindo OU partir pra estados
      visuais futuros (opacity decay, etc.) — depende do gus-31
      Maturação estar pronto

**DoP:** lista de fricções escrita em `_log/neurogus-validacao-DDMM.md`,
discutida com Gustavo, decisão sobre próximos passos tomada.

---

## 10. Decisões já tomadas (não rediscutir)

Cada decisão abaixo foi resolvida e tem justificativa. Mudar exige
argumento novo, não só mudança de gosto.

### 10.1 Stack frontend: 3d-force-graph

**Decidido em:** demanda 14-01 (Claude Chat 28/04)
**Por quê:** API de alto nível, partículas direcionais nativas,
OrbitControls, suporta até ~5k nós (suficiente pro horizonte de uso).
**Trade-off aceito:** não escala pra 10k+ nós. Cosmograph reservado
pra esse caso futuro como "view 2D mapa completo".

### 10.2 Cor dos nós: por tipo, não por curador

**Decidido em:** demanda 14-01 (Claude Chat 28/04)
**Por quê:** o que importa visualmente é o que a memória **é**, não
quem a extraiu. Curador (Haiku/GPT) é metadata de proveniência,
disponível no painel lateral.
**Implementação:** cor gerada dinamicamente via HSL golden-ratio
(decisão complementar tomada nesta sessão pra evitar tabela hardcoded).

### 10.3 Conexões: por afinidade semântica, não por hash_janela

**Decidido em:** sessão 29/04 (correção da proposta original)
**Por quê:** `hash_janela` liga só 2-5 fragmentos da mesma curadoria.
Sem afinidade semântica, grafo vira ilhas desconexas — não é "rede
neural", é "lista de janelas".
**Implementação:** top-K por nó (K=3, threshold cosine 0.6),
pré-computado no backend ao ingerir, salvo em `relacionados[]` no
payload. `hash_janela` vira filtro/destaque secundário.

### 10.4 Stack backend: SSE, não WebSocket

**Decidido em:** demanda 14-01 (Claude Chat 28/04) + revisão 29/04
**Por quê:** comunicação é unidirecional (servidor → browser).
WebSocket bidirecional é overkill, exige libs extras, reconnect
manual. SSE é nativo no browser via EventSource, com reconnect
automático via `Last-Event-ID`.

### 10.5 Onde vive: mesmo container do bot

**Decidido em:** demanda 14-01 (Claude Chat 28/04)
**Por quê:** sem custo extra, sem secrets duplicados, sem deploy
separado. Bot + API + NeuroGus rodam no mesmo processo via
asyncio.gather (já é o padrão atual).

### 10.6 Auth: Bearer token compartilhado (CUSTOM_GPT_TOKEN)

**Decidido em:** sessão 29/04
**Por quê:** single-user, single-purpose. Não vale a complexidade
de OAuth/JWT. Token via query param em SSE/HTML é necessário porque
EventSource não suporta header custom.
**Trade-off aceito:** token aparece em logs/history do browser.
Mitigação: rotação periódica OU criar `NEUROGUS_TOKEN` separado
quando o atrito justificar.

### 10.7 Estados visuais avançados: roadmap futuro (gus-31)

**Decidido em:** sessão 29/04
**Por quê:** decay/quarentena/factual/sintetizado/invalidated
dependem do gus-31 (Maturação do Grafo) estar implementado. NeuroGus
v0 funciona sem — todos os fragmentos são tratados igual visualmente.
**Reservado:** seção 8.9 documenta como cada estado vai aparecer
quando a Maturação for implementada (opacidade pra decay, âncora
pra factual, etc.).

### 10.8 Filtros: single-select, não multi

**Decidido em:** sessão 29/04
**Por quê:** decisivo no v0, fácil no mobile. Multi-select é
power-user feature, fica pra Fase 3+.

### 10.9 Cores dinâmicas: HSL golden-ratio

**Decidido em:** sessão 29/04 (correção do briefing original)
**Por quê:** não escala hardcode de N cores quando aparecem tipos
novos. Golden-ratio garante distribuição visual e consistência por
tipo. Saturação 70%, luminância 60% (vivacidade sem cansar).

### 10.10 Curador modelo (Haiku + GPT-4o-mini)

**Decidido em:** gus-29 Fase 3 (PR #44, 29/04)
**Por quê:** resiliência (se Anthropic offline, GPT continua) +
custo (~10x menor que Haiku+Sonnet) + A/B inter-família mais
informativo.
**Relevante pro NeuroGus:** o campo `curador` no payload pode ter
"haiku", "gpt", e historicamente "sonnet" (legado). Painel lateral
mostra mas não filtra (proveniência, não significado).

---
