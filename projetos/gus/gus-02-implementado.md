---
criado_em: 2026-04-18
tipo: documentacao-projeto
status: concluido
---

# Gus — O que já foi implementado

Tudo que está pronto no código e na infraestrutura.

## Código do bot (7 módulos)

### gus/main.py
- Entry point, inicializa o bot Telegram
- Carrega variáveis de ambiente

### gus/bot.py
- Handlers: texto, foto, PDF, /start, /reset
- Auth deny-all por padrão (segurança)
- `/start` mostra chat_id apenas quando TELEGRAM_CHAT_ID não está configurado
- Mem0 save assíncrono com error handling (não bloqueia resposta)

### gus/llm.py
- Chama Claude API com loop de tool use (máximo 10 rounds)
- Mapa de preços dinâmico (Opus 4.7: $5/$25, Sonnet: $3/$15, Haiku: $0.8/$4)
- Timeout de 120s no client Anthropic
- Cache do system prompt com @lru_cache
- Saída de segurança se loop de tools esgotar

### gus/memory.py
- Busca memórias no Mem0 (search por query)
- Salva par user/assistant no Mem0 após cada conversa

### gus/tools.py
- **search_web**: busca no DuckDuckGo via httpx (timeout 30s)
- **save_to_github**: cria/atualiza .md no repo com frontmatter automático (data/hora BRT, `via: telegram`)
- **read_from_github**: lê .md do repo por path
- Path traversal protection (regex + bloqueio de `..`)
- Validação de filename contra injeção

### gus/media.py
- Processa imagens via visão (Claude multimodal)
- Extrai texto de PDFs

### gus/logger.py
- Log de custos e latência em JSONL
- Registra modelo, tokens, custo por chamada

## System prompt (gus/system_prompt.md)
- Personalidade completa do Gus para Telegram
- Regras de quando ler e quando salvar no GitHub
- Estrutura de pastas do repositório
- Nomenclatura de arquivos
- Wikilinks para conexões entre arquivos (Obsidian)

## Identidade unificada (gus/gus-identity.md)
- Contexto do Gustavo (compartilhado por todas as portas)
- Personalidade do Gus (somente Telegram)
- Projetos ativos, valores, base de conhecimento

## MCP Server Mem0 (.claude/mcp/mem0_server.py)
- 3 ferramentas: buscar_memorias, salvar_memoria, listar_memorias
- Expõe Mem0 como tool do Claude Code via protocolo MCP
- Mesmo user_id ("gustavo") do bot Telegram

## GitHub Actions

### Sync GitHub → Google Drive (.github/workflows/sync-to-drive.yml)
- Trigger: push na main com arquivos .md
- Converte .md em Google Docs
- Preserva estrutura de pastas
- Exclui arquivos de sistema (CLAUDE.md, gus/, .github/)

### Export diário Mem0 (.github/workflows/export-mem0.yml)
- Cron: 3h BRT (6h UTC)
- Exporta todas as memórias para gus-memoria-export.md
- Auto-commit se houver mudanças

## Infraestrutura
- Dockerfile + railway.toml prontos para deploy
- CLAUDE.md com briefing completo do projeto

## Segurança implementada
- Auth deny-all (bot ignora mensagens sem TELEGRAM_CHAT_ID)
- Path traversal validation com regex
- Timeout em todas as chamadas externas (Anthropic 120s, httpx 30s)
- Loop de tools limitado a 10 rounds
- Filename validation contra injeção

Relacionado: [[gus-01-visao-geral]], [[gus-03-configuracao-manual]], [[gus-04-seguranca-protecao]]
