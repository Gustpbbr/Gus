---
tipo: pasta-regras
sistema: fila-de-acoes
atualizado: 2026-04-24
---

# acoes/ — fila de ações a executar no mundo real

Esta pasta é o esqueleto do **Nível 4 (Autonomia)** do Gus. Aqui ficam **ações versionadas** que o bot enfileira quando o Gustavo pede pra executar algo no mundo real — mandar mensagem, enviar email, agendar evento, criar lembrete.

Atualmente **só a estrutura existe**. Os executores (Twilio pra WhatsApp, Gmail API pra email, Google Calendar pra agenda) ainda não estão implementados. Ações ficam em `pendentes/` esperando que um executor venha processar.

## Estrutura

```
acoes/
├── README.md                ← este arquivo
├── pendentes/               ← .md de ações aguardando execução
├── concluidas/              ← .md movidos pra cá depois de executadas
└── lembretes-ativos.md      ← placeholder pra lembretes recorrentes
```

## Formato de uma ação

Todo arquivo em `acoes/pendentes/<id>.md` segue este formato:

```markdown
---
id: 2026-04-24-143055-a7f3
tipo: whatsapp            # whatsapp | email | calendar | lembrete | nota
origem: telegram          # telegram | chatgpt | alexa | claude-code
criado_em: 2026-04-24T14:30:55-03:00
status: pendente          # pendente | aprovado | executado | falhou | cancelado
alto_risco: false         # true exige confirmação antes de executar
---

## Ação

<conteúdo específico por tipo>

## Contexto

<de onde veio, por que foi enfileirada>
```

## Tipos de ação

### `whatsapp`
```yaml
destinatario: mae
mensagem: "Chego 20h"
```

### `email`
```yaml
para: joao@clinica.com
assunto: "Confirmação plantão"
corpo: "João, confirmo o plantão de sábado..."
```

### `calendar`
```yaml
titulo: "Consulta endócrino"
data_inicio: 2026-05-15T14:00:00-03:00
data_fim: 2026-05-15T15:00:00-03:00
notas: ""
```

### `lembrete`
```yaml
quando: 2026-04-25T09:00:00-03:00
texto: "Tomar tapazol"
recorrente: diario      # nenhum | diario | semanal | mensal
```

### `nota`
```yaml
# Nota é basicamente um save_to_github diferente — formato reservado
# pra casos onde queremos a ação versionada mesmo sem side effect.
```

## Critérios pra `alto_risco: true`

Marcar quando:
- Envolve valor monetário (transferência, pagamento)
- Destinatário fora do mapeamento de contatos conhecidos
- Email pra domínio pessoal (não corporativo conhecido)
- Mensagem com palavras-gatilho ("urgente", "emergência", "confidencial")
- Ação irreversível (deletar, cancelar evento de terceiro)

Ações de alto risco **pausam em pendentes** e o executor (quando existir) avisa o Gustavo via Telegram pra confirmar antes.

## Fluxo esperado (quando executor existir)

```
Gustavo: "Gus, manda WhatsApp pra mãe dizendo que chego 20h"
    ↓
Bot chama criar_acao(tipo="whatsapp", conteudo=...)
    ↓
Arquivo em acoes/pendentes/<id>.md (com frontmatter status=pendente)
    ↓
GitHub Action dispara em push em acoes/pendentes/
    ↓
Executor lê o .md, chama Twilio, move pra concluidas/
    ↓
Bot envia no Telegram: "Mensagem pra mãe enviada ✓"
```

## Hoje (estado atual)

- `pendentes/` e `concluidas/` existem (com `.gitkeep` cada pra versionar)
- `lembretes-ativos.md` é placeholder
- Tool `criar_acao` no bot (gus/tools.py) enfileira em `pendentes/`
- **Não tem executor** — ações ficam paradas. Implementação depende de:
  - Conta Twilio + número aprovado (WhatsApp)
  - OAuth Gmail
  - Service Account Google Calendar
  - GitHub Action cron pra processar a fila

## Por que assim (e não execução direta)

1. **Auditabilidade** — cada ação é um commit. Git log vira histórico.
2. **Recuperação** — se Twilio cair, ação fica em pendentes e roda depois.
3. **Testabilidade** — executor pode rodar em dry-run antes de habilitar.
4. **Confirmação** — janela de cancelamento mesmo em baixo risco.
5. **Segurança** — handler do bot não precisa de credenciais Twilio/Gmail. Só o executor tem.

## Exclusão do Drive sync

A pasta `acoes/` **não está** na lista de excluded prefixes hoje. Se começar a conter dados sensíveis (números de telefone, emails pessoais), adicionar `acoes/` em `EXCLUDE_PREFIXES` do `sync_to_drive.py`. Alternativamente, ter uma pasta `sensivel/acoes/` pra casos que envolvem contatos privados.

Relacionado: [[gus-06-autonomia-acoes]] (plano completo), [[gus-04-seguranca-protecao]], [[gus-08-plano-proximos-passos]]
