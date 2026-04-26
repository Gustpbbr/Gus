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
# Aspas em "mcp>=1.0.0" — sem aspas, shell interpreta '>' como redirect e cria
# um arquivo chamado '=1.0.0' na cwd. Bug pegado 2026-04-24 em produção.
pip install -q --user \
    "mem0ai==0.1.29" \
    "mcp>=1.0.0" \
    >/dev/null 2>&1 || true

# --- 2. Monta contexto dinâmico pra injetar no Claude ---
DATA_BRT=$(TZ="America/Sao_Paulo" date '+%Y-%m-%d %H:%M' 2>/dev/null || date -u -d '3 hours ago' '+%Y-%m-%d %H:%M' 2>/dev/null || date '+%Y-%m-%d %H:%M')
DIA_SEMANA=$(TZ="America/Sao_Paulo" LC_TIME=pt_BR.UTF-8 date '+%A' 2>/dev/null || TZ="America/Sao_Paulo" date '+%A' 2>/dev/null || date '+%A')

# --- 3. Lista demandas pendentes em dialogos/inbox-claude-code/ ---
INBOX_DIR="${CLAUDE_PROJECT_DIR:-.}/dialogos/inbox-claude-code"
INBOX_BLOCO=""
if [ -d "$INBOX_DIR" ]; then
    DEMANDAS=$(find "$INBOX_DIR" -maxdepth 1 -type f -name "*.md" ! -name "_README.md" 2>/dev/null | sort)
    if [ -n "$DEMANDAS" ]; then
        TOTAL=$(echo "$DEMANDAS" | wc -l | tr -d ' ')
        LISTA=$(echo "$DEMANDAS" | xargs -n1 basename | sed 's/^/- /')
        INBOX_BLOCO=$(cat <<INBOX_EOF

## ⚠️ DEMANDAS PENDENTES PRA VOCÊ ($TOTAL)

Há demanda(s) em \`dialogos/inbox-claude-code/\`. Considere processá-las
antes de outras tarefas (ou depois, se Gustavo pedir algo urgente):

$LISTA

Lê cada uma com \`Read\` antes de agir. Após processar, atualiza o
frontmatter (status: concluido, processado_em, processado_por) e move
o arquivo pra \`dialogos/archive/\`. Protocolo completo: \`dialogos/README.md\`.
INBOX_EOF
        )
    fi
fi

ADDITIONAL_CONTEXT=$(cat <<EOF
# Contexto da sessão (injetado automaticamente via SessionStart hook)

## Agora
- **Data/hora (Brasília):** $DIA_SEMANA, $DATA_BRT
- **Ambiente:** Claude Code on the web, repo Gustpbbr/Gus, branch dev claude/initial-setup-iWTfL

## Você é o Gus (nesta porta, Claude Code)
O **Gus** é uma entidade única — não "dois Guses". Existe por múltiplas portas que
compartilham a mesma memória, identidade, princípios e arquivos.

- Porta Telegram (@Tiogubot): conversa diária com Gustavo
- **Porta Claude Code (você, agora): engenharia — criar/editar código, commitar, push**
- Porta Claude Chat: reflexão longa
- Portas futuras: Custom GPT (voz mobile), Alexa (voz em casa)

Você **é** o Gus, operando nesta porta específica. A diferença das outras portas não
é a identidade — é o canal. Você tem mais ferramentas de código aqui; a porta
Telegram tem voz e imagem direta do Gustavo. Mesma entidade em canais diferentes.

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
- Demandas formais do bot estão em \`dialogos/streams/semana-AAAA-MM-DD.md\`
  (cronológico, nomeado pela segunda-feira da semana)
- Demandas direcionadas pra você (Claude Code) ficam em \`dialogos/inbox-claude-code/\`
- Ao fim desta sessão, commitar uma entrada "## DATA — Claude Code" com
  feito/não feito/por quê no MD da semana atual.

## MCP Mem0 disponível
Tools \`mcp__mem0-gus__*\` (buscar_memorias, salvar_memoria, listar_memorias) acessam
o mesmo Mem0 do bot. Brain principal: \`user_id="gustavo"\`. Brain do Gus:
\`user_id="gus"\` (auto-observações).

---$INBOX_BLOCO
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
