---
tipo: demanda
origem: claude-chat
destino: tiogu
prioridade: baixa
status: pendente
criado_em: 2026-04-28T14:01:00-03:00
processado_em: ""
processado_por: ""
acao_sugerida: criar_novo
destino_path: projetos/gus/neurogus-28-arquitetura.md
contexto: "Documentacao NeuroGus — arquitetura e decisoes tecnicas (roadmap futuro, nao implementar)"
---

# NeuroGus — Arquitetura e Escolhas Tecnicas

> **Status:** Roadmap futuro. Documento de design para sprint de implementacao quando os pre-requisitos do ADR-001 estiverem concluidos.

---

## Decisao de biblioteca de visualizacao

### 3d-force-graph (vasturiano) — escolhida

Biblioteca JavaScript construida sobre Three.js. Fisica de forcas na CPU, rendering WebGL. API de alto nivel: voce passa `{ nodes, links }` e ela faz tudo.

Suporta nativamente:
- Particulas direcionais nas arestas (feixes de luz com velocidade configuravel)
- OrbitControls (zoom/pan/rotate com touch no mobile)
- Clique em no com callback
- Custom objects por no

Limite: a partir de ~5.000-10.000 nos comeca a travar (simulacao de forcas na CPU). Para a janela ativa do NeuroGus (~50-500 fragmentos recentes), essa limitacao e irrelevante.

### Cosmograph (cosmos.gl) — avaliado, nao escolhido

Engine 100% na GPU via shaders WebGL. Suporta centenas de milhares de nos em tempo real. Nao tem 3D nativo — e grafo 2D de alta performance.

Descartado para o caso principal por ausencia de 3D imersivo e particulas direcionais nativas.

**Uso futuro possivel:** segunda view "mapa completo" de toda a gus_hub. Um botao alterna entre "janela ativa 3D" (3d-force-graph) e "universo completo 2D" (Cosmograph).

---

## Decisao de cor

### Cor por tipo de memoria (adotada)

A cor primaria de cada no representa o tipo semantico: identidade_operacional, decisao, episodico, procedural, meta_reflexao, biografico, preferencia, rotina.

Rationale: o que importa visualmente e o que a memoria e. Ver a distribuicao de tipos no grafo e informacao cognitivamente relevante.

### Cor por curador (descartada)

Mostrar Haiku/Sonnet/Telegram/Claude Code como cor primaria foi avaliado e rejeitado. O curador e metadado de proveniencia, nao de significado. O grafo ficaria organizado por "quem fez" em vez de "o que e".

---

## Arquitetura de sistema

### Onde vive

Dentro da infraestrutura Railway existente — mesma instancia do bot TioGu e da API FastAPI. Sem servico separado, sem custo adicional.

```
api/
├── server.py       <- existente, adiciona rota /neurogus
├── dashboard.py    <- existente
├── camera.py       <- existente (padrao a seguir)
└── neurogus.py     <- NOVO: serve HTML + SSE + /hub/recent

hub/
├── store.py        <- existente, adiciona broadcast() em ingestar()
├── events.py       <- rascunho existente, finalizar fila SSE
├── curador.py      <- existente
└── routes.py       <- existente, adiciona /hub/recent e /hub/stream
```

### Fluxo completo

```
Gustavo escreve no Telegram
        |
    bot.py recebe
        |
curador.py processa (~5-10s, async fire-and-forget)
        |
hub/store.py:ingestar() salva no Qdrant gus_hub
        | <- broadcast(fragmento) aqui
hub/events.py coloca evento em asyncio.Queue global
        |
GET /hub/stream (SSE) consome a fila e empurra pro browser
        |
neurogus.html recebe evento -> novo no nasce no grafo
```

### As 4 pecas de implementacao

**1. hub/events.py — fila SSE**
asyncio.Queue global. broadcast() coloca fragmento na fila. /hub/stream consome e formata como `data: {json}\n\n`. ~40 linhas.

**2. hub/store.py — uma linha**
No final de ingestar(), chamar `await broadcast(payload)`. So isso.

**3. hub/routes.py — dois endpoints novos**
- `GET /hub/recent?limit=50&token=...` -> ultimos N fragmentos para inicializar o grafo no boot
- `GET /hub/stream?token=...` -> SSE com auth por query param

**4. api/neurogus.py — o frontend**
Serve o HTML. No boot, chama /hub/recent para popular o grafo. Conecta ao /hub/stream via EventSource. ~20 linhas de JS a mais em relacao ao prototipo mock.

### Autenticacao

Mesmo Bearer token da API. No SSE usa query param `?token=...` porque o browser nao suporta headers customizados em EventSource. Mesma logica ja em uso no dashboard existente.

---

## Decisoes de design visual

### Tipografia

- **Syne 800** — logo, titulos, valores numericos. Geometrica, forte, sem serifa.
- **Space Mono** — labels, metadados, UI chrome. Monospace tecnico sem ser generico.

Justificativa: evita Inter/Roboto/Arial. O NeuroGus e uma ferramenta pessoal com identidade propria.

### Fundo e atmosfera

`#030312` — e preto puro. O leve azul profundo cria sensacao de espaco sideral sem virar navy.

### Glow nos nos

`MeshPhongMaterial` com `emissive` ativado + `AdditiveBlending` — a esfera brilha de dentro e o brilho vaza para o espaco ao redor. Efeito de glow sem shader customizado.

### Painel lateral

`backdrop-filter: blur(28px)` + `rgba(4,4,22,0.95)` — vidro fume que deixa o grafo visivel atras. Borda sutil. Sem sombra hard — tudo e nevoa.

### Animacao de nascimento

No nasce branco (`#ffffff`) com val aumentado (+4), pulsa 2 segundos, depois transiciona para a cor do tipo. Simula sinapse disparando.

---

## Tamanho estimado de implementacao

| Peca | Linhas estimadas | Complexidade |
|------|-----------------|-------------|
| hub/events.py | ~40 | Baixa |
| hub/store.py (broadcast) | ~5 | Trivial |
| hub/routes.py (2 endpoints) | ~50 | Baixa |
| api/neurogus.py | ~30 | Baixa |
| Frontend (delta do mock) | ~20 JS | Trivial |
| **Total** | **~145** | **Baixa** |

## Resultado
