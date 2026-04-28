---
tipo: schema-canonico
area: dimagem
atualizado: 2026-04-28
---

# Schema canônico — `dimagem/dia/AAAA-MM-DD.md`

Documenta o schema **único** que arquivos `dimagem/dia/` devem seguir.
Resolve a fragmentação observada (arquivos com sufixos `-assim`,
`-outros`, `-master` que apareciam por extração ruim).

## Regra de ouro

**Um arquivo por dia.** Nome: `AAAA-MM-DD.md`. **Nunca** criar
sufixos como `-assim`, `-outros`, `-master`.

Arquivos legacy fragmentados (de antes deste schema) ficam intocados
mas novos saves seguem schema único.

## Estrutura do arquivo

```markdown
---
capturado_em: AAAA-MM-DDTHH:MM:SS
via: telegram
tipo: dia-dimagem
unidade: Dimagem São Gonçalo | Dimagem Taquara
---

# Pacientes — DD/MM/AAAA

| Nome | Data | Exame | Plano | Valor |
|---|---|---|---|---|
| <nome completo> | DD/MM/AAAA | <exame> | <convênio normalizado> | R$ XXX |
```

## Schema das colunas

| Coluna | Formato | Obrigatório |
|---|---|---|
| **Nome** | Nome completo do paciente | Sim |
| **Data** | DD/MM/AAAA (data do exame, geralmente hoje) | Sim |
| **Exame** | Nome do exame (ex: `RM CRANIO`, `TC TORAX`, `US ABDOME`) | Sim |
| **Plano** | Convênio **normalizado** via `dimagem/convenios.json` (ex: `Assim Taquara`, não `ASSIM TAQUARA`) | Sim |
| **Valor** | `R$ XXX` ou `—` se não tiver | Não |

## Convênios canônicos

Ver `dimagem/convenios.json`. **Não inventar variações**:

- ❌ `INTERMEDICA NOVA IGUAÇU`
- ❌ `intermedica ni`
- ✅ `Intermédica – Nova Iguaçu`

## Bot Telegram — fluxo de salvamento

1. Foto de OS Dimagem chega
2. Haiku extrai dados (nome, exame, data, convênio, valor) com gate de confiança
3. Se confiança baixa → pede reenvio (NÃO salva)
4. Se confiança média/alta → preview de aprovação
5. Após aprovação:
   - Lê `dimagem/dia/AAAA-MM-DD.md` (cria se não existe)
   - Append nova linha (deduplica por nome — não duplica se já está)
   - Salva — **sempre no mesmo arquivo do dia**, sem sufixos

## Casos clínicos didáticos

**NÃO salvar aqui.** Vão em `dimagem/casos/<caso-pseudonimo>.md` com
pseudônimo. Aqui é registro operacional pra cobrança e pra Gustavo
saber quem atendeu.

## Migração de arquivos legacy

Arquivos com sufixo (`-assim`, `-outros`) de antes de 28/04/2026
ficam como estão (histórico). Eventualmente podem ser consolidados
manualmente no arquivo principal do dia, mas não é prioridade.
