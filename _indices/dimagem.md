---
tipo: indice
area: dimagem
atualizado: 2026-04-24
---

# Índice — Dimagem

## Estado atual
Dimagem é a clínica de anestesia onde Gustavo trabalha — sustento principal. Captura diária via foto de OS no Telegram, consolidada em UM arquivo por dia em `dimagem/dia/`.

## Últimos editados (5 mais recentes)
- `dimagem/dia/2026-04-24.md` — pacientes do dia (24/04/2026, 9 pacientes)

## Todos os arquivos (ordem alfabética)
- `dimagem/dia/2026-04-24.md`

## Pastas relacionadas
- `dimagem/dia/` — UM arquivo por dia com pacientes/exames/convênios (fluxo principal)
- `dimagem/protocolos/` — protocolos da clínica (sedação, anestesia, etc.)
- `dimagem/casos/` — casos didáticos com pseudônimo (intercorrências, dificuldades técnicas)
- `dimagem/admin/` — pendências administrativas

## Convenções desta área

- **Dia (lista de pacientes):** `dimagem/dia/AAAA-MM-DD.md`. UM arquivo por dia, atualizado por append. Schema fixo: `Nome | Data | Exame | Plano`. Ver `gus/system_prompt.md → Fluxo: foto de OS Dimagem`.
- **Protocolo:** `dimagem/protocolos/protocolo-[nome].md`. Ex: `protocolo-sedacao.md`.
- **Caso:** `dimagem/casos/caso-[descricao-curta]-[mes]-[ano].md`. Ex: `caso-intubacao-dificil-mar-2026.md`. Pseudônimo ou iniciais — não nome real.
- **Admin:** `dimagem/admin/pendencias.md` (mestre) + `dimagem/admin/[assunto].md` pra itens específicos.

## Sobre dados identificáveis

A pasta `dimagem/dia/` contém nomes completos de pacientes — decisão operacional do Gustavo (visibilidade rápida pro dia-a-dia). Se em algum momento ele optar por LGPD-strict, mover toda `dimagem/dia/` pra `sensivel/dimagem/dia/` e ajustar o path no `system_prompt.md`. Casos didáticos (`dimagem/casos/`) continuam com pseudônimo.

## Fluxo quando chegar foto de OS

1. Bot detecta foto de OS Dimagem (cabeçalho + nomes + exames + convênios).
2. `read_from_github("dimagem/dia/AAAA-MM-DD.md")` com a data de hoje.
3. Se existe: extrai pacientes novos, deduplica por nome, append à tabela.
4. Se não existe: cria com frontmatter + cabeçalho + tabela.
5. Atualiza este índice na próxima sessão de manutenção.
