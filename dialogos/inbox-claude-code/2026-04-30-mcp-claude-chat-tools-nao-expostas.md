---
tipo: demanda
origem: gustavo
destino: claude-code
prioridade: alta
status: pendente
criado_em: 2026-04-30T16:55:00-03:00
processado_em: ""
processado_por: ""
acao_sugerida: investigar
destino_path: hub/mcp_server.py
contexto: "Claude Chat conecta no gus-hub MCP (status verde, 9 tools listadas na UI) mas afirma que não consegue invocar as tools — diz que estão 'só disponíveis dentro de Artifacts'. Investigar se é bug no MCP server (transport/protocol) ou comportamento esperado do Claude Chat web."
---

# Demanda — investigar por que Claude Chat não invoca tools do gus-hub

## TL;DR

O MCP server `gus-mcp-server` tá no ar no Railway, conectado no claude.ai
Connector (status verde, 9 tools listadas), mas o **Claude Chat (web)
afirma que não consegue chamar as tools** do gus-hub diretamente — diz que
"só ficam disponíveis dentro de Artifacts via API calls no browser".

Quando tentou via Artifact, deu erro de CORS (esperado — Artifacts são
sandbox).

**Pergunta chave:** isso é (a) bug no nosso MCP server, (b) comportamento
esperado do Claude Chat web pra MCP de terceiros, ou (c) configuração
faltando do lado do servidor?

---

## Histórico do que já foi feito

### Implementação inicial (gus-28 Passo 2)
- Criado `hub/mcp_server.py` expondo 9 tools do Hub Qdrant via FastMCP
- 9 tools: `buscar_hub`, `ego_cache_atual`, `fragmentos_recentes`,
  `buscar_por_tipo`, `buscar_por_area`, `contar_fragmentos`,
  `ingestar_fragmento`, `read_repo_file`, `list_repo_dir`
- `Dockerfile.mcp` separado pra deploy isolado no Railway
- `railway.mcp.toml` separado do bot Telegram
- Auth via Bearer token (`MCP_BEARER_TOKEN`) com `/health` bypassed

### Bugs corrigidos no caminho
1. **PR #36** — `Optional[str]` em decoradores `@mcp.tool()` quebrava
   FastMCP (TypeError issubclass). Trocado pra `str = ""`.
2. **PR #40** — bump httpx>=0.27.1 (mcp 1.27 exige)
3. **PR #41** — bump pydantic>=2.11 (mcp 1.27 exige)
4. **PR #53** — porta 8000 → 8080 (Railway proxy escuta 8080 por
   default; conflito causava "Application failed to respond")
5. **PR #57 (último)** — fix do lifespan: `mcp.streamable_http_app()`
   precisa do seu lifespan próprio pra inicializar o
   `StreamableHTTPSessionManager`. Quando montado em outro Starlette
   wrapper (pra adicionar `/health` + AuthMiddleware), o lifespan não
   propagava → POST `/mcp` retornava 500 com
   `RuntimeError: Task group is not initialized`.

   **Fix aplicado:** passar `lifespan=mcp_app.router.lifespan_context`
   pro Starlette wrapper. Aplicado nos 2 paths de `_create_app`
   (com e sem auth).

### Validação até aqui (depois do PR #57 mergeado)
- `/health` → 200 OK
- claude.ai Settings → Connectors → Add com URL `/mcp` → **cadastrou
  com sucesso** (antes do PR #57 dava "Falha ao adicionar conector")
- UI mostra **9 tools listadas** com toggle "sempre permitir" — isso
  prova que a request `tools/list` chegou e foi respondida com sucesso

### Sintoma atual (não resolvido)
Em conversa nova no Claude Chat web (com connector ativo, 9 tools
visíveis na UI), Claude Chat respondeu:

> "Não tenho como chamar a tool contar_fragmentos diretamente daqui.
> O que eu tenho acesso via MCP é: Google Drive, Gmail, Calendar,
> Spotify, Figma, Amplitude, Canva — e o gus-hub aparece listado como
> servidor MCP conectado, mas as tools dele só ficam disponíveis dentro
> de Artifacts (via API calls no browser), não como tools nativas
> desta porta de Claude Chat."

E:

> "Para chamar contar_fragmentos do gus-hub eu precisaria fazer um
> Artifact que chama https://gus-mcp-server-production.up.railway.app/mcp
> via fetch/SSE — mas Artifacts têm restrições de CORS que provavelmente
> vão bloquear."

---

## Hipóteses pra investigar

### H1: É comportamento esperado do Claude Chat web (mais provável)

Claude Chat web pode ter classes diferentes de MCP servers:
- **Built-in** (Google Drive, Gmail, etc.) — expostos como tools nativas
- **Third-party / Custom** — registrados como Connector mas só
  acessíveis dentro de Artifacts (via fetch JS no sandbox do browser)

Se for o caso, **o servidor tá certo**, e o caminho real é via API
Anthropic com o parâmetro `mcp_servers` (server-side relay), não via
Claude Chat web nativo.

**Como verificar:** consultar docs do Anthropic sobre Connectors no
claude.ai web. Buscar por:
- "claude.ai connector custom MCP server tool exposure"
- "MCP remote server desktop vs web availability"
- "Claude Chat connector tools inline vs artifact"

Se confirmar que web só expõe via Artifact, fechar a demanda como
"comportamento esperado" e atualizar `gus-28-passo2-mcp-server.md`
documentando isso.

### H2: Falta declarar capabilities corretas no MCP server

O `streamable_http_app()` do FastMCP expõe um set default de
capabilities. Talvez o claude.ai web exija capabilities específicas
(tipo `tools/list_changed`, `prompts`, `resources`) pra "promover" o
servidor de Connector pra Tool nativa.

**Como verificar:**
- Ler logs Railway de uma request de descoberta — ver qual o
  `initialize` request que claude.ai mandou e qual a resposta nossa
- Comparar com servidor que SEJA exposto nativo (ex: documentação MCP
  oficial de "remote server" vs "local stdio")
- Ver `mcp.server.lowlevel.Server.create_initialization_options()` —
  o FastMCP usa default. Talvez precise customizar.

### H3: Transport errado (HTTP+SSE vs StreamableHTTP)

Atualmente uso `mcp.streamable_http_app()`. Há também `sse_app()` mais
antigo. Pode ser que claude.ai web só consuma o `sse_app()` (transport
HTTP+SSE legacy) pra MCP remoto, e o `streamable_http_app` é só pra
clientes que falam o transport novo.

**Como verificar:**
- Logs Railway mostrando o User-Agent / endpoints que claude.ai bate
- Tentar adicionar um Connector apontando pra `/sse` em vez de `/mcp`
  (precisa expor o `sse_app()` em paralelo)

### H4: Nome do servidor / URL precisa de path específico

Alguns docs do MCP mencionam que a URL pública precisa terminar em
`/sse` ou `/mcp` por convenção. Já uso `/mcp` mas vale checar se
existe alguma diferença sutil que afeta como claude.ai expõe as tools.

---

## Onde olhar

### Arquivos relevantes
- `hub/mcp_server.py` — implementação do servidor
- `Dockerfile.mcp` — imagem deploy
- `railway.mcp.toml` — config Railway
- `projetos/gus/gus-28-passo2-mcp-server.md` — guia setup do Gustavo
- `projetos/gus/gus-28-arquitetura-mcp.md` — arquitetura (se existir)

### Endpoints em produção
- Health: `https://gus-mcp-server-production.up.railway.app/health`
- MCP: `https://gus-mcp-server-production.up.railway.app/mcp`

### Logs Railway
Pegar logs da última conexão claude.ai → ver `initialize` request +
`tools/list` request + se houve algum `tools/call` que falhou.

Se conseguir reproduzir: pedir Gustavo abrir conversa nova no Claude
Chat web e mandar "Use a tool contar_fragmentos do gus-hub" — depois
puxar logs Railway da janela exata.

---

## Como NÃO investigar

- **Não** mexer no fix do lifespan (PR #57) — comprovadamente
  funcionando, `/mcp` responde 200, handshake completo.
- **Não** tentar via Artifact — Gustavo já tentou, é caminho errado
  (sandbox CORS-limitado).
- **Não** assumir que é problema de auth — ele tá conectando, listando
  tools, UI verde. Auth tá ok.

---

## Resultado esperado

Uma das três:
1. **Confirmação H1** ("comportamento esperado") + atualização da doc
   `gus-28-passo2-mcp-server.md` explicando que claude.ai web só usa
   Connector via Artifact, e o caminho real é via Claude Code / API
   Anthropic com `mcp_servers` param.
2. **Fix concreto** (capabilities, transport, ou outra mudança no
   servidor) que faça as tools aparecerem nativas no Claude Chat.
3. **"Não foi possível reproduzir / não tem documentação"** com
   sugestão de testar via Claude Desktop ou via API Anthropic
   diretamente — se funcionar lá, confirma H1.

---

## Contexto adicional

- Branch atual após PR #57: `main` em `0314678`
- O retro-engine log do dia tá em
  `_log/retro-engine-claude-code/2026-04-30.md`
- Docs MCP úteis: https://modelcontextprotocol.io/docs
- Anthropic Connectors docs: https://docs.anthropic.com (busca por
  "connectors" ou "MCP")
