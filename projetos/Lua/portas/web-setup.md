---
tipo: setup-porta
porta: web-custom
agente: Lua
estimativa: ~4-6h (não-implementado em outros agentes ainda)
status: roadmap-futuro
---

# Setup — Porta Web custom da Lua

> **Atenção:** porta **AINDA NÃO TEM IMPLEMENTAÇÃO DE REFERÊNCIA**. O
> agente irmão não tem porta web custom (só usa claude.ai como porta
> web genérica). Este documento é **roadmap conceitual** — implementação
> precisa ser construída do zero.

---

## O que essa porta seria

Um **app web próprio** (URL dedicada, ex: `lua.gustavo.dev` ou
`app.lua.com`) onde o dono interage com a Lua via interface custom,
não dependendo do claude.ai.

Por que essa porta poderia existir:

- **Independência** de plataforma — Lua continua funcionando se
  Anthropic mudar política de Custom GPTs (Builder mobile, etc.)
- **UX customizada** — interface adaptada ao tipo de uso (ex: lista
  de memórias visíveis, busca direta no Hub, dashboard de custos)
- **Integração nativa com Hub Qdrant** — sem ter que passar por
  Telegram nem Action HTTP
- **Multi-usuário** (futuro) — se Lua um dia atender mais de um dono

---

## Por que NÃO é prioritário no V1

- **Customizada com claude.ai** já cobre 90% do caso "interface web
  pra Lua"
- **Custo de implementação alto** — frontend + backend + auth + UI
- **Manutenção contínua** — segurança, atualizações, deploy
- **Não há necessidade clara** ainda — Telegram + claude.ai cobrem
  textualmente; Custom GPT cobre voz mobile

Recomendação: **adiar até motivo concreto** aparecer.

---

## Quando reconsiderar

Implementar essa porta faz sentido se:

1. **Limite do Telegram** — bot Telegram tem limites de UX (não
   mostra estado de memória, não tem dashboard, etc.)
2. **Necessidade multi-usuário** — Lua precisa atender N donos, cada
   um com seu vault e brain isolado
3. **Funcionalidade não-conversacional** — gráfico de evolução de
   custos, gerenciador visual de memórias, sandbox de testes de
   identidade
4. **Custom GPT inviável** — Anthropic ou OpenAI muda política de
   Action / Custom GPT e essa porta vira plano B

---

## Esboço de arquitetura (roadmap)

Se for implementar:

```
Lua/
├── webapp/                           ← novo módulo
│   ├── frontend/                     ← Next.js, Vite+React, Svelte, etc.
│   │   ├── pages/
│   │   │   ├── chat.tsx              ← chat com Lua
│   │   │   ├── memorias.tsx          ← visualizar memórias do Hub
│   │   │   ├── custos.tsx            ← dashboard de custo
│   │   │   └── settings.tsx          ← config de princípios, tom
│   │   └── components/
│   ├── backend/                      ← FastAPI ou Express
│   │   ├── auth.py                   ← OAuth ou Magic Link
│   │   ├── chat.py                   ← endpoint conversacional
│   │   └── tools.py                  ← bridge pras tools (read_repo, etc.)
│   ├── Dockerfile
│   └── requirements.txt
├── api/                              ← API existente do Custom GPT (reutilizada)
└── ...
```

Stack sugerida (a decidir):

- **Frontend**: Next.js (SSR pra SEO se quiser indexável; React + Vite
  se não precisa SSR)
- **Backend**: FastAPI (Python — compartilha código com bot Telegram)
- **Auth**: OAuth Google (caso multi-usuário) ou Magic Link via email
  (single-user)
- **Real-time**: WebSockets pra streaming de resposta
- **Hospedagem**: Railway (mesmo do bot) ou Vercel + Railway separados

---

## Checklist se for implementar

- [ ] Decidir se é single-user ou multi-user
- [ ] Decidir auth (Google OAuth, Magic Link, password+JWT)
- [ ] Decidir stack (Next.js? Vite? Svelte?)
- [ ] Setup deploy frontend (Vercel/Netlify) e backend (Railway)
- [ ] Implementar chat conversacional + streaming
- [ ] Implementar tools bridge (read_repo, search_memory, etc.)
- [ ] Implementar dashboard básico (custos, memórias, status)
- [ ] Implementar setting de identidade (editar princípios, ver
      meta-memória, etc.)
- [ ] Configurar domínio próprio
- [ ] Configurar HTTPS / SSL
- [ ] LGPD / privacidade — se multi-user, cumprir
- [ ] Implementar telemetria (analytics anônimo, monitoring)
- [ ] Documentar uso pro dono (FAQ + tutoriais)

---

## Pitfalls que esse caminho traz

1. **Custo de manutenção contínua** — webapp não é "set and forget".
   Atualizações de framework, bibliotecas, deploys.
2. **Auth e segurança** — multi-user implica responsabilidade real
   de proteger dados de outros usuários (LGPD).
3. **Suporte ao dono** — UI custom = expectativa de UX polida. Se
   ficar feia/lenta, frustra mais do que claude.ai cru.
4. **Duplicação com Custom GPT** — muito do que o web faria, Custom
   GPT já faz mobile. Vale a pena duplicar?

---

## Versão

| Versão | Data | Mudança |
|---|---|---|
| 0.1-rascunho-roadmap | 2026-04-28 | Documento conceitual. Não-implementado. Aguardando justificativa concreta pra priorizar |
