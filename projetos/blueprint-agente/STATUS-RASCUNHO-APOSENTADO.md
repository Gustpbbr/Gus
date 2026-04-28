---
tipo: status
status: rascunho-aposentado
desde: 2026-04-28
---

# ⚠️ Rascunho aposentado

Esta pasta foi tentativa inicial de criar um **blueprint genérico** de agente
pessoal multi-portas — um guia que pudesse ser copiado pra qualquer repo
limpo e gerar um agente novo do zero.

## Por que está aposentada

Durante o desenvolvimento (sessões de 27-28/04/2026), 3 fatos apareceram:

1. **Estava só ~25% completo** — apenas `00-leia-primeiro/` (5 arquivos) +
   1 nó-folha exemplo (`02-identidade-e-memoria/identidade-canonica/base/`).
   Os outros ~70 arquivos planejados eram pastas vazias com `.gitkeep`.

2. **`projetos/Lua/` virou alternativa mais útil** — em vez de blueprint
   genérico abstrato, fizemos uma instância concreta (Lua) com identidade
   real, system prompts reais, setups reais. Lua resolveu o problema que
   o blueprint resolveria (e foi apontado como mais útil pelo dono).

3. **Insight do dono sobre identidade emergente** — ele apontou que se ele
   responder uma "entrevista de descoberta" com 30 perguntas, o agente vira
   espelho dele, não nasce com identidade própria. O blueprint estava
   estruturado pra esse exato modelo (responder placeholders → instanciar)
   que ele rejeitou.

## O que ficou de útil aqui

- **`00-leia-primeiro/visao-geral.md`** — descreve bem o que um agente
  pessoal multi-portas é
- **`00-leia-primeiro/pre-requisitos.md`** — lista de contas externas
  e custos esperados (~US$15-30/mês)
- **`00-leia-primeiro/passo-a-passo-resumido.md`** — 7 etapas de
  implementação
- **`00-leia-primeiro/glossario.md`** — termos canônicos (porta, brain,
  fragmento, curador, vault, ciclo vital)
- **`02-identidade-e-memoria/identidade-canonica/base/`** — exemplo de
  nó-folha com template universal e arquivo editável

Tudo isso tem valor de referência mesmo sem completar o resto.

## Em vez de continuar isto, ir pra

- **`projetos/Lua/`** — instância concreta com identidade própria
  (mesmo em standby de calibração final, está mais avançada)
- **`projetos/gus/auditorias/2026-04-27/arquitetura-projeto-pre-agi/`** —
  mapa funcional do agente real, com cruzamento contra estado atual

## Status técnico

- Pasta **NÃO** sincroniza com Drive (default já cobre via
  `EXCLUDE_PREFIXES` em `sync_to_drive.py` — `historico/` é excluída,
  esta pasta poderia ser também se virasse legado real)
- Conteúdo **preservado** no histórico do git (PR #17)
- **Pode ser deletada** sem impacto operacional. Mantida porque o conteúdo
  parcial pode ser útil como referência futura
