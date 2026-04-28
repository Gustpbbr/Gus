---
tipo: schema-canonico
agente: Lua
versao: 0.1-rascunho (espelhado de gus-18)
atualizado: 2026-04-28
---

# Schema dos fragmentos atômicos da Lua

Cada **fragmento** salvo no Hub Qdrant `lua_hub` segue este schema.
Aplica-se a brains do dono e da Lua (mesma estrutura, separação por
`user_id`).

> **Origem do schema:** baseado em `gus-18-schema-indexacao.md` do
> agente irmão. A Lua começa com o mesmo schema porque cobre os casos
> bem; refinamentos podem ser feitos quando algum campo provar
> insuficiente em uso real.

---

## Campos obrigatórios

### `conteudo` — string

Texto do fragmento, **auto-suficiente**. Quem lê esse texto sozinho
(sem contexto) deve entender. Sem "ele", "isso", "aquele projeto" sem
nomear.

Exemplo bom:
> "Gustavo prefere crítica direta sem suavizar problemas reais"

Exemplo ruim:
> "Ele prefere assim mesmo"

### `tipo` — string (enum)

Categoria semântica do fragmento. 14 valores possíveis:

| Tipo | Pra que |
|---|---|
| `identidade_operacional` | Padrões sobre como a Lua deve agir (princípios, preferências do dono que afetam comportamento da Lua) |
| `biografico` | Fato biográfico do dono (nome, profissão, condições de saúde estáveis) |
| `emocional` | Estado emocional ou nuance afetiva captada |
| `decisao` | Decisão tomada — contexto + opções consideradas + escolhida |
| `procedural` | Como fazer algo (workflow, receita, processo) |
| `rotina` | Rotina recorrente (horários, hábitos) |
| `meta_reflexao` | Reflexão sobre si, sobre o sistema, sobre o relacionamento agente-dono |
| `conexao_emergente` | Insight sobre conexão entre coisas que aparentemente eram isoladas |
| `episodico` | Evento específico em momento (não recorrente) |
| `cronologico` | Marco temporal (datas importantes, deadlines) |
| `fato` | Fato sobre o mundo (não-pessoal) que a Lua precisa lembrar |
| `preferencia` | Preferência declarada do dono (música, comida, tom, etc.) |
| `lacuna` | Coisa que dono mencionou que falta saber/fazer |
| `projeto` | Status, marco, decisão sobre projeto em andamento |

Default: `episodico` (se classificação não conseguir decidir).

### `estado` — string (enum)

Ciclo de vida do fragmento:

- `ativo` — em uso, busca semântica retorna
- `historico` — preservado, mas não retorna em busca padrão (precisa
  flag explícita)
- `arquivado` — fora do scope cotidiano
- `quarentena` — sob revisão (suspeita de erro, contradição, lixo)

Default: `ativo`.

### `camada_temporal` — string (enum)

Durabilidade esperada do fragmento:

| Camada | Pra que |
|---|---|
| `momento` | Válido só no momento da conversa (descarta logo) |
| `sessao` | Válido durante a sessão de uso |
| `semana` | Válido por dias |
| `rotina` | Válido por semanas/meses |
| `permanente` | Fato estável (data nascimento, nome de filhos, endereços fixos) |

Default: `sessao`.

### `tipo_esquecimento` — string (enum, opcional, nullable)

Política de esquecimento (futuro — pipelines não-implementadas no
agente irmão ainda):

- `null` — não esquece (protegido)
- `lento` — decai ao longo de meses
- `normal` — decai ao longo de semanas
- `efemero` — decai em dias

Default: `null`.

### `confianca` — float (0.0–1.0)

Auto-avaliação do LLM curador sobre quão certo está dessa info:

- `0.0–0.3` — especulativo, pode estar errado
- `0.4–0.6` — razoável, com nuances
- `0.7–0.9` — sólido, baseado em afirmação clara
- `0.9–1.0` — cristal claro, fato direto

Default: `0.7`.

### `peso` — float (0.0–1.0)

Quão importante é este fragmento. Cresce com `confirmacoes` e
`acessos`. Default: `0.5`.

### `confirmacoes` — int

Quantas vezes o dono confirmou (explicitamente ou implicitamente)
esta informação. Default: `0`.

### `acessos` — int

Quantas vezes o fragmento foi retornado em busca semântica útil (boost
de relevância pra quem é frequentemente acessado). Default: `0`.

### `user_id` — string

Brain dono do fragmento:

- `"gustavo"` — fatos sobre o dono
- `"lua"` — auto-observações da Lua

(Pode-se evoluir pra mais brains: `"familia"`, `"trabalho"`, etc.)

### `via` — string

Porta/origem onde o fragmento foi gerado:

- `"telegram-lua"` — bot Telegram da Lua
- `"claude-chat"` — porta Claude Chat
- `"custom-gpt"` — Custom GPT mobile
- `"web-custom"` — porta web (futura)
- `"alexa"` — porta Alexa (futura)
- `"manual"` — adicionado manualmente pelo dono via repo
- `"migracao"` — vindo de outra fonte (export antigo)

### `area` — string

Domínio do fragmento:

- `gus`, `lua` — sobre o agente em si (auto-observações)
- `saude`, `financeiro`, `pessoal`, `dimagem`, `projetos`, `pesquisa`,
  `receitas`, `esportes` — domínios do dono

Default: `""` (sem área específica).

### `projeto` — string

Se o fragmento se refere a projeto específico, nome do projeto.
Senão `""`.

### `criado_em` — string (ISO 8601 BRT)

Timestamp de criação. Ex: `"2026-04-28T15:30:00-03:00"`.

### `ultimo_acesso` — string (ISO 8601 BRT)

Última vez que esse fragmento foi retornado em busca útil. Atualizado
ao acessar. Default: igual a `criado_em`.

---

## Campos extras (curador híbrido — opcional)

Se a Lua usar **curador dual** (dois LLMs em paralelo, ex: Haiku +
Sonnet, pra calibragem), cada execução salva 2 fragmentos com:

### `curador` — string

Qual modelo gerou o fragmento. Ex: `"haiku"`, `"sonnet"`, `"haiku-4-5"`,
`"sonnet-4-6"`.

### `hash_janela` — string (sha8)

Hash dos 8 primeiros chars do sha256 da janela de turnos que gerou o
fragmento. Permite parear fragmentos do mesmo input gerados por
modelos diferentes (comparação par-a-par).

### `janela_turnos` — int

Quantas mensagens cobertas pela janela. Ex: `6` (3 turnos do dono + 3
da Lua).

---

## Exemplos completos

### Fragmento biográfico (sobre o dono)

```json
{
  "conteudo": "Gustavo é anestesiologista no Dimagem (Rio de Janeiro), pesquisador independente em IA brasileiro",
  "tipo": "biografico",
  "estado": "ativo",
  "camada_temporal": "permanente",
  "tipo_esquecimento": null,
  "peso": 0.9,
  "confirmacoes": 3,
  "confianca": 0.95,
  "acessos": 12,
  "user_id": "gustavo",
  "via": "telegram-lua",
  "area": "pessoal",
  "projeto": "",
  "criado_em": "2026-04-28T15:00:00-03:00",
  "ultimo_acesso": "2026-04-30T08:15:00-03:00"
}
```

### Fragmento operacional (sobre a Lua)

```json
{
  "conteudo": "Quando dono está cansado, abreviar respostas e oferecer pausa é mais útil do que aprofundar",
  "tipo": "identidade_operacional",
  "estado": "ativo",
  "camada_temporal": "rotina",
  "tipo_esquecimento": "lento",
  "peso": 0.6,
  "confirmacoes": 1,
  "confianca": 0.75,
  "acessos": 2,
  "user_id": "lua",
  "via": "telegram-lua",
  "area": "lua",
  "projeto": "",
  "criado_em": "2026-04-29T22:00:00-03:00",
  "ultimo_acesso": "2026-04-29T22:00:00-03:00",
  "curador": "sonnet"
}
```

### Fragmento dual (mesmo input, 2 curadores)

Mesmo conteúdo gerado por Haiku **e** Sonnet, com mesmo
`hash_janela`:

```json
// Versão Haiku
{
  "conteudo": "Dono está com hipertireoidismo em tratamento com tapazol",
  "curador": "haiku",
  "hash_janela": "a3f5b8c2",
  ...
}

// Versão Sonnet (do mesmo trecho)
{
  "conteudo": "Hipertireoidismo do dono tratado com tapazol; acompanhamento endocrinológico em andamento",
  "curador": "sonnet",
  "hash_janela": "a3f5b8c2",
  ...
}
```

Ambos no Hub. Comparação par-a-par mostra qual modelo extrai melhor
(mesmo `hash_janela` permite agrupar pares no Obsidian).

---

## Validação

Recomendado validar payload antes de inserir no Qdrant via Pydantic
ou similar. Schema mínimo:

```python
from pydantic import BaseModel, Field
from typing import Optional, Literal

class FragmentoSchema(BaseModel):
    conteudo: str = Field(min_length=10)
    tipo: Literal[
        "identidade_operacional", "biografico", "emocional", "decisao",
        "procedural", "rotina", "meta_reflexao", "conexao_emergente",
        "episodico", "cronologico", "fato", "preferencia", "lacuna",
        "projeto"
    ]
    estado: Literal["ativo", "historico", "arquivado", "quarentena"] = "ativo"
    camada_temporal: Literal[
        "momento", "sessao", "semana", "rotina", "permanente"
    ] = "sessao"
    tipo_esquecimento: Optional[Literal["lento", "normal", "efemero"]] = None
    user_id: str
    via: str
    area: str = ""
    projeto: str = ""
    confianca: float = Field(default=0.7, ge=0.0, le=1.0)
    peso: float = Field(default=0.5, ge=0.0, le=1.0)
    confirmacoes: int = 0
    acessos: int = 0
    criado_em: str
    ultimo_acesso: Optional[str] = None
    curador: Optional[str] = None
    hash_janela: Optional[str] = None
    janela_turnos: Optional[int] = None
```

Se validação falha, fragmento NÃO é inserido — bloqueio.

---

## Versão

| Versão | Data | Mudança |
|---|---|---|
| 0.1-rascunho | 2026-04-28 | Schema espelhado de gus-18 do agente irmão. Aguarda decisão se Lua mantém schema idêntico ou refina |
