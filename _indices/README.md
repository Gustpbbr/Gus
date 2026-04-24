---
tipo: pasta-regras
atualizado: 2026-04-24
---

# _indices/ — dashboards vivos por área

Esta pasta contém **um MD por grande área de conhecimento** do Gustavo. Cada índice é um "mapa" (MOC — Map of Content) que resume o estado atual da área, aponta pros últimos arquivos editados e lista tudo em ordem alfabética.

## Índices atuais

- `00-master.md` — meta-índice, aponta pros outros
- `saude.md`
- `financeiro.md`
- `projetos.md`
- `dimagem.md`
- `receitas.md`
- `capturado.md`

## Regras de formato (todos os índices)

Todo índice segue exatamente este template:

```markdown
---
tipo: indice
area: <nome-da-area>
atualizado: AAAA-MM-DD
---

# Índice — <Nome da Área>

## Estado atual
<resumo curado em 3-7 linhas do que está ativo / aberto / em foco>

## Últimos editados (5 mais recentes)
- AAAA-MM-DD — [[nome-do-arquivo]] — descrição curta
- ...

## Todos os arquivos (ordem alfabética)
- [[nome-arquivo-a]]
- [[nome-arquivo-b]]
- ...

## Pastas relacionadas
- `caminho/pasta-1/` — o que tem aqui
- `caminho/pasta-2/` — o que tem aqui

## Convenções desta área
<regras específicas: nomenclatura, frontmatter, categorização>
```

## Regras de manutenção (o Gus atualiza ao salvar)

O bot do Telegram segue estas regras quando salva um novo MD em qualquer área:

1. **Identifica a área** do conteúdo. Se não bate com nenhuma pasta existente, decide se é importante o suficiente pra criar pasta nova. Se sim:
   - Cria a pasta (salvando um `README.md` inicial dentro dela)
   - Cria um índice correspondente em `_indices/`
   - Atualiza `_indices/00-master.md` listando a nova área
2. **Salva o arquivo** no local correto (com frontmatter padrão).
3. **Atualiza o índice da área** (`_indices/<area>.md`):
   - Adiciona em "Últimos editados" no topo (mantém 5 mais recentes)
   - Adiciona em "Todos os arquivos" em ordem alfabética
   - Se mudou algo estrutural (novo tema, nova subpasta), atualiza "Estado atual" e "Pastas relacionadas"
   - Atualiza o frontmatter `atualizado:` pra data de hoje
4. **Índice é dashboard**, não duplicata. Nunca copia conteúdo dos MDs detalhados; só aponta com wikilinks e dá contexto.

## Regra pra criar pasta nova

Só cria pasta nova quando:
- O assunto é recorrente (vai ter múltiplos MDs ao longo do tempo), OU
- O assunto é importante o suficiente pra ter estado próprio (ex: uma nova clínica, um novo projeto, uma nova condição de saúde)

Não cria pasta pra captura de evento único sem perspectiva de retorno. Nesse caso, usa `capturado/misc/` ou a área mais próxima.
