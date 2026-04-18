---
criado_em: 2026-04-18
tipo: documentacao-projeto
status: pendente
fase: 2
---

# Gus — Segurança e Proteção (Fase 2)

Melhorias defensivas para depois do deploy básico estar funcionando.

## Já implementado

- [x] Auth deny-all (bot ignora sem TELEGRAM_CHAT_ID)
- [x] Path traversal protection (regex + bloqueio de `..`)
- [x] Timeout Anthropic (120s) e httpx (30s)
- [x] Loop de tools limitado (max 10 rounds)
- [x] Filename validation

## A implementar

### 1. Scan de dados sensíveis antes de salvar no GitHub
- **O quê**: antes de salvar um .md via save_to_github, escanear o conteúdo por padrões de dados sensíveis (CPF, cartão de crédito, senhas, API keys)
- **Como**: regex patterns no tools.py, antes do push. Se detectar, avisa o Gustavo e não salva.
- **Onde**: `gus/tools.py`, função `_save_to_github`
- **Prioridade**: alta

### 2. Auto-teste diário das tools
- **O quê**: GitHub Action que testa se as 3 tools respondem corretamente
- **Como**: script Python que faz chamada de teste a cada tool (busca web simples, lê um .md conhecido, salva e deleta um .md de teste)
- **Onde**: `.github/scripts/test_tools.py` + `.github/workflows/test-tools.yml`
- **Prioridade**: média
- **Frequência**: diária (cron) + manual

### 3. Backup do Mem0 (JSON versionado)
- **O quê**: além do export .md diário, salvar dump completo em JSON com metadados
- **Como**: expandir export_mem0.py para gerar também `backups/mem0-YYYY-MM-DD.json`
- **Onde**: `.github/scripts/export_mem0.py`
- **Prioridade**: média

### 4. Health check externo
- **O quê**: monitorar se o bot está online e respondendo
- **Como**: opções:
  - UptimeRobot (free tier) pingando endpoint HTTP do Railway
  - Ou GitHub Action que envia mensagem de teste via Telegram API e verifica resposta
- **Onde**: externo ao código
- **Prioridade**: baixa (Railway já tem restart automático)

### 5. Fallback de busca web
- **O quê**: se DuckDuckGo falhar, ter alternativa
- **Como**: tentar Brave Search API ou SearXNG como fallback no _search_web
- **Onde**: `gus/tools.py`
- **Prioridade**: baixa

### 6. Rate limiting
- **O quê**: limitar número de mensagens por minuto para evitar abuse/custos inesperados
- **Como**: contador in-memory com janela de tempo no bot.py
- **Onde**: `gus/bot.py`
- **Prioridade**: baixa (bot é single-user)

### 7. Log de custos agregado
- **O quê**: além do JSONL por chamada, ter resumo diário/semanal de gastos
- **Como**: GitHub Action que processa o JSONL e gera relatório
- **Onde**: `.github/scripts/cost_report.py`
- **Prioridade**: baixa

## Modelo de ameaças (para bot pessoal)

| Ameaça | Mitigação atual | Status |
|--------|----------------|--------|
| Acesso não autorizado | Auth deny-all | ✅ |
| Path traversal | Regex + bloqueio `..` | ✅ |
| Loop infinito de tools | Max 10 rounds | ✅ |
| API timeout/hang | Timeouts configurados | ✅ |
| Dados sensíveis no GitHub | — | ⏳ A fazer |
| Bot offline sem aviso | — | ⏳ A fazer |
| Mem0 sem backup | Export .md diário | ⚠️ Parcial |
| Custo descontrolado | Log por chamada | ⚠️ Parcial |

Relacionado: [[gus-02-implementado]], [[gus-03-configuracao-manual]], [[gus-05-portas-capacidades]]
