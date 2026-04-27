# `.claude/hooks/`

Hooks do Claude Code que rodam em momentos específicos da sessão. Configurados em `.claude/settings.json`.

## Hooks ativos

### `session-start.sh` (trigger: `SessionStart`)

Roda no início de cada sessão Claude Code Web (skip em local).

- Instala dependências do MCP Mem0 (`mem0ai`, `mcp`) via `pip install --user`
- Idempotente, silencioso em falhas

### `scan_sensivel.py` (trigger: `PreToolUse` em `Write|Edit|NotebookEdit`)

Bloqueia escrita de dados sensíveis (CPF, CNPJ, cartão, API keys) fora de `sensivel/`.

- Espelha `gus/tools.py:_PATTERNS_SENSIVEIS`
- `exit 2` com mensagem em stderr → Claude Code vê e ajusta antes de escrever

### `retro_engine.py` (trigger: `Stop`)

**Retro Engine** — antecipa Fase 5 do roadmap pre-AGI (`gus-22`).

Ao final de cada sessão Claude Code, lê o transcript completo e roda Haiku como curador focado em **autobiografia do agente** (não fatos sobre o Gustavo). Salva fragmentos no Hub Qdrant com `user_id="gus"`, `via="claude-code"`.

Tipos extraídos:
- `decisao_arquitetural` — decisões técnicas com contexto + raciocínio (`tipo_esquecimento: protegido`)
- `meta_reflexao` — padrões de erro / comportamento detectados
- `aprendizado_operacional` — caveats de tools, padrões de como agir
- `marco_evolutivo` — momentos em que o sistema ganhou capacidade nova (`tipo_esquecimento: protegido`)
- `historia_sistema` — fatos sobre evolução do sistema
- `procedural` — protocolos/procedimentos estabelecidos

**Variáveis de ambiente necessárias** (tipicamente em `~/.claude/gus.env`):
- `ANTHROPIC_API_KEY`
- `QDRANT_URL`
- `QDRANT_API_KEY`

Se faltarem, hook é **no-op silencioso** (não quebra fim da sessão).

Log auditável: `_log/retro-engine-claude-code/AAAA-MM-DD.md`.

## Convenções pra novos hooks

- **NUNCA** bloquear o fluxo do Claude Code (sair com `exit 0` mesmo em erro)
- Logar em `_log/<nome-do-hook>/AAAA-MM-DD.md` pra auditoria
- Se precisar de env vars, validar antes e cair pra no-op silencioso se faltar
- Documentar aqui assim que adicionar
