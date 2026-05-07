---
tipo: blueprint-spec
componente: visao-geral
ordem: 1
---

# Visão geral

## O que esse blueprint constrói

Um **agente pessoal de IA** que:

- Tem **identidade própria** (nome, personalidade, princípios não-negociáveis)
- Aparece em **múltiplos canais simultâneos** (Telegram, web, voz mobile,
  etc.) compartilhando memória e identidade entre eles
- **Lembra** das conversas passadas via curadoria automática
  (resumo extrativo periódico salvo em vector store)
- **Escreve no GitHub** como vault de conhecimento (.md estruturados
  por área)
- Sincroniza **bidirecional** com Google Drive (espelho leitura/escrita)
- Tem **autodiagnóstico** e **auto-observação** (logs estruturados,
  retro-engine de fim de sessão)
- **Custo previsível** (~US$5–30/mês dependendo do uso)

## Pra quem serve

- **Pessoa não-programadora** que quer um assistente conversacional
  persistente com memória própria, sem depender de um único produto
  (não é "outro ChatGPT", é teu agente em múltiplos canais)
- **Pesquisador/profissional** que precisa de um segundo cérebro
  estruturado em vault tipo Obsidian/Notion mas com IA escrevendo nele
- **Criador** que quer ter um agente reproduzível por repositório
  (clonar pra outro projeto = novo agente com identidade nova)

## Pra quem NÃO serve

- Quem quer apenas chatbot single-port (use ChatGPT direto)
- Quem não topa custo recorrente (este blueprint pressupõe ~US$5/mês
  mínimo em chamadas Anthropic + Qdrant)
- Quem não quer manter um repositório git ativo (o vault GitHub é
  componente central, não opcional)

## Por que multi-portas

Assistente conversacional com memória só faz sentido se aparece **onde
o dono está**:

- Mensagem rápida no celular → Telegram ou WhatsApp
- Reflexão longa em texto → web (Claude Chat ou similar)
- Voz no carro/casa → Custom GPT mobile, Alexa, Siri
- Desenvolvimento de código → IDE (Claude Code, Cursor)

Cada canal é uma **porta**. Todas as portas leem/escrevem na mesma
memória e seguem a mesma identidade. Sem isso, vira N assistentes
desconexos.

## Princípio central

**1 vault GitHub + 1 brain de memória + N portas que veem tudo.**

```
                ┌──────────────────────────────────────┐
                │  Vault GitHub (este repo)            │  ← fonte de conhecimento
                │  Vector store (Qdrant)               │  ← memória semântica
                │  Identidade canônica em arquivo .md  │  ← quem o agente é
                └──────────────┬───────────────────────┘
                               │
       ┌──────────────┬────────┼────────┬──────────┬──────────────┐
       │              │        │        │          │              │
   Telegram        Claude  Custom GPT  Alexa    IDE/CLI    Plugin Carro
   (default)        Chat    (mobile)   (casa)   (dev)        (futuro)
```

## O que NÃO está incluso

- **Escolha de personalidade do agente** — você decide (templates
  ajudam, mas conteúdo é teu)
- **Conteúdo do vault** — começa vazio. O dono e o agente populam
  juntos durante o uso
- **Código de outras portas** — Telegram tem template completo;
  Custom GPT, Alexa, etc. ficam como roadmap
- **Hospedagem física** — pressupõe Railway pro bot; outros provedores
  (Fly, Render, Heroku) são adaptáveis mas não cobertos
- **Backup de dados pessoais** — vault no GitHub já é versionado,
  mas backups regulares de longo prazo são responsabilidade do dono

## Quanto tempo leva implementar

Estimativa honesta pra ter **bot Telegram funcional + memória básica**:

- Decidir identidade do agente: 1-2h (você + IA conversando)
- Setup contas externas (Anthropic, Qdrant, GitHub, Railway, Telegram bot): 1h
- Implementação guiada pela IA: 4-6h (varia muito)
- Calibragem inicial (ajuste de tom, primeiros saves de memória): 2-3h
- **Total realista**: ~10-12h ao longo de 2-4 dias

Adicionar portas extras (Custom GPT, Alexa) acrescenta 2-4h cada.

## O que vem depois

Depois que o agente está funcional:

- **Curadoria humana** das memórias salvas (revisar e deletar lixo)
- **Documentar decisões arquiteturais** (ADRs em `04-governanca-e-saude/`)
- **Automação de ciclos** (briefing matinal, retrospectiva semanal,
  reflexão quinzenal)
- **Adicionar portas conforme necessidade** real (não criar porta vazia
  só por completude)
