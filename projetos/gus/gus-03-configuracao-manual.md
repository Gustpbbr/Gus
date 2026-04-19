---
criado_em: 2026-04-18
tipo: documentacao-projeto
status: pendente
fase: 1
---

# Gus — Configuração Manual (Gustavo no PC)

Passos que o Gustavo precisa fazer pelo computador/celular. Não são código — são configurações em plataformas externas.

## Prioridade alta (pré-deploy)

### 1. Revogar chaves expostas
- [ ] Revogar token do Telegram no BotFather → /revoke → gerar novo
- [ ] Revogar API key da Anthropic → console.anthropic.com → gerar nova
- [ ] Revogar API key do Mem0 → dashboard Mem0 → gerar nova
- **Por quê**: chaves foram expostas em conversa. Segurança obrigatória antes de deploy.

### 2. Deploy no Railway
- [ ] Criar conta no Railway (railway.app)
- [ ] Novo projeto → Deploy from GitHub → selecionar Gustpbbr/Gus
- [ ] Configurar variáveis de ambiente:
  - `TELEGRAM_BOT_TOKEN` (novo, do BotFather)
  - `TELEGRAM_CHAT_ID` (495256549)
  - `ANTHROPIC_API_KEY` (nova)
  - `MEM0_API_KEY` (nova)
  - `GITHUB_TOKEN` (gerar Personal Access Token com escopo repo)
  - `GITHUB_REPO` (Gustpbbr/Gus)
  - `CLAUDE_MODEL` (claude-sonnet-4-6-20250514 para custo menor)
- [ ] Deploy automático — Railway detecta Dockerfile

### 3. Testar bot
- [ ] Mandar mensagem no Telegram pro bot
- [ ] Verificar que responde
- [ ] Testar /start e /reset
- [ ] Mandar uma foto e ver se processa
- [ ] Pedir pra salvar algo no GitHub e verificar que criou o .md

## Prioridade média (pós-deploy)

### 4. Configurar Google Drive sync
- [ ] Criar Service Account no Google Cloud Console
- [ ] Habilitar Google Drive API
- [ ] Compartilhar pasta do Drive com email da Service Account
- [ ] Adicionar secrets no GitHub:
  - `GOOGLE_CREDENTIALS` (JSON da Service Account, base64)
  - `DRIVE_FOLDER_ID` (ID da pasta raiz no Drive)
- [ ] Rodar workflow manualmente pra testar

### 5. Configurar MCP Mem0 no Claude Code
- [ ] Adicionar em `.claude/mcp.json`:
```json
{
  "mcpServers": {
    "mem0-gus": {
      "command": "python",
      "args": [".claude/mcp/mem0_server.py"],
      "env": {
        "MEM0_API_KEY": "sua-chave-aqui"
      }
    }
  }
}
```
- [ ] Reiniciar Claude Code
- [ ] Testar: pedir pra buscar memórias

### 6. Configurar Obsidian
- [ ] Baixar Obsidian (obsidian.md)
- [ ] Clonar o repo: `git clone https://github.com/Gustpbbr/Gus.git`
- [ ] Abrir a pasta do repo como vault no Obsidian
- [ ] Instalar plugin "Obsidian Git" (Community Plugins → Browse)
- [ ] Configurar auto-pull a cada 10 minutos
- [ ] Abrir Graph View (Ctrl+G) para ver conexões via wikilinks
- [ ] Instalar Obsidian Skills do kepano (no terminal, na raiz do vault):
```bash
npx skills add git@github.com:kepano/obsidian-skills.git
```
- [ ] Skills instaladas (pasta `/.claude` do vault):
  - **obsidian-cli** — controla o Obsidian rodando (ler, criar, buscar notas)
  - **obsidian-markdown** — garante sintaxe correta (wikilinks, embeds, callouts, frontmatter)
  - **obsidian-bases** — cria views tipo banco de dados sobre os MDs (tabelas, filtros)
  - **json-canvas** — cria mapas visuais (.canvas) com nós e conexões
  - **defuddle** — limpa páginas web e converte pra markdown (alternativa ao WebFetch)

### 7. Configurar Claude Chat (app)
- [ ] Criar Project no Claude com nome "Gus"
- [ ] Colar conteúdo de gus-identity.md nas instruções do projeto
- [ ] Adicionar Google Drive como Knowledge (quando Google Docs estiver sincronizado)

## Checklist resumido

| # | Tarefa | Onde | Tempo estimado |
|---|--------|------|----------------|
| 1 | Revogar chaves | BotFather, Anthropic, Mem0 | 10min |
| 2 | Deploy Railway | railway.app | 20min |
| 3 | Testar bot | Telegram | 5min |
| 4 | Google Drive sync | Google Cloud, GitHub | 30min |
| 5 | MCP Mem0 | .claude/mcp.json | 5min |
| 6 | Obsidian + Skills | Desktop | 20min |
| 7 | Claude Chat | App Claude | 5min |

Relacionado: [[gus-01-visao-geral]], [[gus-02-implementado]], [[gus-04-seguranca-protecao]]
