---
exportado_em: 2026-05-03T04:44:45
total: 1278
fonte: hub-qdrant
---

# Memórias do Gustavo — Export Hub Qdrant

*Última atualização: 03/05/2026 às 04:44*

1. Os PRs mergeados post 02/05/2026 incluem melhorias no curador e correções de bugs críticos.
   *(2026-05-03)*

2. No projeto, as demandas pendentes se referem a quatro tarefas: captura multiporta curador, drive sync oauth fix, pendências da Claude Chat consolidadas, e um template.
   *(2026-05-02)*

3. O cache de mídia do bot não possui gerenciamento de orçamento em bytes, o que pode causar falhas de memória.
   *(2026-05-02)*

4. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

5. Estou na branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

6. O estado final dos PRs já tá no código + nos docs gus-XX atualizados.
   *(2026-05-03)*

7. O sistema de captura de fragmentos do Chat estava quebrado devido ao bug.
   *(2026-05-02)*

8. A proposta é criar a estrutura 'dialogos/Gustavo/' com subpastas para Chat, Code e TioGu.
   *(2026-05-03)*

9. O conteúdo no Mem0 SaaS inclui 204 fragmentos, com dados biográficos e preferências sobre o trabalho.
   *(2026-05-03)*

10. O workflow de sincronização entre o Google Drive e o GitHub ainda não está ativo.
   *(2026-05-02)*

11. O Gus é um sistema de agente pessoal multi-porta, operando em várias plataformas como Telegram, Claude Code e futuras integrações.
   *(2026-05-03)*

12. A decisão final sobre o modelo curador será após 12/05/2026, onde será feita a comparação entre os pares Haiku e Sonnet/GPT.
   *(2026-05-02)*

13. A hierarchy dos canais de escrita no Chat ainda precisa ser definida para melhorar a operação.
   *(2026-05-02)*

14. A demanda `2026-05-01-captura-multiporta-curador.md` é parcialmente resolvida pelo PR #67, mas falta o gatilho proativo no Chat.
   *(2026-05-02)*

15. O `auditoria_hub.py` é cego para o brain gus e as classificações são feitas somente por keywords.
   *(2026-05-03)*

16. O Hub Qdrant atualmente contém 40 fragmentos, dos quais 70% são considerados lixo.
   *(2026-05-03)*

17. A primeira fase de testes do projeto já foi concluída, incluindo a validação de PII no output do bot e ajustes de controle de cache para mídia.
   *(2026-05-02)*

18. O Hub Qdrant é a fonte da verdade para o sistema.
   *(2026-05-03)*

19. A captura Claude Code via cron salva transcripts redatados a cada 30 minutos.
   *(2026-05-02)*

20. O projeto Gus envolve um sistema multi-porta que conecta vários canais, como Telegram, Claude Code e Claude Chat, usando um Hub Qdrant como memória central.
   *(2026-05-02)*

21. Há uma demanda parada chamada `2026-05-01-captura-multiporta-curador.md`.
   *(2026-05-02)*

22. A auditoria da memória é realizada diariamente, mas atualmente é cega para o brain 'gus' e ignora o campo 'area'.
   *(2026-05-03)*

23. Gustavo é anestesiologista e não programa. Toda implementação passa pelo Gus.
   *(2026-05-03)*

24. Os itens da Fase 1 foram concluídos e incluem melhorias na auditoria, adição de tags e remoção de código obsoleto.
   *(2026-05-03)*

25. Gus é um sistema de agente pessoal multi-porta, integrando Telegram, Claude Code, Claude Chat e futuras plataformas como Custom GPT mobile e Alexa. A memória central fica no Hub Qdrant.
   *(2026-05-03)*

26. O projeto Gus envolve um bot chamado TioGu, que utiliza um sistema multi-porta com Hub Qdrant como memória central.
   *(2026-05-02)*

27. Fragmentos são processados por um curador, mas o sistema não diferencia entre informações extraídas relacionadas ao Gustavo e suas auto-observações como Gus.
   *(2026-05-03)*

28. O bot do Telegram (TioGu) possui 21 ferramentas distintas integradas.
   *(2026-05-03)*

29. Houve um erro na sincronia entre o Heap e o Drive do Gus.
   *(2026-05-02)*

30. 1. Gustavo é anestesiologista e trabalha com o Dimagem (clínica/laboratório de imagem).
2. Gustavo recebe ordens de serviço do Dimagem e precisa acompanhar pacientes agendados.
3. Preferência: Gus deve descrever OS apenas com dados factuais (nome, exame, horário, convênio) — sem análise clínica ou interpretação que Gustavo já domina.
4. Gus deve confirmar leitura correta dos dados e oferecer salvamento no arquivo do dia, sem expandir para análises não solicitadas.
5. Gustavo valoriza eficiência: ruído deve ser eliminado nas respostas do Gus.
   *(2026-04-28)*

31. Foi decidido que a meta_reflexao do agente Gus deve ser capturada durante as conversas.
   *(2026-05-03)*

32. A stack de memória está em estado intermediário arriscado, com fallback ativo para a coleção legada 'gus'.
   *(2026-05-03)*

33. Fragments recent itens têm um bug crítico do curador, com `format()` falhando 100% desde 30/04.
   *(2026-05-03)*

34. O Drive sync está quebrado atualmente devido à expiração do token OAuth do Google.
   *(2026-05-03)*

35. O foco do projeto é desenvolver um sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa).
   *(2026-05-02)*

36. A demanda `2026-05-01-captura-multiporta-curador.md` precisa de um gatilho proativo no Chat.
   *(2026-05-03)*

37. A opção A para o conteúdo do Mem0 SaaS é mantê-lo em `historico/`, enquanto a opção C planeja filtrá-lo e traduzi-lo para importação futura.
   *(2026-05-03)*

38. Houve uma auditoria que revelou um estado intermediário arriscado da stack de memória, com problemas como 4 chamadas LLM por unidade de input sem mecanismo de deduplicação.
   *(2026-05-03)*

39. As capturas estão funcionando de forma assíncrona no cron GitHub Actions, processadas pelo curador, que já está rodando.
   *(2026-05-02)*

40. Aguarda redeploy (~2 min).
   *(2026-05-03)*

41. A estrutura atual do sistema de escrita do projeto `claude-code` consiste em três canais distintos: escrita em tempo real através de MCP, upload de arquivos .md e demandas inbox.
   *(2026-05-02)*

42. O cache de mídia não tem limite de bytes, o que pode levar a problemas de memória no container do Railway.
   *(2026-05-02)*

43. Aba nova só precisa olhar PRs se houve uma quebra específica que depende do PR mais recente.
   *(2026-05-02)*

44. Quando você fala no Chat 'salva no hub que...' ele chama ingestar_fragmento.
   *(2026-05-03)*

45. O MCP está público — qualquer scanner que descobrir a URL Railway lê todo o Hub.
   *(2026-05-03)*

46. Há 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

47. O estado atual do projeto inclui o TioGu com 163 testes verdes, o Claude Chat com 12 fixes de 31 achados e pendências em várias áreas, incluindo a definição de `MCP_URL_SECRET` no Railway.
   *(2026-05-03)*

48. O PR #72 foi aberto no repositório Gus para abordar as questões identificadas na auditoria do Chat.
   *(2026-05-02)*

49. O segredo devemos configurar no Railway para proteger o MCP.
   *(2026-05-03)*

50. As buscas realizadas no Hub Qdrant devem retornar respostas relevantes para questões sobre exames anteriores.
   *(2026-05-02)*

51. O Hub Qdrant é a fonte da verdade para o projeto.
   *(2026-05-03)*

52. A migração para o Hub Qdrant está em curso e deve ser concluída até 12/05/2026.
   *(2026-05-03)*

53. A memória anterior (Mem0 SaaS) está sendo aposentada e o Hub Qdrant é a nova fonte da verdade.
   *(2026-05-03)*

54. Após o passo 1, o Connector no claude.ai deve ser recriado com a nova URL do MCP.
   *(2026-05-03)*

55. Se um PR precisa ser lido pra entender o presente, é sinal de doc desatualizado — não de PR importante.
   *(2026-05-03)*

56. A stack está em estado intermediário arriscado: Hub Qdrant (`gus_hub`) é a fonte nova, mas a coleção legada `gus` (Mem0 self-hosted) tem ~204 fragmentos não-migrados e o código de leitura em `gus/memory.py` ainda faz fallback pra ela.
   *(2026-05-03)*

57. O manual operacional do Gus contém regras de comportamento e como cada porta usa o Hub.
   *(2026-05-03)*

58. Os canais de controle e armazenamento de dados (hub/store) são utilizados para gerenciar a memória do Gus.
   *(2026-05-02)*

59. O `_estado-atual.md` (27/04) está desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).
   *(2026-05-02)*

60. 1. Gustavo estabeleceu protocolo específico de análise de fotos que deve ser seguido nas próximas conversas
2. Gustavo está processando múltiplas imagens de Ordens de Serviço (OS) médicas com datas históricas (09/01/2026)
3. Paciente Analete da Silva Pinto teve exames de RM (Crânio/Encéfalo com Espectroscopia e RM Fluxo Liquórico) + anestesia em Assim São Gonçalo
4. Há questão em aberto sobre como arquivar OS com datas antigas (se salva no arquivo histórico ou ignora)
   *(2026-04-28)*

61. O bot TioGu utiliza um sistema de caching de prompts que reduz custo de input em até 70% em janelas de 5 minutos.
   *(2026-05-02)*

62. O estado da coleção gus no Qdrant é vazio e o Mem0 SaaS está dormente na pasta histórico.
   *(2026-05-03)*

63. O manual operacional do Gus, regras de comportamento e como cada porta usa o Hub estão no arquivo `dialogos/_bootstrap/gus-bootstrap.md`.
   *(2026-05-02)*

64. Validar se a URL de health returna status ok e se o path /mcp retorna 404.
   *(2026-05-03)*

65. Mem0 SaaS possui 204 fragmentos, sendo 188 em inglês e 16 em português.
   *(2026-05-03)*

66. A coleção legada `gus` na Qdrant está vazia e não possui fragmentos históricos.
   *(2026-05-03)*

67. O processador do MCP deve ser reconfigurado para evitar vazamentos futuros.
   *(2026-05-03)*

68. É necessário setar o `MCP_URL_SECRET` no Railway para proteger o MCP.
   *(2026-05-03)*

69. O bot tem um ponto de falha silencioso ao atingir o limite de uso da API, respondendo apenas a quem envia uma mensagem, sem notificações proativas.
   *(2026-05-02)*

70. O nome 'mem0-from-chat' é puramente legado.
   *(2026-05-03)*

71. A auditoria diária é cega para o brain `gus`, pois ignora o `area` que o curador já preencheu.
   *(2026-05-03)*

72. 1. Gustavo trabalha com um projeto chamado **NeuroGus** — chegaram 3 demandas novas no dia 28/04 (briefing, arquitetura, código v1)
2. Existe um sistema de **múltiplos canais de comunicação** com o Gus (Gus Chat e Gus direto) — mesma entidade, portas diferentes
3. Gustavo usa **workflows automatizados** (ex: `import-from-drive.yml`) para trazer demandas do GitHub
4. Preferência de Gustavo: quer que Gus **dispare workflows e leia demandas automaticamente**, sem esperar aprovação caso estejam prontas
   *(2026-04-28)*

73. A migração ADR-001 visa aposentar a Mem0 SaaS e consolidar o Hub Qdrant como a fonte da verdade.
   *(2026-05-03)*

74. O primeiro passo para resolver o problema identificado é mergear o PR #72 e aguardar o CI passar.
   *(2026-05-02)*

75. O bot Telegram chamado TioGu possui uma arquitetura multi-provider com fallback cross-vendor.
   *(2026-05-02)*

76. Gustavo pediu um panorama geral do projeto antes de focar em um assunto específico.
   *(2026-05-02)*

77. O curador não seta estado (default vira ativo). Ninguém promove fragmentos pra estavel.
   *(2026-05-03)*

78. Gustavo é anestesiologista, sem experiência em programação. Toda implementação passa pelo Gus.
   *(2026-05-03)*

79. Os testes em produção são feitos para garantir o comportamento correto do bot.
   *(2026-05-02)*

80. A stack de memória end-to-end é composta por entradas de múltiplas fontes, procedimentos de ingestão e um Hub curador híbrido que combina Haiku e GPT-4o-mini.
   *(2026-05-03)*

81. O sistema atual não tem integração de testes unitários para a maioria das funcionalidades.
   *(2026-05-02)*

82. O curador tem 4 chamadas LLM por unidade de input (Haiku × GPT × {gustavo, gus}).
   *(2026-05-03)*

83. 1. Caminho completo da pasta de demandas do Gus: `Gustpbbr/Gus/dialogos/inbox-tiogu/`
2. PR #14 foi mergeado hoje (protocolo de portas e tools) — Gustavo pode querer revisar a documentação nova sobre análise de portas e ferramentas
3. Infraestrutura de automação está funcionando: auditoria automática, export diário do Hub e capture de sessão rodando conforme esperado
4. Hook de fim de sessão do retro-engine está funcional (2 entradas registradas ontem à noite)
   *(2026-04-28)*

84. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa.
   *(2026-05-02)*

85. Existem 3 demandas paradas em 'dialogos/inbox-claude-code/'.
   *(2026-05-02)*

86. O connector do Gus Hub precisa ser recadastrado no claude.ai devido ao ponto de falha na URL.
   *(2026-05-02)*

87. Houve um merge de um pull request relacionado a testes de regressão do curador.
   *(2026-05-02)*

88. Gustavo é anestesiologista e não programa, o que implica que toda implementação passa pelo Gus.
   *(2026-05-03)*

89. Arquivo `gus-identity.md` define quem é o Gustavo e quem é o Gus enquanto entidade.
   *(2026-05-03)*

90. O arquivo 'dialogos/_bootstrap/gus-bootstrap.md' é o manual operacional do Gus, contendo as regras de comportamento e como cada porta usa o Hub.
   *(2026-05-02)*

91. Hub é a memória central conectada a vários serviços, como Telegram, Claude Code e Claude Chat.
   *(2026-05-02)*

92. O MCP está público, permitindo que qualquer scanner que descobrir a URL Railway leia todo o Hub.
   *(2026-05-03)*

93. O projeto NeuroGus está com planejamento 100% pronto e falta a implementação.
   *(2026-05-02)*

94. O `_estado-atual.md` (27/04) está desatualizado e não reflete muitas atualizações posteriores documentadas no git, como PRs #57, #60, #63, #64 e #67.
   *(2026-05-02)*

95. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

96. O bot do Telegram, TioGu, possui cerca de 21 ferramentas e opera integrando dependências como python-telegram-bot e FastAPI.
   *(2026-05-03)*

97. A arquitetura do sistema é baseada no processamento paralelo entre vários modelos de linguagem, utilizando fallback em caso de falhas.
   *(2026-05-02)*

98. A variável MCP_URL_SECRET protege o Hub.
   *(2026-05-03)*

99. O passo 6 é validar end-to-end com uma nova conversa no Chat.
   *(2026-05-03)*

100. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

101. Agora o sistema redigirá o segredo, mas deve haver continuidade nos logs com a confirmação da segurança.
   *(2026-05-03)*

102. TioGu possui ~21 ferramentas integradas e opera em Railway.
   *(2026-05-03)*

103. A stack está em estado intermediário arriscado: Hub Qdrant é a fonte nova, mas a coleção legada tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

104. Demanda '2026-05-01-captura-multiporta-curador.md' foi arquivada após a implementação.
   *(2026-05-03)*

105. Houve um bug crítico no curador em 30/04/2026, onde o comando format() falhou 100% com KeyError no JSON literal.
   *(2026-05-03)*

106. O estado da migração revela que a coleção `gus` está vazia.
   *(2026-05-03)*

107. Se o secret 'MEM0_API_KEY' ainda existir, é possível verificar o conteúdo do Mem0 SaaS.
   *(2026-05-03)*

108. 640 PRs no código significam ruído gigante no contexto para ganho zero.
   *(2026-05-03)*

109. Cada chamada LLM já é Haiku + GPT em paralelo.
   *(2026-05-03)*

110. Destrava também escrita real-time do Chat (ingestar_fragmento).
   *(2026-05-03)*

111. Mem0 SaaS deve ser aposentado. O Hub Qdrant é a fonte nova e única de verdade.
   *(2026-05-03)*

112. O Hub é mais fresco que gus-estado-atual.md, que é um snapshot das 03h.
   *(2026-05-02)*

113. As frentes mais ativas nos últimos dias são relacionadas ao PR #60 (MCP URL secret) e PR #64 (cron captura transcripts Claude Code).
   *(2026-05-02)*

114. Não há testes automatizados implementados para o bot, o que representa um alto risco na manutenção do sistema.
   *(2026-05-02)*

115. O bot possui uma arquitetura com um coração em bot.py que gerencia os handlers e o estado.
   *(2026-05-02)*

116. O curador está rodando em loop com 100% de erro há mais de 3 dias.
   *(2026-05-02)*

117. Os 4 arquivos `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md`, `estado-atual.md` dão 80% do contexto pra qualquer aba nova.
   *(2026-05-03)*

118. O Hub atual já tem 70% de meta-lixo — não vale arriscar mais.
   *(2026-05-03)*

119. O PR #72 corrigiu um bug em produção que impedia o curador de funcionar.
   *(2026-05-02)*

120. Vi que tem 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

121. A migração para o Hub Qdrant está na fase 4 e envolve a coleta dual Haiku e Sonnet até 12/05.
   *(2026-05-03)*

122. Hub Qdrant é a fonte da verdade e toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

123. O modelo do bot suporta tanto o LLM da Anthropic quanto o da OpenAI, com implementações robustas de tratamento de erros.
   *(2026-05-02)*

124. O conteúdo do Mem0 SaaS é 204 fragmentos exportados, e esses dados foram armazenados em `historico/`.
   *(2026-05-03)*

125. Os fragmentos na coleção `gus` no Qdrant nunca foram populados.
   *(2026-05-03)*

126. A operação do sistema está comprometida por 4× multiplicação de chamadas LLM por unidade de input.
   *(2026-05-03)*

127. O estado final dos PRs está no código e nos docs gus-XX atualizados.
   *(2026-05-03)*

128. O bot Telegram (TioGu) tem ~21 tools, multimídia, prompt caching, e está em produção.
   *(2026-05-02)*

129. As opções para a migração dos dados do Mem0 SaaS incluem mantê-los em `historico/`, importar para o Hub ou filtrar e traduzir antes da importação.
   *(2026-05-03)*

130. O Hub é mais fresco que `gus-estado-atual.md`, que é um snapshot gerado pelo cron.
   *(2026-05-02)*

131. A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida pelo PR #67, mas falta o gatilho proativo no Chat.
   *(2026-05-02)*

132. Os próximos passos incluem leitura do `_estado-atual.md`, demandas pendentes e várias atualizações estruturais do projeto.
   *(2026-05-02)*

133. A coleção `gus` está vazia — 204 fragmentos prometidos não existem.
   *(2026-05-03)*

134. O `MCP_URL_SECRET` deve ser setado no Railway para proteger o acesso ao Hub.
   *(2026-05-03)*

135. Gustavo Pratti de Barros é anestesiologista e não programa; toda implementação passa pelo Gus.
   *(2026-05-03)*

136. O estado atual do projeto necessita de manutenção nas funções de curador para evitar a poluição alem do necessário no Hub.
   *(2026-05-03)*

137. Gus está na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

138. O MCP está público — qualquer scanner que descobrir a URL Railway lê todo o Hub.
   *(2026-05-03)*

139. O modelo do Chat pode salvar fragmentos sobre Gustavo no brain `gus` sem validação.
   *(2026-05-02)*

140. O sistema de agente pessoal multi-porta integra Telegram, Claude Code e futuras implementações como Alexa.
   *(2026-05-03)*

141. As pastas do Gustavo no Drive devem ser: Chat, Code e TioGu.
   *(2026-05-03)*

142. O estado final dos PRs já está no código e nos docs gus-XX atualizados. PRs descrevem o caminho, não onde a gente está.
   *(2026-05-03)*

143. A implementação do lifecycle no esquema gus-18 foi declarado, mas não está sendo executado, afetando a promoção automática de fragmentos no Hub.
   *(2026-05-03)*

144. Gus está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

145. Tô aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

146. O bot Telegram possui ~21 ferramentas distintas implementadas.
   *(2026-05-03)*

147. O Gus é um sistema de agente pessoal multi-porta que conecta diferentes plataformas.
   *(2026-05-03)*

148. A ambiguidade no status 'fallback-mem0' causa confusão, pois o log não reflete com precisão que esses dados vão diretamente para o Hub.
   *(2026-05-03)*

149. A análise dos logs mostra que a memória Mem0 está sendo usada como fallback, o que é um vetor de perda contínua.
   *(2026-05-03)*

150. Gustavo está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-02)*

151. Os últimos 5 dias mostraram os PRs #67 (curador chat bidirecional + GPT-4o), #64 (captura transcripts Code via cron), #60 (MCP URL secret) e #70 (demanda consolidada).
   *(2026-05-03)*

152. O sistema é um agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa) com memória central no Hub Qdrant.
   *(2026-05-03)*

153. O bot Telegram TioGu está estruturado em várias camadas, incluindo bot.py, llm.py, memory.py e tools.py.
   *(2026-05-02)*

154. Tem 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

155. O estado de migração para o Hub Qdrant é em curso, visando aposentadoria do Mem0 SaaS.
   *(2026-05-03)*

156. A coleção legada `gus` (Mem0 self-hosted) tem ~204 fragmentos não-migrados e o código de leitura em `gus/memory.py` ainda faz fallback pra ela.
   *(2026-05-03)*

157. O Gus é um agente pessoal multi-porta que interage por Telegram, Claude Code e Claude Chat.
   *(2026-05-03)*

158. O sistema multi-porta com Hub Qdrant como memória central opera com GitHub como conhecimento e Drive como espelho.
   *(2026-05-02)*

159. O bot TioGu é desenvolvido em Python, utilizando a biblioteca python-telegram-bot na versão 21.6.
   *(2026-05-02)*

160. O projeto NeuroGus está bloqueado devido a decisões UX que precisam ser tomadas.
   *(2026-05-03)*

161. Hoje o MCP não permite escrita real-time do Chat por falta do MCP_URL_SECRET.
   *(2026-05-03)*

162. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026, quando Gustavo escolherá o modelo definitivo.
   *(2026-05-03)*

163. A stack de memória ainda é considerada em estado intermediário arriscado.
   *(2026-05-03)*

164. O paciente_id canônico é gus (lowercase, sem acentos).
   *(2026-05-02)*

165. Avanços futuros no projeto incluem a reescrita do system_prompt.md e a revisão de ferramentas e métodos utilizados na integração do bot.
   *(2026-05-02)*

166. A implementação de um alerta proativo para o HARD_LIMIT está entre as altas prioridades a serem abordadas no projeto.
   *(2026-05-02)*

167. Os arquivos das demandas paradas são: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, e `_frontmatter-referencia.md`.
   *(2026-05-02)*

168. Atualmente há 3 demandas paradas em dialogos/inbox-claude-code.
   *(2026-05-03)*

169. O Hub não tem nenhum fragmento com tipo=identidade_operacional e estado=estavel, nem procedural e estado=estavel.
   *(2026-05-03)*

170. Os workflows do GitHub estão funcionando corretamente, com 5 runs recentes, todos OK.
   *(2026-05-03)*

171. A recomendação é priorizar testes automáticos robustos, especialmente após a refatoração do código.
   *(2026-05-02)*

172. O estado final dos PRs está no código e nos documentos atualizados, enquanto os PRs descrevem o caminho que foi tomado.
   *(2026-05-03)*

173. A função '_fallback_mem0' foi removida para evitar poluição silenciosa no Hub com entradas não classificadas.
   *(2026-05-03)*

174. O estado final dos PRs já está no código e nos docs gus-XX atualizados; PRs descrevem o caminho, não onde a gente está.
   *(2026-05-03)*

175. O workflow de migração de `gus` para `gus_hub` revelou que não foram encontrados fragmentos durante a migração.
   *(2026-05-03)*

176. O `dimagem.py` é uma integração de domínio e deve ser movido para o diretório `integrations/` para refletir sua natureza.
   *(2026-05-02)*

177. O script para exportar fragmentos do Mem0 SaaS já foi criado e está disponível na pasta de scripts.
   *(2026-05-03)*

178. O LLM Anthropic está utilizando o SDK anthropic na versão 0.40.0.
   *(2026-05-02)*

179. Os documentos relevantes para próximos passos e decisões estão localizados em projetos/gus/.
   *(2026-05-02)*

180. Gus está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-02)*

181. A primeira etapa da migração envolve aprovar a nova estrutura e migrar as memórias existentes para o Hub.
   *(2026-05-03)*

182. O bot TioGu utiliza um sistema multi-porta com Hub Qdrant como memória central e GitHub como conhecimento.
   *(2026-05-02)*

183. Existe uma demanda ativa sobre a sincronização do Drive, a qual está parada.
   *(2026-05-02)*

184. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e envolve resolver a questão do refresh token OAuth expirado.
   *(2026-05-02)*

185. Memória no brain gustavo registra a existência do protocolo de Análise de Exames Laboratoriais.
   *(2026-05-02)*

186. O bot possui uma funcionalidade de caching de prompts que reduz o custo de input em até 70% em janelas de 5 minutos.
   *(2026-05-02)*

187. As entradas de dados no sistema provêm de várias fontes, incluindo Telegram, Claude Chat e Claude Code, que cada uma gera dados usando protocolos de captura multiporta.
   *(2026-05-03)*

188. O processo de auditoria revelou a poluição de fragmentos entre os brains `gustavo` e `gus`.
   *(2026-05-03)*

189. O último fragmento disponível no Hub Qdrant indica que o Hub está ocioso há mais de 6 horas.
   *(2026-05-03)*

190. A recomendação é mover `gus/dimagem.py` para `integrations/`, sinalizando que é específica do contexto clínico e não parte central do sistema.
   *(2026-05-02)*

191. O projeto tem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template.
   *(2026-05-02)*

192. O projeto NeuroGus entrou em cena e a fase 1 do backend SSE está em uma branch separada, enquanto a fase 2 do frontend está bloqueada.
   *(2026-05-02)*

193. A demanda da semana pode ser encontrada no arquivo 'dialogos/streams/[semana-2026-04-21.md]'.
   *(2026-05-03)*

194. A atualização dos documentos de estado atual e de projetos deve ser feita sempre que houver mudanças significativas.
   *(2026-05-02)*

195. O `_estado-atual.md` é gerado pela automática a cada 15 minutos, oferecendo um snapshot do Hub.
   *(2026-05-02)*

196. A demanda de capturas no multiporta curador depende de aprovação do Gustavo.
   *(2026-05-03)*

197. O sistema possui um bug que pode resultar na perda de PII caso não haja verificação no output do bot.
   *(2026-05-02)*

198. A mudança de `drop_pending_updates` de True para False pode causar storm de mensagens em caso de downtime.
   *(2026-05-02)*

199. Fase 3.1 do planejamento é a primeira execução do workflow `migrar-gus-para-hub.yml` em modo dry-run.
   *(2026-05-03)*

200. A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida.
   *(2026-05-02)*

201. O Hub deve utilizar URL secrets para aumentar a segurança.
   *(2026-05-02)*

202. Curador bidirecional cron em desenvolvimento e precisa ser finalizado até 12/05/2026.
   *(2026-05-03)*

203. O `_estado-atual.md` (27/04) está bem desatualizado.
   *(2026-05-02)*

204. As pendências do Gustavo incluem configurar 'MCP_URL_SECRET' no Railway e recadastrar o Connector claude.ai.
   *(2026-05-03)*

205. O resultado da auditoria mostra que a stack está em estado intermediário arriscado devido a cross-brain pollution.
   *(2026-05-03)*

206. O PR #67 introduziu um curador bidirecional no Chat, utilizando Sonnet 4.6 e GPT-4o.
   *(2026-05-02)*

207. O prompt do bot tem 794 linhas, o que dificulta a manutenção e apresenta riscos de drift.
   *(2026-05-02)*

208. Gustavo está na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

209. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

210. A coleta dual de modelos no curador terminou em 12/05/2026, e depois Gustavo escolherá o modelo definitivo.
   *(2026-05-03)*

211. Atualmente, existem 6 demandas pendentes na porta 'inbox-claude-code'.
   *(2026-05-03)*

212. O Hub está em estado intermediário arriscado, pois tem 204 fragmentos não-migrados.
   *(2026-05-03)*

213. Gustavo é anestesiologista e não programa. Toda implementação passa por Gus/Tiogu.
   *(2026-05-03)*

214. A estrutura proposta para dialogos/Gustavo/ será: Chat, Code e TioGu.
   *(2026-05-03)*

215. Os 4 documentos principais que dão 80% do contexto para qualquer aba nova são: 'gus-bootstrap.md', 'gus-identity.md', 'gus-estado-atual.md' e 'estado-atual.md'.
   *(2026-05-03)*

216. O Drive sync está parado e a demanda '2026-05-01-drive-sync-oauth-fix.md' está ativa. A hipótese é que o refresh token OAuth expirou.
   *(2026-05-02)*

217. Existem 3 demandas paradas em `dialogos/inbox-claude-code/` no projeto.
   *(2026-05-02)*

218. A demanda 2026-05-01-captura-multiporta-curador.md está parcialmente resolvida pelo PR #67.
   *(2026-05-02)*

219. O curador de memórias tem a permissão para deletar fragmentos considerados lixo.
   *(2026-05-03)*

220. A captura em tempo real durante a conversa pode ser ativada para aumentar a interação e responsividade do Chat.
   *(2026-05-02)*

221. A stack de memória está em estado intermediário arriscado, com múltiplas produções de fragmentos e sem mecanismo de deduplicação.
   *(2026-05-03)*

222. 4 memórias poluídas precisam ser deletadas manualmente.
   *(2026-05-03)*

223. 1. Após merge e deploys recentes, o auto_diagnostico agora tem acesso ao Hub Qdrant (evolução positiva)
2. Problema identificado: Hub Qdrant mostra 0 fragmentos para user_id=gustavo — curador acessível mas vazio ou fragmentos indexados com user_id incorreto
3. Workflow "Ingest Mem0 from Claude Chat" está falhando pós-merge — precisa investigação
4. Gustavo usa estratégia de rodar auto_diagnostico duas vezes em sequência para detectar mudanças pós-deploy
5. Infraestrutura base saudável: GitHub Token (fine-grained PAT), Anthropic Haiku, Tavily search, volume Railway writable funcionando
   *(2026-04-27)*

224. A memória central do Gus está no Hub Qdrant, com arquivos .md no GitHub que são espelhados no Drive.
   *(2026-05-03)*

225. Gustavo Pratti de Barros é anestesiologista e não programa.
   *(2026-05-03)*

226. A validação de tipo/camada/área no curador foi implementada para garantir que os dados inseridos no Hub sigam o vocabulário gus-18.
   *(2026-05-02)*

227. As frentes mais ativas incluem o PR #67 (curador chat bidirecional + GPT-4o), PR #64 (captura transcripts Code via cron), PR #60 (MCP URL secret) e PR #70 (demanda consolidada).
   *(2026-05-02)*

228. Aba nova só precisa olhar PRs se: você falar 'tá quebrando X depois do PR #YY' → aí sim, lê o PR.
   *(2026-05-03)*

229. O Hub contém 19 fragmentos no brain `gustavo` e está ocioso nas últimas 6h.
   *(2026-05-03)*

230. A Fase 1 refinada do projeto tem 9 itens e requer aproximadamente 7-8 horas de trabalho.
   *(2026-05-03)*

231. A demanda 2026-05-01-drive-sync-oauth-fix.md está ativa.
   *(2026-05-02)*

232. O core obrigatório inclui arquivos de bootstrap e estado atual.
   *(2026-05-02)*

233. Sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) com Hub Qdrant como memória central.
   *(2026-05-02)*

234. O bot utiliza um mecanismo de prompt caching que reduz o custo de input em até 70% nas chamadas para os modelos.
   *(2026-05-02)*

235. A coleta dual de modelos no curador termina em 12/05/2026 e Gustavo escolhe modelo definitivo depois.
   *(2026-05-03)*

236. O workflow de auditoria diária do Hub Qdrant é importante para a manutenção da integridade dos dados.
   *(2026-05-03)*

237. O Gus é um sistema de agente pessoal multi-porta conectado a diversas plataformas.
   *(2026-05-03)*

238. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

239. O bot Telegram, chamado TioGu, utiliza um sistema multi-porta com Hub Qdrant como memória central, onde o Gustavo não programa e a IA implementa.
   *(2026-05-02)*

240. Apenas fragmentos criados antes da migração e depois da Fase 3 vão existir só na coleção antiga, fora do Hub novo.
   *(2026-05-03)*

241. As 4 principais fontes de contexto obrigatórias para novos projetos são: o manual operacional do Gus, informações sobre a identidade do Gustavo, o estado atual do Hub e onde parou na sessão anterior.
   *(2026-05-03)*

242. Os arquivos de projeto são espelhados no Drive, com a memória central no Hub Qdrant.
   *(2026-05-03)*

243. O sistema contém 21 tools que são utilizados por meio do dispatch por nome.
   *(2026-05-02)*

244. O ADR-001 está em curso para migrar para o Hub Qdrant como fonte da verdade.
   *(2026-05-03)*

245. O bot opera com dependências como python-telegram-bot, anthropic SDK, openai, FastAPI e Qdrant.
   *(2026-05-03)*

246. Quatro demandas pendentes foram identificadas no `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

247. O Hub Qdrant é a fonte da verdade, enquanto arquivos .md estão armazenados no GitHub.
   *(2026-05-03)*

248. A leitura de PRs deve ser feita apenas se necessário para investigar bugs ou entender decisões que não estão documentadas.
   *(2026-05-02)*

249. O hook do retro-engine registra 'no-op: anthropic_missing' e continua a execução normalmente, seguindo o fluxo padrão.
   *(2026-05-02)*

250. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

251. A leitura dos últimos arquivos da pasta dialogos/streams/ é importante para entender a demanda da semana.
   *(2026-05-02)*

252. O arquivo de log do retro-engine gerou uma mensagem de erro 'anthropic_missing'.
   *(2026-05-02)*

253. O estado atual do projeto é a migração ADR-001 em curso, aposentar Mem0 SaaS e a coleta dual de modelos.
   *(2026-05-03)*

254. A demanda de Drive sync (`2026-05-01-drive-sync-oauth-fix.md`) está ativa. Hipótese: refresh token OAuth expirou. Três opções: reset OAuth (paliativo) / Service Account (definitivo) / aposentar Drive sync (radical).
   *(2026-05-02)*

255. O sistema do Gus tem controle de acesso, bloqueando escrita se a autenticação não for válida.
   *(2026-05-02)*

256. "Documento sem título.md" provavelmente é lixo de sync.
   *(2026-05-03)*

257. A coletiva legado `gus` tem cerca de 204 fragmentos não-migrados.
   *(2026-05-03)*

258. Gustavo é anestesiologista e não programa. Toda implementação passa pelo Gus/Tiogu.
   *(2026-05-03)*

259. Há um esforço contínuo para manter o sistema Gus atualizado, organizado e funcional.
   *(2026-05-02)*

260. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md` e `_frontmatter-referencia.md`.
   *(2026-05-02)*

261. O arquivo `_estado-atual.md` foi gerado pelo cron às 03h e é um snapshot do Hub.
   *(2026-05-02)*

262. O `_estado-atual.md` (27/04) está desatualizado e não reflete PRs #57, #60, #63, #64, #67.
   *(2026-05-02)*

263. O Hub Qdrant é a nova fonte da verdade e a migração deve ser completada até 12 de maio de 2026.
   *(2026-05-03)*

264. Os testes realizados até o momento atingiram 163 testes verdes, cobrindo diversas partes críticas do sistema, incluindo o LLM dispatch e a memória.
   *(2026-05-02)*

265. A receita de como ler a aba nova e o que não precisa ser lido já foi explicada, incluindo que arquivos do histórico são inutilizados.
   *(2026-05-02)*

266. As decisões arquiteturais são fundamentais ao longo do projeto, como a migração do Mem0 Cloud para o Qdrant.
   *(2026-05-03)*

267. Existem três opções para resolver o problema do Drive sync: resetar OAuth, usar Service Account ou aposentar o Drive sync.
   *(2026-05-03)*

268. Sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa).
   *(2026-05-03)*

269. O projeto tem 4 demandas pendentes no dialogos/inbox-claude-code.
   *(2026-05-03)*

270. Os comandos disponíveis para preferir ao usar arquivos incluem `ego_cache_atual()` e `fragmentos_recentes(horas=24)`.
   *(2026-05-03)*

271. O processo de auditoria na stack de memória revela que o ciclo de fallback em tempo de execução pode causar poluição silenciosa.
   *(2026-05-03)*

272. O workflow `export-mem0` precisa ser acionado na branch `main` do repositório.
   *(2026-05-03)*

273. O estado atual de migração é o ADR-001 em curso, aposentando o Mem0 SaaS, sendo o Hub Qdrant a fonte da verdade.
   *(2026-05-03)*

274. O Chat só salva quando você pede. Não detecta automaticamente fatos ou decisões importantes.
   *(2026-05-03)*

275. O Hub é responsável por integrar e processar as informações entre as ferramentas e o agente.
   *(2026-05-02)*

276. Anotificações automáticas do TioGu devem continuar funcionais.
   *(2026-05-03)*

277. Os testes em `tests/test_curador.py` agora cobrem a validação de erros do curador.
   *(2026-05-02)*

278. Gustavo é anestesiologista, não programa — toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

279. A coleta dual de modelos no curador (Haiku × GPT-4) e o levantamento de dados devem ser feitos com cuidado para evitar redundâncias.
   *(2026-05-03)*

280. A função `ingestar_fragmento` aceita um parâmetro `user_id` que poderia ser mal utilizado se não houver validação adequada.
   *(2026-05-02)*

281. O bot Telegram (TioGu) possui cerca de 21 tools e está em produção no Railway.
   *(2026-05-02)*

282. O bot Telegram, TioGu, possui ~21 ferramentas distintas integradas.
   *(2026-05-03)*

283. O código do projeto está na branch `claude/initial-setup-iWTfL`.
   *(2026-05-02)*

284. Sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) com Hub Qdrant como memória central.
   *(2026-05-02)*

285. O `MCP_URL_SECRET` ainda não está ativado no Railway.
   *(2026-05-03)*

286. A recomendação é alterar `drop_pending_updates=True` para logging do count de pending e enviar uma mensagem ao Gustavo no boot caso haja pendências.
   *(2026-05-02)*

287. A implementação do NeuroGus está 100% planejada e aguarda confirmação dos itens 11.1-11.7 das decisões abertas.
   *(2026-05-02)*

288. As demandas pendentes foram identificadas como prioritárias para serem resolvidas.
   *(2026-05-02)*

289. O passo 1 é gerar novo MCP_URL_SECRET.
   *(2026-05-03)*

290. O 'HARD_LIMIT' é uma falha silenciosa que impede que o usuário perceba que o bot não está respondendo após atingir o limite.
   *(2026-05-02)*

291. A convenção de nomenclatura dos arquivos JSON é <paciente_id>__<data_coleta>__<lab_curto>.json.
   *(2026-05-02)*

292. A partir de 27/04/2026, o Hub Qdrant passou a capturar dados ao invés do Mem0 SaaS.
   *(2026-05-03)*

293. A auditoria do Chat envolve todos os aspectos relacionados ao projeto Claude Chat.
   *(2026-05-03)*

294. Gustavo pode optar por padronizar certas instruções em um arquivo dialogos/_bootstrap/[checklist-boot-aba-nova.md] para deixar a canonização mais clara.
   *(2026-05-03)*

295. O snapshot do Hub registra ocioso há 6h+ na janela fragmentos últimas 6h.
   *(2026-05-02)*

296. O protocolo de Análise IA de Exames Laboratoriais v1 está localizado em Gus-Sync/protocolos/protocolo-exames-laboratoriais-v1.md.
   *(2026-05-02)*

297. O projeto tem 4 demandas pendentes no dialogos/inbox-claude-code.
   *(2026-05-03)*

298. As demandas pendentes incluem a captura multiporta, curador bidirecional cron, e OAuth para sincronização do Drive.
   *(2026-05-03)*

299. Foi decidido remover a função `_fallback_mem0` do código para evitar a inserção de lixo no Hub quando o curador falha.
   *(2026-05-03)*

300. A Fase 5 do projeto está programada para remover a memória Mem0 SaaS.
   *(2026-05-03)*

301. O Hub Qdrant (`gus_hub`) funciona como memória central para o sistema multi-porta.
   *(2026-05-02)*

302. O arquivo `gus-estado-atual.md` serve como um snapshot do Hub, fornecendo informações sobre onde paramos na sessão anterior.
   *(2026-05-03)*

303. O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).
   *(2026-05-02)*

304. O Hub Qdrant deve receber fragmentos úteis e consolidar as informações do Gus.
   *(2026-05-03)*

305. O bot Telegram (TioGu) possui ~21 tools, multimídia, prompt caching, em produção Railway.
   *(2026-05-02)*

306. Para enviar demandas pelo celular, basta criar um arquivo no Drive em Gus-Sync/dialogos/inbox-gustavo/code/ com texto livre.
   *(2026-05-03)*

307. Gustavo está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-02)*

308. O modelo de NeuroGus, com pilotagem planejada, aguarda confirmação dos itens 11.1-11.7.
   *(2026-05-02)*

309. O Hub Qdrant é a fonte da verdade e o Gustavo é anestesiologista, não programa.
   *(2026-05-03)*

310. 1. Gustavo quer que o workflow de migração Mem0 → Qdrant rode e que o auto_diagnóstico seja executado após conclusão.

2. Hub Qdrant está operacional com 4+ fragmentos (subiu de 2), migração em progresso para consolidar 204 memórias. Esperado crescimento conforme workflow processa.

3. Site da arquitetura do Gus foi gerado em HTML e está em `dialogos/inbox-claude-chat/` aguardando Gustavo abrir no claude.ai para renderizar como Artifact.

4. Infra confirmada como estável: GitHub Token (fine-grained PAT), Qdrant, Anthropic (Haiku), Tavily, Volume Railway e Workflows GitHub todos operacionais.

5. Gustavo tem capacidade de revisar demandas, priorizar tarefas e tomar decisões sobre fluxo de trabalho conforme feedback do Gus.
   *(2026-04-28)*

311. O `_estado-atual.md` está desatualizado desde 27/04.
   *(2026-05-03)*

312. Abre app Railway no celular (ou web em https://railway.app).
   *(2026-05-03)*

313. Um passo necessário é criar o MCP_URL_SECRET no Railway para proteger o acesso ao hub.
   *(2026-05-03)*

314. Há 4 demandas pendentes no `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

315. As demandas pendentes são sobre captura multiporta, curador bidirecional cron e autenticação OAuth para o Drive.
   *(2026-05-03)*

316. Hub Qdrant é a fonte da verdade. Coleta dual de modelos no curador (Haiku × GPT-4o-mini, mudou de Sonnet em 29/04 por custo/resiliência) termina 12/05/2026.
   *(2026-05-03)*

317. A porta Claude Chat (claude.ai) serve como interface para interagir com o Hub e o MCP server.
   *(2026-05-03)*

318. A auditoria do Chat envolve tanto a porta Claude Chat (claude.ai) quanto o sistema operacional que a alimenta.
   *(2026-05-02)*

319. O TioGu é um bot do Telegram com arquitetura multi-provider, utilizando LLMs da Anthropic e OpenAI em fallback.
   *(2026-05-02)*

320. O bug no curador causou divergência Haiku × GPT entre 29/04 a 02/05.
   *(2026-05-03)*

321. O Hub tem 19 fragmentos no brain `gustavo` e o sistema está ocioso nas últimas 6 horas.
   *(2026-05-02)*

322. Para Gustavo, a captura dual de modelos no curador (Haiku × GPT) termina em 12/05/2026 — depois Gustavo escolhe modelo definitivo.
   *(2026-05-03)*

323. As demandas pendentes no `dialogos/inbox-claude-code/` são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao e um template.
   *(2026-05-02)*

324. A migração da coleção legada para o hub Qdrant está em andamento.
   *(2026-05-03)*

325. O sistema possui um curador híbrido que permite o uso de Haiku e GPT-4o em paralelo para extração de fragmentos.
   *(2026-05-02)*

326. O bot Telegram (TioGu) conta com ~21 tools, multimídia, caching de prompts e foi desenvolvido para operar continuamente em Railway.
   *(2026-05-02)*

327. O status do Hub é atualizado a cada 15min pelo cron.
   *(2026-05-02)*

328. O plano NeuroGus está 100% pronto.
   *(2026-05-02)*

329. O bot utiliza o framework python-telegram-bot na versão 21.6, que é recente e adequado para sua operação.
   *(2026-05-02)*

330. A auditoria diária é cega ao brain `gus`, registrando apenas fragmentos do brain `gustavo`. Isso impacta a qualidade da curadoria.
   *(2026-05-03)*

331. A decisão final do modelo do curador está prevista para após 12/05/2026.
   *(2026-05-02)*

332. A estratégia de Drive sync atualmente apresenta um problema com o token OAuth expirado.
   *(2026-05-02)*

333. O Hub Qdrant é a fonte da verdade para a memória do Gus.
   *(2026-05-03)*

334. Na análise, foram encontrados dados clínicos, preferências de trabalho e decisões arquiteturais.
   *(2026-05-03)*

335. Hub Qdrant é a fonte da verdade e está no sistema de agente pessoal multi-porta.
   *(2026-05-03)*

336. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

337. Em 02/05/2026, foram 204 fragmentos encontrados na coleção Mem0 SaaS.
   *(2026-05-03)*

338. O fluxo sugere que ao salvar no Drive em 'Gustavo/<porta>/' o script deve preencher o frontmatter automaticamente.
   *(2026-05-03)*

339. A demanda para captura multiporta do Claude Chat está parcialmente resolvida, mas falta o gatilho proativo no Chat.
   *(2026-05-02)*

340. O Panorama do projeto Gus em 02/05/2026 inclui identidade e arquitetura, o que está sólido e em aberto, além de observações sobre o estado final dos PRs.
   *(2026-05-02)*

341. Existem 3 demandas paradas na pasta `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

342. Gustavo escolhe modelo definitivo em 12/05/2026.
   *(2026-05-03)*

343. O bot Telegram (TioGu) possui ~21 tools, multimídia, prompt caching e está em produção no Railway.
   *(2026-05-02)*

344. A ausência de créditos na Anthropic pode impedir consultas que dependem dessa API.
   *(2026-05-02)*

345. A migração do Mem0 SaaS para o Hub Qdrant está em curso, com previsão para conclusão em 12/05/2026.
   *(2026-05-03)*

346. Hub Qdrant armazena fragmentos de memórias e decisões tomadas nas interações.
   *(2026-05-03)*

347. Os commits mais recentes incluem PRs que implementam melhorias e correções relacionadas ao Chat.
   *(2026-05-03)*

348. A falta de um mecanismo de deduplicação nos dados capturados através de múltiplas chamadas pode levar à inserção de dados repetidos no sistema.
   *(2026-05-03)*

349. Todos os processos de captura de dados e informações sensíveis precisam seguir diretrizes rigorosas para evitar vazamentos de PII.
   *(2026-05-02)*

350. O `_estado-atual.md` está desatualizado desde 27/04.
   *(2026-05-03)*

351. A migração do sistema de Mem0 SaaS para Hub Qdrant está em andamento, com a coleta dual de modelos terminando em 12/05/2026.
   *(2026-05-03)*

352. A função `drop_pending_updates` é debatida: manter como True evita a perda de mensagens, mas pode causar confusão se não for notificado ao usuário.
   *(2026-05-02)*

353. Gus é um sistema de agente pessoal multi-porta, que inclui Telegram, Claude Code, Claude Chat e futuras extensões.
   *(2026-05-03)*

354. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

355. Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`. As demandas são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao e um template.
   *(2026-05-03)*

356. Curadores de memória devem ser mantidos atualizados para evitar a poluição de dados.
   *(2026-05-03)*

357. 1. Gustavo quer que o Gus tenha capacidade de disparar todos os 8 workflows disponíveis manualmente (auditoria-mem0, briefing-matinal, check-saude, export-mem0, reflexao-quinzenal, retrospectiva-semanal, sync-to-drive, sync-to-drive-full).

2. Gustavo quer auto diagnóstico do sistema: health check completo que valide GitHub, Hub Qdrant, Anthropic, Tavily, volume Railway e workflows com status visual (✅/⚠️/❌).

3. Gustavo quer que o Gus possa acessar e auditar as memórias: buscar no Hub Qdrant (brain do Gustavo), ver auditoria completa com stats/gaps/duplicatas/frescor, e acessar o próprio brain do Gus (padrões operacionais).

4. O `sync-to-drive-full` copia todos os `.md` do repo pro Drive, exceto a pasta `sensivel/` — workflow simples e sem lógica específica adicional.

5. O `notificar-inbox-tiogu` detecta arquivos novos na inbox e avisa Gustavo no Telegram (workflow de 7s).
   *(2026-04-28)*

358. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) terminará em 12/05/2026, quando Gustavo escolherá o modelo definitivo.
   *(2026-05-03)*

359. As demandas pendentes para a porta incluem: captura multiporta, curador bidirecional cron, e drive-sync OAuth.
   *(2026-05-03)*

360. As duas demandas pendentes e os documentos de próximos passos serão lidos em paralelo.
   *(2026-05-02)*

361. O workflow GitHub Actions processa transcripts commitados via curador, usando secrets do Actions.
   *(2026-05-02)*

362. O bot Telegram (TioGu) tem ~21 tools, multimídia, prompt caching, e usa o Hub Qdrant como memória central.
   *(2026-05-02)*

363. O MCP tá público — qualquer scanner que descobrir a URL Railway lê todo o Hub.
   *(2026-05-03)*

364. Gustavo é anestesiologista, não programa — toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

365. A URL secret protege o MCP.
   *(2026-05-03)*

366. A inclusão de um novo campo 'prompt_version' foi feita para rastrear a versão do prompt utilizado no curador.
   *(2026-05-03)*

367. O script `migrar_gus_para_hub.py` foi executado em dry-run e não encontrou fragmentos para migração.
   *(2026-05-03)*

368. O Hub Qdrant está funcionando corretamente, com 50+ frags, mais recente há 4.4h (02/05 19:44 BRT).
   *(2026-05-03)*

369. A URL `MCP_URL_SECRET` protege o MCP.
   *(2026-05-03)*

370. A fase de auditoria deve incluir a análise da divergência de retorno entre Haiku e GPT quando a saída é vazia.
   *(2026-05-03)*

371. O código de leitura em `gus/memory.py` ainda faz fallback para a coleção legada Mem0 SaaS, que tem aproximadamente 204 fragmentos não-migrados.
   *(2026-05-03)*

372. O Hub Qdrant é a memória central do Gus, armazenando informações essenciais.
   *(2026-05-03)*

373. O arquivo untracked é o log que registra 'no-op: anthropic_missing' e segue.
   *(2026-05-02)*

374. A captura multiporta do Claude Chat precisa de um gatilho proativo no Chat, e isso está em discussão.
   *(2026-05-02)*

375. Gustavo é anestesiologista e utiliza um sistema de agente pessoal multi-porta chamado Gus.
   *(2026-05-03)*

376. Gus é um sistema de agente pessoal multi-porta com memória central no Hub Qdrant e arquivos .md no GitHub, espelhados no Drive.
   *(2026-05-03)*

377. O state final do PRs já está no código e nos docs gus-XX atualizados.
   *(2026-05-03)*

378. As demandas pendentes são: captura-multiporta-curador, drive-sync-oauth-fix e pendencias-claude-chat-consolidacao.
   *(2026-05-02)*

379. A migração para o Hub Qdrant está em andamento, com um cronograma que inclui a descontinuação do Mem0 SaaS.
   *(2026-05-03)*

380. O Hub Qdrant coleta dual até 12/05 com um curador híbrido.
   *(2026-05-02)*

381. Depois de configurar o segredo no Railway, precisamos validar se tudo está funcionando.
   *(2026-05-03)*

382. As auditorias são realizadas diariamente e o sistema classifica fragmentos por keywords, ignorando a área preenchida pelo curador.
   *(2026-05-03)*

383. O `claude.md` na raiz é auto-injetado em toda sessão.
   *(2026-05-02)*

384. A decisão de migração ADR-001 está em curso e tem como objetivo substituir o Mem0 SaaS pelo Hub Qdrant como fonte da verdade.
   *(2026-05-03)*

385. Para cada redeploy, mensagens enviadas durante o downtime são descartadas.
   *(2026-05-02)*

386. Decisões sobre a frequência da captura de memória pro Chat são debatidas, incluindo níveis de agressividade.
   *(2026-05-03)*

387. O sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa) tem como memória central no Hub Qdrant, com arquivos .md no GitHub, espelhados no Drive.
   *(2026-05-03)*

388. O `_estado-atual.md` está desatualizado e o Hub reporta 19 fragmentos.
   *(2026-05-02)*

389. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa.
   *(2026-05-02)*

390. As atualizações recentes no sistema incluem a promoção automática de fragmentos após 30 dias e no mínimo dois acessos, porém isso ainda não foi implementado.
   *(2026-05-03)*

391. Há 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

392. A falta de um mecanismo de deduplica os fragmentos criados gera o risco de poluição cruzada entre os brains.
   *(2026-05-03)*

393. O hook de Stop do retro-engine falhou devido à falta da variável ANTHROPIC_API_KEY.
   *(2026-05-02)*

394. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e precisa de uma decisão.
   *(2026-05-02)*

395. Algumas demandas têm nome quebrado.
   *(2026-05-03)*

396. Adicionar alerta opcional via notificar_telegram se Gustavo quiser saber em tempo real requer secret do Telegram bot.
   *(2026-05-03)*

397. O sistema deve utilizar o `MCP_URL_SECRET` para proteger o acesso ao Hub.
   *(2026-05-02)*

398. O sistema está em produção e o hub ainda não tem o URL_SECRET, representando um risco potencial de segurança.
   *(2026-05-02)*

399. Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, (_frontmatter-referencia.md é só template).
   *(2026-05-03)*

400. O curador do Gus opera com múltiplos modelos (Haiku e GPT-4), com foco na eficiência e na precisão.
   *(2026-05-03)*

401. Gustavo é anestesiologista e não programa. Toda implementação passa por Gus/Tiogu.
   *(2026-05-03)*

402. O objetivo é limpar o Hub, removendo conteúdo antigo e mantendo apenas informações úteis.
   *(2026-05-03)*

403. Gustavo é anestesiologista, não programa.
   *(2026-05-03)*

404. A stack de memória end-to-end do Gus inclui três caminhos de escrita: Telegram, Claude Chat e Claude Code.
   *(2026-05-03)*

405. O arquivo `gus/dimagem.py` deve ser movido para `gus/integrations/dimagem.py`, indicando que é uma integração de domínio e não uma parte central do bot.
   *(2026-05-02)*

406. A stack de memória está em estado intermediário arriscado, com a coleção legada `gus` ainda viva e fallback ativo para Mem0.
   *(2026-05-03)*

407. O planejamento para o NeuroGus está 100% pronto e existem 3 demandas em `inbox-tiogu/` de 28/04.
   *(2026-05-02)*

408. O Protocolo de Análise IA de Exames Laboratoriais v1 define 8 fases sequenciais que qualquer IA executa sobre um exame, gerando saída estruturada reproduzível.
   *(2026-05-02)*

409. Gustavo está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-02)*

410. O estado final do modelo curador deve ser comparado após 12/05/2026.
   *(2026-05-02)*

411. O script `busca_memorias (MCP)` é utilizado para buscar memórias no Hub.
   *(2026-05-03)*

412. A arquitetura do TioGu inclui um sistema de fallback cross-vendor que melhora a resiliência do bot.
   *(2026-05-02)*

413. Importações recentes pelo Drive incluem 3 arquivos novos sobre ingestão de exames no Hub e protocolo truncado.
   *(2026-05-03)*

414. O sistema multi-porta do projeto Gus tem o Hub Qdrant como memória central.
   *(2026-05-02)*

415. Os 60 PRs são considerados ruído gigante no contexto para ganho zero quando se busca entender o estado atual do projeto.
   *(2026-05-02)*

416. O `_estado-atual.md` na pasta projetos/gus está desatualizado em 27/04 — o estado vivo é no `gus-estado-atual.md` que é atualizado a cada 15min.
   *(2026-05-02)*

417. A pasta inbox-mem0-from-chat será renomeada para inbox-chat-raw e o _log/resumos-mem0 será renomeado para _log/curador.
   *(2026-05-03)*

418. Os 3 passos mencionados são todos da porta Claude Chat: MCP_URL_SECRET, Recadastrar Connector claude.ai e Drive sync.
   *(2026-05-03)*

419. A migração do sistema para o Hub Qdrant está em andamento, com previsão de término em 12/05/2026.
   *(2026-05-03)*

420. O estado atual da migração está em curso, e a coletânea legada do Mem0 SaaS precisa ser encerrada, pois o Hub Qdrant é a fonte da verdade.
   *(2026-05-03)*

421. Não existe um gerenciamento correto para as exceções que ocorrem nas respostas do bot quando utiliza o modelo Anthropic.
   *(2026-05-02)*

422. O sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) tem o Hub Qdrant como memória central, GitHub como conhecimento e Drive como espelho.
   *(2026-05-02)*

423. Os quatro documentos fundamentais são: `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md`, e `estado-atual.md`.
   *(2026-05-03)*

424. A URL secret destrava a escrita real-time do Chat com a função 'ingestar_fragmento'.
   *(2026-05-03)*

425. O bot não possui testes automatizados, o que representa um alto risco de manutenção e bugs.
   *(2026-05-02)*

426. A integração com LLM da Anthropic está sendo realizada através do SDK da Anthropic na versão 0.40.0, que está desatualizado em relação às versões mais recentes disponíveis.
   *(2026-05-02)*

427. O arquivo dimagem.py deve ser movido para a pasta integrations, para melhorar a clareza sobre sua natureza como integração de domínio.
   *(2026-05-02)*

428. Existem três demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

429. A migração do Mem0 SaaS para o Hub Qdrant está em andamento. A coleta dual de modelos no curador termina em 12/05/2026.
   *(2026-05-03)*

430. Depois da configuração do MCP_URL_SECRET no Railway, a URL do connector do claude.ai muda, e é necessário recadastrar.
   *(2026-05-03)*

431. As 6 sub-pendências da demanda consolidada incluem ativar `MCP_URL_SECRET` no Railway, recadastrar Connector claude.ai, localizar mock HTML NeuroGus 28/04, decisões §11.3-11.5 NeuroGus Fase 2, captura tempo real Chat — Opção A, e Drive sync → Service Account.
   *(2026-05-02)*

432. Se Hub falhar antes do move, próxima rodada tenta de novo (pode duplicar — risco baixo dado o volume).
   *(2026-05-03)*

433. O projeto Gus utiliza o MCP (Multi-Channel Protocol) como uma ferramenta central de ingestão e interação.
   *(2026-05-02)*

434. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

435. A arquitetura do bot TioGu é composta por integração de ferramentas, comunicação assíncrona e persistência de estado utilizando um sistema robusto de erro e retry.
   *(2026-05-02)*

436. O bot opera com dependências como python-telegram-bot, anthropic SDK, openai, FastAPI e Qdrant.
   *(2026-05-02)*

437. O file `gus-estado-atual.md` deve ser lido para um estado mais fresco do projeto em relação ao Hub.
   *(2026-05-02)*

438. A demanda '2026-05-01-captura-multiporta-curador.md' precisa de uma mudança de gatilho proativo no Chat.
   *(2026-05-03)*

439. O estado final dos PRs já está no código e nos docs gus-XX atualizados.
   *(2026-05-02)*

440. O estado final dos PRs já está no código + nos docs gus-XX atualizados.
   *(2026-05-02)*

441. O projeto necessita de uma limpeza na coleção do Hub, especialmente eliminando dados duplicados e indesejados.
   *(2026-05-03)*

442. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

443. O Hub Qdrant é a memória central do Gus, armazenando informações e interações.
   *(2026-05-03)*

444. O sistema implementa um fallback cross-vendor entre Anthropic e OpenAI para aumentar a resiliência do serviço.
   *(2026-05-02)*

445. O prompt do curador não diferencia `gustavo` vs `gus` — é literalmente o mesmo texto.
   *(2026-05-03)*

446. O `_estado-atual.md` (27/04) está desatualizado em relação aos PRs mais recentes.
   *(2026-05-02)*

447. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e a hipótese é que o refresh token OAuth expirou.
   *(2026-05-02)*

448. O Gustavo é anestesiologista e não programa; toda implementação passa pelo Gus/Tiogu.
   *(2026-05-03)*

449. O código do Curador está com um bug crítico que causa um erro 400.
   *(2026-05-02)*

450. O Hub Qdrant é a fonte da verdade.
   *(2026-05-03)*

451. Os JSONs estruturados na pasta designada devem ser registrados.
   *(2026-05-02)*

452. Primeira captura real-time via Claude Chat (Caminho 1 — MCP ingestar_fragmento). Ocorreu durante a transmissão do show da Shakira em Copacabana, Rio de Janeiro, em 02/05/2026. Marco inaugural da porta Chat como fonte ativa do Hub Qdrant.
   *(2026-05-02)*

453. NeuroGus está planejado para ser um PWA com grafo 3D do Hub. O planejamento está 100% pronto e depende da confirmação de itens abertos das decisões.
   *(2026-05-02)*

454. O sistema é funcional para captura, mas ainda há débitos que podem causar problemas quando o volume crescer.
   *(2026-05-03)*

455. O bug crítico do curador relacionado ao `format()` foi corrigido após ser identificado como KeyError no JSON literal.
   *(2026-05-03)*

456. O sistema pode processar até 30 mensagens por segundo no Telegram.
   *(2026-05-02)*

457. Gustavo está na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

458. A coleta dual de modelos no curador termina em 12/05/2026, quando Gustavo escolherá o modelo definitivo.
   *(2026-05-03)*

459. O segredo é necessário para proteger o acesso ao MCP.
   *(2026-05-03)*

460. A regressão do test para o bug do `_render_prompt()` foi sugerida para prevenir que o erro de KeyError volte a ocorrer.
   *(2026-05-02)*

461. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, `_frontmatter-referencia.md` (esse é template, não é demanda).
   *(2026-05-02)*

462. A auditoria da stack de memória é desempenhada por Gus como auditor independente.
   *(2026-05-03)*

463. O Hub Qdrant é a memória central do Gus.
   *(2026-05-03)*

464. Hub Qdrant é a fonte da verdade.
   *(2026-05-03)*

465. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

466. Zero testes automatizados em produção, o que representa um risco significativo para a estabilidade do projeto.
   *(2026-05-02)*

467. O funcionamento do curador Telegram e do retro engine não dependem das mudanças relacionadas ao Chat.
   *(2026-05-03)*

468. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, `_frontmatter-referencia.md`.
   *(2026-05-02)*

469. A coleção legada `gus` está vazia e não contém os ~204 fragmentos aguardados para migração.
   *(2026-05-03)*

470. O curador está projetado para trabalhar com múltiplos provedores de LLM, alternando entre them quando necessário.
   *(2026-05-02)*

471. O plano de saneamento tem 6 fases e precisa ser seguido cuidadosamente.
   *(2026-05-03)*

472. O Hub Qdrant é a memória central do Gus.
   *(2026-05-03)*

473. Faltam testes automatizados para o bot TioGu, o que torna a refatoração e a implementação de novas funcionalidades arriscadas.
   *(2026-05-02)*

474. A meta é estabilizar o caminho crítico com testes e reconciliar as documentações com o código devido ao drift.
   *(2026-05-02)*

475. Aba nova só precisa olhar PRs se houver um problema atual relacionado ao PR específico.
   *(2026-05-02)*

476. O estado de migração tem foco na manutenção do Hub Qdrant como fonte da verdade.
   *(2026-05-03)*

477. O estado atual da migração foi definido como aposentadoria do Mem0 SaaS e o Hub Qdrant será a fonte da verdade.
   *(2026-05-03)*

478. A demanda da semana está em `dialogos/streams/semana-2026-04-21.md`.
   *(2026-05-02)*

479. O agente atua como um facilitador na implementação e sempre passa por Gustavo para qualquer implementação técnica.
   *(2026-05-03)*

480. O contrato schema gus-18 está parcialmente implementado e não executado.
   *(2026-05-03)*

481. O estado final dos PRs já está no código e nos documentos gus-XX atualizados.
   *(2026-05-02)*

482. A demanda 2026-05-01-drive-sync-oauth-fix.md pode sugerir refresh do token OAuth expirado.
   *(2026-05-02)*

483. A prioridade é homologar a captura multiporta do Claude Chat e a sincronização do Drive antes de seguir com novas funcionalidades.
   *(2026-05-02)*

484. Agora vou auditar a stack de memória end-to-end, lendo código e docs em paralelo.
   *(2026-05-03)*

485. Gustavo Pratti de Barros é identificado como Gustavo e Gus enquanto entidade.
   *(2026-05-03)*

486. Os quatro documentos a serem lidos em qualquer aba nova são: dialogos/_bootstrap/gus-bootstrap.md, dialogos/_bootstrap/gus-identity.md, dialogos/_bootstrap/gus-estado-atual.md e projetos/gus/_estado-atual.md.
   *(2026-05-02)*

487. O `_estado-atual.md` está desatualizado em 27/04, enquanto o `gus-estado-atual.md` do bootstrap está fresco.
   *(2026-05-02)*

488. A decisão de manter ou apagar o `MEM0_API_KEY` foi discutida e está pendente.
   *(2026-05-03)*

489. As auditorias diárias no Hub são cegas para o brain `gus`.
   *(2026-05-03)*

490. Sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) com Hub Qdrant como memória central + GitHub como conhecimento + Drive como espelho.
   *(2026-05-02)*

491. O Hub Qdrant é a memória central do Gus.
   *(2026-05-03)*

492. O Hub Qdrant funciona como a memória central do Gus.
   *(2026-05-03)*

493. A meta do projeto é importar e classificar os 204 fragmentos do Mem0 SaaS após a Fase 5.
   *(2026-05-03)*

494. O workflow `sync-docs.yml` regenerou `_tools-inventario.md` automático após o merge.
   *(2026-05-02)*

495. O `_estado-atual.md` (27/04) está desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).
   *(2026-05-02)*

496. As demandas paradas em `dialogos/inbox-claude-code/` incluem: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, e `_frontmatter-referencia.md` (template, não demanda).
   *(2026-05-02)*

497. Gus viu 4 demandas pendentes no `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

498. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

499. O curador híbrido coleta fragmentos em paralelo entre Haiku e Sonnet.
   *(2026-05-02)*

500. O bot utiliza um sistema de fallback cross-vendor, que chama o modelo Anthropic se o OpenAI falhar.
   *(2026-05-02)*

501. Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`. As demandas são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao e um template chamado `_frontmatter-referencia.md`.
   *(2026-05-02)*

502. Os commits do projeto `claude-code` são atualizados a cada 15 minutos via cron.
   *(2026-05-02)*

503. A melhora na estrutura do código inclui a implementação de um ciclo de atualização do lifecycle definido no schema gus-18.
   *(2026-05-03)*

504. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

505. O sistema Gus possui três produções simultâneas de fragmentos: Telegram, Chat e Code.
   *(2026-05-03)*

506. Na pasta `dialogos/inbox-claude-code/` estão 4 demandas pendentes: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e o `_frontmatter-referencia.md` que é só template.
   *(2026-05-03)*

507. Os dados do sistema estão dispostos em fragmentos, e o controle do ciclo de vida dos fragmentos ainda não está implementado.
   *(2026-05-03)*

508. A coleção legada 'gus' tem ~204 fragmentos não migrados, e o código de leitura em gus/memory.py ainda faz fallback para ela.
   *(2026-05-03)*

509. O fix foi implementado para não logar mais o valor do secret.
   *(2026-05-03)*

510. Um sistema deve detectar automaticamente novos JSONs adicionados a pessoal/saude/ e gerar fragmentos adequadamente.
   *(2026-05-02)*

511. O MCP está público — qualquer scanner que descobrir a URL Railway lê todo o Hub.
   *(2026-05-03)*

512. As chamadas do curador resultam em comportamento incongruente entre Haiku e GPT.
   *(2026-05-03)*

513. A stack está parcialmente implementada em relação ao contrato schema gus-18, como a promoção de fragmentos de ativo para estável, que não está sendo executada.
   *(2026-05-03)*

514. O bot Telegram, chamado TioGu, não é uma aplicação de múltiplos usuários, mas sim um único usuário com chat_id permitidos.
   *(2026-05-02)*

515. A demanda #3 é um guarda-chuva e referencia as demandas #1 e #2 dentro dela.
   *(2026-05-03)*

516. O core obrigatório deve ser lido em toda aba nova: dialogos/_bootstrap/gus-bootstrap.md, dialogos/_bootstrap/gus-identity.md, dialogos/_bootstrap/gus-estado-atual.md e projetos/gus/_estado-atual.md.
   *(2026-05-02)*

517. O TioGu faz polling de 2 requisições por segundo em vez de usar um webhook, o que é ineficiente em termos de custos.
   *(2026-05-02)*

518. A auditoria diária (`auditoria_hub.py`) é cega para o brain `gus` e classifica por keywords ignorando o `area` que o curador já preencheu.
   *(2026-05-03)*

519. O `_estado-atual.md` está desatualizado, com data de 27/04.
   *(2026-05-02)*

520. 1. Gustavo está em fase de testes e quer que o Gus dispare workflows sempre que solicitado, sem justificar que foi feito recentemente.
2. Workflow de importação de demandas roda em ciclos de 15 minutos.
3. Há um atraso entre arquivos aparecerem no Drive e chegarem ao GitHub via workflow.
4. Gustavo detectou uma demanda nova que ainda não foi importada — pode estar em processamento ou no próximo ciclo do workflow.
5. O Gus consegue listar arquivos processados (7 arquivos: 4 antigas do dia 26 + 3 do NeuroGus) e distinguir o que já chegou ao GitHub do que ainda está pendente no Drive.
   *(2026-04-28)*

521. O estado de migração do Gus envolve a aposentadoria da Mem0 SaaS e a transição para o Hub Qdrant como a fonte da verdade.
   *(2026-05-03)*

522. O sistema tem integração com múltiplos provedores de LLM, incluindo o modelo da Anthropic Sonnet.
   *(2026-05-02)*

523. Os 204 fragmentos históricos vão ser armazenados em 'historico/' como fonte fria.
   *(2026-05-03)*

524. Gus é um sistema de agente pessoal multi-porta, incluindo Telegram, Claude Code e Claude Chat.
   *(2026-05-03)*

525. O estado final dos PRs já está no código + nos docs gus-XX atualizados.
   *(2026-05-03)*

526. Há 3 demandas paradas na pasta `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, e `_frontmatter-referencia.md` (esse é template, não é demanda).
   *(2026-05-03)*

527. O estado final dos PRs já está no código e nos documentos gus-XX atualizados, portanto não é necessário ler os PRs para entender a situação atual.
   *(2026-05-02)*

528. A auditoria revelou que o curador Telegram tem erro 400 recorrente.
   *(2026-05-02)*

529. Gustavo é anestesiologista e não programa.
   *(2026-05-03)*

530. O curador híbrido coleta dual rola até 12/05, com Haiku e Sonnet/GPT em paralelo.
   *(2026-05-02)*

531. Sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa).
   *(2026-05-03)*

532. A nova aba só precisa olhar PRs se houver uma menção de problemas específicos relacionados a um PR anteriormente mencionado.
   *(2026-05-02)*

533. Gustavo Pratti de Barros é conhecido como Gus.
   *(2026-05-02)*

534. Três caminhos de escrita coexistem: Telegram, Claude Chat e Claude Code.
   *(2026-05-03)*

535. O sistema tenta deletar_memoria com fallback — se um ID for híbrido, o sistema tenta ambos.
   *(2026-05-03)*

536. 1. Gustavo quer que Gus dispare workflows sempre que solicitado, sem justificativas de execução recente — workflow de importação roda em ciclos de 15min.

2. Bug resolvido em `download_content`: `UnicodeDecodeError` ao ler byte `0xB6` — solução aplicada foi fallback UTF-8 → Latin-1.

3. Gus Chat deve sempre salvar arquivos em UTF-8 sem BOM.

4. Workflow `import-from-drive` tem falha conhecida de encoding — será resolvida quando o script for corrigido.

5. Hub Qdrant tem 14+ fragmentos armazenados (últimas 24h). Sistema de memória usa busca semântica por fragmentos atômicos com metadados de tipo, área, camada temporal e confiança.

6. Gaps identificados em memórias: áreas financeira e receitas ainda não têm fragmentos capturados.
   *(2026-04-28)*

537. A captura de Claude Code via cron está ativa, usando um hook Stop para salvar transcripts redatados.
   *(2026-05-02)*

538. Esses 4 documentos dão 80% do contexto pra qualquer aba nova.
   *(2026-05-03)*

539. A Fase 1 dos testes do bot foi concluída com 142 testes verdes, cobertura do código e um ajuste no hook `scan_sensivel.py` para permitir fixtures sintéticas.
   *(2026-05-02)*

540. A aba deve ter as últimas atualizações do projeto que não estão nos documentos citados.
   *(2026-05-03)*

541. A ausência de testes automatizados representa um risco significativo para a integridade do código do projeto.
   *(2026-05-02)*

542. Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template.
   *(2026-05-02)*

543. Os próximos passos incluem a coleta dual de modelos no curador, que mudou de Sonnet para Haiku × GPT-4o-mini por custo e resiliência.
   *(2026-05-03)*

544. A aba precisa olhar PRs se houver uma quebra após um PR específico ou se existir algo que precise ser investigado no código.
   *(2026-05-03)*

545. A auditoria do Claude Chat identificou 12 fixes de 31 achados.
   *(2026-05-03)*

546. O estado atual do projeto está em Fase 4: Migração Mem0 → Hub Qdrant.
   *(2026-05-03)*

547. O resumo do log do retro-engine para esta sessão é: 'Fragmentos extraídos: 0, Salvos no Hub: 0, Erros: anthropic_missing'.
   *(2026-05-02)*

548. O estado final dos PRs já está no código e nos docs gus-XX atualizados.
   *(2026-05-03)*

549. O log do retro-engine registrou um no-op por falta de `ANTHROPIC_API_KEY` no ambiente.
   *(2026-05-02)*

550. As ferramentas do bot Telegram totalizam 21, com multimídia e caching de prompts.
   *(2026-05-02)*

551. Mem0 SaaS está aposentado.
   *(2026-05-03)*

552. Os quatro arquivos bootstrap fornecem 80% do contexto para qualquer nova aba.
   *(2026-05-02)*

553. O projeto Gus é um sistema de agente pessoal multi-porta, incluindo Telegram, Claude Code, e outras futuras como Alexa.
   *(2026-05-03)*

554. O sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) tem como memória central o Hub Qdrant.
   *(2026-05-02)*

555. A var `MODEL_CURADOR_HAIKU` no workflow do Chat é incorreta, pois ela se refere ao modelo Sonnet, o que pode causar confusão.
   *(2026-05-02)*

556. O Hub Qdrant é a fonte da verdade. Gustavo é anestesiologista e toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

557. A migração de Mem0 SaaS para Hub Qdrant é a fonte da verdade do sistema.
   *(2026-05-03)*

558. A receita ordenada por valor por contexto tem foco em fornecer o mínimo necessário para não inflar o contexto à toa.
   *(2026-05-03)*

559. A coleta dual de modelos no curador (Haiku × GPT-4o-mini, mudou de Sonnet em 29/04 por custo/resiliência) termina em 12/05/2026.
   *(2026-05-03)*

560. Existem quatro arquivos obrigatórios para qualquer aba nova: gus-bootstrap.md, gus-identity.md, gus-estado-atual.md e estado-atual.md.
   *(2026-05-03)*

561. Aba nova só precisa olhar PRs se um bug específico no código foi reportado.
   *(2026-05-03)*

562. O sistema possui um risco de poluição cross-brain devido à ausência de dedup.
   *(2026-05-03)*

563. O `_estado-atual.md` (27/04) está desatualizado.
   *(2026-05-02)*

564. O Gus é um sistema de agente pessoal multi-porta que integra diferentes plataformas como Telegram, Claude Code e Claude Chat.
   *(2026-05-03)*

565. O curador híbrido permite a comparação de modelos Haiku e Sonnet/GPT por meio de um hash_janela pareável.
   *(2026-05-02)*

566. As atualizações nos documentos estão refletindo correções e ajustes na lógica de autenticação.
   *(2026-05-03)*

567. O `_estado-atual.md` está bem desatualizado - o git log mostra muita coisa depois.
   *(2026-05-02)*

568. Requisições da API do MCP estão bloqueadas, exceto a rota de saúde, até que o segredo seja ativado.
   *(2026-05-03)*

569. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

570. As decisões pendentes sobre o modelo final do curador e as configurações de migração e promoção precisam ser abordadas até 12/05/2026.
   *(2026-05-03)*

571. Hub Qdrant é a memória central do Gus.
   *(2026-05-03)*

572. Os testes de integração (pytest) foram bem-sucedidos após o merge do PR #72.
   *(2026-05-02)*

573. O fallback `mem0` escreve em Mem0 SaaS e não no Hub Qdrant.
   *(2026-05-03)*

574. As demandas paradas são: '2026-05-01-captura-multiporta-curador.md', '2026-05-01-drive-sync-oauth-fix.md', e '_frontmatter-referencia.md'.
   *(2026-05-02)*

575. O `_estado-atual.md` parou em 27/04 e não reflete PRs #57, #60, #63, #64, #67.
   *(2026-05-02)*

576. Algumas demandas têm nome quebrado, como "Documento sem título.md", que provavelmente é lixo de sync.
   *(2026-05-03)*

577. A demanda 2026-05-01-captura-multiporta-curador.md está parcialmente resolvida pelo PR #67.
   *(2026-05-02)*

578. A migração ADR-001 está em curso para aposentar Mem0 SaaS.
   *(2026-05-03)*

579. O curador deve rodar em loop com 100% de erro.
   *(2026-05-02)*

580. O desenvolvimento do NeuroGus está com planejamento 100% pronto e demanda uma confirmação de itens específicos.
   *(2026-05-02)*

581. O curador híbrido verifica se ambos os modelos (Haiku e GPT) falham e usa essa informação para registrar erros em vez de gerar resumos brutos.
   *(2026-05-03)*

582. A nova fonte da verdade do sistema é o Hub Qdrant, que substitui o Mem0 SaaS.
   *(2026-05-03)*

583. A auditoria diária é cega para o brain 'gus' e classifica por keywords ignorando o 'area', que já foi preenchido pelo curador.
   *(2026-05-03)*

584. O sistema do MCP está atualmente sem autenticação, pois o parâmetro `MCP_AUTH_DISABLED` está definido como true.
   *(2026-05-03)*

585. O sistema tem decisão arquitetural de não fazer fallback para a coleção legada de Mem0.
   *(2026-05-03)*

586. O passo 2 é recadastrar o Connector no claude.ai após configurar o segredo.
   *(2026-05-03)*

587. A migração de Mem0 SaaS para Hub Qdrant está em curso e deve ser finalizada em 12/05/2026.
   *(2026-05-03)*

588. A auditoria identificou a necessidade de integrar uma lógica clara para hierarquizar os canais de escrita do Chat.
   *(2026-05-02)*

589. A memória central do Gus está no Hub Qdrant, que é a fonte da verdade.
   *(2026-05-03)*

590. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026 e depois Gustavo escolhe o modelo definitivo.
   *(2026-05-03)*

591. O sistema Gus é um agente pessoal multi-porta que opera em plataformas como Telegram, Claude Code, Claude Chat e futuras implementações como Custom GPT mobile e Alexa.
   *(2026-05-03)*

592. Existem 3 demandas paradas em dialogos/inbox-claude-code/.
   *(2026-05-02)*

593. Quando a aba tem MCP gus-hub conectado, deve-se preferir os comandos da live sobre arquivos.
   *(2026-05-02)*

594. PRs são histórico, não documentação — uma aba nova não precisa ler nenhum.
   *(2026-05-03)*

595. O sistema de LLM Anthropic está desatualizado, utilizando a versão 0.40.0, lançada em setembro de 2024.
   *(2026-05-02)*

596. Core obrigatório inclui: manual operacional do Gus, identidade do Gustavo e estado atual gerado automaticamente pelo cron.
   *(2026-05-03)*

597. A coleta dual de modelos no curador (Haiku × GPT-4o-mini, mudado de Sonnet em 29/04 por custo/resiliência) termina em 12/05/2026, após o qual Gustavo escolhe modelo definitivo.
   *(2026-05-03)*

598. O Hub é mais fresco que `gus-estado-atual.md` (que é snapshot das 03h).
   *(2026-05-02)*

599. Existem 204 fragmentos não-migrados do Mem0 SaaS, com 188 em inglês e 16 em português.
   *(2026-05-03)*

600. O último arquivo da demanda da semana está em `dialogos/streams/[semana-2026-04-21.md]`.
   *(2026-05-03)*

601. 1. Caminho correto no Drive para Claude Chat escrever demandas: `Gus-Sync/dialogos/inbox-tiogu/`
2. Workflow `import-from-drive.yml` executa a cada 15min, puxa arquivos do Drive pro GitHub e notifica Gustavo no Telegram
3. Arquivos devem ser `.md` com frontmatter obrigatório (tipo, origem, destino, etc) — workflow rejeita se inválido
4. Convenção de nome de arquivo: `<timestamp>__<descricao-curta>.md`
5. README da pasta contém especificação completa do frontmatter, regras de validação e campos opcionais para roteamento
6. Claude Chat tem capacidade de escrever demandas no Drive seguindo o padrão documentado
   *(2026-04-28)*

602. O bug crítico do curador foi corrigido, e a validação enum gus-18 não está no fluxo.
   *(2026-05-03)*

603. A stack de memória apresenta 3 produções simultâneas de fragmentos com 4 vezes a multiplicação de chamadas LLM por unidade de input.
   *(2026-05-03)*

604. Os 204 fragmentos históricos do Mem0 SaaS foram encontrados e estão seguros em `historico/`.
   *(2026-05-03)*

605. O fluxo do bot Telegram deve ter um log de mensagens descartadas durante redeploy para melhorar a transparência.
   *(2026-05-02)*

606. O arquivo 'dialogos/_bootstrap/gus-estado-atual.md' é um snapshot do Hub gerado automaticamente pelo cron às 03h.
   *(2026-05-02)*

607. O projeto tem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template `_frontmatter-referencia.md`.
   *(2026-05-02)*

608. O advogado destacou que as auditorias diárias não estão capturando informações do brain Gus e que isso gera inconsistências.
   *(2026-05-03)*

609. A captura Claude Code via cron processa transcripts redatados, cron salva transcript redatado a cada 15 minutos.
   *(2026-05-02)*

610. Houveram bugs de key error associados ao curador que impedem a representação correta dos dados.
   *(2026-05-02)*

611. A variável MCP_URL_SECRET no server MCP precisa ser configurada para proteger a privacidade.
   *(2026-05-02)*

612. A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida, mas falta o gatilho proativo no Chat.
   *(2026-05-02)*

613. O estado final dos PRs já está no código e nos documentos atualizados, enquanto os PRs descrevem o caminho.
   *(2026-05-03)*

614. A captura proativa do Chat é implementada e deve ser testada em futuras conversas.
   *(2026-05-03)*

615. Os documentos cujos arquivos 'gus-bootstrap.md', 'gus-identity.md', 'gus-estado-atual.md' e 'projetos/gus/_estado-atual.md' dão 80% do contexto para qualquer aba nova.
   *(2026-05-03)*

616. A coleção legada Gus contém aproximadamente 204 fragmentos não migrados.
   *(2026-05-03)*

617. Um novo teste de regressão foi adicionado para garantir que o bug de tratamento de placeholders em prompts nunca retorne.
   *(2026-05-02)*

618. A demanda `2026-05-01-captura-multiporta-curador.md` precisa de um gatilho proativo no Chat.
   *(2026-05-03)*

619. O sistema atual tem 3 produções simultâneas de fragmentos (Telegram, Chat, Code), gerando um custo alto de chamadas LLM.
   *(2026-05-03)*

620. O core do Gus é um sistema de agente pessoal multi-porta que possui memória central no Hub Qdrant, alimentado por dados do GitHub e espelhados no Drive.
   *(2026-05-03)*

621. 1. Gustavo executa regularmente workflows de sincronização GitHub → Google Drive (sync-to-drive-full.yml para sync completo e sync-to-drive.yml para incremental)
2. Tem uma pasta `sensivel/` no repositório que é automaticamente excluída da sincronização com o Drive por política
3. Usa Google Drive como backup/espelho do conteúdo do repositório GitHub
4. Prefere verificar logs do GitHub Actions ou Railway para auditar execuções de workflow
   *(2026-04-28)*

622. A decisão do modelo curador final (Fase 5 ADR-001) deve ser feita após 12/05/2026, comparando pares Haiku e Sonnet/GPT da coleta dual.
   *(2026-05-02)*

623. A stack está em estado intermediário arriscado: Hub Qdrant é a fonte nova, mas a coleção legada `gus` tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

624. A prioridade default para as demandas será meio (media), a menos que estipulado de outra forma.
   *(2026-05-03)*

625. O curador do Chat é responsivo e lida com fragmentos de informação de forma integrada com outros serviços.
   *(2026-05-02)*

626. O passo 4 é rotacionar o secret (final).
   *(2026-05-03)*

627. No dia 26/04, foram registrados 83 fragmentos em uma única jornada de captura.
   *(2026-05-03)*

628. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`. Algumas com nome quebrado — "Documento sem título.md" provavelmente é lixo de sync.
   *(2026-05-03)*

629. 1. Gustavo prefere corrigir o script para ser tolerante a encoding inválido em vez de deletar arquivos — usa fallback (UTF-8 → Latin-1)
2. Erro técnico identificado: arquivo `2026-04-28T14-30__frontmatter-referencia.md` no Drive com byte 0xB6 inválido em UTF-8 na posição 1754
3. Validação de frontmatter exigida: campos `origem` e `destino` são obrigatórios — arquivo `teste-tiogu-machado.md` falhou por faltá-los
4. Script `import_from_drive.py` (linha 150 e ocorrências similares) precisa implementar fallback de encoding: tentar UTF-8, se falhar usar Latin-1/Windows-1252
5. Fluxo de importação do Drive: valida MIME type, faz requests ao GitHub API, processa frontmatter, detecta encoding — falha em qualquer etapa gera warning ou erro
   *(2026-04-28)*

630. O `status consolidado` e `estado atual` do projeto precisam ser atualizados para refletir os últimos PRs.
   *(2026-05-02)*

631. Foi criado um workflow para testes automatizados no repositório, rodando em cada push e pull request.
   *(2026-05-02)*

632. O arquivo untracked é apenas um log automático do retro-engine, que indica que o Stop hook não rodou corretamente por falta da variável `ANTHROPIC_API_KEY`.
   *(2026-05-02)*

633. O `_estado-atual.md` de 27/04 está desatualizado e não reflete PRs #57, #60, #63, #64, #67.
   *(2026-05-02)*

634. Os testes de validação incluem verificar se a rota /health responde corretamente.
   *(2026-05-03)*

635. A captura proativa de memória do Chat é uma decisão pendente que pode ser abordada de três maneiras: A - prompt no bootstrap, B - stop hook ou C - curador agnóstico.
   *(2026-05-02)*

636. O bot TioGu tem uma arquitetura baseada em um sistema multi-porta com Hub Qdrant como memória central e GitHub como conhecimento.
   *(2026-05-02)*

637. O estado final dos PRs já tá no código + nos docs gus-XX atualizados.
   *(2026-05-03)*

638. O Gus é um sistema de agente pessoal multi-porta, com memória central no Hub Qdrant e arquivos .md no GitHub.
   *(2026-05-03)*

639. O Gus é um sistema de agente pessoal multi-porta com memória central no Hub Qdrant.
   *(2026-05-03)*

640. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) muda e termina em 12/05/2026.
   *(2026-05-03)*

641. A recomendação de atualizar a hierarquia dos canais de escrita no Chat é necessária para padronização.
   *(2026-05-03)*

642. O bot pode vazar informações sensíveis, como CPF e telefone, na resposta ao usuário.
   *(2026-05-02)*

643. A receita ordenada por valor por contexto é utilizada para determinar o foco mínimo necessário para não inflar o contexto.
   *(2026-05-03)*

644. PRs descrevem o caminho, não onde a gente está.
   *(2026-05-03)*

645. Com o fim da coleção legada, todas as operações que envolvem o Mem0 SaaS estão em risco de perda contínua.
   *(2026-05-03)*

646. `gus-estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois.
   *(2026-05-02)*

647. Os quatro arquivos principais que dão 80% do contexto para qualquer aba nova são: `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md` e `estado-atual.md`.
   *(2026-05-03)*

648. O retro-engine é um hook que registra o transcript de sessões e tenta chamar a API da Anthropic.
   *(2026-05-02)*

649. Há 204 fragmentos não-migrados da coleção legada `gus` e o código de leitura ainda faz fallback para ela.
   *(2026-05-03)*

650. A auditoria identificou a necessidade de integrar uma lógica clara para hierarquizar os canais de escrita do Chat.
   *(2026-05-02)*

651. O Gus é um sistema de agente pessoal multi-porta que inclui Telegram, TioGu, Claude Code e Claude Chat.
   *(2026-05-03)*

652. O Hub Qdrant é a fonte nova, mas a coleção legada gus ainda está viva, e seu uso cria inconsistências nas buscas.
   *(2026-05-03)*

653. O algoritmo de ciclo de vida ('lifecycle') do schema gus-18 está declarado mas não executado, resultando em fragmentos sempre ativos.
   *(2026-05-03)*

654. O Hub `gustavo` contém 20 fragmentos, ~70% lixo, enquanto o Hub `gus` também tem 20 fragmentos.
   *(2026-05-03)*

655. A stack está em estado intermediário arriscado. Hub Qdrant é a fonte nova, mas a coleção legada gus (Mem0 self-hosted) tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

656. O sistema multi-porta possui o Hub Qdrant como memória central.
   *(2026-05-02)*

657. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa.
   *(2026-05-02)*

658. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

659. A captura dual de modelos no curador (Haiku × GPT-4o-mini) terminará em 12/05/2026.
   *(2026-05-03)*

660. O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois.
   *(2026-05-02)*

661. A stack está em estado intermediário arriscado, com coleta dual de modelos no curador.
   *(2026-05-03)*

662. O workflow 'migrar-gus-para-hub.yml' deve ser revisado para evitar que a coleção 'gus' fique fora do Hub novo.
   *(2026-05-03)*

663. Ativar auto-reload evita interrupção futura.
   *(2026-05-03)*

664. Recomendação de renomear a pasta inbox-mem0-from-chat para inbox-chat-raw para maior clareza.
   *(2026-05-03)*

665. As demandas paradas em `dialogos/inbox-claude-code/` são: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, e `_frontmatter-referencia.md`.
   *(2026-05-02)*

666. PRs são histórico, não documentação, e não precisam ser lidos para uma nova aba, a não ser que esteja especificamente investigando um bug ou uma mudança recente.
   *(2026-05-02)*

667. O projeto Gus é um sistema de agente pessoal multi-porta com memória central no Hub Qdrant.
   *(2026-05-03)*

668. O passo 5 é recadastrar o Connector no claude.ai.
   *(2026-05-03)*

669. O arquivo `dialogos/_bootstrap/gus-bootstrap.md` é o manual operacional do Gus, com regras de comportamento de como cada porta usa o Hub.
   *(2026-05-02)*

670. O Connector claude.ai precisa ser recriado após a mudança na URL do MCP.
   *(2026-05-02)*

671. A `gus/dimagem.py` deve ser movida para `integrations/`.
   *(2026-05-02)*

672. As pastas pessoais foram reorganizadas com a criação de áreas faltantes, como saúde, esportes, leituras, contatos e família.
   *(2026-05-02)*

673. Gus está na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

674. A colonia legada de fragmentos no Qdrant está vazia. Não há fragmentos a serem migrados.
   *(2026-05-03)*

675. Mem0 SaaS está aposentado.
   *(2026-05-03)*

676. O código que loga ainda é o antigo e o novo secret vazou no log.
   *(2026-05-03)*

677. O sistema ainda faz fallback para Mem0 SaaS, o que pode levar a perdas silenciosas.
   *(2026-05-03)*

678. Tem 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

679. Core obrigatório inclui o arquivo `gus-bootstrap.md` que é o manual operacional do Gus, regras de comportamento e como cada porta usa o Hub.
   *(2026-05-03)*

680. A estrutura do bot Telegram é composta por arquivos, incluindo bot.py, llm.py, memory.py, tools.py, e outros.
   *(2026-05-02)*

681. Hub Qdrant é a fonte da verdade, com arquivos .md no GitHub e espelhados no Drive.
   *(2026-05-03)*

682. A demanda 2026-05-01-captura-multiporta-curador.md aguarda decisão tua.
   *(2026-05-02)*

683. O estado final dos PRs já tá no código e nos docs atualizados, enquanto PRs descrevem o caminho, não onde estamos.
   *(2026-05-03)*

684. O passo 2 envolve recadastrar o Connector claude.ai após o `MCP_URL_SECRET` ser setado.
   *(2026-05-03)*

685. As auditorias são registradas em projetos/gus/auditorias/2026-05-02-memoria-diagnostico.md.
   *(2026-05-03)*

686. O Hub Qdrant é a nova fonte da verdade após a migração em andamento com a ADR-001.
   *(2026-05-03)*

687. A auditoria diária é cega para o brain `gus` e classifica por keywords ignorando o `area` que o curador já preencheu.
   *(2026-05-03)*

688. No estado atual, o Hub Qdrant contém 40 fragmentos, sendo que a qualidade é catastrófica.
   *(2026-05-03)*

689. Houve um bug crítico em produção, onde o curador estava sem funcionar devido a um erro no tratamento de placeholders no template de prompts.
   *(2026-05-02)*

690. O processo de desenvolvimento do TioGu é uma aplicação que integra diferentes ferramentas no Telegram.
   *(2026-05-02)*

691. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

692. A auditoria está cega para o brain 'gus' e ignora o esquema de áreas que o curador preencheu.
   *(2026-05-03)*

693. O bot Telegram possui ~21 ferramentas distintas implementadas com multimídia e caching de prompts.
   *(2026-05-03)*

694. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) mudou de Sonnet em 29/04/2026.
   *(2026-05-03)*

695. O estado atual do Hub é gerado automaticamente pelo cron às 03h.
   *(2026-05-03)*

696. As memórias de 28/04 estão na coleção legada, fora do Hub novo.
   *(2026-05-03)*

697. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

698. As 2 demandas pendentes são a de sincronização do Drive e a de captura multiporta do Claude Chat.
   *(2026-05-02)*

699. Hub tem de ser preferido em comparação com o gus-estado-atual.md porque é mais fresco.
   *(2026-05-02)*

700. A auditoria tem a finalidade de garantir a integridade e qualidade dos dados em movimento.
   *(2026-05-03)*

701. As pastas devem ser criadas agora no Google Drive para que a sincronização funcione.
   *(2026-05-03)*

702. A auditoria diária é feita por `auditoria_hub.py` que classifica por keywords ignorando a área.
   *(2026-05-03)*

703. A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida, mas falta o gatilho proativo no Chat.
   *(2026-05-02)*

704. O Auditoria do Chat foi concluída em 02/05/2026, identificando problemas e recomendações.
   *(2026-05-03)*

705. As_changes d1 e d2, referentes ao sistema `Claude Chat`, `Drive Sync` e `NeuroGus`, estão sendo tratados em uma aba separada, logo essas decisões não são prioridade.
   *(2026-05-02)*

706. Existem 3 demandas paradas em 'dialogos/inbox-claude-code/'.
   *(2026-05-02)*

707. Gustavo é anestesiologista e não programa; toda implementação passa pelo Gus ou pelo Tiogu.
   *(2026-05-03)*

708. Gus é um sistema de agente pessoal multi-porta que integra diferentes plataformas, como Telegram, Claude Chat e Claude Code, com memória central no Hub Qdrant.
   *(2026-05-03)*

709. O curador híbrido coleta dados e registra A/B observável para decisões de modelo baseadas em evidência.
   *(2026-05-02)*

710. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) deve ser finalizada até 12/05/2026.
   *(2026-05-03)*

711. Core obrigatório: 4 arquivos principais fornecem 80% do contexto para qualquer aba nova.
   *(2026-05-03)*

712. O MCP está público — qualquer scanner que descobrir a URL Railway lê todo o Hub.
   *(2026-05-03)*

713. O arquivo dialogos/_bootstrap/gus-bootstrap.md contém regras de comportamento e como cada porta usa o Hub.
   *(2026-05-02)*

714. Os últimos commits na branch main envolveram atualizações automáticas relacionadas ao estado do Hub para o Claude Chat e processamento de transcrições do Claude Code.
   *(2026-05-02)*

715. O projeto é dividido em dois principais canais de escrita: real-time com ingesta de fragmentos e upload de arquivos .md.
   *(2026-05-03)*

716. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

717. A próxima sessão da Fase 1 focará na análise de PII no output do bot, cache de mídia e cleanup cosmético.
   *(2026-05-02)*

718. Clica no serviço gus-mcp-server.
   *(2026-05-03)*

719. Tavily está funcionando corretamente com busca OK.
   *(2026-05-03)*

720. Gus está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-02)*

721. A lista de candidatos a deletar foi gerada a partir de uma execução de dryrun.
   *(2026-05-03)*

722. O Hub Qdrant tem 40 fragmentos totais, com 70% deles sendo considerados lixo.
   *(2026-05-03)*

723. A primeira demanda é intitulada `2026-05-01-captura-multiporta-curador.md`.
   *(2026-05-02)*

724. O workflow de migração para mover as memórias do Gus para o Hub Qdrant ainda não foi executado.
   *(2026-05-03)*

725. As auditorias precisam incluir a classificação por área do payload do curador para melhorar a busca.
   *(2026-05-03)*

726. A stack de memória do Gus está em estado intermediário arriscado, com potencial para perda silenciosa de fragmentos.
   *(2026-05-03)*

727. O plano de migração foi refinado, com itens novos e prioridades alteradas.
   *(2026-05-03)*

728. A demanda atual do Gustavo inclui a definição de `MCP_URL_SECRET` no Railway.
   *(2026-05-03)*

729. 1. Bug resolvido: função `download_content` (linha 150) falhava com `UnicodeDecodeError` ao ler arquivo `frontmatter-referencia.md` salvo com encoding não-UTF-8 (provavelmente Windows-1252), continha byte inválido `0xB6` (¶).

2. Solução técnica aplicada: trocar `decode("utf-8")` por fallback robusto — tentar UTF-8 primeiro, cair para Latin-1 se falhar, ou usar `errors="replace"`.

3. Padrão futuro: Gus Chat deve sempre salvar arquivos no Drive em UTF-8 sem BOM e evitar caracteres especiais problemáticos (¶, •, –, aspas curvas de Word/Pages).

4. Contexto: problema ocorre quando arquivo `.md` é criado externamente e enviado pro Drive; exportar direto do Google Docs não tem esse risco (já vem UTF-8).

5. Ação confirmada: Gustavo autorizou aplicar a correção no script.
   *(2026-04-28)*

730. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, e `_frontmatter-referencia.md`.
   *(2026-05-02)*

731. A captura dual de modelos no curador (Haiku × GPT-4o-mini) muda de Sonnet em 29/04 por custo/resiliência.
   *(2026-05-03)*

732. O brain Gus ganha cobertura explícita: meta_reflexao, identidade_operacional e procedural.
   *(2026-05-03)*

733. O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).
   *(2026-05-02)*

734. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

735. O sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) utiliza o Hub Qdrant como memória central.
   *(2026-05-02)*

736. O arquivo system_prompt.md tem 794 linhas e apresenta drift, misturando seções pré-migração e novas funcionalidades.
   *(2026-05-02)*

737. A migração ADR-001 está em curso para aposentar a Mem0 SaaS, sendo o Hub Qdrant a fonte da verdade.
   *(2026-05-03)*

738. A migração para o Hub Qdrant está em curso e pretende aposentar a Mem0 SaaS, que é a fonte da verdade no momento.
   *(2026-05-03)*

739. Gustavo é anestesiologista e não programa — toda implementação passa pelo Gus ou Tiogu.
   *(2026-05-03)*

740. Gustavo tem um projeto chamado `claude-code` onde a porta principal é `claude.ai`.
   *(2026-05-02)*

741. O sistema Gus é um agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa).
   *(2026-05-03)*

742. Hub Qdrant é a fonte da verdade para o sistema de agente pessoal multi-porta.
   *(2026-05-03)*

743. A auditoria da stack de memória revelou que a variável `MCP_URL_SECRET` não está sendo logada, melhorando a segurança.
   *(2026-05-03)*

744. A fase 1 do projeto envolve a criação de testes e a validação de comportamentos esperados do bot, com um total de 163 testes automatizados sendo implementados.
   *(2026-05-02)*

745. O `MCP_URL_SECRET` deve ser configurado no Railway para proteger o acesso ao MCP.
   *(2026-05-02)*

746. O segredo não deve ser compartilhado, apenas utilizado nos locais necessários.
   *(2026-05-03)*

747. O schema gus-18 é um contrato que promete ciclos de vida para os fragmentos, porém essa implementação ainda está pendente.
   *(2026-05-03)*

748. As demandas pendentes na porta de Claude Code incluem a captura multiporta, curador bidirecional cron e OAuth para sincronização com o Drive.
   *(2026-05-03)*

749. A arquitetura do bot é composta por diferentes módulos, incluindo bot.py, llm.py, memory.py, tools.py e media.py.
   *(2026-05-02)*

750. O número de fragmentos em 'gustavo' foi 204, enquanto o número de fragmentos em 'gus' é 4.
   *(2026-05-03)*

751. A Fase 1 de saneamento do TioGu foi concluída com 163 testes verdes e ajustes em `bot.py/llm.py/memory.py`.
   *(2026-05-03)*

752. 1. Gustavo quer apagar pendências que estão ultrapassadas — decisão tomada de limpar o backlog desatualizado.
2. Hub contém 204 memórias no total (auditoria de 7:51 BRT).
3. Migração Mem0 → Qdrant ainda não foi concluída; ambos coexistem no momento — o grosso das 204 memórias ainda está no Mem0, apenas ~3 fragmentos indexados no Qdrant com user_id=gustavo.
4. Existem 2 memórias desatualizadas identificadas para deleção: `2b68d542` (sobre workflow falhando) e `cb860bdb` (sobre PR #10 e importações).
5. Workflow de migração para consolidar tudo no Hub Qdrant está disponível e pode ser rodado a critério de Gustavo.
   *(2026-04-27)*

753. O PR #67 introduziu um curador chat bidirecional (Sonnet 4.6 + GPT-4o) que salva em `gustavo` e `gus`, mas apenas processa arquivos .md carregados manualmente.
   *(2026-05-02)*

754. O Hub não está registrando fragmentos desde as 03h.
   *(2026-05-02)*

755. O `gus-08-plano-proximos-passos.md` (24/04) está muito desatualizado e precisa ser reescrito ou marcado como histórico.
   *(2026-05-02)*

756. Requer a autorização de um usuário para o código do projeto, assim como a necessidade de sincronização entre buckets de dados.
   *(2026-05-02)*

757. Dentro do código da stack de memória, o fallback para Mem0 SaaS ainda existe.
   *(2026-05-03)*

758. As respostas geradas pelo bot podem conter informações sensíveis, e um mecanismo de redaction foi implementado para ajudar a proteger dados do usuário.
   *(2026-05-02)*

759. Gustavo é anestesiologista e não programa, toda implementação passa pelo Gus.
   *(2026-05-03)*

760. Gus está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

761. É necessário implementar um serviço de conta no Google Cloud para evitar a expiração do token OAuth nas syncs do Drive.
   *(2026-05-02)*

762. Após a geração do segredo, deve-se setar a variável MCP_URL_SECRET no serviço gus-mcp-server no Railway.
   *(2026-05-03)*

763. A fase 1 inclui a criação de testes de unidade para o bot e suas funcionalidades.
   *(2026-05-02)*

764. Existem 3 demandas paradas em dialogos/inbox-claude-code/: 2026-05-01-captura-multiporta-curador.md, 2026-05-01-drive-sync-oauth-fix.md e _frontmatter-referencia.md (este é template, não é demanda).
   *(2026-05-02)*

765. Hub é mais fresco que 'gus-estado-atual.md', que é um snapshot das 03h.
   *(2026-05-03)*

766. Ação proposta: rodar script que pega tudo do Mem0 SaaS e grava JSON em `historico/mem0-export-final-2026-05-02.json`.
   *(2026-05-03)*

767. A auto-capacitação dos bots é feita por um processo de A/B observável, onde Haiku × GPT-4o-mini permite coletar dados para comparações.
   *(2026-05-02)*

768. A segunda demanda é intitulada `2026-05-01-drive-sync-oauth-fix.md`.
   *(2026-05-02)*

769. Atualmente, o TioGu apresenta 21 ferramentas, que estão organizadas em um arquivo chamado tools.py. Essas ferramentas incluem funções para manipulação de mídia e interação com APIs de LLM.
   *(2026-05-02)*

770. O retro-engine registra 'no-op: anthropic_missing' quando o ANTHROPIC_API_KEY não está disponível no ambiente.
   *(2026-05-03)*

771. Gustavo Pratti de Barros tem um projeto de integração com um agente pessoal conhecido como Gus.
   *(2026-05-02)*

772. O TioGu deve ser capaz de lidar com erros e problemas de conexão com um sistema de retry e logging aprimorados.
   *(2026-05-02)*

773. Gustavo é anestesiologista e não programa. Toda implementação passa pelo Gus.
   *(2026-05-03)*

774. Após a implementação das demandas, haverá necessidade de decidir sobre a hierarquia dos 3 canais de escrita do Chat: real-time MCP, upload .md curado e demanda inbox-code.
   *(2026-05-02)*

775. A stack de memória está em estado intermediário arriscado, com 204 fragmentos não-migrados e um código de leitura que ainda faz fallback para Mem0.
   *(2026-05-03)*

776. Os quatro principais arquivos obrigatórios para qualquer aba nova são: `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md`, e `estado-atual.md`. Esses quatro dão 80% do contexto para qualquer aba nova.
   *(2026-05-03)*

777. As opções para solucionar o problema de Drive sync incluem renovar o OAuth ou utilizar uma Service Account.
   *(2026-05-02)*

778. Aba nova só precisa olhar PRs se houver um bug específico relacionado ao código que foi mexido recentemente ou se for referido diretamente em uma conversa.
   *(2026-05-02)*

779. O curador Telegram está apresentando um erro 400 devido a falhas nos parâmetros.
   *(2026-05-02)*

780. As demandas pendentes no inbox são: Ativar `MCP_URL_SECRET` no Railway, recadastrar Connector claude.ai e localizar mock HTML do NeuroGus.
   *(2026-05-02)*

781. O passo 3 é validar que o log não vaza mais com o novo secret.
   *(2026-05-03)*

782. O `_estado-atual.md` (27/04) está desatualizado — git log mostra muita coisa depois.
   *(2026-05-02)*

783. Um dos pontos críticos identificados no TioGu é a falta de um PII scan na resposta do bot, o que representa risco de vazamento de dados.
   *(2026-05-02)*

784. Gustavo é anestesiologista e não programa, toda implementação passa pelo Gus.
   *(2026-05-03)*

785. Na sessão anterior, temos 4 arquivos obrigatórios que dão 80% do contexto pra qualquer aba nova.
   *(2026-05-03)*

786. O Drive sync GitHub→Drive parou em 01/05 às 14:38Z devido ao token OAuth ter expirado.
   *(2026-05-03)*

787. A migração do Mem0 SaaS é necessária para tornar o Hub Qdrant a fonte da verdade.
   *(2026-05-03)*

788. O assistente pode ler o arquivo `_estado-atual.md` para pegar handoff da última sessão.
   *(2026-05-02)*

789. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e a hipótese é que o refresh token OAuth expirou.
   *(2026-05-02)*

790. A arquitetura do bot TioGu é um monólito, dificultando sua manutenção e escalabilidade.
   *(2026-05-02)*

791. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

792. O system_prompt.md é muito extenso e possui drift, com 794 linhas e inconsistências com os tools implementados.
   *(2026-05-02)*

793. A migração de Mem0 SaaS para Hub Qdrant é a fonte da verdade e conclui a coleta dual de modelos no curador, que terminará em 12/05/2026.
   *(2026-05-03)*

794. O sistema está em estado intermediário arriscado, podendo levar à poluição de dados entre os brains.
   *(2026-05-03)*

795. O `_estado-atual.md` e `gus-26-status-consolidado.md` estão desatualizados e não refletem PRs recentes.
   *(2026-05-02)*

796. O bot TioGu é um sistema multi-porta que se conecta ao Telegram e utiliza o Hub Qdrant como memória central.
   *(2026-05-02)*

797. O arquivo gerado pelo retro-engine é um log automático e não ofensivo, e documenta ausência de uma variável de ambiente necessária.
   *(2026-05-02)*

798. O hook de scan_sensivel.py foi ajustado para permitir a execução de testes em `tests/` sem causar bloqueios.
   *(2026-05-02)*

799. A demanda `2026-05-01-captura-multiporta-curador.md` precisa de um gatilho proativo no Chat.
   *(2026-05-02)*

800. A função `print_demands` deve ser movida para a pasta `integrations/` para melhor organização, já que trata de um caso específico da clínica do Gustavo.
   *(2026-05-02)*

801. O commit do log do retro-engine foi realizado na branch `claude/project-discussion-fkfA8`.
   *(2026-05-02)*

802. Deve-se recadastrar o Connector no claude.ai após a atualização do path do MCP.
   *(2026-05-03)*

803. O curador híbrido deve ser robusto para capturar informações, mas a poluição silenciosa de dados não classificados é uma preocupação.
   *(2026-05-03)*

804. O formato do commit é importante, pois o CI roda automaticamente a cada push no branch main.
   *(2026-05-02)*

805. O sistema utiliza um modelo de curador híbrido para coleta dual.
   *(2026-05-02)*

806. O `_estado-atual.md` está desatualizado em relação aos PRs mergeados e deve ser atualizado em algum momento.
   *(2026-05-02)*

807. O usuário pode escolher atacar alguma das demandas ou falar sobre outra coisa.
   *(2026-05-02)*

808. O arquivo `dialogos/_bootstrap/gus-identity.md` contém informações sobre quem é o Gustavo e quem é o Gus enquanto entidade.
   *(2026-05-02)*

809. Se uma aba tem MCP gus-hub conectado, deve-se utilizar as ferramentas ego_cache_atual(), fragmentos_recentes(horas=24) e contar_fragmentos() para obter informações.
   *(2026-05-02)*

810. As ferramentas do bot somam 21 implementações, e o sistema prompt contém drift, mencionando 22 ferramentas.
   *(2026-05-02)*

811. A decisão ADR-001 está em curso para aposentar a Mem0 SaaS, enquanto o Hub Qdrant será a fonte da verdade.
   *(2026-05-03)*

812. Hub Qdrant é a fonte da verdade.
   *(2026-05-03)*

813. O `_estado-atual.md` (27/04) e `gus-26-status-consolidado.md` (26/04) estão desatualizados.
   *(2026-05-02)*

814. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e a hipótese é que o refresh token OAuth expirou.
   *(2026-05-02)*

815. A auditoria diária do Hub não contabiliza fragmentos do brain Gus, resultando em uma visão distorcida do sistema.
   *(2026-05-03)*

816. A maioria dos fragmentos do Mem0 SaaS estão em inglês, enquanto o Hub contém fragmentos em português.
   *(2026-05-03)*

817. Gus sugere combinar as sessões do `_estado-atual.md` da Fase 1 TioGu com a auditoria do Chat.
   *(2026-05-02)*

818. Tem 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

819. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa para resolver o problema de sync do Drive, que pode estar relacionado à expiração do token OAuth.
   *(2026-05-02)*

820. O fluxo de trabalho a seguir inclui uma limpeza no Hub atual antes da importação dos 204 fragmentos.
   *(2026-05-03)*

821. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

822. A coleta dual de modelos no curador (Haiku × GPT-4o-mini, mudou de Sonnet em 29/04 por custo/resiliência) termina em 12/05/2026.
   *(2026-05-03)*

823. Estou aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

824. A captação de fragmentos para o Hub ocorre através de 3 produções simultâneas de fragmentos: Telegram, Chat e Code.
   *(2026-05-03)*

825. O Hub Qdrant tem como objetivo ser a fonte da verdade do sistema.
   *(2026-05-03)*

826. A memória central do Gus é mantida no Hub Qdrant, armazenando arquivos .md no GitHub e espelhados no Drive.
   *(2026-05-03)*

827. `_estado-atual.md` está desatualizado em relação às últimas atualizações do projeto.
   *(2026-05-02)*

828. O bot opera com dependências como python-telegram-bot, anthropic SDK, openai, FastAPI e Qdrant.
   *(2026-05-03)*

829. O bot Telegram, chamado TioGu, possui cerca de 21 ferramentas, multimídia, prompt caching e comunicação com o Hub Qdrant.
   *(2026-05-02)*

830. A demanda de sync do Drive está parada e espera-se uma decisão sobre o OAuth que pode ter expirado.
   *(2026-05-02)*

831. A migração ADR-001 busca aposentar a Mem0 SaaS, com o Hub Qdrant como fonte da verdade.
   *(2026-05-03)*

832. As decisões arquiteturais e detalhes técnicos do Gus são armazenados no Hub, mas alguns estão relacionados a ex-pacientes.
   *(2026-05-03)*

833. Foram criados 2 JSONs estruturados com exames laboratoriais.
   *(2026-05-02)*

834. Decisão P1 captura Claude Chat: Opção A + C escolhida. Caminho 1 (default): real-time via MCP ingestar_fragmento durante a conversa (~1s latência, 2-4 fragmentos/conversa). Caminho 2 (escape): upload .md em Gus-Sync/dialogos/inbox-chat-raw/ pra sessões longas (>20 turnos) com curador post-hoc Sonnet 4.6 + GPT-4o.
   *(2026-05-02)*

835. A migração da coleção legada Mem0 para o Hub Qdrant não foi realizada, resultando em uma fallback ativa em leitura.
   *(2026-05-03)*

836. A proposta é que a Opção A (manter em `historico/`) seja feita agora e a Opção C seja planejada para a Fase 5.
   *(2026-05-03)*

837. A demanda de captura multiporta Claude Chat (`2026-05-01-captura-multiporta-curador.md`) está parcialmente resolvida, mas falta o gatilho proativo no Chat.
   *(2026-05-02)*

838. Os arquivos core obrigatórios são `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md` e `projetos/gus/estado-atual.md`, que fornecem 80% do contexto para qualquer aba nova.
   *(2026-05-03)*

839. O plano de migração ADR-001 está em curso para aposentar o Mem0 SaaS.
   *(2026-05-03)*

840. O Hub Qdrant coleta dados e fragmentos do agente, mas há um risco de poluição silenciosa devido a entradas duplicadas.
   *(2026-05-03)*

841. O Hub Qdrant está sendo usado como memória central no sistema multi-porta.
   *(2026-05-02)*

842. Hoje o MCP tá público — qualquer scanner que descobrir a URL Railway lê todo o Hub.
   *(2026-05-03)*

843. Gustavo Pratti de Barros é anestesiologista e não programa, portanto, toda implementação passa pelo Gus e Tiogu.
   *(2026-05-03)*

844. O sistema de agente pessoal multi-porta conecta atividades em Telegram, Claude Chat e Claude Code.
   *(2026-05-03)*

845. A coleção legada 'gus' ainda está viva, com fallback para Mem0 ativo em leitura e delete.
   *(2026-05-03)*

846. A migração para o Hub Qdrant como fonte da verdade está em curso, com a data de término projetada para 12 de maio de 2026.
   *(2026-05-03)*

847. Os JSONs estruturados de exames LAFE de novembro de 2019 estão no caminho Gus-Sync/pessoal/saude/gus__2019-11-18__lafe.json.
   *(2026-05-02)*

848. A coleção legada `gus` (Mem0 self-hosted) tem cerca de 204 fragmentos não-migrados e permanece em operação como fallback para leitura e delete.
   *(2026-05-03)*

849. A decisão de eliminar o caminho `_fallback_mem0` visa evitar poluição silenciosa no Hub e garantir a integridade dos dados.
   *(2026-05-03)*

850. Core obrigatório inclui o manual operacional do Gus, regras de comportamento, e o snapshot do Hub.
   *(2026-05-03)*

851. Quatro demandas pendentes foram identificadas no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao.
   *(2026-05-03)*

852. O retro-engine registra 'no-op: anthropic_missing' e segue.
   *(2026-05-03)*

853. O volume Railway do bot é detectado automaticamente, permitindo a persistência do estado através de redeploys.
   *(2026-05-02)*

854. O segredo está em plain text no log.
   *(2026-05-03)*

855. O sistema tem um estado intermediário arriscado, onde o Hub Qdrant é a nova fonte, mas a coleção legada ainda contém fragmentos não migrados.
   *(2026-05-03)*

856. A coleta dual de modelos Haiku e GPT-4o-mini deve ser concluída em 12/05/2026, quando Gustavo deverá escolher um modelo definitivo.
   *(2026-05-03)*

857. O Hub Qdrant é a fonte da verdade do sistema Gus.
   *(2026-05-03)*

858. O Hub é mais fresco que `gus-estado-atual.md` (snapshot das 03h).
   *(2026-05-03)*

859. Três demandas estão paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, `_frontmatter-referencia.md` (esse é template, não é demanda).
   *(2026-05-02)*

860. O projeto contém três demandas paradas em dialogos/inbox-claude-code: 2026-05-01-captura-multiporta-curador.md, 2026-05-01-drive-sync-oauth-fix.md e _frontmatter-referencia.md.
   *(2026-05-02)*

861. Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template.
   *(2026-05-02)*

862. O estado final dos PRs está no código e nos documentos gus-XX atualizados; PRs descrevem o caminho, não o presente.
   *(2026-05-03)*

863. Os logs do `_log/resumos-mem0/` confirmam que o curador não estava funcionando.
   *(2026-05-02)*

864. Gustavo é anestesiologista e não programa — toda implementação passa pelo Gus ou Tiogu.
   *(2026-05-03)*

865. O bot possui prompt caching que reduz o custo de input em janelas de 5 minutos.
   *(2026-05-02)*

866. A migração de 204 memórias de gus deve ser realizada para evitar poluição do Hub.
   *(2026-05-03)*

867. Sempre que possível, é melhor usar ferramentas MCP ao invés de arquivos .md.
   *(2026-05-02)*

868. Se os testes de validação passarem, avançar para o próximo passo que é recadastrar o Connector no claude.ai.
   *(2026-05-03)*

869. É necessário ler [gus-estado-atual.md](http://gus-estado-atual.md) para obter um snapshot do Hub.
   *(2026-05-03)*

870. O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).
   *(2026-05-02)*

871. A equipe registrou que o curador híbrido gera resumos brutos quando falha, o que pode poluir o Hub com dados não classificados.
   *(2026-05-03)*

872. Gustavo é anestesiologista e não programa; toda implementação passa pelo Gus ou Tiogu.
   *(2026-05-03)*

873. A auditoria diária é cega para o brain gus e não considera o area que o curador já preencheu.
   *(2026-05-03)*

874. Há 4 demandas pendentes sendo triadas no inbox-claude-code.
   *(2026-05-03)*

875. Demandas pendentes na porta inbox-claude-code incluem captura multiporta, curador bidirecional cron e drive-sync OAuth.
   *(2026-05-03)*

876. A captura de fragmentos acontece em três frentes: Telegram, Chat e Code.
   *(2026-05-03)*

877. A demanda 2026-05-01-captura-multiporta-curador.md precisa de um gatilho proativo no Chat.
   *(2026-05-02)*

878. Existem 6 demandas pendentes na porta inbox-claude-code, sendo 3 demandas reais.
   *(2026-05-03)*

879. A conta Anthropic está sem créditos.
   *(2026-05-03)*

880. O estado final dos PRs já está documentado no código e nos docs gus-XX atualizados.
   *(2026-05-03)*

881. O Hub é a fonte da verdade. Gustavo é anestesiologista, não programa — toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

882. As decisões abertas do projeto incluem a aprovação de itens 11.1-11.7.
   *(2026-05-02)*

883. O estado final dos PRs já está no código e nos documentos atualizados; novas abas não precisam ser criadas se o conteúdo for apenas histórico.
   *(2026-05-03)*

884. Aba nova deve sempre consultar o Hub, que é mais fresco que o snapshot das 03h.
   *(2026-05-03)*

885. A auditoria do Chat envolve todos os aspectos relacionados ao projeto Claude Chat.
   *(2026-05-03)*

886. Um dos workflows está apresentando falhas, especificamente a importação de demandas do Drive.
   *(2026-05-02)*

887. O bot Telegram TioGu usa um sistema multi-porta com Hub Qdrant como memória central.
   *(2026-05-02)*

888. A aba que contém o MCP gus-hub conectado permite ler o cache de identidade atual, últimas 3 decisões e 5 meta-reflexões, além de fragmentos recentes das últimas 24 horas.
   *(2026-05-02)*

889. O Hub Qdrant é a nova fonte da verdade, e a migração do sistema Mem0 está em andamento. O sistema utiliza em paralelo dois curadores (Haiku e GPT-4o-mini) com multiplicação por 4 nas chamadas LLM.
   *(2026-05-03)*

890. O agente pessoal do Gustavo Pratti de Barros é chamado Gus.
   *(2026-05-03)*

891. A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida pelo PR #67.
   *(2026-05-02)*

892. Há riscos de poluição cross-brain entre os brains 'gustavo' e 'gus' devido à duplicação de fragmentos sem deduplicação.
   *(2026-05-03)*

893. Os 4 arquivos essenciais para qualquer aba nova no projeto são: `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md` e `estado-atual.md`.
   *(2026-05-03)*

894. A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida pelo PR #67 (curador bidirecional), mas falta o gatilho proativo no Chat.
   *(2026-05-02)*

895. O Hub Qdrant coleta dual rola até 12/05.
   *(2026-05-02)*

896. O paciente_id canônico é gus.
   *(2026-05-02)*

897. Pergunta se deve processar as demandas ou se há algo específico em mente.
   *(2026-05-03)*

898. A auditoria atual do Hub não está considerando a coleta de dados do brain 'gus', causando uma falta de visibilidade sobre seu estado.
   *(2026-05-03)*

899. Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

900. Gustavo Pratti de Barros é um anestesiologista, não programa.
   *(2026-05-03)*

901. A auditória diária é cega para o brain `gus` e ignora o `area` já preenchido pelo curador.
   *(2026-05-03)*

902. As 4 fases do projeto dão 80% do contexto para qualquer nova aba.
   *(2026-05-03)*

903. As escolhas de codificação no curador incluem 4 chamadas LLM por input para lidar com cada interagir, aumentando os custos operacionais.
   *(2026-05-03)*

904. O script `export_mem0.py` é responsável por exportar dados do Mem0 SaaS.
   *(2026-05-03)*

905. O curador utilizado no Telegram apresentou erro 400 envolvendo KeyError, especificamente no formato do JSON em uso.
   *(2026-05-02)*

906. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e precisa de uma decisão sobre a tecnologia a ser utilizada.
   *(2026-05-02)*

907. A migração ADR-001 está em curso, visando aposentar o Mem0 SaaS fazendo do Hub Qdrant a fonte da verdade.
   *(2026-05-03)*

908. O plano para reclassificar e reintegrar 204 fragmentos do Mem0 é esperado na Fase 5.
   *(2026-05-03)*

909. A coleta dual de modelos no curador termina em 12/05/2026, quando Gustavo escolherá um modelo definitivo.
   *(2026-05-03)*

910. O Hub está coletando dados de fragmentos de múltiplas fontes, mas o custo de processamento está aumentando devido à quantidade de chamadas LLM feitas por entrada.
   *(2026-05-03)*

911. A coleção legada de memórias do Gus ainda existe, mas deve ser migrada para o Hub. Existia o risco de inconsistências entre as buscas feitas no Hub e na coleção legada.
   *(2026-05-03)*

912. O Gus é um sistema de agente pessoal multi-porta que possui um Hub central.
   *(2026-05-03)*

913. O arquivo de log gerado pelo retro-engine é inofensivo e documenta um comportamento esperado.
   *(2026-05-02)*

914. Os arquivos core obrigatórios para qualquer aba nova são: dialogos/_bootstrap/gus-bootstrap.md, dialogos/_bootstrap/gus-identity.md, dialogos/_bootstrap/gus-estado-atual.md e projetos/gus/_estado-atual.md.
   *(2026-05-03)*

915. O bot Telegram (TioGu) possui ~21 tools, multimídia, prompt caching e está em produção no Railway.
   *(2026-05-02)*

916. 204 fragmentos foram exportados do Mem0 SaaS para o diretório historico.
   *(2026-05-03)*

917. Atualmente o bot TioGu não possui testes automatizados, representando um risco significativo para a manutenção do sistema.
   *(2026-05-02)*

918. O projeto Gus tem um sistema multi-porta que integra o Telegram, Claude Code, Claude Chat e futuros modelos como Custom GPT e Alexa.
   *(2026-05-02)*

919. O NeuroGus está planejado com PWA e grafo 3D do Hub, com planejamento 100% pronto.
   *(2026-05-02)*

920. A demanda #3 refere-se a pendências Claude Chat que incluem: ativar MCP URL secret no Railway, recadastrar o Connector Claude.ai, localizar um mock HTML do NeuroGus, e decidir sobre a captura em tempo real do Chat.
   *(2026-05-02)*

921. A auditoria do Claude Chat revelou 12 fixes de 31 achados.
   *(2026-05-03)*

922. Em 02/05, o curador falhou em salvar fragmentos devido a problemas de formato que estavam presentes em 29/04.
   *(2026-05-03)*

923. Gustavo Pratti de Barros é anestesiologista e não programa.
   *(2026-05-03)*

924. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

925. A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida pelo PR #67.
   *(2026-05-02)*

926. O projeto Gus é um sistema de agente pessoal multi-porta com memória central no Hub Qdrant.
   *(2026-05-03)*

927. A auditoria do Chat envolve todos os aspectos relacionados ao projeto Claude Chat.
   *(2026-05-03)*

928. Gus é um sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa).
   *(2026-05-03)*

929. A seção 'Como você captura memória pro Hub' foi reescrita com 2 caminhos: Caminho 1 (MCP) e Caminho 2 (upload .md).
   *(2026-05-03)*

930. A coleta de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

931. O '_estado-atual.md' está desatualizado e não reflete muitas mudanças recentes.
   *(2026-05-02)*

932. Gustavo é anestesiologista e não programa. Toda implementação passa por um sistema de agente pessoal multi-porta que utiliza core obrigatório como arquivos de bootstrap para regras e identidade.
   *(2026-05-03)*

933. O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).
   *(2026-05-02)*

934. O projeto TioGu é um bot desenvolvido para o Telegram que utiliza um sistema multi-porta com arquitetura Hub Qdrant como memória central.
   *(2026-05-02)*

935. A conexão entre o curador e o módulo llm é muito direta e pode ser melhorada para aumentar a modularidade.
   *(2026-05-02)*

936. A proposta de mudança no `drop_pending_updates` do bot Telegram é mantê-lo como True, mas adicionar uma mensagem de aviso se houver mensagens pendentes durante o boot.
   *(2026-05-02)*

937. O curador usa dois modelos em paralelo: Haiku e GPT-4o-mini.
   *(2026-05-03)*

938. O branch atual é `claude/project-discussion-fkfA8` e contém um arquivo `_log/retro-engine` novo desta sessão.
   *(2026-05-02)*

939. Uma nova suite de testes para o projeto foi implementada, abrangendo uma cobertura ampla das funcionalidades principais.
   *(2026-05-02)*

940. A estrutura da receita para análise e informações do projeto é orientada pelo core obrigatório.
   *(2026-05-03)*

941. O status final dos PRs já está no código e nos docs gus-XX atualizados, portanto, não é necessário ler PRs antigos.
   *(2026-05-02)*

942. O contrato schema gus-18 está parcialmente implementado.
   *(2026-05-03)*

943. A coleta dual de modelos no curador deve ser finalizada até 12/05/2026.
   *(2026-05-03)*

944. A implementação do ciclo de atualização de `acessos` e `ultimo_acesso` em `lembrar()` é necessária para o correto funcionamento do sistema.
   *(2026-05-03)*

945. As demandas pendentes no inbox são: Ativar `MCP_URL_SECRET` no Railway, recadastrar Connector claude.ai e localizar mock HTML do NeuroGus.
   *(2026-05-03)*

946. A auditoria diária é cega para o brain 'gus' e classifica por keywords, ignorando a área já preenchida pelo curador.
   *(2026-05-03)*

947. O Hub Qdrant está na Fase 4 da migração Mem0 → Hub Qdrant.
   *(2026-05-02)*

948. Todo fragmento fica de estado "ativo" pra sempre.
   *(2026-05-03)*

949. O PR #72 introduziu melhorias de segurança no MCP server, garantindo que ele opere em modo fail-closed sem autenticação.
   *(2026-05-02)*

950. A auto-notificação do Telegram pode ser mantida para demandas na pasta TioGu.
   *(2026-05-03)*

951. 1. Gustavo trabalha com agendamento/gestão de pacientes para exames de RM (ressonância magnética).
2. Padrão de resposta esperado do Gus: formato com detecção de imagem, lista de pacientes já no sistema do dia, e solicitação de confirmação (sim/ok/manda ou não/cancela).
3. Gus deve manter esse padrão de resposta estruturado em futuras interações com Gustavo.
4. Roberta Xavier Lins foi adicionada ao arquivo do dia com exame de RM Coluna Dorsal + Lombar + Anestesia agendada para 15h-19h30, plano Intermédica.
   *(2026-04-28)*

952. O bot Telegram (TioGu) tem 21 tools, multimídia, prompt caching e está em produção no Railway.
   *(2026-05-02)*

953. O bot chama APIs externas sem cache, o que gera custo e pode exaurir recursos em meses de baixa cota.
   *(2026-05-02)*

954. O bot do Telegram, TioGu, possui 21 ferramentas distintas integradas.
   *(2026-05-02)*

955. A auditoria do Chat foi concluída e vários problemas foram identificados, incluindo questões de segurança, confiabilidade e arquitetura.
   *(2026-05-02)*

956. A nova estrutura `Gus-Sync/dialogos/inbox-gustavo/{chat,code,tiogu}/` no Drive permite a captura direta sem frontmatter.
   *(2026-05-03)*

957. O arquivo '_estado-atual.md' está desatualizado em relação ao projeto.
   *(2026-05-02)*

958. A decisão de migração ADR-001 ainda está em curso, visando aposentar o Mem0 SaaS.
   *(2026-05-03)*

959. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

960. Sobre a decisão de manter `drop_pending_updates=True`, uma abordagem recomendada é logar o count de pending e avisar o Gustavo no boot.
   *(2026-05-02)*

961. Hub é mais fresco que `gus-estado-atual.md` (que é snapshot das 03h).
   *(2026-05-03)*

962. Os arquivos com as demandas pendentes são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template `_frontmatter-referencia.md`.
   *(2026-05-02)*

963. Os arquivos obrigatórios para toda aba nova são: dialogos/_bootstrap/gus-bootstrap.md, dialogos/_bootstrap/gus-identity.md, dialogos/_bootstrap/gus-estado-atual.md e projetos/gus/_estado-atual.md.
   *(2026-05-02)*

964. As 18 entradas que entraram em modo `fallback-mem0` em 28/04 não estão na coleção `gus`.
   *(2026-05-03)*

965. Vou ler as 2 demandas pendentes + docs de próximos passos + PRs recentes em paralelo.
   *(2026-05-02)*

966. O arquivo untracked é só esse log honesto: "00:26:07 BRT — sessão encerrada".
   *(2026-05-02)*

967. Após criar um arquivo no Drive, o cron pegará e auto-injetará frontmatter em ≤15min.
   *(2026-05-03)*

968. Gustavo é anestesiologista e não programa, toda implementação passa pelo Gus/Tiogu.
   *(2026-05-03)*

969. A stack está em estado intermediário arriscado: a coleção legada 'gus' tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

970. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md` e `_frontmatter-referencia.md`.
   *(2026-05-02)*

971. A migração do sistema Mem0 para o Hub Qdrant deve ser realizada, e detalhes sobre a execução se encontram em documentos no GitHub.
   *(2026-05-03)*

972. O workflow de migração descobriu que a coleção 'gus' está vazia, apesar das menções a 204 fragmentos.
   *(2026-05-03)*

973. Sessão 3B da Fase 2 abordará a reescrita do arquivo `system_prompt.md` para melhorar o desempenho do bot.
   *(2026-05-02)*

974. As memórias em Qdrant e Mem0 SaaS devem ser geridas separadamente.
   *(2026-05-03)*

975. A opção de manter o `drop_pending_updates=True` evita uma avalanche de updates após o deploy, mas impede que mensagens enviadas durante o downtime sejam processadas.
   *(2026-05-02)*

976. A migração ADR-001 está em curso, que aposenta Mem0 SaaS.
   *(2026-05-03)*

977. Há 3 produções simultâneas de fragmentos com 4× multiplicação de chamadas LLM por unidade de input.
   *(2026-05-03)*

978. A convenção de nomenclatura de arquivos dos exames utiliza o formato <paciente_id>__<data_coleta>__<lab_curto>.json.
   *(2026-05-02)*

979. A captura proativa do Chat agora é instrução explícita no bootstrap.
   *(2026-05-03)*

980. Três demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md` e `_frontmatter-referencia.md` (esse é template, não é demanda).
   *(2026-05-02)*

981. Hub Qdrant é a fonte da verdade após migração.
   *(2026-05-03)*

982. Os 4 documentos essenciais para contexto em qualquer aba nova são: dialogos/_bootstrap/gus-bootstrap.md, dialogos/_bootstrap/gus-identity.md, dialogos/_bootstrap/gus-estado-atual.md e projetos/gus/_estado-atual.md.
   *(2026-05-02)*

983. Três opções de solução para o Drive sync: resetar OAuth, criar Service Account, ou aposentar Drive sync.
   *(2026-05-03)*

984. O Hub Qdrant é a nova fonte da verdade do sistema de agente pessoal multi-porta.
   *(2026-05-03)*

985. A captura de sessões do Stop hook foi verificada como funcional após os merges dos PRs.
   *(2026-05-02)*

986. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md` e `_frontmatter-referencia.md` (template, não é demanda).
   *(2026-05-02)*

987. As decisões sobre o Drive sync e o acesso ao Hub são essenciais para o funcionamento operacional do Chat.
   *(2026-05-03)*

988. O bot Telegram está em produção na Railway com 21 tools.
   *(2026-05-02)*

989. As demandas pendentes em `dialogos/inbox-claude-code/` incluem '2026-05-01-captura-multiporta-curador.md' e '2026-05-01-drive-sync-oauth-fix.md'.
   *(2026-05-02)*

990. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e a hipótese é que o refresh token OAuth expirou.
   *(2026-05-02)*

991. O planejamento do NeuroGus está 100% pronto e faltam ~145 linhas para implementar.
   *(2026-05-02)*

992. O projeto envolve um bot chamado TioGu, que utiliza uma arquitectura de multi-porta com Hub Qdrant como memória central. O sistema é montado para integrar diferentes APIs e faz uso de ferramentas como Claude AI e Telegram.
   *(2026-05-02)*

993. O `_estado-atual.md` de 27/04 está desatualizado, havendo muitas mudanças depois.
   *(2026-05-02)*

994. O arquivo de log gerado pelo retro-engine contém a informação de que não foi possível coletar fragmentos devido à ausência da chave ANTHROPIC_API_KEY.
   *(2026-05-02)*

995. O core obrigatório para qualquer aba nova inclui: dialogos/_bootstrap/gus-bootstrap.md, dialogos/_bootstrap/gus-identity.md, dialogos/_bootstrap/gus-estado-atual.md, projetos/gus/_estado-atual.md.
   *(2026-05-03)*

996. A auditoria diária é cega para o brain gus e classifica por keywords ignorando o area que o curador já preencheu.
   *(2026-05-03)*

997. O estado final dos PRs está no código e nos documentos atualizados. PRs descrevem o caminho, não o estado atual, e uma nova aba deve referir-se ao estado atual do projeto.
   *(2026-05-03)*

998. Os fragmentos no Hub são classificados, mas o sistema ainda apresenta vulnerabilidades que podem levar à poluição de dados.
   *(2026-05-03)*

999. 1. Gustavo dispara regularmente workflow `import-from-drive.yml` para sincronizar arquivos do Drive com GitHub — tempo de execução esperado é até 15 minutos
2. Gustavo prefere confirmação clara quando workflows são disparados
3. Gus é a identidade unificada do agente pessoal; Tiogu é apenas o bot no Telegram — mesma entidade, memória e princípios em múltiplas plataformas (Claude Chat, Claude Code, futuro Alexa e Custom GPT)
4. Gustavo tem 4 demandas abertas do dia 26/04 que continuam sem novidade
   *(2026-04-28)*

1000. Gus está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

1001. Há um tratamento de risco clínico real no fluxo de Dimagem, onde um nome trocado em prontuário é tratado com bloqueio e reenvio em vez de alerta.
   *(2026-05-02)*

1002. A solução para o problema de sincronização com o Google Drive envolve três opções: 1 - reset de OAuth, 2 - uso de uma Service Account ou 3 - aposentadoria da sincronização.
   *(2026-05-02)*

1003. O sistema Gus é um agente pessoal multi-porta conectado a várias interfaces, incluindo Telegram, Claude Code, Claude Chat e futuras interfaces.
   *(2026-05-03)*

1004. Há 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1005. A causa do erro 400 é a interpretação incorreta de placeholders no template JSON.
   *(2026-05-02)*

1006. A stack atual está em estado intermediário arriscado devido à coexistência da coleção legada e da nova.
   *(2026-05-03)*

1007. _frontmatter-referencia.md é um template, não é uma demanda.
   *(2026-05-02)*

1008. O `_estado-atual.md` (27/04) está desatualizado.
   *(2026-05-02)*

1009. O estado da stack de memória é de estado intermediário arriscado: Hub Qdrant é a fonte nova, mas a coleção legada gus (Mem0 self-hosted) tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

1010. A fase 1 do TioGu foi concluída, com 163 testes verdes.
   *(2026-05-03)*

1011. A documentação está sendo mantida em dia, essencial para referência futura e validação de decisões.
   *(2026-05-02)*

1012. Atualmente, o TioGu utiliza LLMs da Anthropic e OpenAI, com fallback integrado para cada um.
   *(2026-05-02)*

1013. O sistema inclui um mecanismo de caching de promts, permitindo maior eficiência nas chamadas aos LLMs.
   *(2026-05-02)*

1014. Os testes de unidade cobririam o caminho crítico do bot, incluindo LLM dispatch e memória.
   *(2026-05-02)*

1015. 1. Hub Qdrant agora funciona corretamente — 2+ fragmentos salvos, merge resolveu o problema crítico; Gustavo pode enviar PDFs quando quiser.

2. Sistema de curador híbrido (Haiku + Sonnet em paralelo) está operacional com schema gus-18 completo, embeddings locais via sentence-transformers, e controle de ciclo de vida (ativo/histórico/esquecido).

3. Experimento de 14 dias coletando pares Haiku × Sonnet encerra ~12/05/2026; após isso, Gustavo analisará logs em `_log/resumos-mem0/` no Obsidian para decidir qual modelo(s) manter.

4. Canal `dialogos/` operacional em ambas direções: workflow `notificar-inbox-tiogu.yml` notifica bot quando arquivo entra em inbox; tool `rotear_arquivo` permite mover arquivos após confirmação.

5. 16 workflows ativos (dobrou desde última análise): notificação inbox, archive automático, migração Qdrant, migração Mem0→Qdrant, importação Drive, etc.

6. Pendências técnicas: PR #10 ainda aberta (cosmético), workflow "Ingest Mem0 from Claude Chat" falhando (provável endpoint antigo), `memory.py` importa mem0ai à toa (limpeza Fase 5), suporte a vídeo ainda falta.

7. Estrutura repo expandida: novas pastas `api/`, `scripts/`, `_log/`, `agenda/`, `docs/`.
   *(2026-04-27)*

1016. O Hub Qdrant é a fonte da verdade para o sistema de agentes pessoais multi-porta.
   *(2026-05-03)*

1017. A atualização do '_estado-atual.md' foi marcada como pendente.
   *(2026-05-02)*

1018. O Hub Qdrant está ocioso há 6h+ na janela 'fragmentos últimas 6h'.
   *(2026-05-02)*

1019. A divergência entre os outputs do Haiku e do GPT é dramática, com o Haiku rejeitando fragmentos.
   *(2026-05-03)*

1020. A validação do estado atual do projeto é feita por auditorias diárias.
   *(2026-05-03)*

1021. As atualizações mais recentes incluem a correção do bug do formato no curador e a estruturação do Hub.
   *(2026-05-03)*

1022. Existem 3 demandas paradas em 'dialogos/inbox-claude-code/'.
   *(2026-05-02)*

1023. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1024. O estado final dos PRs já tá no código + nos docs gus-XX atualizados. PRs descrevem o caminho, não onde a gente tá.
   *(2026-05-03)*

1025. A coleta dual de modelos no curador termina em 12/05/2026 — depois Gustavo escolhe modelo definitivo.
   *(2026-05-03)*

1026. A demanda #3 é uma guarda-chuva que referencia as demandas #1 e #2 dentro dela.
   *(2026-05-02)*

1027. Os fragmentos do brain 'gus' estão apresentando risco de poluição cruzada com fragmentos do brain 'gustavo'.
   *(2026-05-03)*

1028. A coleta dual de modelos no curador parte do Haiku e vai até GPT-4o-mini.
   *(2026-05-03)*

1029. A demanda da semana está documentada no arquivo `semana-2026-04-21.md`.
   *(2026-05-03)*

1030. Os testes automatizados cobrem caminhos críticos do sistema, incluindo dispatch de LLM, retries, memória, state, regex, validações, e scanner de PII.
   *(2026-05-02)*

1031. O estado final dos PRs já está no código e nos docs gus-XX atualizados.
   *(2026-05-03)*

1032. A migração Mem0 para Hub Qdrant está na fase 4, e a coleta dual de Haiku e Sonnet deve terminar em 12/05, quando a decisão sobre o modelo do curador final será tomada.
   *(2026-05-02)*

1033. O `_estado-atual.md` (27/04) está bem desatualizado — o git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67).
   *(2026-05-02)*

1034. A coleta dual Haiku × Sonnet roda até 12/05, e depois decidirão o modelo final do curador.
   *(2026-05-03)*

1035. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

1036. A captura diária das memórias e o sistema de auditoria do hub não estão sincronizados, resultando em incoerências de logs e na estrutura das memórias.
   *(2026-05-03)*

1037. A URL do Connector no claude.ai precisa ser atualizada após a configuração do segredo.
   *(2026-05-03)*

1038. A terceira demanda é intitulada `_frontmatter-referencia.md` e é um template, não é uma demanda.
   *(2026-05-02)*

1039. Um panorama geral do projeto foi solicitado e será analisado junto com as últimas atualizações que não estão nos documentos citados.
   *(2026-05-02)*

1040. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026. Após isso, Gustavo escolhe o modelo definitivo.
   *(2026-05-03)*

1041. A stack está em estado intermediário arriscado.
   *(2026-05-03)*

1042. Gus coletou demandas pendentes do inbox e último stream da semana.
   *(2026-05-02)*

1043. Gus é um sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa).
   *(2026-05-03)*

1044. A coleção legada `gus` na Qdrant está vazia e não contém fragmentos.
   *(2026-05-03)*

1045. O código do bot TioGu possui aproximadamente 5.800 linhas de código organizado em diretórios como gus e hub.
   *(2026-05-02)*

1046. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1047. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, `_frontmatter-referencia.md`.
   *(2026-05-02)*

1048. O script de limpeza do Hub, utilizando um dry run para identificar candidatos à exclusão, será criado após a aprovação da lista de candidatos marcada por Gustavo.
   *(2026-05-03)*

1049. A coleta dos 204 fragmentos não migrados da coleção legada `gus` é uma pendência a ser resolvida.
   *(2026-05-03)*

1050. O `MEM0_API_KEY` deve ser removido para evitar qualquer risco de acesso ao conteúdo antigo no Mem0 SaaS.
   *(2026-05-03)*

1051. Os fronts ativos incluem o saneamento do TioGu e a auditoria do Claude Chat.
   *(2026-05-03)*

1052. Gustavo está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-02)*

1053. As demandas pendentes são captura multiporta, curador bidirecional cron e drive-sync OAuth.
   *(2026-05-03)*

1054. Os 204 fragmentos exportados do Mem0 SaaS foram considerados de qualidade superior ao Hub atual.
   *(2026-05-03)*

1055. O curador híbrido (Haiku × Sonnet/GPT) coleta dual até 12/05 para avaliação de desempenho.
   *(2026-05-02)*

1056. O bot Telegram, TioGu, possui cerca de 21 ferramentas.
   *(2026-05-02)*

1057. O bot Telegram (TioGu) possui ~21 tools, multimídia, prompt caching, e está em produção no Railway.
   *(2026-05-02)*

1058. O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois.
   *(2026-05-02)*

1059. O arquivo 'dialogos/_bootstrap/gus-identity.md' define quem é o Gustavo e quem é o Gus enquanto entidade.
   *(2026-05-02)*

1060. Os logs do Railway estão expondo o `MCP_URL_SECRET` em texto claro.
   *(2026-05-03)*

1061. O Hub Qdrant é a nova fonte da verdade e a coleta dual de modelos termina em 12/05/2026.
   *(2026-05-03)*

1062. O estado de migração ADR-001 está em curso para aposentar Mem0 SaaS.
   *(2026-05-03)*

1063. O log do retro-engine está em `claude/greeting-checkin-94weM`.
   *(2026-05-03)*

1064. O sistema usa um Bot Telegram chamado TioGu, que possui cerca de 21 ferramentas.
   *(2026-05-02)*

1065. Vi que tem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, `_frontmatter-referencia.md` (esse é template, não é demanda).
   *(2026-05-02)*

1066. O commit referente à Sessão 1 da Fase 1 foi feito com o ID 55c1de8, incluindo o workflow de CI para rodar testes em PR e push na branch principal.
   *(2026-05-02)*

1067. O botão 'Merge pull request' foi presenciado durante o processo de merge.
   *(2026-05-02)*

1068. O arquivo `dialogos/_bootstrap/gus-estado-atual.md` é um snapshot do Hub gerado automaticamente pelo cron a cada 03h.
   *(2026-05-02)*

1069. As demandas paradas são: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, e `_frontmatter-referencia.md`.
   *(2026-05-02)*

1070. Os documentos essenciais para qualquer aba nova são: `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md` e `estado-atual.md`. Eles fornecem 80% do contexto necessário.
   *(2026-05-03)*

1071. A prioridade default para novas demandas pode ser definida como 'media'.
   *(2026-05-03)*

1072. O bot possui um sistema de gate de confiança para proteger dados sensíveis, especialmente na visualização de arquivos PDF.
   *(2026-05-02)*

1073. O sistema de captura de PII no TioGu é limitado, pois a verificação de dados sensíveis ocorre apenas antes de salvar no GitHub, não na saída do bot.
   *(2026-05-02)*

1074. A composição de fragmentos criados é gerada a partir de 3 produções simultâneas (Telegram, Chat, Code), resultando em múltiplas chamadas LLM.
   *(2026-05-03)*

1075. O sistema multi-porta usa o Hub Qdrant como memória central.
   *(2026-05-02)*

1076. Atividades pendentes do Gustavo incluem setar `MCP_URL_SECRET` no Railway e recadastrar Connector claude.ai.
   *(2026-05-03)*

1077. Os arquivos com as demandas pendentes incluem: captura-multiporta-curador, drive-sync-oauth-fix e pendencias-claude-chat-consolidacao.
   *(2026-05-03)*

1078. Gustavo Pratti de Barros é a identidade principal do Gus.
   *(2026-05-02)*

1079. A seção 'Disciplina anti-esquecimento' do Gus encontra-se atualizada para incluir dois caminhos de captura.
   *(2026-05-03)*

1080. A coleção legada 'gus' está vazia, e não há fragmentos a serem migrados.
   *(2026-05-03)*

1081. O sistema de agente pessoal do Gus utiliza memória central no Hub Qdrant e arquivos .md no GitHub.
   *(2026-05-03)*

1082. Fragmentos são salvos no Hub com tags que especificam o tipo de conteúdo e o agente responsável pela captura.
   *(2026-05-03)*

1083. O `_estado-atual.md` (27/04) está desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).
   *(2026-05-02)*

1084. O commit `cc6306d` inclui melhorias na auditoria e acompanhamento das interações do chat.
   *(2026-05-02)*

1085. O curador do Gus espera implementar funcionalidades de atualização de memória, como 'peso', 'acessos', e 'tipo_esquecimento'.
   *(2026-05-03)*

1086. O primeiro passo a ser seguido é gerar um novo segredo (`MCP_URL_SECRET`).
   *(2026-05-03)*

1087. Hub Qdrant é a nova fonte da verdade.
   *(2026-05-03)*

1088. A migração ADR-001 está em curso, com o Hub Qdrant como fonte da verdade.
   *(2026-05-03)*

1089. O projeto Gus é um sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) com Hub Qdrant como memória central.
   *(2026-05-02)*

1090. A arquitetura do TioGu é baseada em um sistema de memória centralizado via Hub Qdrant, com fallback para Mem0 em caso de perda de conexão.
   *(2026-05-02)*

1091. A coleta de fragmentos históricos não retornou nenhuma entrada na migração para o Hub.
   *(2026-05-03)*

1092. O conteúdo armazenado nos arquivos exportados é considerado de qualidade superior ao que está atualmente no Hub.
   *(2026-05-03)*

1093. O Hub Qdrant é o único conteúdo atual, e os fragmentos legados não são relevantes.
   *(2026-05-03)*

1094. O sistema Hub está ocioso nas últimas 6 horas.
   *(2026-05-03)*

1095. O MCP está público, permitindo acesso total ao Hub sem proteção.
   *(2026-05-03)*

1096. Após setar a variável, aguardar o redeploy no Railway que leva cerca de 2 a 3 minutos.
   *(2026-05-03)*

1097. O estado final dos PRs já está no código e nos documentos gus-XX atualizados.
   *(2026-05-02)*

1098. O retro-engine é um hook que roda quando uma sessão Claude Code termina e deveria capturar a sessão, mas falta a variável ANTHROPIC_API_KEY.
   *(2026-05-02)*

1099. O sistema atualmente utiliza 4 chamadas de LLM por unidade de input, o que gera um custo elevado.
   *(2026-05-03)*

1100. Os quatro arquivos `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md` e `_estado-atual.md` dão 80% do contexto pra qualquer aba nova.
   *(2026-05-03)*

1101. Há 3 demandas paradas em dialogos/inbox-claude-code/
   *(2026-05-02)*

1102. O bot Telegram possui ~21 tools, multimídia, prompt caching em produção.
   *(2026-05-02)*

1103. A arquitetura do TioGu é multi-provider com fallback cross-vendor, permitindo resiliência.
   *(2026-05-02)*

1104. Os quatro arquivos obrigatórios fornecem 80% do contexto para qualquer nova aba.
   *(2026-05-03)*

1105. A stack está em estado intermediário arriscado.
   *(2026-05-03)*

1106. O projeto implica na necessidade de uma auditoria frequente e na atualização dos sistemas de memória para garantir a qualidade dos dados.
   *(2026-05-03)*

1107. A captura de transcripts no Claude Code está sendo resolvida pelo PR #64.
   *(2026-05-03)*

1108. A auditoria diária (`auditoria_hub.py`) é cega ao brain `gus` e ignora sua relevância e informações.
   *(2026-05-03)*

1109. Gustavo é anestesiologista, não programa.
   *(2026-05-03)*

1110. Recomenda-se mover o arquivo `dimagem.py` para o diretório `integrations/`, uma vez que ele representa uma integração específica e não é parte do núcleo do projeto.
   *(2026-05-02)*

1111. Os logs do retro-engine indicam 'no-op: anthropic_missing' devido à falta da variável ANTHROPIC_API_KEY na porta Code.
   *(2026-05-02)*

1112. O Hub Qdrant é usado como memória central do sistema.
   *(2026-05-02)*

1113. O sistema vai sincronizar arquivos de texto puro, .md, .html, .csv e Google Docs nativos.
   *(2026-05-03)*

1114. O workflow de sincronização entre o Google Drive e o GitHub foi disparado com sucesso.
   *(2026-05-02)*

1115. O estado do conexão do MCP é acessível por qualquer pessoa que conhecer a URL.
   *(2026-05-03)*

1116. A demanda 2026-05-01-drive-sync-oauth-fix.md está ativa.
   *(2026-05-02)*

1117. A captura em tempo real do Chat é uma decisão a ser tomada, podendo aumentar a interação de decisões relevantes durante a conversa.
   *(2026-05-02)*

1118. A memória central do Gus está no Hub Qdrant, com arquivos .md no GitHub e espelhados no Drive.
   *(2026-05-03)*

1119. O `_estado-atual.md` (27/04) está desatualizado em relação ao git log.
   *(2026-05-02)*

1120. Existem 4 caminhos de escrita que coexistem dentro do sistema, mas nem todos possuem regras totalmente compatíveis.
   *(2026-05-03)*

1121. O plenário de testes do Curador foi modificado após a correção do bug.
   *(2026-05-02)*

1122. A auditoria do Chat indicou que o curador Telegram enfrenta um erro 400 recorrente, prejudicando a captura de dados.
   *(2026-05-03)*

1123. O arquivo 'projetos/gus/_estado-atual.md' mostra onde paramos na sessão anterior e é mais 'operacional' que o bootstrap.
   *(2026-05-02)*

1124. A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida pelo PR #67 (curador bidirecional), mas falta o gatilho proativo no Chat.
   *(2026-05-02)*

1125. O core obrigatório em toda aba nova inclui 4 arquivos: `dialogos/_bootstrap/gus-bootstrap.md`, `dialogos/_bootstrap/gus-identity.md`, `dialogos/_bootstrap/gus-estado-atual.md`, e `projetos/gus/_estado-atual.md`.
   *(2026-05-02)*

1126. O novo canal Gus-Sync/dialogos/inbox-gustavo/{chat,code,tiogu}/ auto-injeta frontmatter, facilitando a captura via Drive.
   *(2026-05-03)*

1127. Os itens 1.6 e 1.7 da Fase 1 envolvem decisões que devem ser tomadas durante a execução e são consideradas mais críticas.
   *(2026-05-03)*

1128. D3 envolve gerenciar pendências de mensagens durante redeploys, decidindo entre descartar mensagens ou avisar o usuário.
   *(2026-05-02)*

1129. Estou aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1130. Aba nova só precisa olhar PRs se for reportado bug específico no código.
   *(2026-05-03)*

1131. Faltam o status consolidado, próximos passos, NeuroGus, e os PRs recentes pra fechar o panorama.
   *(2026-05-02)*

1132. O acesso ao Hub Qdrant é feito através de um MCP server público no Railway.
   *(2026-05-02)*

1133. O Anthropic está sem créditos, o que significa que não é possível realizar busca ou interações com esse serviço até que sejam adicionados créditos.
   *(2026-05-03)*

1134. PR #67 introduziu o curador chat bidirecional (Sonnet 4.6 + GPT-4o) que salva em `gustavo` + `gus`.
   *(2026-05-03)*

1135. A aba nova só precisa olhar PRs se houver um bug específico no código que foi mexido recentemente.
   *(2026-05-03)*

1136. O Gus é um sistema de agente pessoal multi-porta, com memória central no Hub Qdrant e arquivos em .md no GitHub.
   *(2026-05-03)*

1137. É recomendado usar 'ego_cache_atual()' para obter identidade, últimas decisões e meta-reflexões sempre que a aba tem o MCP gus-hub conectado.
   *(2026-05-02)*

1138. O curador híbrido cross-vendor já cobre '1 vendor caiu'.
   *(2026-05-03)*

1139. O bot é baseado em python-telegram-bot e possui backend integrado com FastAPI.
   *(2026-05-02)*

1140. 1. Schema atual do Mem0 é `gus-18` com campos: `tipo`, `area`, `campa_temporal`, `confiança` — não possui campo `origem` (source de telegram/chat/code).
2. Gustavo quer melhorias no schema documentadas como sugestões, não ordens — com instrução explícita pra verificar se já não foi planejado/implementado em outra branch antes de agir.
3. Demandas de código são salvas em `dialogos/inbox-claude-code/` com prioridade e status claro.
4. `save_to_github` salva sempre na branch main por padrão — comportamento correto para que workflows de importação (`import-from-drive`, etc.) consigam ler as demandas.
   *(2026-04-28)*

1141. Os últimos PRs que modificaram o código do projeto foram: PR #67 (curador-chat bidirecional + GPT-4o), PR #64 (captura transcripts Code via cron), PR #60 (MCP URL secret) e PR #70 (demanda consolidada).
   *(2026-05-02)*

1142. O Hub é a memória central do agente pessoal e é chamado de 'gus_hub'.
   *(2026-05-03)*

1143. A stack de memória está em um estado intermediário arriscado.
   *(2026-05-03)*

1144. O arquivo _estado-atual.md está desatualizado com relação aos últimos PRs.
   *(2026-05-02)*

1145. A demanda para Drive sync está ativa, com a hipótese de que o refresh token OAuth expirou.
   *(2026-05-02)*

1146. A arquitetura do Hub Qdrant é documentada em `gus-18-schema-indexacao.md` e outros arquivos relacionados.
   *(2026-05-03)*

1147. Para disparar todos os workflows, normalmente seria necessário executar cada um individualmente, pois não suporta disparo em lote.
   *(2026-05-03)*

1148. O nome da pasta no Drive pode ser definido como 'Gustavo/' ou 'pelo-gustavo/'.
   *(2026-05-03)*

1149. O `_estado-atual.md` está desatualizado, com data de 27/04.
   *(2026-05-03)*

1150. O MCP está público — qualquer scanner que descobrir a URL Railway lê todo o Hub. URL secret protege.
   *(2026-05-03)*

1151. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1152. As últimas atualizações do projeto não estão necessariamente nos documentos citados.
   *(2026-05-02)*

1153. A demanda 1 da consolidação trata da proteção do MCP público.
   *(2026-05-02)*

1154. O sistema Gus é um agente pessoal multi-porta com memória central no Hub Qdrant.
   *(2026-05-03)*

1155. O desenvolvedor planeja manter a compatibilidade entre LLMs, permitindo fallback entre Anthropic e OpenAI.
   *(2026-05-02)*

1156. O sistema multi-porta inclui Telegram, Claude Code, e Claude Chat, com Hub Qdrant como memória central.
   *(2026-05-02)*

1157. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa. Hipótese: refresh token OAuth expirou.
   *(2026-05-02)*

1158. O último _estado-atual.md está desatualizado desde 27/04.
   *(2026-05-02)*

1159. Na auditoria do Chat, foram encontrados problemas de segurança, confiabilidade e arquitetura que precisam ser resolvidos.
   *(2026-05-02)*

1160. O Hub Qdrant coletor dual rola até 12/05.
   *(2026-05-02)*

1161. A migração do Mem0 SaaS para o Hub Qdrant está em curso, com previsão para ser finalizada em 12/05/2026.
   *(2026-05-03)*

1162. Se um PR precisa ser lido para entender o presente, é sinal de documentação desatualizada.
   *(2026-05-03)*

1163. Ao setar `MCP_URL_SECRET`, fica disponível escrita real-time do Chat (função `ingestar_fragmento`).
   *(2026-05-03)*

1164. Os riscos operacionais do bot incluem a possibilidade de dados sensíveis vazarem devido à ausência de um PII scan efetivo na resposta do bot.
   *(2026-05-02)*

1165. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1166. A convenção de nomenclatura dos arquivos JSON deve ser registrada.
   *(2026-05-02)*

1167. O estado final dos PRs já está no código e nos documentos gus-XX atualizados.
   *(2026-05-02)*

1168. O estado final dos PRs já está no código + nos docs gus-XX atualizados.
   *(2026-05-03)*

1169. O núcleo obrigatório para qualquer novo projeto deve incluir: manual operacional, identidade do Gus, estado atual, e o estado atual dos projetos.
   *(2026-05-02)*

1170. O script para verificar as memórias no Mem0 está disponível no caminho `.github/scripts/export_mem0.py`.
   *(2026-05-03)*

1171. A persistência do estado é feita com gravação atômica, evitando perda de dados durante redeploys.
   *(2026-05-02)*

1172. Foi identificado que o '_estado-atual.md' e o 'gus-26-status-consolidado.md' estão desatualizados em relação a PRs recentes.
   *(2026-05-02)*

1173. Agora é possível enviar demandas pelo celular para o Drive sem precisar digitar YAML.
   *(2026-05-03)*

1174. A stack de memória está em estado intermediário arriscado: o Hub Qdrant é a fonte nova, mas a coleção legada tem fragmentos não migrados.
   *(2026-05-03)*

1175. Há uma programação de sessões para o projeto, com um total de 30 horas em 8-9 sessões ao longo de duas semanas.
   *(2026-05-02)*

1176. A arquitetura do bot é projetada para um único usuário, sem suporte a multi-tenancy.
   *(2026-05-02)*

1177. Gus é um sistema de agente pessoal multi-porta que integra várias plataformas como Telegram, Claude Code e Claude Chat, com memória central no Hub Qdrant.
   *(2026-05-03)*

1178. Os JSONs estruturados na pasta designada devem ser registrados.
   *(2026-05-02)*

1179. As 18 entradas 'fallback-mem0' de 28/04 foram pro Mem0 SaaS porque a migração ainda não estava 100% deploy-ada naquele dia.
   *(2026-05-03)*

1180. Última vez que houve commit foi dia 01/05 às 14:38Z, sync GitHub→Drive.
   *(2026-05-03)*

1181. A coleta dual de modelos no curador irá terminar em 12/05/2026.
   *(2026-05-03)*

1182. O Gustavo é anestesiologista e não programa, delegando toda implementação para o Gus e o Tiogu.
   *(2026-05-03)*

1183. O passo 4, relacionado ao Drive sync, foi resolvido pela implementação do WIF no PR #76.
   *(2026-05-03)*

1184. O workflow `migrar_gus_para_hub.py` foi executado em dry-run e não encontrou fragmentos na coleção 'gus'.
   *(2026-05-03)*

1185. O último update do projeto Gus foi realizado em 02/05/2026, montando um panorama geral da situação atual.
   *(2026-05-02)*

1186. A stack de memória está em estado intermediário arriscado com 4 caminhos de escrita coexistindo.
   *(2026-05-03)*

1187. Atualmente, o bot não possui um alerta que avisaria quando o limite de cota no uso de serviços é atingido, o que pode levar à perda de funcionalidade.
   *(2026-05-02)*

1188. A migração da Mem0 SaaS para o Hub Qdrant está em curso.
   *(2026-05-03)*

1189. Quatro demandas pendentes foram identificadas no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao.
   *(2026-05-02)*

1190. O sistema Gus é um agente pessoal multi-porta que opera em diferentes plataformas como Telegram e Claude Chat, com a memória central armazenada no Hub Qdrant.
   *(2026-05-03)*

1191. O projeto conta com um sistema multi-porta conectado ao Hub Qdrant.
   *(2026-05-02)*

1192. As opções para o que fazer com os 204 fragmentos incluem mantê-los em `historico/` ou importá-los para o Hub.
   *(2026-05-03)*

1193. A captura de memória ocorre em três canais: Telegram, Claude Chat, e Claude Code.
   *(2026-05-03)*

1194. Sessão 3A da Fase 2 inclui a atualização da documentação `_estado-atual.md` e `gus-26-status-consolidado.md`.
   *(2026-05-02)*

1195. A auditoria do Hub deve incluir o uso do campo `area` do payload para uma análise mais precisa.
   *(2026-05-03)*

1196. O Gus é um sistema de agente pessoal multi-porta com memória central no Hub Qdrant, arquivos .md no GitHub, espelhados no Drive.
   *(2026-05-03)*

1197. Realizar a rotaçã do segredo do MCP é essencial após as implementações de segurança.
   *(2026-05-03)*

1198. Os resultados do último projeto indicam que o estado atual do hub está fresco, com um snapshot gerado às 03h.
   *(2026-05-03)*

1199. Existem 6 demandas listadas no inbox-claude-code, mas apenas 3 são reais.
   *(2026-05-03)*

1200. As ferramentas do sistema devem ser documentadas em um arquivo auto-gerado chamado _tools-inventario.md.
   *(2026-05-02)*

1201. A documentação do projeto inclui um arquivo chamado _estado-atual.md, que é atualizado periodicamente para refletir o estado atual das implementações e decisões tomadas.
   *(2026-05-02)*

1202. A captura multiporta no Claude Chat precisa de um gatilho proativo que não está implementado.
   *(2026-05-02)*

1203. O retro-engine registra as sessões encerradas, mas a função acaba falhando quando a chave ANTHROPIC_API_KEY não está disponível no ambiente.
   *(2026-05-02)*

1204. O bot possui 21 ferramentas implementadas, distribuídas entre suas funcionalidades.
   *(2026-05-02)*

1205. Os 4 documentos obrigatórios que dão 80% do contexto para qualquer aba nova são: `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md` e `estado-atual.md`.
   *(2026-05-03)*

1206. A arquitetura do bot Telegram é baseada em um sistema multi-porta com Hub Qdrant como memória central.
   *(2026-05-02)*

1207. Foram propostos pontos para a fase 1 da revisão do bot.
   *(2026-05-02)*

1208. O estado final dos pull requests já está no código + nos documentos gus-XX atualizados.
   *(2026-05-03)*

1209. O bot Telegram descarta silenciosamente mensagens enviadas durante o downtime após cada redeploy Railway, sem aviso para o Gustavo.
   *(2026-05-02)*

1210. O sistema de agente pessoal multi-porta integra Telegram, TioGu, Claude Code e Claude Chat.
   *(2026-05-03)*

1211. Uma auditoria revelou que o Hub está retornando resultados inconsistentes devido a fallbacks para a coleção legada, introduzindo poluição no sistema.
   *(2026-05-03)*

1212. O curador foge do esquema `gus-18` por falta de implementação para o ciclo de vida dos fragmentos, resultando em fragmentos como 'ativo' para sempre.
   *(2026-05-03)*

1213. A captura Claude Code via cron (PR #64) permite que um hook Stop salve a transcript redatada, com cron a cada 30 minutos para processamento.
   *(2026-05-02)*

1214. Em volume crescente, brain `gus` vira cópia ruidosa do brain `gustavo`.
   *(2026-05-03)*

1215. O `_estado-atual.md` (27/04) está bem desatualizado em relação ao git log que mostra muita coisa depois.
   *(2026-05-02)*

1216. O documento `gus-estado-atual.md` está desatualizado, datado de 27/04.
   *(2026-05-02)*

1217. Os 204 fragmentos do Mem0 SaaS devem ser reclassificados e possivelmente traduzidos na fase 5.
   *(2026-05-03)*

1218. Todos os fragmentos criados antes da migração e depois da Fase 3 vão existir só na coleção antiga.
   *(2026-05-03)*

1219. A implementação do lifecycle para o schema gus-18 está declarada, mas não implementada.
   *(2026-05-03)*

1220. O Hub é mais fresco que gus-estado-atual.md (snapshot das 03h). Sempre que possível, prefira tools MCP a arquivo .md.
   *(2026-05-03)*

1221. A stack de memória está em estado intermediário arriscado, com o Hub Qdrant como nova fonte e a coleção legada `gus` ainda ativa.
   *(2026-05-03)*

1222. O PR #76 migrou pra WIF e você já configurou os secrets.
   *(2026-05-03)*

1223. A auditoria diária (`auditoria_hub.py`) é cega para o brain `gus` e classifica por keywords ignorando o `area` que o curador já preencheu.
   *(2026-05-03)*

1224. A migração de 204 fragmentos da coleção Mem0 SaaS para o Hub Qdrant é uma prioridade.
   *(2026-05-03)*

1225. O log do retro-engine desta sessão não conseguiu extrair fragmentos devido à falta de `ANTHROPIC_API_KEY`.
   *(2026-05-02)*

1226. O segredo vazou em vários logs e transcripts, resultando na necessidade de rotação.
   *(2026-05-03)*

1227. O TioGu possui uma implementação de fallback cross-vendor para os LLMs, aumentando a resiliência do sistema.
   *(2026-05-02)*

1228. O estado final dos PRs já está no código e nos documentos gus-XX atualizados.
   *(2026-05-03)*

1229. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1230. O hub Qdrant é a fonte de verdade do sistema Gus.
   *(2026-05-03)*

1231. 1. Gustavo trabalha com gestão de pacientes organizados por planos de saúde (Assim Taquara vs. outros planos: Intermédica + Leve Saúde)
2. Preferência por separar dados de pacientes em arquivos markdown (.md) segregados por data e tipo de plano
3. Gustavo está testando processamento de PDFs com o Gus — já fez um teste e agora vai testar outro
   *(2026-04-27)*

1232. O projeto `claude-code` contém uma estrutura de demandas organizadas em `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

1233. O ciclo de vida dos fragmentos no schema gus-18 não está sendo executado como prometido, o que gera uma dívida técnica silenciosa.
   *(2026-05-03)*

1234. O hub Qdrant é a nova arquitetura que armazena a memória central do Gus.
   *(2026-05-03)*

1235. É necessário não remover a variável MCP_AUTH_DISABLED que deve ser mantida como true.
   *(2026-05-03)*

1236. Foi recomendado que o curador mudasse sua implementação para utilizar ingestão em tempo real.
   *(2026-05-02)*

1237. As memórias são processadas em tempo real com uma dupla chamada de LLM, passando pelo Haiku e pelo GPT.
   *(2026-05-03)*

1238. O curador Gus utiliza Haiku e GPT-4o-mini em paralelo para gerar respostas.
   *(2026-05-03)*

1239. Um total de 204 fragmentos da coleção legada ainda não foram migrados e permanecem no Mem0 SaaS.
   *(2026-05-03)*

1240. O TioGu utiliza o framework python-telegram-bot na versão 21.6.
   *(2026-05-02)*

1241. A stack de memória está em estado intermediário arriscado, pois o Hub Qdrant é a nova fonte, mas a coleção legada ainda está ativa.
   *(2026-05-03)*

1242. Os arquivos 'gus-01 a gus-09' são considerados desnecessários para leitura, a menos que por curiosidade histórica.
   *(2026-05-02)*

1243. O sistema espera um comportamento de redundância e resiliência através do uso de múltiplos provedores de LLM.
   *(2026-05-02)*

1244. Uma das demandas pendentes é a `2026-05-01-drive-sync-oauth-fix.md`.
   *(2026-05-02)*

1245. O sistema não registrou novas memórias recentemente, o que pode afetar a continuidade das atualizações.
   *(2026-05-02)*

1246. Arquivo `gus-bootstrap.md` contém manual operacional do Gus e regras de comportamento.
   *(2026-05-03)*

1247. 2 demandas pendentes pra essa porta: `dialogos/inbox-/`.
   *(2026-05-02)*

1248. O Hub Qdrant é a fonte da verdade para dados.
   *(2026-05-03)*

1249. Gustavo é anestesiologista e não programa. Toda implementação passa pelo Gus/Tiogu.
   *(2026-05-03)*

1250. O bot do Telegram, TioGu, possui 21 ferramentas distintas integradas.
   *(2026-05-02)*

1251. O último dia de captura no Mem0 SaaS foi em 26/04.
   *(2026-05-03)*

1252. Os arquivos incluem `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md` e `_frontmatter-referencia.md`.
   *(2026-05-02)*

1253. O bot Telegram (TioGu) tem ~21 tools, multimídia, prompt caching, e opera em Railway.
   *(2026-05-02)*

1254. O Gustavo é anestesiologista e não programa; toda implementação passa pelo Gus.
   *(2026-05-03)*

1255. Curador tem dois processos principais: `ingest_chat_raw.py` e `curador_claude_code.py`. Ambos precisam ser auditados.
   *(2026-05-03)*

1256. O ambiente precisa ter o `ANTHROPIC_API_KEY` configurado para evitar erro no log do retro-engine auto-gerado.
   *(2026-05-03)*

1257. A decisão sobre o parâmetro drop_pending_updates pode ser alterada para uma abordagem que avise o usuário em caso de mensagens descartadas durante interrupções.
   *(2026-05-02)*

1258. O Hub Qdrant é a memória central do Gus, onde informações são armazenadas.
   *(2026-05-03)*

1259. Os arquivos com as demandas pendentes são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template `_frontmatter-referencia.md`.
   *(2026-05-03)*

1260. A demanda dialogos/inbox-claude-code tem 3 pendências.
   *(2026-05-03)*

1261. O passo para criar um Service Account e configurar a WIF já foi realizado, o que elimina a necessidade de decidir entre as opções de Drive sync.
   *(2026-05-03)*

1262. Os JSONs estruturados de exames LAFE de janeiro de 2026 estão no caminho Gus-Sync/pessoal/saude/gus__2026-01-27__lafe.json.
   *(2026-05-02)*

1263. A auditoria do Chat envolve todos os aspectos relacionados ao projeto Claude Chat.
   *(2026-05-03)*

1264. Quatro demandas pendentes foram identificadas no dialogos/inbox-claude-code.
   *(2026-05-02)*

1265. Gustavo precisa adicionar saldo em console.anthropic.com/settings/billing.
   *(2026-05-03)*

1266. O sistema tem suporte a captura multimídia via integração com o Claude Chat.
   *(2026-05-02)*

1267. D4 propõe mover o arquivo dimagem.py para a pasta integrations para melhor sinalização de dependências.
   *(2026-05-02)*

1268. Bootstrap gus-chat atualizado pra v6 (02/05/2026): captura real-time via MCP como padrão, 2 caminhos documentados, brain gus agora recebe meta_reflexao e identidade_operacional do Chat. Refs Mem0 removidas, paths curador/hub atualizados. PR #77 renomeia legacy mem0 → curador/hub.
   *(2026-05-02)*

1269. URL secret protege.
   *(2026-05-03)*

1270. A demanda `2026-05-01-captura-multiporta-curador.md` precisa de um gatilho proativo no Chat.
   *(2026-05-03)*

1271. A migração coleta dual Haiku × Sonnet roda até 12/05.
   *(2026-05-02)*

1272. A coleta de dados no Hub é realizada em modo dual: Haiku e Sonnet/GPT em paralelo.
   *(2026-05-02)*

1273. Interações no celular agora podem ser feitas criando arquivos diretamente na nova pasta no Drive, sem necessidade de YAML.
   *(2026-05-03)*

1274. O Chat deve ler seu estado e o bootstrap do Drive para garantir informações atualizadas.
   *(2026-05-03)*

1275. As pendências de Gustavo incluem setar `MCP_URL_SECRET` no Railway e decidir sobre a sincronização do Drive.
   *(2026-05-03)*

1276. As metas e decisões durante o projeto estão sendo decididas na aba separada.
   *(2026-05-02)*

1277. Gus é um sistema de agente pessoal multi-porta que opera através de interfaces como Telegram, Claude Code e Claude Chat, e será expandido no futuro para incluir Custom GPT mobile e Alexa.
   *(2026-05-03)*

1278. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa.
   *(2026-05-02)*
