---
tipo: demanda
origem: tiogu
destino: claude-code
prioridade: alta
status: pendente
criado_em: 2026-04-27T06:16:00-03:00
processado_em: ""
processado_por: ""
---

# Trocar Haiku por Sonnet na curadoria do Mem0

## Demanda
O modelo responsável pela curadoria automática de memórias (resumo extrativo a cada 3 turnos) deve ser trocado de **Claude Haiku** para **Claude Sonnet**.

## Contexto
Gustavo identificou que a qualidade da curadoria determina diretamente a qualidade do cérebro do Gus:

> "Uma curadoria boa vai dar um cérebro bom. Uma curadoria ruim vai levar a um cérebro ruim."

O Haiku é barato mas raso — perde nuances, não captura endereços, preferências sutis, decisões implícitas. O Sonnet tem profundidade analítica suficiente pra fazer curadoria de qualidade.

## Critério de sucesso
- O script/worker que roda a cada 3 turnos usa `claude-sonnet-*` (não `claude-haiku-*`) como modelo
- Custo aumenta levemente mas é aceitável dado o impacto na qualidade da memória
- Confirmar qual arquivo de código faz essa chamada e qual variável define o modelo
