---
tipo: demanda
origem: tiogu
destino: claude-code
prioridade: media
status: concluido
criado_em: 2026-04-26T00:43:00-03:00
processado_em: 2026-04-26T01:00:00-03:00
processado_por: claude-code
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

## Resultado

Gustavo redirecionou (durante a sessão Claude Code Web 25/04 ~01:00 BRT): site não precisa ser commitado em `site-arquitetura/`; em vez disso, deve ser entregue ao **Claude Chat** como demanda pra ser renderizado como Artifact no claude.ai (ele não consegue abrir HTML local). Pedido também: site sóbrio, compacto, baseado em qualquer material atualizado.

Entregas feitas nesta rodada:

1. **Demanda principal pro Claude Chat** com HTML completo embutido:
   `dialogos/inbox-claude-chat/2026-04-26T01-00__site-arquitetura.md`

2. **Notificação ao TioGu** (cumpre o critério de sucesso original):
   `dialogos/inbox-tiogu/2026-04-26T01-00__site-arquitetura-pronto.md`

Conteúdo do site (resumo sóbrio, página única, ~5 KB):
- Diagrama SVG inline (5 portas → 3 camadas compartilhadas + canal `dialogos/`)
- Tabela de portas (cérebro / função / status)
- Camadas compartilhadas (Mem0, GitHub vault, Drive mirror, identidade)
- Componentes operacionais (Railway, GH Actions, MCPs, hooks)
- Canal `dialogos/` (descrição + estrutura)
- Projetos ativos (Phronesis, MGE/MGX, TER, Axon, Gus)

Fontes consultadas (todas em `origin/main`, snapshot 2026-04-26):
`gus/gus-identity.md`, `gus/gus-bootstrap.md`, `projetos/gus/_estado-atual.md`,
`projetos/gus/gus-12-portas-futuras.md`, `projetos/gus/gus-16-canal-unificado.md`,
`dialogos/README.md`.

Próximo passo: este arquivo deve ir pra `dialogos/archive/` no commit que fecha a tarefa.
