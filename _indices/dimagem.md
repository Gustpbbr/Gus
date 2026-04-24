---
tipo: indice
area: dimagem
atualizado: 2026-04-24
---

# Índice — Dimagem

## Estado atual
Dimagem é a clínica de anestesia onde Gustavo trabalha — sustento principal. *(Seed inicial — preencher com contexto real quando capturado.)*

## Últimos editados (5 mais recentes)
- *(sem registros ainda)*

## Todos os arquivos (ordem alfabética)
- *(sem registros ainda)*

## Pastas relacionadas
- `dimagem/protocolos/` — protocolos da clínica (sedação, anestesia, etc.)
- `dimagem/casos/` — casos interessantes / didáticos
- `dimagem/admin/` — pendências administrativas

## Convenções desta área

- **Protocolo:** `dimagem/protocolos/protocolo-[nome].md`. Ex: `protocolo-sedacao.md`.
- **Caso:** `dimagem/casos/caso-[descricao-curta]-[mes]-[ano].md`. Ex: `caso-intubacao-dificil-mar-2026.md`.
- **Admin:** `dimagem/admin/pendencias.md` (mestre) + `dimagem/admin/[assunto].md` pra itens específicos.
- **Dados de paciente:** nunca salvar identificação do paciente (nome, RG, CPF). Se precisar, usar pseudônimo ou iniciais em `dimagem/casos/` e documentos identificáveis vão pra `sensivel/dimagem/`.

## Fluxo quando chegar nota de plantão ou caso

1. Bot identifica se é protocolo (reutilizável), caso (didático) ou admin (pendência).
2. Cria MD na subpasta correta com frontmatter.
3. Atualiza este índice.
