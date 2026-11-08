# Protocolo de pesquisa de fornecedores e orçamento via WhatsApp

**Versão:** 1.0 — 2026-11-08
**Escopo:** serviços para o apartamento em Copacabana, RJ (região prioritária: Copacabana e Zona Sul).
**Modo de operação:** ChatGPT + pesquisa na web + links oficiais para WhatsApp; **não** exige WhatsApp Business API.

## Regra prioritária: orçamento já preparado

Antes de pesquisar novamente, ler [ORCAMENTOS-PREPARADOS.md](ORCAMENTOS-PREPARADOS.md). Se houver arquivo do serviço solicitado, **apresentar os links finais armazenados** no arquivo específico e não gastar uma nova pesquisa nem refazer o texto, salvo se o usuário pedir atualização ou detectar erro. O gatilho **"quero o orçamento pro gás"** aponta para [servicos/gas/ORCAMENTO-GAS-2026-11-09.md](servicos/gas/ORCAMENTO-GAS-2026-11-09.md).

**Não presumir acesso automático ao GitHub em novas conversas.** É obrigatório realmente ler os arquivos antes de afirmar que os links estão preparados.

## 0. Resultado esperado

Quando o usuário solicitar um serviço ou disser "preciso fazer orçamentos":

- Localizar **pelo menos 5 fornecedores independentes**, sempre que houver opções verificáveis. Não inventar opções para atingir o número.
- Apresentar nome, especialidade, região atendida, telefone e **site oficial verificado**; se houver, **Instagram comercial**.
- Criar **para cada fornecedor** um link clicável que abra o WhatsApp com o **destinatário e o texto já preenchidos**, faltando somente o toque humano em **Enviar**.
- Citar fontes e declarar o que foi verificado e o que é apenas alegação comercial.
- Preparar orçamento comparável (mão de obra, materiais, visita, prazo, garantia, condições e segurança).
- Nunca alegar que enviou mensagens, leu respostas ou testou o celular do usuário.

## 1. Levantamento de requisitos

1. Interpretar tipo de serviço e especialidade: gás, hidráulica, elétrica, janelas acústicas, marcenaria etc.
2. Usar contexto prévio disponível do apartamento, **sem presumir** que outro chat ou outro arquivo foi carregado.
3. Região padrão do projeto: Copacabana / Zona Sul do Rio de Janeiro. Não compartilhar o endereço completo com prestadores sem autorização do usuário.
4. Perguntar só quando faltar um dado indispensável; senão prosseguir e declarar hipóteses.
5. Para serviços técnicos, levantar exigências de segurança e necessidade de visita técnica.

## 2. Fontes e busca ampla

Pesquisar em fontes complementares:
- Site oficial, página de contato e links publicados pelo fornecedor.
- Mecanismos de busca, perfis empresariais e diretórios relevantes.
- Instagram **público**: perfil comercial, biografia, posts indexados, portfólio acessível e botão público de contato, quando ferramentas permitirem.
- Fabricantes e listagens de assistência/instaladores autorizados, se aplicável.
- Plataformas de avaliações e reclamações, com cautela sobre datas e amostras.

**Transparência Instagram:** busca via web por perfis não equivale a navegar autenticado dentro do Instagram. Se a página exigir login, não afirmar que verificou posts, atividade recente ou comentários. Link de perfil encontrado em outro site deve ser identificado como "perfil divulgado em fonte externa", não "perfil auditado".

**Critérios de seleção:** compatibilidade com serviço, atendimento geográfico, meios de contato, credenciais/segurança quando aplicáveis, evidência pública; não confundir anúncios com avaliações independentes.

## 3. Conferência de identidade e links

Para cada empresa:
1. Encontrar o domínio **real** citado em fonte oficial/autorrepresentação. Abrir e conferir o destino; não inventar URL baseada no nome.
2. Conferir o perfil Instagram publicado pela empresa ou indicado de modo verificável. Não supor @username.
3. Extrair o número **exatamente** como publicado e observar se é WhatsApp confirmado, telefone móvel apenas, ou contato não confirmado.
4. Preferir número do site/perfil oficial a agregadores; se fontes divergirem, explicar.
5. Verificar se presta o serviço pedido e se atende Copacabana; se não for claro, marcar "a confirmar".
6. Evitar franquias, nomes fantasia e filiais duplicadas como fornecedores independentes.

Se não for possível verificar um site, marcar "site não confirmado"; se só houver Instagram, mostrar o Instagram **sem inventar um site**. Se WhatsApp não for publicado, não inventar número.

## 4. Mensagem de orçamento

**Tom obrigatório em todos os serviços:** as mensagens destinadas ao WhatsApp devem ser educadas, naturais e pessoais. Começar com "Olá, tudo bem? Meu nome é [NOME]. Gostaria de solicitar um orçamento..." e terminar com agradecimento. Substituir [NOME] somente no texto final da conversa com o usuário, quando autorizado. O local de execução pode indicar **bairro e rua** no WhatsApp privado quando explicitamente autorizado pelo usuário, mas a versão gravada neste GitHub público deve preservar apenas localização genérica (Copacabana/RJ), sem rua específica ou dados pessoais.

**Não usar a abertura seca "Olá! Quero orçamento..."** nem textos que soem como formulário. Manter, porém, todas as questões técnicas essenciais em linguagem cordial e concisa.



Elaborar mensagem única, curta e objetiva, adaptada ao serviço. Perguntar:
- disponibilidade e atendimento em Copacabana;
- visita técnica presencial e custo da visita;
- preço discriminado de mão de obra, materiais e adaptações;
- prazo, condições de pagamento, garantia e comprovantes;
- documentação/qualificações necessárias em serviços especializados.

Exemplo para gasista:

> Olá, tudo bem? Meu nome é [NOME]. Gostaria de solicitar um orçamento para avaliar a retirada de um aquecedor a gás atualmente instalado dentro do box e sua transferência para um local permitido, em apartamento em Copacabana/RJ. Vocês realizam visita técnica? Se possível, gostaria de saber o valor da avaliação e receber uma proposta que considere ventilação, exaustão, tubulações, testes de segurança, materiais, mão de obra, prazo e garantia. Muito obrigado!

**Segurança:** mudanças em aquecedores a gás dependem de avaliação presencial e atendimento às exigências aplicáveis; não oferecer instruções improvisadas de remanejamento.

## 5. URL técnica do WhatsApp — REGRA CRÍTICA

Formato:

https://wa.me/NUMERO?text=MENSAGEM_CODIFICADA

- NUMERO = código do país + DDD + número, **somente dígitos** (sem +, espaços, traços ou parênteses).
- MENSAGEM_CODIFICADA = texto integral codificado em UTF-8 para componente de URL (equivalente a encodeURIComponent).
- Nunca deixar espaços, acentos, quebras de linha ou caracteres reservados crus no parâmetro text.
- Construir **antes da resposta** um link Markdown final contendo a URL pronta, literal e completa para cada número.
- **Não** usar concatenação/interpolação no destino do link apresentado, porque o cliente pode não renderizá-lo como esperado.
- Não afirmar que a mensagem foi enviada: só o usuário toca em Enviar dentro do WhatsApp.
- O envio será feito a partir da conta WhatsApp escolhida pelo sistema do usuário, não por uma integração direta com sua conta.

**Exemplo ilustrativo** com número fictício 5521999999999:

Mensagem: "Olá! Quero um orçamento."

URL pronta:

https://wa.me/5521999999999?text=Ol%C3%A1%21%20Quero%20um%20or%C3%A7amento.

Markdown clicável (em respostas reais, substituir por número confirmado e mensagem apropriada):

[WhatsApp — Solicitar orçamento](https://wa.me/5521999999999?text=Ol%C3%A1%21%20Quero%20um%20or%C3%A7amento.)

**Não utilizar o exemplo fictício para contactar uma empresa real.**

### Diagnóstico se link falhar

1. Oferecer primeiro o link simples https://wa.me/NUMERO para verificar abertura da conversa.
2. Reexaminar país, DDD, número e URL encoding.
3. Reconstruir URL completa como texto estático clicável, e oferecer alternativa copiável.
4. Se o WhatsApp abrir sem texto, testar uma frase menor e caracteres especiais.
5. Não garantir suporte idêntico em todos os navegadores e versões do aplicativo.

## 6. Apresentação dos resultados

Para cada opção:

**N. Nome comercial**
- **Serviço e adequação:** o que foi efetivamente encontrado.
- **Bairro/área:** confirmação ou ressalva.
- **Site oficial:** link real ou "não localizado".
- **Instagram:** link real ou "não localizado"; especificar grau de verificação.
- **WhatsApp:** número, procedência e estado de verificação.
- **Solicitar orçamento via WhatsApp:** link final, já com texto codificado.
- **Observações:** credenciamento, reputação, visita, segurança; só afirmar o que as fontes suportam.
- **Fontes consultadas:** links/citações.

Adicionar tabela comparativa e mapa quando útil. Não inventar preço, prazo ou disponibilidade.

## 7. Após respostas recebidas

O ChatGPT **não lê automaticamente** as conversas privadas do WhatsApp. O usuário poderá colar respostas ou anexar arquivos. Não presumir acesso a mensagens não trazidas.

Comparar cada proposta: valor total, serviço incluído, itens não incluídos, custos extras, materiais, visita, tempo, garantia, qualificações, método de pagamento, comprovantes. Identificar divergências; criar links para perguntas de esclarecimento no mesmo padrão do item 5.

Atualizar o PAINEL-SERVICOS.md **somente mediante pedido do usuário**, usando escrita autenticada do GitHub e verificação posterior. Não colocar endereço, telefone pessoal, CPF, fotos privadas, propostas completas ou dados financeiros no repositório público.

## 8. Critérios objetivos de conclusão

- [ ] Pelo menos 5 fornecedores diferentes pesquisados ou insuficiência justificada.
- [ ] Empresa e especialidade conferidas.
- [ ] Site correto e Instagram público (quando encontrados), com grau de confirmação.
- [ ] Telefone identificado sem inferência; WhatsApp qualificado como confirmado/não confirmado.
- [ ] Link wa.me estático e final para cada número disponível, com texto pronto.
- [ ] Pedido de orçamento tecnicamente coerente e comparável.
- [ ] Informações de contato, área e reputação fundamentadas.
- [ ] Nenhuma mensagem enviada automaticamente.
- [ ] Usuário informado sobre limitações de acesso ao Instagram e WhatsApp.

## 9. Resumo operacional para novas conversas

"Consulte o GitHub Gustpbbr/Gus, arquivo projetos/Apto Copacabana/PROTOCOLO-ORCAMENTOS.md. Execute a pesquisa de [serviço] seguindo integralmente o protocolo, com ao menos cinco fornecedores verificáveis, site/Instagram e link direto wa.me com o texto pronto."
