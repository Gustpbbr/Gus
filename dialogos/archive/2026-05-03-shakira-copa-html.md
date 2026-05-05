---
tipo: demanda
origem: gustavo
destino: claude-code
prioridade: alta
status: concluido
criado_em: 2026-05-03T01:08:34.453320-03:00
processado_em: 2026-05-03T14:15:00-03:00
processado_por: claude-code
---

Gus code, por favor agende a criação de um html as 8h da manha de 03 maio de 2026, [fazendo](http://fazendo.um) a estrutura de um site sobre o show da Shakira em copa copacabana. Faca a estrutura e coloque como demanda para o Claude chat terminar, melhorando estetica e informação

## Resultado (2026-05-03)

Hora 8h já tinha passado quando processei (Gustavo aprovou seguir em ~14h).
Estrutura V1 criada: `capturado/shakira-copa-2026/index.html`.

Decisões:
- Local escolhido: `capturado/shakira-copa-2026/` (categoria "captura" do CLAUDE.md
  é o catch-all certo — não vira projeto Gus, não é pessoal/saude).
- HTML mobile-first sem framework, paleta rosa+roxo (Shakira-friendly).
- Placeholders explícitos `[BRACKETS]` em todo conteúdo factual + comentários
  HTML em cada seção dizendo o que Chat deve fazer.
- Estrutura: hero / info / sobre / setlist / FAQ / footer.
- 6 seções, cards com gradient, accordion FAQ via `<details>` nativo.

Demanda pro Chat finalizar criada em:
`dialogos/inbox-claude-chat/2026-05-03T14-15__shakira-copa-html-finalizar.md`.
Lá tem checklist do que falta (web search pra confirmar show, conteúdo real,
estética, acessibilidade) + protocolo de entrega via `-vX`.