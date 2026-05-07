---
tipo: referencia-tecnica
data: 2026-04-26
status: definido
area: infra-memoria
usado-por: gus-20-etapa2-hub-qdrant.md, gus-21-etapa3-curador.md
---

# Schema de indexação — payload do Hub Qdrant

Documento de referência. Todo fragmento salvo no Hub carrega este payload.
Qualquer instância que escrever ou ler do Hub deve seguir este schema.

## Payload completo de um fragmento

```json
{
  "conteudo": "texto do fragmento — auto-suficiente, sem referência externa",
  "tipo": "identidade_operacional",
  "estado": "ativo",
  "camada_temporal": "permanente",
  "tipo_esquecimento": null,
  "peso": 0.5,
  "confirmacoes": 0,
  "confianca": 0.8,
  "via": "telegram",
  "area": "gus",
  "projeto": "",
  "user_id": "gustavo",
  "criado_em": "2026-04-26T17:00:00-03:00",
  "ultimo_acesso": "2026-04-26T17:00:00-03:00",
  "acessos": 0
}
```

## Tipos de fragmento (campo `tipo`)

| Tipo | Descrição | Meia-vida |
|---|---|---|
| `identidade_operacional` | Quem o Gus é, como opera, princípios | permanente |
| `biografico` | Fatos sobre o Gustavo: família, carreira, história | permanente |
| `emocional` | Estados emocionais recorrentes, padrões afetivos | alta |
| `decisao` | Decisões tomadas com contexto e raciocínio | alta |
| `procedural` | Como fazer algo: protocolos, rotinas, preferências | alta |
| `rotina` | Padrões detectados: horários, hábitos, recorrências | média |
| `meta_reflexao` | Auto-análise do Gus: padrões de erro, calibrações | alta |
| `conexao_emergente` | Relações descobertas entre conceitos ou projetos | média |
| `episodico` | Evento específico com data, não generalizável | baixa |
| `cronologico` | Narrativa comprimida de período (dia, semana) | baixa |
| `fato` | Informação factual sobre o mundo relevante ao Gustavo | média |
| `preferencia` | O que Gustavo gosta, prefere, evita | alta |
| `lacuna` | O que o Gus não sabe mas deveria saber | média |
| `projeto` | Estado atual de um projeto específico | média |

## Estados (campo `estado`)

| Estado | Significado |
|---|---|
| `ativo` | Fragmento novo, ainda sendo observado |
| `estavel` | Confirmado por uso ou tempo (≥30 dias sem contradição) |
| `historico` | Verdadeiro no passado, pode não ser mais |
| `esquecido` | Irrelevante, não retornado em buscas |

Promoção `ativo → estavel`: automática após 30 dias sem contradição e ≥2 acessos.

## Camadas temporais (campo `camada_temporal`)

| Camada | Janela | Exemplo |
|---|---|---|
| `momento` | Minutos/hora | "Gustavo está com pressa agora" |
| `sessao` | Uma interação | "Hoje falamos sobre Phronesis" |
| `semana` | 7 dias | "Esta semana foco em infraestrutura" |
| `rotina` | Recorrente | "Toda segunda trabalha no Phronesis" |
| `permanente` | Sem expiração | "Gustavo é anestesiologista" |

## Tipos de esquecimento (campo `tipo_esquecimento`)

| Tipo | Quando usar |
|---|---|
| `null` | Padrão — fragmento ativo |
| `funcional` | Informação desatualizada, substituída por outra |
| `deliberado` | Gustavo pediu explicitamente para esquecer |
| `superado` | Decisão ou situação que não se aplica mais |
| `protegido` | NUNCA esquecer — núcleo duro de identidade |

## Campos de lifecycle

| Campo | Tipo | Descrição |
|---|---|---|
| `peso` | float 0.0–1.0 | Relevância acumulada. Sobe com acessos, desce com tempo |
| `confirmacoes` | int | Quantas vezes o fragmento foi validado/confirmado |
| `confianca` | float 0.0–1.0 | Certeza do curador na extração |
| `acessos` | int | Quantas vezes foi retornado em busca |

## Tags de origem (campo `via`)

Lista canônica vive em `hub/vocabularios.py:VIAS_CANONICAS` — fonte única.
Atualizada em 02/05/2026 (item 1.1 do plano de saneamento).

### Portas humanas (interação direta com Gustavo)

| Valor | Porta |
|---|---|
| `telegram-claude` | Bot Telegram em modo Claude (Anthropic) |
| `telegram-gpt` | Bot Telegram em modo GPT (OpenAI) |
| `claude-code` | Claude Code (esta porta) |
| `claude-chat` | Claude Chat web (claude.ai) |
| `custom-gpt` | Custom GPT (mobile/web ChatGPT) |
| `alexa` | Alexa Echo (futuro) |
| `carro-audio` | Voz no carro (futuro) |

### Casos especiais

| Valor | Significado |
|---|---|
| `manual` | Entrada manual via Obsidian/CLI |
| `curador` | Quando o próprio curador atribui (raro) |
| `api` | Cliente API genérico (default `IngestarReq`) |
| `legacy-mem0-saas` | Importação histórica do Mem0 SaaS aposentado (Fase 5.6) |

### Prefixos aceitos (extensibilidade controlada)

- `workflow-<nome>` — workflows automáticos (briefing, retrospectiva, etc.)
- `emergente:<nome>` — vias novas em validação, antes de promoção

## Áreas (campo `area`)

`gus` · `saude` · `financeiro` · `projetos` · `pessoal` · `dimagem` · `pesquisa` · `receitas` · `esportes`

## Os dois brains (campo `user_id`)

O Hub tem dois contextos de memória completamente distintos:

| `user_id` | O que armazena | Quem escreve |
|---|---|---|
| `gustavo` | Tudo sobre o Gustavo — fatos, preferências, projetos, saúde, decisões de vida | Curador (de interações), portas |
| `gus` | Autobiografia do próprio Gus como agente — sua história, seus aprendizados, sua evolução | Retro Engine, instâncias do Gus |

São grafos independentes. Uma busca com `user_id=gustavo` nunca retorna fragmentos do `gus` e vice-versa. Ver `gus-24` para detalhamento da camada autobiográfica do Gus.

## Schema dinâmico — tipos e áreas emergentes

As listas de `tipo` e `area` acima são **pontos de partida**, não listas fechadas. O Gus e o Gustavo vão evoluir e novos domínios vão emergir naturalmente.

### Regra para tipo desconhecido

Quando o Curador encontrar uma informação que não se encaixa em nenhum tipo existente, deve salvar com prefixo `emergente:`:

```json
{ "tipo": "emergente:ritual-diario", "conteudo": "Gustavo faz meditação às 6h antes de qualquer outra atividade" }
```

Isso preserva a informação sem forçar encaixe incorreto.

### Ciclo de promoção de tipos emergentes

1. Curador salva com `tipo: "emergente:nome"`
2. Quando o mesmo `emergente:nome` aparecer ≥3 vezes em fragmentos distintos, sinaliza candidato a canônico
3. Revisão manual (Gustavo ou Claude Code): promover ao schema oficial ou descartar
4. Se promovido: atualizar este documento e reindexar fragmentos existentes

### Regra para área desconhecida

Mesma lógica: `area: "emergente:nome-da-area"` até promoção.

Áreas que podem surgir naturalmente: `culinaria`, `viagens`, `música`, `familia`, `filosofia`, `meditacao`, qualquer projeto novo que ganhe volume suficiente.

### O que NÃO deve ser criado como tipo emergente

- Variações de tipos existentes com nome diferente (`decisao_tecnica` → usar `decisao`)
- Tipos muito específicos que nunca vão se repetir (`pergunta-de-sabado` → usar `episodico`)
- Tipos que são só subtipos de área (`saude-joelho` → usar `tipo: fato, area: saude`)

## Regras de escrita

1. `conteudo` deve ser auto-suficiente — sem "ele", "isso", "aquele projeto" sem nomear
2. `tipo_esquecimento=protegido` nunca é sobrescrito por automação
3. Fragmentos com `estado=esquecido` não aparecem em buscas (filtro padrão)
4. `user_id` é sempre `gustavo` ou `gus` — nunca misturar os dois grafos
5. Tipos `emergente:*` são temporários — toda instância que os encontrar sabe que precisam de revisão
6. Ao criar fragmento com tipo emergente, adicionar campo `emergente_motivo` explicando por que não encaixou nos tipos existentes
