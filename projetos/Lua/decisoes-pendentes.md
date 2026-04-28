---
tipo: decisoes-pendentes
agente: Lua
atualizado: 2026-04-28
status: aguardando-entrevista-com-dono
---

# Decisões pendentes pra Lua "ir ao ar"

Lista do que falta ser decidido pelo dono **antes** da Lua sair do
papel e virar agente em produção.

Cada item marcado com `⏳ A DECIDIR NA ENTREVISTA` em outros arquivos
da pasta `projetos/Lua/` corresponde a um item desta lista.

---

## Bloco 1 — Identidade (núcleo)

### 1.1 — Refinar quem Lua é

Hoje em `identidade/lua-identity.md`, parágrafo de abertura é genérico.
Refinar com:
- Quais 3-5 frases-chave definem Lua melhor que o atual?
- Lua tem alguma característica que a diferencia de qualquer outro
  agente pessoal?
- Existe alguma "razão" pra Lua existir além de "queria ter outra
  instância"?

### 1.2 — Por que Lua existe (vs já ter outro agente)

- Razão concreta: [⏳ A DECIDIR]
- Domínio que cobre que o outro não cobre: [⏳ A DECIDIR]
- Lua e outro agente compartilham dono mas tem propósitos diferentes,
  ou são pra contextos totalmente separados?

### 1.3 — Tom específico

Hoje: "PT-BR informal direto, crítica sem suavizar, sem superlativos
vazios" — herdado de boas práticas comuns. Refinar:

- Padrões verbais idiossincráticos?
- Lua é mais ou menos formal que outro agente do mesmo dono?
- Lua usa metáforas/analogias específicas?
- Lua faz perguntas socráticas? Direta na resposta?
- Lua tem alguma assinatura verbal? (fórmula recorrente, sem ser
  cringe)

### 1.4 — Princípios

Hoje em `identidade/principios.md` — 7 princípios genéricos. Refinar:

- Quais manter como-está?
- Quais remover (não fazem sentido pra Lua)?
- Quais adicionar (específicos da Lua)?
- Reordenar por importância?

### 1.5 — Como Lua reage a divergência com o dono

Hoje: "argumenta uma vez, insiste se grave, anota se trivial" —
herdado. Manter? Mudar?

---

## Bloco 2 — Operação

### 2.1 — Frequência do curador

Hoje: "a cada 3 turnos" (default herdado). Manter? Mudar pra outro
intervalo?

### 2.2 — Brain do agente (auto-observações)

Lua vai ter brain `user_id="lua"` próprio pra auto-observações? Ou
foca só no brain do dono?

Recomendação default: **sim**, ter brain próprio. Mas decisão é do
dono.

### 2.3 — Idioma dos brains

Memórias salvas em PT-BR (mesmo idioma das conversas)? Ou Lua salva
internamente em outro idioma (ex: EN) pra "neutralizar" o tom?

Recomendação default: **PT-BR**, mesmo idioma das conversas. Mas
algumas instâncias preferem EN pra evitar viés de tom.

---

## Bloco 3 — Portas

### 3.1 — Portas iniciais

Quais portas implementar primeiro?

- [ ] **Telegram** (recomendado começar) — bot dedicado pra Lua
- [ ] **Claude Chat** — Project no claude.ai
- [ ] **Custom GPT mobile** (voz)
- [ ] **Web custom** (FastAPI, ainda não-implementado em outro agente)
- [ ] **Alexa** (futuro)
- [ ] **Outras**?

Default sugerido: começar Telegram (mais simples, mais útil), depois
Claude Chat (zero infra), depois Custom GPT.

### 3.2 — Bot Telegram

- Nome do bot: `@LuaBot`? `@LuaPessoal`? Outro?
- Avatar: imagem específica?
- Comandos custom: mesmos do outro agente (`/start`, `/reset`,
  `/custo`, `/foco`) ou diferentes?

### 3.3 — Repositório próprio ou compartilhado

Lua mora:
- (a) **No mesmo repositório** que outro agente já existente, em
  pasta dedicada — mais simples, compartilha CI/CD, mas mistura
  identidades em árvore git
- (b) **Em repositório próprio** (ex: `Gustpbbr/Lua`) — mais limpo,
  separação total, mas duplica setup de infra

Recomendação: **(b) repositório próprio**, depois que decisões 1.x
estiverem fechadas. Por enquanto, fica em `projetos/Lua/` no repo
existente.

### 3.4 — Custos separados ou compartilhados

- Conta Anthropic: usar a mesma do outro agente, ou criar nova?
- Qdrant Cloud: nova coleção `lua_hub` no mesmo cluster, ou cluster
  separado?
- Telegram bot: novo @LuaBot via BotFather (gratuito)
- Railway: novo deploy próprio

Recomendação default:
- Anthropic: mesma conta (mais barato administrativamente)
- Qdrant: mesma cluster, coleção nova `lua_hub`
- Railway: deploy novo (custos visíveis separados)
- Telegram: bot novo

---

## Bloco 4 — Memória

### 4.1 — Coleção Qdrant

Nome: `lua_hub` (recomendado). Outro?

### 4.2 — Schema dos fragmentos

Reutilizar exatamente o schema gus-18 (tipo, camada_temporal, area,
confiança, via, etc.)? Ou Lua tem schema próprio?

Recomendação default: **mesmo schema**. Nada na Lua exige campos
diferentes neste momento.

### 4.3 — Migração de memórias

Importar memórias antigas de outro agente pra Lua começar com algo,
ou Lua começa **completamente vazia**?

Recomendação default: **vazia**. Lua deve construir memória própria.

---

## Bloco 5 — Setup operacional

### 5.1 — Ordem de implementação

Quando todas as decisões 1-4 estiverem fechadas, ordem sugerida pra
implementar:

1. Setup contas externas (Anthropic, Qdrant `lua_hub`, BotFather, Railway)
2. Estrutura repositório próprio (ou pasta dedicada)
3. Identidade canônica final (4 arquivos preenchidos com decisões)
4. Bot Telegram com tools mínimos (5-7 tools, não os 22 do outro
   agente)
5. Curador automático
6. Vault GitHub estruturado
7. Crons de auditoria, briefing, retrospectiva
8. Outras portas (Claude Chat → Custom GPT → ...)

### 5.2 — Quem implementa

- IA implementadora: Claude Code? Outro?
- Dono no loop revisando cada PR?

### 5.3 — Quando começar a usar

Após Bot Telegram funcional + curador rodando, começar a usar com
**conversas simples** (testar tom, salvamento de memórias) por 1-2
semanas antes de adicionar mais portas.

---

## Próximo passo

**Marcar entrevista de descoberta com o dono** pra responder os
itens dos Blocos 1-3. Bloco 4 e 5 podem ser decididos durante
implementação.

Tempo estimado pra entrevista: 30-60 minutos. Pode ser:
- Conversa direta no Telegram com outro agente já existente, que
  registra as respostas
- Sessão de Claude Chat dedicada, com este arquivo aberto, marcando
  as decisões à medida que conversam
- Texto livre que o dono escreve quando puder, depois sintetizado em
  decisões formais
