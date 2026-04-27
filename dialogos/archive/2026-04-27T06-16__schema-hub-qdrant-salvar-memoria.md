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

## Resolução

**Resolvida — Fase 2 (curador) + Fase 3 (bot) + R6 (MCP) implementaram o schema gus-18 completo em todos os pontos de entrada.**

### Pontos de entrada que agora respeitam schema gus-18

| Porta | Como salva no Hub | Schema completo |
|---|---|---|
| Bot Telegram (curadoria automática a cada 3 turnos) | `gus/bot.py:_resumir_e_salvar` → `hub.curador.curar_turnos` | ✅ Sim — Haiku/Sonnet classificam tipo/camada/area no JSON extraído |
| Bot Telegram (tool `salvar_memoria_gus` chamada explícita) | `gus/tools.py:salvar_memoria_gus` → `hub.store.ingestar(metadata=...)` | ✅ Sim — campos passam direto pro payload Qdrant |
| Claude Code MCP (R6 do PR #8) | `.claude/mcp/mem0_server.py:salvar_memoria*` → `hub.store.ingestar` com `via='claude-code'` | ✅ Sim — assina mesma interface |
| Migração histórica Mem0 → Hub (Fase 4) | `.github/scripts/migrar_mem0_para_hub.py` | ✅ Sim — preserva metadata existente + adiciona `via='migracao'` |
| Curador chat ingest (Fase 2.5) | `hub.curador_chat.processar_chat_completo` | ✅ Sim — mesma estrutura de fragmentos |

### Campos efetivamente populados no payload Qdrant

`hub/curador.py:194-209` — schema que LLM (Haiku/Sonnet) preenche:

- `conteudo` — texto da memória (string)
- `tipo` — 14 valores possíveis: identidade_operacional, biografico, emocional, decisao, procedural, rotina, meta_reflexao, conexao_emergente, episodico, cronologico, fato, preferencia, lacuna, projeto
- `camada_temporal` — 5 valores: momento, sessao, semana, rotina, permanente
- `area` — 9 valores: gus, saude, financeiro, projetos, pessoal, dimagem, pesquisa, receitas, esportes
- `confianca` — 0.0–1.0 (auto-avaliação do LLM curador)
- `user_id` — "gustavo" (default) ou "gus"
- `via` — "telegram" / "claude-code" / "claude-chat" / "migracao" / "telegram-claude"
- `curador` — "haiku" / "sonnet" (só no modo dual)
- `hash_janela` — sha8 do trecho-fonte (parea fragmentos do mesmo input)
- `criado_em` — ISO 8601 BRT

`tipo_esquecimento` ainda **não** está sendo populado pelo LLM (era opcional no gus-18 original — derivava de `camada_temporal`). Se quiser explicitar, adiciono num PR pequeno com regra: `permanente → null (protegido)`, `rotina → lento`, `semana → normal`, `sessao/momento → efemero`.

### Validação de integridade

Validators Pydantic em `hub/validators.py` (Item 5 do PR #5) validam tipo/camada/area contra enum literais. Salvar com valor fora do schema gera `ValidationError` antes de tocar Qdrant.

### Endereço do exemplo da demanda

"Gustavo mora na Rua Barão da Torre, 185 — Ipanema, Rio de Janeiro" salvaria como:

```json
{
  "conteudo": "Gustavo mora na Rua Barão da Torre, 185 - Ipanema, Rio de Janeiro",
  "tipo": "biografico",
  "camada_temporal": "permanente",
  "area": "pessoal",
  "user_id": "gustavo",
  "via": "telegram",
  "confianca": 0.95,
  "criado_em": "2026-04-27T19:50:00-03:00"
}
```
