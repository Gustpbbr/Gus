---
tipo: setup-porta
porta: claude-chat
agente: Lua
estimativa: ~30min
status: aguardando-decisoes
---

# Setup — Porta Claude Chat (claude.ai)

Passo a passo pra ter a Lua em uma aba do **claude.ai** (web). Esta
é a **porta de reflexão longa** — texto longo, debate de ideias,
análise profunda.

---

## O que essa porta é (e não é)

**É:**
- Aba do navegador em `claude.ai`
- Conversa de reflexão longa, com contexto extenso
- Project com Files (vault leitura) e Instructions (boot da Lua)
- Acesso ao mesmo modelo Claude que o bot Telegram usa

**NÃO é:**
- Bot rodando em servidor (não tem deploy próprio)
- Acesso a tools de execução (não pode salvar repo, não pode buscar
  web — a menos que ative tool específica em sessão)
- Acesso direto à memória dinâmica do Qdrant (memória persistente é
  feita pelo bot Telegram; Claude Chat lê do **vault Drive**, que é
  espelho do GitHub)

---

## Pré-requisitos

- Conta Anthropic (claude.ai) com plano que permite Projects (Pro
  ou Team — Free não tem Projects)
- Repositório da Lua decidido (pasta dedicada ou repo próprio)
- (Opcional) Sync GitHub ↔ Drive configurado pra alimentar Project
  com vault — caso ainda não tenha, esta porta funciona com
  arquivos colados manualmente ou só com Instructions

---

## Etapa 1 — Criar o Project

1. Login em `claude.ai`
2. Sidebar → **Projects** → **Create new project**
3. **Nome**: `Lua`
4. **Descrição**: `Agente pessoal de IA — porta de reflexão longa.
   Identidade, princípios e bootstrap em arquivos do projeto.`
5. **Knowledge**: deixar vazio por enquanto (preenche na Etapa 3)
6. **Custom instructions**: copiar conteúdo de
   `projetos/Lua/system-prompts/claude-chat-instructions.md` (apenas
   o trecho marcado "COPIE A PARTIR DAQUI"). Detalhes nesse arquivo.

---

## Etapa 2 — Adicionar arquivos canônicos da identidade

No campo **Project Knowledge / Files**, adicionar (upload manual ou
sync via Drive):

- `lua-identity.md` — quem a Lua é
- `principios.md` — pilares não-negociáveis
- `lua-meta-memoria.md` — autobiografia narrativa
- `lua-bootstrap.md` — script de ativação
- (se houver outras docs canônicas relevantes)

Esses arquivos viram referência da Lua dentro do Project. Toda
conversa nesta porta tem acesso a eles.

> **Sync via Drive** (recomendado quando configurado): se o repo da
> Lua tiver workflow `sync-to-drive`, basta criar pasta `Lua-Sync/`
> no Drive e arquivos chegam automaticamente. Project pode ler do
> Drive.

---

## Etapa 3 — Validar boot

Em uma conversa nova dentro do Project:

1. Escrever: `Quem é você?`
2. Resposta esperada: a Lua se apresenta usando os arquivos do
   Project, mencionando nome, propósito, e tom canônico
3. Se responder como "Claude assistente genérico", o boot falhou
   — conferir Instructions e Files

4. Escrever: `Quais seus princípios não-negociáveis?`
5. Resposta esperada: a Lua lista os 7 princípios (ou versão
   refinada após entrevista)

---

## Etapa 4 — Sync com Drive (opcional, recomendado depois)

Pra que a Lua nesta porta tenha **vault** acessível (não só
identidade), configurar sync GitHub → Drive.

Detalhes em `05-transversais/t3-sync-com-superficies-externas.md`
(blueprint genérico) — mesmo padrão do agente irmão.

Resumo:
1. Service Account Google com OAuth refresh token
2. GitHub Action `sync-to-drive` em push de `**.md`
3. Pasta dedicada `Lua-Sync/` no Drive
4. Project Lua adiciona pasta inteira como Knowledge (Drive integration
   no claude.ai)

Resultado: qualquer arquivo `.md` do repo da Lua, em qualquer momento,
fica disponível pra leitura nesta porta — sem upload manual.

---

## Etapa 5 — Workflow Drive → GitHub (opcional)

Pra que a Lua nesta porta possa **escrever** no vault:

1. Lua na porta sugere conteúdo (ex: "salva esse resumo")
2. Dono pega o conteúdo + cria arquivo no Drive
3. Workflow `import-from-drive` (cron 15min) puxa pra GitHub
4. Bot Telegram (outra porta) avisa: "demanda nova chegou"
5. Dono ou bot processa a demanda (move pra path certo)

Mesmo padrão de Drive ↔ GitHub do agente irmão, agora pra Lua. Detalhes
em `05-transversais/t3-sync-com-superficies-externas.md`.

---

## Como usar essa porta no dia-a-dia

Use Claude Chat / Lua quando:

- **Reflexão profunda** — debater decisão importante
- **Análise** de documento longo (paper, PDF, livro)
- **Síntese** de muito texto em resumo curto
- **Discussão crítica** — pedir pra Lua "atacar" uma ideia tua

Não use Claude Chat / Lua quando:

- Tarefa de **execução** (salvar arquivo, buscar web em tempo real,
  enviar mensagem) → use Telegram
- Captura **rápida** de pensamento → use Telegram (mensagens curtas)
- Voz → use Custom GPT (quando configurado)

---

## Pitfalls comuns

### 1. Lua "esquece" entre conversas

Cada nova conversa no Project começa limpa. Memória persistente
**não** é compartilhada com bot Telegram em runtime nessa porta. Se o
dono quer que a Lua aqui saiba o que conversou no Telegram ontem, ele
precisa colar manualmente o resumo (ou esperar export de memória que
está no vault Drive sincronizado).

### 2. Lua responde como Claude genérico

- Instructions vazias?
- Files canônicos não carregados?
- Conferir: começar conversa nova com `Quem é você?` deve retornar
  Lua, não Claude

### 3. Custom GPT, Telegram e Claude Chat dão respostas inconsistentes

- Cada porta carrega system_prompt **próprio**
- Se mudou tom em um, mudar em todos
- Boa prática: identidade **base** (lua-identity, principios) é
  shared; system prompts são adapters por canal

### 4. Project não suporta sync Drive

Plano Pro/Team do claude.ai já suporta. Plano Free não. Se for esse
o caso, upload manual dos files (Etapa 2) é a alternativa.

---

## Versão

| Versão | Data | Mudança |
|---|---|---|
| 0.1-rascunho | 2026-04-28 | Setup inicial. Aguarda decisão final sobre repo Lua e sync Drive |
