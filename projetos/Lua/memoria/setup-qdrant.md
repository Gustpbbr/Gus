---
tipo: setup-memoria
componente: qdrant-cloud
agente: Lua
estimativa: ~20min
status: aguardando-decisoes
---

# Setup — Coleção Qdrant `lua_hub`

Passo a passo pra criar a coleção da Lua no Qdrant Cloud, separada
da memória de outros agentes.

---

## Pré-requisito

Conta Qdrant Cloud (`cloud.qdrant.io`). **Free tier** é suficiente:
- 1 cluster
- 4 GiB de armazenamento
- Sem expiração

Se já tem cluster (porque outro agente já usa), pode reusar — Lua
ganha **coleção separada** dentro do mesmo cluster.

---

## Etapa 1 — Decidir cluster

Opção A — **Mesmo cluster** que outro agente usa:
- ✅ US$0 (free tier cobre N coleções no mesmo cluster)
- ✅ Operacionalmente simples
- ⚠️ Free tier tem limite de 4 GiB compartilhado entre todas as coleções
- ⚠️ Se outro agente tem incidente, Lua pode ser afetada

Opção B — **Cluster novo** dedicado pra Lua:
- ✅ Isolamento total
- ⚠️ Conta separada ou sub-projeto na conta atual
- ✅ Free tier permite múltiplos clusters em contas diferentes
- ✅ Pode usar mesma conta com 2 clusters se ainda dentro do free tier

Recomendação V1: **Opção A** (mesmo cluster, coleção separada). Migrar
pra B se Lua crescer e precisar isolamento.

---

## Etapa 2 — Criar coleção `lua_hub`

Via UI ou via Python.

### Via UI Qdrant Cloud

1. Login `cloud.qdrant.io`
2. Cluster → Open Cluster Console
3. Tab **Collections** → **Create Collection**
4. **Name**: `lua_hub`
5. **Vector configuration**:
   - **Size**: `384` (sentence-transformers `all-MiniLM-L6-v2`)
   - **Distance**: `Cosine`
6. **Create**

### Via Python (recomendado pra reproduzir setup)

```python
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PayloadSchemaType
)

client = QdrantClient(
    url="https://xyz.qdrant.io",  # do cluster
    api_key="seu-api-key",
)

COLLECTION = "lua_hub"
EMBED_DIM = 384

# 1. Criar coleção
client.create_collection(
    collection_name=COLLECTION,
    vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE),
)

# 2. Criar índices de payload (pra filtrar por user_id, tipo, area, etc.)
campos_indexar = (
    "user_id", "tipo", "estado", "area", "via", "projeto",
    "tipo_esquecimento", "camada_temporal", "curador",
)
for field in campos_indexar:
    client.create_payload_index(
        collection_name=COLLECTION,
        field_name=field,
        field_schema=PayloadSchemaType.KEYWORD,
    )

print(f"Coleção {COLLECTION} criada com índices.")
```

---

## Etapa 3 — Estrutura dos brains

A Lua tem **2 brains** dentro da mesma coleção `lua_hub`:

| Brain | `user_id` | Pra que serve |
|---|---|---|
| **Dono** | `"gustavo"` | Fatos sobre o dono — saúde, projetos, preferências, contexto pessoal |
| **Lua** | `"lua"` | Auto-observações da Lua — padrões aprendidos, princípios emergidos, aprendizados táticos |

Filtros via `user_id` separam os dois brains. Mesma coleção, mesma
infra, busca semântica isolada.

---

## Etapa 4 — Schema do payload (gus-18 adaptado)

Cada fragmento tem este payload:

```json
{
  "conteudo": "texto do fragmento auto-suficiente em PT-BR",
  "tipo": "biografico",
  "estado": "ativo",
  "camada_temporal": "permanente",
  "tipo_esquecimento": null,
  "peso": 0.5,
  "confirmacoes": 0,
  "confianca": 0.85,
  "acessos": 0,
  "via": "telegram-lua",
  "area": "saude",
  "projeto": "",
  "user_id": "gustavo",
  "criado_em": "2026-04-28T15:00:00-03:00",
  "ultimo_acesso": "2026-04-28T15:00:00-03:00",
  "curador": "haiku",
  "hash_janela": "abc12345",
  "janela_turnos": 6
}
```

Detalhes em `memoria/schema-fragmentos.md`.

---

## Etapa 5 — Validar setup

```python
# Inserir fragmento de teste
from qdrant_client.models import PointStruct
import uuid
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

texto_teste = "Lua foi criada em 28/04/2026 como agente pessoal de IA"
vetor = embedder.encode(texto_teste).tolist()

frag_id = str(uuid.uuid4())
client.upsert(
    collection_name=COLLECTION,
    points=[PointStruct(
        id=frag_id,
        vector=vetor,
        payload={
            "conteudo": texto_teste,
            "tipo": "biografico",
            "estado": "ativo",
            "camada_temporal": "permanente",
            "user_id": "lua",
            "via": "manual-teste",
            "area": "lua",
            "criado_em": "2026-04-28T15:00:00-03:00",
        },
    )],
)

# Buscar
from qdrant_client.models import Filter, FieldCondition, MatchValue

resultado = client.query_points(
    collection_name=COLLECTION,
    query=embedder.encode("quando lua nasceu").tolist(),
    query_filter=Filter(must=[
        FieldCondition(key="user_id", match=MatchValue(value="lua"))
    ]),
    limit=3,
    with_payload=True,
)

for p in resultado.points:
    print(f"  {p.score:.3f} - {p.payload['conteudo']}")
```

Se imprime o fragmento de teste, setup está OK.

---

## Etapa 6 — Variáveis de ambiente

No Railway (e em `.env.example`):

```
QDRANT_URL=https://xyz.qdrant.io
QDRANT_API_KEY=...

# Coleção (default já é "lua_hub" no código, mas pode override)
QDRANT_COLLECTION=lua_hub
```

---

## Pitfalls comuns

### 1. Dimensão do vetor errada

Se mudar de `all-MiniLM-L6-v2` (384 dim) pra outro modelo (ex:
`text-embedding-ada-002` da OpenAI = 1536 dim), tem que **recriar a
coleção** com novo `size`. Não dá pra mudar dimensão de coleção
existente.

### 2. Filtro `user_id` errado retorna brain errado

Se busca esquecer filtro, pode retornar fragmentos do brain do dono
quando esperava do brain da Lua. Sempre filtrar.

### 3. Coleção criada sem índices de payload

Sem índices, filtros funcionam mas são lentos (full scan). Criar
índices nos campos da Etapa 2.

### 4. Free tier Qdrant esgota

4 GiB cobre milhões de fragmentos pequenos. Mas se Lua acumula
muito (ex: ingestão de papers científicos com texto longo), pode
estourar. Monitorar via dashboard Qdrant.

---

## Versão

| Versão | Data | Mudança |
|---|---|---|
| 0.1-rascunho | 2026-04-28 | Setup espelhado em `hub.store` do agente irmão. Aguarda decisão sobre cluster |
