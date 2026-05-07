Criar uma nova demanda no inbox correto com base na descrição do usuário.

Argumento recebido: $ARGUMENTS

**Passo 1 — Entender a demanda**

Se $ARGUMENTS estiver vazio, pergunte: "Descreva a demanda: o que deve ser feito, destino (claude-code / tiogu / claude-chat), prioridade (alta/media/baixa) e contexto."

Se $ARGUMENTS tiver conteúdo, extraia as seguintes informações (use padrão se não especificado):
- `destino`: claude-code (padrão) | tiogu | claude-chat | gpt-chat
- `prioridade`: media (padrão) | alta | baixa
- `acao_sugerida`: implementar (padrão) | investigar | criar_novo | deletar
- `area`: inferir do conteúdo (ex: gus, saude, dimagem, financeiro...)
- `titulo`: resumo de 3-8 palavras
- `corpo`: descrição completa em markdown

**Passo 2 — Gerar nome do arquivo**

Formato: `dialogos/inbox-{destino}/AAAA-MM-DDTHH-MM__{slug}.md`
- Data/hora: usar `date +%Y-%m-%dT%H-%M` via bash
- Slug: 3-5 palavras do título em kebab-case (sem acentos)

**Passo 3 — Criar o arquivo**

```yaml
---
tipo: demanda
origem: gpt-chat
destino: <destino>
prioridade: <prioridade>
status: pendente
criado_em: <ISO8601 com timezone -03:00>
processado_em: ""
processado_por: ""
acao_sugerida: <acao_sugerida>
destino_path: <path relevante ou "a definir">
contexto: "<resumo de 1 linha>"
---

# <Título>

## O que fazer

<corpo da demanda>

## Critério de sucesso

<o que indica que está pronto>
```

**Passo 4 — Confirmar**

Mostre o conteúdo do arquivo e o path para o usuário confirmar antes de salvar. Após confirmação, salve com a tool Write e confirme criação.
