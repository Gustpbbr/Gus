---
tipo: lembretes
atualizado: 2026-04-24
---

# Lembretes ativos

Lista de lembretes recorrentes ou agendados que o Gus deve disparar.

Formato:

```yaml
- id: 2026-04-24-lembrete-tapazol
  texto: Tomar tapazol
  quando: 2026-04-25T09:00:00-03:00
  recorrente: diario         # nenhum | diario | semanal | mensal
  ativo: true
```

**Estado atual:** placeholder. Nenhum lembrete configurado ainda. Quando a fila de ações tiver executor, lembretes tipo `recorrente: diario` são verificados por um cron do GitHub Actions e disparam mensagens no Telegram.

## Regras de manutenção

- Cada lembrete é um bloco YAML separado
- Quando `ativo: false`, lembrete pausa sem apagar
- Histórico de lembretes antigos vai pra `concluidas/` com data de última execução no frontmatter
- Bot pode listar, criar, desativar lembretes via conversa (ação tipo `lembrete`)
