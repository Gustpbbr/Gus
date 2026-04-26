---
tipo: guia-setup
data: 2026-04-26
status: concluido
area: infra-memoria
anterior: gus-15-decisao-migracao.md
proximo: gus-19-etapa1-mem0-selfhost.md
---

# Setup do ambiente — Qdrant Cloud + Railway

## Status atual (2026-04-26)

- Cluster Qdrant Cloud criado: `Gus`, GCP us-east4
- URL: `https://e18d26d4-ac4c-4fd5-afe1-9beae5754123.us-east4-0.gcp.cloud.qdrant.io:6333`
- Variáveis adicionadas no Railway: `QDRANT_URL` e `QDRANT_API_KEY`

## Pré-requisitos

- Conta Railway com o serviço Gus rodando
- `ANTHROPIC_API_KEY` já configurada no Railway
- `MEM0_API_KEY` ainda presente (manter durante migração, remover depois)

## Passo a passo para recriar (se necessário)

### 1. Criar cluster no Qdrant Cloud

1. Acessar cloud.qdrant.io
2. Create Cluster → Free tier
3. Nome: `Gus`
4. Cloud provider: GCP
5. Região: us-east4 (Virginia)
6. Configuração: 1 nó, 4GiB disco, 1GiB RAM
7. Criar e aguardar o cluster ficar ativo
8. Copiar: Cluster Endpoint URL + API Key

### 2. Configurar variáveis no Railway

No serviço Gus → Variables → New Variable:

```
QDRANT_URL=https://<cluster-id>.us-east4-0.gcp.cloud.qdrant.io:6333
QDRANT_API_KEY=<api-key-do-qdrant>
```

A porta `:6333` no final da URL é obrigatória.

### 3. Verificar

Após o próximo deploy, o log deve mostrar inicialização sem erros de conexão.
Para testar manualmente, consultar `gus-19-etapa1-mem0-selfhost.md` (seção validação).

## Variáveis de ambiente completas do projeto

| Variável | Onde configurar | Obrigatória |
|---|---|---|
| `ANTHROPIC_API_KEY` | Railway | sim |
| `TELEGRAM_BOT_TOKEN` | Railway | sim |
| `GITHUB_TOKEN` | Railway | sim |
| `GITHUB_REPO` | Railway | sim |
| `MEM0_API_KEY` | Railway | temporário (migração) |
| `QDRANT_URL` | Railway | sim (após etapa 1) |
| `QDRANT_API_KEY` | Railway | sim (após etapa 1) |
| `CUSTOM_GPT_TOKEN` | Railway | sim (API) |
| `API_PUBLIC_URL` | Railway | sim (API) |
