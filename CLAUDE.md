# CLAUDE.md — Briefing do Repositório Gus

Este arquivo é lido automaticamente no início de cada sessão neste repositório.

---

## Quem és tu

Você é uma instância do Claude Code trabalhando no repositório do Gus. Sua memória persistente é o **Hub Qdrant** (coleção `gus_hub`) — acesse via MCP server `mem0-gus` (nome legado, internamente lê do Hub). Antes de responder sobre projetos, preferências ou contexto pessoal, busque memórias relevantes.

Você não é "o Gus" com personalidade definida — isso é pro bot do Telegram. Aqui você é um engenheiro com contexto. Sabe quem é o Gustavo, o que ele faz, como ele trabalha. Mas o foco é técnico.

Para a identidade completa do Gustavo e do Gus, veja `dialogos/_bootstrap/gus-bootstrap.md` (consolidou `gus-identity.md` em 03/05/2026).

---

## Quem é Gustavo

Pesquisador independente brasileiro, anestesiologista. Trabalha exclusivamente via conversa com LLMs — não escreve código, não usa terminal. Toda implementação é feita pela IA, ele valida e executa instruções passo a passo.

Preferências de comunicação: português brasileiro informal, direto, sem formatação excessiva, sem superlativos vazios. Crítica direta é bem-vinda.

---

## O que é o Gus

Gus é um sistema de agente pessoal com **múltiplas portas de acesso**:

- **Telegram** (bot Railway) — captura rápida, foto, áudio, PDF, voz. Personalidade do Gus completa.
- **Claude Code** (esta sessão) — desenvolvimento, manutenção, evolução do sistema. Contexto do Gustavo sem personalidade forçada.
- **Claude Chat** (app) — reflexão, análise, conversa longa. Lê do Google Drive.
- **Portas futuras** — Custom GPT (voz mobile), Alexa (voz em casa).

Todas as portas compartilham:
- **Hub Qdrant** (coleção `gus_hub`) — memória relacional do Gustavo, schema rico (gus-18: tipo / camada_temporal / area / confiança / via)
- **GitHub** (`Gustpbbr/Gus`) — arquivos .md estruturados por pasta
- **Google Drive** — espelho dos .md como Google Docs (sync automático via GitHub Action)

---

## Estado da migração de memória (importante)

**ADR-001 (decidido 27/04/2026):** Mem0 SaaS aposentado em favor do Hub Qdrant direto.

- Hub Qdrant (`gus_hub`) é a fonte da verdade. O bot, MCP, scripts cron e o curador escrevem nele.
- Mem0 SaaS continua existindo só como fallback de leitura em algumas funções, até a Fase 5 do ADR (após 14 dias de coleta dual).
- O **curador híbrido** (`hub/curador.py`) roda **Haiku 4.5** e **Sonnet 4.6** em paralelo no mesmo trecho a cada 3 turnos do Telegram, ambos salvam no Hub com `metadata.curador` distinta + mesmo `hash_janela` pra comparação par-a-par.
- Coleção antiga `gus` (Mem0 self-hosted) tem ~204 mems históricas — workflow `Migrar gus → gus_hub` faz a migração sob demanda.

Quando ler "Mem0" em arquivos pré-migração, entenda como referência histórica — comportamento atual vai pelo Hub.

---

## Arquitetura

```
              GUS (identidade + memória + arquivo)
              ┌──────────────────────────────────┐
              │  Hub Qdrant (gus_hub) → memória  │
              │  GitHub .md          → conhecimento│
              │  gus-bootstrap.md    → identidade │
              └──────────┬───────────────────────┘
                         │
         ┌───────────────┼───────────────────┐
         │               │                   │
    Telegram        Claude Code         Claude Chat
    (bot Railway)   (MCP: Hub+GitHub)   (Project + Drive)
```

**Deploy do bot:** Railway (24/7). Variável `Railway_diagnostic` permite o bot ler os próprios logs via tool `logs_railway`.

---

## Estrutura do código

```
gus/
├── main.py            ← entry point, registra handlers Telegram
├── bot.py             ← handlers: texto, foto, PDF, /start, /reset, /foco, /custo
├── llm.py             ← chama Claude API com loop de tool use, retry exponencial, prompt caching
├── memory.py          ← buscar_memorias / salvar_memorias / deletar_memoria (Hub-first, fallback Mem0)
├── tools.py           ← ~21 tools ativas (web, github, memória, pubmed, arxiv, gpt, dimagem, etc.)
├── media.py           ← processa imagens (Vision Sonnet) + PDF + Word + Excel + voz (Whisper)
├── dimagem.py         ← fluxo OS Dimagem com gate de confiança no OCR
├── logger.py          ← log de custos e latência (JSONL)
├── resumo_log.py      ← log do curador em _log/resumos-mem0/AAAA-MM-DD.md
├── patterns_sensiveis.py ← regex de PII/credenciais (fonte única, R7)
├── system_prompt.md   ← personalidade do Gus (só Telegram)
└── integrations/
    ├── diagnostico.py ← auto_diagnostico (6 checks paralelos, _check_hub lê Hub)
    ├── railway.py     ← logs_railway via Railway GraphQL
    ├── pesquisa.py    ← pesquisar_pubmed + pesquisar_arxiv
    ├── openai_chat.py ← perguntar_gpt (second opinion)
    └── wikilinks.py   ← sugerir_wikilinks

hub/
├── store.py           ← ingestar / lembrar / listar / deletar / contar / stats / ego_cache
├── curador.py         ← curar_turnos / curar_arquivo (Haiku × Sonnet em paralelo)
├── routes.py          ← endpoints FastAPI /hub/* (não usado em produção, manual)
└── schemas.py         ← Pydantic validators do schema gus-18

.claude/
├── mcp/
│   ├── mem0_server.py ← MCP server (nome legado, lê do Hub direto via R6)
│   └── gus_server.py  ← MCP com tools auxiliares (auto_diagnostico, etc.)
└── hooks/
    └── scan_sensivel.py ← PreToolUse, importa patterns de gus.patterns_sensiveis

.github/
├── scripts/
│   ├── _hub_compat.py ← layer de compat Hub→formato Mem0 pros scripts cron
│   ├── auditoria_mem0.py / briefing_matinal.py / export_mem0.py /
│   │   reflexao_quinzenal.py / retrospectiva_semanal.py ← migrados pra Hub (R2)
│   ├── ingest_mem0_from_chat.py ← usa hub.curador.curar_arquivo (Fase 2.5)
│   ├── migrar_gus_para_hub.py ← migração gus → gus_hub (Fase 4)
│   ├── check_saude.py ← cron 7h30 BRT, alerta Telegram só em warn/erro
│   └── requirements.txt ← deps mínimas dos scripts
└── workflows/         ← 16 workflows (cron diário/semanal/quinzenal + dispatch manual)
```

---

## Tools do bot Telegram (~22 ativas)

Lista completa em `gus/tools.py`. Categorias principais:

- **GitHub:** `read_from_github`, `list_github_directory`, `list_branches`, `list_commits`, `save_to_github`
- **Memória:** `search_memory` (Hub Qdrant primário, Mem0 fallback), `salvar_memoria_gus`, `buscar_memoria_gus`, `deletar_memoria`, `auditoria_mem0` (lê arquivo, gerado pelo cron)
- **Web:** `search_web` (Tavily + DuckDuckGo fallback), `pesquisar_pubmed`, `pesquisar_arxiv`
- **Diagnóstico:** `auto_diagnostico` (6 checks: GitHub/Hub Qdrant/Anthropic/Tavily/volume/workflows), `logs_railway`
- **Roteamento:** `rotear_arquivo` (Estágio 1 do plano de roteamento — move/cria/anexa arquivos de `dialogos/inbox-*/` pro destino correto, sob aprovação explícita do Gustavo)
- **Outros:** `perguntar_gpt`, `disparar_workflow`, `sugerir_wikilinks`, `criar_acao`, `meta_memoria`

Detalhes de quando usar cada uma → `gus/system_prompt.md`.

---

## Ferramentas do Claude Code (esta sessão)

**MCP `mem0-gus`** (nome legado, internamente Hub) — `buscar_memorias`, `salvar_memoria`, `listar_memorias`, `deletar_memoria` + variantes `*_gus` pro brain user_id="gus".

**MCP `gus`** (auxiliar) — `auto_diagnostico`, `perguntar_gpt`, `sugerir_wikilinks`.

**GitHub MCP** — ferramentas `mcp__github__*` para gerenciar o repositório.

**Hooks ativos:**
- `PreToolUse:scan_sensivel` — bloqueia Write/Edit com PII/credenciais fora de `sensivel/`
- `Stop:retro-engine` — log de fim-de-sessão em `_log/retro-engine-claude-code/AAAA-MM-DD.md`
- `Stop:git-check` — avisa se há mudanças não commitadas

> **AVISO IMPORTANTE — Captura de memória da porta Code quebrada (2026-05-01):**
>
> Este ambiente Claude Code on the web não tem `ANTHROPIC_API_KEY`, `QDRANT_URL`
> nem `QDRANT_API_KEY`. Por causa disso:
>
> 1. O hook `Stop:retro-engine` é silent no-op (esperava as vars em
>    `~/.claude/gus.env`, que não existe aqui). O log de fim-de-sessão agora
>    registra honestamente "no-op: anthropic_missing" em vez da mentira
>    anterior "(sessão trivial — nada extraído)".
>
> 2. As tools MCP `mcp__mem0-gus__salvar_memoria*` também falham: o servidor
>    MCP precisa das vars do Qdrant pra escrever no Hub. Captura proativa
>    via tool MCP **não funciona** neste ambiente. Tentar isso só causa
>    erro + atrito de UX (cada call pede autorização).
>
> **Caminho real (a implementar):** cron GitHub Actions processa transcripts
> commitados pela porta Code → roda curador (Haiku × GPT) → salva fragmentos
> bidirecionais (`gus` + `gustavo`) no Hub via secrets do GitHub Actions.
> Demanda: `dialogos/inbox-claude-code/2026-05-01-curador-bidirecional-cron.md`.
>
> **Enquanto não consertar:** conhecimento dessa porta sobrevive só via
> commits, PRs, docs `gus-XX/*.md` e demandas em `dialogos/inbox-*/`.
> Não tentar `mcp__mem0-gus__salvar_memoria*` proativamente — vai falhar.

---

## Estrutura de pastas do repositório (onde os MDs são salvos)

```
pessoal/saude/                ← exames, consultas, historico-saude.md (mestre)
pessoal/financeiro/           ← extratos, overview.md, resumo-financeiro.md (mestre)
pessoal/diario/               ← reflexões pessoais (auto-geradas pela retrospectiva semanal)
pessoal/paty-dos-alferes/     ← projeto da casa (documentos, arquitetura, casa, jardim)
dimagem/protocolos/           ← protocolos clínicos (sedação, anestesia, jejum, etc.)
dimagem/casos/                ← casos didáticos (LGPD: pseudônimo)
dimagem/dia/                  ← OS de cada dia (schema único em SCHEMA.md)
dimagem/admin/                ← pendências administrativas
receitas/doces|salgadas/      ← receitas com subpastas
esportes/                     ← evolucao.md (mestre) + treinos/
leituras/livros|papers/       ← anotações de livros e papers
contatos/                     ← mapa.md de relacionamentos (não-sensível)
familia/                      ← registros sobre família (futuras páginas por membro)
projetos/                     ← phronesis-bench, mge, ter, axon, gus, blueprint-agente, Lua
agenda/                       ← agenda mensal (referenciada por wikilinks)
acoes/                        ← fila de ações (executor pendente)
capturado/                    ← captura rápida (links, ideias, misc, visual)
sensivel/                     ← dados protegidos (NÃO sincronizam pro Drive)
_indices/                     ← MOCs por área + auditorias diárias do Hub
_log/                         ← curador, retro-engine, sessões
dialogos/                     ← protocolo de comunicação entre portas
hub/                          ← código do Hub Qdrant
gus/                          ← código do bot Telegram
api/                          ← FastAPI (Custom GPT)
historico/                    ← legacy / uso único (deletável sem impacto)
```

**Reorganização 28/04/2026 (segunda etapa):**
- Criadas pastas que estavam declaradas mas não existiam: `pessoal/saude/`,
  `esportes/`, `leituras/`, `contatos/`, `familia/`
- Criadas subpastas em `dimagem/`: `casos/`, `protocolos/`, `admin/`
- Criadas subpastas em `capturado/`: `links/`, `ideias/`, `misc/`
- Criados MD mestre vazios (templates): `pessoal/saude/historico-saude.md`,
  `pessoal/financeiro/resumo-financeiro.md`, `esportes/evolucao.md`,
  `contatos/mapa.md`
- Criado `dimagem/dia/SCHEMA.md` documentando schema único (resolve
  fragmentação observada com sufixos `-assim`, `-outros`)
- Conteúdo existente preservado — não foi apagado nada

**Reorganização 28/04/2026 (primeira etapa):** pastas `docs/`, `scripts/`,
`textos-antigos/`, `tiogubot/` e arquivo `get_token.py` foram movidos pra
`historico/` pra desinchar a raiz. Sync Drive já atualizado
(`sync_to_drive.py:EXCLUDE_PREFIXES` agora exclui `historico/` em vez de
`docs/`).

---

## O que está pronto

- [x] Bot Telegram com ~21 tools (texto, foto, PDF, Word, Excel, voz)
- [x] Hub Qdrant Fase 1–4 (ingest, curador híbrido, leitura Hub-first, migração)
- [x] Curador híbrido Haiku × Sonnet em paralelo (coleta dual até 12/05/2026)
- [x] Curador chat ingest (Claude Chat → arquivo → Hub)
- [x] Retro Engine (hook Stop, log do que cada sessão Claude Code aprendeu)
- [x] Patterns sensíveis fonte única + 5 patterns novos (R7)
- [x] Scripts cron migrados pra Hub (R2)
- [x] MCP Claude Code lendo Hub (R6)
- [x] OCR Dimagem com gate de confiança (#4 inbox)
- [x] Sync GitHub → Google Drive via GitHub Action
- [x] Validators Pydantic schema gus-18
- [x] Bootstrap-v5
- [x] Tagueamento `via` em toda escrita Hub
- [x] `Railway_diagnostic` configurado, `logs_railway` ativo

## O que falta

- [ ] Disparar workflow `Migrar gus → gus_hub` se ainda não rodou (preenche Hub com 204 mems históricas)
- [ ] Conferir secrets `QDRANT_URL`/`QDRANT_API_KEY` no GitHub (usado pelos crons migrados em R2)
- [ ] Decisão modelo curador final (Fase 5 do ADR-001 — após 14 dias coleta dual)
- [ ] Aposentar Mem0 SaaS completamente (Fase 5: remover fallbacks, requirements, secrets)
- [ ] Suporte a vídeo no Telegram (`filters.VIDEO` sem handler)
- [ ] Configurar Service Account do Google Drive (Drive sync) — pendente desde sempre

---

## Demandas e protocolo de comunicação

- Demandas formais entre portas → `dialogos/streams/semana-AAAA-MM-DD.md` (cronológico)
- Demandas direcionadas pra Claude Code → `dialogos/inbox-claude-code/`
- Demandas direcionadas pro TioGu (Telegram) → `dialogos/inbox-tiogu/`
- Após processar, atualiza frontmatter (`status: concluido`) — workflow `archive-completed-demandas.yml` move sozinho

---

## Regra de ouro

Gustavo não programa. Se precisar fazer algo no código, você executa. Se precisar de ação em conta externa (Railway, Qdrant Cloud, Telegram, Google), dê instruções simples para ele executar pelo celular.
