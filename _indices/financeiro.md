---
tipo: indice
area: financeiro
atualizado: 2026-04-24
---

# Índice — Financeiro

## Estado atual
Arquivo de overview criado como ponto de partida. Sem números fechados ainda. Renda principal: Dimagem. Obra em Paty do Alferes começa maio/2026 sem orçamento fechado. Custo do Gus estimado em ~US$X/mês (a confirmar).

Arquivo mestre: `pessoal/financeiro/resumo-financeiro.md` — situação geral, metas. *(a criar)*

## Últimos editados (5 mais recentes)
- `overview.md` — 2026-04-24

## Todos os arquivos (ordem alfabética)
- `overview.md` — overview financeiro geral (rascunho inicial)

## Pastas relacionadas
- `pessoal/financeiro/` — extratos, resumo-financeiro.md (mestre)

## Convenções desta área

- **Mestre:** `pessoal/financeiro/resumo-financeiro.md` — atualizar a cada captura relevante.
- **Extrato:** `pessoal/financeiro/extrato-[banco-ou-fonte]-[mes]-[ano].md`.
- **Notas isoladas:** `pessoal/financeiro/nota-[descricao-curta].md`.
- **Dados sensíveis** (conta, agência, chave Pix, cartão): salvar em `sensivel/financeiro/`, não aqui.
- **Frontmatter padrão:** `tipo`, `data`, `valor_total` (quando faz sentido).

## Fluxo quando chegar um extrato

1. Bot detecta se é sensível (número de cartão, conta completa etc.) → se sim, vai pra `sensivel/financeiro/`.
2. Se for resumo agregado sem dados identificáveis, vai pra `pessoal/financeiro/`.
3. Atualizar `resumo-financeiro.md` com total ou observação do mês.
4. Atualizar este índice.
