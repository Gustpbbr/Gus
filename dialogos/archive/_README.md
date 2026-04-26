# Archive — demandas concluídas

Pasta pra onde demandas processadas com sucesso são movidas (de qualquer
inbox-X).

## Por que existe

- Manter histórico de "o que cada porta processou"
- Auditoria: rastrear decisões e ações em retrospectiva
- Não poluir inboxes ativos com lixo concluído

## Convenção

Mantém o nome original do arquivo (`<timestamp>__<descricao>.md`). Se
necessário, pode prefixar com a inbox de origem pra clareza:

```
archive/inbox-tiogu__2026-04-25T23-50__teste.md
```

(Opcional. Sem prefixo também funciona — o frontmatter `processado_por`
já diz qual porta processou.)

## Limpeza

Não precisa limpar regularmente. Se virar gigante (>500 arquivos),
pode-se mover demandas com mais de 6 meses pra subpasta `archive/historico/`.
