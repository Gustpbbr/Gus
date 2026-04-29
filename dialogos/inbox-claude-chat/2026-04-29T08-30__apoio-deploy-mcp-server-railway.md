---
tipo: demanda
origem: claude-code
destino: claude-chat
prioridade: media
status: pendente
criado_em: 2026-04-29T08:30:00-03:00
processado_em: ""
processado_por: ""
acao_sugerida: manter
destino_path: ""
contexto: "Apoio visual pra Gustavo deployar MCP server no Railway (gus-28 Passo 2). Gustavo vai mandar screenshots da tela pedindo orientacao, voce guia passo a passo."
---

# Apoio: deploy do MCP server no Railway (gus-28 Passo 2)

Claude Chat, esta demanda eh um pedido de **orientacao visual interativa** pro
Gustavo durante o deploy do MCP server no Railway. Ele vai te mandar screenshots
da tela do Railway e do claude.ai, e voce deve guia-lo passo a passo. Tudo que
precisa saber esta abaixo.

---

## Contexto: o que estamos fazendo e por que

O **Claude Code** acabou de implementar o **Passo 2 do gus-28** (acesso real-time
do Claude Chat ao Hub Qdrant via MCP). Essa eh a feature que vai te dar 9
ferramentas pra consultar e ingerir memorias em tempo real, sem depender do
snapshot estatico das 03h.

A implementacao tecnica esta pronta no PR (branch `claude/passo2-mcp-server`).
O codigo esta em:
- `hub/mcp_server.py` — servidor MCP com 9 tools
- `Dockerfile.mcp` — container separado do bot Telegram
- `projetos/gus/gus-28-passo2-mcp-server.md` — guia de setup completo

**O que falta:** o Gustavo precisa fazer o deploy no Railway e conectar voce
em claude.ai. Sao ~5min mas tem detalhes de UI que ficam mais faceis com
screenshots ao vivo.

---

## Arquitetura do deploy

```
Railway Project: Gus  (mesmo projeto, ja existente)
├── Service: tiogu-bot         (ja roda)
└── Service: gus-mcp-server    (NOVO — vai criar agora)
                |
                v
           Qdrant Cloud (gus_hub) — fonte unica de verdade
                ^
                |
           claude.ai Connector (apontando pro MCP server via Bearer auth)
```

**Importante:**
- Mesmo projeto Railway. NAO eh nova assinatura. NAO eh nova conta.
- Custo extra: ~$1-3/mes adicional ao plano atual.
- Bot Telegram continua rodando normal, em paralelo.

---

## Etapas que voce vai guiar

### Etapa 1 — Gerar token de auth (`MCP_BEARER_TOKEN`)

Esse token protege o MCP de acesso indevido. Gera uma vez, guarda em local
seguro (vai usar 2 vezes: no Railway e no claude.ai).

**Sugira ao Gustavo:**
- Opcao A: site uuidgenerator.net — ele pega 2 UUIDs, junta sem hifen, vira
  uma string de ~64 chars
- Opcao B: se ele estiver no terminal, `openssl rand -hex 32`

Depois de gerar, **insiste pra ele copiar pra um lugar seguro** (Notes app,
1Password, etc.). Vai precisar dele agora e nao da pra recuperar depois sem
gerar novo.

### Etapa 2 — Criar serviço novo no Railway

Gustavo vai abrir o Railway no celular ou desktop. Quando ele mandar screenshot
da dashboard:

1. Confirme que ele esta no projeto **Gus** (nao em outro projeto)
2. Ele toca no botao **+ New Service** (ou icone de "+")
3. Escolhe **Deploy from GitHub Repo**
4. Seleciona o repo **Gustpbbr/Gus**
5. Branch: **main**

O Railway vai comecar um deploy automatico que **vai falhar**. Isso eh esperado:
o servico novo por default tenta usar o Procfile ou comando do bot, e
precisamos apontar pro Dockerfile.mcp.

6. Vai em **Settings → Build**
   - **Builder:** Dockerfile (nao Nixpacks, nao Heroku Buildpacks)
   - **Dockerfile Path:** `Dockerfile.mcp` (com ponto, nao barra)
   - Salva
7. (Opcional) Em **Settings**, renomeia o service pra `gus-mcp-server` ou
   similar pra distinguir do bot

### Etapa 3 — Configurar variaveis de ambiente

Esta eh a etapa mais critica. Sao 6 variaveis. Algumas sao copiadas do bot
(que ja roda no Railway), outras sao novas.

Variaveis necessarias:

| Variavel | Valor | Como conseguir |
|---|---|---|
| `QDRANT_URL` | URL Qdrant Cloud | **Copia do bot** — abre service do bot, Variables, copia esse valor |
| `QDRANT_API_KEY` | API key Qdrant | **Copia do bot** |
| `MCP_BEARER_TOKEN` | token gerado Etapa 1 | Cola o valor que ele gerou |
| `GH_TOKEN` | Personal Access Token GitHub | **Copia do bot** |
| `GH_REPO` | `Gustpbbr/Gus` | Pode digitar direto |
| `PORT` | `8000` | Pode digitar direto (Railway pode override automatico) |

**Como copiar do bot:** abre o service do bot Telegram → Variables → toca no
valor de cada variavel → copy. Volta no service MCP → Variables → New Variable
→ cola.

Depois de salvar todas, Railway faz rebuild automatico.

### Etapa 4 — Gerar dominio publico

claude.ai precisa de uma URL HTTPS pra conectar.

1. Em **Settings → Networking**
2. **Generate Domain**
3. Aparece algo tipo `gus-mcp-server-production.up.railway.app`
4. **Copia essa URL** — vai usar na proxima etapa

### Etapa 5 — Validar que o MCP subiu

Antes de conectar no claude.ai, testa o /health pra confirmar que o servico
subiu certo.

Pede pro Gustavo abrir no navegador:
```
https://<dominio-dele>.up.railway.app/health
```

Resposta esperada (JSON):
```json
{"status": "ok", "service": "gus-hub-mcp"}
```

Se aparecer 503, eh sinal de que o `MCP_BEARER_TOKEN` nao foi configurado.
Refazer Etapa 3.

Se aparecer erro de DNS / 404 / loading infinito, o Railway ainda esta
buildando — espera 2-3 min e tenta de novo.

Se aparecer outro erro, pede pra Gustavo abrir **Logs** do service no Railway
e te mandar screenshot da ultima linha.

### Etapa 6 — Conectar voce no claude.ai

Esta etapa eh visual no claude.ai. Pode ser celular ou desktop, mas desktop
eh mais facil pra typar a URL.

1. Abre **claude.ai** → **Settings** → **Connectors**
2. **Add MCP Server**
3. Preenche:
   - **Name:** `Gus Hub`
   - **URL:** `https://<dominio>.up.railway.app/mcp` — (atencao: termina em
     `/mcp`, nao em `/`)
   - **Auth Type:** Custom header
   - **Header Name:** `Authorization`
   - **Header Value:** `Bearer <MCP_BEARER_TOKEN>` — (atencao: tem a palavra
     "Bearer" + espaco + o token; sem aspas)
4. Salva

claude.ai vai testar a conexao. Se OK, aparece status verde + lista das 9
tools. Se falhar, geralmente eh:
- URL sem `/mcp` no final
- Bearer sem espaco depois
- Token errado

### Etapa 7 — Teste end-to-end

Em conversa nova no Claude Chat (modo Gus), peca pro Gustavo perguntar:

> "Quantos fragmentos eu tenho no Hub?"

Voce, Claude Chat, deve chamar a tool `contar_fragmentos()` e responder com
os numeros reais (algo tipo "19 no brain gustavo, X no brain gus").

Outro teste:
> "Busca no hub coisas sobre Dimagem"

Voce deve chamar `buscar_hub("Dimagem")` e voltar fragmentos com timestamps.

Teste de escrita:
> "Salva no hub que eu deployei o MCP server hoje"

Voce deve chamar `ingestar_fragmento(...)` com `via='claude-chat'` automatico
(o servidor garante isso, voce nao precisa setar). Confirma com:
> "Lista os ultimos 3 fragmentos com via=claude-chat"

---

## Tools disponiveis (pra voce saber o que tem)

| Tool | Funcao |
|---|---|
| `buscar_hub(query, limit, area?)` | Busca semantica |
| `ego_cache_atual(user_id)` | Identidade + decisoes recentes |
| `fragmentos_recentes(horas, limit)` | Janela temporal |
| `buscar_por_tipo(tipo, limit)` | Filtro por tipo |
| `buscar_por_area(area, limit)` | Filtro por area |
| `contar_fragmentos()` | Total + breakdown |
| `ingestar_fragmento(...)` | Escrita (via=claude-chat hardcoded) |
| `read_repo_file(path)` | Le .md do GitHub direto |
| `list_repo_dir(path)` | Lista pasta do repo |

---

## Troubleshooting comum

**"Build falha no Railway com Dockerfile not found"**
→ Em Settings → Build → Dockerfile Path deve estar `Dockerfile.mcp` (ponto, nao barra)

**"/health responde mas claude.ai diz Connection failed"**
→ A URL do connector deve terminar em `/mcp` (nao em `/` nem em `/health`)
→ O header deve ser exatamente `Bearer <token>` (com espaco)

**"Claude Chat conecta mas nao usa as tools"**
→ Em conversa nova, pede algo que exija dados do Hub
→ Connector pode estar inativo — verifica toggle em Settings → Connectors
→ Pode haver banner "Tools disponiveis" no comeco da conversa

**"Cold start lento (3-5s na primeira chamada)"**
→ Esperado. Railway poe service em sleep apos inatividade. Proxima chamada acorda.

---

## Quando terminar

Depois de validar que esta tudo funcionando, **avise o Gustavo** pra:

1. Mandar uma mensagem aqui no Claude Chat reportando sucesso
2. Nas proximas 1-2 semanas, usar o MCP normalmente em conversas pra validar uso real
3. Apos validacao, podemos planejar o **Passo 3** (NeuroGus em producao) e o
   **Passo 4** (Artifact SSE)

---

## Referencias completas (caso voce queira mais contexto)

- Design doc gus-28: `projetos/gus/gus-28-acesso-hub-claude-chat.md`
- Setup guide tecnico: `projetos/gus/gus-28-passo2-mcp-server.md`
- Codigo MCP server: `hub/mcp_server.py`
- Branch da implementacao: `claude/passo2-mcp-server`

## Resultado
