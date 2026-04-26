# Inbox — TioGu (Telegram)

Demandas que **TioGu (bot Telegram)** deve processar.

## Quem escreve aqui

- **Claude Chat** (claude.ai) cria arquivos no Drive em
  `Gus-Sync/dialogos/inbox-tiogu/` — workflow `import-from-drive.yml`
  puxa em até 15min
- **Claude Code** commita direto no GitHub
- **Custom GPT** chama nossa API REST (futuro: endpoint específico)
- **Gustavo** pode criar manual (Obsidian)

## Quem lê aqui

- **TioGu Telegram** — quando Gustavo pedir explicitamente
  ("Tiogu, processa as demandas pendentes" ou similar)
- Hoje a leitura é manual; futuro: cron 5min varre `prioridade: alta`

## Frontmatter obrigatório

Ver `dialogos/README.md` na raiz da pasta. Demanda mal formatada não é importada.

## Após processar

TioGu deve:
1. Marcar `status: concluido` + `processado_em` + `processado_por: tiogu`
2. Mover arquivo pra `dialogos/archive/`
3. Opcionalmente registrar resultado (memory_id Mem0, commit hash, etc.)
   no campo `## Resultado` no corpo do arquivo
