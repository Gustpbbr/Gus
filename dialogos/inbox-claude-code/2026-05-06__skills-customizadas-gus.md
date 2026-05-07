---
tipo: demanda
origem: gustavo
destino: claude-code
prioridade: media
status: pendente
criado_em: 2026-05-06T21:30:00-03:00
processado_em: ""
processado_por: ""
acao_sugerida: implementar
destino_path: .claude/skills/
contexto: Criar skills customizadas do Gus para uso no Claude Code: /status-gus, /gerar-demanda, /auditar-curador.
---

# Skills customizadas do Gus

## Skills a criar

### `/status-gus`
Ao invocar: lê `git log --oneline -10`, `_indices/_auditoria-hub.md` e
`dialogos/inbox-claude-code/`. Produz painel em ~10 linhas: pendentes no
inbox, fragmentos no Hub, últimos commits, estado geral do sistema.

Elimina a necessidade de pedir esse contexto manualmente no início de cada sessão.

### `/gerar-demanda`
Usuário descreve o que quer em linguagem natural. Skill formata com frontmatter
correto (`tipo`, `origem`, `destino`, `prioridade`, `criado_em`) e salva em
`dialogos/inbox-claude-code/`. Elimina atrito de criar demandas no formato certo.

### `/auditar-curador`
Lê os últimos N fragmentos salvos pelo curador (filtrável por `curador=gpt`,
`curador=haiku`, etc.), avalia qualidade (vago? repetido? tipo errado?),
sugere deletes ou correções. Versão interativa do levantamento que está
o inbox como demanda hoje.

## Critério de sucesso

- `/status-gus` funciona no início de sessão sem argumentos extras
- `/gerar-demanda` cria arquivo com frontmatter válido e salva no lugar certo
- `/auditar-curador` lista fragmentos com análise de qualidade
