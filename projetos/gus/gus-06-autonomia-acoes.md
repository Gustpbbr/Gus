---
criado_em: 2026-04-18
tipo: documentacao-projeto
status: planejado
fase: 4
---

# Gus — Autonomia e Fila de Ações (Fase 4)

Sistema para o Gus executar ações no mundo real a partir de comandos de voz ou texto.

## Conceito

Gustavo está no carro, falando com o ChatGPT (Kai), e diz:
> "Manda um WhatsApp pra minha mãe falando que chego às 20h"

O GPT não consegue mandar WhatsApp diretamente. Mas pode:
1. Criar um arquivo em `acoes/pendentes/` no GitHub
2. Um executor (GitHub Action ou bot) processa a ação
3. A ação é executada e movida para `acoes/concluidas/`

## Arquitetura

```
Voz/Texto → ChatGPT/Claude → GitHub (acoes/pendentes/) → Executor → Ação real
                                                              ↓
                                                     acoes/concluidas/
```

### Estrutura de pastas
```
acoes/
├── pendentes/         ← ações aguardando execução
│   └── 2026-04-18-whatsapp-mae.md
├── concluidas/        ← ações já executadas
│   └── 2026-04-18-whatsapp-mae.md
└── falhas/            ← ações que falharam
    └── 2026-04-18-email-clinica.md
```

### Formato do arquivo de ação
```yaml
---
tipo: whatsapp
destinatario: Mãe
prioridade: normal
criado_em: 2026-04-18T15:30:00
via: chatgpt
status: pendente
---

Mensagem: "Oi mãe, chego às 20h hoje. Beijo!"
```

## Tipos de ação suportados (planejados)

| Tipo | Canal | Como executar |
|------|-------|---------------|
| whatsapp | WhatsApp Business API ou Twilio | API call do executor |
| email | Gmail API | Google Workspace API |
| calendar | Google Calendar | Calendar API (já planejado na Fase 3) |
| lembrete | Telegram | Bot manda mensagem no horário |
| compra | Lista de compras | Salva em .md + notifica |
| nota | GitHub | Salva .md direto (já funciona) |

## Executor

### Opção A: GitHub Action (cron)
- Roda a cada 5-15 minutos
- Lê `acoes/pendentes/`
- Processa cada ação pelo tipo
- Move para `concluidas/` ou `falhas/`
- Simples, mas delay de até 15 minutos

### Opção B: Worker no Railway
- Processo separado do bot, rodando 24/7
- Monitora pasta via GitHub webhooks ou polling
- Execução quase imediata
- Mais complexo, mais custo

### Recomendação
Começar com GitHub Action (Opção A). Se o delay for problema, migrar para worker.

## Fluxo completo (exemplo)

1. Gustavo no carro: "Kai, manda WhatsApp pra minha mãe que chego às 20h"
2. ChatGPT (Custom GPT com Actions) cria arquivo via GitHub API:
   - Path: `acoes/pendentes/2026-04-18-whatsapp-mae.md`
   - Conteúdo: tipo whatsapp, destinatário Mãe, mensagem
3. GitHub Action detecta novo arquivo (cron ou push trigger)
4. Executor lê o arquivo, identifica tipo "whatsapp"
5. Chama Twilio/WhatsApp Business API com a mensagem
6. Move arquivo para `acoes/concluidas/`
7. Opcionalmente notifica Gustavo via Telegram: "WhatsApp enviado pra Mãe ✓"

## Pré-requisitos

- [ ] Custom GPT funcionando (Fase 3)
- [ ] APIs configuradas (Twilio, Gmail, Calendar)
- [ ] Contatos mapeados (mãe = +55..., clínica = email@...)
- [ ] Executor implementado (Action ou worker)

## Considerações de segurança

- Ações envolvem comunicação real — confirmar antes de executar?
- Opção: ações de "baixo risco" (lembrete, nota) executam direto; "alto risco" (WhatsApp, email) pedem confirmação via Telegram
- Rate limit: máximo N ações por hora
- Log completo de todas as ações executadas

Relacionado: [[gus-05-portas-capacidades]], [[gus-01-visao-geral]], [[gus-07-decisoes-descartadas]]
