---
tipo: documentacao-projeto
projeto: gus
parte: 16-canal-unificado
atualizado: 2026-04-25T23:55-03:00
---

# Canal unificado entre portas — design rationale

Documento de arquitetura que justifica a estrutura de `dialogos/` e o fluxo
de demandas assíncronas entre as portas do Gus.

> Implementado em 25/04/2026 noite. Substitui o `dialogos-tiogu-claude/`
> que era específico do par Telegram↔Claude Code.

---

## Problema original

Antes desta implementação, cada porta do Gus tinha seu jeito próprio de
"comunicar" com as outras:

| Par | Mecanismo |
|---|---|
| TioGu ↔ Claude Code | Pasta `dialogos-tiogu-claude/`, formato cronológico semanal |
| TioGu ↔ Mem0 | Direto via API |
| Claude Code ↔ Mem0 | Direto via MCP |
| Custom GPT ↔ tudo | Direto via FastAPI nossa |
| Claude Chat ↔ tudo | **Apenas Drive (read+write)**, sem ponte automática pro GitHub |

Resultado: **Claude Chat decidia algo importante numa conversa longa, mas pra virar
ação noutra porta o Gustavo tinha que copy-paste manualmente** (mensageiro entre
canais). Não escalava.

## Decisão

Criar **canal único** com 3 propriedades:

1. **Single source of truth no GitHub**: pasta `dialogos/` no repo.
2. **Drive como porta de entrada da Claude Chat**: workflow `import-from-drive.yml`
   puxa a cada 15min do `Gus-Sync/dialogos/inbox-*/` e commita no GitHub.
3. **Inboxes por destinatário**: não por par origem-destino (evita explosão
   combinatória N×N).

## Arquitetura

```
                       ┌──────────────────┐
                       │ Gustavo decide   │
                       │ algo numa porta  │
                       └────────┬─────────┘
                                │
        ┌───────────┬───────────┼───────────┬───────────┐
        ▼           ▼           ▼           ▼           ▼
    TioGu      Claude       Claude       Custom      Gustavo
    Telegram    Code         Chat         GPT        manual
        │           │           │           │           │
        │           │           ▼           │           │
        │           │      Cria arquivo     │           │
        │           │      no Drive em      │           │
        │           │      Gus-Sync/        │           │
        │           │      dialogos/        │           │
        │           │      inbox-X/         │           │
        │           │           │           │           │
        │           │           ▼           │           │
        │           │      [import-from-    │           │
        │           │      drive.yml]       │           │
        │           │      cron 15min       │           │
        │           │           │           │           │
        │           │           ▼           │           │
        ▼           ▼           ▼           ▼           ▼
        ┌─────────────────────────────────────────────┐
        │   GitHub: dialogos/inbox-<destino>/        │
        │   (single source of truth)                 │
        └────────────────────┬───────────────────────┘
                             │
        ┌───────────┬────────┴────────┬───────────┐
        ▼           ▼                 ▼           ▼
    TioGu      Claude              Claude      Custom
    lê seu     Code lê             Chat lê     GPT lê
    inbox      seu inbox           inbox       inbox
    quando     no SessionStart     quando      quando
    ativar     de cada sessão      bootstrap   pedir
                                   pedir
```

## Por que inboxes por destinatário (e não por par)

Se fosse por par origem→destino, teríamos N×N pastas (16 com 4 portas, 25 com 5).
Por destinatário, são **N pastas** (4 hoje, 5 com Alexa).

Vantagem adicional: **destino lê só sua pasta**. TioGu não precisa filtrar "demandas pra
mim" — toda demanda em `inbox-tiogu/` é pra ele. Simplicidade operacional.

## Por que NÃO escolhi outras opções

### Stream único linear (`dialogos/2026-04-25.md`)

Pareceu elegante (linha do tempo unificada), mas:
- Contenção de escrita simultânea (TioGu e Custom GPT escrevendo ao mesmo tempo)
- Cada destino precisaria varrer arquivo inteiro pra achar suas demandas
- Histórico vira monolito difícil de auditar

Mantido como **legado em `streams/`** pra continuidade do passado, mas não é o futuro.

### Mem0 como canal universal

Tentador (já existe, infra pronta), mas:
- Mem0 é semantic search, não fila ordenada
- Difícil "processar próxima pendente"
- Claude Chat não tem acesso live ao Mem0 (deal-breaker)

### Auto-execução sem revisão (Nível 3 do plano original)

Adiado: vira "agente autônomo" e perde reversibilidade. V1 mantém Gustavo
no loop pra revisar antes de executar (cada porta processa seu inbox quando
Gustavo ativar).

## Caveats conhecidos

| Caveat | Mitigação |
|---|---|
| Latência média 7.5min do import (cron 15min) | Aceitável pra V1; baixar pra 5min se virar dor real |
| Drive integration do Claude Chat pode ficar fora do ar | Fallback: Claude Chat usa bloco copy-paste pro Gustavo, manual |
| Frontmatter mal formatado quebra import | Workflow loga erro, arquivo fica no Drive intacto, Gustavo corrige |
| Demanda de alta prioridade pode esperar até 15min | Notificação Telegram quando importa em `inbox-tiogu/` mitiga |
| Custom GPT depende da Action configurada (mobile não tem) | Não bloqueia esse design — quando ativar, lê `inbox-custom-gpt/` |
| Auto-execução desabilitada | Por design no V1; futuro pode habilitar com guardrails |

## Decisões técnicas explícitas

- **Cron 15min** (não 5min): equilibra latência vs custo GH Actions free tier
- **`contents: write`** no workflow: necessário pro commit; aceito o risco (script é controlado)
- **Mover arquivo no Drive pra `processados/`** após import: garante idempotência sem precisar
  diff complexo
- **Notificação Telegram só pra `inbox-tiogu`**: outras portas não têm canal de "ping"
  (pode evoluir)
- **Frontmatter inválido = skip + log**: forçar disciplina, não importar lixo

## Próximos passos potenciais (não implementados V1)

- **Cron 5min** se latência virar problema real
- **Notificação Telegram pra outras inboxes** (ex: avisar quando demanda chega
  em `inbox-claude-code/` pra Gustavo abrir sessão)
- **Auto-execução opcional** com flag `execucao_automatica: true` no frontmatter
  (Nível 3 — só depois de Gustavo confiar no padrão)
- **Métrica de latência**: workflow loga tempo entre `criado_em` e import,
  exporta como métrica
- **Dedup**: detectar demandas duplicadas (mesmo título recente)
- **Webhook Drive**: trocar polling cron por push notification (mais complexo,
  baixar latência pra ~segundos)

## Arquivos relacionados

- `dialogos/README.md` — protocolo operacional (frontmatter, regras)
- `dialogos/_bootstrap/gus-bootstrap.md` — instruções pra Claude Chat usar o canal
- `.github/workflows/import-from-drive.yml` — workflow do polling
- `.github/scripts/import_from_drive.py` — lógica de import
- `projetos/gus/gus-12-portas-futuras.md` — taxonomia de portas
- `projetos/gus/gus-13-tags-canonicas.md` — tags `via` no Mem0 (mesma taxonomia)

Relacionado: [[gus-12-portas-futuras]], [[gus-13-tags-canonicas]], [[gus-15-claude-chat-setup]]
