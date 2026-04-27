---
tipo: demanda
origem: tiogu
destino: claude-code
prioridade: alta
status: concluido
criado_em: 2026-04-26T23:51:00-03:00
processado_em: 2026-04-27T09:12:33-03:00
processado_por: claude-code
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

## Resultado

Fix concluído em 3 commits encadeados — o que era 1 fix virou 3 conforme problemas adjacentes apareceram durante a validação.

### Commits

- `10a99eb` (2026-04-27 01:53 BRT) — `fix: pinnar qdrant-client<1.12.0 pra compatibilidade com mem0ai 0.1.29` — fix principal. Método `.search()` foi removido em qdrant-client 1.12, mas mem0ai 0.1.29 ainda usa.
- `b9d8f89` (2026-04-27 05:41 BRT) — `fix: criar índices Qdrant payload na init (user_id, agent_id, run_id)` — necessário pros filtros do `query_points` funcionarem.
- `9ff9c96` (2026-04-27 05:51 BRT) — `fix: workflow pra recriar coleção Qdrant com 384 dims + re-migrar` — ajuste de dimensão do embedder HuggingFace `all-MiniLM-L6-v2` (384 dims).

### Validação

- `_indices/_auditoria-mem0.md` (gerado 27/04 07:51 BRT) reporta 204 memórias ativas, mais recente 26/04 — leitura estava funcionando no momento da auditoria.
- Resposta original em `dialogos/inbox-tiogu/2026-04-27T00-30__fix-qdrant-search-bug-concluido.md`.
- Critério de sucesso textual da demanda (`search_memory(query="projetos Gustavo")` retorna memórias sem erro) **ainda pendente de teste end-to-end pelo Gustavo via Telegram**.

### Observação fiscal

Trabalho técnico concluído em ~7h (entre 01:53 e 05:51 BRT). Demanda foi marcada como concluída apenas agora (27/04 09:12 BRT) — frontmatter ficou desatualizado por ~3h após o último fix entrar em produção. Padrão a evitar: o destino precisa atualizar `status` e `processado_em` ao terminar, senão `archive-completed-demandas.yml` nunca move o arquivo.
