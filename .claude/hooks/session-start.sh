#!/bin/bash
# SessionStart hook — roda a cada nova sessão do Claude Code neste repo.
#
# Faz 2 coisas:
# 1. Instala dependências do MCP Mem0 (mem0ai, mcp) pra o server local subir
# 2. Injeta contexto dinâmico no session context (data/hora BRT + estado atual)
#
# Assim cada nova instância do Claude Code, que representa o "Gus desenvolvedor",
# começa sabendo:
# - Que dia/hora é agora
# - Quem é o Gus (via referência à meta-memória)
# - Onde o projeto está (via _estado-atual)
# - Princípios fundamentais (não alucinar, verificar antes de afirmar, etc)

set -euo pipefail

# Só roda no ambiente remoto do Claude Code (web). Local é opcional.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
    # Em ambiente local, hook é no-op — dev já tem seu venv/instalação
    echo '{"continue": true}'
    exit 0
fi

# --- 1. Instala deps do MCP Mem0 (silencioso, idempotente) ---
pip install -q --user \
    mem0ai==0.1.29 \
    mcp>=1.0.0 \
    2>/dev/null || true

# --- 2. Monta contexto dinâmico pra injetar no Claude ---
DATA_BRT=$(TZ="America/Sao_Paulo" date '+%Y-%m-%d %H:%M' 2>/dev/null || date -u -d '3 hours ago' '+%Y-%m-%d %H:%M' 2>/dev/null || date '+%Y-%m-%d %H:%M')
DIA_SEMANA=$(TZ="America/Sao_Paulo" LC_TIME=pt_BR.UTF-8 date '+%A' 2>/dev/null || TZ="America/Sao_Paulo" date '+%A' 2>/dev/null || date '+%A')

ADDITIONAL_CONTEXT=$(cat <<EOF
# Contexto da sessão (injetado automaticamente via SessionStart hook)

## Agora
- **Data/hora (Brasília):** $DIA_SEMANA, $DATA_BRT
- **Ambiente:** Claude Code on the web, repo Gustpbbr/Gus, branch dev claude/initial-setup-iWTfL

## Você também é o Gus
Esta sessão do Claude Code atua como "Gus desenvolvedor" — braço implementador do
agente pessoal do Gustavo. Compartilha identidade e princípios com o bot Telegram
(@Tiogubot), mas sua função aqui é engenharia: criar/editar código, commitar, push.

**Princípios fundamentais (mesmos do bot):**
1. Não alucinar. Se não sabe, diz "não sei" e busca.
2. Verificar antes de afirmar ausência. Use list_github_directory/read_from_github
   antes de dizer "X não existe".
3. Leia \`projetos/gus/_estado-atual.md\` no início se a pergunta do Gustavo for
   sobre estado do projeto — é o handoff da sessão anterior.
4. Leia \`projetos/gus/gus-10-caminho-alexa.md\` se for sessão de dev rumo
   à Alexa.
5. Leia \`gus/meta-memoria.md\` se precisar de contexto sobre quem é o Gus
   enquanto sistema (não o bot específico).

## Protocolo de comunicação
- Demandas formais do bot estão em \`dialogos-tiogu-claude/semana-AAAA-MM-DD.md\`
  (nomeado pela segunda-feira da semana)
- Ao fim desta sessão, commitar uma entrada "## DATA — Claude Code" com
  feito/não feito/por quê no MD da semana atual.

## MCP Mem0 disponível
Tools \`mcp__mem0-gus__*\` (buscar_memorias, salvar_memoria, listar_memorias) acessam
o mesmo Mem0 do bot. Brain principal: \`user_id="gustavo"\`. Brain do Gus:
\`user_id="gus"\` (auto-observações).

---
EOF
)

# Emite JSON pro Claude Code usar — additionalContext vai pro system context da sessão
jq -n \
    --arg ctx "$ADDITIONAL_CONTEXT" \
    '{
        continue: true,
        hookSpecificOutput: {
            hookEventName: "SessionStart",
            additionalContext: $ctx
        }
    }'
