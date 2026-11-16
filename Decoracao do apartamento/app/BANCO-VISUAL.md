# Atlas do Apartamento — banco visual interativo (MVP 1.0)

**Código:** [banco-visual.html](banco-visual.html)  
**Data:** 2026-11-16  
**Privacidade:** o código é público, mas os dados de apartamento são privados e **não** foram gravados neste repositório.

## Objetivo

Um mapa de fotografias vinculadas à planta do apartamento, com galerias filtradas por ambiente, cadastro de parede/ângulo, notas, status de origem e cópias exportáveis. O aplicativo funciona em um único HTML estático. As imagens ficam apenas no dispositivo em IndexedDB; **não há sincronização automática** com Google Drive nem upload automático ao GitHub.

## Abrir no computador ou celular

1. No GitHub, abra `banco-visual.html` e use **Download raw file** para salvar o arquivo.
2. Abra esse HTML com Chrome/Edge, conectado à internet para carregar as bibliotecas **PDF.js** e **JSZip** pelas URLs fixas do CDN.
3. Clique em **Importar projeto PDF** e escolha `EXECUTIVO GUSTAVO COPACABANA - OBRA.pdf`. O aplicativo extrairá a planta da página 10, 14 renders das páginas 2–8 e 11 pranchas técnicas de referência, preservados localmente.
4. **Alternativa preferencial para a biblioteca já existente:** baixe `Banco visual Copacabana.zip` da pasta privada **Apartamento Copacabana** no Google Drive. Clique em **Importar pacote ZIP**. O aplicativo lê `plan.jpg` e as 14 fotos em `img/i01.jpg ... i14.jpg`, recuperando os metadados de ambiente, notas e câmeras estimadas do `index.html` do pacote. Importação e extração acontecem no navegador.
5. Use **Adicionar fotos** para incluir imagens reais, sem misturá-las aos renders. Selecione a foto, defina o ambiente e pressione **Salvar ficha**.
6. Para ajustar a câmera, arraste o marcador circular na planta. Para inserir uma posição nova ou deslocar um ponto, use **Posicionar na planta**. O controle deslizante define a direção em graus.
7. Para levar o acervo a outro dispositivo, use **Backup** e, no outro navegador, **Restaurar**. O arquivo JSON exportado **inclui todas as imagens** e deve ser tratado como privado.

## O que está implementado

- Planta navegável com pontos de câmera e direção;
- Galeria com filtros de ambiente, tipo e pesquisa textual;
- Importação client-side de projeto PDF e pacote visual ZIP, mais fotos individuais;
- Associação de fotos com posição na planta, rotação, ambiente, parede e observações;
- Registro da natureza da imagem (foto real, render, simulação, referência, prancha técnica);
- Persistência local via IndexedDB e exportação/restauração JSON;
- Visualização ampliada e exclusão seletiva;
- Código genérico integrado à estrutura existente do projeto de decoração.

## Limitações e cuidados

- **Não existe classificação por IA** neste MVP. As imagens do projeto são catalogadas de acordo com a estrutura conhecida do PDF; as do ZIP recebem os metadados inscritos no pacote. Novas fotos são cadastradas manualmente.
- **Marcadores são estimativas**; o projeto não contém coordenadas de câmera verificadas. Não utilizar a interface como levantamento dimensional ou técnico.
- A importação PDF aceita o executivo com pelo menos 21 páginas, conforme o arquivo fornecido. PDFs de outra arquitetura necessitam de calibração de pranchas e regras de extração.
- A dependência de bibliotecas CDN exige conexão para importar PDF/ZIP. As imagens já guardadas no navegador podem ser vistas offline, mas armazenamento local pode ser apagado pelo navegador ou pelo usuário.
- O editor fotográfico existente em `app/index.html` e o catálogo de materiais permanecem ferramentas separadas; **não foi implementada integração profunda** entre as máscaras do editor e os marcadores do Atlas.
- O Google Drive **não é** acessado diretamente pelo navegador do aplicativo. Para evitar credenciais em código público, o fluxo atual é: baixar da pasta privada → importar arquivo localmente. Uma integração Drive autenticada exige um backend com gestão de acessos.
- Não inserir o PDF executivo, fotos privadas, ZIPs de imagens ou backup com dados pessoais no repositório público `Gustpbbr/Gus`.

## Testes mínimos manuais

1. Abrir HTML, confirmar que a galeria inicia vazia em um navegador novo.
2. Importar o ZIP do Drive e verificar **14 imagens** e planta, com imagens no cômodo correto e pinos tracejados.
3. Selecionar a imagem, editar ficha, alterar ângulo e arrastar pino.
4. Exportar backup; importar novamente em outro navegador e conferir galeria e planta.
5. Importar o PDF de 21 páginas, conferir 14 renders e 11 pranchas técnicas.
6. Testar o celular em modo retrato e paisagem.

## Evoluções propostas

- Login e armazenamento privado sincronizado (Drive ou object storage).
- Classificação de ambientes e paredes por IA com revisão manual.
- Links para variantes e materiais por parede e elemento.
- Múltiplas plantas e versões temporais de obra.
- Calibração em escala de coordenadas e câmera, com visualização 3D vinculada.
