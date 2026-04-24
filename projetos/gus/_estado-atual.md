---
tipo: estado-atual-sessao
atualizado: 2026-04-24
---

# Estado atual — handoff entre sessões

Documento vivo. Atualizar no final de cada sessão que deixa algo no meio.

## Última sessão (2026-04-23/24) — maratona até caminho pra Alexa

### Infraestrutura base (sessão 23/abr → madrugada 24)
- Deploy Railway com todas variáveis. `TELEGRAM_CHAT_ID=495256549`. Bot responde, usa Mem0, salva/lê GitHub.
- 12 testes funcionais validados em produção via Telegram.

### Bugs críticos corrigidos
- **Bug 1 (data):** `datetime.now(BRT)` injetado no system prompt a cada chamada
- **Bug 2 (busca):** Tavily primário + DuckDuckGo fallback
- **Bug 3 (repo):** nome `Gustpbbr/Gus` declarado no system prompt
- **Bug 4 (descoberta):** `list_github_directory` adicionada
- **Bug workflow export-mem0:** pin `mem0ai==0.1.29` + `permissions: contents: write`

### Features novas — 13 tools totais no bot
- `read_from_github`, `list_github_directory`, `list_commits`, `search_memory`, `meta_memoria`, `auditoria_mem0`, `salvar_memoria_gus`, `buscar_memoria_gus`, `search_web`, `save_to_github`, `criar_acao`, `disparar_workflow`
- Processamento multimídia: imagens (resize + formato detectado), PDFs (Claude nativo), Word, Excel, **áudio/voz via Whisper** ← concluído hoje

### Arquitetura de memória — 2 cérebros + narrativa
- Mem0 brain `user_id="gustavo"` — fatos sobre o Gustavo
- Mem0 brain `user_id="gus"` — auto-observações do bot (começou vazio 24/04)
- `gus/meta-memoria.md` — narrativa reflexiva do Gus
- `_indices/_auditoria-mem0.md` — auditoria diária do brain `gustavo`
- Resumo extrativo a cada 3 turnos (era 5)

### Princípios fundamentais (topo do system prompt)
1. Não alucinar
2. Buscar antes de afirmar (Tavily primeiro)
3. Citar fonte quando buscou
4. Verificar antes de afirmar ausência

### SELF-1 validado em produção
- Primeira reflexão quinzenal (forced run) gerou observações reais e acionáveis sobre viés do Mem0 e drift de foco
- Ciclo natural: sábado semanas pares 10h BRT

### Protocolo `dialogos-tiogu-claude/`
- Canal bidirecional entre bot Telegram e Claude Code via commits versionados
- MD por semana (nomeado pela segunda-feira)
- Gus escreve demandas → Claude Code responde com feito/não feito/por quê
- Inaugurado 24/04 com demanda da própria criação do protocolo

### Resiliência
- Retry exponencial em 5xx/529 Anthropic
- Fallback Sonnet → Haiku
- Mensagens de erro PT específicas (sem créditos, chave inválida, etc)
- Rate limit 20 msg/min
- Scan de dados sensíveis + pasta `sensivel/` excluída do Drive
- Recovery de contexto em redeploy (system prompt instrui bot a usar search_memory/list_commits quando histórico vazio)

### Workflows GitHub Actions ativos
- `export-mem0.yml` (3h BRT) — `.md` + `.json`
- `auditoria-mem0.yml` (6h BRT) — `_indices/_auditoria-mem0.md`
- `briefing-matinal.yml` (7h BRT dias úteis) — msg no Telegram
- `retrospectiva-semanal.yml` (sexta 20h BRT) — `pessoal/diario/semana-*`
- `reflexao-quinzenal.yml` (sábado 10h BRT semanas pares) — SELF-1
- `sync-to-drive.yml` — bloqueado por policy Google Cloud

### Futuros mapeados
- `projetos/gus/futuro/` com 14 ideias (fut-01 a fut-14)
- `fut-14-criar-demanda-automatica.md` registrou gap do protocolo (bot não commita demandas sozinho)

### Plano consolidado até Alexa
- **Novo MD criado:** `projetos/gus/gus-10-caminho-alexa.md` — plano atualizado, caminho crítico, esforços estimados, decisões em aberto

### Extras que entraram depois (ainda 2026-04-24, turno final da manhã)

**Ontologia "Gus = entidade, bot = porta" (commit `eb85526`):**
- Antes, `system_prompt.md` e `.claude/hooks/session-start.sh` tinham linguagem ambígua ("Gus rodando como bot no Telegram", "Gus desenvolvedor") que tratava o bot como sinônimo de Gus.
- Agora explicitamente: Gus é a entidade única; Telegram, Claude Code, Claude Chat, Custom GPT, Alexa são **portas**. Todas compartilham identidade/memória/princípios/arquivos.
- Refletido em 3 arquivos: `system_prompt.md`, `meta-memoria.md`, `.claude/hooks/session-start.sh`.

**SessionStart hook (commit `0b25ab0`):**
- `.claude/hooks/session-start.sh` + `.claude/settings.json` criados.
- Injeta contexto dinâmico (~2000 chars) a cada nova sessão Claude Code: data/hora BRT, identidade do Gus nesta porta, princípios, ponteiros pros MDs-chave, info MCP Mem0.
- Também instala `mem0ai==0.1.29` + `mcp` no boot — MCP server sobe sem erro de versão.
- Rodada só em ambiente remoto (`CLAUDE_CODE_REMOTE=true`).

**Volume Railway persistente (commit `c573cae`):**
- Gustavo criou volume 5GB em `/app/data` (região US East, mesma do serviço).
- `logger.py` auto-detect: se `/app/data` existe, usa `/app/data/logs/`; senão fallback pra `logs/` local.
- `bot.py` auto-detect: se `/app/data` existe, persiste `conversation_histories`, `turn_counters`, `last_saved_turn`, `message_timestamps` em `/app/data/bot_state.json`.
- Write atômico (`tmp + os.replace`). Salva após cada `_responder()` e em `/reset`.
- Resolve: custo mensal real (HARD_LIMIT confiável), sem "Sim solto" em redeploy, contador de turnos preservado.

## Pendente pra próxima sessão

### Prioridade 1 — **Obsidian no PC** (próximo passo declarado pelo Gustavo)
- Tua ação: instalar Obsidian no Windows, clonar repo via GitHub Desktop em `C:\Users\Gustavo\Documents\Gus`, abrir como vault, instalar plugins Obsidian Git + Dataview
- Eu acompanho: orientação passo-a-passo se travar em algum ponto
- Ver detalhes em `gus-03-configuracao-manual.md` seção 5

### Prioridade 2 — **Custom GPT no ChatGPT** (próximo passo do caminho Alexa, depois do Obsidian)
- Meu trabalho: 3-4h (FastAPI, endpoints, OpenAPI, auth, integração com main.py)
- Tua ação: 20min (Railway secret, criação do GPT em ChatGPT Builder, teste em voz)
- Ver detalhes em `gus-10-caminho-alexa.md` Passo 1

### ✅ Já resolvido — Volume Railway
- Volume `gus-volume` criado com 5GB em `/app/data`.
- Código auto-detect implementado (commit `c573cae`). Sem ação adicional necessária.

### Pendências menores
- Claude Chat Project — refazer validação com identity.md colado
- Drive sync — aguardar decisão sobre Google Cloud policy OU ativar Drive nativo no ChatGPT depois de trocar assinatura Plus
- `fut-06-voz-telegram.md` pode ser marcado como concluído (Whisper entregue)

## Decisões tomadas hoje

- **ChatGPT Plus atual (`gustavo.pratti84@`)** serve pro Custom GPT. Troca de assinatura pro email principal fica pra depois.
- **Drive nativo no ChatGPT** é nice-to-have mas não bloqueia — ativar quando trocar Plus.
- **Executor da fila:** ainda não decidido qual primeiro (Twilio vs Calendar vs Gmail).
- **Protocolo `dialogos-tiogu-claude/`** tem gap conhecido (bot não registra sozinho) — fut-14 captura a solução, implementar quando o protocolo for usado ativamente.

## Bugs em aberto (não bloqueantes)
- Mem0 tem latência de indexação (minutos) — memórias recém-salvas podem não aparecer em busca imediata
- DDG pode falhar se Tavily estourar limite mensal
- Tracking de custo reseta em redeploy (resolve com volume Railway)

## Como usar este arquivo

1. Próxima sessão: ler PRIMEIRO, depois `gus-10-caminho-alexa.md` se for sessão de dev rumo à Alexa
2. Ao fim da sessão: atualizar "Última sessão" + "Pendente"
3. Commit + push antes de encerrar

Relacionado: [[gus-01-visao-geral]], [[gus-10-caminho-alexa]], [[gus-02-implementado]], [[gus-08-plano-proximos-passos]]
