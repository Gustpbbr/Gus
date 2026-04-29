---
tipo: referencia
fonte: dialogos
versao: 1.0
atualizado_em: 2026-04-28
---

# Frontmatter de demandas — referência

Toda demanda em `dialogos/inbox-*/` precisa de frontmatter YAML válido. Sem
frontmatter ou com campos obrigatórios faltando, o cron `import-from-drive`
rejeita o arquivo e move pra `dialogos/processados-erro/<inbox>/` no Drive.

> **MANTER SINCRONIZADO** — existem cópias deste arquivo em 5 lugares:
> - `dialogos/_frontmatter-referencia.md` (raiz, fonte canônica)
> - `dialogos/inbox-tiogu/_frontmatter-referencia.md`
> - `dialogos/inbox-claude-code/_frontmatter-referencia.md`
> - `dialogos/inbox-claude-chat/_frontmatter-referencia.md`
> - `dialogos/inbox-custom-gpt/_frontmatter-referencia.md`
>
> Ao adicionar/remover/renomear campo: atualizar **todas as 5 cópias** + o
> validator em `.github/scripts/import_from_drive.py` (função
> `validate_frontmatter`) + a constante `PORTAS_VALIDAS` se afetar origem/destino.
>
> **Convenção do prefixo `_`:** arquivos em `inbox-*/` cujo nome começa com `_`
> são tratados como **referência/doc**, não como demanda. O cron
> `import-from-drive` pula validação de frontmatter pra eles (modo mirror).
> Mesmo padrão de `_README.md` em cada inbox.

## Campos obrigatórios

`tipo`, `origem`, `destino`, `prioridade`, `status`, `criado_em`.

Demais campos (`processado_em`, `processado_por`, `acao_sugerida`,
`destino_path`, `contexto`) são opcionais mas convenção.

---

## Exemplos por inbox

### inbox-tiogu/ (Claude Chat → TioGu)

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
contexto: "Frase curta descrevendo o que é e pra onde vai (máx 200 chars)"
---
```

Usado por: Claude Chat, Custom GPT (futuro), Gustavo manual.
TioGu lê quando Gustavo pede ou cron varre prioridade alta.

---

### inbox-claude-code/ (TioGu ou Gustavo → Claude Code)

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
Claude Code lê no início de sessão ou quando ativado.

---

### inbox-claude-chat/ (TioGu → Claude Chat)

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
contexto: "Resumo de conversa Telegram 28/04 pra Claude Chat ler na próxima sessão"
---
```

Usado por: TioGu (deposita resumos e contexto pro Claude Chat recuperar).
Claude Chat lê no boot do modo Gus (busca no Drive).

---

### inbox-custom-gpt/ (qualquer porta → Custom GPT)

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
contexto: "Config de voice prompt pro Custom GPT mobile"
---
```

Usado por: qualquer porta. Custom GPT acessa via Actions REST (futuro).

---

## Valores válidos por campo

| Campo            | Valores aceitos                                      |
|------------------|------------------------------------------------------|
| `tipo`           | `demanda` (único valor aceito pelo workflow)         |
| `origem`         | `claude-chat`, `tiogu`, `claude-code`, `custom-gpt`, `gustavo` |
| `destino`        | `tiogu`, `claude-code`, `claude-chat`, `custom-gpt`  |
| `prioridade`     | `alta`, `media`, `baixa`                             |
| `status` (criação) | `pendente`                                         |
| `status` (depois)  | `concluido`, `cancelado`                           |
| `acao_sugerida`  | `criar_novo`, `append`, `mover`, `manter`            |

Regra adicional: `origem != destino` (sem sentido enfileirar pra si mesma).

---

## Onde é validado

- Workflow: `.github/workflows/import-from-drive.yml` (cron 15min)
- Script: `.github/scripts/import_from_drive.py`
- Função: `validate_frontmatter(fm, file_name)` — retorna lista de erros, vazia se OK
- Falha → arquivo movido pra `Gus-Sync/dialogos/processados-erro/<inbox>/` no Drive (PR #22)

## Histórico

| Versão | Data | Mudança |
|---|---|---|
| 1.0 | 2026-04-28 | Versão inicial — 5 cópias canonicalizadas, sync manual |
