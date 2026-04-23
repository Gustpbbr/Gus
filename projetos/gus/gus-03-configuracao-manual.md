---
tipo: documentacao-projeto
projeto: gus
parte: 3-de-7
atualizado: 2026-04-23
---

# Gus — Configuração manual (Fase 1)

Tudo aqui é o que o Gustavo executa pelo navegador/celular. Nenhuma etapa exige escrever código.

## Pré-requisito: revogar chaves expostas

Antes de qualquer deploy: **revogar todas as chaves que possam ter aparecido em conversas anteriores**.

1. **Telegram Bot Token** — no app, abrir `@BotFather`, mandar `/revoke`, escolher o bot. BotFather devolve um token novo.
2. **Anthropic API Key** — `console.anthropic.com` → API Keys → deletar a antiga, criar nova.
3. **Mem0 API Key** — `app.mem0.ai` → Dashboard → rotacionar a key.
4. **GitHub Token** — `github.com/settings/tokens` → revogar tokens antigos, criar novo com escopo `repo` (só o que precisa).

Guardar as 4 novas num gerenciador de senhas. Não colar em chat público em hipótese nenhuma.

## 1. Deploy no Railway (~20 min)

1. Acessar `railway.app`, login com GitHub.
2. **New Project** → **Deploy from GitHub repo** → `Gustpbbr/Gus`.
3. Railway detecta o `Dockerfile` e o `railway.toml` — build começa automático.
4. Em **Variables**, adicionar (copiar nome exato):

```
TELEGRAM_BOT_TOKEN=<novo token do BotFather>
TELEGRAM_CHAT_ID=<deixar vazio por enquanto>
ANTHROPIC_API_KEY=<nova key>
MEM0_API_KEY=<nova key>
GITHUB_TOKEN=<novo token com escopo repo>
GITHUB_REPO=Gustpbbr/Gus
```

Variáveis opcionais (só se quiser mudar do default):
```
MODEL_DEFAULT=claude-sonnet-4-6
HARD_LIMIT_USD_MONTH=30
MAX_TOKENS_RESPONSE=2048
```

O nome correto é **`MODEL_DEFAULT`** — não `CLAUDE_MODEL`.

5. Clicar em **Deploy**. Aguardar o log indicar `Gus iniciado. Aguardando mensagens...`

## 2. Descobrir o chat_id e ativar o bot (~5 min)

O bot começa em modo **deny-all** — ele ignora qualquer mensagem enquanto `TELEGRAM_CHAT_ID` estiver vazio, exceto o comando `/start`.

1. No Telegram, abrir a conversa com o bot novo.
2. Mandar `/start`.
3. O bot responde: `Seu chat_id é: <número>`.
4. Copiar o número, voltar no Railway, preencher `TELEGRAM_CHAT_ID` com ele e fazer redeploy.
5. Mandar "oi" pro bot. Se responder, está vivo.

Se não responder, conferir os logs do Railway (Deployments → View Logs).

## 3. Google Drive sync via Service Account (~30 min)

1. **Criar projeto no Google Cloud** — `console.cloud.google.com` → New Project → nome `gus-drive-sync`.
2. **Habilitar a API** — APIs & Services → Library → buscar "Google Drive API" → Enable.
3. **Criar Service Account** — IAM & Admin → Service Accounts → Create → nome `gus-sync`.
4. **Gerar chave JSON** — na service account criada → Keys → Add Key → Create new key → JSON. Baixa um arquivo `.json`.
5. **Pasta raiz no Drive** — criar pasta `Gus-Sync` no Drive pessoal.
6. **Compartilhar a pasta com a service account** — clicar direito na pasta → Compartilhar → colar o `client_email` que está no JSON → dar permissão de Editor.
7. **Pegar o ID da pasta** — abrir a pasta no browser, copiar o ID da URL (`drive.google.com/drive/folders/<ID_AQUI>`).
8. **Configurar secrets no GitHub** — `github.com/Gustpbbr/Gus/settings/secrets/actions` → New secret:
   - `GOOGLE_CREDENTIALS` = conteúdo completo do JSON (copiar tudo, incluindo `{` e `}`).
   - `DRIVE_ROOT_FOLDER_ID` = o ID da pasta.
9. **Testar** — fazer qualquer commit que altere um `.md` de conteúdo (ex: criar `capturado/misc/teste.md`). O workflow `Sync MD to Google Drive` deve rodar e criar o Google Doc.

O sync **não espelha** `CLAUDE.md`, `README.md`, nem arquivos em `gus/`, `docs/` ou `.github/` — só conteúdo (saúde, projetos, receitas, etc). Isso evita poluir o Drive com código e documentação técnica.

## 4. MCP Mem0 no Claude Code (~5 min)

O servidor MCP está em `.claude/mcp/mem0_server.py` e expõe `buscar_memorias`, `salvar_memoria`, `listar_memorias`. Para habilitar no Claude Code (esta sessão):

1. Instalar deps localmente no ambiente do Claude Code: `pip install mem0ai mcp`.
2. Configurar o MCP em `.claude/settings.json` (projeto) ou `~/.claude.json` (usuário). Exemplo mínimo para o settings do projeto:

```json
{
  "mcpServers": {
    "mem0-gus": {
      "command": "python",
      "args": [".claude/mcp/mem0_server.py"],
      "env": {
        "MEM0_API_KEY": "<sua key>"
      }
    }
  }
}
```

3. Reiniciar o Claude Code. As três tools aparecem disponíveis.
4. Testar: pedir pro Claude "lista minhas memórias no Mem0". Deve retornar o conteúdo que o bot do Telegram salvou.

## 5. Obsidian + plugins (~20 min)

1. Baixar Obsidian (`obsidian.md`) no PC.
2. **Open folder as vault** → apontar para a pasta local do repo clonado.
3. Instalar plugins da comunidade:
   - **Obsidian Git** — sync automático com GitHub (pull a cada 10min, commit+push ao editar).
   - **Obsidian Skills (kepano)** — inclui cli, markdown, bases, canvas, defuddle. Habilita dashboards queryáveis a partir de frontmatter.
4. Abrir um `.md` qualquer e verificar Graph View — os wikilinks devem aparecer como conexões.

## 6. Claude Chat como Project (~5 min)

1. `claude.ai` → Projects → New.
2. Nome: `Gus`.
3. **Instructions**: colar o conteúdo de `gus/gus-identity.md`.
4. (Opcional) Conectar integrações do Google Drive para leitura da pasta `Gus-Sync`.

Agora o app Claude tem o mesmo contexto que o bot do Telegram e o Claude Code — só com personalidade neutra em vez da do Gus.

## Ordem recomendada

1 → 2 (bot vivo já desbloqueia o uso principal)
3 (sync Drive, vale a pena antes do uso intenso)
4 → 5 → 6 (qualidade de vida — dá pra pausar aqui)

## Validação final

- [ ] Bot responde "oi" no Telegram com contexto de projetos
- [ ] Um `.md` criado via Telegram aparece no GitHub em minutos
- [ ] Esse mesmo `.md` aparece no Google Drive como Google Doc em alguns minutos
- [ ] Claude Code consegue listar memórias via MCP
- [ ] Obsidian Graph View mostra wikilinks entre arquivos

Se tudo isso passou, Fase 1 está completa.

Relacionado: [[gus-02-implementado]], [[gus-04-seguranca-protecao]]
