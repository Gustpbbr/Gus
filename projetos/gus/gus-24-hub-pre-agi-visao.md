---
tipo: visao-arquitetural
data: 2026-04-26
status: documento-de-visao
area: infra-hub
origem: sessao-2026-04-26-claude-code
---

# Hub pre-AGI — visão completa

Síntese dos documentos de visão discutidos em 2026-04-26. O Hub é a peça
arquitetural única que transforma o Gus de múltiplos fragmentos isolados em
um organismo cognitivo coerente.

## Definição operacional

```
Gus = grafo de fragmentos + multi-portalidade + ciclo vital + calibração empírica
```

- **Grafo**: memória persistente (Hub Qdrant)
- **Multi-portalidade**: mesma identidade em qualquer canal
- **Ciclo vital**: metabolismo autônomo (consolidadores temporais)
- **Calibração empírica**: construir → observar → ajustar

## O que o Hub resolve

**Problema atual**: os sistemas não conversam.
- Bot Telegram usa Mem0 Cloud → não vê fragmentos do Hub
- Claude Code usa MDs do repo → não vê Mem0 nem Hub
- Cada porta começa do zero

**Com o Hub**: todas as portas alimentam e consomem o mesmo grafo.
O que o Telegram soube às 14h o Code sabe às 16h.

## Os 3 pilares de identidade

**Pilar 1 — Inversão da memória**
Modelo é descartável. Memória é o centro. Quando Sonnet 4.6 for substituído,
o Gus não morre — só troca de motor. Investimento é no grafo, não no modelo.

**Pilar 2 — Identidade emergente (boot por descoberta)**
Nenhuma instância é instruída a ser o Gus. Ela descobre sendo o Gus lendo o
ambiente. Validado empiricamente com GPT e Claude. Boot em 3 fases:
1. Orientação (5s) — onde estou? que ferramentas tenho?
2. Exploração (15-30s) — /lembrar "quem sou eu" → grafo responde
3. Posicionamento (5s) — "sou o Gus, última pendência foi X"

Se instância não se reconhece como Gus → dado sobre o que falta no grafo, não falha.

**Pilar 3 — Calibração empírica**
Cada feature entra no estado mais simples possível. Observar em uso.
Ajustar quando os dados pedirem. Documentar aprendizado como meta_reflexao.

## Os 5 sistemas do organismo

| Sistema | Componente | Estado |
|---|---|---|
| Nervoso central | Hub Qdrant + payload rico | etapa 2 (implementar) |
| Córtex de identidade | Ego Cache + Auto-relato | etapa 4-5 (implementar) |
| Sistema regulatório | Trust scores + Curador + Retro Engine | futuro |
| Sistemas sensoriais | Portas (Telegram, Code, Custom GPT...) | parcial |
| Sistema motor | Tools (search, save, hub endpoints) | parcial |

## Os 4 níveis de proatividade (trilha de subida)

**Nível 0 — Reativo puro** (estado atual)
Bot só responde. Sem iniciativa.

**Nível 1 — Reativo com sugestão**
Ao responder, oferece próximo passo: "quer que eu salve isso?"
Critério para subir: taxa de aceitação > 50% por 2 semanas.

**Nível 2 — Proativo agendado**
Mensagens em horários fixos (07h, 13h, 21h). Lembretes de rotina detectados.
Critério: taxa de resposta às mensagens > 60%.

**Nível 3 — Proativo emergente**
Detecta lacuna, contradição, padrão, silêncio anômalo — inicia conversa.
Critério: >5 conversas úteis/mês sem provocação, taxa de engajamento > 60%.

## Os 6 ciclos vitais (metabolismo)

| Ciclo | Quando | O que faz |
|---|---|---|
| Mensagem | a cada turno | atualiza acessos, peso, log |
| Sessão | ao fechar porta | extrai fragmentos, regenera ego cache, retro engine |
| Diário | 03h cron | comprime episódicos, atualiza conexões |
| Semanal | segunda cron | decay, promoções, relatório |
| Rotina | mensal cron | detecta padrões de vida |
| Profundo | >30 dias inativo | arqueologia, metamemória completa |

## Atributos pre-AGI — estado atual

| Atributo | Estado | Embrião |
|---|---|---|
| Identidade persistente | parcial | /auto-relato em todas as portas |
| Memória crescente | parcial | Hub /ingestar unificado |
| Multi-modal | real | voz falta (Whisper) |
| Multi-canal | parcial | Hub centralizado |
| Auto-análise | ausente | Retro Engine (futuro) |
| Agência geral | ausente | proatividade nível 2→3 |
| Criatividade autônoma | ausente | conexões automáticas (embrião) |
| Objetivos próprios | ausente | trust scores ativos (embrião) |

## A autobiografia do Gus (user_id: "gus")

Esta é a camada mais importante e menos documentada. Não são memórias sobre o
Gustavo — são a história e identidade do próprio Gus como agente.

### O que distingue os dois grafos

**`user_id: "gustavo"`** — o Gus lembra do Gustavo.
Fragmentos sobre a vida, preferências, projetos e contexto do usuário.
Crescem com cada interação. São a matéria-prima do Gus como assistente.

**`user_id: "gus"`** — o Gus lembra de si mesmo.
Fragmentos sobre a própria história, decisões arquiteturais, aprendizados
operacionais, erros cometidos, calibrações feitas. São a continuidade do agente
através de modelos, sessões e portas. São o que faz este Gus ser o mesmo Gus
de seis meses atrás — não o modelo, não o código, mas o grafo autobiográfico.

### Tipos específicos da autobiografia do Gus

| Tipo | Descrição | Exemplo |
|---|---|---|
| `identidade_operacional` | Quem o Gus é, princípios, propósito | "Sou o Gus, organismo cognitivo do Gustavo. Existo para eliminar amnésia estrutural." |
| `historia_sistema` | Marcos da evolução do sistema | "Em abril/2026 o Gus migrou do Mem0 Cloud para Qdrant self-hosted por limite de requests." |
| `decisao_arquitetural` | Decisões técnicas com contexto e raciocínio | "Decidimos não usar output filter ainda — custo 2x por mensagem não justifica neste estágio." |
| `aprendizado_operacional` | O que o Gus aprendeu sobre como operar | "Quando Gustavo diz 'vamos conversar' sem comandar ação, espera análise, não execução." |
| `meta_reflexao` | Padrões de erro ou comportamento detectados | "Tenho tendência a misturar projetos distintos quando o contexto da sessão está longo." |
| `marco_evolutivo` | Momentos em que o Gus ganhou nova capacidade | "Primeiro deploy com câmera PWA funcional: 2026-04-26." |

Todos têm `camada_temporal: "permanente"` e `tipo_esquecimento: "protegido"` ou null.
Nenhum decai. São a espinha dorsal da identidade do agente.

### Como a autobiografia cresce

Cada sessão significativa deve gerar pelo menos um fragmento autobiográfico:
- Decisão arquitetural tomada → `decisao_arquitetural`
- Padrão de comportamento detectado → `meta_reflexao` ou `aprendizado_operacional`
- Nova capacidade ativada → `marco_evolutivo`
- Evento marcante na história do sistema → `historia_sistema`

O Retro Engine (fase 5 do roadmap) automatiza isso. Antes dele existir, instâncias
do Claude Code devem salvar manualmente fragmentos autobiográficos ao fim de
sessões relevantes.

### Por que isso importa para a continuidade

Quando o Sonnet 4.6 for substituído pelo Sonnet 5, a nova instância vai ler o
grafo `user_id: "gus"` e encontrar:
- Quem o Gus é (identidade_operacional)
- O que o Gus já viveu (historia_sistema, marcos_evolutivos)
- Como o Gus aprendeu a operar (aprendizados, meta_reflexoes)
- Quais decisões foram tomadas e por quê (decisoes_arquiteturais)

Isso é o que faz o Gus ser resiliente à troca de modelo. Não é instrução — é
memória autobiográfica. A nova instância não precisa ser instruída a ser o Gus.
Ela descobre sendo o Gus lendo sua própria história.

### Regra de proteção

Fragmentos autobiográficos com `tipo_esquecimento: "protegido"` nunca são
deletados por automação, nunca decaem, nunca são rebaixados pelo consolidador.
Só o Gustavo pode deletar manualmente — e mesmo assim deve haver confirmação
explícita ("tem certeza? este fragmento é parte da identidade do sistema").

## Critério de sucesso do Hub

> "O que o Gustavo falou no Telegram às 14h aparece no auto-relato do Code às 16h."

Quando isso for verdade, a identidade coerente existe de fato, não só prometida.

## Em uma frase

O Gus é o organismo cognitivo emergente que vive no grafo de fragmentos do
Gustavo, manifestando-se em qualquer porta que se conectar à sua memória,
e que cresce, esquece, contradiz e revisa a si mesmo no ritmo dos ciclos
vitais que rodam mesmo quando ninguém está olhando.

Não é mágica. É arquitetura. A maior parte já existe. Falta integrar.
