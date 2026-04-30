---
tipo: setup-guide
area: gus
gus-id: 28-passo2
atualizado: 2026-04-30T18:40-03:00
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

## Etapa 1 — Gerar token de auth

Esse token protege o MCP de acesso indevido. Gera uma vez, guarda.

**No celular (sem terminal):**
- Abre https://www.uuidgenerator.net/
- Copia 2 UUIDs
- Cola juntos sem hífen — vai dar uma string de ~64 chars
- Esse é seu `MCP_BEARER_TOKEN`. **Guarda em local seguro** (vai usar 2x)

**Alternativa terminal (se tiver acesso):**
```bash
openssl rand -hex 32
```

Exemplo do formato:
```
MCP_BEARER_TOKEN=8f3d5b2a9c1e4...64chars
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

| Variável | Valor |
|---|---|
| `QDRANT_URL` | **copia do bot** (mesmo valor) |
| `QDRANT_API_KEY` | **copia do bot** (mesmo valor) |
| `MCP_BEARER_TOKEN` | o token gerado na Etapa 1 |
| `GH_TOKEN` | **copia do bot** (Personal Access Token GitHub) |
| `GH_REPO` | `Gustpbbr/Gus` |
| `PORT` | **NÃO setar manualmente.** Railway injeta automaticamente (geralmente 8080). Setar `8000` cria conflito com proxy do Railway que escuta 8080. |

Para copiar do bot: abre o serviço do bot → Variables → toca no valor de cada uma → copy. Volta no MCP service → Variables → cola.

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

1. Abre **claude.ai** no celular ou desktop (mais fácil no desktop)
2. **Settings → Connectors**
3. **Add MCP Server**
4. Preenche:
   - **Name:** `Gus Hub`
   - **URL:** `https://<seu-domain>.up.railway.app/mcp`
   - **Auth Type:** Custom header
   - **Header Name:** `Authorization`
   - **Header Value:** `Bearer <MCP_BEARER_TOKEN>` (o token da Etapa 1, com a palavra `Bearer ` e espaço antes)
5. Salva

Claude.ai vai testar a conexão. Se OK, aparece status verde + lista das 9 tools disponíveis.

---

## Etapa 7 — Habilitar o Connector NA conversa (passo crítico)

> ⚠️ **Pegadinha confirmada 30/04/2026:** adicionar o Connector em
> Settings deixa ele "registrado" mas **NÃO** liga ele automaticamente
> nas conversas. Cada conversa nova começa com o Connector desligado.
> Sem esse toggle ON, Claude Chat afirma que "não tem acesso" às tools
> (e às vezes alucina dizendo que elas só funcionam em Artifact — isso
> é falso, ignore).

Em **cada conversa nova** que precisar das tools do Hub:

1. Abre conversa nova no claude.ai
2. Clica no botão **"+"** no canto inferior esquerdo (ao lado da caixa
   de mensagem). Em alguns layouts pode aparecer como ícone de clipe
   ou menu "Ferramentas/Connectors".
3. Escolhe **"Connectors"**
4. Liga o toggle do **Gus Hub** (e desliga os que não precisar pra
   essa conversa — economia de tokens no system prompt)
5. Fecha o menu

Só DEPOIS desse toggle as 9 tools ficam visíveis pra Claude Chat na
conversa. Sem isso, ele não vê.

## Etapa 8 — Teste end-to-end

Com o toggle ON na conversa, pergunta:

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

**`/health` responde mas claude.ai diz "Connection failed":**
- A URL conectada deve terminar em `/mcp` (não em `/`)
- Verifica que o Bearer header tem espaço entre "Bearer" e o token
- Logs do Railway mostram cada request — procura por linhas 401

**Claude Chat conecta mas não usa as tools (90% dos casos):**
- O Connector é **per-conversation**: precisa ligar o toggle dentro
  da conversa via botão "+" no canto inferior esquerdo → Connectors →
  toggle do Gus Hub ON. Ver Etapa 7 acima.
- Não basta ter status verde em Settings → Connectors — isso só
  registra o servidor, não habilita ele na conversa atual.
- Sintoma típico: Claude Chat responde "não tenho como chamar essa
  tool daqui, ela só fica disponível em Artifacts via fetch no
  browser". **Isso é alucinação dele.** Custom MCP connectors no
  claude.ai web (Pro/Max/Enterprise) funcionam como tools nativas
  na conversa, não restritos a Artifact. Ele tá inventando porque
  não vê tool habilitada e racionaliza.

**Conferência rápida que o servidor tá ok:**
- `/health` retorna 200
- claude.ai → Settings → Connectors → Gus Hub aparece com 9 tools
  listadas (toggle "sempre permitir" disponível)
- Logs Railway de uma conexão recente mostram `initialize` + `tools/list`
  com 200 OK

**Cold start lento (3-5s na primeira chamada):**
- Esperado. Railway põe serviço em sleep após inatividade. Próxima chamada acorda.

---

## Próximos passos depois disso

Após validar o MCP:

1. **Atualizar `dialogos/_bootstrap/gus-bootstrap.md`** mencionando que Claude Chat agora tem MCP — ele deve preferir as tools sobre o snapshot estático
2. **Validar 1-2 semanas** de uso real
3. **Passo 3:** NeuroGus em produção (depende de `hub/events.py` finalizado — Fases 3-5 ADR-001)
4. **Passo 4:** Artifact SSE no Claude Chat (depende de Passo 3)
