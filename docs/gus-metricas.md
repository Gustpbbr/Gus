# GUS FRAMEWORK — Sistema de Métricas

**Tipo:** estado-do-projeto + manual  
**Data:** 2026-04-09  
**Status:** implementar junto com o Gus V1.0  
**Conexão:** gus-briefing-opus.md, gus-lancamento-github.md

---

## Princípio

Métricas servem a dois propósitos:
1. **Para você** — entender se o Gus está funcionando e melhorando sua vida
2. **Para o produto** — contar uma história convincente com números reais

Toda métrica deve ser coletada automaticamente — você não anota nada manualmente.

---

## GRUPO 1 — Economia de recursos

*As mais importantes para o lançamento público*

| Métrica | O que mede | Como coletar |
|---|---|---|
| Tokens por sessão | Consumo médio por conversa | API Anthropic retorna token count em cada resposta |
| Custo diário (USD) | Gasto real na API | Somar custo de todas as chamadas do dia |
| Custo mensal total | Gasto mensal | Acumular custo diário |
| % uso por modelo | Quanto Opus vs Sonnet vs Haiku | Contar chamadas por modelo no log |
| Redução vs baseline | Economia real | Comparar com média antes do Gus |

**Baseline — registrar ANTES de ligar o Gus:**
- Abrir 3 sessões antigas e anotar token count de cada uma
- Calcular média — esse é o "antes"

---

## GRUPO 2 — Qualidade das sessões

*As mais convincentes para demonstrar valor real*

| Métrica | O que mede | Como coletar |
|---|---|---|
| Sessões sem reexplicação (%) | Contexto carregado automaticamente | Flag no início de cada sessão: buscou MemPalace? |
| Drawers recuperados por sessão | Quanto contexto o Gus trouxe | mempalace_search retorna count |
| Entradas Mem0 carregadas | Identidade aplicada | Mem0 retorna memories usadas |
| Tempo até resposta útil | Velocidade de contexto | Timestamp primeira mensagem vs primeira resposta com contexto |

---

## GRUPO 3 — Uso do sistema

*Para entender padrões e otimizar o Gus ao longo do tempo*

| Métrica | O que mede | Como coletar |
|---|---|---|
| Mensagens por dia | Volume de uso | Contar no log diário |
| Projetos consultados/semana | Abrangência de uso | Registrar qual wing foi consultado |
| Comandos mais usados | O que mais agrega valor | Contar por tipo: busca, MGE, CEX, criação |
| Horários de pico | Quando você mais usa | Timestamp de cada mensagem |

---

## GRUPO 4 — Proatividade do Gus

*Para calibrar as mensagens proativas ao longo do tempo*

| Métrica | O que mede | Como coletar |
|---|---|---|
| Mensagens proativas/semana | Volume de iniciativa do Gus | Contar no scheduler log |
| Taxa de resposta | Você respondeu ou ignorou | Flag na mensagem seguinte |
| Tipos mais respondidos | Quais alertas são úteis | Categoria da mensagem proativa |
| Tipos mais ignorados | Quais alertas são inúteis | Categoria das sem resposta |

---

## GRUPO 5 — Memória

*Para mostrar crescimento e saúde do sistema*

| Métrica | O que mede | Como coletar |
|---|---|---|
| Arquivos indexados total | Tamanho do MemPalace | mempalace status |
| Drawers total | Fragmentos de memória | mempalace status |
| Crescimento semanal | MemPalace evoluindo | Diff do status semanal |
| Entradas no Mem0 | Identidade crescendo | mem0.list() count |
| Buscas com resultado útil | Qualidade do índice | Flag manual ou por feedback |

---

## GRUPO 6 — Produto (para o lançamento)

*Os números que vão no README*

| Métrica | Valor alvo em 30 dias | Como apresentar |
|---|---|---|
| Dias de uso contínuo | 30 | "30 dias de uso real" |
| Redução de tokens | >80% | "94% menos tokens por sessão" |
| Arquivos acessíveis | 1494 | "1494 arquivos em linguagem natural" |
| Sessões sem reexplicação | >90% | "Zero reexplicação de contexto" |
| Projetos gerenciados | todos ativos | "X projetos simultâneos" |
| Custo mensal estimado | a medir | "De R$X para R$Y por mês" |

---

## Como implementar — o log do Gus

Adicionar ao `gus_core.py` um sistema de log estruturado:

```python
# A cada mensagem recebida e respondida, salvar:
{
  "timestamp": "2026-04-09T21:00:00",
  "tipo": "entrada_usuario" | "proativa_gus",
  "modelo_usado": "sonnet" | "opus" | "haiku",
  "tokens_input": 1250,
  "tokens_output": 340,
  "custo_usd": 0.0023,
  "mempalace_buscou": true,
  "mempalace_drawers": 4,
  "mem0_carregou": true,
  "mem0_entries": 12,
  "projeto_consultado": "phronesis-bench",
  "comando_tipo": "busca" | "mge" | "cex" | "criacao" | "conversa"
}
```

Salvar em `logs/gus_metrics.jsonl` — uma linha por interação.

---

## Dashboard de métricas

Depois de 2 semanas de logs, o Claude Code gera um dashboard HTML automaticamente a partir do `gus_metrics.jsonl`.

O dashboard mostraria:
- Gráfico de tokens por dia (linha)
- Custo acumulado (linha)
- Distribuição de modelos usados (pizza)
- Projetos mais consultados (barra)
- Horários de uso (heatmap)
- Taxa de resposta às mensagens proativas (barra)

Esse dashboard vira evidência concreta para o README e para conversas de parceria.

---

## Métricas do README — como apresentar

Após 30 dias, o README teria uma seção assim:

```
## Resultados reais — 30 dias de uso

| Antes | Depois |
|---|---|
| ~1.000.000 tokens/sessão | ~12.000 tokens/sessão |
| Reexplicação em 100% das sessões | Reexplicação em 0% das sessões |
| 3 modelos Opus simultâneos | Roteamento automático Haiku/Sonnet/Opus |
| Custo: ~$150/mês | Custo: ~$18/mês |
| 0 projetos com contexto persistente | 1494 arquivos acessíveis em linguagem natural |

Dados coletados automaticamente. Logs disponíveis em /examples/logs-sample.jsonl
```

Números reais, verificáveis, impossíveis de refutar.

---

## Pré-requisitos

- [ ] Registrar baseline ANTES de ligar o Gus (token count de 3 sessões antigas)
- [ ] Sistema de log implementado desde o primeiro dia
- [ ] Revisão semanal das métricas (5 minutos)
- [ ] Após 30 dias: gerar dashboard e extrair números para README

---

## Nota

A métrica mais poderosa não é técnica — é humana: "abri uma sessão nova e o Gus já sabia tudo sobre meu projeto." Isso não aparece em nenhum número, mas é o que vai fazer alguém instalar.

Os números provam que funciona. A história faz alguém querer.
