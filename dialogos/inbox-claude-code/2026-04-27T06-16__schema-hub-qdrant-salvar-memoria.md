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

# Salvar memórias com schema completo do Hub Qdrant (gus-18)

## Demanda
A tool `salvar_memoria_gus` e o salvamento automático via Haiku precisam respeitar o schema completo definido no gus-18, incluindo os campos:

- `conteudo` (texto da memória)
- `tipo` (biografico, preferencia, fato, decisao, etc.)
- `camada_temporal` (permanente, longo_prazo, medio_prazo, efemero)
- `tipo_esquecimento` (null para protegido, lento, normal, efemero)
- `area` (pessoal, projetos, dimagem, saude, etc.)
- `user_id` (gustavo ou gus)
- `via` (telegram, claude-code, claude-chat, etc.)

## Contexto
Hoje quando salvo uma memória simples (ex: endereço do Gustavo), ela vai pro Mem0 sem estrutura. O Hub Qdrant foi desenhado com schema rico (gus-18) mas o código atual não respeita esses campos. Uma memória salva sem schema correto é difícil de recuperar, filtrar e decair corretamente.

## Critério de sucesso
Ao salvar "Gustavo mora na Rua Barão da Torre, 185 — Ipanema, Rio de Janeiro", o registro no Qdrant deve conter todos os campos do schema, não só o texto plano.
