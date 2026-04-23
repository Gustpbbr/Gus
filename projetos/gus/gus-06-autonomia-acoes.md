---
tipo: documentacao-projeto
projeto: gus
parte: 6-de-7
atualizado: 2026-04-23
---

# Gus — Autonomia e fila de ações (Fase 4)

Até aqui o Gus responde, busca e salva. Fase 4 adiciona capacidade de **executar ações no mundo real** sob comando — mandar WhatsApp, disparar email, criar evento, ativar lembrete.

O risco cresce. O design aqui prioriza **auditabilidade e confirmação** em cima de velocidade.

## Fluxo base: fila de ações

```
Gustavo (Telegram, ChatGPT voz, Alexa)
   ↓
Gus cria arquivo em acoes/pendentes/<id>.md
   ↓
GitHub Action dispara em push em acoes/pendentes/
   ↓
Executor lê o .md, executa a ação, move para acoes/concluidas/
   ↓
Notifica Gustavo no Telegram com resultado + link
```

Cada ação é **um arquivo versionado**. Histórico completo fica no git. Nada é silencioso.

## Formato do arquivo de ação

```yaml
---
id: 2026-04-23-143055-a7f3
tipo: whatsapp            # whatsapp | email | calendar | lembrete | nota
origem: telegram          # telegram | chatgpt | alexa | claude-code
criado_em: 2026-04-23T14:30:55-03:00
status: pendente          # pendente | aprovado | executado | falhou | cancelado
alto_risco: false         # true exige confirmação antes de executar
---

## Ação

destinatario: mãe
mensagem: "Oi mãe, chego 20h pro jantar"

## Contexto

Gustavo no carro perguntou via ChatGPT voz: "manda msg pra mãe dizendo que chego 20h".
```

## Tipos de ação na Fase 4

### 1. WhatsApp (via Twilio API)

- Requer número Twilio + template aprovado (WhatsApp Business não permite mensagem livre sem template pré-aprovado para destinatários novos).
- Funciona sem template pra contatos que já responderam nas últimas 24h.
- Custo: ~US$0,005 por mensagem.

### 2. Email (Gmail API via OAuth)

- Escopo `gmail.send`, sem leitura.
- Assinatura automática "enviado pelo Gus a pedido de Gustavo".
- Sempre `from: gustavo@...`, nunca domínio próprio.

### 3. Google Calendar — já mapeado em [[gus-05-portas-capacidades]]

Aqui entra `create_event` como tipo de ação com confirmação.

### 4. Lembrete (proativo interno)

- Salva em `acoes/lembretes-ativos.md` com timestamp de disparo.
- GitHub Action cron a cada 15min verifica e dispara os vencidos.
- Dispara mensagem no Telegram com o texto do lembrete.

### 5. Nota

- Só cria `.md` no GitHub. Já existe via `save_to_github`, mas entra aqui como tipo de ação para unificar fluxo.

## Confirmação de ações de alto risco

Critério para marcar `alto_risco: true`:

- Valor monetário envolvido (ex: "transfere R$X")
- Destinatário fora do mapeamento de contatos conhecidos
- Email para domínio pessoal do destinatário (não corporativo listado)
- Mensagem com palavras-gatilho ("urgente", "emergência", "confidencial")
- Ação irreversível (deletar arquivo, cancelar evento de terceiro)

Se `alto_risco: true`, o executor pausa em `status: pendente` e manda no Telegram:

```
Gus: Ação de alto risco aguardando confirmação.

[Resumo]
Enviar WhatsApp pra "Fulano (+55...)" dizendo "transfere 5k"

Responde "confirma" pra executar, "cancela" pra descartar.
```

Sem confirmação em 1h, ação vai automática para `cancelado`.

## Mapeamento de contatos

Arquivo `contatos/mapa.md` (único, não publicado no Drive sync — adicionar à exclusão do workflow):

```
---
tipo: mapa-contatos
atualizado: 2026-04-23
---

- mãe → WhatsApp +55 XX XXXX-XXXX
- pai → WhatsApp +55 XX XXXX-XXXX
- clínica-dimagem → email contato@...
- endócrino → WhatsApp +55 XX XXXX-XXXX
```

O Gus consulta esse arquivo quando a ação menciona nome de contato. Se o nome não bate exatamente, pergunta — nunca adivinha.

**Importante:** esse arquivo **não** vai pro Drive sync. Adicionar `contatos/` à lista `EXCLUDE_PREFIXES` em `.github/scripts/sync_to_drive.py`.

## Log completo de ações

Além do git (que versiona os `.md`), todo resultado de execução vai para `logs/acoes.jsonl`:

```json
{"timestamp":"2026-04-23T14:31:08-03:00","id":"2026-04-23-143055-a7f3","tipo":"whatsapp","status":"executado","destinatario":"mãe","custo_usd":0.005,"latencia_s":1.2}
```

Relatório semanal pode resumir: quantas ações por tipo, falhas, custo acumulado.

## Caso de uso canônico — o carro

```
Gustavo no carro: "Alexa, pergunta pro Gus pra avisar a mãe que chego 20h"
         ↓
Alexa Skill → Lambda → Claude API + contatos/mapa.md
         ↓
Claude gera ação:
  tipo: whatsapp
  destinatario: mãe
  mensagem: "Oi mãe, chego 20h pro jantar"
  alto_risco: false
         ↓
Lambda salva acoes/pendentes/2026-04-23-143055-a7f3.md
         ↓
GitHub Action dispara, Twilio envia, move para acoes/concluidas/
         ↓
Telegram: "Mensagem pra mãe enviada ✓"
```

Gustavo não tirou a mão do volante.

## Por que fila e não execução direta

1. **Auditabilidade** — cada ação é um commit. Git log vira histórico de "o que o Gus fez".
2. **Recuperação** — se Twilio cair, a ação fica em pendente e roda quando voltar.
3. **Testabilidade** — dá pra simular o executor em dry-run antes de habilitar.
4. **Confirmação** — permite janela de cancelamento mesmo em ações de baixo risco.
5. **Segurança** — o handler do Alexa/ChatGPT não precisa de credenciais do Twilio/Gmail. Só o executor (GitHub Action com secrets) tem.

## Pré-requisitos antes de começar Fase 4

- Custom GPT funcionando (valida arquitetura Mem0+GitHub via API externa)
- Fase 2 completa (scan de dados sensíveis, rate limiting, backup Mem0)
- `contatos/mapa.md` criado manualmente e excluído do sync Drive

Sem esses três, o risco de dano excede o benefício.

Relacionado: [[gus-05-portas-capacidades]], [[gus-04-seguranca-protecao]], [[gus-07-decisoes-descartadas]]
