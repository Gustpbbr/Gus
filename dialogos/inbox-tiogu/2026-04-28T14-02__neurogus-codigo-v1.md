---
tipo: demanda
origem: claude-chat
destino: tiogu
prioridade: baixa
status: pendente
criado_em: 2026-04-28T14:02:00-03:00
processado_em: ""
processado_por: ""
acao_sugerida: criar_novo
destino_path: projetos/gus/neurogus-28-codigo-v1.md
contexto: "Documentacao NeuroGus — codigo do prototipo visual mock v1 (nao e producao)"
---

# NeuroGus — Codigo do Prototipo Visual v1

> **Atencao:** Este e um mock de validacao estetica, nao codigo de producao. Dados sao simulados via setInterval. SSE real, autenticacao e conexao com Qdrant sao implementados separadamente conforme spec em `neurogus-28-arquitetura.md`.

## Como usar

Salvar como `.html` e abrir no browser. Nao requer servidor — carrega 3d-force-graph via CDN.

## Dependencias (CDN)

- Three.js r128
- 3d-force-graph 1.73.3
- Google Fonts: Space Mono + Syne

## Funcionalidades do mock

- Grafo 3D com 30 fragmentos simulados e rotacao orbital automatica
- Cor por tipo de memoria (8 tipos, 8 cores)
- Labels flutuantes: 5 nos mais proximos da camera + vizinhanca do no selecionado
- Painel lateral com metadados, barra de confianca e conexoes clicaveis
- Filtros por tipo de memoria
- Simulacao de novo fragmento a cada 9s (substitui SSE real)
- Toast de nascimento de fragmento
- Exclusao de fragmento com atualizacao do grafo
- Responsive (mobile-ready)

## Localizacao do arquivo HTML

O arquivo `neurogus.html` completo esta disponivel na pasta `inbox-tiogu` do Drive (criado em 28/04/2026 nessa mesma sessao Claude Chat).

## Proximos passos para versao real

1. Substituir dados simulados por `GET /hub/recent?limit=50&token=...`
2. Substituir `setInterval(addFrag, 9000)` por `new EventSource('/hub/stream?token=...')`
3. Adicionar handler SSE: `es.onmessage = (e) => addRealFragment(JSON.parse(e.data))`
4. Adicionar `DELETE /hub/fragmento/{id}` no botao de exclusao
5. Mover HTML para `api/neurogus.py` e servir via FastAPI

## Resultado
