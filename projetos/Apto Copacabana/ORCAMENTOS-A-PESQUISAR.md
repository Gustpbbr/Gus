# Fila de serviços a orçar — Apto Copacabana

**Criado em:** 2026-11-08  
**Objetivo:** registrar, aos poucos, cada serviço da lista que o usuário vai fornecer. **Ainda não pesquisar fornecedores** para os novos itens, salvo quando o usuário pedir explicitamente.

## Como usar este índice

- O usuário está preparando uma lista de serviços; cada novo item deverá gerar ou atualizar um arquivo em `servicos/<slug>/PEDIDO-ORCAMENTO.md`.
- O modelo está em [MODELO-PEDIDO-ORCAMENTO.md](MODELO-PEDIDO-ORCAMENTO.md).
- O procedimento de continuidade entre abas está em [CONTINUIDADE-ORCAMENTOS.md](CONTINUIDADE-ORCAMENTOS.md).
- A pesquisa de fornecedores e os links `wa.me` só serão preparados **na fase posterior**.
- Não colocar detalhes pessoais do imóvel neste repositório público.

## Lista de novos pedidos

| ID | Serviço | Ambiente | Arquivo específico | Estado | Última atualização |
|---|---|---|---|---|---|
| — | Aguardando o usuário fornecer a lista | — | — | `aguardando-lista` | 2026-11-08 |

**Não confundir com serviços já pesquisados:** o remanejamento do aquecedor a gás já está em [ORCAMENTOS-PREPARADOS.md](ORCAMENTOS-PREPARADOS.md), com sete contatos preparados; não recriar esse serviço aqui como pendente de pesquisa.

## Ao receber cada item

1. Verificar se já existe arquivo equivalente no GitHub.
2. Criar ou atualizar o arquivo individual e sua descrição, sem presumir especificações não dadas.
3. Atualizar esta tabela substituindo a linha de espera quando a primeira entrada for criada.
4. Informar ao usuário o que foi registrado.
5. Esperar a lista continuar; **não iniciar busca de fornecedores**.

## Estados da fila

- `a-detalhar`: há lacunas que podem afetar o orçamento.
- `aguardando-pesquisa`: pedido documentado, ainda sem fornecedores.
- `pesquisa-em-andamento`: busca expressamente solicitada.
- `links-prontos`: pesquisas completas; mover ou referenciar em `ORCAMENTOS-PREPARADOS.md`.

Quando um pedido for pesquisado, preservar o arquivo original e referenciar a pesquisa concluída; não apagar o histórico.
