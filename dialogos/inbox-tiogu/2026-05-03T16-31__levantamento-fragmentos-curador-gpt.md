---
tipo: demanda
origem: claude-chat
destino: claude-code
prioridade: alta
status: pendente
criado_em: 2026-05-03T16:31:00-03:00
processado_em: ""
processado_por: ""
acao_sugerida: listar todos os fragmentos com curador=gpt nos brains gustavo e gus, gerar relatório
destino_path: dialogos/inbox-claude-code/
contexto: Gustavo quer auditar a qualidade dos fragmentos gerados pelo curador GPT após identificar pelo menos um fragmento incorreto sobre MGX (UUID 0329c718). Suspeita de que há outros com problemas similares (conteúdo vago, impreciso ou errado).
---

# Levantamento de todos os fragmentos com curador=gpt

## O que fazer

1. Buscar no Hub Qdrant (brains `gustavo` e `gus`) todos os fragmentos onde `curador=gpt`
2. Gerar relatório com:
   - Total de fragmentos com `curador=gpt` em cada brain
   - Lista completa: UUID, tipo, área, conteúdo, criado_em, via
   - Se possível, comparar com fragmentos `curador=haiku` do mesmo período para avaliar diferença de qualidade
3. Salvar relatório em `Gus-Sync/projetos/gus/` com nome `gus-auditoria-curador-gpt-AAAA-MM-DD.md`

## Motivação

Curador GPT gerou pelo menos um fragmento errado identificado por Gustavo (MGX como "metodologia passada"). Pode haver outros. O Hub já tem ~70% de meta-lixo — este levantamento é insumo para a fase de saneamento já planejada.

## Critério de sucesso

Relatório gerado e salvo no Drive com lista completa dos fragmentos curador=gpt + análise de qualidade.
