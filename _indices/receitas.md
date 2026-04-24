---
tipo: indice
area: receitas
atualizado: 2026-04-24
---

# Índice — Receitas

## Estado atual
*(Seed inicial — atualizar quando primeira receita for capturada.)*

## Últimos editados (5 mais recentes)
- *(sem registros ainda)*

## Todos os arquivos (ordem alfabética)
- *(sem registros ainda)*

## Pastas relacionadas
- `receitas/doces/` — com subpastas (tortas, bolos, sobremesas)
- `receitas/salgadas/` — com subpastas (massas, carnes, vegetarianas)

## Convenções desta área

- **Nomenclatura:** `receitas/[doces|salgadas]/[subcategoria]/[nome-da-receita].md`.
- **Frontmatter padrão:** `tipo: doce|salgada`, `categoria: tortas|bolos|massas|carnes|etc`, `tempo_preparo_min`, `rendimento`, `origem` (link ou nome do livro/site).
- **Estrutura do MD:** ingredientes (lista), modo de preparo (lista numerada), observações (texto livre).

## Fluxo quando chegar receita

1. Bot identifica doce ou salgado, subcategoria.
2. Se subpasta não existe e a categoria é recorrente, cria subpasta.
3. Salva MD com frontmatter.
4. Atualiza este índice.
