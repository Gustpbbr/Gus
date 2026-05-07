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
destino_path: .github/scripts/
contexto: Evoluir workflows GitHub Actions de scripts determinísticos para agentes que raciocinam sobre o contexto antes de agir (Claude Agent SDK).
---

# Workflows GitHub Actions como agentes SDK

## Motivação

Hoje scripts como `auditoria_hub.py`, `briefing-matinal.py` e `reflexao_quinzenal.py`
são determinísticos — sempre fazem a mesma coisa, com o mesmo template. Um agente
no lugar receberia o objetivo e decidiria sozinho o que fazer: consultar o Hub,
ver fragmentos novos, adaptar o output ao contexto real do dia.

## O que implementar

1. Escolher 1 workflow como piloto (sugestão: `briefing-matinal.py` — output
   mais visível, fácil de comparar antes/depois)
2. Reescrever usando Claude Agent SDK com tool use em loop
3. Definir as tools disponíveis pro agente (read Hub, read GitHub, etc.)
4. Comparar qualidade do output vs versão atual por 1-2 semanas

## Critério de sucesso

Briefing gerado pelo agente é visivelmente mais adaptado ao dia real
do que o template atual. Custo de tokens dentro do aceitável.
