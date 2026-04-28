# pessoal/saude/

Saúde do Gustavo — exames, consultas, condições, medicamentos, evolução.

## Estrutura

- **`historico-saude.md`** — MD mestre. Visão consolidada: condições atuais,
  medicamentos em uso, alergias, histórico relevante. Atualizar quando
  mudar tratamento.
- **`exame-<tipo>-<mes>-<ano>.md`** — cada exame em arquivo próprio
  (ex: `exame-sangue-abr-2026.md`).
- **`consulta-<especialidade>-<mes>-<ano>.md`** — cada consulta
  (ex: `consulta-endocrino-abr-2026.md`).

## Convenções

- Wikilinks: cada exame/consulta inclui `Relacionado: [[historico-saude]]`
- Frontmatter automático no save: `capturado_em`, `via`
- Sensível (CPF, dados de outros pacientes): NÃO entra aqui — usar `sensivel/`

## Quando salvar

Ver `gus/system_prompt.md` — bot Telegram detecta exames e protocolos
e salva aqui automaticamente.
