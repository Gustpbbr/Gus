---
tipo: status
status: rascunho-em-standby
desde: 2026-04-28
---

# ⚠️ Rascunho em standby

Esta pasta tem a **instância inicial da Lua** — primeira tentativa de
fazer um agente novo (não o Gus) com identidade própria, memória
persistente e múltiplas portas.

## Estado atual (2026-04-28)

15 arquivos criados em rascunho 0.1:

```
projetos/Lua/
├── README.md (mapa)
├── decisoes-pendentes.md (5 blocos pra entrevista)
├── identidade/ (4 arquivos: identity, principios, bootstrap, meta-memoria)
├── system-prompts/ (telegram + claude-chat-instructions)
├── portas/ (telegram, claude-chat, custom-gpt, web, alexa)
└── memoria/ (setup-qdrant, schema-fragmentos)
```

**Identidade preenchida em rascunho genérico**, baseada em boas práticas
comuns. Não passou pela calibração final do dono.

## Por que está em standby

3 razões apareceram em conversa do dono (28/04/2026):

1. **Trocar agente não resolve** — Lua usa mesma stack do Gus
   (Anthropic Claude + Qdrant + Telegram + GitHub + Railway). Se
   problemas estruturais aparecerem (tipo Dimagem fragmentado), vão
   aparecer aqui também — não é questão de modelo, é arquitetura de
   decisão.

2. **Identidade emergente vs identidade definida** — entrevista de
   descoberta (30 perguntas) cria agente com a cara do dono, não
   agente que se descobre com uso. Pra Lua nascer **dela mesma**, ela
   precisa de identidade mínima inicial e cristalizar com tempo —
   arquitetura diferente da do blueprint padrão.

3. **Lua não é prioridade imediata** — Gus tem coisas mais úteis pra
   evoluir (ex: foco do TioGu em diagnóstico/comunicação rápida e
   tirar fluxos estruturados que falham 3 em 5).

## O que ficou útil aqui

Mesmo em standby, o conteúdo serve como **rascunho de referência**:

- **`portas/*.md`** — passo-a-passo de setup pra cada canal (Telegram,
  Claude Chat, Custom GPT, web, Alexa). Útil pro dia em que alguém
  (Gustavo ou outro) for implementar um agente novo seguindo essa
  estrutura.
- **`memoria/setup-qdrant.md`** — receita pra criar coleção Qdrant
  separada com índices canônicos.
- **`memoria/schema-fragmentos.md`** — schema gus-18 documentado de
  forma genérica (pode ser reaproveitado em qualquer agente novo).
- **`decisoes-pendentes.md`** — checklist de 5 blocos pra entrevista
  de descoberta (com nota de que precisa ser refeita em formato de
  identidade emergente, não placeholder fill).

## Quando reativar

Reativar Lua faz sentido se:

1. **Caso de uso concreto aparece** — alguém (Cleir? Outro?) precisa
   de agente novo, e os princípios da entrevista emergente estão
   maduros
2. **Decisão arquitetural sobre identidade emergente** — desenhar
   sistema onde o agente cristaliza tom/princípios via uso (não
   resposta de questionário do dono)
3. **TioGu reorientado** — quando TioGu virar "diagnóstico/comunicação
   rápida", Lua pode absorver fluxos estruturados que TioGu deixou.
   Mas isso depende do dono decidir isso intencionalmente.

## Status técnico

- Pasta **NÃO** sincroniza com Drive (default já cobre — não está em
  uso operacional)
- Conteúdo **preservado** no histórico do git (PR #18)
- **Pode ser deletada** sem impacto operacional — nenhum código vivo
  depende dessa pasta. Mantida porque o conteúdo serve como referência
  futura quando o tema voltar.

## Última atualização significativa

| Data | O que aconteceu |
|---|---|
| 2026-04-28 | Criação dos 15 arquivos em rascunho 0.1 (PR #18) |
| 2026-04-28 | Decisão de standby + adição deste arquivo de status |
