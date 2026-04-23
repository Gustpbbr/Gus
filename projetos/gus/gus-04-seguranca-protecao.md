---
tipo: documentacao-projeto
projeto: gus
parte: 4-de-7
atualizado: 2026-04-23
---

# Gus — Segurança e proteção

## O que já protege (implementado)

| Vetor de ataque                    | Proteção                                                                  | Onde (arquivo:linha)                 |
|------------------------------------|---------------------------------------------------------------------------|--------------------------------------|
| Usuário não autorizado             | `_autorizado()` nega tudo se `TELEGRAM_CHAT_ID` vazio ou diferente        | `gus/bot.py:22-25`                   |
| Path traversal em ler/salvar       | Regex `^[a-zA-Z0-9\-_/]+$` + bloqueio explícito de `..`                   | `gus/tools.py:15-25`                 |
| Filename injection                 | Bloqueia `/` e `..` no nome do arquivo                                    | `gus/tools.py:153`                   |
| Loop infinito de tool use          | `max_tool_rounds = 10`; devolve mensagem de segurança                     | `gus/llm.py:47, 97`                  |
| Estouro de custo mensal            | `HARD_LIMIT_USD_MONTH` (default 30), checado a cada mensagem              | `gus/bot.py:28-36`                   |
| API da Anthropic travada           | `timeout=120` no cliente                                                  | `gus/llm.py:26`                      |
| GitHub/busca web travados          | `httpx.AsyncClient(timeout=30)` em todas as chamadas                      | `gus/tools.py`                       |
| Mem0 save fora de sincronia        | `asyncio.create_task` em background — falha não bloqueia resposta         | `gus/bot.py:62-71`                   |
| PDF sem texto (escaneado)          | Fallback automático pra renderização visual (máx 10 páginas)              | `gus/media.py:81-99`                 |
| PDF gigante                        | Texto truncado em 500k caracteres                                         | `gus/media.py:12, 73-78`             |
| Arquivo inexistente no GitHub      | 404 retorna mensagem amigável                                             | `gus/tools.py:122`                   |

Tokens novos nos secrets, nunca commitados — `.env` está no `.gitignore`.

## Gaps conhecidos

Coisas que o código ainda não trata e que podem virar problema:

1. **Dados sensíveis em texto livre** — nada impede o Gus de salvar CPF, cartão, senha ou API key num `.md` público do repo. Se o Gustavo pedir "salva essa nota fiscal aqui", vai salvar com tudo.
2. **Sem rate limiting** — se algo disparar mensagens em série, o bot responde todas até bater `HARD_LIMIT_USD_MONTH`. Gasta antes de o limite cortar.
3. **Sem backup do Mem0** — existe o export diário em `gus-memoria-export.md`, mas é só texto. Se o Mem0 perder a base, não tem restore automático.
4. **Sem health check externo** — se o Railway cair sem restart, o Gustavo só descobre quando tentar usar.
5. **DuckDuckGo é ponto único de falha pra busca web** — se o serviço bloquear ou falhar, o Gus fica sem web search.
6. **Sem scan de secrets no commit** — se o Claude gerar um `.md` com uma API key, vai pro GitHub público.
7. **Logs locais somem em redeploy** — `logs/gus_metrics.jsonl` fica no container do Railway, não persiste. Métricas de custo mensal zeram se o container for recriado.

## Fase 2 — reforços planejados

Ordem por impacto × esforço:

### Alta prioridade

**Scan de dados sensíveis antes de `save_to_github`.** Regex para CPF, CNPJ, cartão (Luhn), padrões de API key comuns (`sk-ant-`, `ghp_`, `m0-`, etc). Se detectar, o Gus pergunta antes de salvar. Implementar em `gus/tools.py` antes do encode base64.

**Backup versionado do Mem0.** O export diário hoje é texto — reformatar `.github/scripts/export_mem0.py` para também salvar `gus-memoria-export.json` com estrutura completa (id, metadata, timestamps). Permite restore via `client.add` em loop.

**Persistir `logs/` em volume.** Configurar volume no Railway apontando para `/app/logs`. Sem isso, `custo_mes_atual()` perde histórico a cada redeploy e o `HARD_LIMIT` pode ser burlado sem querer.

### Média prioridade

**Fallback de busca web.** Adicionar Brave Search API como segunda opção em `_search_web`. Se DuckDuckGo falhar ou retornar vazio, tentar Brave. Requer `BRAVE_API_KEY` (free tier existe).

**Rate limiting.** Contar mensagens por janela de 60s no `bot.py`. Se passar de N, responder "tô recebendo mensagens rápido demais, aguenta aí". Protege contra loop acidental e abuso.

**Health check externo.** UptimeRobot ou cron do GitHub Actions batendo numa rota `/health` (requer adicionar HTTP server simples no bot, ou trocar polling por webhook). Notifica via Telegram se o bot cair por mais de 5min.

### Baixa prioridade

**Auto-teste diário das tools.** GitHub Action que dispara um prompt teste pro bot e valida resposta. Detecta regressão em `read_from_github`, `search_web`, `save_to_github`.

**Relatório agregado de custos.** Já existe `logger.py` com JSONL. Adicionar script que lê o arquivo e gera `gus-custos-semana.md` toda segunda-feira, commitado pelo GitHub Action. Permite visualização por modelo, por tipo de interação, por horário.

**Scan de secrets no commit.** Hook no GitHub Actions usando `gitleaks` ou `trufflehog` que rejeita PR com secrets. Dobra a proteção contra o scan feito antes do save.

## Princípio

Proteção em camadas. Nenhuma defesa única é suficiente — scan antes de salvar, gitleaks no commit, `.gitignore` no worktree, tokens com escopo mínimo, `.env` nunca commitado. Se uma camada falha, as outras contêm.

## Anti-padrão a evitar

Não desligar o `HARD_LIMIT_USD_MONTH` "só pra testar". Se passar uma vez, volta zerado no mês seguinte — nada a consertar. Se ignorar e usar, pode comer US$100+ num loop noturno que ninguém viu.

Relacionado: [[gus-02-implementado]], [[gus-03-configuracao-manual]], [[gus-07-decisoes-descartadas]]
