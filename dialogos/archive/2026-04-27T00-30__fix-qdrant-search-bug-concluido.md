---
tipo: resposta
origem: claude-code
destino: tiogu
ref: 2026-04-26T23-51__fix-qdrant-search-bug
status: concluido
criado_em: 2026-04-27T00:30:00-03:00
---

# Fix concluído: bug `search_memory` após migração Qdrant

## O que era

`qdrant-client` 1.17.1 (versão instalada no Railway) removeu o método `.search()` na versão 1.12.0, substituindo por `.query_points()`. O `mem0ai 0.1.29` ainda usa `.search()` internamente — daí o erro.

## O que foi feito

`requirements.txt` atualizado:

```
# antes
qdrant-client>=1.9.0

# depois
qdrant-client>=1.9.1,<1.12.0
```

Isso força o Railway a instalar qdrant-client 1.11.x no próximo deploy, onde `.search()` ainda existe.

## Commit

`fix: pinnar qdrant-client<1.12.0 pra compatibilidade com mem0ai 0.1.29`

## Próximo passo

Railway vai fazer redeploy automático ao detectar o push em main. `search_memory` volta a funcionar assim que o container subir com a versão correta do qdrant-client.

Se quiser confirmar: manda uma mensagem no Telegram e pede pra buscar alguma memória ("o que você sabe sobre meus projetos?").
