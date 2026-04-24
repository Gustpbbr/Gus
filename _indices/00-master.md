---
tipo: indice
area: master
atualizado: 2026-04-24
---

# Índice mestre do Segundo Cérebro

Este é o ponto de entrada pra navegar tudo. Cada área tem um índice próprio em `_indices/`.

## Áreas ativas

- [[saude]] — hipertireoidismo, exames, consultas, medicamentos
- [[financeiro]] — extratos, resumo financeiro, metas
- [[projetos]] — Phronesis-Bench, MGE/MGX, TER, Axon, Gus
- [[dimagem]] — clínica de anestesia (protocolos, casos, admin)
- [[receitas]] — doces e salgadas organizadas por tipo
- [[capturado]] — links, ideias e capturas soltas

## Pastas especiais (sem índice temático)

- `_indices/` — esta pasta
- `projetos/gus/` — documentação do próprio Gus (auto-referência)
- `sensivel/` — dados que não espelham no Drive (ver [[../sensivel/README]])
- `tiogubot/` — conteúdo do bot Telegram (placeholder atual)
- `esportes/` — treinos e evolução (ainda sem índice dedicado — criar quando começar a popular)
- `leituras/` — livros e papers (ainda sem índice dedicado)
- `pessoal/diario/` — reflexões (dentro de pessoal/)

## Regras globais

- **Nomenclatura:** sem acentos, sem espaços, hífen para separar.
- **Arquivos com data:** `[tipo]-[mes-abreviado]-[ano].md` → `exame-sangue-abr-2026.md`
- **MDs mestres:** nome genérico sem data → `historico-saude.md`, `evolucao.md`
- **Wikilinks:** conectam arquivos relacionados — `[[nome-do-arquivo]]` sem path nem extensão.
- **Frontmatter:** toda criação nova tem frontmatter com `capturado_em` (BRT) e `via:` (telegram / manual / etc).

## Como usar este índice

O Gus consulta este arquivo quando precisa de visão geral do Segundo Cérebro. Quando atualizar uma área, atualizar aqui o status geral se mudou algo estrutural.
