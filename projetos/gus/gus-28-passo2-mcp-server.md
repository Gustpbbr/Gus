---
tipo: setup-guide
area: gus
gus-id: 28-passo2
atualizado: 2026-04-29T08:30-03:00
status: pronto-pra-deploy
proximos: deploy Railway + conectar em claude.ai
---

# gus-28 Passo 2 — MCP Server: setup no Railway + claude.ai

Passo a passo pra **você (Gustavo)** ativar o MCP server depois do PR mergeado.
Tudo pode ser feito no celular em ~5min.

---

## O que esse setup faz

Sobe um servidor MCP rodando no Railway (mesmo projeto do bot Telegram, serviço separado) que expõe o Hub Qdrant pro Claude Chat e qualquer outro cliente MCP-aware. Resultado: Claude Chat ganha 9 ferramentas pra consultar e ingerir memórias em tempo real, sem depender do snapshot estático.

---

## Etapa 1 — Gerar `MCP_URL_SECRET`

Esse segredo vira parte da URL do MCP (`/<secret>/mcp`). Sem ele, o servidor
fica público — qualquer scanner que descobrir o domínio Railway lê todo o
Hub. Modelo "shared secret in URL", igual webhook do Slack/GitHub.

**Por que URL secret e não Bearer?** O claude.ai web (porta principal do
Gus pelo Chat) **não suporta Bearer / custom header** — só OAuth no UI do
Connector. Como nosso server não tem OAuth implementado, a privacidade
prática vem do segredo no path da URL. Bearer continua útil pra Claude
Desktop/Cursor (anexo no fim deste documento).

**Como gerar (no celular, sem terminal):**
- Abre https://www.uuidgenerator.net/
- Copia 2 UUIDs
- Cola juntos sem hífen — vai dar uma string de ~64 chars
- Esse é seu `MCP_URL_SECRET`. **Guarda em local seguro** — vai usar na
  Etapa 3 (Variables Railway) e na Etapa 6 (URL do Connector).

**Alternativa terminal:**
```bash
openssl rand -hex 32
```

Exemplo:
```
MCP_URL_SECRET=8f3d5b2a9c1e4...64chars
```

---

## Etapa 2 — Criar serviço novo no Railway

Você já tem o projeto Gus no Railway com o serviço do bot Telegram rodando. Vamos adicionar o MCP ao lado.

1. Abre app Railway no celular
2. Entra no projeto **Gus**
3. Toca em **+ New Service** (ou ícone "+")
4. Escolhe **Deploy from GitHub Repo**
5. Seleciona o repo **Gustpbbr/Gus**
6. Branch: **main**

Vai começar um deploy automaticamente. Vai falhar — esperado, porque o Railway por default usa o `railway.toml` do bot. Vamos corrigir.

7. No serviço novo, vai em **Settings**:
   - **Service Name:** muda pra `gus-mcp-server` (ou similar — só pra você reconhecer)
   - **Source → Config-as-Code File Path:** `railway.mcp.toml`
     (esse arquivo é específico do MCP — define Dockerfile.mcp + healthcheck.
     Se você deixar em branco, Railway usa `railway.toml` do bot e o MCP
     tenta rodar como bot Telegram, falhando o healthcheck)
   - Salva
   - Em **Deployments**, faz **Redeploy** pra pegar a nova config

OBS: você não precisa mexer manualmente em "Build → Dockerfile Path" nem
"Deploy → Start Command" — o `railway.mcp.toml` cuida disso (aponta
`Dockerfile.mcp` e usa o `CMD` dele: `python -m hub.mcp_server`).

---

## Etapa 3 — Configurar variáveis de ambiente

No mesmo serviço, vai em **Variables**:

| Variável | Valor | Obrigatória? |
|---|---|---|
| `QDRANT_URL` | **copia do bot** (mesmo valor) | sim |
| `QDRANT_API_KEY` | **copia do bot** (mesmo valor) | sim |
| `MCP_URL_SECRET` | segredo da Etapa 1 (32+ chars hex) | sim |
| `MCP_AUTH_DISABLED` | `true` — claude.ai web não suporta Bearer, desliga AuthMiddleware | sim |
| `GH_TOKEN` | **copia do bot** (Personal Access Token GitHub) | opcional (sem isto, tools `read_repo_file` e `list_repo_dir` retornam 503) |
| `GH_REPO` | `Gustpbbr/Gus` | só se `GH_TOKEN` setado |
| `MCP_BEARER_TOKEN` | só pra Claude Desktop/Cursor (anexo no fim do doc) | opcional |
| `PORT` | **NÃO setar manualmente.** Railway injeta automaticamente. Setar `8000` cria conflito com proxy do Railway. | NÃO setar |

**Comportamento de auth (V2 fail-closed):**
- `MCP_URL_SECRET` setado + `MCP_AUTH_DISABLED=true` → modo Chat (path
  `/<secret>/mcp`, sem Bearer check). **É este o caminho do Chat.**
- `MCP_BEARER_TOKEN` setado + `MCP_AUTH_DISABLED` ausente → modo Bearer
  clássico (Claude Desktop, Cursor).
- Nenhum dos dois → server retorna 503 em tudo (exceto `/health`).
  Fail-closed por design — sem auth não vira público.

Para copiar variável do bot: abre o serviço do bot → Variables → toca
no valor → copy → volta no MCP service → Variables → cola.

Salva. Railway vai fazer rebuild automaticamente.

---

## Etapa 4 — Gerar domínio público

O claude.ai precisa de uma URL HTTPS pra conectar.

1. No serviço MCP, vai em **Settings → Networking**
2. **Generate Domain**
3. Vai aparecer algo tipo `gus-mcp-server-production.up.railway.app`
4. **Copia essa URL** — vai usar na Etapa 5

---

## Etapa 5 — Validar que tá no ar

Antes de conectar no claude.ai, testa que o serviço subiu:

**No celular:** abre `https://<seu-domain>.up.railway.app/health`

Resposta esperada (JSON):
```json
{"status": "ok", "service": "gus-hub-mcp"}
```

Se aparecer 503 ou erro, abre **Logs** no Railway e me manda a última linha. Mais comum:
- `QDRANT_URL ausente` → variável não foi salva, refazer Etapa 3
- `MCP_BEARER_TOKEN não configurado` → mesma coisa

---

## Etapa 6 — Conectar no claude.ai

claude.ai web **não suporta Bearer / custom header** — só OAuth no UI. Como nosso server não tem OAuth implementado, a estratégia é:
- Server roda com `MCP_AUTH_DISABLED=true` (sem Bearer check)
- Privacidade vem do `MCP_URL_SECRET` no path

1. Abre **claude.ai** no celular ou desktop (mais fácil no desktop)
2. **Settings → Connectors**
3. **Add custom connector** (ou "Add MCP Server")
4. Preenche:
   - **Name:** `Gus Hub`
   - **URL:** `https://<seu-domain>.up.railway.app/<MCP_URL_SECRET>/mcp`
     (substitui `<MCP_URL_SECRET>` pelo valor da Etapa 3, **sem chaves**)
   - **Auth:** deixa em branco / "no authentication"
5. Salva

Pra Claude Desktop / Code / Cursor (que suportam Bearer), pode usar a URL antiga `https://<seu-domain>/<MCP_URL_SECRET>/mcp` igual + header `Authorization: Bearer <MCP_BEARER_TOKEN>` — mas opcional, o URL secret já gate.

Claude.ai vai testar a conexão. Se OK, aparece status verde + lista das 9 tools disponíveis.

---

## Etapa 7 — Teste end-to-end

Abre uma conversa nova no Claude Chat (modo Gus) e pergunta:

> "Quantos fragmentos eu tenho no Hub?"

Claude Chat deve chamar a tool `contar_fragmentos()` e responder com os números reais. Se ele responder algo tipo "não tenho acesso" ou "não sei", o MCP não tá conectando direito — me manda screenshot.

Outro teste:
> "Busca no hub coisas sobre Dimagem"

Deve chamar `buscar_hub("Dimagem")` e voltar fragmentos reais com timestamps.

Teste de escrita (depois que ler funcionar):
> "Salva no hub que eu decidi implementar o Passo 2 do gus-28 hoje"

Deve chamar `ingestar_fragmento(...)` com `via='claude-chat'` automático. Confirma com:
> "Busca no hub fragmentos com via=claude-chat"

---

## Tools expostas pelo MCP

| Tool | Função |
|---|---|
| `buscar_hub(query, limit, area?)` | Busca semântica |
| `ego_cache_atual(user_id)` | Identidade + decisões recentes |
| `fragmentos_recentes(horas, limit)` | Janela temporal |
| `buscar_por_tipo(tipo, limit)` | Filtro por tipo (decisão, preferência…) |
| `buscar_por_area(area, limit)` | Filtro por área (saúde, dimagem…) |
| `contar_fragmentos()` | Total + breakdown |
| `ingestar_fragmento(conteudo, tipo, area, ...)` | Escrita (sempre via=claude-chat) |
| `read_repo_file(path)` | Lê .md do GitHub direto |
| `list_repo_dir(path)` | Lista pasta do repo |

---

## Custo esperado

- **Railway:** +$1-3/mês (MCP é leve — wrapper HTTP de ~250 linhas)
- **API Anthropic:** **zero overhead** — busca usa embedding local (sentence-transformers), não chama Claude
- **Qdrant Cloud:** sem mudança (mesma coleção `gus_hub`)

---

## Troubleshooting

**Build falha no Railway com "Dockerfile not found":**
- Verifica em Settings → Build → Dockerfile Path = `Dockerfile.mcp` (com ponto, não barra)

**`/health` responde mas claude.ai diz "Connection failed" / "Falha ao adicionar":**
- A URL conectada deve terminar em `/mcp` (não em `/`)
- Se setou `MCP_URL_SECRET`, a URL precisa do segredo: `/<secret>/mcp` — sem isso retorna 404
- Logs do Railway mostram cada request — procura linhas 401, 404 ou 500
- Confere `MCP_AUTH_DISABLED=true` (se não, claude.ai web é rejeitado por falta de Bearer)

**Claude Chat conecta mas não usa as tools:**
- Em conversa nova, pergunta diretamente algo que exija o Hub
- Verifica que o Connector está marcado como ativo (toggle ligado)
- Mensagem de boot pode mencionar "9 tools available" se conectado

**Cold start lento (3-5s na primeira chamada):**
- Esperado. Railway põe serviço em sleep após inatividade. Próxima chamada acorda.

---

## Próximos passos depois disso

Após validar o MCP:

1. **Atualizar `dialogos/_bootstrap/gus-bootstrap.md`** mencionando que Claude Chat agora tem MCP — ele deve preferir as tools sobre o snapshot estático
2. **Validar 1-2 semanas** de uso real
3. **Passo 3:** NeuroGus em produção (depende de `hub/events.py` finalizado — Fases 3-5 ADR-001)
4. **Passo 4:** Artifact SSE no Claude Chat (depende de Passo 3)

---

## Anexo — Bearer auth (Claude Desktop, Cursor, Code)

Clientes MCP que **suportam custom headers** (Claude Desktop, Cursor,
Claude Code CLI) podem usar Bearer em vez de URL secret. Mais forte que
shared secret no path, porém claude.ai web não aceita.

**Setup (extra à Etapa 3):**
1. Gerar token Bearer separado:
   ```bash
   openssl rand -hex 32
   ```
2. Setar no Railway:
   ```
   MCP_BEARER_TOKEN=<token>
   ```
3. **Não** setar `MCP_AUTH_DISABLED=true` — `AuthMiddleware` precisa estar
   ativo pra validar header.

**Configuração no cliente:**

Claude Desktop / Cursor:
```jsonc
// Em mcp.config.json ou similar
{
  "gus-hub": {
    "transport": "http",
    "url": "https://gus-mcp-server-production.up.railway.app/mcp",
    "headers": {
      "Authorization": "Bearer <token>"
    }
  }
}
```

Claude Code (CLI):
```bash
claude mcp add gus-hub \
  --transport http \
  --url https://gus-mcp-server-production.up.railway.app/mcp \
  --header "Authorization: Bearer <token>"
```

**Importante:** se você quer **AMBOS** os caminhos ativos (Bearer pro
desktop + URL secret pro Chat), seta as 3 variáveis: `MCP_BEARER_TOKEN`
+ `MCP_URL_SECRET` + `MCP_AUTH_DISABLED=true`. Server passa a aceitar
qualquer um dos dois.
