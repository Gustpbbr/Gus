# esportes/

Atividade física — treinos, evolução, metas.

## Estrutura

- **`evolucao.md`** — MD mestre. Visão consolidada da evolução
  (peso, performance, metas em andamento, modalidades praticadas).
- **`treinos/`** — registros de cada treino. `treino-AAAA-MM-DD.md`.

## Convenções

- Wikilinks: cada treino inclui `Relacionado: [[evolucao]]`
- Frontmatter automático no save
- Métricas: registrar em formato consistente pra agregação futura
  (ex: distância em km, tempo em minutos, peso em kg)

## Quando o bot salva aqui

Bot detecta menção a treino/exercício/atividade física e salva em
`esportes/treinos/treino-<data>.md`. Atualiza `evolucao.md` se
mencionar progresso (PR, meta atingida, etc.).

## Templates futuros

Quando começar a usar, criar:

- `metas-AAAA.md` — metas anuais
- `lesoes-historico.md` — histórico de lesões pra evitar overtraining
