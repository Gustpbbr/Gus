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

| Valor | Porta |
|---|---|
| `telegram` | Bot Telegram |
| `claude-code` | Esta porta (Claude Code) |
| `custom-gpt` | Custom GPT |
| `curador` | Extraído automaticamente pelo Curador Haiku |
| `manual` | Inserido manualmente |

## Áreas (campo `area`)

`gus` · `saude` · `financeiro` · `projetos` · `pessoal` · `dimagem` · `pesquisa` · `receitas` · `esportes`

## Regras de escrita

1. `conteudo` deve ser auto-suficiente — sem "ele", "isso", "aquele projeto" sem nomear
2. `tipo_esquecimento=protegido` nunca é sobrescrito por automação
3. Fragmentos com `estado=esquecido` não aparecem em buscas (filtro padrão)
4. `user_id` é sempre `gustavo` ou `gus` (brain operacional do próprio Gus)
