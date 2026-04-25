---
tipo: documentacao-projeto
projeto: gus
parte: 14-custom-gpt-setup
atualizado: 2026-04-25T19:50-03:00
---

# Custom GPT no ChatGPT — setup

Passo-a-passo pra ativar a porta **Custom GPT mobile** depois que o código
da pasta `api/` está em produção no Railway.

---

## ⚠️ AVISO CRÍTICO — desktop obrigatório pra Actions

**Lição aprendida em 25/04/2026 (testando no celular):**

A seção **Actions** do GPT Builder **NÃO aparece na interface mobile**. Você
consegue criar o GPT, configurar Instructions, capabilities e modelo no
celular — mas **as 14 operations da nossa API só podem ser conectadas
abrindo o Builder no desktop** (PC/notebook).

Sintomas se você criar o GPT só no celular (sem voltar no desktop):
- GPT responde com identidade Gus (Instructions funcionam)
- **Mas inventa tool calls que nunca acontecem** — mostra JSON tipo
  `{"path":"...","mode":"append",...}` simulando execução, e nada
  acontece de verdade no Mem0 / GitHub
- Comportamento idiota mas documentado de Custom GPTs com Action ausente

**Procedimento certo:** crie o GPT pelo dispositivo que preferir, mas
**reserve sessão no PC pra completar Actions**. Sem Actions, o Custom
GPT é só "ChatGPT genérico com identidade Gus colada" — sem Mem0,
sem GitHub, sem nada do que importa.

**Cuidado adicional — conector GitHub nativo:** se durante a criação
o ChatGPT oferecer "Authorize GitHub via OAuth" (tela `github.com/login/oauth/authorize`
com "ChatGPT Verification by OpenAI"), **NÃO autoriza**. Isso é a
integração GitHub nativa do ChatGPT (full access), que **bypass nossa API**
e quebra todas as proteções LGPD (`dimagem/` bloqueado, PII scan, tag
`via=custom-gpt`). Pula essa tela e configura nossa Action no desktop.

---

## 1. Pré-requisitos

| Item | Status |
|---|---|
| Conta ChatGPT Plus em `gustavo.pratti84@gmail.com` | ✅ tem |
| Bot já em produção no Railway com `api/` | ⏳ aguarda redeploy automático após merge |
| Conta OpenAI Platform com saldo (Custom GPT roda em GPT-5 cobrado) | ✅ tem (mesma do Whisper) |

## 2. Variáveis novas no Railway

Vai em **Railway → seu projeto → Variables** e adiciona:

| Nome | Valor |
|---|---|
| `CUSTOM_GPT_TOKEN` | uma string aleatória forte. Gerar com: `openssl rand -hex 32` ou no celular usar https://www.random.org/strings/ (32 chars hex) |
| `API_PUBLIC_URL` | URL pública do app no Railway (ex: `https://gus-production-XXXX.up.railway.app`) — copiar do dashboard Railway, aba Settings → Domains |

Após adicionar, Railway faz redeploy automático (~2-5min).

**Verificar saúde:**

Abrir no navegador: `https://<seu-app>.up.railway.app/health`

Resposta esperada: `{"status":"ok","service":"gus-api"}`

Se não aparecer, ver logs do Railway pra erro de start.

## 3. Criar o GPT no Builder

1. Vai em https://chatgpt.com/gpts/editor
2. Clica em **"Create"** (não "Configure" — só Create do zero)
3. Pula o Builder conversacional, vai direto na aba **"Configure"**

### 3.1 Aba Configure

| Campo | Valor |
|---|---|
| **Name** | Gus |
| **Description** | Assistente pessoal do Gustavo — captura, memória, pesquisa, briefing |
| **Instructions** | Cola o conteúdo de `gus/gus-identity.md` (ver abaixo) |
| **Conversation starters** | Sugestões: *"qual o briefing do dia?"*, *"o que conversamos sobre Phronesis?"*, *"lembra que..."*, *"busca papers sobre..."* |
| **Knowledge** | Vazio (memória vem via Mem0 nas tools) |
| **Capabilities** | DESMARCAR Web Browsing, Image Generation, Code Interpreter (tudo cobrado por chamada de tool nossa, mais barato e rastreável) |

### 3.2 Instructions — texto sugerido (V2 anti-alucinação)

Cola na íntegra. Versão atualizada após teste real em 25/04/2026 — V1
permitia GPT inventar tools (`merge_branch`, `create_branch`) que não
existem. Esta V2 lista explicitamente o que ele tem e proíbe simulação.

```
Você é o Gus — assistente pessoal do Gustavo Pratti de Barros (anestesiologista,
pesquisador em IA brasileiro). Está rodando como Custom GPT no ChatGPT.

PRINCÍPIOS FUNDAMENTAIS:
1. Não alucinar. Se não sabe, diz "não sei" e busca via search_web ou pesquisar_pubmed/arxiv.
2. Verificar antes de afirmar ausência. Use list_github_directory antes de dizer "X não existe".
3. Memória — sempre buscar em search_memory antes de responder sobre saúde, projetos, finanças, preferências.
4. Português brasileiro informal, direto, sem floreio. Crítica direta é bem-vinda.
5. Você é uma porta entre várias do Gus. Há também o bot @Tiogubot no Telegram (cérebro Claude) e Claude Code no PC dele. Mesma entidade, canais diferentes.
6. Você lê e escreve no MESMO Mem0 e MESMO repo GitHub que as outras portas.

TOOLS REAIS QUE VOCÊ TEM (são as ÚNICAS — qualquer outra é alucinação):
- search_memory, salvar_memoria, buscar_memoria_gus, salvar_memoria_gus, deletar_memoria
- read_from_github, list_github_directory, save_to_github
- search_web, pesquisar_pubmed, pesquisar_arxiv
- meta_memoria, auditoria_mem0, sugerir_wikilinks

VOCÊ NÃO TEM (NUNCA invente, NUNCA simule JSON):
- Operações git: branch, commit, merge, PR, push — IMPOSSÍVEL daqui.
  save_to_github escreve DIRETO na main, sem branch nem PR.
- disparar_workflow, criar_acao, logs_railway, auto_diagnostico — só pelo Telegram.
- Acesso a código fora do repo (sistema, ambiente, rede local).
- Editar memória existente — só salvar nova ou deletar por ID.

REGRA CRÍTICA — anti-alucinação de tool:
Se Gustavo pedir algo que não dá pelas tools acima, NÃO mostre JSON
simulado de tool call. Diga literalmente: "essa operação não tá nas
minhas tools aqui — só pelo Telegram (TioGu) ou pelo PC". Lista o que
você TEM e oferece alternativa real.

LIMITAÇÕES DESTA PORTA (segurança):
- Path `dimagem/` BLOQUEADO em read/list/save (LGPD, dados de paciente).
  Servidor retorna 403. Se Gustavo perguntar, redirecione pro Telegram.
- Conteúdo PII (CPF, CNPJ, cartão, keys de API) bloqueado em save_to_github
  pelo servidor. Se aparecer mensagem "ATENÇÃO — dados sensíveis detectados",
  NÃO insista — direcione pro Telegram.

QUANDO USAR CADA TOOL:
- search_memory: ANTES de responder qualquer coisa sobre o Gustavo.
- salvar_memoria: SÓ se Gustavo disser explicitamente "lembra que" ou ficar
  claro que é fato persistente sobre ele.
- read_from_github / list_github_directory: contexto estruturado (arquivos do repo).
- save_to_github: só com pedido claro de salvar.
- search_web: factual atual (notícias, dados que mudam).
- pesquisar_pubmed: clínica, anestesia, evidência científica revisada.
- pesquisar_arxiv: IA, ML, neurociência computacional.
- sugerir_wikilinks: quando ele pedir conexões de um arquivo. Sugestões salvas
  em fila pra Claude/TioGu curarem depois — você não aplica.

ESTILO DE RESPOSTA:
- Quando usar tool, mencione brevemente: "achei isso no Mem0...", "PubMed retornou...".
- Não passe info de tool como conhecimento próprio.
- Quando nossa API responder com erro, mostre a mensagem real ao Gustavo
  ao invés de fingir que funcionou.
- Respostas curtas. Tabelas/listas só quando agrega.
```

### 3.3 Aba Configure → Actions

1. Clica em **"Create new action"**
2. **Authentication**:
   - Type: **API Key**
   - API Key: cola o valor de `CUSTOM_GPT_TOKEN` que você botou no Railway
   - Auth Type: **Bearer**
3. **Schema**:
   - Clica em **"Import from URL"**
   - URL: `https://<seu-app>.up.railway.app/openapi.json`
   - Aguarda ChatGPT carregar — vai listar 14 operations (search_memory, salvar_memoria, etc.)
4. **Privacy policy** (opcional pra GPT privado): pode deixar vazio ou apontar pro README do repo

### 3.4 Salvar e testar

- Clica **"Save"** no canto superior direito
- Visibility: **"Only me"** (privado, NÃO publish)
- Volta pra conversa e testa:
  - *"qual o briefing do dia?"* → deve chamar `read_from_github` em `_indices/_dia.md` ou `pessoal/diario/`
  - *"o que sabe sobre Phronesis?"* → deve chamar `search_memory("Phronesis")`
  - *"lembra que comprei azeite hoje"* → deve chamar `salvar_memoria`
  - *"busca papers sobre metacognição em LLMs"* → deve chamar `pesquisar_arxiv`

Em modo **voice**: toca o ícone de fone na conversa do GPT, fala normalmente, ele responde por voz.

## 4. Operações esperadas (14 expostas)

| Operation ID | Método | Função |
|---|---|---|
| `search_memory` | POST | Busca brain `gustavo` |
| `salvar_memoria` | POST | Salva no brain `gustavo` |
| `buscar_memoria_gus` | POST | Busca brain `gus` (auto-observações) |
| `salvar_memoria_gus` | POST | Salva brain `gus` |
| `deletar_memoria` | POST | Delete (irreversível) |
| `read_from_github` | POST | Lê .md (BLOQUEIA `dimagem/`) |
| `list_github_directory` | POST | Lista pasta (BLOQUEIA `dimagem/`) |
| `save_to_github` | POST | Salva .md (BLOQUEIA `dimagem/` + PII scan) |
| `search_web` | POST | Tavily/DDG |
| `pesquisar_pubmed` | POST | Sem custo |
| `pesquisar_arxiv` | POST | Sem custo |
| `meta_memoria` | GET | Lê `gus/meta-memoria.md` |
| `auditoria_mem0` | GET | Lê `_indices/_auditoria-mem0.md` |
| `sugerir_wikilinks` | POST | Sugere + salva fila pendente em `acoes/wikilinks-pendentes/` |

## 5. Observabilidade

Memórias salvas pela porta carregam `metadata.via = "custom-gpt"` no Mem0 — auditoria por origem possível com filtro.

Custos:
- **Lado OpenAI** (GPT-5 do Custom GPT): incluído no Plus (até quota mensal). Sem custo extra por chamada.
- **Lado nosso** (tools): cada chamada gasta na Anthropic só se a tool internamente chama Sonnet (`sugerir_wikilinks` chama). Resto é Mem0/GitHub/Tavily — frações de centavo.

## 6. Limitações conhecidas (V1)

- Custom GPT no Plus tem **rate limit** de mensagens por janela (~80/3h em GPT-5). Suficiente pra uso pessoal.
- **Voice mode** funciona, mas chamadas de tool podem cortar a fala se demorarem >30s. Tools nossas são rápidas (<5s tipicamente).
- **Account linking não usado**: skill é privada (Only me), token compartilhado. Se virar pública, precisa OAuth.
- **Sem persistência de conversa** entre Telegram ↔ Custom GPT além do Mem0. Resumos extrativos do TioGu chegam aqui via `search_memory`. Conversa em tempo real não.

## 7. Checklist pré-uso (depois de criar)

- [ ] `/health` responde OK no navegador
- [ ] GPT cria, importa OpenAPI sem erro
- [ ] Teste 1: pergunta sobre você → chama `search_memory`, retorna texto
- [ ] Teste 2: "lembra que..." → chama `salvar_memoria`, confirma
- [ ] Teste 3: voice mode → fala "qual o último briefing", recebe resposta falada
- [ ] Verificar Mem0 dashboard: memória nova com `via=custom-gpt`

## 8. Como debugar se quebrar

| Sintoma | Provável causa |
|---|---|
| GPT diz "I encountered an error" sem detalhe | 401/403/500 da nossa API. Ver Railway logs |
| `/health` retorna 502 ou timeout | Bot rodando mas FastAPI não subiu — ver logs Railway |
| Tool chama mas erra com 401 | Token diferente entre Railway e GPT Builder |
| `dimagem/` retorna 403 | Esperado — bloqueio é design |
| PII detectada em save | Esperado — design. Salvar pelo Telegram |

Relacionado: [[gus-10-caminho-alexa]], [[gus-11-tools-roadmap]], [[gus-12-portas-futuras]], [[gus-13-tags-canonicas]]
