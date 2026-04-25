---
tipo: estado-atual-sessao
atualizado: 2026-04-25T17:15-03:00
---

# Estado atual — handoff entre sessões

Documento vivo. Atualizar no final de cada sessão que deixa algo no meio.

## Última sessão (2026-04-25 — dia inteiro, várias rodadas)

Maratona de implementações. Detalhes completos em `dialogos-tiogu-claude/semana-2026-04-21.md`.

### Hoje (resumo)
- **Sprint 1 fechado**: `auto_diagnostico` ✅ produção, `logs_railway` 🚧 (aguarda PC)
- **Sprint 2 parcial**: `pesquisar_pubmed` + `pesquisar_arxiv` ✅, `perguntar_gpt` ✅
- **Wikilinks** `sugerir_wikilinks` ✅ produção
- **Dimagem A+B ativado** com confirmação prévia + contexto Haiku (state em bot_state.json)
- **Tagueamento `via` no Mem0** fechado — bot Telegram (`telegram-claude`) e MCP local (`claude-code`) ambos taggam `metadata.via`
- **MCP server local** (`.claude/mcp/mem0_server.py` + `.claude/mcp/gus_server.py`) com 9 tools nas duas pontas
- **Hook `scan_sensivel.py`** PreToolUse no Claude Code (espelha defesa do bot)
- **Cron `check-saude.yml`** novo (07:30 BRT, alerta Telegram só se autodiagnóstico falhar)
- **Documentação arquitetural**:
  - `gus-11-tools-roadmap.md` — inventário oficial vivo (~40 tools, status, histórico)
  - `gus-12-portas-futuras.md` — diretriz de portas futuras (Telegram-GPT, Custom GPT, Alexa, carro)
  - `gus-13-tags-canonicas.md` — contrato canônico dos brains/tags
- **Análise dashboard Mem0**: brain `gustavo` real é 164 (não 128); brain `gus` ~4; quota 37%; 3 entities; 4+ memórias poluídas identificadas
- **Decisão Alexa = porta complementar, não destino final**. Conversa fluida real é Custom GPT mobile + eventualmente Claude voice. Alexa V1 sem câmera, sem ações (Sprint 3 pulado).

### Bot agora em 21 tools

`read_from_github`, `list_github_directory`, `list_branches`, `list_commits`, `search_memory`, `meta_memoria`, `auditoria_mem0`, `salvar_memoria_gus`, `buscar_memoria_gus`, `deletar_memoria`, `search_web`, `pesquisar_pubmed`, `pesquisar_arxiv`, `save_to_github`, `criar_acao`, `disparar_workflow`, `logs_railway` (🚧), `auto_diagnostico`, `sugerir_wikilinks`, **`perguntar_gpt` (NOVO)**, + processamento implícito (imagens, PDFs, Word, Excel, áudio Whisper).

## Pendente pra próxima sessão

### Prioridade 1 — **Custom GPT no ChatGPT** (próximo passo do caminho Alexa)
- **Validado como objetivo em si** (não só ensaio pra Alexa) — é a porta de "conversa fluida em voz" via app ChatGPT mobile.
- Meu trabalho: ~3-4h (FastAPI em pasta `api/`, endpoints REST espelhando subset de tools, OpenAPI 3.0 schema, Bearer token auth, integração com `main.py` rodando bot + FastAPI em paralelo via asyncio, ajustes Dockerfile/railway.toml pra expor `$PORT`)
- Ação do Gustavo: ~20min (gerar `CUSTOM_GPT_TOKEN`, criar GPT no chatgpt.com/gpts/editor, importar OpenAPI, testar voz)
- Conta: `gustavo.pratti84@gmail.com` (já tem ChatGPT Plus)
- Doc detalhada em `gus-10-caminho-alexa.md` Passo 1

### Prioridade 2 — Quando Gustavo voltar pro PC
- Criar `~/.claude/gus.env` (4 keys: MEM0, ANTHROPIC, GITHUB, TAVILY) — destrava MCP daqui
- Limpar 4+ memórias poluídas via MCP (depende de gus.env)
- Token novo Railway + `scripts/test_railway_logs.py` cascata diagnóstica → valida `logs_railway`
- Investigar 3ª entity no Mem0

### Prioridade 3 — Em sequência
- Volume Railway (`/app/data` 1GB, ~30min meu + 5min Gustavo) — persiste logs/históricos
- Decidir se Sprint 3 volta (email/calendar/TTS) ou pula direto pra Alexa V1
- Alexa Skill V1 (Dot 3, Polly, voz pura) — depois do Custom GPT
- Termux + wake word "Gus" no S8 (pós-Alexa) — Opção B aprovada

### Pendentes menores
- Claude Chat Project — refazer validação com identity.md colado
- `fut-06-voz-telegram.md` pode ser marcado como concluído (Whisper entregue)
- Apagar arquivo de teste `capturado/misc/teste-drive-sync.md` quando quiser
- Workflow YAML do `enrich_mem0_export.py` — script existe, sem cron
- Observar dimagem A+B em produção 1-2 semanas, depois decidir tirar A

## Decisões importantes tomadas hoje

- **Alexa não é o destino final** — é porta complementar pra comandos curtos em casa. Conversa fluida = mobile (Custom GPT primeiro, Claude voice depois)
- **Câmera no Echo Show é inviável via Skill** — Skills custom não acessam câmera. Caminho real é câmera IP separada (S8 velho com IP Webcam = R$ 0)
- **Wake word "Gus" no S8** = Termux + openWakeWord (Opção B), futuro pós-Alexa
- **Sprint 2 = só GPT-5 mini** (Perplexity adiado, Gemini não priorizado)
- **Sprint 3 pulado nesta rodada** — Alexa V1 será leitura/captura/pergunta apenas

## Bugs em aberto (não bloqueantes)
- Mem0 latência de indexação (minutos)
- DDG fallback se Tavily esgotar
- Quota Retrieval API Mem0 em 37% no dia 25 — monitorar
- 4+ memórias poluídas no brain `gustavo` aguardando MCP local pra deletar

## Como usar este arquivo

1. Próxima sessão: ler PRIMEIRO, depois `gus-10-caminho-alexa.md` se for sessão de dev rumo à Alexa
2. Ao fim da sessão: atualizar "Última sessão" + "Pendente"
3. Commit + push antes de encerrar

Relacionado: [[gus-01-visao-geral]], [[gus-10-caminho-alexa]], [[gus-11-tools-roadmap]], [[gus-12-portas-futuras]], [[gus-13-tags-canonicas]]
