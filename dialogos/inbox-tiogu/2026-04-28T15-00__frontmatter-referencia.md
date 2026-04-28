---
tipo: demanda
origem: claude-chat
destino: tiogu
prioridade: baixa
status: pendente
criado_em: 2026-04-28T15:00:00-03:00
processado_em: ""
processado_por: ""
acao_sugerida: criar_novo
destino_path: docs/exemplos/frontmatter-referencia.md
contexto: "Referencia de frontmatter valido para cada inbox do canal dialogos/"
---

# Referencia: Frontmatter por caixa de dialogo

Exemplos de frontmatter valido para cada inbox do canal dialogos/.
Campos obrigatorios: tipo, origem, destino, prioridade, status, criado_em.

---

## inbox-tiogu/ (Claude Chat -> TioGu)

```yaml
---
tipo: demanda
origem: claude-chat
destino: tiogu
prioridade: baixa
status: pendente
criado_em: 2026-04-28T14:00:00-03:00
processado_em: ""
processado_por: ""
acao_sugerida: criar_novo
destino_path: projetos/gus/algum-documento.md
contexto: "Frase curta descrevendo o que e e para onde vai (max 200 chars)"
---
```

Usado por: Claude Chat, Custom GPT (futuro), Gustavo manual.
TioGu le quando Gustavo pedir ou cron varre prioridade alta.

---

## inbox-claude-code/ (TioGu ou Gustavo -> Claude Code)

```yaml
---
tipo: demanda
origem: tiogu
destino: claude-code
prioridade: media
status: pendente
criado_em: 2026-04-28T14:00:00-03:00
processado_em: ""
processado_por: ""
acao_sugerida: criar_novo
destino_path: hub/nova-feature.py
contexto: "Implementar endpoint /hub/recent conforme spec em neurogus-arquitetura.md"
---
```

Usado por: TioGu (quando Gustavo pede via Telegram), Gustavo manual.
Claude Code le no inicio de sessao ou quando ativado.

---

## inbox-claude-chat/ (TioGu -> Claude Chat)

```yaml
---
tipo: demanda
origem: tiogu
destino: claude-chat
prioridade: baixa
status: pendente
criado_em: 2026-04-28T14:00:00-03:00
processado_em: ""
processado_por: ""
acao_sugerida: manter
destino_path: ""
contexto: "Resumo de conversa Telegram 28/04 para Claude Chat ler na proxima sessao"
---
```

Usado por: TioGu (deposita resumos e contexto para o Claude Chat recuperar).
Claude Chat le no boot do modo Gus (busca no Drive).

---

## inbox-custom-gpt/ (qualquer porta -> Custom GPT)

```yaml
---
tipo: demanda
origem: claude-chat
destino: custom-gpt
prioridade: baixa
status: pendente
criado_em: 2026-04-28T14:00:00-03:00
processado_em: ""
processado_por: ""
acao_sugerida: manter
destino_path: ""
contexto: "Config de voice prompt para Custom GPT mobile"
---
```

Usado por: qualquer porta. Custom GPT acessa via Actions REST (futuro).

---

## Valores validos por campo

| Campo            | Valores                                              |
|------------------|------------------------------------------------------|
| tipo             | demanda (unico valor aceito pelo workflow)           |
| origem           | claude-chat, tiogu, claude-code, custom-gpt, gustavo |
| destino          | tiogu, claude-code, claude-chat, custom-gpt          |
| prioridade       | alta, media, baixa                                   |
| status (criacao) | pendente                                             |
| status (depois)  | concluido, cancelado                                 |
| acao_sugerida    | criar_novo, append, mover, manter                    |

## Resultado
