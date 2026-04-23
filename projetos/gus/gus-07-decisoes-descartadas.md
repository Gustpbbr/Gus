---
tipo: documentacao-projeto
projeto: gus
parte: 7-de-7
atualizado: 2026-04-23
---

# Gus — Decisões descartadas e abertas em aberto

Este arquivo documenta **o que o Gus decidiu não fazer** e **por quê**. Serve pra não reabrir discussão a cada sessão nova e pra registrar o caminho, não só o destino.

## Descartado com motivo

### Frameworks de orquestração (Langchain, LlamaIndex, CrewAI)

Descartado. O Gus tem 7 arquivos Python que fazem tudo — tool use loop nativo do Anthropic SDK resolve. Frameworks agregam camadas de abstração sem ganho real em um agente single-user com 3 tools.

Reabrir apenas se: Gus crescer para múltiplos usuários ou tool count explodir (>20).

### Mem0 self-hosted

Descartado. A hosted API custa US$0 no free tier para um user ativo, atualiza sozinho, e tem SDK pronto. Self-hosted exige VPS, Postgres + pgvector + OpenAI embeddings, backup próprio. Zero benefício pro Gustavo.

Reabrir apenas se: Mem0 hosted mudar modelo de cobrança e o custo virar proibitivo.

### Webhook em vez de polling

Descartado. Para bot de um único usuário, polling é mais simples — não precisa de domínio, certificado TLS, endpoint HTTP público. Long polling do `python-telegram-bot` é estável.

Reabrir apenas se: bot atender múltiplos usuários (>10) ou latência de polling virar problema perceptível.

### Heroku em vez de Railway

Descartado. Heroku matou o free tier. Railway tem free tier ativo, deploy via Dockerfile, UI simples pra variáveis, restart policy. Mesma lógica serve também para Fly.io e Render — não há razão pra mudar do Railway até encontrar problema real.

### MemPalace

Descartado. Era a proposta original do planejamento antigo (ver `docs/gus-briefing-opus.md`) — indexação local de arquivos em Windows via CLI própria. Substituído pelo conjunto **Mem0 + GitHub + Drive sync**, que é:
- Plataforma-neutro (não depende de Windows)
- Visível (conteúdo em `.md`, não num banco local)
- Multi-porta (qualquer IA lê o Drive; Mem0 tem SDK)
- Backup automático (git + GitHub Action de export)

Os MDs em `docs/` são resquícios dessa fase e estão desatualizados.

### Windows Task Scheduler

Descartado junto com MemPalace. Proatividade agora vem de GitHub Actions com cron (sem PC do Gustavo ligado) e de mensagens ad-hoc do bot. Task Scheduler exigia máquina ligada 24/7.

### Roteamento automático de modelo no `llm.py`

Descartado por ora. A primeira versão tinha heurística ("se input >1k chars → Opus", etc). Retirado por duas razões:
1. Complexidade extra sem economia mensurável (o `HARD_LIMIT_USD_MONTH` já protege o teto).
2. Sonnet 4.6 resolve 95% dos casos. Quando precisar de Opus específico, o Gustavo pode pedir explicitamente.

Reabrir apenas se: custo mensal começar a bater em `HARD_LIMIT_USD_MONTH` regularmente.

### Dashboard HTML de métricas

Descartado por ora. O plano antigo (`docs/gus-metricas.md`) previa HTML dashboard gerado do `jsonl`. Substituído por: relatório semanal em `.md`, visível no Obsidian ou Drive. Sem código HTML para manter.

Reabrir apenas se: métricas virarem input de decisão frequente e tabela no `.md` não bastar.

## Em aberto (não é hora ainda)

### SELF-1 — camada de metacognição e metavontade

Proposta da Kimi. Dois agentes internos dialogam periodicamente:
- **Nosis** (cognição) — observa padrões, identifica viés, sugere revisões
- **Thymos** (vontade) — acompanha metas, intenções, drift de propósito

Mais um **CEX Deliberador** para decisões complexas: análise multi-perspectiva antes de responder.

Não implementar até: as 5 fases estarem concluídas **e** o uso real validar que o Gus tem massa crítica de memória pra uma camada metacognitiva ser diferente de teatro. Risco alto de virar bloat que só gasta tokens.

### Painel web próprio (PWA)

Considerado na fase de planejamento. Adiado indefinidamente — Telegram + ChatGPT + Alexa + Claude Code cobrem todos os casos de uso. Painel web só entra se aparecer uma necessidade que nenhuma das outras portas resolve.

### Integração com Notion ou similar

Não. `.md` no GitHub + Drive + Obsidian já forma um triângulo completo de edição, visualização e sincronização. Notion adiciria uma fonte a mais sem resolver problema existente.

### Múltiplos usuários no Gus

Não. O Gus é projetado como agente **pessoal** — `user_id = "gustavo"` hardcoded em `memory.py:8` e `export_mem0.py:15`. `TELEGRAM_CHAT_ID` único em `bot.py`.

Se o Gustavo quiser oferecer a mesma arquitetura para outros, não é "abrir o Gus" — é clonar o repo e cada pessoa roda o seu. Nome diferente, bot diferente, Mem0 com user_id próprio.

## Regras para adicionar coisas ao Gus

1. **Começar pelo caso de uso real** — não pela feature interessante.
2. **Reaproveitar camadas existentes** (Mem0, GitHub, Drive, Claude API). Adicionar dependência só se não der pra resolver com o que tem.
3. **Preferir `.md` + GitHub Action em cima de servidor próprio.** Tudo que for cron, relatório, export, notificação pode ser Action.
4. **Confirmar antes de desinstalar.** Se remover algo que parece inútil, checar em 2-3 semanas se alguém sentiu falta.
5. **Se a decisão for reversível (mudar modelo default, ajustar limite), fazer.** Se for irreversível (deletar histórico, revogar token em produção), pausar e confirmar.

## O que o Gus não é

Para deixar explícito:

- **Não é um produto** — é infraestrutura pessoal do Gustavo. Sem roadmap comercial, sem SLA, sem usuários externos.
- **Não é substituto do Gustavo** — executa ações sob comando, não toma decisões por ele.
- **Não é memória total** — Mem0 guarda o que é salvo ativamente; `.md` guardam o que é estruturado. Conversa espontânea não vira memória a menos que uma delas seja explicitamente atualizada.
- **Não é IA "geral"** — é um conjunto de tools bem definidas em volta do Claude. Quando precisar de algo fora do escopo, é o Gustavo direto no Claude Code/Chat.

Relacionado: [[gus-01-visao-geral]], [[gus-04-seguranca-protecao]], [[gus-05-portas-capacidades]], [[gus-06-autonomia-acoes]]
