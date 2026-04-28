# Gus — agente pessoal multi-portas

Sistema do Gustavo Pratti de Barros (anestesiologista/pesquisador IA brasileiro).
Uma identidade única acessível por múltiplos canais que compartilham memória,
princípios e arquivos.

> **Não programa direto** — todo código é escrito pela IA via conversa, ele
> revisa e aprova. Comunicação em português brasileiro informal, crítica
> direta bem-vinda.

---

## Mapa do repositório

### 🟢 Arquitetura ativa (faz o projeto funcionar)

| Pasta | Função | Quem lê / escreve |
|---|---|---|
| **`gus/`** | Código do bot Telegram (Sonnet 4.6, ~22 tools) | Railway roda 24/7 |
| **`hub/`** | Hub Qdrant — schemas, store, curador híbrido (Haiku × Sonnet) | Bot + crons + MCP |
| **`api/`** | FastAPI exposta pra Custom GPT (futuro) | Railway (segundo deploy) |
| **`dialogos/`** | Protocolo entre portas — inboxes, streams, archive, _bootstrap | Todas as portas |
| **`pessoal/`** | Saúde, financeiro, diário, Paty dos Alferes (terreno+casa) | Gustavo + bot |
| **`dimagem/`** | Clínica — protocolos, casos, dia (LGPD: pseudônimo em casos) | Bot extrai OS automático |
| **`projetos/`** | Phronesis-Bench, MGE, TER, Axon, Gus | Gustavo + Claude Chat |
| **`agenda/`** | Agenda mensal | Wikilinks |
| **`acoes/`** | Fila de ações pendentes (executor a desenvolver) | Bot enfileira |
| **`capturado/`** | Captura rápida (links, ideias, misc) | Bot salva |
| **`receitas/`** | Receitas (doces, salgadas) | Pessoal |
| **`sensivel/`** | Dados protegidos (NÃO sincroniza pro Drive) | Bot scan + manual |

### ⚙️ Configuração e infra

| Pasta/arquivo | Função |
|---|---|
| `.claude/` | Config Claude Code (MCPs `mem0-gus` e `gus`, hooks `scan_sensivel` + retro-engine) |
| `.github/` | 16 workflows (cron diário/semanal + dispatch) + scripts |
| `.obsidian/` | Config Obsidian (uso local do Gustavo) |
| `Dockerfile`, `railway.toml`, `requirements.txt` | Deploy bot Telegram no Railway |
| `.mcp.json` | Config dos MCP servers do Claude Code |
| `CLAUDE.md` | Briefing automático lido a cada sessão Claude Code |
| `.env.example` | Template de variáveis de ambiente |
| `.gitignore` | Ignora `.env`, `__pycache__/`, `secrets/`, `get_token.py` |

### 📊 Auditorias e logs (gerados automaticamente)

| Pasta | Conteúdo |
|---|---|
| `_indices/` | MOCs por área + auditoria diária do Hub (`_auditoria-mem0.md`, gerado por cron 6h BRT) |
| `_log/` | Curador (`resumos-mem0/`), Retro Engine (`retro-engine-claude-code/`), sessões (`sessoes-claude-code/`) |

### 📤 Outputs públicos

| Arquivo | Função |
|---|---|
| `gus-memoria-export.md` / `.json` | Export diário do Hub Qdrant (cron 3h BRT). Sincroniza pro Drive. |

### 📦 Histórico (deletável sem impacto)

`historico/` — versões antigas, scripts de uso único, setup docs feitos uma vez.
Ver `historico/README.md` pro detalhamento. Reorganizado em 28/04/2026 pra
desinchar a raiz.

---

## Arquitetura em 1 desenho

```
                        ┌──────────────────────────────┐
                        │  Hub Qdrant (gus_hub)        │  ← memória única
                        │  GitHub vault (este repo)    │  ← conhecimento único
                        │  gus-identity.md             │  ← identidade única
                        └─────────────┬────────────────┘
                                      │
        ┌──────────────┬──────────────┼──────────────┬───────────────┐
        │              │              │              │               │
   Telegram       Claude Code     Claude Chat    Custom GPT      Alexa
   (@Tiogubot)    (esta sessão)   (claude.ai)    (mobile)        (casa)
   Sonnet 4.6     Sonnet 4.6      Sonnet 4.6     GPT-5           futuro
   ATIVO          ATIVO           ATIVO          em setup        roadmap
```

---

## Documentos canônicos pra entender o sistema

Ler em ordem:

1. **`CLAUDE.md`** — briefing curto, lido por cada sessão Claude Code
2. **`projetos/gus/_estado-atual.md`** — handoff entre sessões (atualizado 27/04)
3. **`projetos/gus/gus-12-portas-futuras.md`** — diretriz arquitetural multi-portas
4. **`projetos/gus/gus-13-tags-canonicas.md`** — taxonomia de tags `via` no Hub
5. **`projetos/gus/gus-25-roadmap-ativacao.md`** — roadmap de ativação das portas
6. **`projetos/gus/gus-26-status-consolidado.md`** — status consolidado
7. **`projetos/gus/gus-27-protocolo-portas-tools.md`** — crivo arquitetural pra novas portas/tools
8. **`dialogos/README.md`** — protocolo de comunicação entre portas
9. **`historico/README.md`** — o que está arquivado e por quê

---

## Estado atual (27-28/04/2026)

- ✅ Bot Telegram em produção (Railway 24/7) com 22 tools
- ✅ Hub Qdrant ativo, curador híbrido salvando (coleta dual até 12/05/2026)
- ✅ Mem0 SaaS aposentado pelo ADR-001 (só fallback de leitura até Fase 5)
- ✅ Sync GitHub ↔ Drive bidirecional (cron 15min)
- ✅ Roteamento Estágio 0 (notificação) + Estágio 1 (`rotear_arquivo`) implementados
- ⏳ Custom GPT — Action depende de Builder DESKTOP
- ⏳ Suporte a vídeo no Telegram — sem `filters.VIDEO` registrado
- ⏳ Decisão modelo curador final (Fase 5 ADR-001) — após 12/05

Detalhes em `projetos/gus/_estado-atual.md`.

---

## Como usar (você, Gustavo)

- **Conversa diária** → Telegram (@Tiogubot) — texto, foto, PDF, Word, Excel, voz
- **Reflexão longa** → Claude Chat (claude.ai) — Project com `gus-bootstrap` ativo
- **Mexer em código** → este Claude Code (web ou desktop)
- **Pedir resumo do que TioGu/Chat disse** → tool `read_from_github` ou Claude Chat lê do Drive

## Quem mais lê este repo

- Bot do Telegram (Railway): código + system_prompt
- 16 workflows GitHub Actions: scripts + crons
- Sync GitHub → Drive (espelho público + sandbox de demandas)
- Sync Drive → GitHub (workflow `import-from-drive.yml`)
