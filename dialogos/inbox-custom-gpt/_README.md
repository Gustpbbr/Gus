# Inbox — Custom GPT (mobile)

Demandas que **Custom GPT** (no app ChatGPT mobile) deve processar.

## Status

V1 ainda não automatiza leitura — Custom GPT lê só quando Gustavo pedir
explicitamente ("Gus, lê inbox-custom-gpt e processa as pendentes").

## Quem escreve

- **Claude Chat / Claude Code / TioGu / Gustavo** — todos podem encaminhar
  demandas pra Custom GPT processar com voz fluida em mobile

## Frontmatter

Ver `dialogos/README.md`.

## Tipos típicos

- Resumir conteúdo longo em formato falável
- Buscar informação específica e ler em voz alta
- Capturar pensamento por voz e salvar (Custom GPT chama `salvar_memoria`)

## Após processar

1. Status, processado_em, processado_por: `custom-gpt`
2. Mover pra `archive/`
