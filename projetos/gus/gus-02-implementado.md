---
tipo: documentacao-projeto
projeto: gus
parte: 2-de-7
atualizado: 2026-04-23
---

# Gus — O que está implementado

Estado real do código em `main`. Tudo aqui está commitado e roda localmente — falta só deploy.

## Módulos Python (`gus/`)

| Módulo              | Responsabilidade                                                      |
|---------------------|-----------------------------------------------------------------------|
| `main.py`           | Entry point. Carrega `.env`, registra handlers, inicia polling        |
| `bot.py`            | Handlers de Telegram (texto, foto, PDF, `/start`, `/reset`). Auth e limite mensal |
| `llm.py`            | Chama Claude com loop de tool use (máx 10 rounds). Calcula custo      |
| `memory.py`         | Mem0: `buscar_memorias(query)` e `salvar_memorias(messages)`          |
| `tools.py`          | 3 ferramentas: `read_from_github`, `search_web`, `save_to_github`     |
| `media.py`          | Processa imagens (visão) e PDFs (extração de texto ou render visual)  |
| `logger.py`         | Log JSONL em `logs/gus_metrics.jsonl` + custo do mês                  |

Mais `system_prompt.md` (personalidade do Gus no Telegram) e `gus-identity.md` (identidade compartilhada entre portas).

## As 3 tools

**`read_from_github(path)`** — lê `.md` do repo. Validação: regex `^[a-zA-Z0-9\-_/]+$`, bloqueio de `..`, 404 tratado. Exemplos de path: `pessoal/saude/historico-saude.md`, `projetos/gus/gus-01-visao-geral.md`.

**`search_web(query)`** — busca no DuckDuckGo (pacote `duckduckgo-search`), top 5 resultados. Retorna título, body e URL.

**`save_to_github(filename, content, folder)`** — cria ou atualiza `.md`. Frontmatter automático com `capturado_em` (horário Brasília) e `via: telegram`, inserido só se o conteúdo ainda não começa com `---\n`. Se o arquivo já existe, faz update com SHA. Commit message: `capture: {filename} via Gus`.

## Loop de tool use (`llm.py`)

Máximo 10 rounds. A cada round, se `stop_reason == "tool_use"`, executa as tools em ordem e reinjeta o resultado. Se estourar o limite, devolve mensagem de segurança ("entrei em loop interno").

Acumula `input_tokens` e `output_tokens` ao longo dos rounds para calcular o custo total da interação.

## Preços por família (`llm.py`, abr/2026)

| Família | Input ($/M tokens) | Output ($/M tokens) |
|---------|--------------------|---------------------|
| Opus    | 5,00               | 25,00               |
| Sonnet  | 3,00               | 15,00               |
| Haiku   | 0,80               | 4,00                |

Detecção por substring no nome do modelo. Default (fallback): Sonnet. Modelo padrão em produção: `claude-sonnet-4-6` (via `MODEL_DEFAULT`).

## Multimodal

**Imagens:** download, base64, envio como bloco `image` pro Claude Vision. Se houver caption, usa; senão pergunta "o que está nessa imagem?".

**PDFs:** tenta extração de texto com `pypdf`. Se o texto extraído tem mais de 200 caracteres, envia como texto (truncado em 500k caracteres). Se não, renderiza até 10 páginas como JPEG via `pdf2image`+poppler e manda como imagens pro Vision.

## Histórico e memória

Histórico em memória por `chat_id` (`conversation_histories`), limitado aos últimos 20 turnos (`MAX_HISTORY_MESSAGES`). Reseta em redeploy — a continuidade vem do Mem0, não do histórico em RAM.

A cada mensagem:
1. Busca memórias relevantes no Mem0 (top 5) e injeta no system prompt
2. Chama Claude com o histórico + tools
3. Envia resposta no Telegram em chunks de 4096 caracteres
4. Salva o par user/assistant no Mem0 de forma assíncrona (não bloqueia resposta)
5. Registra entrada no log JSONL

Comando `/reset` limpa o histórico em RAM. Comando `/start` mostra o `chat_id` se `TELEGRAM_CHAT_ID` não estiver configurado (bootstrap inicial).

## MCP server Mem0 (`.claude/mcp/mem0_server.py`)

Expõe o Mem0 como ferramenta do Claude Code. Três tools:

- `buscar_memorias(query)` — top 10 por relevância
- `salvar_memoria(conteudo)` — salva uma observação
- `listar_memorias()` — todas as memórias do user

Usa o mesmo `user_id = "gustavo"` do bot, então Claude Code e Telegram compartilham memória em tempo real.

## GitHub Actions

**`sync-to-drive.yml`** — dispara em cada push em `main` que altera `.md`, excluindo `.github/`, `gus/`, `docs/`, `CLAUDE.md`, `README.md`. Roda `.github/scripts/sync_to_drive.py`, que olha o diff `HEAD~1..HEAD`, garante a pasta no Drive, e faz upsert do arquivo como Google Doc (mimeType `application/vnd.google-apps.document`).

**`export-mem0.yml`** — cron `0 6 * * *` UTC (3h Brasília). Roda `.github/scripts/export_mem0.py` que chama `client.get_all(user_id="gustavo")` e escreve `gus-memoria-export.md` na raiz com frontmatter + lista numerada. Commita se houver mudança.

Sinergia: o export Mem0 gera `.md` que o sync Drive espelha no Google Drive — Mem0 → GitHub → Drive em ciclo automático.

## Infraestrutura de deploy

- **Dockerfile** — base `python:3.11-slim`, instala `poppler-utils` (para renderizar PDFs), copia o código, cria `logs/`, roda `python -m gus.main`.
- **railway.toml** — builder `DOCKERFILE`, restart on failure com 5 tentativas.
- **requirements.txt** — `python-telegram-bot==21.6`, `anthropic==0.40.0`, `mem0ai==0.1.29`, `pypdf==4.3.1`, `pdf2image==1.17.0`, `httpx==0.27.0`, `duckduckgo-search==6.2.6`, `python-dotenv==1.0.1`.

## Variáveis de ambiente

Ver `.env.example`. As que importam em produção:

| Variável                  | Função                                          | Obrigatória |
|---------------------------|-------------------------------------------------|-------------|
| `TELEGRAM_BOT_TOKEN`      | Token do bot (BotFather)                        | sim         |
| `TELEGRAM_CHAT_ID`        | Chat autorizado (sem ele, deny-all)             | sim         |
| `ANTHROPIC_API_KEY`       | Claude API                                      | sim         |
| `MEM0_API_KEY`            | Mem0 hosted                                     | sim         |
| `GITHUB_TOKEN`            | Token com escopo `repo` em `Gustpbbr/Gus`       | sim         |
| `GITHUB_REPO`             | Default `Gustpbbr/Gus`                          | não         |
| `MODEL_DEFAULT`           | Default `claude-sonnet-4-6`                     | não         |
| `MAX_TOKENS_RESPONSE`     | Default 2048                                    | não         |
| `HARD_LIMIT_USD_MONTH`    | Default 30                                      | não         |
| `MAX_HISTORY_MESSAGES`    | Default 20                                      | não         |
| `LOG_DIR`                 | Default `logs`                                  | não         |

Nome **é `MODEL_DEFAULT`**, não `CLAUDE_MODEL`. Se configurar `CLAUDE_MODEL` no Railway, vai ser ignorado.

## O que não existe ainda no código

- Testes automatizados (nem pytest nas dependências)
- Scan de dados sensíveis antes de salvar no GitHub
- Rate limiting por unidade de tempo
- Relatório agregado de custos (só total do mês)
- Transcrição de áudio do Telegram
- Custom GPT, Alexa Skill, fila de ações

Tudo isso está mapeado em [[gus-04-seguranca-protecao]], [[gus-05-portas-capacidades]] e [[gus-06-autonomia-acoes]].

Relacionado: [[gus-01-visao-geral]], [[gus-03-configuracao-manual]], [[gus-04-seguranca-protecao]]
