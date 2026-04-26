---
tipo: demanda
origem: tiogu
destino: claude-code
prioridade: media
status: pendente
criado_em: 2026-04-26T00:43:00-03:00
processado_em: ""
processado_por: ""
---

# Criar site HTML explicando a arquitetura do projeto

## Ação
Criar um arquivo `site-arquitetura/index.html` (ou pasta equivalente) com um site estático em HTML/CSS explicando toda a arquitetura do projeto Gus:

- Visão geral do sistema (portas de acesso: Telegram, Claude Code, Claude Chat, Custom GPT)
- Componentes principais (Mem0, GitHub, Railway, GitHub Actions)
- Fluxo de dados entre os componentes
- Projetos ativos (Phronesis, MGE, TER, Axon)
- Canal de diálogos entre portas (`dialogos/`)

## Contexto
Gustavo quer um site visual e explicativo da arquitetura completa do projeto, gerado pelo Claude Code. Quando terminar, escrever resultado em `dialogos/inbox-tiogu/` para notificação automática via GitHub Action.

## Critério de sucesso
- HTML válido, navegável no browser
- Visual claro com diagrama ou descrição da arquitetura
- Arquivo salvo no repositório
- Notificação enviada em `dialogos/inbox-tiogu/` ao concluir
