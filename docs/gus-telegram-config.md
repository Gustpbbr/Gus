# GUS — Configuração Telegram Bot

**Tipo:** manual + estado-do-projeto  
**Data:** 2026-04-09  
**Status:** planejado — executar após MemPalace + Mem0 + CLAUDE.md  
**Conexão:** ver `gus-conceito-produto.md` e `gus-modelo-negocio.md`

---

## Por que Telegram primeiro

- Zero fricção — já instalado no celular
- Notificação nativa
- Recebe E responde pelo mesmo lugar
- Mais simples de construir que PWA
- O Painel do Gus entra depois, quando o Telegram começar a ser limitante

---

## Arquitetura V1.0

```
MemPalace + Mem0
        ↓
Gus (API Anthropic)
        ↓
Telegram Bot
        ↓
Seu celular
```

---

## PARTE 1 — Criar o Bot no Telegram (5 minutos)

1. Abre o Telegram e busca por `@BotFather`
2. Manda `/newbot`
3. Nome do bot: `Gus` ou `GusAGI`
4. Username: precisa terminar em `bot` — ex: `gus_pessoal_bot`
5. BotFather te dá um **token** — salva, é a chave do bot
6. Busca seu bot pelo username e manda `/start`
7. Acessa no browser:
   ```
   https://api.telegram.org/botSEU_TOKEN/getUpdates
   ```
8. Aparece seu **chat_id** — salva esse número também

**O que guardar:**
- Token do bot
- Seu chat_id pessoal

---

## PARTE 2 — Instalar dependências (2 minutos)

No PowerShell:
```
pip install python-telegram-bot anthropic mem0
```

---

## PARTE 3 — O Script do Gus

O Claude Code constrói isso por você numa sessão. O script tem três partes:

**3a — Receber mensagens:**
```
Você manda msg no Telegram
        ↓
Script recebe via webhook
        ↓
Passa para o Gus processar
```

**3b — Processar com contexto:**
```
Busca contexto no MemPalace
Carrega perfil do Mem0
Roteia para modelo certo
Chama API Anthropic
```

**3c — Responder e memorizar:**
```
Manda resposta no Telegram
Salva interação no Mem0
Atualiza contexto se necessário
```

---

## PARTE 4 — Roteamento de Modelos

O Gus decide sozinho qual modelo usar — invisível para você:

| Situação | Modelo | Motivo |
|---|---|---|
| Resposta simples, tarefa direta | Haiku | Barato, rápido |
| Conversa normal, uso geral | Sonnet | Equilibrado |
| Decisão complexa, análise profunda | Opus | Máxima capacidade |

Você nunca escolhe o modelo. O Gus roteia automaticamente.

---

## PARTE 5 — Mensagens Proativas (Scheduler)

O Windows Task Scheduler acorda o Gus 3x por dia:

**7h — Briefing da manhã:**
- Consulta MemPalace: pendências dos projetos
- Consulta Mem0: contexto pessoal, agenda
- Gera resumo curto (2-3 linhas)
- Manda no Telegram

**13h — Check do meio-dia:**
- Verifica projetos sem atualização recente
- Sugere próximo passo se relevante

**21h — Resumo do dia:**
- O que foi feito
- O que ficou pendente
- Prepara briefing de amanhã

**V1.0 — regras flexíveis:**
Manda sempre, sem filtro complexo. Você aprende o comportamento do Gus, o Gus aprende o seu. Aperta as regras nas versões seguintes.

**Evolução planejada:**
```
V1.0 — manda sempre, 3x por dia
V1.5 — você define quais tipos de msg quer
V2.0 — Gus aprende o que você responde vs ignora
V3.0 — Phronesis completa, julgamento autônomo
```

---

## PARTE 6 — Arquivo de Configuração

Um único `gus_config.json` — preenche uma vez, nunca mais mexe:

```json
{
  "telegram_token": "SEU_TOKEN",
  "telegram_chat_id": "SEU_CHAT_ID",
  "anthropic_key": "SUA_KEY",
  "mem0_key": "SUA_KEY",
  "mempalace_path": "C:/Users/Gustavo/Desktop/CLAUDE",
  "schedule": ["07:00", "13:00", "21:00"],
  "modelo_padrao": "claude-sonnet-4-6",
  "modelo_complexo": "claude-opus-4-6",
  "modelo_simples": "claude-haiku-4-5-20251001"
}
```

---

## Ordem de Execução

1. Criar bot no BotFather — você faz (5 min)
2. Salvar token e chat_id — você faz (2 min)
3. Rodar `pip install python-telegram-bot anthropic mem0`
4. Pedir pro Claude Code construir o script completo
5. Preencher `gus_config.json` com suas keys
6. Testar mandando "oi" pro bot
7. Configurar Task Scheduler para mensagens proativas

**Tempo total estimado:** 1 hora numa sessão direcionada com o Claude Code.

---

## Pré-requisitos antes de executar este guia

- [ ] MemPalace instalado e minerado ← em andamento
- [ ] MCP configurado no Claude Code
- [ ] Mem0 configurado com API key
- [ ] CLAUDE.md orquestrador montado
- [ ] Token do Telegram (BotFather)
- [ ] Chat_id pessoal

---

## Nota

A decisão de começar pelo Telegram em vez do Painel PWA veio da pergunta: "não seria mais fácil tentar pelo Telegram primeiro?" — sim, muito mais. O menor atrito possível para a V1.0 é o caminho certo. O Painel entra quando o Telegram começar a ser limitante.

O Gus pelo Telegram já resolve o problema original (tokens, contexto, memória) e adiciona proatividade — tudo antes de construir qualquer interface visual.
