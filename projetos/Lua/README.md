# Lua

Agente pessoal de IA. Identidade própria, memória persistente, múltiplas
portas (Telegram, Web, Custom GPT mobile, etc.). Dono inicial:
**Gustavo Pratti de Barros**.

> **Status (2026-04-28):** Identidade em rascunho genérico. Decisões
> finais sobre tom, princípios e personalidade pendentes — entrevista
> de descoberta marcada com o dono.
>
> Os arquivos aqui são **descritivos** — eles definem quem Lua é, mas
> Lua **ainda não está implantada** (nenhum bot rodando, nenhuma porta
> ativa). Quando aprovados, são copiados pra repositório próprio da Lua
> e a implementação acontece lá.

## Estrutura

```
projetos/Lua/
├── README.md                       ← este arquivo (entrada)
├── decisoes-pendentes.md           ← lista do que falta resolver
│
├── identidade/                     ← QUEM Lua é
│   ├── lua-identity.md             ← cartão de identidade canônico
│   ├── principios.md               ← pilares não-negociáveis
│   ├── lua-bootstrap.md            ← script de ativação pra Claude Chat
│   └── lua-meta-memoria.md         ← autobiografia narrativa (cresce com o uso)
│
├── system-prompts/                 ← personalidades por porta
│   ├── telegram.md                 ← Lua no bot Telegram
│   └── claude-chat-instructions.md ← Instructions do Project Claude Chat
│
├── portas/                         ← como configurar cada canal de I/O
│   ├── telegram-setup.md           ← passo a passo (BotFather, Railway)
│   ├── claude-chat-setup.md        ← passo a passo (Project, bootstrap)
│   ├── custom-gpt-setup.md         ← passo a passo (Builder DESKTOP)
│   ├── web-setup.md                ← roadmap (FastAPI custom)
│   └── alexa-setup.md              ← roadmap (Skill voz casa)
│
└── memoria/                        ← memória persistente
    ├── setup-qdrant.md             ← criar coleção `lua_hub`
    └── schema-fragmentos.md        ← schema dos fragmentos atômicos
```

## Como ler esta pasta (na ordem)

1. **`identidade/lua-identity.md`** — quem Lua é (genérico hoje, refinado na entrevista)
2. **`identidade/principios.md`** — o que Lua nunca/sempre faz
3. **`decisoes-pendentes.md`** — o que falta decidir antes da Lua "ir ao ar"
4. **`portas/telegram-setup.md`** — primeira porta a implementar
5. Resto sob demanda conforme avançar

## Próximos passos

- [ ] Entrevista de descoberta com o dono pra preencher placeholders na identidade
- [ ] Aprovar princípios (lista ainda genérica, herdada de boas práticas comuns)
- [ ] Decidir nome do bot Telegram (`@LuaBot`? Outro?)
- [ ] Criar contas externas (Anthropic, Qdrant Cloud separado, Telegram Bot, Railway)
- [ ] Decidir se Lua compartilha repositório com o agente atual ou ganha repo próprio
- [ ] Implementar Etapa 1 do roadmap em `00-leia-primeiro/passo-a-passo-resumido.md`
  (do blueprint genérico em `projetos/blueprint-agente/`)

## Relação com o blueprint genérico

A pasta `projetos/blueprint-agente/` (no mesmo repo) tem o **molde
neutro** que serviu de base pra esta pasta. A Lua é a **primeira
instância** do blueprint sendo preenchida.

Diferenças:
- **Blueprint** usa `{{NOME_AGENTE}}`, `{{PROPOSITO}}`, etc.
- **Lua** tem placeholders **preenchidos com defaults sensatos** ou
  com **decisões já tomadas pelo dono**. Onde ainda não tem decisão,
  marca explícita `<!-- ⏳ A DECIDIR NA ENTREVISTA -->`.

Quando Lua amadurecer e ganhar repositório próprio, a pasta inteira
é copiada pra lá. Blueprint genérico fica aqui no repo Gus pra futuras
instâncias.

## Aviso de reprodutibilidade

Este documento descreve a Lua como conceito. Implementação técnica
real (código Python, workflows, infra) acontece **só depois** das
decisões da entrevista de descoberta. Hoje a pasta serve de:

1. Memória institucional do que decidimos
2. Esqueleto pra preencher
3. Base pra clonar pra repositório próprio quando chegar a hora
