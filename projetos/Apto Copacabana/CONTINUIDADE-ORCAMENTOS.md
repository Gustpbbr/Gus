# Continuidade entre conversas — Orçamentos do Apto Copacabana

**Versão:** 1.0 · **Data:** 2026-11-08  
**Objetivo:** permitir que outra conversa do ChatGPT retome este trabalho consultando arquivos concretos no GitHub, sem depender do histórico do chat original.

## Atualização operacional — Serviço 06 PESQUISADO em 2026-11-08

Pesquisa de **8 empresas de janelas acústicas**, autorizada pelo usuário, sem medidas disponíveis. [Contatos/WhatsApps](servicos/06-janela-acustica/FORNECEDORES-JANELAS-2026-11-08.md), com mensagem de primeiro contato curta: comparar troca da janela com segunda janela interna, avaliar visita e custo. Instagram identificado apenas quando vinculado a fonte; nenhum contato enviado. Sem decisão de modelo ou fornecedor.

## Atualização operacional — Serviço 02 PESQUISADO em 2026-11-08

O usuário informou que **os ventiladores novos ainda serão escolhidos** e pediu busca de instaladores, inclusive Instagram. Foram encontrados **7 fornecedores**, listados em [FORNECEDORES-VENTILADORES-2026-11-08.md](servicos/02-ventiladores-teto/FORNECEDORES-VENTILADORES-2026-11-08.md); WhatsApp com mensagem curta para retirar ventiladores antigos e instalar novos, com preço por unidade. Instagram verificado indiretamente apenas para O Rei dos Reparos; não inventar perfis. **Nenhuma mensagem enviada.**

## Atualização operacional — Serviço 01 PESQUISADO em 2026-11-08

A pedido expresso do usuário, foram localizados **8 fornecedores** para reforma elétrica. Sites e números, perfil da especialidade, notas de verificação e links WhatsApp com primeiro contato **curto e cordial** estão em [FORNECEDORES-ELETRICA-2026-11-08.md](servicos/01-reforma-eletrica/FORNECEDORES-ELETRICA-2026-11-08.md). O detalhamento técnico permanece em [PEDIDO-ORCAMENTO.md](servicos/01-reforma-eletrica/PEDIDO-ORCAMENTO.md). Nenhum envio ou resposta confirmado.

**Regra crucial:** mensagens iniciais de TODOS os serviços devem ser breves. Não incluir checklist técnico extenso no primeiro WhatsApp; deixar análise técnica para vistoria/etapa posterior.

## Atualização operacional — lista inicial já recebida em 2026-11-08

**O usuário enviou e autorizou a criação dos 16 MDs iniciais.** Eles estão indexados em [ORCAMENTOS-A-PESQUISAR.md](ORCAMENTOS-A-PESQUISAR.md), numerados 01–16. Não criar itens duplicados ao reabrir a conversa. **Agora o próximo passo é enriquecer os itens ainda sem pesquisa, um por vez. Serviço 01 já foi pesquisado por ordem expressa; os demais exigem pedido específico.**

**Correção mais recente:** serviço 11 prevê **máquina de lavar convencional Brastemp de 8 kg (não lava e seca)**. A adequação elétrica específica está postergada; esta etapa trata apenas de retirada do bidê e preparação hidráulica/esgoto. O serviço 01 também exclui a lavadora desta fase.

**Exemplos de gatilhos:** "detalhar o 11", "vamos para o serviço 05", "altere a janela do 06" → abrir os MDs correspondentes. "Quero o orçamento pro gás" → serviço 07, links já preparados.

## Intenção explícita do usuário em 2026-11-08

O usuário vai **fornecer uma lista de serviços para os quais precisa de orçamento**, possivelmente em várias mensagens. **Nesta fase não deseja pesquisa de fornecedores.**

A tarefa inicial é:
1. Receber cada serviço da lista.
2. Criar **um arquivo Markdown específico para cada serviço**, ainda sem fornecedores ou links fictícios.
3. Registrar o escopo conhecido e as lacunas técnicas como "a confirmar".
4. Manter um índice consolidado dos serviços ainda não pesquisados.
5. Conforme o usuário fornecer informações adicionais, atualizar o Markdown do serviço correspondente, preservando decisões anteriores relevantes.
6. **Somente quando o usuário pedir a pesquisa daquele serviço**, aplicar o protocolo completo de fornecedores (mínimo cinco verificáveis quando disponíveis, sites oficiais, Instagram público, WhatsApp pré-preenchido) e atualizar o registro.
7. **Somente quando o usuário pedir para apresentar/enviar os orçamentos**, entregar links `wa.me` já preparados, sem afirmar que enviou mensagens.

**Importante:** "preparar o Markdown" NÃO significa pesquisar fornecedores, gerar links `wa.me` reais, agendar envios, solicitar orçamentos ou marcar contato como realizado.

## Ponto de entrada obrigatório em conversa nova

Repositório: `Gustpbbr/Gus`  
Pasta: `projetos/Apto Copacabana/`

Ordem de leitura quando a conversa envolve orçamento do apartamento:
1. `README.md` — visão e links;
2. **`CONTINUIDADE-ORCAMENTOS.md`** — este procedimento;
3. **`ORCAMENTOS-A-PESQUISAR.md`** — fila de pedidos e respectivos arquivos;
4. `ORCAMENTOS-PREPARADOS.md` — pesquisas completas e links prontos;
5. `PROTOCOLO-ORCAMENTOS.md` — pesquisa, validação e WhatsApp;
6. `PAINEL-SERVICOS.md` — andamento transversal.

Se o usuário disser:
- **"Vou listar os serviços"**: receber itens e criar/atualizar arquivos `servicos/<slug>/PEDIDO-ORCAMENTO.md`; NÃO pesquisar empresas.
- **"Acrescente esse detalhe ao orçamento da [categoria]"**: ler o arquivo específico, adicionar a informação na seção apropriada e atualizar a data; não alterar dados confirmados sem razão.
- **"Pesquise fornecedores da [categoria]"**: pesquisar, verificar e registrar contatos no arquivo específico e em `ORCAMENTOS-PREPARADOS.md`.
- **"Quero o orçamento pro gás"**: serviço de gás JÁ pesquisado; conferir o índice `ORCAMENTOS-PREPARADOS.md` e apresentar links guardados em `servicos/gas/ORCAMENTO-GAS-2026-11-09.md`.
- **"Quero o orçamento da [categoria]"**: se constar como `links-prontos`, abrir e apresentar os links. Se constar como `aguardando-pesquisa`, informar isso e perguntar se deseja realizar a pesquisa agora, a menos que já tenha autorizado a pesquisa na mesma solicitação.
- **"Atualize a lista"**: ler índices e registrar cada etapa que o usuário efetivamente confirmou.

## Estados por serviço

`a-detalhar` → `aguardando-pesquisa` → `pesquisa-em-andamento` → `pesquisa-concluida` (levantamento de contatos públicos, possível personalização privada pendente) → `links-prontos` → `mensagens-enviadas-pelo-usuario` → `aguardando-respostas` → `orcamentos-recebidos` → `comparacao` → `contratado` → `concluido`.

Também podem existir `pausado`, `cancelado` ou `indisponivel`.

**Nunca avançar estado com base em suposição.** A preparação dos links não significa mensagem enviada. A pesquisa não significa serviço contratado.

## Padrão para novos arquivos

Para cada serviço mencionado pela primeira vez:
- Criar `servicos/<slug-curto>/PEDIDO-ORCAMENTO.md`, baseado em [MODELO-PEDIDO-ORCAMENTO.md](MODELO-PEDIDO-ORCAMENTO.md).
- Nome do serviço, ambiente, descrição e exigências conhecidas.
- Critérios que o fornecedor deverá responder.
- Informações técnicas faltantes, se houver, explicitamente como `a confirmar`.
- Texto de orçamento em **rascunho** (opcional, sempre revisável).
- Não criar empresas, telefones, Instagram ou links WhatsApp por antecipação.
- Incluir data da informação e a indicação `fonte: informado pelo usuário` sem copiar detalhes pessoais.
- Adicionar a linha no índice `ORCAMENTOS-A-PESQUISAR.md` e, se útil, no painel central.

**Deduplicação:** se já existir um arquivo do serviço, atualizá-lo, não criar outro sem necessidade. Se houver mais de uma contratação independente na mesma categoria, diferenciar por escopo.

## Estrutura de documentação

- `CONTINUIDADE-ORCAMENTOS.md`: regras de trabalho entre chats.
- `ORCAMENTOS-A-PESQUISAR.md`: serviços levantados, ainda sem pesquisa completa.
- `MODELO-PEDIDO-ORCAMENTO.md`: modelo para arquivo individual.
- `servicos/<slug>/PEDIDO-ORCAMENTO.md`: pedido individual em construção.
- `ORCAMENTOS-PREPARADOS.md`: pesquisas de fornecedores e links reais `wa.me`.
- `PROTOCOLO-ORCAMENTOS.md`: método técnico de busca e envio manual.
- `PAINEL-SERVICOS.md`: gestão de status e respostas.

## Política de privacidade — ESSENCIAL

O repositório `Gustpbbr/Gus` está **público**. Guardar **somente** procedimento e descrição genérica dos serviços. Não escrever aqui endereço exato, unidade, fotos internas, detalhes de segurança, dados pessoais, orçamentos privados, contratos, números pessoais ou chaves.

Se os dados recebidos forem sensíveis, omitir/redigir do Markdown público, avisar o usuário e propor um repositório **privado** para o segundo cérebro completo. Não publicar dados sensíveis mesmo que tenham sido mencionados no chat.

## Limitação real do ChatGPT

**Nenhum arquivo do GitHub é carregado automaticamente em uma conversa nova.** É necessário que o conector esteja disponível e que o assistente de fato abra os arquivos. Não afirmar leitura sem ter consultado o GitHub.

Comando robusto para começar em outra aba:

> Consulte o GitHub `Gustpbbr/Gus`, pasta `projetos/Apto Copacabana`. Leia `CONTINUIDADE-ORCAMENTOS.md`, `ORCAMENTOS-A-PESQUISAR.md` e `ORCAMENTOS-PREPARADOS.md` antes de responder. Quero continuar a lista de orçamentos do apartamento.

Se os arquivos não estiverem acessíveis, explicar a limitação e pedir o conteúdo necessário; **não reconstruir o projeto de memória ou suposições**.
