---
tipo: demanda
origem: gustavo
destino: claude-code
prioridade: baixa
status: pendente
criado_em: 2026-05-06T21:30:00-03:00
processado_em: ""
processado_por: ""
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
