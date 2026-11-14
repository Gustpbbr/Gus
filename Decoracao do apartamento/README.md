# Decoração do apartamento — Plano mestre do simulador

**Versão:** 0.1 — planejamento
**Data:** 2026-11-14
**Status:** arquitetura e requisitos; implementação ainda não iniciada
**Repositório:** `Gustpbbr/Gus` (PÚBLICO)
**Pasta canônica:** `Decoracao do apartamento/`

> **Objetivo:** criar um aplicativo web interativo para experimentar combinações de decoração e reforma, usando fotografias reais, imagens de referência e — quando apropriado — geometria 3D. O usuário seleciona piso, bancada, portas, armários, paredes, colunas, azulejos, louças, metais, cortinas, iluminação ou mobiliário e escolhe entre dezenas de materiais e modelos. Apenas a região selecionada muda. É possível comparar, salvar e exportar versões.

## 1. Organização, integração e segurança

- Esta pasta concentra o **produto digital** (planejamento, especificações, código e evolução do simulador).
- O projeto de **obras, contratações e orçamentos** já existe em `projetos/Apto Copacabana/`; não duplicar seu conteúdo. Consultar `projetos/Apto Copacabana/README.md`, `DECISOES.md` e `PRIVACIDADE.md` quando necessário.
- **Atenção:** este repositório é público. Não armazenar aqui fotografias internas, plantas arquitetônicas detalhadas, vistas que revelem acessos, endereço completo, documentos pessoais, orçamentos identificados, chaves, tokens nem credenciais.
- Criar repositório **privado** ou armazenamento privado com autenticação para imagens originais, máscaras que revelem a planta, desenhos executivos, projetos de marcenaria, configurações específicas do imóvel e arquivos de usuário. O site público, se existir, não deve expor esses ativos.
- O versionamento público pode conter apenas **código genérico, dados sintéticos de exemplo, documentação sem detalhes sensíveis e modelos abstratos**. Evitar fotos do imóvel em screenshots, commits, logs e issues.
- Separar as decisões confirmadas pelo usuário das sugestões, estudos e resultados simulados.
- Conectar um catálogo de produtos só após validar direitos de uso das imagens/texturas e política dos fornecedores.
- Não criar deploy, serviço pago, domínio, autenticação externa ou publicação de imagens reais sem autorização específica.

## 2. Formato recomendado

**Aplicativo web responsivo, preparado para PWA**, acessível no computador e no smartphone. Primeiro um editor 2D fotográfico com camadas, máscaras e perspectivas calibradas; depois, se houver necessidade, módulo 3D/híbrido para objetos, layout, abertura de portas e novas câmeras.

**Por que:** a fotografia preserva detalhes do imóvel que um 3D apressado perderia; o 3D, em contrapartida, permite alterar geometria e ponto de vista. A solução híbrida combina as vantagens progressivamente.

**Alternativas:** site de catálogo estático (insuficiente para edição), app nativo Android/iOS (complexidade prematura), 3D puro (alto custo de modelagem), edição somente com IA generativa (baixa determinabilidade e potencial de distorcer superfícies não solicitadas).

## 3. Capacidades técnicas que o projeto exige

### 3.1. Arquitetura, design e especificação

- Leitura de plantas, elevações, cortes, cotas e imagens arquitetônicas.
- Classificação dos elementos: existentes, previstos no executivo, já executados, hipóteses e propostas descartadas.
- Estudo de estilos: contemporâneo, Japandi, escandinavo, tropical brasileiro, retrô, industrial leve, minimalista, orgânico e combinações.
- Colorimetria: temperatura, subtons, contraste, saturação, incidência da luz, materiais foscos/brilhantes e harmonia entre ambientes.
- Materiais: pedras naturais e industrializadas, porcelanatos, cerâmicas, madeiras, MDF, laminados, tintas, papéis de parede, tecidos, metais e louças.
- Critérios práticos: desempenho em umidade, limpeza, resistência, manutenção, dimensionamento, circulação e custo.
- Recomendações justificadas; indicar claramente as premissas que dependem de medição ou de profissional habilitado.

### 3.2. Imagens e fidelidade geométrica

- Importar fotos originais em resolução adequada, mantendo arquivo-matriz **imutável**.
- Cadastrar câmeras/vistas do mesmo cômodo; distinguir foto real, render do executivo e simulação.
- **Máscaras por região**: piso, bancada, rodabanca, paredes separadas, colunas, azulejos, rejuntes, armários por porta/módulo, eletrodomésticos, cubas, metais e elementos decorativos.
- Desenhar, ajustar e versionar máscaras com polígonos vetoriais (SVG) e/ou raster alfa, com identificação única e hierarquia.
- Modelar planos aproximados e perspectiva: quatro cantos, pontos de fuga, homografia, orientação das réguas/placas, escala de textura, azulejos e rejuntes.
- Tratar oclusão e sobreposição (ex.: torneira à frente da parede, gabinete à frente do piso, cuba sobre bancada).
- Compor textura sem alterar regiões não selecionadas, preservando contornos, sombras, brilho, iluminação e perspectiva tanto quanto possível.
- **Modo de validação visual:** alternância antes/depois, sobreposição semitransparente, zoom, grade, detecção de vazamento de máscara e comparação por diferença.
- Permitir retoque/correção manual das regiões; segmentação automática apenas como auxílio, não como verdade definitiva.
- Preservar paginação, quantidade de fileiras, formas, proporções e textura original quando o usuário não solicitar mudança.
- Toda edição deve registrar versão, máscara, material, parâmetros e imagem base, possibilitando reversão determinística.

### 3.3. Materiais e catálogo

- Categorias: pisos, revestimentos de paredes, rodapés, bancadas, frontões, armários, MDF, metais, louças, eletrodomésticos, cortinas, persianas, papel de parede, ventiladores, iluminação, decoração e mobiliário.
- Cada item com: ID, nome, marca, modelo, coleção, família de cor, foto/texture sample, tamanho físico, acabamento (polido/fosco/acetinado), espessura, orientação, preço e data, fornecedor/link, licença de imagem e observações.
- Cadastrar dezenas ou centenas de alternativas por categoria, com filtro por cor, preço, material, acabamento, resistência e estilo.
- Distinguir `textura real do fabricante`, `foto comercial`, `aproximação visual` e `material gerado`.
- Importação controlada de arquivos e cadastramento manual. Não copiar em massa imagens sem permissão.
- Preços e disponibilidade são mutáveis: mostrar fonte, consulta e data; não afirmar estoque atual sem verificação.

### 3.4. Editor interativo

- Home com ambientes; selecionar ambiente e vista.
- Clique/toque na imagem para selecionar a superfície; destaque temporário da região.
- Painel de opções por elemento com miniaturas, filtro, busca, favoritos e variações.
- Aplicação da mudança em tempo quase imediato para cores/texturas 2D já preparadas.
- Controles: zoom, mover, desfazer/refazer, restaurar original, bloquear regiões, alternar luz simulada quando implementado.
- Permitir alterar individualmente cada face de parede, coluna e módulo de armário, sem alterar os demais.
- Modo comparar A/B com divisor, duas colunas e alternância original/simulado.
- Salvar projeto/versão com nome, data, materiais selecionados e vistas.
- Exportar PNG/JPEG da vista e PDF/CSV com memorial de escolhas, medidas estimadas e links de referência.
- A interface deve funcionar com mouse e toque; preservar controles de precisão e ter acessibilidade básica.

### 3.5. Objetos e geometria

- Mudanças de **cor e textura sobre geometria fixa**: objetivo do MVP.
- Substituição de objetos (cuba, torneira, geladeira, cooktop, ventilador, cortina, móveis): exigir recortes e variantes preparadas, imagens em perspectiva compatível ou modelos 3D.
- Mudanças de tamanho, posição ou forma de mobiliário: modo geométrico/3D; uma máscara 2D sozinha não consegue gerar uma geometria verdadeira.
- Calibração métrica com cotas comprovadas, nunca inferir milímetros exatos apenas de uma foto.
- Futuro: abertura de portas, verificação de colisões, circulação, alturas, vista superior e passeio virtual.

### 3.6. Pesquisa, curadoria e orçamento

- Pesquisa de fabricantes e produtos reais no Brasil, quando solicitada, com links e fontes.
- Comparação técnica e estética das alternativas e recomendações explicadas.
- Associação das áreas de superfície aos quantitativos do executivo ou medições confirmadas.
- Cálculo estimativo de peças, perdas, materiais e faixas de custo; separar material de mão de obra.
- Exportar lista de compras e memorial descritivo, deixando claro o que foi apenas simulado.

### 3.7. Assistente inteligente dentro do aplicativo (fase futura)

- Consulta conversacional: “mostre bancadas bege com armários Freijó” ou “compare A e B”.
- Sugestões de paletas e cenários, com explicação dos contrastes.
- Busca de produtos compatíveis, filtrando por dimensões e acabamentos.
- Auditoria de coerência entre ambientes e detecção de combinações tecnicamente inadequadas.
- Ações de edição por linguagem natural apenas com validação visual, controle de escopo, confirmação de operações destrutivas e histórico.
- **A IA não deve declarar que uma renderização é fotograficamente exata se apenas aproximou textura, iluminação ou geometria.**

## 4. Capacidade real da IA e dependências

| Capacidade | Disponibilidade / condição |
|---|---|
| Ler o projeto executivo e discutir métricas/estética | Possível com o arquivo fornecido; medições críticas precisam de conferência local |
| Criar especificações de software e código | Possível nas ferramentas autorizadas disponíveis |
| Criar e atualizar MDs/código no GitHub conectado | Possível conforme permissões do conector; cada operação precisa ser verificada |
| Sugerir paletas e materiais | Possível; códigos/marcas devem ser conferidos |
| Preparar máscaras 2D e transformações de imagem | Viável por desenvolvimento e revisão; não é automaticamente perfeito |
| Renderizar substituições rápidas de material | Viável depois de implementar e calibrar motor e máscara |
| Criar recortes realistas de novos objetos | Possível com tratamento 2D/3D e/ou modelos preparados; não garantido para qualquer foto |
| Criar modelo 3D navegável preciso | Viável como projeto de modelagem; exige geometria e referências adequadas |
| Hospedar app e controlar infraestrutura | Depende de configuração, permissões, segurança e autorização do usuário |
| Pesquisa de produtos e preços atualizados | Depende de acesso a fontes externas e validação no momento |
| Trabalho autônomo permanente entre conversas | **Não presumir**; requer automações/serviços explicitamente configurados |

**Limites importantes:** IA pode errar na segmentação de superfícies, na percepção de cores e na escala de materiais; imagens geradas são hipóteses visuais, não projetos executivos; alterações elétricas/estruturais exigem profissionais responsáveis.

## 5. Arquitetura preliminar de software

- **Frontend:** TypeScript + React + Vite; interface responsiva com componentes acessíveis.
- **Composição 2D:** Canvas/WebGL conforme desempenho; React Konva ou PixiJS como candidatos a testar.
- **Máscaras:** SVG/polígonos para contornos editáveis, alfa raster para limites complexos; armazenar referência e versão.
- **Texturização:** mapeamento de plano por homografia/WebGL, resolução controlada, orientação e paginação, máscaras de oclusão e composição preservando detalhes da foto.
- **Estado e projetos:** JSON versionado; persistência local para protótipo sem dados pessoais e backend autenticado para uso entre dispositivos.
- **Catálogo:** JSON/SQLite no protótipo; banco de dados no backend se crescer.
- **3D futuro:** Three.js ou Babylon.js a validar em prova de conceito; formatos glTF/GLB.
- **Testes:** unitários (transformações e catálogo), visuais de regressão, integração e responsividade.
- **Deploy:** protótipo com dados sintéticos em hospedagem estática; versão real privada com autenticação, controle de acesso e armazenamento protegido.
- **Segredos:** variáveis de ambiente no provedor; nunca credenciais no Git ou código cliente.

A escolha final das bibliotecas exige protótipo de desempenho, sobretudo em celular e com imagens grandes.

## 6. Modelo de dados conceitual

- `Apartment` — conjunto de ambientes sem identificar publicamente o imóvel.
- `Room` — ambiente, características gerais, vistas disponíveis.
- `View` — fotografia/render, origem, licença, largura/altura, câmera e versão.
- `Surface` — ID estável, tipo, geometria/máscara, plano, escala, prioridade de camada, condição existente/projetada.
- `Mask` — polígono SVG ou imagem alfa, revisão, dependências, validador.
- `Material` — ID, fabricante, modelo, categoria, variação, texture URL privada/licenciada, escala física, acabamento, fonte.
- `ObjectVariant` — versão de objeto, dimensões, origem da imagem/modelo e ângulos suportados.
- `Selection` — superfície -> material/variante + parâmetros; representação independente da foto.
- `Scenario` — conjunto de seleções com nome, status, data, ancestral e notas.
- `Measurement` — valor, unidade, origem (executivo/levantamento/estimativa), grau de confiança.
- `PriceObservation` — preço, unidade, loja, data, URL, condições e observações.
- `Decision` — proposta vs. decisão confirmada; histórico sem sobrescrever decisões anteriores.

## 7. Fases do projeto e entregas

### Fase 0 — Base, privacidade e inventário (primeira)

- [ ] Definir onde ficarão fotos, plantas, máscaras e dados sensíveis **em repositório/armazenamento privado**.
- [ ] Selecionar foto-matriz e vista da cozinha, guardadas fora do Gus público.
- [ ] Inventariar assets: formatos, resolução, diferentes perspectivas e permissões de uso.
- [ ] Separar o que é existente, render da arquiteta e simulação.
- [ ] Definir medidas confiáveis e registrar lacunas.
- **Aceite:** existe um inventário consistente sem publicar nenhuma imagem interna.

### Fase 1 — Prova de conceito com imagem sintética

- [ ] Criar frontend com seleção de ambiente e vista de demonstração.
- [ ] Definir 4–6 regiões editáveis em **imagem sintética**, com máscaras independentes.
- [ ] Trocar cores, texturas e manter pixels não selecionados inalterados.
- [ ] Implementar antes/depois e restaurar original.
- **Aceite:** clique, troca, reset e comparação funcionam no desktop e celular.

### Fase 2 — Cozinha real (MVP privado)

- [ ] Calibrar foto da cozinha e validar as regiões: piso, bancada, armários, paredes, coluna e revestimento.
- [ ] Criar ferramenta de ajuste manual de máscaras, zoom e depuração.
- [ ] Cadastrar catálogo inicial real: pelo menos 10 opções de bancada, 10 pisos, 10 armários e 10 acabamentos de parede.
- [ ] Aplicar textura em perspectiva, com escala e orientação ajustáveis.
- [ ] Salvar cenários A/B/C e exportar imagem.
- **Aceite:** a alteração de uma categoria não deforma nem muda visualmente nenhuma outra região; avaliação visual aprovada pelo usuário.

### Fase 3 — Produto utilizável

- [ ] Implementar filtros, favoritos, pesquisa e importação de materiais.
- [ ] Suportar múltiplas vistas do mesmo ambiente com mapeamentos próprios.
- [ ] Persistir projetos em conta privada e sincronizar entre dispositivos.
- [ ] Histórico de decisões, desfazer/refazer, cópia e nomeação de versões.
- [ ] Gerar memorial de materiais e lista de especificações.
- **Aceite:** usuário consegue testar opções e retomar projeto salvo sem assistência técnica.

### Fase 4 — Outros ambientes e orçamento

- [ ] Cadastrar banheiro, sala, quarto, hall e área de serviço.
- [ ] Expandir catálogo: louças, metais, eletrodomésticos, papéis, cortinas, persianas, luminárias, ventiladores e móveis.
- [ ] Conectar quantitativos e faixas de preços com fontes e datas.
- [ ] Checar continuidade entre paletas dos ambientes.
- **Aceite:** versão por ambiente e visão integrada de materiais escolhidos.

### Fase 5 — Geometria, 3D e IA assistida

- [ ] Testar importação/criação de modelo 3D calibrado.
- [ ] Permitir trocar objetos completos, dimensões e posições dentro de limites geométricos.
- [ ] Implementar visualização navegável e comparação 2D/3D.
- [ ] Adicionar pesquisa e comandos conversacionais com confirmação e controle de escopo.
- **Aceite:** mudanças de objetos e posições respeitam dimensões conhecidas e limitações explicitadas.

## 8. Experiência de uso desejada

1. Abrir aplicativo -> selecionar **cozinha**.
2. Selecionar foto ou vista; ver referência original sem filtros.
3. Tocar em “bancada” -> catálogo com pedra, cor, textura, preço e fonte.
4. Escolher material -> visualizador muda **somente** a bancada.
5. Tocar no piso -> escolher material e paginação; atualizar a mesma cena.
6. Escolher armário inferior, aéreo, parede e coluna de forma independente.
7. Salvar “Alternativa A”; duplicar para “Alternativa B” e fazer outras escolhas.
8. Comparar A x B ou cada uma x original.
9. Exportar visual e memorial para conversar com fornecedores.
10. Reabrir e continuar de onde parou, com decisões confirmadas destacadas.

## 9. Qualidade, testes e critérios de fidelidade

- **Regra de ouro:** fora da máscara ativa, não deve haver alteração de pixels na camada de composição 2D (salvo efeitos de luz/sombra explicitamente autorizados).
- Máscaras devem respeitar as bordas das paredes, contornos de objetos e regiões vazadas, sem halos visíveis em zoom.
- Manter o original íntegro e permitir retorno perfeito a ele.
- Ladrilhos e réguas têm dimensões físicas conhecidas; aplicar repetição correta em perspectiva.
- Preservar objetos sobrepostos e juntas, inclusive em mudanças pontuais.
- Registrar quando não há textura fidedigna: não inventar a aparência exata de um produto.
- Testar em celular Android e desktop, telas pequenas, imagens pesadas e conexões lentas.
- Criar imagens de teste sintéticas para testes automatizados; não colocar fotos privadas no repositório público.
- Testes visuais de regressão: captura original, máscara, composição, diferença e relatório das áreas afetadas.

## 10. Estrutura futura pretendida

```text
Decoracao do apartamento/
├── README.md                 # Este plano mestre
├── docs/                     # Requisitos, arquitetura, decisões técnicas e critérios de QA
├── catalogo-exemplo/         # Dados sintéticos e públicos/licenciados
├── app/                      # Frontend web
├── tests/                    # Testes automatizados com imagens fictícias
└── PRIVACIDADE.md            # Regras específicas, quando necessário
```

**Fora deste repositório público:** `assets-reais/` (fotografias, planta executiva, máscaras, arquivos métricos, materiais privados, projetos salvos e dados do usuário). Preferir local privado com backup, autenticação e controle de acesso.

## 11. Prioridades, riscos e decisões pendentes

**Prioridade 1:** provar que troca individual de materiais sobre uma foto calibrada funciona sem corromper o restante.

**Riscos principais:** máscaras imperfeitas, perspectiva/texturas irreais, fotos em resolução baixa, diferenças de iluminação entre vistas, custos de preparação por ângulo, direitos autorais de texturas e vazamento de arquivos do imóvel.

**Decisões pendentes (não presumir):** provedor privado de assets, plataforma de hospedagem protegida, acesso de convidados, política de backup, nível de fidelidade exigido e licença de imagens de fabricantes.

**Regra de continuidade:** em conversas futuras, ler primeiro este README e as alterações posteriores antes de desenvolver. Verificar operações reais no GitHub; não alegar implementação, deploy ou leitura de arquivos sem confirmação.

---

**Próximo passo concreto:** criar projeto demonstrativo com imagem fictícia e regiões editáveis, ao mesmo tempo que se define armazenamento privado e o inventário das fotografias reais. Só então integrar a foto-matriz e a biblioteca de materiais do apartamento.
