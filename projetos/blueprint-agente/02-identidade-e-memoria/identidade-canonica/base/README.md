---
tipo: blueprint-spec
componente: identidade-canonica-base
opcional: false
estimativa-implementacao: ~1h (decisão) + ~30min (escrita)
---

# Identidade canônica — Base

O **arquivo central** que define quem o agente é. Lido na inicialização
de cada porta. Tipicamente 1-2 páginas em prosa direta.

## O que é

Documento `identity.md` que responde:

1. **Nome** do agente
2. **Propósito** — pra que serve, em 1 frase
3. **Tom de comunicação** — formal/informal, idioma, padrões de fala
4. **Quem é o dono** — informação mínima sobre a pessoa que usa o agente
5. **Relação com o dono** — agente é assistente neutro, parceiro
   crítico, espelho reflexivo, etc.
6. **Limites** — o que o agente NÃO faz (ex: terapia profunda, decisão
   médica final, decisão financeira por conta própria)

## Por que importa

A identidade é **lida em toda inicialização** de toda porta. Sem ela:

- Bot Telegram responde com voz genérica (parece outro chatbot)
- Claude Chat não sabe assumir personalidade quando você ativa o
  bootstrap
- Custom GPT alucina personalidade
- Curador da memória não sabe filtrar o que é fato sobre o dono vs
  reflexão genérica

Identidade fraca = agente sem coerência entre canais.

## Decisões a tomar pelo dono do agente

- [ ] **`{{NOME_AGENTE}}`** — nome curto, único, fácil de chamar.
      Evite ambiguidade com produtos existentes.
- [ ] **`{{PROPOSITO_UMA_FRASE}}`** — máx 1 frase. Pode ser ampla
      ("assistente pessoal de IA com memória persistente") ou
      especializada ("assistente de pesquisa em saúde da família").
- [ ] **`{{TOM}}`** — formal? informal? português brasileiro? bilíngue?
      verboso? direto? técnico? acessível?
- [ ] **`{{DONO_IDENTIDADE}}`** — nome (ou apelido), profissão, papel
      principal. NÃO inclua dados sensíveis (CPF, endereço, etc.).
- [ ] **`{{RELACAO_DONO_AGENTE}}`** — assistente que executa? parceiro
      que questiona? espelho reflexivo? scribe que registra?
- [ ] **`{{LIMITES_EXPLICITOS}}`** — 3-5 áreas onde o agente recusa ou
      pede ajuda humana (ex: decisão médica, jurídica, financeira de
      alto valor).

## Como implementar (passo a passo)

1. **Faça uma sessão de descoberta** com a IA implementadora. Ela
   conversa contigo por 30-60min entendendo:
   - Como você fala e prefere ser tratado
   - Que tipo de ajuda mais procura
   - O que te irrita em outros assistentes (suavização excessiva?
     formalidade demais? uso de emoji?)
   - Áreas profissionais e pessoais que vão aparecer

2. **IA esboça** o `identity.md` com base nessa conversa,
   preenchendo placeholders. Você revisa.

3. **Iteração**: ler em voz alta. Soa como agente que faria sentido?
   Quais frases parecem genéricas e poderiam ser substituídas?

4. **Trim**: tirar tudo que é genérico ou óbvio. Identity tem que ser
   afiada — 1-2 páginas no máximo. Não é manual de uso, é cartão de
   identidade.

5. **Commitar**: arquivo final em `<repo>/agente/identity.md` (ou path
   equivalente — `agente/` é convenção sugerida).

## Estrutura de arquivos esperada

```
agente/                          ← pasta do código + identidade
├── identity.md                  ← este componente
├── principios.md                ← componente irmão (próxima pasta)
├── meta-memoria.md              ← componente irmão
├── bootstrap.md                 ← componente irmão
└── system_prompt.md             ← personalidade específica de uma porta
                                   (a porta primária, geralmente Telegram)
```

## Templates inclusos

- **`template.md`** — esqueleto pra você preencher. Tem placeholders
  marcados com `{{}}` e comentários `<!-- HINT: ... -->` que você
  apaga ao preencher.

## Critérios de teste

Identidade está pronta se:

1. **Dois leitores diferentes** (você + a IA implementadora) leem
   `identity.md` em voz alta e descrevem o agente da mesma forma
2. **Bot teste**: cole `identity.md` como system prompt num chat
   isolado (Anthropic Workbench, OpenAI Playground), pergunte 3 coisas
   triviais. Respostas têm o tom correto?
3. **Curador teste**: peça pra IA implementadora extrair "3 fatos sobre
   o agente" lendo só o `identity.md`. Os fatos batem com o que você
   queria expressar?

Se 1 dos 3 falha, identidade ainda não está calibrada. Volta pro passo
3 (iteração).

## Pitfalls comuns

### Pitfall 1 — Identidade genérica

Sintoma: identidade soa como qualquer assistente IA. Frases tipo "Sou
um assistente útil que ajuda em tarefas diversas".

Causa: pulou a sessão de descoberta. Tentou escrever identidade no
abstrato.

Mitigação: refazer a sessão de descoberta com mais profundidade. Pegar
3-5 exemplos concretos de "uma conversa que você gostaria de ter com
o agente" e basear a identidade neles.

### Pitfall 2 — Identidade longa demais

Sintoma: `identity.md` tem 5+ páginas. Inclui regras de uso de tools,
personalidade detalhada, exemplos verbosos.

Causa: confundiu identidade com manual operacional.

Mitigação: separar. Identidade = 1-2 páginas (nome, propósito, tom,
limites). Tudo operacional vai pro `system_prompt.md` da porta
específica.

### Pitfall 3 — Vazar dados sensíveis

Sintoma: `identity.md` inclui CPF, endereço, número de telefone,
documentos do dono.

Causa: confundiu identidade do **agente** com dossiê do **dono**.

Mitigação: identidade fala sobre o **agente** (quem ele é, como age).
Dados do dono ficam no vault em `pessoal/` ou `sensivel/`, lidos sob
demanda via tools. Identity pode mencionar primeiro nome do dono,
profissão genérica, e nada mais.

### Pitfall 4 — Tom inconsistente entre portas

Sintoma: bot Telegram fala informal mas Claude Chat fica formal.
Mesma identidade, comportamentos diferentes.

Causa: cada porta carrega o `system_prompt.md` específico, e o tom foi
definido lá em vez de na identidade base.

Mitigação: tom canônico fica em `identity.md`. `system_prompt.md` por
porta apenas adapta canal (ex: "Telegram tem limite de caracteres,
quebre mensagens longas") sem mudar tom.

## Dependências

- `principios.md` — princípios são componente irmão, definidos junto
  ou logo depois
- Vault GitHub configurado (Etapa 3 do roadmap) — pra ter onde commitar

## Referências externas

- Conceito de "voice and tone" em design de produto:
  https://www.nngroup.com/articles/voice-and-tone/
- Anthropic — boas práticas de prompt design:
  https://docs.anthropic.com/claude/docs/prompt-engineering

## Próximo componente

Após identidade base pronta, implementar **`principios/`** (componente
irmão). Princípios são instâncias específicas de "como o agente deve
agir" e complementam a identidade.
