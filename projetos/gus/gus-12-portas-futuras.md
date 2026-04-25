---
tipo: arquitetura-futuro
area: gus
atualizado: 2026-04-25T15:20-03:00
status: diretriz, sem implementação
---

# Portas futuras do Gus — diretriz arquitetural

Documento de design pra orientar implementação **quando chegar a hora**.
Hoje o Gus existe em 3 portas (Telegram-Claude, Claude Code, Claude Chat web).
Este doc desenha **como adicionar mais portas** sem retrabalho de identidade,
memória ou tools.

**Não é roadmap de execução.** É contrato arquitetural.

---

## Princípio central

**1 vault GitHub + 1 brain Mem0 + N portas que veem tudo.**

Cada porta é um **canal de input/output**, não um agente separado. Uma única
identidade (Gus) vista por canais diferentes.

```
                ┌──────────────────────────────────────┐
                │       REPO Gustpbbr/Gus (vault)      │  ← fonte única
                │       Mem0 brain "gustavo" (único)   │  ← fonte única
                │       metadata.via tagueia origem    │
                └──────────────┬───────────────────────┘
                               │
       ┌──────────────┬────────┼────────┬──────────┬──────────────┐
       │              │        │        │          │              │
  @Tiogubot     @GptGusBot   Claude  Alexa     Custom GPT    Plugin Carro
  Telegram      Telegram      Code   Skill     mobile         (TTS+STT)
  (Sonnet)      (GPT-5)       (esta) (Lambda)  (GPT obrig.)   (?)
   já existe    futuro        existe futuro    futuro         futuro
```

---

## Diretriz 1 — Brain Mem0 único, com tag por origem

Cada memória recebe `metadata.via` na criação:

| Porta | metadata.via |
|---|---|
| Bot Telegram com cérebro Claude | `telegram-claude` (atual default) |
| Bot Telegram com cérebro GPT | `telegram-gpt` |
| Claude Code (sessão de dev) | `claude-code` |
| Alexa skill | `alexa` |
| Custom GPT mobile | `custom-gpt` |
| Plugin de áudio do carro | `carro-audio` |
| Workflow GH (cron, batch) | `workflow-<nome>` |

**Search default não filtra:** qualquer porta vê tudo que qualquer outra escreveu.
**Search filtrado** (`filters={"metadata": {"via": "telegram-gpt"}}`) só pra debug
ou comparação intencional ("o que cada cérebro disse sobre X?").

**Por que único e não separado:** evita memória contraditória cruzada e mantém
o princípio "Gus = entidade única". O ônus de "qual cérebro escreveu" fica como
metadata pesquisável, não como ruptura.

**Implementado:** `gus/memory.py:salvar_memorias` aceita `via` desde 25/04/2026
(default `telegram-claude` via env `MEM0_VIA_TAG`). Cada deploy de porta nova
seta `MEM0_VIA_TAG=<sua-tag>` e fica auto-tagueado.

---

## Diretriz 2 — Vault GitHub único, sem fork

Todas as portas leem/escrevem no **mesmo `Gustpbbr/Gus`**. Sem clones, sem
mirrors. Conflito de escrita simultânea é resolvido pela camada `_save_to_github`
(GET sha → PUT com sha; em 409, retry com sha fresh).

**Decisão pendente quando crescer:** se 3+ portas escreverem ao mesmo tempo,
adicionar lock advisory ou fila. Não é prioridade hoje.

---

## Diretriz 3 — system_prompt em camadas

```
system_prompt
├── base.md        ← identidade Gus, princípios, valores (compartilhado)
├── tools.md       ← descrição das tools (gerado a partir do TOOLS atual)
└── porta-X.md     ← especificidades da porta (estilo, formato, latência)
```

Hoje `gus/system_prompt.md` é um arquivo único. Quando adicionar primeira porta
nova, refatora pra essa estrutura. **Por enquanto, só anotar a ideia.**

Variantes esperadas por porta:

| Porta | Adaptações no system_prompt |
|---|---|
| Telegram-Claude | atual, completo |
| Telegram-GPT | mais conciso (GPT é verboso), reforço de "não suavize" |
| Alexa | TTS-friendly (sem markdown, frases curtas), evitar URLs |
| Custom GPT | OpenAPI schema gerado, instruções de quando usar tools externas |
| Carro-áudio | resposta < 30s de leitura TTS, nada de tabela |

---

## Diretriz 4 — Tools como contrato, não código

`gus/tools.py:TOOLS` é o **catálogo Anthropic-formatado**. Pra outras portas:

| Porta | Como usa |
|---|---|
| Telegram-Claude | nativo (já é Anthropic) |
| Telegram-GPT | conversão automática Anthropic → OpenAI schema (~30 linhas Python). Roteador `executar_tool` continua igual. |
| Claude Code | MCPs (`.claude/mcp/mem0_server.py`, `.claude/mcp/gus_server.py`) — equivalência manual hoje, automatizar quando virar dor |
| Alexa | subset (read-only + ações leves), via Lambda chama `executar_tool` |
| Custom GPT | OpenAPI 3.0 gerado a partir de `TOOLS`, FastAPI hospeda endpoints |
| Carro-áudio | subset (mãos no volante — só leitura + TTS), provider TBD |

**Princípio:** funções Python ficam. O que muda por porta é o **schema** de exposição.

---

## Diretriz 5 — Quem escolhe cérebro

| Porta | Cérebro | Por quê |
|---|---|---|
| Telegram-Claude | Sonnet 4.6 | já calibrado, prompt caching, PT-BR forte |
| Telegram-GPT | GPT-5 (default) | comparação, second opinion |
| Claude Code | Opus/Sonnet | ambiente já é Anthropic |
| Alexa | Sonnet (preferência) ou Haiku (custo) | latência via voz pesa |
| Custom GPT mobile | GPT (obrigatório) | OpenAI hospeda |
| Carro-áudio | Haiku 4.5 (rapidez) | latência crítica |

**Cérebro é configuração**, não estrutura. Trocar Sonnet por GPT no Telegram-Claude
é editar um env var (`MODEL_DEFAULT`), com cuidado de schema de tools.

---

## Diretriz 6 — Portas futuras NÃO derrubam portas atuais

Cada porta tem seu próprio:
- Container/Lambda/processo
- Token (Telegram, Alexa, etc.)
- Variáveis de ambiente
- Logs

O **único acoplamento** é vault + Mem0. Se Alexa der ruim, TioGu segue. Se TioGu
quebrar, Alexa segue.

---

## O que NÃO é unificável

- **Áudio**: Whisper (OpenAI) é universal pra STT, mas TTS varia (ElevenLabs, OpenAI TTS, Polly Alexa). Cada porta escolhe.
- **Capacidades de visão**: Claude tem PDF nativo, GPT processa por página, Gemini tem tudo + code execution. Tools de visão variam.
- **Prompt caching**: estratégia diferente por provedor.
- **Custos**: pagam-se em providers diferentes, mas logger consolidado em `logs/gus_metrics.jsonl` registra origem.

---

## Sequência sugerida de implementação (quando chegar a hora)

Ordem por dependência + ROI:

1. **Telegram-GPT** — porta nova mais simples (mesma stack de `python-telegram-bot`, só muda LLM client). Valida o desenho de "2 cérebros, 1 vault, 1 Mem0 com tag".
2. **Claude Code com paridade total** — atualizar MCPs pra cobrir ações que faltam (ver `gus-11-tools-roadmap.md`). Já estamos nisso.
3. **Custom GPT mobile** — primeiro contato com voz. FastAPI hospeda endpoints, GPT consome.
4. **Alexa** — voz em casa. Reusar arquitetura do Custom GPT (FastAPI), Lambda intermedeia.
5. **Carro-áudio** — última. Depende de hardware/plataforma específica.

Cada porta nova = 3-7 dias dedicados.

---

## Decisões pendentes pra documentar

| Decisão | Pendente porque |
|---|---|
| Brains separados ou tag única? | **Definido: tag única** (esta diretriz) |
| FastAPI próprio ou expor MCPs? | Indefinido — decidir antes do Custom GPT |
| Alexa skill custom ou via Action de IA pronta? | Indefinido — pesquisar custos |
| TTS: ElevenLabs (voice clone) ou padrão? | Tendendo a ElevenLabs |
| Lock advisory pra escrita simultânea no GitHub? | Só implementar se conflito virar dor |

---

## Como atualizar este doc

Quando uma porta nova for implementada (mesmo experimentalmente):
1. Mover ela da seção "futuro" pra "ativa"
2. Documentar o que efetivamente foi feito vs o que estava previsto aqui
3. Atualizar tag da memória usada
4. Adicionar entrada em `gus-11-tools-roadmap.md` com cross-link

Relacionado: [[gus-01-visao-geral]], [[gus-05-portas-capacidades]], [[gus-10-caminho-alexa]], [[gus-11-tools-roadmap]]
