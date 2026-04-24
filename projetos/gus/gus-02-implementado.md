---
tipo: documentacao-projeto
projeto: gus
parte: 2-de-7
atualizado: 2026-04-24
---

# Gus — O que está implementado

Estado real do código em `main`. Reflete o que tá deployado no Railway e rodando em produção.

## Módulos Python (`gus/`)

| Módulo              | Responsabilidade                                                      |
|---------------------|-----------------------------------------------------------------------|
| `main.py`           | Entry point. Registra handlers `/start`, `/reset`, `/custo`, `/foco` + mensagem, foto, documento |
| `bot.py`            | Handlers Telegram. Auth, rate limit (20/min), limite custo mensal, contador de turnos, rate limiting, resumo extrativo a cada 3 turnos, query Mem0 contextual (últimas 3 msgs do user) |
| `llm.py`            | Chama Claude com loop de tool use (máx 10 rounds). Retry exponencial (1s/2s/4s/8s) em 5xx/529. Fallback pro Haiku se Sonnet falhar. Mensagens de erro amigáveis em português. Data/hora atual injetada no system prompt a cada chamada. Função `gerar_resumo_turnos` (Haiku) |
| `memory.py`         | Mem0 client. `buscar_memorias(query)`, `salvar_memorias(messages)`, `buscar_memorias_detalhada(query, limit)` |
| `tools.py`          | 9 ferramentas (ver abaixo) |
| `media.py`          | PDF nativo do Claude (OCR + layout), imagens com resize + compressão + detecção MIME via Pillow, docx via python-docx, xlsx via openpyxl, cache SHA-256, download com retry |
| `logger.py`         | Log JSONL em `logs/gus_metrics.jsonl` + custo do mês |

Mais `system_prompt.md` (personalidade + regras do Gus no Telegram) e `gus-identity.md` (identidade compartilhada entre portas).

## As 9 tools ativas

| Tool | Função |
|------|--------|
| `read_from_github(path)` | Lê arquivo do repo. Validação anti-traversal. |
| `list_github_directory(path)` | Lista conteúdo de uma pasta (arquivos + subpastas ordenados). |
| `list_commits(path, limit, since_days)` | Histórico via GitHub API. Retorna hash/data BRT/autor/mensagem. |
| `search_memory(query, limit)` | Busca ativa no Mem0 (semântica). |
| `meta_memoria()` | Retorna `_indices/_meta-memoria.md` — stats, duplicatas, gaps. |
| `search_web(query)` | Tavily primário, DuckDuckGo fallback. |
| `save_to_github(filename, content, folder)` | Salva com frontmatter automático + scan de dados sensíveis (CPF, CNPJ, cartão, 4 tipos de API keys). Se detectar fora de `sensivel/`, não salva e avisa. |
| `criar_acao(tipo, conteudo, alto_risco)` | Enfileira em `acoes/pendentes/<id>.md`. Tipos: whatsapp, email, calendar, lembrete, nota. Executor ainda não existe. |
| (implícito) | Processamento automático de imagem, PDF, Word, Excel quando recebidos. |

## Comandos Telegram

| Comando | Função |
|---------|--------|
| `/start` | Boas-vindas. Se `TELEGRAM_CHAT_ID` vazio, mostra chat_id pra configurar. |
| `/reset` | Limpa histórico + contadores. Dispara save do resumo pendente antes. |
| `/custo` | Gasto do mês vs `HARD_LIMIT_USD_MONTH`. Reseta em redeploy. |
| `/foco <descrição>` | Salva foco da sessão no Mem0 com tag `[FOCO-ATUAL]`. |

## Loop de tool use (`llm.py`)

Máximo 10 rounds. A cada round, se `stop_reason == "tool_use"`, executa as tools em ordem e reinjeta o resultado. Se estourar, devolve "entrei em loop interno".

Acumula `input_tokens` e `output_tokens` ao longo dos rounds pra calcular custo total.

Retry exponencial por modelo (4 tentativas: 1s, 2s, 4s, 8s) em erros 5xx/529/429. Se esgotar Sonnet, tenta Haiku. Erros 4xx (sem retry) caem num classificador que gera mensagem amigável em português (sem créditos, chave inválida, payload grande, rate limit, timeout, sem conexão).

## Preços por família (`llm.py`, abr/2026)

| Família | Input ($/M tokens) | Output ($/M tokens) |
|---------|--------------------|---------------------|
| Opus    | 5,00               | 25,00               |
| Sonnet  | 3,00               | 15,00               |
| Haiku   | 0,80               | 4,00                |

Default: `claude-sonnet-4-6`. Fallback: `claude-haiku-4-5`. Resumo extrativo: `claude-haiku-4-5`. SELF-1 Nosis/Thymos: Haiku. SELF-1 Síntese: Sonnet.

## Multimodal

**Imagens:** detecção automática de formato via Pillow (JPG, PNG, WebP, HEIC, etc). Resize pra 1.15MP máximo se for maior. Re-encode JPEG quality 85. Cache SHA-256 (até 50 entradas LRU).

**PDFs:** Claude nativo via `document` content type. Até 100 páginas / 32MB. OCR e preservação de layout embutidos. Se exceder 32MB, rejeita com aviso claro. Cache SHA-256 igual imagens.

**Word (.docx):** `python-docx` extrai texto de parágrafos + conteúdo de tabelas.

**Excel (.xlsx):** `openpyxl` read-only extrai dados por planilha em formato tabular.

Download com retry exponencial (2s, 4s, 8s) em falhas de rede.

## Histórico e memória

Histórico em memória por `chat_id` (`conversation_histories`), limitado aos últimos 40 turnos (`MAX_HISTORY_MESSAGES`). Reseta em redeploy — a continuidade vem do Mem0.

A cada mensagem:
1. Rate limit check (20 msg/min por chat_id)
2. Custo check (`HARD_LIMIT_USD_MONTH`)
3. Busca Mem0 com query contextual (últimas 3 msgs do Gustavo concatenadas)
4. Injeção de memórias relevantes no system prompt
5. Chama Claude com histórico + tools
6. Envia resposta no Telegram em chunks de 4096 chars
7. Cada 3 turnos do usuário, dispara resumo extrativo (Haiku) → Mem0 curado
8. Registra no log JSONL

## MCP server Mem0 (`.claude/mcp/mem0_server.py`)

Expõe 3 ferramentas para o Claude Code:
- `buscar_memorias(query)` — top 10
- `salvar_memoria(conteudo)` — observação
- `listar_memorias()` — todas

Usa mesmo `user_id="gustavo"` do bot. Chave via `~/.claude/mem0.key`.

## GitHub Actions (`.github/workflows/`)

| Workflow | Cron | Função |
|----------|------|--------|
| `sync-to-drive.yml` | Push `.md` em main | Sync pro Google Drive como Google Docs (BLOQUEADO — precisa secrets GOOGLE_CREDENTIALS + DRIVE_ROOT_FOLDER_ID) |
| `export-mem0.yml` | `0 6 * * *` (3h BRT) | Exporta todas memórias → `gus-memoria-export.md` + `.json` |
| `meta-memoria.yml` | `0 9 * * *` (6h BRT) | Auditoria Mem0 → `_indices/_meta-memoria.md` (stats, duplicatas, gaps — sem LLM, determinístico) |
| `briefing-matinal.yml` | `0 10 * * 1-5` (7h BRT dias úteis) | Briefing pro Telegram (precisa secrets TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID + ANTHROPIC_API_KEY) |
| `retrospectiva-semanal.yml` | `0 23 * * 5` (sexta 20h BRT) | Retrospectiva em `pessoal/diario/semana-AAAA-WW.md` |
| `reflexao-quinzenal.yml` | `0 13 * * 6` (sábado 10h BRT, só semanas pares) | SELF-1: Nosis + Thymos + Síntese em `projetos/gus/reflexoes/` |

Todos os scripts em `.github/scripts/` têm **skip silencioso** se secrets essenciais ausentes — evita email de falha.

## Estruturas de pastas

| Pasta | Conteúdo |
|-------|----------|
| `_indices/` | Dashboards MOC por área (master, saude, financeiro, projetos, dimagem, receitas, capturado) + `_meta-memoria.md` auto-gerado |
| `sensivel/` | Dados sensíveis (excluída do Drive sync) |
| `acoes/pendentes/` + `acoes/concluidas/` | Fila de ações (sem executor ainda) |
| `acoes/lembretes-ativos.md` | Lembretes recorrentes (sem cron ativo ainda) |
| `projetos/gus/` | Documentação do próprio Gus (gus-01 a gus-09 + `_estado-atual.md`) |
| `pessoal/diario/` | Retrospectivas semanais auto-geradas |
| `projetos/gus/reflexoes/` | Reflexões quinzenais (SELF-1) auto-geradas |

## Infraestrutura de deploy

- **Dockerfile** — base `python:3.11-slim`, instala `poppler-utils` (legado — PDF nativo não precisa mais, mas mantém por compatibilidade)
- **railway.toml** — builder `DOCKERFILE`, restart on failure 5x
- **requirements.txt** — 11 deps: `python-telegram-bot 21.6`, `anthropic 0.40.0`, `mem0ai 0.1.29`, `pypdf 4.3.1` (legado), `pdf2image 1.17.0` (legado), `httpx 0.27.0`, `duckduckgo-search 6.2.6`, `python-dotenv 1.0.1`, `Pillow 10.4.0`, `python-docx 1.1.2`, `openpyxl 3.1.5`

## Variáveis de ambiente

| Variável                    | Função                                          | Obrigatória |
|-----------------------------|-------------------------------------------------|-------------|
| `TELEGRAM_BOT_TOKEN`        | Bot Telegram                                    | sim         |
| `TELEGRAM_CHAT_ID`          | Chat autorizado (deny-all se vazio)             | sim         |
| `ANTHROPIC_API_KEY`         | Claude API                                      | sim         |
| `MEM0_API_KEY`              | Mem0 hosted                                     | sim         |
| `GITHUB_TOKEN`              | Fine-grained PAT com escopo Contents write      | sim         |
| `TAVILY_API_KEY`            | Busca web primária                              | não (fallback DDG) |
| `GITHUB_REPO`               | Default `Gustpbbr/Gus`                          | não         |
| `MODEL_DEFAULT`             | Default `claude-sonnet-4-6`                     | não         |
| `MODEL_FALLBACK`            | Default `claude-haiku-4-5`                      | não         |
| `MODEL_RESUMO`              | Default `claude-haiku-4-5`                      | não         |
| `MAX_TOKENS_RESPONSE`       | Default 2048                                    | não         |
| `HARD_LIMIT_USD_MONTH`      | Default 30                                      | não         |
| `MAX_HISTORY_MESSAGES`      | Default 40 (20 turnos)                          | não         |
| `TURNOS_PARA_RESUMO`        | Default 3                                       | não         |
| `RATE_LIMIT_MSG_PER_MINUTE` | Default 20                                      | não         |
| `LOG_DIR`                   | Default `logs`                                  | não         |

## Segurança implementada

| Vetor | Proteção | Onde |
|-------|----------|------|
| Usuário não autorizado | Deny-all se `TELEGRAM_CHAT_ID` vazio ou diferente | `bot.py:22` |
| Path traversal | Regex `^[a-zA-Z0-9\-_/]+$` + bloqueio de `..` | `tools.py:17-30` |
| Filename injection | Bloqueia `/` e `..` no filename | `tools.py:375` |
| Loop infinito de tools | `max_tool_rounds = 10` | `llm.py` |
| Dados sensíveis em MD | Regex CPF/CNPJ/cartão/API keys antes de salvar | `tools.py:37, 376-385` |
| Rate limit abuse | Janela 60s por chat_id | `bot.py:43-56` |
| Estouro de custo | `HARD_LIMIT_USD_MONTH` | `bot.py:36` |
| API timeouts | Anthropic 120s, httpx 30s, retry exponencial | `llm.py` |
| Mem0 save failure | `asyncio.create_task` com try/except, não bloqueia resposta | `bot.py:59-70` |
| Overload Anthropic | Retry + fallback Haiku + mensagem amigável PT | `llm.py` |

## Resiliência

- Retry exponencial em 5xx/529 da Anthropic (1-2-4-8s, 4 tentativas)
- Fallback automático Sonnet → Haiku
- 4xx mapeados pra mensagens em português (sem créditos, rate limit, payload grande, etc)
- Download de mídia com retry (2s/4s/8s)
- Workflows com skip silencioso se secrets faltam
- Mem0 save falha não interrompe conversa

## Bloqueios e pendências

Ver [[_estado-atual]] pra lista atualizada. Resumo:

- **Drive sync**: bloqueado por política Google Cloud (`iam.disableServiceAccountKeyCreation`)
- **Claude Chat Project**: validação falhou, precisa refazer com `gus-identity.md` colado em Project Instructions
- **Volume Railway pra `logs/`**: sem isso, tracking de custo reseta em redeploy
- **Executor da fila de ações**: Twilio/Gmail/Calendar não conectados — ações ficam em pendentes
- **Meta-memória primeira execução**: infra existe, cron roda amanhã 6h BRT (ou manual via workflow_dispatch)
- **Whisper áudio**: pré-requisito é chave OpenAI

Relacionado: [[gus-01-visao-geral]], [[gus-03-configuracao-manual]], [[gus-04-seguranca-protecao]], [[_estado-atual]]
