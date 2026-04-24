---
tipo: indice
area: projetos
atualizado: 2026-04-24
---

# Índice — Projetos

## Estado atual (abril/2026)

**Projetos ativos:**
- **Phronesis-Bench** — benchmark de metacognição e prudência epistêmica para LLMs. Prioridade máxima. Deadline: hackathon Kaggle/DeepMind em 16/abr/2026.
- **MGE/MGX** — pipeline multi-agente de geração criativa estruturada.
- **TER** — framework filosófico-computacional de deliberação ética para IA.
- **Axon** — governança contextual para famílias com crianças neurodivergentes.
- **Gus** — agente pessoal multi-porta (este sistema). Documentação própria em `projetos/gus/` + índice especial abaixo.

## Últimos editados (5 mais recentes)
- 2026-04-24 — [[gus/_estado-atual]] — handoff atualizado com bugs fechados hoje
- 2026-04-23 — [[gus/gus-01-visao-geral]] — criação inicial dos 7 MDs

## Todos os arquivos (ordem alfabética por projeto)
- `projetos/axon/` — *(ainda sem arquivos)*
- `projetos/gus/` — 8 arquivos (ver subseção abaixo)
- `projetos/mge/` — *(ainda sem arquivos)*
- `projetos/phronesis-bench/` — *(ainda sem arquivos)*
- `projetos/ter/` — *(ainda sem arquivos)*

### `projetos/gus/` (documentação do Gus)
- [[gus/_estado-atual]] — handoff entre sessões (ler PRIMEIRO ao retomar)
- [[gus/gus-01-visao-geral]]
- [[gus/gus-02-implementado]]
- [[gus/gus-03-configuracao-manual]]
- [[gus/gus-04-seguranca-protecao]]
- [[gus/gus-05-portas-capacidades]]
- [[gus/gus-06-autonomia-acoes]]
- [[gus/gus-07-decisoes-descartadas]]

## Pastas relacionadas
- `projetos/phronesis-bench/` — briefings e artefatos do Phronesis
- `projetos/mge/` — MGE/MGX
- `projetos/ter/` — TER
- `projetos/axon/` — Axon
- `projetos/gus/` — Gus (auto-referência)

## Convenções desta área

- **Um diretório por projeto** em `projetos/`.
- **Briefing inicial** em cada pasta: `[projeto]-00-briefing.md` ou `README.md`.
- **Estado do projeto:** manter um `[projeto]-estado-atual.md` atualizado quando houver marco.
- **Decisões importantes:** arquivo próprio ou dentro do briefing, sempre com data.
- **Wikilinks cross-projeto:** linkar explicitamente quando um projeto depende ou influencia outro.

## Fluxo quando chegar atualização de projeto

1. Bot identifica qual projeto.
2. Se é marco, decisão ou evento — cria MD próprio nomeado por data.
3. Se é evolução pequena — atualiza o `estado-atual.md` do projeto.
4. Atualiza este índice em "Últimos editados" e "Todos os arquivos".
