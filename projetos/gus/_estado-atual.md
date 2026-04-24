---
tipo: estado-atual-sessao
atualizado: 2026-04-24
---

# Estado atual — handoff entre sessões

Documento vivo. Atualizar no final de cada sessão que deixa algo no meio.

## Última sessão (2026-04-24 fim de tarde) — Drive Inbox + regras de save + agendas

### Apps Script Drive Inbox → GitHub
- Claude Projetos (e qualquer app com Drive) pode salvar `.md` em `Gus-Sync/Inbox/`
- Apps Script varre a pasta a cada 5min, empurra pro GitHub via API, move pra `Inbox/Processado/`
- Código: `.github/scripts/drive_inbox_to_github.gs`
- Guia passo-a-passo: `docs/drive-inbox-setup.md`
- Extrai path destino do frontmatter `github_path:`; fallback `capturado/misc/`
- **Próximo passo externo do Gustavo:** configurar o trigger `processInbox` a cada 5min no script.google.com (em andamento nesta sessão)

### Fix no sync de ida (GitHub → Drive)
- Antes: `.md` virava Google Doc convertido (perdia formato puro)
- Agora: salva como texto puro (`mimetype="text/plain"`), sem conversão
- Adicionado workflow `sync-to-drive-full.yml` (dispatch manual) pra re-subir tudo quando precisar

### 3 regras obrigatórias de comportamento ao salvar (system_prompt.md)
- **Regra 1** — salvar direto, sem perguntar "posso salvar?"; exceção é scan de sensível
- **Regra 2** — confirmar imediatamente após sucesso com path + 1 linha do conteúdo
- **Regra 3** — antes de re-salvar, usar `list_commits(path=..., since_days=1)` pra ver se já tem commit recente

### Agendas mensais capturadas (estrutura vazia)
- `agenda/abril-2026.md`, `agenda/maio-2026.md`, `agenda/junho-2026.md`
- Semanas e dias prontos, eventos a preencher via bot

## Sessão 2026-04-24 tarde — Obsidian + Drive sync

### Obsidian configurado no PC
- Vault aberto em `C:\Gus\Gus` apontando pro repo clonado via GitHub Desktop
- Plugins ativos: **Obsidian Git** (auto commit-and-sync 10min, pull on startup, signs visuais) e **Dataview**
- Grafo de conexões visível — wikilinks entre MDs funcionando
- Author configurado: Gustavo + email GitHub
- `.gitignore` atualizado com `get_token.py`

### Drive sync funcionando ✅
- **3 tentativas até dar certo** — documentado em `docs/drive-sync-setup.md`
- Tentativa 1: service account key JSON — bloqueada por `iam.disableServiceAccountKeyCreation`
- Tentativa 2: Workload Identity Federation — autenticação ok, mas service account não tem Drive storage quota
- Tentativa 3: OAuth2 com refresh token — **funcionou** ✅
- Arquivos `.md` de conteúdo no main → aparecem em `Gus-Sync/` no Drive como Google Docs
- Secrets configurados: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN`, `DRIVE_ROOT_FOLDER_ID`
- `get_token.py` salvo localmente em `C:\Gus\Gus` (não commitado — têm credenciais)

### Infraestrutura base (sessão 23/abr → madrugada 24)
- Deploy Railway com todas variáveis. `TELEGRAM_CHAT_ID=495256549`. Bot responde, usa Mem0, salva/lê GitHub.
- 12 testes funcionais validados em produção via Telegram.

### Features ativas — 13 tools totais no bot
- `read_from_github`, `list_github_directory`, `list_commits`, `search_memory`, `meta_memoria`, `auditoria_mem0`, `salvar_memoria_gus`, `buscar_memoria_gus`, `search_web`, `save_to_github`, `criar_acao`, `disparar_workflow`
- Multimídia: imagens, PDFs, Word, Excel, **áudio/voz via Whisper**

### Workflows GitHub Actions ativos
- `export-mem0.yml` (3h BRT)
- `auditoria-mem0.yml` (6h BRT)
- `briefing-matinal.yml` (7h BRT dias úteis)
- `retrospectiva-semanal.yml` (sexta 20h BRT)
- `reflexao-quinzenal.yml` (sábado 10h BRT semanas pares)
- `sync-to-drive.yml` — **funcionando via OAuth2** ✅
- `sync-to-drive-full.yml` — dispatch manual, re-sincroniza todos os `.md`

## Pendente pra próxima sessão

### Em andamento (ação Gustavo)
- **Apps Script `processInbox`** — criar trigger time-based a cada 5min no script.google.com pra fechar o fluxo Drive Inbox → GitHub

### Prioridade 1 — **Custom GPT no ChatGPT** (próximo passo do caminho Alexa)
- Meu trabalho: ~3-4h (FastAPI, endpoints, OpenAPI, auth, integração com main.py)
- Ação do Gustavo: ~20min (Railway secret, criação do GPT no ChatGPT Builder, teste em voz)
- Conta a usar: `gustavo.pratti84@gmail.com` (já tem ChatGPT Plus)
- Ver detalhes em `gus-10-caminho-alexa.md` Passo 1

### Pendentes menores
- Claude Chat Project — refazer validação com identity.md colado
- `fut-06-voz-telegram.md` pode ser marcado como concluído (Whisper entregue)
- Apagar arquivo de teste `capturado/misc/teste-drive-sync.md` quando quiser

## Decisões tomadas
- Drive sync via OAuth2 (não service account) — única opção viável com Gmail pessoal sem Workspace
- Refresh token não expira enquanto app não for desautorizado — manutenção baixa
- WIF configurado no Google Cloud mas não usado (não atrapalha)

## Bugs em aberto (não bloqueantes)
- Mem0 tem latência de indexação (minutos)
- DDG pode falhar se Tavily esgotar limite mensal

## Como usar este arquivo

1. Próxima sessão: ler PRIMEIRO, depois `gus-10-caminho-alexa.md` se for sessão de dev rumo à Alexa
2. Ao fim da sessão: atualizar "Última sessão" + "Pendente"
3. Commit + push antes de encerrar

Relacionado: [[gus-01-visao-geral]], [[gus-10-caminho-alexa]], [[gus-02-implementado]], [[gus-08-plano-proximos-passos]]
