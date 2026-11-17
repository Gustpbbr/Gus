# Ateliê do Apartamento — protótipo 0.1

## Atlas — planejamento de perspectivas C01 (2026-11-16)

A página [banco-visual.html](banco-visual.html) agora contém o módulo **Nova perspectiva · C01 · Cozinha**:

- Altura da câmera em centímetros (padrão 110), distância focal em mm equivalente a sensor full-frame de 36 mm (padrão 24) e rumo no plano (padrão 180°).
- Convenção do rumo na planta exibida: 0° para cima, 90° direita, 180° baixo e 270° esquerda. **Não é azimute geográfico**.
- Calculo do campo visual horizontal a partir da focal, sem atribuir automaticamente distância de câmera, escala física ou geometria 3D.
- Toque em **Posicionar C01 na planta**, depois toque no local aproximado da câmera. Um marcador "C" tracejado aparece, separado dos marcadores das fotos.
- Toque em **Salvar parâmetros** para registrar a proposta em IndexedDB local; o backup do Atlas inclui os dados de C01.
- Marcador, altura e direção são **hipóteses de trabalho**, não levantamento técnico nem renderização. Não há geração automática da nova imagem.

**Privacidade:** nenhuma planta, fotografia, posição específica do imóvel ou arquivo de câmera particular fica no código público do GitHub. A posição só é registrada no navegador do usuário e em backups que ele exporta.


## Protótipo 3D autônomo

- **Arquivo:** [cozinha-3d.html](cozinha-3d.html)
- **Instalação:** nenhuma; basta baixar o HTML e abrir no navegador com suporte a CSS 3D.
- **Funções:** girar câmera, zoom por botões e pinça, selecionar categorias/superfícies, trocar pisos/bancadas/armários/parede/revestimento, salvar cenários A e B localmente e exportar escolhas JSON.
- **Limites:** geometria **esquemática**, não calibrada ao executivo; materiais procedurais ilustrativos; não reproduz o apartamento com precisão dimensional e não fornece renderização fisicamente realista.
- **Privacidade:** somente modelos sintéticos no repositório público; fotos e planta detalhada não estão embutidas.

## O que está implementado

Editor web local de fotografias, com uma única página HTML, sem dependências externas e sem servidor.

- Abrir uma imagem a partir do dispositivo.
- Marcar superfícies como polígonos independentes; nomear e selecionar áreas.
- Ajustar os vértices com o mouse ou toque.
- Aplicar cores, seis texturas demonstrativas procedurais ou imagens de textura importadas.
- Controlar opacidade, escala da textura e modos de mistura.
- Comparar antes/depois, ocultar contornos e desfazer/refazer.
- Exportar PNG sem guias visuais.
- Salvar e recuperar as regiões do projeto em arquivo JSON.

**Atenção:** não há modelo 3D, mapeamento projetivo preciso, verificação de escala física, fotorrealismo garantido, catálogo comercial validado ou sincronização automática entre perspectivas. As texturas embutidas são amostras de estudo, não reproduções de produtos.

## Como abrir

1. Baixar `index.html` deste diretório, mantendo extensão `.html`.
2. Abrir o arquivo com um navegador moderno no computador (Chrome, Edge ou Firefox). Não precisa instalar nada.
3. Clicar em **Abrir fotografia** e escolher uma imagem local.
4. Escolher a categoria da superfície, clicar em **Marcar região**, marcar ao menos três pontos no contorno e selecionar **Fechar contorno**.
5. Selecionar a região e aplicar um acabamento; ajustar intensidade e modo de mistura.
6. Salvar a composição como PNG; salvar o projeto como JSON, para retomar os contornos depois.

### Reabrindo um projeto

- Carregar **a mesma fotografia original** para a qual as máscaras foram desenhadas.
- Clicar em **Abrir projeto JSON**.
- Se importar JSON antes de abrir a fotografia, depois selecionar a foto com exatamente o mesmo nome.
- O JSON não inclui a fotografia-base, mas pode incluir texturas privadas incorporadas; tratar o arquivo exportado como confidencial.

## Onde os dados ficam

Toda manipulação de imagem acontece no navegador; esta página não envia fotos a servidor. Não usa biblioteca remota nem CDN. Não grava automaticamente o projeto no GitHub. Os arquivos só saem do dispositivo se o usuário voluntariamente os compartilhar ou armazenar em outro serviço.

O repositório `Gustpbbr/Gus` é **público**. Não adicionar fotografias reais, imagens de interiores, plantas, contornos do apartamento ou projetos JSON aqui.

## Limitações do MVP e próximos marcos

1. **Calibração geométrica**: cada parede e bancada poderá receber plano, escala e perspectiva próprios. Atualmente a textura é repetida em coordenadas 2D do canvas.
2. **Qualidade visual**: máscara de oclusão, contornos suaves, sombras e reflexos coerentes.
3. **Edição de máscara avançada**: zoom e pan de precisão, subtração, furos, agrupamentos e máscaras alfa.
4. **Catálogo real**: inserir fichas de fabricantes, texturas licenciadas e dados de dimensão, marca e linha.
5. **Variantes de objetos**: geometria pré-preparada, modelos 3D e substituição de torneiras, cubas, cooktops etc.
6. **Projetos por cômodo, com múltiplas vistas** e sincronização privada de escolhas.

## Critérios de validação

- A fotografia permanece como camada original; máscaras só modificam áreas selecionadas na imagem de trabalho.
- Exportação sem contornos ou pontos de controle.
- Contornos identificados e reversíveis; desfazer/refazer testável.
- Aplicação de uma cor no piso não altera dados de outra região.
- Não prometer realismo exato de pedra, madeira ou cerâmica com as texturas ilustrativas atuais.

Para planejamento de longo prazo, ver [plano mestre](../README.md).
