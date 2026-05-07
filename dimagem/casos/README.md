# dimagem/casos/

Casos clínicos didáticos do Dimagem. **LGPD: usar pseudônimo sempre.**

## Estrutura

- **`caso-<descricao-curta>-<mes>-<ano>.md`** — cada caso interessante,
  com pseudônimo do paciente, exame realizado, intercorrências relevantes,
  aprendizados clínicos.

## Regras LGPD

❌ **Nunca** salvar:
- Nome real do paciente
- CPF, RG ou documentos
- Convênio + procedimento + data juntos (rastreável)

✅ Salvar:
- Pseudônimo curto (`Paciente A`, `Caso da intubação difícil`)
- Faixa etária (criança, adolescente, adulto, idoso)
- Tipo de exame e intercorrência (sem identificadores)
- Aprendizado clínico, decisão tomada, resultado

## Diferença pra `dimagem/dia/`

- **`dimagem/dia/`**: registro operacional/contábil. Nome+exame+convênio
  do dia, mantém rastreabilidade pra cobrança. Permitido usar nome
  real porque é o registro próprio do trabalho.
- **`dimagem/casos/`**: registro didático/educacional. Pseudônimo,
  foco em aprendizado. Sai pro Drive (sync), pode ser compartilhado.
