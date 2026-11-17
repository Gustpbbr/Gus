# Índice integrado — Apto Copacabana

**Inventário iniciado:** 2026-11-17  
**Estado:** inventário parcial verificado por leitura direta de GitHub e Google Drive.  
**Escopo:** documentação de gestão, orçamento e ferramentas visuais.  
**Privacidade:** este arquivo está em repositório público; não incluir dados pessoais, endereço completo, imagens internas, plantas, contratos, notas fiscais ou detalhes de segurança.

## 1. Pontos de entrada existentes

### A. Gestão da reforma — pasta atual
- [README — guia de entrada](README.md)
- [Lista oficial 01–19 de serviços](ORCAMENTOS-A-PESQUISAR.md)
- [Painel de serviços](PAINEL-SERVICOS.md)
- [Orçamentos preparados](ORCAMENTOS-PREPARADOS.md)
- [Continuidade de orçamentos](CONTINUIDADE-ORCAMENTOS.md)
- [Protocolo de orçamentos](PROTOCOLO-ORCAMENTOS.md)
- [Registro de decisões](DECISOES.md)
- [Política de privacidade](PRIVACIDADE.md)
- [Grupos de contratação](grupos/)
- [Serviços individuais e atalhos](servicos/)

A lista oficial documenta 19 serviços numerados, base de 16 itens iniciais mais 17–19 adicionados em 2026-11-08. Os grupos e os documentos individuais não devem ser recriados sem necessidade; seguir os links canônicos do índice de serviços.

### B. Decoração, catálogo e aplicativos — pasta já existente
- [Plano mestre do simulador](../../Decoracao%20do%20apartamento/README.md)
- [Atlas visual e manual](../../Decoracao%20do%20apartamento/app/BANCO-VISUAL.md)
- [HTML do Atlas](../../Decoracao%20do%20apartamento/app/banco-visual.html)
- [Editor 2D](../../Decoracao%20do%20apartamento/app/index.html)
- [Protótipo 3D](../../Decoracao%20do%20apartamento/app/cozinha-3d.html)
- [Catálogo de materiais](../../Decoracao%20do%20apartamento/catalogo/README.md)

O README do catálogo declara 240 referências; total não recontado neste inventário. As simulações são estudos, não desenhos executivos ou medidas verificadas.

### C. Google Drive — acervo privado
Foram localizadas duas pastas acessíveis, com propósitos diferentes:
- **Apartamento Copacabana**: pacotes ZIP visuais privados (um com cerca de 1,6 MB e outro com cerca de 33,3 MB). O conteúdo interno, a integridade e a equivalência entre eles ainda não foram confrontados.
- **Apto Copacabana**: cópias dos arquivos Markdown de gestão, grupos e subpastas dos serviços 01–19.

**Não inserir no GitHub público links diretos para acervo privado, IDs, imagens, plantas ou dados pessoais.** Guardar identificadores e inventário integral de mídias exclusivamente no Drive privado.

## 2. Comprovações e ressalvas em 2026-11-17

- Confirmada por listagem determinística a existência das pastas e arquivos principais acima.
- O arquivo `ORCAMENTOS-A-PESQUISAR.md` foi lido em GitHub e Drive e teve conteúdo textual exatamente igual na comparação realizada. **Isso não comprova sincronização automática**, nem igualdade das demais cópias.
- O `DECISOES.md` consultado é um modelo inicial e não deve ser tomado como registro completo de escolhas posteriores.
- O Atlas registra armazenamento local (IndexedDB) e exportação/restauração manual; sem sincronização automática com Drive.
- O PDF executivo mencionado no manual do Atlas **ainda não foi confirmado como arquivo separado** dentro dessas duas pastas do Drive. Não interpretar isso como prova de ausência em todo o Drive.
- A documentação de gestão foi revisada pela última vez em novembro de 2026, podendo conter estados de fornecimento/compra desatualizados.
- Não foi feito levantamento técnico de campo, validação dimensional ou comparação integral do acervo visual.

## 3. Política de fonte da verdade

| Informação | Fonte primária | Regra |
|---|---|---|
| Plantas, fotos originais, documentos técnicos e contratos | Drive privado / original identificado | Verificar revisão, autoria e integridade |
| Serviços e andamento documentado | Arquivos canônicos desta pasta, após confirmação | Não inferir contratação a partir de pesquisa |
| Alternativas de materiais e simulações | Catálogo / aplicativo de decoração | Não tratar simulação como material comprado |
| Orçamentos, cotações e pagamentos | Documento formal ou planilha privada vinculada | Fonte e data obrigatórias |
| Decisões | Registro explícito com aprovação | Sugestões e conversas não são aprovação |
| Cotas e quantitativos | Planta técnica aprovada + conferência profissional | Toda extração automatizada nasce pendente |

Estados mínimos: **documentado / observado / inferido / pendente / aprovado / substituído**.

## 4. Próxima rodada de inventário

1. Conferir os dois ZIPs visuais: estrutura interna, origem e eventuais duplicatas.
2. Localizar e classificar todas as versões do projeto executivo e plantas de levantamento/demolição/proposta; não inventar a versão vigente.
3. Identificar fotos reais, renders, simulações, referências e pranchas sem misturar as classes.
4. Comparar os demais MDs entre GitHub e Drive para verificar se são cópias idênticas, divergentes ou antigas.
5. Consolidar um índice **privado** no Drive, com IDs, URLs, revisões, hash/tamanho quando possível e estado da validação.
6. Separar escolhas já aprovadas de materiais ainda em estudo; preencher o registro de decisões somente após verificação.
7. Definir planilha de controle de serviços, cotação, compras e pendências — sem substituir os documentos existentes.

## 5. Regras de alteração

- Não mover, apagar, renomear nem sobrescrever originais durante o inventário.
- Nunca publicar fotos internas, endereço completo, notas, propostas privadas ou plantas no Gus público.
- Todo novo registro deve conter fonte, data, responsável pela conferência e estado.
- Se houver conflito de versões, marcar **PENDENTE**; não escolher por dedução.
- A aprovação técnica e a liberação de serviços cabem a profissionais habilitados.
- Nas próximas conversas, ler os arquivos canônicos relevantes antes de afirmar um estado atualizado.

## 6. Alertas de revisão de escopo (não corrigir sem validação)

- O item 05 da lista oficial ainda está nomeado como **split 18.000 BTU/h**. O dimensionamento e a seleção final precisam ser conferidos antes de transformar o item em especificação fechada.
- O item 11 ainda descreve adaptação do banheiro para **lavadora Brastemp convencional de 8 kg**. Esse cadastro pode estar superado pelo planejamento de **lava e seca**; revisar escopo hidráulico, elétrico e dimensional com base na escolha atual e em documentos de suporte.
- Os estados `links-prontos`, `pesquisa-concluida` ou `aguardando-pesquisa` refletem o arquivo consultado, datado de 2026-11-08. Não significam orçamento recebido, compra, contratação ou execução.
- A lista 01–19 é uma **lista de serviços a orçar**, não substitui a EAP completa da obra, inspeções, dependências, licenças, comissionamento, limpeza final e entrega.
