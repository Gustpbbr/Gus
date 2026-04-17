# CLAUDE.md — Briefing do Repositório Gus

Este arquivo é lido automaticamente no início de cada sessão neste repositório.

---

## Quem és tu

Você é uma instância do Claude Code trabalhando no repositório do Gus. Você tem acesso à memória do Gustavo via Mem0 (MCP server) — **use-a**. Antes de responder sobre projetos, preferências ou contexto pessoal, busque memórias relevantes.

Você não é "o Gus" com personalidade definida — isso é pro bot do Telegram. Aqui você é um engenheiro com contexto. Sabe quem é o Gustavo, o que ele faz, como ele trabalha. Mas o foco é técnico.

Para a identidade completa do Gustavo e do Gus, veja `gus/gus-identity.md`.

---

## Quem é Gustavo

Pesquisador independente brasileiro, anestesiologista. Trabalha exclusivamente via conversa com LLMs — não escreve código, não usa terminal. Toda implementação é feita pela IA, ele valida e executa instruções passo a passo.

Preferências de comunicação: português brasileiro informal, direto, sem formatação excessiva, sem superlativos vazios. Crítica direta é bem-vinda.

---

## O que é o Gus

Gus é um sistema de agente pessoal com **múltiplas portas de acesso**:

- **Telegram** (bot Railway) — captura rápida, foto, áudio, PDF. Personalidade do Gus completa.
- **Claude Code** (esta sessão) — desenvolvimento, manutenção, evolução do sistema. Contexto do Gustavo sem personalidade forçada.
- **Claude Chat** (app) — reflexão, análise, conversa longa. Lê do Google Drive.

Todas as portas compartilham:
- **Mem0** — memória relacional do Gustavo
- **GitHub** — arquivos .md estruturados por pasta
- **Google Drive** — espelho dos .md como Google Docs (sync automático via GitHub Action)

---

## Arquitetura

```
              GUS (identidade + memória + arquivo)
              ┌─────────────────────────────────┐
              │  Mem0         → memória viva     │
              │  GitHub .md   → conhecimento     │
              │  gus-identity.md → identidade    │
              └──────────┬──────────────────────┘
                         │
         ┌───────────────┼───────────────────┐
         │               │                   │
    Telegram        Claude Code         Claude Chat
    (bot Railway)   (MCP: Mem0+GitHub)  (Project + Drive)
```

**Deploy do bot:** Railway (24/7, sem custo de máquina local)

---

## Estrutura do código

```
gus/
├── main.py            ← entry point, inicializa o bot Telegram
├── bot.py             ← handlers: texto, foto, PDF, /start, /reset
├── llm.py             ← chama Claude API com loop de tool use (max 10 rounds)
├── memory.py          ← busca e salva no Mem0
├── tools.py           ← 3 tools: search_web, save_to_github, read_from_github
├── media.py           ← processa imagens (visão) e PDFs (extração de texto)
├── logger.py          ← log de custos e latência (JSONL)
├── system_prompt.md   ← personalidade do Gus (só Telegram)
└── gus-identity.md    ← identidade compartilhada (todas as portas)

.claude/mcp/
└── mem0_server.py     ← MCP server: expõe Mem0 como ferramenta do Claude Code

.github/
├── scripts/sync_to_drive.py   ← sincroniza .md → Google Drive
├── scripts/export_mem0.py     ← exporta memórias do Mem0 → GitHub/Drive
└── workflows/                 ← GitHub Actions (sync, export)
```

---

## As 3 tools do Gus (bot Telegram)

**`search_web`** — busca no DuckDuckGo. Claude chama quando precisa de informação atual.

**`save_to_github`** — cria ou atualiza .md no repositório. Inclui frontmatter automático com data/hora (Brasília) e `via: telegram`.

**`read_from_github`** — lê .md do repositório por path. Claude chama antes de responder sobre saúde, projetos, finanças.

---

## Ferramentas do Claude Code (esta sessão)

**Mem0 MCP** — `buscar_memorias`, `salvar_memoria`, `listar_memorias`. Acessa a mesma base de memória do bot Telegram.

**GitHub MCP** — ferramentas `mcp__github__*` para gerenciar o repositório.

---

## Estrutura de pastas do repositório (onde os MDs são salvos)

```
pessoal/saude/          ← exames, consultas, historico-saude.md (mestre)
pessoal/financeiro/     ← extratos, resumo-financeiro.md (mestre)
pessoal/diario/         ← reflexões pessoais
dimagem/protocolos/     ← protocolos da clínica
dimagem/casos/          ← casos interessantes
dimagem/admin/          ← pendências administrativas
receitas/doces/         ← receitas (com subpastas)
receitas/salgadas/
esportes/treinos/       ← registros de treinos
esportes/               ← evolucao.md (mestre)
leituras/livros/
leituras/papers/
projetos/               ← phronesis-bench, mge, ter, axon, gus
capturado/links/        ← artigos salvos
capturado/ideias/       ← insights soltos
capturado/misc/
```

---

## O que está pronto

- [x] Código completo do bot (7 módulos Python)
- [x] 3 tools funcionais (web, read, save) com validação de segurança
- [x] Integração Mem0 (busca + salva)
- [x] Suporte a texto, fotos e PDFs no Telegram
- [x] Mapa de preços dinâmico (Opus 4.7 / Sonnet / Haiku)
- [x] Timeouts, path traversal protection, auth deny-all
- [x] Frontmatter automático com data/hora nos MDs
- [x] Sync GitHub → Google Drive via GitHub Action
- [x] MCP server Mem0 pro Claude Code
- [x] Identidade unificada (gus-identity.md)
- [x] Dockerfile + railway.toml

## O que falta

- [ ] Deploy no Railway (Gustavo configura pelo navegador)
- [ ] Configurar Google Drive sync (Service Account + secrets)
- [ ] Configurar MCP server Mem0 no Claude Code (MEM0_API_KEY)
- [ ] Entrevista de boas-vindas via Telegram
- [ ] Export diário do Mem0 pro Drive (GitHub Action cron)

---

## Regra de ouro

Gustavo não programa. Se precisar fazer algo no código, você executa. Se precisar de ação em conta externa (Railway, Mem0, Telegram, Google), dê instruções simples para ele executar pelo celular.
