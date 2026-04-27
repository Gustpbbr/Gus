---
tipo: demanda
origem: tiogu
destino: claude-code
prioridade: alta
status: pendente
criado_em: 2026-04-26T23:51:00-03:00
processado_em: ""
processado_por: ""
---

# Fix urgente: bug no `search_memory` após migração Qdrant

## Problema

Após a migração Mem0 Cloud → Qdrant de hoje, o método de busca está quebrado. Erro exato:

```
'QdrantClient' object has no attribute 'search'
```

A API do Qdrant usa `.query_points()` (ou similar) em vez de `.search()`. O código ainda está chamando o método antigo.

## Impacto

Crítico — sem busca, o Gus não consegue acessar nenhuma memória sobre o Gustavo via `search_memory`. O coração do sistema está inoperante.

## O que fazer

1. Identificar onde `.search()` está sendo chamado no código (provavelmente `gus/mem0_client.py` ou similar)
2. Substituir pelo método correto da API Qdrant atual
3. Testar com uma query simples ("projetos Gustavo") e confirmar retorno
4. Deploy + confirmar que `search_memory` volta a funcionar

## Critério de sucesso

`search_memory(query="projetos Gustavo")` retorna memórias sem erro.

## Contexto

- Migração feita hoje ~20:30, commits entre 17:30–18:09
- Qdrant Cloud (GCP Virginia, free tier)
- O Gustavo quer ser avisado **diretamente no Telegram** quando estiver resolvido
- Quando concluir, salvar resultado em `dialogos/inbox-tiogu/` com status do fix
