# Biblioteca de imagens reais e produtos — Ateliê do Apartamento

**Atualização:** 2026-11-14 · **Versão:** 1.0 (inventário inicial)  
**Inventário:** 163 referências reais de produtos, padrões comerciais e pedras, em 10 categorias.  
**Pré-visualizações externas cadastradas:** 17; os outros registros abrem a **página/galeria da fonte** e NÃO exibem miniatura inventada.

## Como usar
- `galeria.html`: catálogo visual responsivo em um único arquivo, com busca, filtros e links para galerias reais. Baixe o HTML e abra no navegador. As miniaturas externas requerem internet.
- `catalogo.json`: dados estruturados, aptos a integrar o futuro editor 2D e a cozinha 3D.
- `catalogo.js`: mesma base como `window.GUS_CATALOGO`, para páginas HTML abertas localmente sem `fetch(file://...)`.
- `FONTES_E_DIREITOS.md`: fontes, metodologia e direitos de imagem.

## Princípios
1. **Produto real != fotografia reutilizável**. Catálogos e fotos comerciais são de seus titulares. No GitHub público, somente referências e links; nunca fazer upload de imagens protegidas sem licença explícita.
2. **Foto, render, textura e amostra** não são intercambiáveis. As amostras do fabricante podem ter diferenças perceptíveis da pedra ou da chapa real. A textura útil para perspectiva deve ser preparada, calibrada e preferencialmente licenciada.
3. **Público e privado separados.** Nada de fotos internas do apartamento, documentos executivos, máscaras específicas do imóvel, endereços ou segredos neste repositório público.
4. **Disponibilidade não é verificada**; consultar loja, medidas, tensão, estoque e preço na data de compra.
5. **Produto exato vs. página da coleção.** Nem toda referência possui URL individual. `paginaFonte` pode abrir uma coleção oficial que permite localizar o padrão pelo nome.
6. **Sem automação de scraping/hotlink em massa.** O sistema futuro deve respeitar licenças, limites e condições de uso dos sites.
7. **Categorias futuras:** papel de parede tropical, persianas e blackouts, portas de correr, ferragens, tecidos, ventiladores, ar-condicionado, iluminação, rodapés, espelhos, fechaduras, móveis e acessórios. Adicionar somente após encontrar referências documentadas.

## Padrão de campos (`catalogo.json`)
`id`, `categoria`, `nome`, `marca`, `linha`, `familiaCor`, `formato`, `acabamento`, `ambientes`, `tipo`, `paginaFonte`, `imagemExterna`, `creditoImagem`, `classificacaoImagem`, `integracao`, `licencaParaRepublicacao`, `validadoEm`, `observacoes`.

Uma miniatura com `imagemExterna` **não significa autorização de reprodução**. Antes de transformar em texturas hospedadas, solicitar permissão ou usar ativos abertamente licenciados, mantendo atribuição.

## Integração com app
O editor existente em `../app/index.html` usa padrões ilustrativos independentes. Este banco **ainda não altera automaticamente** imagens nem transforma os produtos em mapas PBR. Próxima integração: filtros por região, seleção da textura preparada, escala, orientação, paginação, máscara e exportação com material/série vinculados.

## Contagem por categoria

- Pedras naturais e bancadas: 10
- Pisos e porcelanatos: 18
- Revestimentos de parede: 18
- MDF e painéis de madeira: 72
- Tintas e cores: 18
- Metais de cozinha: 8
- Metais de banheiro: 8
- Cubas de cozinha: 2
- Cubas de banheiro: 8
- Eletrodomésticos: 1

## Fontes gerais
- Portobello: https://www.portobello.com.br/revestimentos/linha/gouache
- Portobello concretos: https://www.portobello.com.br/revestimentos/concretos?channel=multimarcas&view=produtos
- Duratex Inspira: https://duratex.com.br/inspira/inspiracoes
- Duratex BIM: https://www.downloads.duratexmadeira.com.br/
- Docol cozinha: https://www.docol.com.br/br/monocomando/cozinhas/monocomandos?map=ft%2Ccategory-1%2Ccategory-3&page=1
- Docol banheiro: https://www.docol.com.br/br/banheiros/torneiras-e-misturadores/monocomandos
- Deca cubas: https://www.deca.com.br/ambientes/banheiro-e-lavabo/cubas-para-banheiro/cuba-de-apoio
- Coral paleta: https://www.coral.com.br/pt/paletas-de-cor/filters/globalId_a4feea61-0a9b-4554-9c52-a340009e0e9d
- Tramontina cubas: https://www.tramontina.com.br/

Consulte `FONTES_E_DIREITOS.md` para detalhes.
