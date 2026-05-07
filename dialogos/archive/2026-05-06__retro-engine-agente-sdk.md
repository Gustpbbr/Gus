---
tipo: demanda
origem: gustavo
destino: claude-code
prioridade: baixa
status: concluido
criado_em: 2026-05-06T21:30:00-03:00
processado_em: "2026-05-07T00:00:00-03:00"
processado_por: claude-code
acao_sugerida: implementar
destino_path: .claude/hooks/retro_engine.py
contexto: Reescrever Retro Engine como agente SDK que filtra ruído do transcript, decide quando extrair e pode rodar em PostToolUse além do Stop.
---

# Retro Engine como agente SDK

## Problema atual

Retro Engine (`retro_engine.py`) extrai zero fragmentos em todas as sessões.
Causa raiz: transcript JSONL está cheio de tool outputs e resultados de bash —
o Haiku vê ruído em vez de conversa. Prompt muito restritivo também contribui.

## Proposta com SDK

1. **Filtrar transcript**: extrair só turnos `user` e `assistant` de texto real,
   ignorar blocos `tool_use` e `tool_result`
2. **Decidir relevância**: agente verifica se a sessão tem decisões, aprendizados
   ou marcos antes de chamar Haiku (evita custo em sessões triviais)
3. **Extração por fragmento**: raciocinar sobre cada candidato individualmente
4. **PostToolUse rolling window**: rodar a cada 7 mensagens além do Stop,
   capturando insights enquanto a sessão ainda está quente

## Resultado esperado

Retro Engine começa a extrair fragmentos autobiográficos reais das sessões
Claude Code — resolvendo o "buraco fundo" documentado no próprio docstring
do hook desde a criação.

## Implementado em

Branch `claude/review-project-structure-esL3J` — commit `ad86e5e`.
Fixes no `retro_engine.py`:
- Parser reescrito: filtra só `type=user/assistant`, ignora continuation summaries injetados
- Truncação prioriza fim da sessão em vez de início+fim
- Loop tool use Haiku: `registrar_fragmento` (por fragmento) + `sessao_trivial`
- Extração estruturada via tool schema, sem parsing de JSON livre
