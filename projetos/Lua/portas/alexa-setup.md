---
tipo: setup-porta
porta: alexa
agente: Lua
estimativa: ~6-10h (não-implementado em outros agentes)
status: roadmap-futuro
---

# Setup — Porta Alexa Skill da Lua

> **Atenção:** porta **AINDA NÃO TEM IMPLEMENTAÇÃO DE REFERÊNCIA**. O
> agente irmão tem doc conceitual mas nenhuma implementação real. Este
> documento é roadmap.

---

## O que essa porta seria

Uma **Alexa Skill custom** (publicada na Amazon Developer Console) que
permite o dono falar com a Lua usando dispositivos Echo (Echo Dot,
Show, etc.). Casos de uso:

- "Alexa, abrir Lua. O que falamos ontem?"
- "Alexa, perguntar à Lua: salva o lembrete de comprar pão"
- "Alexa, pedir à Lua: quais minhas pendências?"

---

## Por que essa porta poderia existir

- **Voz em casa sem celular** — dono em pé na cozinha, mãos sujas,
  pode falar com Lua via Echo
- **Captura rápida** — falar é mais rápido que digitar pra ideias
  curtas
- **Conexão contínua** — Echo está sempre escutando, ativação por
  wake word "Alexa"
- **Acessibilidade** — útil pra quem não pode/quer usar tela

---

## Por que NÃO é prioritário no V1

- **Custom GPT mobile já cobre voz** — em qualquer lugar (não só em
  casa), com voz nativa do app ChatGPT, sem custo de implementação
- **Alexa Skill custom é trabalho grande** — Lambda function + intents
  + speech model + publicação na store + manutenção
- **Limitações da Alexa Skill** — câmera não acessível, ações de fora
  da skill bloqueadas, latência alta de resposta
- **Sem ROI claro** — se o dono não usa Echo intensivamente, não vale

---

## Quando reconsiderar

Implementar Alexa Skill faz sentido se:

1. **Dono tem Echo Dot ou Show e usa diariamente**
2. **Custom GPT mobile inadequado** — bateria fraca, contexto sem
   celular na mão
3. **Captura de pensamento em casa** vira fricção sem voz hands-free
4. **Família compartilha** — outros membros da casa usam Lua via voz
   (cuidado com privacidade compartilhada)

---

## Decisões críticas se implementar

### 1. Skill custom OU Skill com Hosted Lambda

- **Skill custom** (Lambda externa, ex: AWS Lambda própria ou
  endpoint Railway) — mais flexível mas exige conta AWS
- **Hosted Skill** (Amazon hospeda) — mais simples mas limitado em
  bibliotecas

Recomendação: **Lambda externa via Railway** — Lua já tá no Railway,
só adicionar handler.

### 2. Voz pura ou voz + tela (Echo Show)

- **Voz pura (Echo Dot)** — só áudio, sem tela
- **Voz + tela (Echo Show)** — pode mostrar imagem, gráfico, lista

V1 deveria ser **só voz pura** (cobre todos Echo). V2 adicionar suporte
Echo Show.

### 3. Persona Lua adaptada vs idêntica

Voz da Lua na Alexa pode ser:

- **Voz Polly default** (escolhida pelo dono na Skill config)
- **Voz custom** (mais caro, exige clones de voz com licença)

Recomendação V1: voz Polly default em PT-BR, escolher uma neutra.

### 4. Wake word

Alexa Skill custom **não pode mudar wake word** (continua "Alexa,
abrir Lua"). Pra ter "Lua" como wake word direto, precisa Termux + S8
ou hardware custom — fora do escopo Alexa Skill.

---

## Esboço de arquitetura (roadmap)

```
┌────────────────────┐      ┌──────────────────┐      ┌─────────────┐
│ Echo Dot/Show      │ ──→  │ AWS Lambda       │ ──→  │ Lua API     │
│ "Alexa, abrir Lua" │      │ Skill handler    │      │ (FastAPI    │
│                    │      │ + intents        │      │  Railway)   │
└────────────────────┘      └──────────────────┘      └─────────────┘
                                                              │
                                                       ┌──────▼──────┐
                                                       │ Lua brain   │
                                                       │ + vault     │
                                                       └─────────────┘
```

Skill recebe input voz, transcreve via Alexa, Lambda formata pra Lua
API, Lua API responde texto, Lambda passa pra Polly TTS, voz volta
pro Echo.

---

## Custos esperados (estimativa)

- **AWS Lambda (Free tier 1M req/mês)**: provavelmente US$0
- **Polly TTS**: US$4/1M caracteres pro padrão (Lua respostas curtas
  são ~500 chars cada → 2000 respostas ≈ US$0.004)
- **Lua API extra**: depende do uso. Conversas Alexa tendem a ser
  curtas (10-30 turnos/dia max), custo Anthropic ~US$2-5/mês
- **Total**: ~US$5/mês adicional sobre infra existente

Plus US$80-200 inicial pelo dispositivo Echo (uma vez).

---

## Checklist se implementar

- [ ] Decidir se vai V1 só voz ou também tela (Echo Show)
- [ ] Conta Amazon Developer (gratuita)
- [ ] Criar Skill custom (developer.amazon.com)
- [ ] Definir intents (`SalvarMemoriaIntent`, `BuscarMemoriaIntent`,
      `PerguntarLuaIntent`, etc.)
- [ ] Implementar Lambda handler (Python ou Node.js)
- [ ] Configurar endpoint pra Lua API
- [ ] Definir voz Polly (pt-BR-neural)
- [ ] Configurar conversation flow (1-shot vs multi-turn)
- [ ] Testar em simulador da Amazon
- [ ] Beta com dispositivo real
- [ ] Publicar (ou deixar em "Development" se for pessoal)
- [ ] Documentar pro dono usar

---

## Pitfalls comuns

### 1. Latência alta

Alexa → Lambda → Lua API → Anthropic → ... Total fica ~5-10s.
Audível, dono pode ficar impaciente.

Mitigação: usar Haiku 4.5 (rápido) por default na Alexa, só Sonnet
quando dono pedir explicitamente.

### 2. Voz Polly soa robótica

Vozes neurais (`pt-BR-Camila-neural`, `pt-BR-Vitoria-neural`) são
melhores que vozes padrão. Custar mais, mas vale a pena.

### 3. Privacidade compartilhada

Se Echo está na sala, todos da casa podem invocar a Lua. Cuidado com
o que Lua revela se outro membro pergunta:

- "Como tá meu projeto X?" → Lua não deveria responder pra qualquer
  voz, só pra dono
- Mitigação: Alexa tem Voice Profile (reconhece voz do dono) — usar
  isso pra autenticar
- Alternativa: Lua só responde sobre tópicos não-sensíveis na Alexa,
  e só na voz reconhecida do dono pra tópicos sensíveis

### 4. Echo não escuta direito o "Lua" no nome da Skill

Sotaque, ruído de fundo. Skill name **invocation name** pode ser
ajustado em "Lua" ou "minha Lua" ou "Lua Pessoal".

---

## Versão

| Versão | Data | Mudança |
|---|---|---|
| 0.1-rascunho-roadmap | 2026-04-28 | Documento conceitual. Implementação adiada — depende de Custom GPT estar funcional primeiro |
