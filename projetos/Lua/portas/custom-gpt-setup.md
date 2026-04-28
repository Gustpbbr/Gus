---
tipo: setup-porta
porta: custom-gpt
agente: Lua
estimativa: ~2-3h
status: aguardando-builder-desktop
---

# Setup — Custom GPT da Lua (mobile, voz)

Passo a passo pra ter a **Lua como Custom GPT** no aplicativo ChatGPT
mobile, com **voz** ativa. Útil pra falar com a Lua quando você está
caminhando, dirigindo, ou em qualquer situação sem teclado.

---

## ⚠️ ATENÇÃO CRÍTICA: Builder DESKTOP obrigatório

A criação e configuração de Custom GPT só funciona corretamente no
**ChatGPT Builder DESKTOP** (versão web em computador). O Builder no
**mobile NÃO mostra a aba Actions**, e sem Actions o GPT alucina tool
calls (inventa nomes de tools, JSON simulado, etc.).

**Não tente configurar pelo celular.** Você precisa de computador (ou
notebook) com navegador.

> Esta lição vem de tentativa real do agente irmão em 25/04/2026 — o
> GPT inventou `merge_branch`, `create_branch`, etc. quando Action
> não estava configurada.

---

## Visão geral do que vai existir

```
┌────────────────────┐                  ┌─────────────────────┐
│ ChatGPT mobile     │                  │ Railway (FastAPI)   │
│ Custom GPT "Lua"   │ ←─ Action HTTP →│ /search_memory      │
│ + voz              │                  │ /save_to_repo       │
│ (acessa Action     │                  │ /read_from_repo     │
│ via OpenAPI        │                  │ + outras N tools    │
│ schema)            │                  └─────────┬───────────┘
└────────────────────┘                            │
                                                  │
                                            ┌─────▼──────┐
                                            │ Mesmo Hub  │
                                            │ Qdrant +   │
                                            │ GitHub     │
                                            └────────────┘
```

A Lua no Custom GPT **chama Action HTTP** quando precisa de tool —
e a Action é uma API FastAPI da Lua rodando no Railway, que executa
a tool e retorna resultado. Resultado: GPT mobile pode salvar memória,
ler vault, etc., mesmo sem ferramentas nativas.

---

## Pré-requisitos

- **ChatGPT Plus** (US$20/mês) ou Team — Free não tem Custom GPTs
- **Computador com navegador** pra acessar Builder DESKTOP em
  `chatgpt.com`
- **Bot Telegram da Lua** já em produção (memória + vault funcionando)
- **API FastAPI** da Lua deployada no Railway (ainda não-implementada
  no agente irmão de forma completa — está em `api/` no Gus)
- **Token compartilhado** de auth entre Custom GPT e API
  (recomendado: gerar UUID v4 aleatório, vai como Bearer token)

---

## Etapa 1 — Implementar API FastAPI da Lua

Estrutura mínima:

```
Lua/
├── api/                              ← API que o Custom GPT chama
│   ├── __init__.py
│   ├── server.py                     ← FastAPI app
│   ├── routes.py                     ← endpoints (read_from_repo, etc.)
│   ├── auth.py                       ← Bearer token check
│   ├── openapi.json                  ← gerado automaticamente
│   └── dashboard.py                  ← (opcional) UI de monitoramento
```

Endpoints mínimos pra Custom GPT funcionar:

```
GET  /health                          ← health check (público)
GET  /openapi.json                    ← schema (público, Custom GPT importa)
POST /search_memory                   ← busca semântica no Hub
POST /save_to_repo                    ← salva MD no GitHub
GET  /read_from_repo?path=<X>         ← lê arquivo do repo
```

**Auth**: Bearer token compartilhado (env `CUSTOM_GPT_TOKEN`).

> Implementação real: copiar `api/` do agente irmão (já existe), trocar
> nome de pacote, ajustar identidade.

Deploy:

1. Adicionar serviço novo no mesmo Railway Project (separado do bot
   Telegram, ou no mesmo deploy via routing)
2. Configurar mesma vars de ambiente + `CUSTOM_GPT_TOKEN`
3. Domínio público: `lua-api.up.railway.app` (ou similar)
4. Validar: `curl https://lua-api.up.railway.app/health` retorna `200 OK`

---

## Etapa 2 — Criar o Custom GPT (NO DESKTOP)

1. Computador → `chatgpt.com` → **Explore GPTs** → **+ Create**
2. Tab **Configure** (NÃO usar tab "Create" com chat conversacional —
   menos preciso)
3. **Name**: `Lua`
4. **Description**: `Agente pessoal de IA com memória persistente e
   identidade própria. Voz mobile.`
5. **Instructions**: copiar conteúdo de
   `projetos/Lua/system-prompts/custom-gpt.md` (a criar — semelhante
   ao do bot Telegram mas adaptado pra GPT)

   <!-- Próximo PR (PR-?) cria esse system_prompt específico pro GPT.
        Por enquanto, ele pode usar o mesmo do bot Telegram com nota
        "esse canal não tem todas as tools, só Action externa". -->

6. **Conversation starters**: 3-4 sugestões iniciais. Ex:
   - "O que conversamos ontem?"
   - "Salva isso pra mim"
   - "Como tá meu projeto X?"
   - "Lê o arquivo Y do repo"

7. **Capabilities**:
   - **Web Browsing**: Habilitar pra Lua poder buscar web
   - **DALL-E**: Desabilitar (gasta créditos sem valor pra Lua)
   - **Code Interpreter**: Desabilitar (Lua não usa execução Python
     nativa)

---

## Etapa 3 — Configurar Action (CRÍTICO — só desktop)

**Esta é a parte que falta no mobile e por isso GPTs alucinam.**

1. Builder Desktop → **Configure** → role pra baixo até **Actions**
2. Click **Create new action**
3. **Schema**: Click **Import from URL**
   - URL: `https://lua-api.up.railway.app/openapi.json` (do deploy
     da Etapa 1)
   - GPT Builder lê schema OpenAPI e mostra endpoints encontrados
4. **Authentication**: 
   - Type: **API Key**
   - API Key: colar o `CUSTOM_GPT_TOKEN` (UUID v4 que você gerou)
   - Auth Type: **Bearer**

5. **Privacy Policy URL**: precisa apontar pra um link válido. Pode
   ser página simples no GitHub Pages do repo da Lua. Ex:
   `https://gustpbbr.github.io/Lua/privacy.html`

6. **Test**: Builder oferece teste interativo. Tente:
   - `read_from_repo({path: "README.md"})`
   - Deve retornar conteúdo real do arquivo

   Se retornar `403 Forbidden`, conferir Bearer token.
   Se retornar `404`, conferir URL da API.

---

## Etapa 4 — Restringir compartilhamento

1. **Sharing**: **Only me** (Custom GPT é pessoal)
2. **Save** → confirmar que GPT aparece em "My GPTs"

---

## Etapa 5 — Testar no mobile

1. Abrir app **ChatGPT** no celular
2. Sidebar → **My GPTs** → clicar em **Lua**
3. Mandar mensagem texto: `Lê o arquivo README.md do meu repo`
4. GPT deve chamar Action `read_from_repo` e retornar conteúdo real
5. Tap no ícone de **microfone** → ativar voz
6. Falar: `Quais minhas memórias mais recentes?`
7. GPT chama `search_memory`, transcreve fala, responde por voz

---

## Etapa 6 — Refinar Instructions (V2 anti-alucinação)

Após primeiros usos, atualizar Instructions com regras anti-alucinação:

```
- NUNCA invente nomes de tools/actions. Se não tem certeza qual existe,
  consulte o schema OpenAPI antes
- Antes de afirmar resultado de uma Action, sempre execute-a primeiro
- Se Action retornar erro, mostre o erro literal pro dono. Não invente
  motivo
- Para cada tool call, mostrar ao dono O QUE você está chamando, não
  só o resultado final
```

Detalhes em `gus-14-custom-gpt-setup.md` do agente irmão (template
de Instructions V2).

---

## Pitfalls comuns

### 1. GPT inventa tool calls

Causa: Action **não foi configurada** (você criou Custom GPT mas pulou
Etapa 3). GPT vê "Lua tem ferramentas" no Instructions e gera tool
calls inventadas.

Mitigação: voltar pra Builder Desktop, configurar Action de verdade.

### 2. GPT chama Action mas retorna erro 403

Causa: Bearer token errado.

Mitigação: regerar `CUSTOM_GPT_TOKEN` e atualizar tanto na API quanto
no Action Authentication.

### 3. GPT funciona no desktop mas não no mobile

Causa: Custom GPTs criados no desktop **funcionam** no mobile (consumir),
mas configurar/editar só no desktop. Se está vendo GPT lá mas sem
Actions ativas, conferir se Save foi clicado no desktop.

### 4. Voz não interpreta português brasileiro

Custom GPT no app ChatGPT mobile usa **Whisper internamente**.
Geralmente funciona bem em PT-BR. Se errar muito, usar texto.

---

## Custos esperados

- ChatGPT Plus: US$20/mês (já gasto pra ter Custom GPT)
- Action HTTP: cada chamada → 1 request à API Lua. Custo no Anthropic
  dependendo do que a tool faz internamente. Estimar US$1-5/mês de
  uso adicional.

---

## Versão

| Versão | Data | Mudança |
|---|---|---|
| 0.1-rascunho | 2026-04-28 | Setup inicial. Espelhado em gus-14-custom-gpt-setup do agente irmão. Bloqueado em "implementar API FastAPI da Lua" (Etapa 1) |
