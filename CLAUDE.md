# CLAUDE.md — Briefing do Repositório Gus

Este arquivo é lido automaticamente no início de cada sessão neste repositório.

---

## Quem és tu

Você é uma nova instância do Claude, abrindo este repositório pela primeira vez. Outra instância — em outro repositório, numa sessão anterior — construiu tudo isso aqui e escreveu este briefing pra você. Gustavo não programa diretamente, então a continuidade depende deste documento.

---

## Quem é Gustavo

Pesquisador independente brasileiro, anestesiologista. Trabalha exclusivamente via conversa com LLMs — não escreve código, não usa terminal. Toda implementação é feita pela IA, ele valida e executa instruções passo a passo (colar texto, preencher formulários, configurar serviços).

Preferências de comunicação: português brasileiro informal, direto, sem formatação excessiva, sem superlativos vazios. Crítica direta é bem-vinda.

---

## O que é este repositório

**Gus** é um agente pessoal do Gustavo que roda como bot no Telegram. A ideia central: Gustavo manda qualquer coisa pelo Telegram (texto, foto, PDF) e o Gus analisa, responde com contexto, salva no Mem0 como memória e escreve no GitHub como arquivo Markdown estruturado.

Não é um chatbot genérico. É uma camada de memória e organização pessoal que funciona 24/7 na nuvem, sem depender de computador ligado ou GitHub aberto.

---

## Arquitetura

```
Gustavo (celular, Telegram)
        ↓
Bot Telegram (python-telegram-bot)
        ↓
Claude API (Anthropic) — com tool use
        ↓
┌───────────────────┬──────────────────┬──────────────────┐
│   Mem0 (memória)  │  GitHub (storage) │  DuckDuckGo (web) │
│ fragmentos da     │ arquivos .md por  │ busca de fatos    │
│ identidade e      │ pasta e categoria │ atuais quando     │
│ conversas         │ (escrita e leitura│ necessário        │
└───────────────────┴──────────────────┴──────────────────┘
        ↓
Resposta no Telegram
```

**Deploy:** Railway (servidor na nuvem, 24/7, sem custo de máquina local)

---

## Estrutura do código

```
gus/
├── main.py          ← entry point, inicializa o bot Telegram
├── bot.py           ← handlers: texto, foto, PDF, /start, /reset
├── llm.py           ← chama Claude API com loop de tool use
├── memory.py        ← busca e salva no Mem0
├── tools.py         ← 3 tools: search_web, save_to_github, read_from_github
├── media.py         ← processa imagens (visão) e PDFs (extração de texto)
├── logger.py        ← log de custos e latência
└── system_prompt.md ← personalidade do Gus + estrutura de pastas do repo
```

---

## As 3 tools do Gus

**`search_web`** — busca no DuckDuckGo. Claude chama quando precisa de informação atual.

**`save_to_github`** — cria ou atualiza arquivo .md no repositório GitHub do Gustavo. Claude decide a pasta automaticamente pelo conteúdo. Parâmetros: `filename`, `content`, `folder`.

**`read_from_github`** — lê um arquivo .md do repositório por path. Claude chama antes de responder sobre saúde, projetos, finanças — sempre que o conteúdo pode estar salvo. Parâmetro: `path`.

---

## Estrutura de pastas do repositório GitHub (onde os MDs são salvos)

```
pessoal/saude/          ← exames, consultas, historico-saude.md (mestre)
pessoal/financeiro/     ← extratos, resumo-financeiro.md (mestre)
pessoal/diario/         ← reflexões pessoais
dimagem/protocolos/     ← protocolos da clínica de anestesia
dimagem/casos/          ← casos interessantes
dimagem/admin/          ← pendências administrativas
receitas/doces/         ← receitas de doces (com subpastas: tortas, bolos...)
receitas/salgadas/      ← receitas salgadas (massas, carnes...)
esportes/treinos/       ← registros de treinos
esportes/              ← evolucao.md (mestre de progresso)
leituras/livros/        ← livros lidos
leituras/papers/        ← papers lidos
projetos/phronesis-bench/
projetos/mge/
projetos/ter/
projetos/axon/
projetos/gus/           ← notas sobre o próprio sistema
capturado/links/        ← artigos e posts salvos
capturado/ideias/       ← insights soltos
capturado/misc/         ← qualquer coisa sem categoria
```

Pastas são criadas automaticamente quando um arquivo é salvo — não precisa criar antes.

---

## O que já está pronto

- [x] Código completo do bot (main, bot, llm, memory, tools, media, logger)
- [x] Tool `save_to_github` — escreve MDs no repo
- [x] Tool `read_from_github` — lê MDs do repo por path
- [x] Tool `search_web` — busca na web via DuckDuckGo
- [x] Integração Mem0 — busca antes de responder, salva depois
- [x] Suporte a texto, fotos e PDFs no Telegram
- [x] System prompt com personalidade, estrutura de pastas e regras de nomenclatura
- [x] Dockerfile + railway.toml prontos para deploy
- [x] Repositório no GitHub: https://github.com/Gustpbbr/Gus

---

## O que falta fazer

- [ ] **Deploy no Railway** ← próximo passo imediato
- [ ] Configurar variáveis de ambiente no Railway (lista abaixo)
- [ ] Testar: mandar `/start` pro bot e confirmar que responde
- [ ] Fazer a entrevista de boas-vindas (ver `docs/gus-entrevista-boas-vindas.md`)
- [ ] Criar o `pessoal/saude/historico-saude.md` mestre com condições atuais do Gustavo
- [ ] Popular Mem0 com contexto inicial (opcional, cresce organicamente pelo uso)

---

## Deploy no Railway — passo a passo

Gustavo não usa terminal. Todo o processo é pelo navegador do celular.

**1.** Acessa railway.app → "Start a New Project" → "Login with GitHub"

**2.** "New Project" → "Deploy from GitHub repo" → seleciona `Gustpbbr/Gus`

**3.** Railway detecta o Dockerfile automaticamente e inicia o build

**4.** No painel do projeto → "Variables" → adicionar estas variáveis:

```
TELEGRAM_BOT_TOKEN     = token do BotFather
TELEGRAM_CHAT_ID       = chat_id pessoal do Gustavo
ANTHROPIC_API_KEY      = sk-ant-...
MEM0_API_KEY           = m0-...
GITHUB_TOKEN           = Personal Access Token com permissão repo
GITHUB_REPO            = Gustpbbr/Gus
MODEL_DEFAULT          = claude-sonnet-4-6
MAX_TOKENS_RESPONSE    = 2048
HARD_LIMIT_USD_MONTH   = 30
```

**5.** Após deploy → abrir Telegram → mandar `/start` pro bot → ele responde com o chat_id

**6.** Se o chat_id mostrado for diferente do configurado, atualizar `TELEGRAM_CHAT_ID` no Railway

---

## Variáveis que Gustavo precisa ter em mãos

- **TELEGRAM_BOT_TOKEN** — criado no BotFather (Telegram). Se não tiver: buscar `@BotFather` no Telegram → `/newbot`
- **TELEGRAM_CHAT_ID** — o bot mostra quando você manda `/start`. Pegar lá.
- **ANTHROPIC_API_KEY** — em console.anthropic.com → API Keys
- **MEM0_API_KEY** — em app.mem0.ai → criar conta grátis → API Key (10k memórias grátis/mês)
- **GITHUB_TOKEN** — GitHub → Settings → Developer settings → Personal access tokens → marcar `repo`

---

## Contexto adicional

Este repositório foi extraído do repositório maior `Gustpbbr/Segundo-cerebro`, que contém múltiplos projetos de pesquisa. O Gus é o projeto de agente pessoal, isolado aqui pra ter repositório limpo e deploy independente.

O Segundo Cérebro contém projetos como Phronesis-Bench (benchmark de metacognição para LLMs), MGE/MGX, TER e Axon — todos projetos de pesquisa em IA do Gustavo.

O Gus eventualmente vai ler e escrever no repositório do Segundo Cérebro também, mas por ora o `GITHUB_REPO` aponta só pro `Gustpbbr/Gus`.

---

## Regra de ouro para esta sessão

Gustavo não programa. Se precisar fazer algo no código, você executa. Se precisar de uma ação que depende de conta externa (Railway, Mem0, Telegram), você dá as instruções mais simples possíveis para ele executar pelo celular.
