---
tipo: indice
area: saude
atualizado: 2026-04-24
---

# Índice — Saúde

## Estado atual
Gustavo tem **hipertireoidismo** em tratamento com **tapazol**, acompanhado por endocrinologista. O histórico completo fica em `pessoal/saude/historico-saude.md` (mestre).

*(Seed inicial — atualizar com dados reais quando primeira consulta/exame for capturado pelo bot.)*

## Últimos editados (5 mais recentes)
- *(sem registros ainda)*

## Todos os arquivos (ordem alfabética)
- *(sem registros ainda)*

## Pastas relacionadas
- `pessoal/saude/` — exames, consultas, historico-saude.md (mestre)

## Convenções desta área

- **Arquivo mestre:** `pessoal/saude/historico-saude.md` — condições, medicamentos, evolução. Atualizar ao receber novo exame ou consulta.
- **Exame:** `pessoal/saude/exame-[tipo]-[mes]-[ano].md`. Ex: `exame-sangue-abr-2026.md`.
- **Consulta:** `pessoal/saude/consulta-[especialidade]-[mes]-[ano].md`. Ex: `consulta-endocrino-abr-2026.md`.
- **Frontmatter padrão:** `tipo: exame|consulta`, `data: AAAA-MM-DD`, `valores_alterados: [lista]` (só exames).
- **Wikilinks obrigatórios:** todo exame e consulta deve linkar pro `[[historico-saude]]`.

## Fluxo quando chegar um exame novo

1. Bot transcreve valores em tabela dentro do MD do exame.
2. Bot marca flags de valores fora da faixa.
3. Bot atualiza `pessoal/saude/historico-saude.md` com o novo exame (resumo + link).
4. Bot atualiza este índice: adiciona em "Últimos editados" e "Todos os arquivos".
