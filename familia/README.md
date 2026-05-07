# familia/

Registros sobre a família do Gustavo.

## ⚠️ Decisão pendente sobre estrutura

Estrutura mínima criada. Como crescer a partir daqui depende do uso.
Possibilidades:

- **`<nome-membro>.md`** — página dedicada por familiar (cônjuge,
  filhos, pais, irmãos)
- **`saude-familia.md`** — saúde dos familiares próximos (importante
  pra histórico de saúde do Gustavo, contexto de decisões)
- **`memorias-conjuntas.md`** — registros de eventos importantes
- **`agenda-familiar.md`** — datas relevantes (aniversários,
  recorrências familiares)

## Diferença pra `contatos/`

- **`familia/`**: registro **profundo** sobre familiares próximos,
  com histórico, contexto, dinâmicas familiares
- **`contatos/`**: registro **superficial** de pessoas em geral
  (incluindo família), foco em "saber quem é cada um"

## ⚠️ LGPD — terceiros

Familiares também são "terceiros" do ponto de vista LGPD. Dados
sensíveis (saúde de familiares, situação financeira de cônjuge,
documentos) vão em `sensivel/familia/`, não aqui.

Aqui ficam contextos compartilháveis: relacionamentos, eventos
significativos, padrões observados pelo Gustavo, decisões importantes
em conjunto.

## Como o bot trata

Bot detecta menção a familiar e registra em `familia/<nome-curto>.md`
ou em `familia/memorias-conjuntas.md`, conforme contexto. Em dúvida,
pergunta antes.
