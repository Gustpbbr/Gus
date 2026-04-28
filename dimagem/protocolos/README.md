# dimagem/protocolos/

Protocolos clínicos do Dimagem — sedação, anestesia, jejum, contraste,
emergência.

## Estrutura

- **`protocolo-sedacao-<contexto>.md`** — protocolos de sedação por
  tipo de exame ou faixa etária
- **`protocolo-anestesia-<contexto>.md`**
- **`protocolo-emergencia-<situacao>.md`**
- **`<assunto-protocolar>.md`** — geral

## Convenção

- Frontmatter: `tipo`, `area: dimagem`, `versao`, `validado_em`
- Manter cada protocolo curto e operacional (passos, doses, contraindicações)
- Validação: ao mudar protocolo, atualizar `validado_em` e versão

## Quando salvar

Bot Telegram detecta quando você compartilha protocolo da clínica
e salva aqui. Nunca incluir dados de paciente — protocolo é regra
geral, não caso específico (esse vai em `casos/`).
