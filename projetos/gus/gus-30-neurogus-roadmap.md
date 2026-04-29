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
  real — grafo 3D onde cada nó é um fragmento do Hub Qdrant, conectados por
  feixes de luz quando vêm da mesma janela de conversa.
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
- A **cor** indica o `tipo` semântico (8 cores fixas, ver design visual).
- Esferas conectadas por **arestas com partículas de luz** quando vêm do
  mesmo `hash_janela` (mesma janela de curadoria — fragmentos extraídos
  juntos da mesma conversa).
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
