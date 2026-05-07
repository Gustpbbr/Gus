---
tipo: referencia
fonte: dialogos
versao: 1.0-gpt-chat
atualizado_em: 2026-05-05
---

# Frontmatter de demandas — referência

Toda demanda em `dialogos/inbox-*/` precisa de frontmatter YAML válido. Sem
frontmatter ou com campos obrigatórios faltando, o cron `import-from-drive`
rejeita o arquivo e move pra `dialogos/processados-erro/<inbox>/` no Drive.

> **MANTER SINCRONIZADO** — este arquivo segue o mesmo formato das referências
> existentes nos demais inboxes:
> - `dialogos/_frontmatter-referencia.md` (raiz, fonte canônica)
> - `dialogos/inbox-tiogu/_frontmatter-referencia.md`
> - `dialogos/inbox-claude-code/_frontmatter-referencia.md`
> - `dialogos/inbox-claude-chat/_frontmatter-referencia.md`
> - `dialogos/inbox-custom-gpt/_frontmatter-referencia.md`
> - `dialogos/inbox-gpt-chat/_frontmatter-referencia.md`
>
> Ao adicionar/remover/renomear campo: atualizar todas as cópias + o
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

### inbox-gpt-chat/ (qualquer porta → GPT Chat)

```yaml
---
tipo: demanda
origem: gustavo
destino: gpt-chat
prioridade: baixa
status: pendente
criado_em: 2026-05-05T10:00:00-03:00
processado_em: ""
processado_por: ""
acao_sugerida: manter
destino_path: ""
contexto: "Contexto breve para a porta GPT Chat analisar, revisar ou planejar na próxima sessão"
---
```

Usado por: Gustavo manualmente, Claude Code, Claude Chat, TioGu ou Custom GPT quando quiserem deixar uma demanda de análise, revisão, planejamento ou síntese para a porta GPT Chat.

---

## Valores válidos por campo

| Campo            | Valores aceitos                                      |
|------------------|------------------------------------------------------|
| `tipo`           | `demanda` (único valor aceito pelo workflow)         |
| `origem`         | `claude-chat`, `tiogu`, `claude-code`, `custom-gpt`, `gpt-chat`, `gustavo` |
| `destino`        | `tiogu`, `claude-code`, `claude-chat`, `custom-gpt`, `gpt-chat` |
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
- Falha → arquivo movido pra `Gus-Sync/dialogos/processados-erro/<inbox>/` no Drive

## Histórico

| Versão | Data | Mudança |
|---|---|---|
| 1.0-gpt-chat | 2026-05-05 | Cópia adaptada para `inbox-gpt-chat/` |
