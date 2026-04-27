---
tipo: demanda
origem: tiogu
destino: claude-code
prioridade: alta
status: concluido
criado_em: 2026-04-27T06:16:00-03:00
processado_em: 2026-04-27T19:50:00-03:00
processado_por: claude-code
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

## Resolução

**Resolvida (superada) — Fase 2 do ADR-001 implementou solução melhor que a pedida.**

Em vez de trocar Haiku por Sonnet (perda de informação — assume sem evidência que Sonnet é melhor), foi implementado **curador híbrido dual** nas PRs #5/#6/#7:

- `hub/curador.py:269-270` — Haiku 4.5 e Sonnet 4.6 rodam **em paralelo** sobre o mesmo trecho de turnos (`asyncio.gather`)
- Cada modelo extrai fragmentos atômicos seguindo schema gus-18 (tipo / camada_temporal / area)
- Ambos salvam no Hub Qdrant com `metadata.curador="haiku"` ou `"sonnet"` distinto, mas mesmo `hash_janela` (sha8 do trecho-fonte)
- Mesmo `hash_janela` permite parear lado a lado no Obsidian em `_log/resumos-mem0/AAAA-MM-DD.md` (uma entrada por curador, mesmo hash visível) → comparação direta de qualidade

**Por que isso é superior:**

1. Coleta evidência durante 14 dias (até 2026-05-12) antes de decidir o modelo final — decisão por dado, não por palpite
2. Custo ~2× durante coleta, mas é fixo e pequeno (~US$0.15/dia max). Após decisão, fica só um dos dois
3. Se Sonnet for melhor → mantém só Sonnet (custo do worker volta pro nível original)
4. Se Haiku for "bom o suficiente" pra captura grossa → mantém Haiku no fluxo automático e usa Sonnet só pra reprocessamento profundo de ingestão de chats (que é exatamente o que o `dialogos/streams/curador-chat-ingest.md` Fase 2.5 faz)
5. Se forem comparáveis → ganha o mais barato

**Arquivos relevantes:**

- `hub/curador.py` — implementação dual (linhas 250–340)
- `hub/store.py` — `ingestar(... metadata={"curador": ...})` salva no Qdrant
- `gus/bot.py:_resumir_e_salvar` — chama `hub.curador.curar_turnos` no lugar do antigo `gerar_resumo_turnos` Mem0
- `_log/resumos-mem0/AAAA-MM-DD.md` — append-only com 1 entrada por curador, mesmo hash_janela visível

**Variáveis de ambiente (Railway):**

- `MODEL_CURADOR_HAIKU=claude-haiku-4-5` (default)
- `MODEL_CURADOR_SONNET=claude-sonnet-4-6` (default)

Decisão final do modelo único fica na **Fase 5 do ADR-001** (após coleta de 14 dias).
