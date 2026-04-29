---
tipo: plano-execucao
origem: claude-code
destino: claude-code
prioridade: media
status: concluido
criado_em: 2026-04-28T19:50:00-03:00
processado_em: 2026-04-28T19:55:00-03:00
processado_por: claude-code
referente: gus-28-acesso-hub-claude-chat (Passo 1)
---

# Plano de execução — Passo 1 do gus-28

Geração de `gus-estado-atual.md` em `dialogos/_bootstrap/` a cada 15min,
lendo do Hub Qdrant. Resolve lag de 21h do Claude Chat (snapshot às 03h)
sem mudar arquitetura.

## Contexto técnico

- **Documento de referência:** `dialogos/inbox-tiogu/2026-04-28T18-00__gus-28-acesso-hub-claude-chat.md`
- **Hub atual:** `hub/store.py` tem `ego_cache(user_id)` retornando dict com
  identidade, decisões recentes, meta-reflexões. Tem `listar(user_id, limit)`
  pra scroll.
- **Stack:** Python + qdrant-client + sentence-transformers (já em
  `.github/scripts/requirements.txt` do R2).
- **Secrets já no GH Actions:** `QDRANT_URL`, `QDRANT_API_KEY`.
- **Path de saída:** `dialogos/_bootstrap/gus-estado-atual.md` (sincroniza
  pro Drive automaticamente).

## Escopo desta tarefa

1. Criar `.github/scripts/gerar_estado_atual_chat.py`
2. Criar `.github/workflows/gerar-estado-claude-chat.yml` (cron `*/15 * * * *`)
3. Atualizar `dialogos/_bootstrap/gus-bootstrap.md` referenciando o novo arquivo
4. Smoke test sintaxe + YAML
5. PR único

**NÃO inclui:**
- Passo 2 (MCP wrapper) — sessão futura
- NeuroGus — depende de pré-requisitos não-implementados
- Mudança no system_prompt do TioGu pra injetar ego_cache
- Outras demandas em `inbox-tiogu/`

## Checkpoints

- [x] Branch `claude/passo1-estado-atual-claude-chat` criada
- [x] Inspecionar `hub/store.py:ego_cache()` (já existe — retorna identidade, decisões recentes, meta-reflexões)
- [x] Plano escrito (este arquivo)
- [x] Script `gerar_estado_atual_chat.py` criado
- [x] Workflow `gerar-estado-claude-chat.yml` criado
- [x] `gus-bootstrap.md` atualizado com referência ao novo arquivo
- [x] Sintaxe Python OK (script)
- [x] YAML válido (workflow)
- [x] Smoke test offline rodou — output ~318 tokens, dentro do alvo
- [x] PR aberto

## Decisões tomadas

1. **Path final:** `dialogos/_bootstrap/gus-estado-atual.md` (não `_indices/`).
   Razão: bootstrap é onde Claude Chat lê pra ativar identidade. Faz sentido
   que o "estado vivo" fique junto do "identidade base" — Claude Chat lê
   ambos ao iniciar.

2. **Sem dependência de Mem0:** script usa só `hub/store.py`. Já estamos
   pós-Fase 4 do ADR-001.

3. **Frescor da janela:** últimas **6h** de fragmentos. Não 24h pra evitar
   ruído (resumos antigos), nem 1h pra evitar quase-vazio em horários
   ociosos. 6h cobre uma "manhã" típica de uso.

4. **Limite de tokens:** ~500-1500 (3-4% janela 200k). Bem abaixo do que
   Claude Chat aguenta, deixa espaço pra conversa.

5. **Idempotência:** workflow só commita se houve mudança real (git diff).
   Evita commit no-op de 96 commits/dia (4×24).

6. **Filtro de fragmentos:** preferência por `tipo` em ['decisao', 'preferencia',
   'biografico', 'episodico', 'meta_reflexao']. Excluir 'lacuna' (são
   pendências, não fatos).

## Resultado esperado

Após cron rodar 1x:
- Arquivo `dialogos/_bootstrap/gus-estado-atual.md` com timestamp atual,
  ego_cache populado, fragmentos recentes
- Drive sincronizado (próximo cron `sync-to-drive` em ≤15min após push)
- Claude Chat no próximo boot: arquivo aparece no Project (se Drive sync ativo)

## Próxima sessão (se for outra aba Claude Code)

Se interromper antes de terminar e outra aba continuar:
- Ler este arquivo em `dialogos/inbox-claude-code/`
- Conferir checkpoints `[ ]` ainda não-feitos
- Continuar do primeiro `[ ]`
- Atualizar checkpoints feitos antes de cada commit
- Quando concluído tudo: marcar `status: concluido` no frontmatter

## Resultado
