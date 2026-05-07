---
tipo: demanda
origem: gustavo
destino: claude-code
prioridade: baixa
status: pendente
criado_em: 2026-05-06T21:30:00-03:00
processado_em: ""
processado_por: ""
acao_sugerida: investigar
destino_path: hub/curador.py
contexto: Evoluir curador para processar fragmentos individualmente com raciocínio por fragmento — consulta Hub antes de salvar, evita duplicatas e fragmentos vagos.
---

# Curador com raciocínio por fragmento (Agent SDK)

## Motivação

O curador atual (`hub/curador.py`) manda bloco de turnos pra Haiku + Sonnet e
pede extração holística. Resultado: fragmentos vagos passam (ex: MGX errado
identificado em 03/05), duplicatas entram sem filtro, tipo é estimado sem
contexto do que já existe no Hub.

## Proposta

Curador agêntico por fragmento:
1. Extrai candidatos (como hoje)
2. Para cada candidato, consulta Hub: "já existe algo parecido?"
3. Se duplicata → descarta ou atualiza
4. Se conteúdo vago → refina ou descarta
5. Define tipo/camada com base no contexto real, não só no texto

## Trade-off

Mais chamadas à API, mais latência. Aceitável pra memória de longo prazo
(roda assíncrono, não bloqueia bot). Ganho: Hub com muito menos ruído.

## Pré-requisito

Fase de saneamento do Hub (1.7 — limpeza ativa) deve estar concluída
para não contaminar a base de comparação.
