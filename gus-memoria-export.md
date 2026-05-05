---
exportado_em: 2026-05-04T05:13:12
total: 4396
fonte: hub-qdrant
---

# Memórias do Gustavo — Export Hub Qdrant

*Última atualização: 04/05/2026 às 05:13*

1. O projeto Phronesis está em publicação e revisão no Alignment Forum.
   *(2026-05-03)*

2. Os PRs mergeados post 02/05/2026 incluem melhorias no curador e correções de bugs críticos.
   *(2026-05-03)*

3. A migração para o Hub Qdrant está em curso, com o objetivo de aposentadoria do Mem0 SaaS.
   *(2026-05-03)*

4. O Hub Qdrant é a memória central do sistema.
   *(2026-05-03)*

5. No projeto, as demandas pendentes se referem a quatro tarefas: captura multiporta curador, drive sync oauth fix, pendências da Claude Chat consolidadas, e um template.
   *(2026-05-02)*

6. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) terminará em 12/05/2026.
   *(2026-05-03)*

7. O cache de mídia do bot não possui gerenciamento de orçamento em bytes, o que pode causar falhas de memória.
   *(2026-05-02)*

8. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

9. Estou na branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

10. A comunicação com a API do Mem0 SaaS deve ser verificada para confirmar a existência de conteúdos históricos e decidir sobre a eliminação do secret.
   *(2026-05-03)*

11. Gustavo tem hipertireoidismo em tratamento.
   *(2026-05-04)*

12. Gustavo está em tratamento de hipertireoidismo.
   *(2026-05-03)*

13. O MCP está público, permitindo que qualquer scanner leia todo o Hub.
   *(2026-05-03)*

14. O estado final dos PRs já tá no código + nos docs gus-XX atualizados.
   *(2026-05-03)*

15. A instrução correta para o Chat ao ser ativado é responder de forma casual e breve, informando que está pronto.
   *(2026-05-03)*

16. O Gus é um sistema de agente pessoal multi-porta que se comunica através de diferentes plataformas como Telegram, Claude Code e Claude Chat.
   *(2026-05-03)*

17. O sistema de captura de fragmentos do Chat estava quebrado devido ao bug.
   *(2026-05-02)*

18. Um total de 208 fragmentos foi exportado da Mem0 SaaS para o diretório de histórico.
   *(2026-05-03)*

19. O status dos fragmentos que não são classificados polui o Hub com dados irrelevantes.
   *(2026-05-03)*

20. Os '204 fragmentos históricos' estavam mesmo lá. Hipótese A8.1 confirmada: estavam no Mem0 SaaS (api.mem0.ai).
   *(2026-05-03)*

21. A proposta é criar a estrutura 'dialogos/Gustavo/' com subpastas para Chat, Code e TioGu.
   *(2026-05-03)*

22. A busca padrão no Hub retorna apenas os fragmentos do brain 'gustavo' a menos que seja especificado 'user_id'.
   *(2026-05-03)*

23. O arquivo `gus-identity.md` tem que ser atualizado para refletir a mudança do Google Drive de 'GitHub-Sync' para 'Gus-Sync'.
   *(2026-05-04)*

24. O conteúdo no Mem0 SaaS inclui 204 fragmentos, com dados biográficos e preferências sobre o trabalho.
   *(2026-05-03)*

25. O sistema de agente pessoal multi-porta usa memória central no Hub Qdrant.
   *(2026-05-03)*

26. O sistema Axon é um sistema de governança contextual entre estados humanos e ações digitais.
   *(2026-05-04)*

27. O conteúdo no Mem0 SaaS possui maior qualidade em comparação aos fragmentos atuais no Hub.
   *(2026-05-03)*

28. A refatoração do `tools.py` foi concluída, dividindo-o em 7 módulos focados, mantendo a estrutura do array TOOLS.
   *(2026-05-04)*

29. O workflow de sincronização entre o Google Drive e o GitHub ainda não está ativo.
   *(2026-05-02)*

30. Os arquivos de estado do projeto sempre devem ser lidos, preferindo a consulta no Hub sobre o arquivo `gus-estado-atual.md`.
   *(2026-05-03)*

31. O `_estado-atual.md` na pasta projetos/gus foi atualizado em 27/04 e está desatualizado para o processo atual.
   *(2026-05-03)*

32. O Gus é um sistema de agente pessoal multi-porta, operando em várias plataformas como Telegram, Claude Code e futuras integrações.
   *(2026-05-03)*

33. A captura de transcripts do Claude Code está quebrada desde 01/05.
   *(2026-05-03)*

34. A decisão final sobre o modelo curador será após 12/05/2026, onde será feita a comparação entre os pares Haiku e Sonnet/GPT.
   *(2026-05-02)*

35. Apenas análise de estado final dos PRs ligado ao código e as documentações atualizadas.
   *(2026-05-03)*

36. O curador do Gus utiliza Haiku e GPT-4o-mini como modelos para processamento.
   *(2026-05-03)*

37. A hierarchy dos canais de escrita no Chat ainda precisa ser definida para melhorar a operação.
   *(2026-05-02)*

38. A fase 4 do projeto envolve a promoção automática de fragmentos da memória de ativo para estável após 30 dias.
   *(2026-05-03)*

39. O bootstrap atual tem 30+ subseções num arquivo só. Não tem TL;DR no topo nem ordem clara "leia A, depois B, C lazy".
   *(2026-05-03)*

40. Drive sync (WIF/PR #76) precisa estar verde para que o bootstrap atualizado chegue no Drive.
   *(2026-05-03)*

41. O arquivo `gus-bootstrap.md` tem 421 linhas e contém a maior parte do contexto necessário para qualquer interação inicial do Chat.
   *(2026-05-04)*

42. O workflow de migração para o Hub revelou que não há fragmentos a migrar da coleção `gus`.
   *(2026-05-03)*

43. A metodologia MGX foi aplicada em projetos passados e se tornou referência para as decisões e desenvolvimentos atuais.
   *(2026-05-03)*

44. A auditoria do Chat revelou possíveis vulnerabilidades de segurança, como o `MCP_URL_SECRET` não configurado, permitindo acesso não autorizado ao Hub.
   *(2026-05-04)*

45. A demanda `2026-05-01-captura-multiporta-curador.md` é parcialmente resolvida pelo PR #67, mas falta o gatilho proativo no Chat.
   *(2026-05-02)*

46. O `auditoria_hub.py` é cego para o brain gus e as classificações são feitas somente por keywords.
   *(2026-05-03)*

47. O projeto está utilizando um sistema multi-porta com Hub Qdrant como memória central conectado a um GitHub como conhecimento e um Drive como espelho.
   *(2026-05-03)*

48. O bot utiliza uma estratégia de caching de prompts e um sistema de retries para lidar com falhas, aumentando a resiliência do sistema.
   *(2026-05-03)*

49. O Hub Qdrant atualmente contém 40 fragmentos, dos quais 70% são considerados lixo.
   *(2026-05-03)*

50. A remoção do fallback de Mem0 sugere uma transição completa para o novo sistema baseado no Hub Qdrant.
   *(2026-05-03)*

51. A primeira fase de testes do projeto já foi concluída, incluindo a validação de PII no output do bot e ajustes de controle de cache para mídia.
   *(2026-05-02)*

52. Há 3 demandas pendentes no `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

53. O Hub Qdrant é a fonte da verdade para o sistema.
   *(2026-05-03)*

54. A captura Claude Code via cron salva transcripts redatados a cada 30 minutos.
   *(2026-05-02)*

55. O `_estado-atual.md` da pasta projetos/gus está desatualizado de 27/04.
   *(2026-05-03)*

56. A demanda `sync-to-drive.yml` deve ser validada após a instalação do WIF e o saldo do Anthropic.
   *(2026-05-03)*

57. O bot do Telegram, TioGu, possui cerca de 21 ferramentas.
   *(2026-05-03)*

58. A estrutura do projeto Gus-Sync contém pastas principais: dialogos, projetos/gus, pessoal, dimagem, _indices e _log.
   *(2026-05-03)*

59. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/` (algumas com nome quebrado — 'Documento sem título.md' provavelmente é lixo de sync).
   *(2026-05-03)*

60. O bot do Telegram, TioGu, possui 21 ferramentas distintas integradas.
   *(2026-05-03)*

61. O arquivo gus-identity.md contém informações sobre quem é Gustavo e quem é o Gus enquanto entidade.
   *(2026-05-03)*

62. Haiku do curador não roda sem créditos.
   *(2026-05-03)*

63. O projeto Gus envolve um sistema multi-porta que conecta vários canais, como Telegram, Claude Code e Claude Chat, usando um Hub Qdrant como memória central.
   *(2026-05-02)*

64. O estado atual do projeto e as atualizações são documentadas no arquivo '_estado-atual.md'.
   *(2026-05-03)*

65. Há uma demanda parada chamada `2026-05-01-captura-multiporta-curador.md`.
   *(2026-05-02)*

66. A auditoria da memória é realizada diariamente, mas atualmente é cega para o brain 'gus' e ignora o campo 'area'.
   *(2026-05-03)*

67. O script `limpeza_hub_dryrun.py` gera relatório de IDs candidatos a delete sem afetar a base atual.
   *(2026-05-03)*

68. As regras DURAS do Bootstrap incluem diretrizes essenciais para a operação do Gus.
   *(2026-05-03)*

69. O Chat A salvou de verdade. Fragmento existe (UUID 42aea182-d4a2-4626-8a85-5ede861b311b), via=claude-chat, brain gus (autoreflexão).
   *(2026-05-03)*

70. O Drive sync GitHub→Drive parece quebrado, com commits indicando atividade até 01/05 e depois nenhum.
   *(2026-05-03)*

71. Gustavo é anestesiologista e não programa. Toda implementação passa pelo Gus.
   *(2026-05-03)*

72. Os itens da Fase 1 foram concluídos e incluem melhorias na auditoria, adição de tags e remoção de código obsoleto.
   *(2026-05-03)*

73. Gus é um sistema de agente pessoal multi-porta, integrando Telegram, Claude Code, Claude Chat e futuras plataformas como Custom GPT mobile e Alexa. A memória central fica no Hub Qdrant.
   *(2026-05-03)*

74. O workflow de migração `migrar_gus_para_hub.py` indica que não há fragmentos na coleção 'gus'.
   *(2026-05-03)*

75. Em paralelo ao trabalho clínico, Gustavo é pesquisador independente ativo em IA e construtor de sistemas, operando múltiplos projetos de pesquisa, produto e arquitetura.
   *(2026-05-04)*

76. A seção 'Personalidade do Gus' deve ser migrada para o arquivo system_prompt.md, que é específico para o bot Telegram.
   *(2026-05-03)*

77. Vou ignorar a Anthropic e créditos, vou mexer nisso depois.
   *(2026-05-04)*

78. Os principais projetos em andamento incluem Phronesis-Bench e NeuroGus.
   *(2026-05-04)*

79. O projeto Gus envolve um bot chamado TioGu, que utiliza um sistema multi-porta com Hub Qdrant como memória central.
   *(2026-05-02)*

80. O Hub Qdrant é a fonte da verdade para o Gus.
   *(2026-05-03)*

81. O sistema de auditoria diária é cego para o brain gus e não valida a presença de fragmentos.
   *(2026-05-03)*

82. Pronto pra ouvir qual o assunto específico que tu quer focar.
   *(2026-05-03)*

83. Gus é um sistema de agente pessoal multi-porta que conecta o Telegram, Claude Code, Claude Chat e futuras integrações.
   *(2026-05-03)*

84. NeuroGus, uma visualização 3D do Hub, está totalmente desenhado e desbloqueia quando as decisões do §11.1-11.5 forem finalizadas.
   *(2026-05-03)*

85. O bug crítico do curador foi corrigido.
   *(2026-05-03)*

86. Fragmentos são processados por um curador, mas o sistema não diferencia entre informações extraídas relacionadas ao Gustavo e suas auto-observações como Gus.
   *(2026-05-03)*

87. O curador Telegram apresenta erro 400 recorrente, resultando em apenas uma entrada por dia. Isso pode indicar que o ingesto do Chat também esteja falhando silenciosamente.
   *(2026-05-03)*

88. Salvou em user_id='gus' mas a Aba B provavelmente buscou em user_id='gustavo' (default). buscar_hub sem o param user_id busca só no brain gustavo.
   *(2026-05-03)*

89. Gustavo está em tratamento para hipertireoidismo.
   *(2026-05-04)*

90. O bot do Telegram (TioGu) possui 21 ferramentas distintas integradas.
   *(2026-05-03)*

91. O Hub Qdrant é a fonte da verdade. Coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

92. Houve um erro na sincronia entre o Heap e o Drive do Gus.
   *(2026-05-02)*

93. 1. Gustavo é anestesiologista e trabalha com o Dimagem (clínica/laboratório de imagem).
2. Gustavo recebe ordens de serviço do Dimagem e precisa acompanhar pacientes agendados.
3. Preferência: Gus deve descrever OS apenas com dados factuais (nome, exame, horário, convênio) — sem análise clínica ou interpretação que Gustavo já domina.
4. Gus deve confirmar leitura correta dos dados e oferecer salvamento no arquivo do dia, sem expandir para análises não solicitadas.
5. Gustavo valoriza eficiência: ruído deve ser eliminado nas respostas do Gus.
   *(2026-04-28)*

94. Foi decidido que a meta_reflexao do agente Gus deve ser capturada durante as conversas.
   *(2026-05-03)*

95. A demanda pro Chat finalizar foi criada e está em 'dialogos/inbox-claude-chat/'.
   *(2026-05-03)*

96. O sistema 'Gus' é um agente pessoal multi-porta que opera em Telegram, Claude Code, Claude Chat, e Custom GPT, com a Alexa planejada como porta futura.
   *(2026-05-04)*

97. A stack de memória está em estado intermediário arriscado, com fallback ativo para a coleção legada 'gus'.
   *(2026-05-03)*

98. Fragments recent itens têm um bug crítico do curador, com `format()` falhando 100% desde 30/04.
   *(2026-05-03)*

99. A implementação do fallback para Vision está prevista para ser realizada em Python com o uso de funções específicas para tratar o conteúdo multimodal.
   *(2026-05-04)*

100. A migração para o Hub Qdrant é regida pela decisão ADR-001, com o objetivo de aposentar a Mem0 SaaS.
   *(2026-05-03)*

101. O último upgrade do SDK do Anthropic foi para a versão 0.97.0 em janeiro de 2025, com mudanças que mantiveram a compatibilidade da API.
   *(2026-05-04)*

102. Se a mensagem de abertura mencionar "Gus", o protocolo Gus Chat é ativado.
   *(2026-05-04)*

103. O projeto `inbox-mem0-from-chat/` é um legado, já que o Mem0 SaaS está aposentado. O nome foi herdado e agora precisa ser renomeado para `inbox-chat-raw/`.
   *(2026-05-03)*

104. O bot Telegram (TioGu) possui aproximadamente 21 ferramentas, multimídia, e cache de prompt em produção no Railway.
   *(2026-05-03)*

105. O Drive sync está quebrado atualmente devido à expiração do token OAuth do Google.
   *(2026-05-03)*

106. O upgrade do SDK da Anthropic para a versão 0.50 está na lista de pendências do projeto.
   *(2026-05-04)*

107. O foco do projeto é desenvolver um sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa).
   *(2026-05-02)*

108. A demanda `2026-05-01-captura-multiporta-curador.md` precisa de um gatilho proativo no Chat.
   *(2026-05-03)*

109. A coleção legada `gus` está vazia e não possui fragmentos históricos.
   *(2026-05-03)*

110. A opção A para o conteúdo do Mem0 SaaS é mantê-lo em `historico/`, enquanto a opção C planeja filtrá-lo e traduzi-lo para importação futura.
   *(2026-05-03)*

111. Bootstrap atual menciona "buscar_hub" mas não destaca que pra brain "gus" precisa passar "user_id='gus'" explicitamente.
   *(2026-05-03)*

112. Gus é um sistema de agente pessoal multi-porta que atua através de plataformas como Telegram, Claude Code, e Claude Chat.
   *(2026-05-03)*

113. O arquivo gus-identity.md apresenta drift em 2 linhas erradas sobre Mem0 e GitHub-Sync.
   *(2026-05-04)*

114. As demandas pendentes no `dialogos/inbox/` incluem captura multiporta, curador bidirecional cron, e oauth para drive-sync.
   *(2026-05-03)*

115. Os 3 passos são todos da porta Claude Chat.
   *(2026-05-03)*

116. Houve uma auditoria que revelou um estado intermediário arriscado da stack de memória, com problemas como 4 chamadas LLM por unidade de input sem mecanismo de deduplicação.
   *(2026-05-03)*

117. As capturas estão funcionando de forma assíncrona no cron GitHub Actions, processadas pelo curador, que já está rodando.
   *(2026-05-02)*

118. Aguarda redeploy (~2 min).
   *(2026-05-03)*

119. A estrutura atual do sistema de escrita do projeto `claude-code` consiste em três canais distintos: escrita em tempo real através de MCP, upload de arquivos .md e demandas inbox.
   *(2026-05-02)*

120. O cache de mídia não tem limite de bytes, o que pode levar a problemas de memória no container do Railway.
   *(2026-05-02)*

121. O `_estado-atual.md` da pasta projetos/gus está desatualizado desde 27/04.
   *(2026-05-03)*

122. Para o estado atual do trabalho a qualquer momento, Gustavo deve consultar o Hub via ego_cache_atual ou fragmentos_recentes, ou ler o arquivo gus-estado-atual.md.
   *(2026-05-03)*

123. O caminho `fallback-mem0` escreve em Mem0 SaaS, o que representa um vetor de perda importante.
   *(2026-05-03)*

124. O próximo redeploy no Railway não deve vazar o segredo novamente após a adição de um pattern para cobrir hex de 32+ chars.
   *(2026-05-03)*

125. Aba nova só precisa olhar PRs se houve uma quebra específica que depende do PR mais recente.
   *(2026-05-02)*

126. Anthropic é usado para documentos, enquanto OpenAI é utilizado para texto.
   *(2026-05-04)*

127. Quando você fala no Chat 'salva no hub que...' ele chama ingestar_fragmento.
   *(2026-05-03)*

128. O MCP está público — qualquer scanner que descobrir a URL Railway lê todo o Hub.
   *(2026-05-03)*

129. O projeto está em processo de migração do sistema Mem0 SaaS para o Hub Qdrant.
   *(2026-05-03)*

130. Há 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

131. O sistema Gus foi atualizado para operar com um Hub Qdrant direto, aposentando o Mem0.
   *(2026-05-04)*

132. A demanda `2026-05-01-captura-multiporta-curador.md` precisa de um gatilho proativo no Chat.
   *(2026-05-03)*

133. Hub Qdrant é a fonte da verdade.
   *(2026-05-03)*

134. Gustavo tem hipertireoidismo em tratamento.
   *(2026-05-04)*

135. A stack tem uma ferramente de auditoria chamada `auditoria_hub.py` que ignora o `area` dos fragmentos.
   *(2026-05-03)*

136. O estado atual do projeto inclui o TioGu com 163 testes verdes, o Claude Chat com 12 fixes de 31 achados e pendências em várias áreas, incluindo a definição de `MCP_URL_SECRET` no Railway.
   *(2026-05-03)*

137. O curador híbrido cross-vendor já cobre '1 vendor caiu'.
   *(2026-05-03)*

138. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

139. O sistema de auditoria atual não abrange a metade da informação disponível no Hub.
   *(2026-05-03)*

140. A decisão de migração ADR-001 visa aposentar a Mem0 SaaS, tornando o Hub Qdrant a fonte da verdade.
   *(2026-05-03)*

141. O tempo que um fragmento permanece ativo no Hub é indefinido se não for feita a promoção automática.
   *(2026-05-03)*

142. O PR #72 foi aberto no repositório Gus para abordar as questões identificadas na auditoria do Chat.
   *(2026-05-02)*

143. O próximo passo da migração será disparar o workflow `migrar-gus-para-hub` para preencher o Hub com as memórias históricas.
   *(2026-05-03)*

144. O segredo devemos configurar no Railway para proteger o MCP.
   *(2026-05-03)*

145. A demanda de atualização dos arquivos de identidade e estado atual é essencial para manter a precisão dos dados.
   *(2026-05-04)*

146. Decisões arquiteturais: 'migração Mem0 Cloud → Qdrant self-hosted, autonomy + permanence rather than renting'.
   *(2026-05-03)*

147. A memória do Gustavo e as reflexões do agente são organizadas em dois brains independentes no Hub Qdrant.
   *(2026-05-03)*

148. O retro-engine registra 'no-op: anthropic_missing' e segue.
   *(2026-05-03)*

149. O passo seguinte envolve recadastrar o Connector claude.ai após a ativação do segredo.
   *(2026-05-03)*

150. A captura multiporta curador é uma das demandas pendentes.
   *(2026-05-03)*

151. X desafios foram identificados: a stack está em estado intermediário arriscado e a poluição cruzada entre os cérebros de Gus e Gustavo se confirma.
   *(2026-05-03)*

152. As buscas realizadas no Hub Qdrant devem retornar respostas relevantes para questões sobre exames anteriores.
   *(2026-05-02)*

153. O bot opera com dependências como python-telegram-bot, anthropic SDK, openai, FastAPI e Qdrant.
   *(2026-05-03)*

154. A pasta do Google Drive se chama Gus-Sync, não GitHub-Sync.
   *(2026-05-04)*

155. O bot Telegram possui ~21 ferramentas distintas implementadas.
   *(2026-05-03)*

156. A aba nova no Drive pode pegar e implementar uma demanda em 2-3 horas.
   *(2026-05-03)*

157. O estado do curador é monitorado, com logs que capturam o comportamento e erros.
   *(2026-05-03)*

158. TioGu está usando duas APIs diferentes: Anthropic e OpenAI. Anthropic é usado para processamento de imagens e PDFs, enquanto OpenAI é usado para texto puro.
   *(2026-05-03)*

159. A coleção legada do Gus ainda contém 204 fragmentos não migrados.
   *(2026-05-03)*

160. O estado atual do projeto Gus envolve a migração para o Hub Qdrant como fonte da verdade.
   *(2026-05-03)*

161. O Hub Qdrant é a fonte da verdade para o projeto.
   *(2026-05-03)*

162. Os maiores arquivos no projeto foram reduzidos de 1140 para 561 linhas, com as funcionalidades divididas em módulos focados.
   *(2026-05-04)*

163. O ciclo de migração da memória 'gus' para o Hub deve ser iniciado manualmente.
   *(2026-05-03)*

164. A migração para o Hub Qdrant está em curso e deve ser concluída até 12/05/2026.
   *(2026-05-03)*

165. NeuroGus é um projeto de visualização do Hub.
   *(2026-05-03)*

166. A memória anterior (Mem0 SaaS) está sendo aposentada e o Hub Qdrant é a nova fonte da verdade.
   *(2026-05-03)*

167. Após o passo 1, o Connector no claude.ai deve ser recriado com a nova URL do MCP.
   *(2026-05-03)*

168. As 18 entradas 'fallback-mem0' de 28/04 foram pro Mem0 SaaS, porque a migração ainda não estava 100% deploy-ada.
   *(2026-05-03)*

169. Sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) com Hub Qdrant como memória central.
   *(2026-05-04)*

170. Se um PR precisa ser lido pra entender o presente, é sinal de doc desatualizado — não de PR importante.
   *(2026-05-03)*

171. Ele tem interesses em segurança em IA, filosofia e systems thinking.
   *(2026-05-04)*

172. A migração do gus para o Hub Qdrant está em curso, e a coleta dual de modelos no curador termina em 12/05/2026.
   *(2026-05-03)*

173. Recentemente, foram focados esforços em hardening: PR #72 corrigiu um bug do curador que falhava 100% (KeyError em chaves JSON do template de prompt); PR #80 redatou vazamento de segredo em logs do MCP; PR #83 introduziu bootstrap-v6 com dois caminhos de captura (real-time MCP + upload curado).
   *(2026-05-03)*

174. O bot Telegram (TioGu) contém aproximadamente 21 tools, multimídia, prompt caching, e está em produção no Railway.
   *(2026-05-03)*

175. O filtro e a tradução dos 204 fragmentos estão planejados para a Fase 5.
   *(2026-05-03)*

176. As operações de deletar fragmentos no sistema não possuem uma trilha de auditoria.
   *(2026-05-03)*

177. O sistema ainda faz fallback para a coleção legada, o que pode causar inconsistências em buscas.
   *(2026-05-03)*

178. O segredo `MCP_URL_SECRET` protege o acesso ao MCP server.
   *(2026-05-03)*

179. Existem 18 entradas que foram capturadas em fallback para Mem0 SaaS, que estão agora fora do Hub.
   *(2026-05-03)*

180. O sistema de agente pessoal Gus tem memória central no Hub Qdrant e arquivos .md no GitHub.
   *(2026-05-03)*

181. Gustavo é anestesiologista e não programa. Toda implementação passa pelo Gus.
   *(2026-05-03)*

182. A stack de memória end-to-end está em estado intermediário arriscado.
   *(2026-05-03)*

183. O Hybrido Curador é um pipeline de extração de fragmentos usando Anthropic e OpenAI em paralelo.
   *(2026-05-03)*

184. O script 'comparar_curadores.py' deve ser implementado para analisar a performance dos modelos.
   *(2026-05-03)*

185. A stack está em estado intermediário arriscado: Hub Qdrant (`gus_hub`) é a fonte nova, mas a coleção legada `gus` (Mem0 self-hosted) tem ~204 fragmentos não-migrados e o código de leitura em `gus/memory.py` ainda faz fallback pra ela.
   *(2026-05-03)*

186. O manual operacional do Gus contém regras de comportamento e como cada porta usa o Hub.
   *(2026-05-03)*

187. Os canais de controle e armazenamento de dados (hub/store) são utilizados para gerenciar a memória do Gus.
   *(2026-05-02)*

188. O `_estado-atual.md` (27/04) está desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).
   *(2026-05-02)*

189. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`. Algumas com nome quebrado — 'Documento sem título.md' provavelmente é lixo de sync.
   *(2026-05-03)*

190. O conteúdo está seguro em `historico/`.
   *(2026-05-03)*

191. Houve uma migração de Mem0 SaaS para Hub Qdrant que se completou em 12/05/2026.
   *(2026-05-03)*

192. O Hub Qdrant é a fonte da verdade.
   *(2026-05-03)*

193. 1. Gustavo estabeleceu protocolo específico de análise de fotos que deve ser seguido nas próximas conversas
2. Gustavo está processando múltiplas imagens de Ordens de Serviço (OS) médicas com datas históricas (09/01/2026)
3. Paciente Analete da Silva Pinto teve exames de RM (Crânio/Encéfalo com Espectroscopia e RM Fluxo Liquórico) + anestesia em Assim São Gonçalo
4. Há questão em aberto sobre como arquivar OS com datas antigas (se salva no arquivo histórico ou ignora)
   *(2026-04-28)*

194. O Hub Qdrant é a memória central do Gus, sendo que os dados operacionais são armazenados em arquivos .md no GitHub.
   *(2026-05-03)*

195. O arquivo gus-identity.md contém informações redundantes que já estão no gus-bootstrap.md.
   *(2026-05-03)*

196. O plano de saneamento da memória inclui 9 itens, sendo essa fase crítica para evitar poluição futura da base de dados.
   *(2026-05-03)*

197. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

198. O hub Qdrant é usado como a memória central do sistema.
   *(2026-05-03)*

199. Próximo passo natural seria Fase 0 — só leituras, valida hipóteses antes de mexer em código.
   *(2026-05-03)*

200. O protocolo de ativação 'Gus' é disparado ao mencionar 'Gus' em uma conversa.
   *(2026-05-04)*

201. Hub Qdrant é a fonte da verdade.
   *(2026-05-03)*

202. NeuroGus é uma visualização 3D do Hub, totalmente desenhado e desbloqueado com as decisões §11.1-11.5.
   *(2026-05-04)*

203. Atualmente, os projetos ativos de Gustavo incluem Phronesis-Bench, NeuroGus, MGE/MGX, TER e Axon.
   *(2026-05-03)*

204. O upgrade da SDK Anthropic foi bem-sucedido, mantendo a compatibilidade com a API anterior, e agora está na versão 0.97.
   *(2026-05-04)*

205. Estou na branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

206. A aposentadoria do Mem0 SaaS está planejada para após 12/05/2026.
   *(2026-05-04)*

207. O TioGu é um bot Telegram baseado em Python.
   *(2026-05-03)*

208. O bot TioGu utiliza um sistema de caching de prompts que reduz custo de input em até 70% em janelas de 5 minutos.
   *(2026-05-02)*

209. No projeto Claude Chat, existe um sistema de captura duplo entre Haiku e Sonnet que roda até 12/05, após isso será decidido o modelo curador final.
   *(2026-05-03)*

210. O estado da coleção gus no Qdrant é vazio e o Mem0 SaaS está dormente na pasta histórico.
   *(2026-05-03)*

211. Conflito em `_estado-atual.md` — duas sessões diferentes do mesmo dia (Fase 1 TioGu via PR #73 + auditoria do Chat).
   *(2026-05-03)*

212. Para configurar o MCP_URL_SECRET no Railway, deve-se gerar dois UUIDs e salvá-los juntos.
   *(2026-05-03)*

213. O sistema "Gus" é um agente pessoal multi-porta que opera em um Hub Qdrant.
   *(2026-05-03)*

214. A função '_resumir_e_salvar' atualmente registra status 'fallback-mem0', mas pode poluir o Hub com fragmentos não-classificados quando falha.
   *(2026-05-03)*

215. O sistema Gus é um agente pessoal multi-porta, operando através de Telegram, Claude Code, e Claude Chat com um MCP Connector.
   *(2026-05-03)*

216. Atualmente, o sistema Gus está em operação, um agente pessoal multi-porta conectado ao Hub Qdrant.
   *(2026-05-04)*

217. O manual operacional do Gus, regras de comportamento e como cada porta usa o Hub estão no arquivo `dialogos/_bootstrap/gus-bootstrap.md`.
   *(2026-05-02)*

218. A captura de multiporta está entre as demandas pendentes.
   *(2026-05-03)*

219. Validar se a URL de health returna status ok e se o path /mcp retorna 404.
   *(2026-05-03)*

220. O arquivo `gus-estado-atual.md` é gerado a cada 15 minutos por um cron e contém informações sobre ego cache, decisões recentes, reflexões ativas e fragmentos das últimas 6 horas.
   *(2026-05-03)*

221. A demanda de Shakira foi capturada na estrutura HTML e está no caminho 'capturado/shakira-copa-2026/index.html'.
   *(2026-05-03)*

222. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

223. O estado atual do Hub Qdrant é considerado arriscado, com 204 fragmentos não migrados e 3 produções simultâneas de fragmentos.
   *(2026-05-03)*

224. Gustavo é anestesiologista no Dimagem e tem hipertireoidismo.
   *(2026-05-03)*

225. Mem0 SaaS possui 204 fragmentos, sendo 188 em inglês e 16 em português.
   *(2026-05-03)*

226. Coleta dual de modelos no curador (Haiku × GPT-4o-mini, mudou de Sonnet em 29/04 por custo/resiliência) termina 12/05/2026.
   *(2026-05-03)*

227. A coleção legada `gus` na Qdrant está vazia e não possui fragmentos históricos.
   *(2026-05-03)*

228. Gustavo é anestesiologista, não programa — toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

229. O arquivo gus-identity.md foi deletado.
   *(2026-05-03)*

230. O MCP server está público — qualquer scanner que descobrir a URL Railway pode ler todo o Hub.
   *(2026-05-03)*

231. Gustavo Pratti de Barros é anestesiologista.
   *(2026-05-03)*

232. O processador do MCP deve ser reconfigurado para evitar vazamentos futuros.
   *(2026-05-03)*

233. O estado da migração ADR-001 está em curso e a coleta dual de modelos no curador termina em 12/05/2026.
   *(2026-05-03)*

234. É necessário setar o `MCP_URL_SECRET` no Railway para proteger o MCP.
   *(2026-05-03)*

235. O bot tem um ponto de falha silencioso ao atingir o limite de uso da API, respondendo apenas a quem envia uma mensagem, sem notificações proativas.
   *(2026-05-02)*

236. Gustavo é falante nativo de português, baseado no Rio de Janeiro.
   *(2026-05-04)*

237. Ele tem hipertireoidismo sob tratamento com Tapazol, acompanhado por um endocrinologista.
   *(2026-05-04)*

238. O MCP está público em gus-mcp-server-production.up.railway.app/mcp e precisa de um URL secret para proteção.
   *(2026-05-03)*

239. 26/04 foi o último dia de captura no Mem0 SaaS.
   *(2026-05-03)*

240. Tô aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

241. Logs do Railway mostram que o MCP montado em /<URL_SECRET (64 chars)>/mcp.
   *(2026-05-03)*

242. O nome 'mem0-from-chat' é puramente legado.
   *(2026-05-03)*

243. A curadoria do Telegram está apresentando erro 400 recorrente, resultando em apenas uma entrada por dia com erro nos logs.
   *(2026-05-03)*

244. Farinha de trigo com maior elasticidade é crucial na fabricação de massas para macarrão.
   *(2026-05-03)*

245. A auditoria diária é cega para o brain `gus`, pois ignora o `area` que o curador já preencheu.
   *(2026-05-03)*

246. 1. Gustavo trabalha com um projeto chamado **NeuroGus** — chegaram 3 demandas novas no dia 28/04 (briefing, arquitetura, código v1)
2. Existe um sistema de **múltiplos canais de comunicação** com o Gus (Gus Chat e Gus direto) — mesma entidade, portas diferentes
3. Gustavo usa **workflows automatizados** (ex: `import-from-drive.yml`) para trazer demandas do GitHub
4. Preferência de Gustavo: quer que Gus **dispare workflows e leia demandas automaticamente**, sem esperar aprovação caso estejam prontas
   *(2026-04-28)*

247. Atualmente, o arquivo '_estado-atual.md' está desatualizado desde 27/04.
   *(2026-05-04)*

248. A migração ADR-001 visa aposentar a Mem0 SaaS e consolidar o Hub Qdrant como a fonte da verdade.
   *(2026-05-03)*

249. O primeiro passo para resolver o problema identificado é mergear o PR #72 e aguardar o CI passar.
   *(2026-05-02)*

250. O bot Telegram chamado TioGu possui uma arquitetura multi-provider com fallback cross-vendor.
   *(2026-05-02)*

251. O arquivo `gus-identity.md` está desatualizado e precisa ser corrigido para remover informações sobre o Mem0.
   *(2026-05-04)*

252. Estou na branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

253. O bot Telegram, chamado TioGu, possui 21 ferramentas e utiliza prompt caching.
   *(2026-05-04)*

254. Gustavo viaja com a esposa e está desenvolvendo uma casa em Paty do Alferes.
   *(2026-05-03)*

255. A demanda '2026-05-01-captura-multiporta-curador.md' foi arquivada.
   *(2026-05-03)*

256. TioGu e Retro Engine são independentes e não são impactados pelas demandas na porta Claude.
   *(2026-05-03)*

257. O ciclo de vida dos fragmentos deve incluir atualização de peso, acessos e promover a estabilidade após 30 dias.
   *(2026-05-03)*

258. Gus está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

259. Foi identificado um bug crítico no curador que causava falhas no método format() desde 30/04.
   *(2026-05-03)*

260. Gustavo pediu um panorama geral do projeto antes de focar em um assunto específico.
   *(2026-05-02)*

261. A futura auditoria (no fluxo do projeto) deve rastrear `motivo` do delete com mais evidência e relatar mudanças relevantes no hub Qdrant.
   *(2026-05-03)*

262. O Phronesis-Bench é um projeto ativo em fase de publicação.
   *(2026-05-03)*

263. O estado de migração ADR-001 está em curso, com o objetivo de aposentar o Mem0 SaaS e garantir que o Hub Qdrant seja a fonte da verdade.
   *(2026-05-03)*

264. O cron de auditoria diária ignora o brain gus e classifica por keywords.
   *(2026-05-03)*

265. Gustavo Pratti de Barros é anestesiologista e não programa, toda implementação passa pelo Gus.
   *(2026-05-03)*

266. O curador não seta estado (default vira ativo). Ninguém promove fragmentos pra estavel.
   *(2026-05-03)*

267. Gustavo é anestesiologista, sem experiência em programação. Toda implementação passa pelo Gus.
   *(2026-05-03)*

268. O bot Telegram opera com dependências como python-telegram-bot, anthropic SDK, openai, FastAPI e Qdrant.
   *(2026-05-03)*

269. O projeto NeuroGus está em fase de desbloqueio após decisões sobre os §§11.1-11.5, focando na visualização 3D do Hub.
   *(2026-05-03)*

270. Gustavo é anestesiologista e apresenta hipertireoidismo.
   *(2026-05-04)*

271. Os arquivos de protocolos devem ser separados e chamados somente quando necessário, evitando carregar informações desnecessárias no boot.
   *(2026-05-03)*

272. O estado atual do projeto é a coleta dual de modelos Haiku e GPT-4o-mini, que termina em 12/05/2026.
   *(2026-05-03)*

273. O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).
   *(2026-05-03)*

274. As atualizações recentes do projeto estão registradas em PRs no código.
   *(2026-05-03)*

275. O `gus-estado-atual.md` deve ser gerado a cada 15 minutos e refletir o estado dinâmico do sistema.
   *(2026-05-03)*

276. Os testes em produção são feitos para garantir o comportamento correto do bot.
   *(2026-05-02)*

277. A stack de memória end-to-end é composta por entradas de múltiplas fontes, procedimentos de ingestão e um Hub curador híbrido que combina Haiku e GPT-4o-mini.
   *(2026-05-03)*

278. O sistema atual não tem integração de testes unitários para a maioria das funcionalidades.
   *(2026-05-02)*

279. O curador tem 4 chamadas LLM por unidade de input (Haiku × GPT × {gustavo, gus}).
   *(2026-05-03)*

280. A primeira fase do NeuroGus está totalmente pré-definida e desbloqueada.
   *(2026-05-03)*

281. O segredo `MCP_URL_SECRET` deve ser gerado como uma string de ~64 caracteres hex, obtida a partir de 2 UUIDs concatenados sem hífens.
   *(2026-05-03)*

282. Logs do Railway mostram o segredo ativo do MCP.
   *(2026-05-03)*

283. Gustavo toma decisões sobre a estrutura do projeto Gus e sua implementação através de um conjunto de arquivos no GitHub.
   *(2026-05-03)*

284. A estrutura de retorno do curador considera vários fatores, mas não existem mecanismos de deduplicação.
   *(2026-05-03)*

285. O sistema Gus é um agente pessoal multi-porta, incluindo Telegram, Claude Code e outros futuros.
   *(2026-05-03)*

286. A captura de memória dos diálogos com o TioGu foi aprimorada para garantir que as informações sensíveis sejam processadas de forma segura.
   *(2026-05-03)*

287. 1. Caminho completo da pasta de demandas do Gus: `Gustpbbr/Gus/dialogos/inbox-tiogu/`
2. PR #14 foi mergeado hoje (protocolo de portas e tools) — Gustavo pode querer revisar a documentação nova sobre análise de portas e ferramentas
3. Infraestrutura de automação está funcionando: auditoria automática, export diário do Hub e capture de sessão rodando conforme esperado
4. Hook de fim de sessão do retro-engine está funcional (2 entradas registradas ontem à noite)
   *(2026-04-28)*

288. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa.
   *(2026-05-02)*

289. A frequência sugerida para a captura proativa do Chat foi categorizada em modos: agressivo, balanceado e conservador.
   *(2026-05-03)*

290. Temos 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao e o `_frontmatter-referencia.md` é só template.
   *(2026-05-03)*

291. A auditoria diária em `auditoria_hub.py` ignora o brain `gus` e classifica por keywords.
   *(2026-05-03)*

292. Existem 3 demandas paradas em 'dialogos/inbox-claude-code/'.
   *(2026-05-02)*

293. Gustavo está em tratamento para hipertireoidismo.
   *(2026-05-04)*

294. Vou olhar gus-30 (NeuroGus) por partes + PRs recentes mais relevantes pra fechar o gap pós-27/04.
   *(2026-05-03)*

295. O connector do Gus Hub precisa ser recadastrado no claude.ai devido ao ponto de falha na URL.
   *(2026-05-02)*

296. Houve um merge de um pull request relacionado a testes de regressão do curador.
   *(2026-05-02)*

297. Existem 6 demandas pendentes no inbox-claude-code, das quais 3 são reais, relacionadas à captura multiporta, curador bidirecional cron, e drive-sync OAuth.
   *(2026-05-03)*

298. Gustavo é anestesiologista e não programa, o que implica que toda implementação passa pelo Gus.
   *(2026-05-03)*

299. Arquivo `gus-identity.md` define quem é o Gustavo e quem é o Gus enquanto entidade.
   *(2026-05-03)*

300. Algumas demandas têm nome quebrado — 'Documento sem título.md' provavelmente é lixo de sync.
   *(2026-05-03)*

301. Desde 02/05, o projeto TioGu possui um logger que rastreia as operações no Hub Qdrant.
   *(2026-05-03)*

302. O arquivo 'dialogos/_bootstrap/gus-bootstrap.md' é o manual operacional do Gus, contendo as regras de comportamento e como cada porta usa o Hub.
   *(2026-05-02)*

303. Hub é a memória central conectada a vários serviços, como Telegram, Claude Code e Claude Chat.
   *(2026-05-02)*

304. Foram propostos dois fixes: um para limpar fragmentos obsoletos no Hub e outro para ajustar a resposta de boot do Chat.
   *(2026-05-03)*

305. Algumas demandas têm nome quebrado — "Documento sem título.md" provavelmente é lixo de sync.
   *(2026-05-03)*

306. O MCP está público, permitindo que qualquer scanner que descobrir a URL Railway leia todo o Hub.
   *(2026-05-03)*

307. Status pós-Shakira: Inbox claude-code só tem uma demanda pendente com 2 itens já feitos.
   *(2026-05-03)*

308. O projeto NeuroGus está com planejamento 100% pronto e falta a implementação.
   *(2026-05-02)*

309. O projeto Gus é um sistema de agente pessoal multi-porta que integra diversas plataformas, como Telegram e Claude Chat, utilizando uma memória central chamada Hub Qdrant.
   *(2026-05-03)*

310. O `_estado-atual.md` (27/04) está desatualizado e não reflete muitas atualizações posteriores documentadas no git, como PRs #57, #60, #63, #64 e #67.
   *(2026-05-02)*

311. Os arquivos.lazy (gus-protocolo-demanda.md, gus-protocolo-drive.md, gus-pastas-do-projeto.md e gus-tipos-fragmento.md) serão carregados sob demanda quando o Gus precisar de informações mais específicas.
   *(2026-05-03)*

312. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

313. O bot do Telegram, TioGu, possui cerca de 21 ferramentas e opera integrando dependências como python-telegram-bot e FastAPI.
   *(2026-05-03)*

314. A arquitetura do sistema é baseada no processamento paralelo entre vários modelos de linguagem, utilizando fallback em caso de falhas.
   *(2026-05-02)*

315. A variável MCP_URL_SECRET protege o Hub.
   *(2026-05-03)*

316. As demandas pendentes na porta inbox-claude-code incluem: captura multiporta curador, sincronização de OAuth quebrada, e pendências consolidadas do Claude Chat.
   *(2026-05-03)*

317. O passo 6 é validar end-to-end com uma nova conversa no Chat.
   *(2026-05-03)*

318. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

319. O estado do sistema está em risco com a poluição de informações cruzadas entre os brains 'gustavo' e 'gus'.
   *(2026-05-03)*

320. O timeline de atualização das memórias do Claude deve ser recalibrado com as informações mais recentes sobre o sistema Gus.
   *(2026-05-03)*

321. Agora o sistema redigirá o segredo, mas deve haver continuidade nos logs com a confirmação da segurança.
   *(2026-05-03)*

322. A auditoria identificou a necessidade de integrar uma lógica clara para hierarquizar os canais de escrita do Chat.
   *(2026-05-03)*

323. Mem0 foi aposentado desde 27/04/2026. Hub Qdrant é a fonte única de memória.
   *(2026-05-03)*

324. O bot opera com dependências como python-telegram-bot, anthropic SDK, openai, FastAPI e Qdrant.
   *(2026-05-03)*

325. O estado final dos PRs já está no código e nos docs gus-XX atualizados. PRs descrevem o caminho, não onde a gente está.
   *(2026-05-03)*

326. O arquivo gus-identity.md foi completamente deletado como parte da refatoração.
   *(2026-05-04)*

327. O estado final dos PRs já está no código + nos docs gus-XX atualizados.
   *(2026-05-04)*

328. A seção 'Personalidade do Gus (somente Telegram)' não se aplica a outras portas do sistema.
   *(2026-05-03)*

329. TioGu possui ~21 ferramentas integradas e opera em Railway.
   *(2026-05-03)*

330. O estado final dos PRs já está no código + nos docs gus-XX atualizados.
   *(2026-05-03)*

331. O sistema Gus está em produção — um agente pessoal multi-portas rodando em um backbone do Hub Qdrant.
   *(2026-05-03)*

332. A stack está em estado intermediário arriscado: Hub Qdrant é a fonte nova, mas a coleção legada tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

333. Demanda '2026-05-01-captura-multiporta-curador.md' foi arquivada após a implementação.
   *(2026-05-03)*

334. Houve um bug crítico no curador em 30/04/2026, onde o comando format() falhou 100% com KeyError no JSON literal.
   *(2026-05-03)*

335. O estado da migração revela que a coleção `gus` está vazia.
   *(2026-05-03)*

336. Se o secret 'MEM0_API_KEY' ainda existir, é possível verificar o conteúdo do Mem0 SaaS.
   *(2026-05-03)*

337. Gustavo Pratti de Barros é anestesiologista e não programa — toda implementação passa pelo Gus.
   *(2026-05-03)*

338. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

339. A sequência correta após regenerar o secret é: merger PR #80, aguardar redeploy, rotacionar secret, recadastrar o Connector no claude.ai.
   *(2026-05-03)*

340. As pendências na coleção de memórias legadas serão revisitadas antes da Fase 1 do projeto.
   *(2026-05-03)*

341. A fonte de verdade sobre quem é o Gus e quem é o Gustavo não está centralizada, levando a inconsistências entre arquivos.
   *(2026-05-03)*

342. A opção A para a abordagem com o legado Mem0 SaaS foi aceita.
   *(2026-05-03)*

343. O curador Telegram apresenta erro 400 recorrente, com apenas uma entrada por dia, sempre mostrando erro.
   *(2026-05-03)*

344. 640 PRs no código significam ruído gigante no contexto para ganho zero.
   *(2026-05-03)*

345. A stack está em estado intermediário arriscado: Hub Qdrant é a fonte nova, mas a coleção legada gus tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

346. Cada chamada LLM já é Haiku + GPT em paralelo.
   *(2026-05-03)*

347. O arquivo `gus-identity.md` é redundante com `gus-bootstrap.md` e está desatualizado.
   *(2026-05-03)*

348. O sistema usa Hub Qdrant como memória relacional do Gustavo e autorreflexão do agente.
   *(2026-05-03)*

349. O curador híbrido falhava silenciosamente e o sistema gravava no Mem0 antigo, levando a perda de dados.
   *(2026-05-03)*

350. Destrava também escrita real-time do Chat (ingestar_fragmento).
   *(2026-05-03)*

351. Estou aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

352. O arquivo gus-bootstrap.md contém informações essenciais para a operação do Gus.
   *(2026-05-03)*

353. Mem0 SaaS deve ser aposentado. O Hub Qdrant é a fonte nova e única de verdade.
   *(2026-05-03)*

354. O Hub é mais fresco que gus-estado-atual.md, que é um snapshot das 03h.
   *(2026-05-02)*

355. O projeto Gus é um sistema de agente pessoal multi-porta que integra diversas plataformas, gerenciando informações em um Hub central.
   *(2026-05-03)*

356. A proposta de otimização B envolve quebrar o bootstrap em arquivos por função, reduzindo a carga inicial do sistema.
   *(2026-05-03)*

357. As frentes mais ativas nos últimos dias são relacionadas ao PR #60 (MCP URL secret) e PR #64 (cron captura transcripts Claude Code).
   *(2026-05-02)*

358. O projeto Gus utiliza o Hub Qdrant como fonte única de memória, aposentando o Mem0.
   *(2026-05-03)*

359. A identidade do Gustavo e do Gus deve ser consolidada no `gus-bootstrap.md` e não em um arquivo separado.
   *(2026-05-03)*

360. O arquivo `gus-tipos-fragmento.md` deve conter o schema gus-18 completo, exemplos e anti-exemplos de tipos válidos, e a diferenciação entre os brains `gustavo` e `gus`.
   *(2026-05-04)*

361. O bootstrap não apresenta um entry point claro ou ordem de leitura, o que confunde o Chat.
   *(2026-05-03)*

362. O modelo do Chat ignora Haiku e só registra fragmentos com `curador: gpt`, o que levanta a dúvida se Haiku está silenciado ou se há um problema de filtragem.
   *(2026-05-03)*

363. Os testes de regressão foram adaptados para incluir verificação dos campos Usage, Message e exceptions da API Anthropic.
   *(2026-05-04)*

364. Os quatro arquivos essenciais para qualquer nova aba são: `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md` e `estado-atual.md`.
   *(2026-05-03)*

365. Não há testes automatizados implementados para o bot, o que representa um alto risco na manutenção do sistema.
   *(2026-05-02)*

366. O bot possui uma arquitetura com um coração em bot.py que gerencia os handlers e o estado.
   *(2026-05-02)*

367. A captura de memória e o funcionamento das APIs ocorrem em módulos, com divisão clara de responsabilidades.
   *(2026-05-03)*

368. O bot lida com PDF s de forma específica, orientando o usuário para enviar screenshots quando o Anthropic não pode processá-los.
   *(2026-05-04)*

369. O estado da migração indica que a coleção legada `gus` (Mem0 SaaS) tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

370. Em volume crescente, brain gus vira cópia ruidosa do brain gustavo.
   *(2026-05-03)*

371. O sistema Gus registra uma série de auditórias para garantir a qualidade das memórias e a funcionalidade do Hub.
   *(2026-05-03)*

372. Estou aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

373. O curador está rodando em loop com 100% de erro há mais de 3 dias.
   *(2026-05-02)*

374. A reescrita do `system_prompt.md` removendo drift é recomendada para preservar o comportamento crítico do bot.
   *(2026-05-04)*

375. Os 4 arquivos `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md`, `estado-atual.md` dão 80% do contexto pra qualquer aba nova.
   *(2026-05-03)*

376. O sistema multi-porta (Telegram, Claude Code, Claude Chat, Custom GPT, Alexa) utiliza o Hub Qdrant como memória central.
   *(2026-05-04)*

377. O Hub atual já tem 70% de meta-lixo — não vale arriscar mais.
   *(2026-05-03)*

378. O PR #76 resolve a migração para WIF e já configurou os secrets necessários.
   *(2026-05-03)*

379. A arquitetura do bot é modular, separando funcionalidades em diferentes arquivos, como handlers para diferentes tipos de mensagens (texto, foto, documento, voz) e um arquivo de estado para persistência de dados.
   *(2026-05-04)*

380. O PR #72 corrigiu um bug em produção que impedia o curador de funcionar.
   *(2026-05-02)*

381. Algumas demandas estão com nome quebrado — 'Documento sem título.md' provavelmente é lixo de sync.
   *(2026-05-03)*

382. O `_estado-atual.md` (27/04) está desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).
   *(2026-05-04)*

383. Gus é um sistema de agente pessoal multi-porta com memória central no Hub Qdrant, espelhado no GitHub e no Drive.
   *(2026-05-03)*

384. Hub Qdrant é a fonte da verdade do sistema de Gus, enquanto a coleção legada Mem0 SaaS tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

385. O projeto Gus é um agente pessoal multi-porta operacional, com conexão ao Gus Hub.
   *(2026-05-03)*

386. As demandas pendentes no `dialogos/inbox-claude-code/` são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao.
   *(2026-05-03)*

387. O convênio do paciente é Unimed.
   *(2026-05-03)*

388. O arquivo 'dialogos/_bootstrap/gus-estado-atual.md' é atualizado automaticamente pelo cron a cada 15 minutos.
   *(2026-05-03)*

389. O Gus tá aqui na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

390. Vi que tem 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

391. A seção 'Como fazer o boot' foi adicionada ao bootstrap-v6.2 para orientar o comportamento do Chat durante a ativação.
   *(2026-05-03)*

392. Arquivos iniciais que Claude lê quando inicia incluem `gus-bootstrap.md`, `gus-estado-atual.md` e `gus-identity.md`.
   *(2026-05-04)*

393. Algumas demandas têm nome quebrado, como 'Documento sem título.md', que provavelmente é lixo de sync.
   *(2026-05-03)*

394. O Hub é mais fresco que `gus-estado-atual.md`, que é um snapshot do cron às 03h.
   *(2026-05-03)*

395. Os 204 fragmentos históricos estavam no Mem0 SaaS (api.mem0.ai), não no Qdrant Cloud self-hosted.
   *(2026-05-03)*

396. A migração para o Hub Qdrant está na fase 4 e envolve a coleta dual Haiku e Sonnet até 12/05.
   *(2026-05-03)*

397. O `meta-relatorio-hub.yml` gera `_indices/_meta-relatorio-hub.md` com baseline atual de qualidade.
   *(2026-05-03)*

398. Recomendação de otimização para o bootstrap é dividir o arquivo em core e arquivos lazy.
   *(2026-05-03)*

399. Gustavo Pratti de Barros é anestesista na Dimagem (Rio de Janeiro, 3 unidades) e pesquisador independente em IA.
   *(2026-05-04)*

400. O Hub Qdrant é a única fonte de memória relacional do Gustavo e da autorreflexão do agente.
   *(2026-05-04)*

401. Hub Qdrant é a fonte da verdade e toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

402. O conteúdo dos fragmentos do Mem0 SaaS tem qualidade superior ao Hub atual.
   *(2026-05-03)*

403. O modelo do bot suporta tanto o LLM da Anthropic quanto o da OpenAI, com implementações robustas de tratamento de erros.
   *(2026-05-02)*

404. O curador Telegram apresentou erro 400 recorrente, indicando que falhou em salvar fragmentos e que o processo de captura não estava funcionando corretamente.
   *(2026-05-03)*

405. Estou aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

406. O conteúdo do Mem0 SaaS é 204 fragmentos exportados, e esses dados foram armazenados em `historico/`.
   *(2026-05-03)*

407. Os fragmentos na coleção `gus` no Qdrant nunca foram populados.
   *(2026-05-03)*

408. Uma auditoria foi realizada e constatou a insegurança do MCP Hub, que está acessível publicamente sem `MCP_URL_SECRET`.
   *(2026-05-03)*

409. A operação do sistema está comprometida por 4× multiplicação de chamadas LLM por unidade de input.
   *(2026-05-03)*

410. O MCP está público — qualquer scanner que descobrir a URL Railway lê todo o Hub.
   *(2026-05-03)*

411. O estado final dos PRs está no código e nos docs gus-XX atualizados.
   *(2026-05-03)*

412. O Hub Qdrant é a única fonte da verdade, enquanto a coleção legada Gus tem 204 fragmentos não migrados.
   *(2026-05-03)*

413. O bot Telegram (TioGu) tem ~21 tools, multimídia, prompt caching, e está em produção.
   *(2026-05-02)*

414. Gustavo tem interesse em segurança em IA, filosofia e systems thinking. Ele viaja com a esposa e desenvolve casa em Paty do Alferes.
   *(2026-05-04)*

415. A fase 1 do TioGu foi concluída com 163 testes verdes e limpeza do código.
   *(2026-05-03)*

416. O conteúdo da Mem0 SaaS foi exportado para a pasta 'historico/'.
   *(2026-05-03)*

417. A recadastramento do Connector no claude.ai deve ser realizado após a configuração do `MCP_URL_SECRET`.
   *(2026-05-03)*

418. As opções para a migração dos dados do Mem0 SaaS incluem mantê-los em `historico/`, importar para o Hub ou filtrar e traduzir antes da importação.
   *(2026-05-03)*

419. A recomendação foi a opção B, que envolve manter um arquivo core e criar 3 novos arquivos lazy.
   *(2026-05-03)*

420. O Hub é mais fresco que `gus-estado-atual.md`, que é um snapshot gerado pelo cron.
   *(2026-05-02)*

421. Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`.
   *(2026-05-04)*

422. Amostragem dos 204 fragmentos mostrou que a qualidade do conteúdo é superior ao Hub atual, que é mais meta-conversa.
   *(2026-05-03)*

423. O bootstrap atual é redundante em relação a `gus-identity.md`, que pode ser descartado.
   *(2026-05-03)*

424. Quando o segredo for regenerado e setado no Railway, o Connector deve ser recadastrado.
   *(2026-05-03)*

425. O Hub Qdrant é a nova fonte da verdade para o sistema Gus.
   *(2026-05-03)*

426. A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida pelo PR #67, mas falta o gatilho proativo no Chat.
   *(2026-05-02)*

427. Os próximos passos incluem leitura do `_estado-atual.md`, demandas pendentes e várias atualizações estruturais do projeto.
   *(2026-05-02)*

428. Os passos para rotacionar o secret envolvem: regenerar, atualizar no Railway, aguardar redeploy, e validar log.
   *(2026-05-03)*

429. A migração ADR-001 está em curso e envolve deixar Mem0 SaaS e utilizar o Hub Qdrant como fonte da verdade.
   *(2026-05-03)*

430. A memória central do Gus está localizada no Hub Qdrant, onde são armazenados arquivos .md em um repositório GitHub.
   *(2026-05-03)*

431. A stack de memória end-to-end está em estado intermediário arriscado com Hub Qdrant como fonte nova.
   *(2026-05-03)*

432. A coleção `gus` está vazia — 204 fragmentos prometidos não existem.
   *(2026-05-03)*

433. A captura proativa do Chat agora é instrução explícita no bootstrap.
   *(2026-05-03)*

434. O `MCP_URL_SECRET` deve ser setado no Railway para proteger o acesso ao Hub.
   *(2026-05-03)*

435. O `tipo_esquecimento` é aceito no schema gus-18, mas o filtro de busca ignora esse campo.
   *(2026-05-03)*

436. Gustavo Pratti de Barros é anestesiologista e não programa; toda implementação passa pelo Gus.
   *(2026-05-03)*

437. Hoje o Chat só salva quando pedido, não detecta automaticamente fatos ou decisões relevantes durante a conversa.
   *(2026-05-03)*

438. O estado atual do projeto necessita de manutenção nas funções de curador para evitar a poluição alem do necessário no Hub.
   *(2026-05-03)*

439. Gus está na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

440. Os testes de regressão do curador foram feitos e 12 bugs foram corrigidos.
   *(2026-05-03)*

441. Os 204 fragmentos históricos estavam no Mem0 SaaS (api.mem0.ai), não no Qdrant Cloud self-hosted.
   *(2026-05-03)*

442. O sistema irá eliminar as memórias do Mem0 SaaS, uma vez que todas as 204 frags tenham sido migradas.
   *(2026-05-03)*

443. O arquivo `gus-estado-atual.md` é gerado a cada 15 minutos e é uma captura do que ocorreu desde a última atualização do Hub.
   *(2026-05-04)*

444. O script de exportação do Mem0 SaaS cria um arquivo JSON em 'historico/mem0-export-final-2026-05-02.json' para preservação de dados.
   *(2026-05-03)*

445. A estrutura do sistema Gus e suas interações são complexas, envolvendo múltiplos canais de comunicação e integração.
   *(2026-05-04)*

446. A função do curador é essencial para a migração e integração das memórias no Hub Qdrant.
   *(2026-05-03)*

447. o Hub é mais fresco que gus-estado-atual.md (que é snapshot das 03h).
   *(2026-05-03)*

448. O bot Telegram (TioGu) está integrado com uma arquitetura multi-provedor e um hub centralizado.
   *(2026-05-04)*

449. O trabalho de auditoria atual está em andamento na memória e Hub Qdrant.
   *(2026-05-03)*

450. O arquivo `gus-identity.md` contém drift factual e informação desatualizada.
   *(2026-05-04)*

451. A captura de memória ocorre quando o curador salva os fragmentos da conversa em `_log/resumos-mem0/`.
   *(2026-05-03)*

452. O sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa) tem a memória central no **Hub Qdrant**.
   *(2026-05-03)*

453. O MCP está público — qualquer scanner que descobrir a URL Railway lê todo o Hub.
   *(2026-05-03)*

454. Gustavo Pratti de Barros é a identidade central do sistema Gus.
   *(2026-05-03)*

455. A coleta dual de modelos no curador termina em 12/05/2026, quando Gustavo escolherá o modelo definitivo.
   *(2026-05-03)*

456. O modelo do Chat pode salvar fragmentos sobre Gustavo no brain `gus` sem validação.
   *(2026-05-02)*

457. O sistema de agente pessoal multi-porta integra Telegram, Claude Code e futuras implementações como Alexa.
   *(2026-05-03)*

458. O processamento e execução das demandas devem ser preferidos em ferramentas MCP sobre arquivos .md sempre que possível.
   *(2026-05-03)*

459. A abordagem atual em desenvolvimento gera fragmentos duplicados, poluindo a memória do Gus.
   *(2026-05-03)*

460. A stack de memória está em estado intermediário arriscado: Hub Qdrant é a fonte nova, mas a coleção legada gus (Mem0 self-hosted) tem fragmentos não-migrados.
   *(2026-05-03)*

461. A migração para o Hub Qdrant implica a aposentadoria do Mem0 SaaS.
   *(2026-05-03)*

462. As pastas do Gustavo no Drive devem ser: Chat, Code e TioGu.
   *(2026-05-03)*

463. O nome da pasta pode ser Gustavo, pelo-gustavo ou from-gustavo.
   *(2026-05-03)*

464. O estado final dos PRs já está no código e nos docs gus-XX atualizados. PRs descrevem o caminho, não onde a gente está.
   *(2026-05-03)*

465. O estado atual dos PRs está no código e nos docs gus-XX atualizados, enquanto as decisões arquiteturais devem ser documentadas.
   *(2026-05-03)*

466. O arquivo `gus-identity.md` contém informações erradas sobre a memória relacional utilizada pelo Gustavo.
   *(2026-05-03)*

467. O arquivo gus-identity.md foi deletado e suas informações foram migradas para gus-bootstrap.md e gus/system_prompt.md.
   *(2026-05-03)*

468. A inserção de novas funções deve incluir a implementação de um cron para promover fragmentos de `ativo` para `estavel` após 30 dias.
   *(2026-05-03)*

469. A implementação do lifecycle no esquema gus-18 foi declarado, mas não está sendo executado, afetando a promoção automática de fragmentos no Hub.
   *(2026-05-03)*

470. O arquivo `gus-identity.md` é redundante com o bootstrap e está desatualizado.
   *(2026-05-03)*

471. Gus está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

472. Tô aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

473. O bot Telegram possui ~21 ferramentas distintas implementadas.
   *(2026-05-03)*

474. Não existe script que compare os resultados de Haiku e GPT durante a coleta dual.
   *(2026-05-03)*

475. O Gus é um sistema de agente pessoal multi-porta que conecta diferentes plataformas.
   *(2026-05-03)*

476. A auditoria diária do Hub Qdrant é cega para o brain gus e ignora metade dos fragmentos.
   *(2026-05-03)*

477. A ambiguidade no status 'fallback-mem0' causa confusão, pois o log não reflete com precisão que esses dados vão diretamente para o Hub.
   *(2026-05-03)*

478. As demandas pendentes no inbox-claude-code incluem captura multiporta, curador bidirecional cron e OAuth para sync do Drive.
   *(2026-05-03)*

479. A análise dos logs mostra que a memória Mem0 está sendo usada como fallback, o que é um vetor de perda contínua.
   *(2026-05-03)*

480. Gustavo está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-02)*

481. Os últimos 5 dias mostraram os PRs #67 (curador chat bidirecional + GPT-4o), #64 (captura transcripts Code via cron), #60 (MCP URL secret) e #70 (demanda consolidada).
   *(2026-05-03)*

482. Atualmente opera múltiplos projetos simultaneamente em pesquisa, produto e arquitetura.
   *(2026-05-04)*

483. Gustavo Pratti de Barros é anestesiologista e não programa; toda implementação passa pelo Gus ou Tiogu.
   *(2026-05-03)*

484. As próximas etapas incluem validar a operação do Chat e garantir que o saldo do Anthropic seja reabastecido.
   *(2026-05-03)*

485. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

486. O sistema é um agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa) com memória central no Hub Qdrant.
   *(2026-05-03)*

487. Gustavo Pratti de Barros é anestesiologista no Dimagem, pesquisador independente em IA, e trabalha em múltiplos projetos simultaneamente.
   *(2026-05-04)*

488. A implementação do fallback para Vision será feita através de uma função de conversão de formato de imagem.
   *(2026-05-04)*

489. O último `_estado-atual.md` da pasta projetos/gus está de 27/04 — está desatualizado.
   *(2026-05-03)*

490. O bot Telegram TioGu está estruturado em várias camadas, incluindo bot.py, llm.py, memory.py e tools.py.
   *(2026-05-02)*

491. O conteúdo do Mem0 SaaS é provavelmente padrão ruim do Hub atual, com 70% lixo.
   *(2026-05-03)*

492. O Gus é utilizado por Gustavo, que é anestesiologista e não programa, portanto toda implementação é realizada por Gus ou Tiogu.
   *(2026-05-03)*

493. A migração do Mem0 SaaS para o Hub Qdrant está em curso e prevista para ser concluída em 12/05/2026.
   *(2026-05-03)*

494. O curador híbrido do sistema Gus roda um pipeline de extração de fragmentos utilizando Anthropic e OpenAI em paralelo.
   *(2026-05-04)*

495. O arquivo gus-bootstrap.md deve incluir um TL;DR que informe sobre a identidade compartilhada com outras portas, capacidades do Gus e regras básicas de operação.
   *(2026-05-03)*

496. As mudanças no sistema Gus devem ser comunicadas claramente para garantir a compreensão adequada por parte do Claude.
   *(2026-05-03)*

497. Os quatro arquivos obrigatórios dão 80% do contexto para qualquer aba nova.
   *(2026-05-03)*

498. Tem 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

499. O custo do modelo gpt-4o em relação ao Sonnet é mais barato quando o fallback é ativado.
   *(2026-05-03)*

500. ADR-001 está em curso, com o objetivo de aposentar o Mem0 SaaS e tornar o Hub Qdrant a fonte da verdade.
   *(2026-05-03)*

501. As 204 memórias históricas aguardam migração, mas a coleção legada está vazia.
   *(2026-05-03)*

502. As últimas demandas pendentes no `dialogos/inbox-claude-code/` incluem captura de multiporta curador, correção de OAuth de sincronização do Drive e pendências de consolidação do Claude Chat.
   *(2026-05-03)*

503. Gustavo Pratti de Barros é anestesiologista no Rio de Janeiro, atuando no Dimagem (clínica de imagem diagnóstica com 3 unidades: Nova Iguaçu, Taquara, São Gonçalo).
   *(2026-05-04)*

504. Os 7 docs do checklist anterior te dão o estado atual.
   *(2026-05-03)*

505. O estado de migração para o Hub Qdrant é em curso, visando aposentadoria do Mem0 SaaS.
   *(2026-05-03)*

506. Os 3 passos a serem realizados são: setar `MCP_URL_SECRET` no Railway, recadastrar o Connector no claude.ai e decidir sobre o Drive sync.
   *(2026-05-03)*

507. Gustavo Pratti de Barros é anestesiologista no Dimagem e pesquisador independente em IA, operando múltiplos projetos simultaneamente em pesquisa, produto e arquitetura.
   *(2026-05-03)*

508. A estrutura de pastas e arquivos deve acompanhar a nova nomenclatura, removendo referências ao Mem0.
   *(2026-05-03)*

509. A coleção legada `gus` (Mem0 self-hosted) tem ~204 fragmentos não-migrados e o código de leitura em `gus/memory.py` ainda faz fallback pra ela.
   *(2026-05-03)*

510. O Gus é um agente pessoal multi-porta que interage por Telegram, Claude Code e Claude Chat.
   *(2026-05-03)*

511. Gustavo se envolve com mercados financeiros e educação sobre investimentos como um interesse contínuo.
   *(2026-05-03)*

512. O conteúdo da memória do Gus será reclassificado e traduzido na Fase 5, após a limpeza da Hub.
   *(2026-05-03)*

513. O curador híbrido utiliza Haiku e GPT-4o-mini para gerar respostas.
   *(2026-05-03)*

514. Hub Qdrant é a fonte nova, mas a coleção legada gus (Mem0 self-hosted) tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

515. O sistema multi-porta com Hub Qdrant como memória central opera com GitHub como conhecimento e Drive como espelho.
   *(2026-05-02)*

516. Estão pendentes melhorias para o TioGu: adicionar um teste de regressão pro bug do `_render_prompt()` e reescrever `system_prompt.md`.
   *(2026-05-03)*

517. O sistema atual usa Claude/ChatGPT-Kai/Gemini, informação que faltava no bootstrap e foi adicionada.
   *(2026-05-04)*

518. Esses 4 arquivos dão 80% do contexto pra qualquer aba nova: `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md`, `estado-atual.md`.
   *(2026-05-03)*

519. A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida, mas falta o gatilho proativo no Chat.
   *(2026-05-04)*

520. Gus é um sistema de agente pessoal multi-porta que conecta diferentes plataformas, como Telegram, Claude Code, Claude Chat e outras futuras.
   *(2026-05-03)*

521. A coleção legada 'gus' foi confirmada como vazia, o que implica que não há fragmentos a serem migrados.
   *(2026-05-03)*

522. O estado do Hub é ocioso nas últimas 6 horas.
   *(2026-05-03)*

523. O Chat possui três modos de captura de fragmentos: real-time, upload de .md e demanda em inbox.
   *(2026-05-03)*

524. A otimização do bootstrap pode ser feita através da reordenação para melhorar sua eficácia.
   *(2026-05-03)*

525. Gus está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

526. O bot TioGu é desenvolvido em Python, utilizando a biblioteca python-telegram-bot na versão 21.6.
   *(2026-05-02)*

527. O projeto NeuroGus está bloqueado devido a decisões UX que precisam ser tomadas.
   *(2026-05-03)*

528. Hoje o MCP não permite escrita real-time do Chat por falta do MCP_URL_SECRET.
   *(2026-05-03)*

529. Hub Qdrant é a nova arquitetura que armazena todos os fragmentos de memória.
   *(2026-05-03)*

530. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026, quando Gustavo escolherá o modelo definitivo.
   *(2026-05-03)*

531. O estado final dos PRs já está no código + nos docs gus-XX atualizados.
   *(2026-05-03)*

532. Os 204 fragmentos prometidos não existem na coleção `gus`.
   *(2026-05-03)*

533. O arquivo gus-identity.md é redundante com o bootstrap e está desatualizado.
   *(2026-05-03)*

534. O ADR-001 é a decisão em curso para migrar da Mem0 SaaS para o Hub Qdrant.
   *(2026-05-03)*

535. A stack de memória ainda é considerada em estado intermediário arriscado.
   *(2026-05-03)*

536. A documentação atual do bootstrap não enfatiza que a busca deve ser feita com o parâmetro `user_id` correto.
   *(2026-05-03)*

537. vi que tem 4 demandas pendentes no `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

538. O bootstrap que Claude lê pode ser otimizado.
   *(2026-05-03)*

539. O workflow de migração confirmou que a coleção legada está vazia e não contém fragmentos.
   *(2026-05-03)*

540. O paciente_id canônico é gus (lowercase, sem acentos).
   *(2026-05-02)*

541. Gustavo é anestesiologista e não programa, então toda implementação passa pelo Gus.
   *(2026-05-03)*

542. A arquitetura do bot é composta por um loop de polling do Telegram que se conecta a um modelo de linguagem (llm.py), utilizando o Anthropic Sonnet como principal modelo, com fallback para o OpenAI gpt-4o-mini.
   *(2026-05-03)*

543. URL secret protege o MCP e destrava escrita real-time do Chat (ingestar_fragmento).
   *(2026-05-03)*

544. O bootstrap não tem uma estrutura com entry point claro nem ordem de leitura.
   *(2026-05-03)*

545. A coleção `gus` está vazia.
   *(2026-05-03)*

546. A captura dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

547. Há uma demanda de validação em curso no hub MCP para a segurança do sistema.
   *(2026-05-03)*

548. As linhas 29 e 31 do arquivo `gus-identity.md` apresentam informações falsas sobre o uso de Mem0 e o nome da pasta do Drive.
   *(2026-05-04)*

549. Avanços futuros no projeto incluem a reescrita do system_prompt.md e a revisão de ferramentas e métodos utilizados na integração do bot.
   *(2026-05-02)*

550. A implementação de um alerta proativo para o HARD_LIMIT está entre as altas prioridades a serem abordadas no projeto.
   *(2026-05-02)*

551. As ferramentas do bot Telegram totalizam 21, com multimídia e caching de prompts.
   *(2026-05-03)*

552. O curador documentou que 29/04 a 02/05 o bug no curador foi corrigido.
   *(2026-05-03)*

553. A estrutura de arquivos do TioGu inclui ferramentas diversas, uma camada de memória e funcionalidade de manipulação de mídia.
   *(2026-05-04)*

554. Hub é mais fresco que gus-estado-atual.md, sempre que possível, prefira tools MCP a arquivo .md.
   *(2026-05-03)*

555. Gustavo é anestesiologista, não programa — toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

556. Os arquivos core obrigatórios são: `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md`, `projetos/gus/_estado-atual.md`.
   *(2026-05-04)*

557. A coleta dual Haiku × Sonnet roda até 12/05, depois será decidida o modelo curador final.
   *(2026-05-03)*

558. Os arquivos das demandas paradas são: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, e `_frontmatter-referencia.md`.
   *(2026-05-02)*

559. A stack de memória está em estado intermediário arriscado devido à coexistência da coleção legada `gus` com o novo Hub Qdrant.
   *(2026-05-03)*

560. Atualmente há 3 demandas paradas em dialogos/inbox-claude-code.
   *(2026-05-03)*

561. A coleção legada gus (Mem0) tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

562. Demanda #1 do inbox inclui a ativação do `MCP_URL_SECRET` no Railway para manter a segurança do Hub.
   *(2026-05-04)*

563. Há um bug no curador que resultou em inconsistências na captura de informações entre os diferentes brains.
   *(2026-05-03)*

564. O Hub não tem nenhum fragmento com tipo=identidade_operacional e estado=estavel, nem procedural e estado=estavel.
   *(2026-05-03)*

565. As memórias do Gustavo devem ser atualizadas para refletir a aposentadoria do Mem0 e a adoção do Hub Qdrant como fonte única.
   *(2026-05-03)*

566. Estou aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`, algumas com nome quebrado — 'Documento sem título.md' provavelmente é lixo de sync.
   *(2026-05-03)*

567. Os workflows do GitHub estão funcionando corretamente, com 5 runs recentes, todos OK.
   *(2026-05-03)*

568. As demandas pendentes no inbox-claude-code incluem captura multiporta curador, drive sync OAuth quebrado e pendências do Claude Chat consolidadas.
   *(2026-05-03)*

569. O procedimento de ingesta de dados do Mem0 SaaS envolveu 204 fragmentos que estavam armazenados.
   *(2026-05-03)*

570. Exportação do conteúdo Mem0 SaaS foi completada com sucesso e gravada em histórico.
   *(2026-05-03)*

571. A migração Mem0 para Hub Qdrant está na fase 4 e a coleta dual Haiku × Sonnet roda até 12/05.
   *(2026-05-03)*

572. Hub Qdrant é a fonte da verdade, com memória central onde estão armazenados os dados.
   *(2026-05-03)*

573. O PR #84 contém 8 commits que precisam ser revisados antes do merge.
   *(2026-05-03)*

574. A recomendação é priorizar testes automáticos robustos, especialmente após a refatoração do código.
   *(2026-05-02)*

575. O clipping de arquivos que precisa ser feito depois de um upload no Drive deve seguir a ordem: ler → modificar em container → upload com sufixo → não apagar anterior.
   *(2026-05-03)*

576. O estado atual do projeto tem 20 fragmentos no Hub `gustavo` e 20 no Hub `gus`, sendo que o conteúdo é predominantemente lixo.
   *(2026-05-03)*

577. Gustavo tem hipertireoidismo em tratamento.
   *(2026-05-04)*

578. A função do estado-atual.md é reativa — deve ser lido apenas quando Gustavo perguntar algo específico.
   *(2026-05-03)*

579. Os 19 fragmentos do Hub `gustavo` são consistentes com o Hub estando seco entre 28/04 e 02/05.
   *(2026-05-03)*

580. O estado final dos PRs está no código e nos documentos atualizados, enquanto os PRs descrevem o caminho que foi tomado.
   *(2026-05-03)*

581. A função '_fallback_mem0' foi removida para evitar poluição silenciosa no Hub com entradas não classificadas.
   *(2026-05-03)*

582. A opção B de otimização do bootstrap é a recomendada por trazer ganho real sem risco de perda de informação.
   *(2026-05-03)*

583. No Chat, peça para ele validar se leu o bootstrap e mencionar a versão e os caminhos de captura.
   *(2026-05-03)*

584. Gustavo é anestesiologista e não programa — toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

585. O estado final dos PRs já está no código e nos docs gus-XX atualizados; PRs descrevem o caminho, não onde a gente está.
   *(2026-05-03)*

586. O workflow de migração de `gus` para `gus_hub` revelou que não foram encontrados fragmentos durante a migração.
   *(2026-05-03)*

587. Hipertireoidismo é uma condição de saúde em tratamento por Gustavo.
   *(2026-05-03)*

588. O sistema está em estado intermediário arriscado com débitos que vão estourar quando o volume crescer.
   *(2026-05-03)*

589. O `dimagem.py` é uma integração de domínio e deve ser movido para o diretório `integrations/` para refletir sua natureza.
   *(2026-05-02)*

590. O script para exportar fragmentos do Mem0 SaaS já foi criado e está disponível na pasta de scripts.
   *(2026-05-03)*

591. O curador do sistema utiliza Haiku e GPT-4o-mini para extração de fragmentos.
   *(2026-05-03)*

592. O caminho `fallback-mem0` ainda escreve em Mem0 SaaS e é um vetor de perda contínua.
   *(2026-05-03)*

593. A auditoria do Chat considera aspectos de segurança, confiabilidade e arquitetura do sistema.
   *(2026-05-03)*

594. Ativos projetos incluem Phronesis-Bench, NeuroGus, MGE/MGX, TER e Axon.
   *(2026-05-04)*

595. Os arquivos auxiliares são 'gus-protocolo-demanda.md', 'gus-protocolo-drive.md', 'gus-pastas-do-projeto.md' e 'gus-tipos-fragmento.md'.
   *(2026-05-04)*

596. O LLM Anthropic está utilizando o SDK anthropic na versão 0.40.0.
   *(2026-05-02)*

597. O Hub atualmente não possui nenhum fragmento do tipo identidade_operacional nem procedural que tenha sido promovido a estado estavel.
   *(2026-05-03)*

598. O gap de documentação no bootstrap foi identificado, não esclarecendo a necessidade de usar 'user_id' para buscar no brain 'gus'.
   *(2026-05-03)*

599. O export de fragmentos do Mem0 SaaS resultou em 204 registros, sendo 188 em inglês e 16 em português.
   *(2026-05-03)*

600. Atualmente, Gustavo está em tratamento para hipertireoidismo.
   *(2026-05-03)*

601. Os documentos relevantes para próximos passos e decisões estão localizados em projetos/gus/.
   *(2026-05-02)*

602. Gus está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-02)*

603. A primeira etapa da migração envolve aprovar a nova estrutura e migrar as memórias existentes para o Hub.
   *(2026-05-03)*

604. O sistema tem um risco alto de poluição cruzada entre os brains Gustavo e Gus devido à duplicação de chamadas LLM.
   *(2026-05-03)*

605. O bot TioGu utiliza um sistema multi-porta com Hub Qdrant como memória central e GitHub como conhecimento.
   *(2026-05-02)*

606. Validações são necessárias após a configuração do segredo no Railway, incluindo checar a % URL /health e 404 no endpoint /mcp.
   *(2026-05-03)*

607. Existe uma demanda ativa sobre a sincronização do Drive, a qual está parada.
   *(2026-05-02)*

608. O Chat possui capacidades como utilizar o MCP gus-hub, Drive nativo, Web search, Calendar, Gmail, Spotify e Figma, mas não pode fazer patch in-place no Drive e nem escrita direta no GitHub.
   *(2026-05-03)*

609. Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e o `_frontmatter-referencia.md` que é só template.
   *(2026-05-03)*

610. Vi que tem 4 demandas pendentes no `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

611. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e envolve resolver a questão do refresh token OAuth expirado.
   *(2026-05-02)*

612. A metodologia MGX é um pipeline multi-agente para a geração e avaliação de propostas.
   *(2026-05-04)*

613. A estrutura de auditoria diária ignora completamente metade do Hub.
   *(2026-05-03)*

614. Hub é mais fresco que `gus-estado-atual.md`, que é um snapshot das 03h.
   *(2026-05-03)*

615. Passo 1 deve ser feito: setar MCP_URL_SECRET no Railway.
   *(2026-05-03)*

616. Gustavo está em tratamento para hipertireoidismo.
   *(2026-05-03)*

617. Memória no brain gustavo registra a existência do protocolo de Análise de Exames Laboratoriais.
   *(2026-05-02)*

618. O bot possui uma funcionalidade de caching de prompts que reduz o custo de input em até 70% em janelas de 5 minutos.
   *(2026-05-02)*

619. O Hub Qdrant é a memória central do sistema Gus.
   *(2026-05-03)*

620. A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida, mas falta o gatilho proativo no Chat.
   *(2026-05-03)*

621. As entradas de dados no sistema provêm de várias fontes, incluindo Telegram, Claude Chat e Claude Code, que cada uma gera dados usando protocolos de captura multiporta.
   *(2026-05-03)*

622. O processo de auditoria revelou a poluição de fragmentos entre os brains `gustavo` e `gus`.
   *(2026-05-03)*

623. Os principais fronts ativos no momento incluem TioGu e Claude Chat, com foco na auditoria e saneamento.
   *(2026-05-03)*

624. O Gus é projetado para operar de maneira eficiente, carregando informações conforme necessário em vez de manter tudo disponível sempre.
   *(2026-05-04)*

625. O último fragmento disponível no Hub Qdrant indica que o Hub está ocioso há mais de 6 horas.
   *(2026-05-03)*

626. O Hub Qdrant é a memória central que armazena os dados e é integrado ao sistema multi-porta.
   *(2026-05-03)*

627. Estou aqui para criar um panorama geral do projeto.
   *(2026-05-03)*

628. As frentes de urgência incluem ativar o URL secreto no conector MCP e resolver a falha do curador Telegram.
   *(2026-05-04)*

629. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

630. Memória do Gus é gerenciada via Qdrant com fragmentos ativos e estáveis.
   *(2026-05-03)*

631. A recomendação é mover `gus/dimagem.py` para `integrations/`, sinalizando que é específica do contexto clínico e não parte central do sistema.
   *(2026-05-02)*

632. A estrutura do sistema deve permitir uma fácil manutenção e atualização dos arquivos necessários para o funcionamento do Chat.
   *(2026-05-03)*

633. O projeto tem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template.
   *(2026-05-02)*

634. O projeto NeuroGus entrou em cena e a fase 1 do backend SSE está em uma branch separada, enquanto a fase 2 do frontend está bloqueada.
   *(2026-05-02)*

635. A segurança no MCP Hub é um ponto crítico, pois não possui autenticação configurada corretamente.
   *(2026-05-03)*

636. A demanda da semana pode ser encontrada no arquivo 'dialogos/streams/[semana-2026-04-21.md]'.
   *(2026-05-03)*

637. A decisão de manutenção só em `historico/` foi registrada.
   *(2026-05-03)*

638. As pastas de demanda do Gustavo no Drive serão criadas dentro de dialogos/Gustavo/ com subpastas para Chat, Code e TioGu.
   *(2026-05-03)*

639. TioGu usa dois provedores LLM: Anthropic e OpenAI.
   *(2026-05-04)*

640. A atualização dos documentos de estado atual e de projetos deve ser feita sempre que houver mudanças significativas.
   *(2026-05-02)*

641. A stack de memória end-to-end está em estado intermediário arriscado: Hub Qdrant é a fonte nova, mas a coleção legada gus (Mem0 self-hosted) tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

642. O `_estado-atual.md` é gerado pela automática a cada 15 minutos, oferecendo um snapshot do Hub.
   *(2026-05-02)*

643. A demanda de capturas no multiporta curador depende de aprovação do Gustavo.
   *(2026-05-03)*

644. O sistema de auditoria diária do Hub é cego para o brain `gus`.
   *(2026-05-03)*

645. O sistema possui um bug que pode resultar na perda de PII caso não haja verificação no output do bot.
   *(2026-05-02)*

646. O estado de migração da Fase 1 do TioGu foi concluído com 163 testes verdes e 12 fixes de auditoria no Claude Chat.
   *(2026-05-03)*

647. A decisão de aposentadoria de Mem0 foi documentada na ADR-001, que precisa ser revisitada após 12/05/2026.
   *(2026-05-04)*

648. As demandas paradas são: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, e `_frontmatter-referencia.md` (esse é um template, não é demanda).
   *(2026-05-04)*

649. A captura em tempo real do Chat agora escreve para o Hub via ferramenta `ingestar_fragmento`; cai de volta para upload curado de `.md` para sessões longas. O cérebro `gus` (autorreflexão do agente) é ativamente populado.
   *(2026-05-04)*

650. A arquitetura de memória do Gus foi migrada do Mem0 para o Qdrant Hub.
   *(2026-05-03)*

651. Todos os logs devem ser verificados para evitar vazamento de informações sensíveis.
   *(2026-05-03)*

652. A seção 'Personalidade do Gus (somente Telegram)' deve ser migrada para 'gus/system_prompt.md'.
   *(2026-05-03)*

653. O status atual do Phronesis-Bench é que o projeto está publicado e em revisão no Alignment Forum.
   *(2026-05-04)*

654. A mudança de `drop_pending_updates` de True para False pode causar storm de mensagens em caso de downtime.
   *(2026-05-02)*

655. As demandas paradas são: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, e `_frontmatter-referencia.md`.
   *(2026-05-04)*

656. 6 demandas pendentes no inbox-claude-code, algumas com nome quebrado (provavelmente lixo de sync).
   *(2026-05-03)*

657. O sistema MCP está público, permitindo que qualquer scanner que descubra a URL Railway leia todo o Hub.
   *(2026-05-03)*

658. O procedimento de migração ADR-001 está em curso, visando aposentar a Mem0 SaaS.
   *(2026-05-03)*

659. Fase 3.1 do planejamento é a primeira execução do workflow `migrar-gus-para-hub.yml` em modo dry-run.
   *(2026-05-03)*

660. A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida.
   *(2026-05-02)*

661. Gustavo é anestesiologista e não programa.
   *(2026-05-03)*

662. O arquivo gus-estado-atual.md da pasta projetos/gus está desatualizado, datando de 27/04.
   *(2026-05-03)*

663. O valor do MCP_URL_SECRET deve ser regenerado para garantir a segurança do sistema.
   *(2026-05-03)*

664. Claude Chat opera através de uma memória e para inicialização lê arquivos no bootstrap.
   *(2026-05-04)*

665. Reality check: a coleção legada `gus` deve ser removida para evitar fallback e garantir a integridade dos dados.
   *(2026-05-03)*

666. O sistema de agente pessoal multi-porta está em funcionamento.
   *(2026-05-03)*

667. O Hub deve utilizar URL secrets para aumentar a segurança.
   *(2026-05-02)*

668. Curador bidirecional cron em desenvolvimento e precisa ser finalizado até 12/05/2026.
   *(2026-05-03)*

669. O `_estado-atual.md` (27/04) está bem desatualizado.
   *(2026-05-02)*

670. As pendências do Gustavo incluem configurar 'MCP_URL_SECRET' no Railway e recadastrar o Connector claude.ai.
   *(2026-05-03)*

671. O pipeline de upload do Chat tem problemas de confiabilidade, incluindo falta de retry em chamadas de rede.
   *(2026-05-03)*

672. O resultado da auditoria mostra que a stack está em estado intermediário arriscado devido a cross-brain pollution.
   *(2026-05-03)*

673. A migração ADR-001 do sistema envolve a aposentadoria do Mem0 SaaS.
   *(2026-05-03)*

674. O upgrade do SDK Anthropic altera a versão de 0.40 para >=0.50.
   *(2026-05-04)*

675. O PR #67 introduziu um curador bidirecional no Chat, utilizando Sonnet 4.6 e GPT-4o.
   *(2026-05-02)*

676. A auditoria do Chat abrange tudo que envolve a porta Claude Chat, incluindo a entrada e saída do sistema.
   *(2026-05-03)*

677. O serviço gus-mcp-server deve ter a variável MCP_URL_SECRET guardada para funcionamento correto.
   *(2026-05-03)*

678. Recentemente, houve a correção de um bug crítico do curador que causava falha na função format().
   *(2026-05-03)*

679. A migração de Mem0 SaaS para Hub Qdrant está em andamento e deve ser concluída até 12/05/2026.
   *(2026-05-03)*

680. A porta do Claude Chat lê dados via Drive utilizando project knowledge e não mantém informações atualizadas do sistema Gus.
   *(2026-05-03)*

681. O caderno de demandas da semana está em `dialogos/streams/semana-2026-04-21.md`.
   *(2026-05-04)*

682. Gustavo Pratti de Barros é anestesiologista e não programa.
   *(2026-05-03)*

683. O prompt do bot tem 794 linhas, o que dificulta a manutenção e apresenta riscos de drift.
   *(2026-05-02)*

684. A proposta de otimização incluiu 3 opções: reordenar o bootstrap, criar arquivos lazy, ou um bootstrap minimal com o conhecimento do projeto.
   *(2026-05-03)*

685. O curador híbrido utiliza Haiku e GPT-4o-mini em paralelo.
   *(2026-05-03)*

686. O Gus é um sistema de agente pessoal multi-porta que usa a memória central no Hub Qdrant.
   *(2026-05-03)*

687. O projeto Gus é um sistema de agente pessoal multi-porta.
   *(2026-05-03)*

688. Gustavo está na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

689. A arquitetura de memória persistente foi migrada do Mem0 para o Hub Qdrant.
   *(2026-05-04)*

690. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

691. A coleta dual de modelos no curador terminou em 12/05/2026, e depois Gustavo escolherá o modelo definitivo.
   *(2026-05-03)*

692. Sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa).
   *(2026-05-03)*

693. Atualmente, existem 6 demandas pendentes na porta 'inbox-claude-code'.
   *(2026-05-03)*

694. A refatoração do arquivo bot.py resultou na divisão do código em arquivos menores, seguindo o princípio da responsabilidade única.
   *(2026-05-04)*

695. A demanda #3 é guarda-chuva e referencia as demandas #1 e #2 dentro dela.
   *(2026-05-03)*

696. Quando o curador híbrido falha, entrar com resumo cru pode ser pior do que simplesmente registrar erro + perder a janela.
   *(2026-05-03)*

697. Os principais projetos ativos incluem Phronesis-Bench, NeuroGus, MGE/MGX, TER, e Axon.
   *(2026-05-04)*

698. A migração do gerador de resumos 'Mem0 SaaS' para o 'hub' está em andamento e exige uma limpeza ativa do Hub após a auditoria.
   *(2026-05-03)*

699. O Hub está em estado intermediário arriscado, pois tem 204 fragmentos não-migrados.
   *(2026-05-03)*

700. A auditoria diária (`auditoria_hub.py`) é cega para o brain `gus` e classifica por keywords ignorando a área que o curador já preencheu.
   *(2026-05-03)*

701. Gustavo valoriza a comunicação direta e informal, e busca propor ações com a frase 'quer que eu faça X?'.
   *(2026-05-04)*

702. Componente da Etapa 4 (gus-22) está estruturalmente quebrado.
   *(2026-05-03)*

703. Gustavo é anestesiologista e não programa. Toda implementação passa por Gus/Tiogu.
   *(2026-05-03)*

704. A triagem e auditoria se faz necessário para evitar a poluição cruzada de informações entre os brains.
   *(2026-05-03)*

705. A auditoria diária é cega para o brain gus e classifica por keywords, ignorando o area que o curador já preencheu.
   *(2026-05-03)*

706. A estrutura proposta para dialogos/Gustavo/ será: Chat, Code e TioGu.
   *(2026-05-03)*

707. Os últimos commits têm mostrado bastante coisa nova: PR #67 (curador-chat bidirecional + GPT-4o), PR #64 (captura transcripts Code via cron), PR #60 (MCP URL secret), PR #70 (demanda consolidada).
   *(2026-05-04)*

708. Os 4 documentos principais que dão 80% do contexto para qualquer aba nova são: 'gus-bootstrap.md', 'gus-identity.md', 'gus-estado-atual.md' e 'estado-atual.md'.
   *(2026-05-03)*

709. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026, depois Gustavo escolhe o modelo definitivo.
   *(2026-05-03)*

710. Gustavo Pratti de Barros é anestesiologista baseado no Rio de Janeiro, atuando na Dimagem, uma clínica de imagem diagnóstica com três unidades: Nova Iguaçu, Taquara e São Gonçalo. Além do trabalho clínico, é um pesquisador independente ativo em inteligência artificial e construção de sistemas, operando em múltiplos projetos de pesquisa e produto simultaneamente.
   *(2026-05-03)*

711. A ferramenta automática de captura do Chat deve chamar o `ingestar_fragmento` quando necessário.
   *(2026-05-03)*

712. Gustavo tem um projeto em andamento que envolve auditoria em várias superfícies do Claude Chat.
   *(2026-05-03)*

713. A estrutura do projeto Gus abrange as pastas 'dialogos/', 'projetos/gus/', 'pessoal/', 'dimagem/', entre outras, com sincronização via WIF.
   *(2026-05-03)*

714. Existem 204 fragmentos não migrados na coleção legada gus do Mem0, que faz fallback em leitura.
   *(2026-05-03)*

715. Tem 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-04)*

716. O Hub Qdrant é a memória central do sistema Gus e armazena informações sobre o Gustavo e o Gus.
   *(2026-05-03)*

717. O sistema Gus — agente pessoal multi-porta — está em produção, com quatro portas ativas: Telegram, Claude Code, Claude Chat e Custom GPT em configuração.
   *(2026-05-04)*

718. O Drive sync está parado e a demanda '2026-05-01-drive-sync-oauth-fix.md' está ativa. A hipótese é que o refresh token OAuth expirou.
   *(2026-05-02)*

719. Existem 3 demandas paradas em `dialogos/inbox-claude-code/` no projeto.
   *(2026-05-02)*

720. O Handoff auto-gerado pelo cron 03h é um snapshot do Hub.
   *(2026-05-03)*

721. Os projetos ativos incluem Phronesis-Bench (publicação), NeuroGus (visualização do Hub), MGE/MGX, TER e Axon.
   *(2026-05-04)*

722. O projeto Gus é um sistema de agente pessoal multi-porta, com memória central no Hub Qdrant e arquivos .md no GitHub.
   *(2026-05-03)*

723. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) terminará em 12/05/2026.
   *(2026-05-03)*

724. A demanda 2026-05-01-captura-multiporta-curador.md está parcialmente resolvida pelo PR #67.
   *(2026-05-02)*

725. O processo de migração tem várias fases, e a coleta dual de modelos no curador é para diversificação.
   *(2026-05-03)*

726. O curador de memórias tem a permissão para deletar fragmentos considerados lixo.
   *(2026-05-03)*

727. A captura em tempo real durante a conversa pode ser ativada para aumentar a interação e responsividade do Chat.
   *(2026-05-02)*

728. O bootstrap atual carrega muita informação que é 'uso eventual', ocupando contexto sem ser utilizado.
   *(2026-05-03)*

729. Aposentadoria do Mem0 SaaS planejada após 12/05/2026, quando termina coleta dual A/B Anthropic Haiku × OpenAI GPT-4o-mini do curador.
   *(2026-05-03)*

730. O Hub Qdrant é a nova fonte da verdade e a coleção legada `gus` tem ~204 fragmentos não migrados.
   *(2026-05-03)*

731. A stack de memória está em estado intermediário arriscado, com múltiplas produções de fragmentos e sem mecanismo de deduplicação.
   *(2026-05-03)*

732. O plano de ação está dividido em fases e inclui a limpeza do Hub e a auditoria registrada em A4.
   *(2026-05-03)*

733. As demandas pendentes no inbox são: ativar `MCP_URL_SECRET` no Railway, recadastrar o Connector claude.ai, localizar o mock HTML NeuroGus, decisões §11.3-11.5 da NeuroGus, entre outras.
   *(2026-05-04)*

734. 4 memórias poluídas precisam ser deletadas manualmente.
   *(2026-05-03)*

735. Ativar `MCP_URL_SECRET` no Railway (Gustavo).
   *(2026-05-03)*

736. O estado da migração ADR-001 está em curso, e a coleta dual de modelos no curador termina em 12/05/2026.
   *(2026-05-03)*

737. O sistema atualmente tem fragmentos que são capturados em diferentes operações, o que pode causar poluição nas memórias.
   *(2026-05-03)*

738. 1. Após merge e deploys recentes, o auto_diagnostico agora tem acesso ao Hub Qdrant (evolução positiva)
2. Problema identificado: Hub Qdrant mostra 0 fragmentos para user_id=gustavo — curador acessível mas vazio ou fragmentos indexados com user_id incorreto
3. Workflow "Ingest Mem0 from Claude Chat" está falhando pós-merge — precisa investigação
4. Gustavo usa estratégia de rodar auto_diagnostico duas vezes em sequência para detectar mudanças pós-deploy
5. Infraestrutura base saudável: GitHub Token (fine-grained PAT), Anthropic Haiku, Tavily search, volume Railway writable funcionando
   *(2026-04-27)*

739. O Chat se baseia em memória para a inicialização no começo das mensagens.
   *(2026-05-03)*

740. A memória central do Gus está no Hub Qdrant, com arquivos .md no GitHub que são espelhados no Drive.
   *(2026-05-03)*

741. Gustavo Pratti de Barros é anestesiologista e não programa.
   *(2026-05-03)*

742. A validação de tipo/camada/área no curador foi implementada para garantir que os dados inseridos no Hub sigam o vocabulário gus-18.
   *(2026-05-02)*

743. O contrato schema gus-18 está parcialmente implementado.
   *(2026-05-03)*

744. O diário de auditoria está cego para o brain `gus` e classifica por palavras-chave, ignorando a área preenchida pelo curador.
   *(2026-05-03)*

745. A decisão de usar `MCP_URL_SECRET` no Railway foi recomendada para aumentar a segurança do sistema.
   *(2026-05-03)*

746. O arquivo `gus-protocolo-demanda.md` deve conter informações sobre quando criar uma demanda assíncrona para outra porta, estrutura do caminho, frontmatter obrigatório e validações automáticas.
   *(2026-05-04)*

747. O Hub Qdrant é a memória central do Gus, armazenando arquivos .md no GitHub e espelhando-os no Drive.
   *(2026-05-03)*

748. As frentes mais ativas incluem o PR #67 (curador chat bidirecional + GPT-4o), PR #64 (captura transcripts Code via cron), PR #60 (MCP URL secret) e PR #70 (demanda consolidada).
   *(2026-05-02)*

749. Aba nova só precisa olhar PRs se: você falar 'tá quebrando X depois do PR #YY' → aí sim, lê o PR.
   *(2026-05-03)*

750. Gustavo Pratti de Barros é um anestesiologista baseado no Rio de Janeiro, trabalhando na Dimagem (clínica de imagem diagnóstica, três unidades: Nova Iguaçu, Taquara, São Gonçalo). Juntamente com o trabalho clínico, ele é um pesquisador independente ativo em IA e construtor de sistemas, operando em múltiplos projetos de pesquisa e produto simultaneamente.
   *(2026-05-04)*

751. A coleta de dados é feita de forma bidirecional entre o Gustavo e o Gus.
   *(2026-05-03)*

752. Os fragmentos criados antes da migração e depois da fase 3 vão existir só na coleção antiga, fora do Hub novo.
   *(2026-05-03)*

753. Hub Qdrant está na fase 4 da migração de memória, com a coleta dual Haiku e Sonnet rodando até 12/05, com uma decisão a ser tomada sobre o modelo curador final.
   *(2026-05-03)*

754. O script `migrar_gus_para_hub.py` indicou que não há fragmentos a serem migrados, retornando 0 fragmentos com conteúdo.
   *(2026-05-03)*

755. Foi gerado um teste de regressão para garantir o correto funcionamento do campo 'usage' após o upgrade da SDK.
   *(2026-05-04)*

756. O Hub contém 19 fragmentos no brain `gustavo` e está ocioso nas últimas 6h.
   *(2026-05-03)*

757. A Fase 1 refinada do projeto tem 9 itens e requer aproximadamente 7-8 horas de trabalho.
   *(2026-05-03)*

758. A demanda 2026-05-01-drive-sync-oauth-fix.md está ativa.
   *(2026-05-02)*

759. A estrutura da memória é baseada no Hub Qdrant, agora com mais de 1076 fragmentos em dois brains (gustavo para informações sobre ele e gus para auto reflexão do agente).
   *(2026-05-03)*

760. A arquitetura do bot é baseada em python-telegram-bot e FastAPI, rodando em Railway.
   *(2026-05-03)*

761. O core obrigatório inclui arquivos de bootstrap e estado atual.
   *(2026-05-02)*

762. No processo de calibração da memória do Claude, é importante atualizar informações desatualizadas referindo a Mem0 e incluir as funcionalidades recentes do Hub Qdrant.
   *(2026-05-04)*

763. O arquivo gus-identity.md não é a fonte única de verdade, já que o bootstrap e o system_prompt contém informações complementares.
   *(2026-05-03)*

764. Gus está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

765. Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

766. Sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) com Hub Qdrant como memória central.
   *(2026-05-02)*

767. Existem referências a 'gus-identity.md' em outros arquivos que precisam ser atualizadas.
   *(2026-05-03)*

768. A aba nova só precisa olhar PRs se você falar 'tá quebrando X depois do PR #YY'.
   *(2026-05-03)*

769. O bot utiliza um mecanismo de prompt caching que reduz o custo de input em até 70% nas chamadas para os modelos.
   *(2026-05-02)*

770. A coleta dual de modelos no curador termina em 12/05/2026 e Gustavo escolhe modelo definitivo depois.
   *(2026-05-03)*

771. O bootstrap carrega muita informação que é de uso eventual, ocupando contexto sem ser utilizada com frequência.
   *(2026-05-04)*

772. Em volume crescente, brain gus vira cópia ruidosa do brain gustavo.
   *(2026-05-03)*

773. O Gus é um sistema de agente pessoal multi-porta com memória central no Hub Qdrant, onde arquivos .md são armazenados no GitHub.
   *(2026-05-03)*

774. O sistema Gus é um agente pessoal multi-porta que opera em um Hub Qdrant.
   *(2026-05-04)*

775. O novo segredo deve ser gerado como o anterior, suprimindo a necessidade do histórico anterior.
   *(2026-05-03)*

776. O workflow de auditoria diária do Hub Qdrant é importante para a manutenção da integridade dos dados.
   *(2026-05-03)*

777. Gus é um sistema de agente pessoal multi-porta que integra diversas funcionalidades e memória centralizada no Hub Qdrant.
   *(2026-05-03)*

778. O Gus é um sistema de agente pessoal multi-porta conectado a diversas plataformas.
   *(2026-05-03)*

779. As auditorias diárias do Hub Qdrant não consideram as memórias legadas do Gus.
   *(2026-05-03)*

780. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

781. Os arquivos com as demandas pendentes são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template `_frontmatter-referencia.md`.
   *(2026-05-03)*

782. O bot Telegram, chamado TioGu, utiliza um sistema multi-porta com Hub Qdrant como memória central, onde o Gustavo não programa e a IA implementa.
   *(2026-05-02)*

783. Apenas fragmentos criados antes da migração e depois da Fase 3 vão existir só na coleção antiga, fora do Hub novo.
   *(2026-05-03)*

784. O sistema usa Claude, ChatGPT, Kai e Gemini.
   *(2026-05-03)*

785. Os stakeholders do Gus (Gustavo e Gus) devem decidir sobre qual modelo de agente será utilizado após a migração.
   *(2026-05-03)*

786. As 4 principais fontes de contexto obrigatórias para novos projetos são: o manual operacional do Gus, informações sobre a identidade do Gustavo, o estado atual do Hub e onde parou na sessão anterior.
   *(2026-05-03)*

787. Após configurar o MCP_URL_SECRET no Railway, é necessário recadastrar o Connector no claude.ai para que funcione com o novo URL.
   *(2026-05-03)*

788. A integração do sistema é feita pelo MCP Gus-hub, que conecta as diversas portas disponíveis.
   *(2026-05-03)*

789. O segredo é regenerado gerando dois UUIDs e concatenando-os.
   *(2026-05-03)*

790. Os arquivos de projeto são espelhados no Drive, com a memória central no Hub Qdrant.
   *(2026-05-03)*

791. O sistema contém 21 tools que são utilizados por meio do dispatch por nome.
   *(2026-05-02)*

792. O MCP está público, o que significa que qualquer scanner pode ler todo o Hub.
   *(2026-05-03)*

793. O ADR-001 está em curso para migrar para o Hub Qdrant como fonte da verdade.
   *(2026-05-03)*

794. O bot opera com dependências como python-telegram-bot, anthropic SDK, openai, FastAPI e Qdrant.
   *(2026-05-03)*

795. O sistema Gus utiliza Hub Qdrant como fonte única de memória, aposentando o sistema Mem0.
   *(2026-05-04)*

796. A transformação proposta visa reduzir o total de tokens do bootstrap e otimizar a leitura pelo chat.
   *(2026-05-03)*

797. Temos três produções simultâneas de fragmentos (Telegram, Chat, Code) com 4× multiplicação de chamadas LLM por unidade de input.
   *(2026-05-03)*

798. Os arquivos com as demandas pendentes são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao.
   *(2026-05-03)*

799. Quatro demandas pendentes foram identificadas no `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

800. A Fase 1 do projeto contempla 9 itens de quick wins.
   *(2026-05-03)*

801. O Hub Qdrant é a fonte da verdade, enquanto arquivos .md estão armazenados no GitHub.
   *(2026-05-03)*

802. Estou na branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

803. Próximas ações envolvem um foco específico orientado a processos nos fronts ativos listados por Gustavo.
   *(2026-05-03)*

804. Gustavo está trabalhando na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

805. Gustavo tem hipertireoidismo em tratamento.
   *(2026-05-03)*

806. Existem três demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, e `_frontmatter-referencia.md` (esse é template, não é demanda).
   *(2026-05-03)*

807. A leitura de PRs deve ser feita apenas se necessário para investigar bugs ou entender decisões que não estão documentadas.
   *(2026-05-02)*

808. O Hub Qdrant atual é a fonte da verdade, substituindo a coleção legada de fragmentos do Mem0 SaaS.
   *(2026-05-03)*

809. O hook do retro-engine registra 'no-op: anthropic_missing' e continua a execução normalmente, seguindo o fluxo padrão.
   *(2026-05-02)*

810. A necessidade de curadoria no Chat está se intensificando devido às falhas recorrentes que estão sendo observadas e exigem resposta em um painel de controle.
   *(2026-05-04)*

811. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

812. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

813. A leitura dos últimos arquivos da pasta dialogos/streams/ é importante para entender a demanda da semana.
   *(2026-05-02)*

814. O Connectors precisa ser recadastrado no claude.ai com o novo segredo gerado.
   *(2026-05-03)*

815. Decisões arquiteturais → ADR (gus-15 é exemplo).
   *(2026-05-03)*

816. O sistema "Gus" — agente pessoal multi-porta — está em produção. Quatro portas ativas: Telegram (@Tiogubot), Claude Code, Claude Chat (com Connector MCP gus-hub) e Custom GPT em configuração; Alexa planejada como porta futura.
   *(2026-05-03)*

817. A demanda `2026-05-01-captura-multiporta-curador.md` precisa de um gatilho proativo no Chat.
   *(2026-05-03)*

818. A migração de OAuth user para Workload Identity Federation com Service Account foi realizada para maior segurança no acesso ao Drive.
   *(2026-05-04)*

819. O bot utiliza um sistema de fallback que permite ação imediata em caso de falhas no serviço principal.
   *(2026-05-04)*

820. A arquitetura de memória do sistema Gus foi migrada para o Hub Qdrant em 2026 a partir do Mem0.
   *(2026-05-04)*

821. A coleção legada `gus` está vazia, e os anúncios sobre 204 fragmentos não existem.
   *(2026-05-03)*

822. A stack está em estado intermediário arriscado: Hub Qdrant (`gus_hub`) é a fonte nova, mas a coleção legada `gus` (Mem0 self-hosted) tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

823. O arquivo de log do retro-engine gerou uma mensagem de erro 'anthropic_missing'.
   *(2026-05-02)*

824. O arquivo gus-identity.md contém drift factual com duas linhas erradas sobre o estado atual do sistema.
   *(2026-05-04)*

825. O estado da migração ADR-001 está em curso e a coleta dual de modelos no curador funciona até 12/05/2026.
   *(2026-05-03)*

826. O curador Telegram registra erro 400 recorrente, e o estado das execuções mostra apenas uma entrada por dia, sempre resultando em erro.
   *(2026-05-03)*

827. Gerar novo MCP_URL_SECRET vírgula Railway → gus-mcp-server → Variables → edita pro novo valor.
   *(2026-05-03)*

828. O estado atual do trabalho pode ser consultado no Hub via `ego_cache_atual` ou `fragmentos_recentes`, ou pelo arquivo `gus-estado-atual.md` que é atualizado pelo cron a cada 15 minutos.
   *(2026-05-04)*

829. A seção 'Personalidade do Gus (somente Telegram)' deve ser removida do arquivo `gus-identity.md` e transferida para `gus/system_prompt.md`.
   *(2026-05-04)*

830. O projeto possui demandas pendentes que precisam ser resolvidas através de um sistema de priorização.
   *(2026-05-03)*

831. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

832. O estado final dos PRs já está no código e nos documentos atualizados.
   *(2026-05-04)*

833. O estado atual do projeto é a migração ADR-001 em curso, aposentar Mem0 SaaS e a coleta dual de modelos.
   *(2026-05-03)*

834. O último estado do Hub está fresco a cada 15 minutos devido ao cron.
   *(2026-05-03)*

835. O Hub ainda faz fallback para a coleção legada Mem0, que foi confirmada como vazia durante a migração.
   *(2026-05-03)*

836. Os testes estão passando e cobrem uma parte significativa do código do TioGu, garantindo que mudanças não quebrem funcionalidades existentes.
   *(2026-05-03)*

837. A capacidade atual do Hub Qdrant é de armazenar os dados do agente Gus, mas ainda existem fragmentos herdados da coleção Mem0.
   *(2026-05-03)*

838. O schema gus-18 está parcialmente implementado: o lifecycle é declarado mas não executado.
   *(2026-05-03)*

839. A demanda de Drive sync (`2026-05-01-drive-sync-oauth-fix.md`) está ativa. Hipótese: refresh token OAuth expirou. Três opções: reset OAuth (paliativo) / Service Account (definitivo) / aposentar Drive sync (radical).
   *(2026-05-02)*

840. O sistema do Gus tem controle de acesso, bloqueando escrita se a autenticação não for válida.
   *(2026-05-02)*

841. Recentemente, houve correções críticas implementadas, incluindo um erro que causava falhas de 100% no curador.
   *(2026-05-03)*

842. Estou aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/` (algumas com nome quebrado — 'Documento sem título.md' provavelmente é lixo de sync).
   *(2026-05-03)*

843. A leitura de  `gus-estado-atual.md` é um snapshot do Hub gerado automaticamente às 03h.
   *(2026-05-03)*

844. Atributos de fragmentos não estão sendo atualizados corretamente no sistema.
   *(2026-05-03)*

845. Após a fusão, aguardar o redeploy no Railway é essencial.
   *(2026-05-03)*

846. "Documento sem título.md" provavelmente é lixo de sync.
   *(2026-05-03)*

847. A coletiva legado `gus` tem cerca de 204 fragmentos não-migrados.
   *(2026-05-03)*

848. As informações no arquivo gus-identity.md não são mais a única fonte de verdade sobre Gus e Gustavo, pois o arquivo gus-bootstrap.md é mais completo e atualizado.
   *(2026-05-03)*

849. O sistema Gus é um agente pessoal multi-porta que inclui Telegram, Claude Code, Claude Chat com MCP Connector, Custom GPT e Alexa planejada.
   *(2026-05-03)*

850. A stack de memória está em estado intermediário arriscado: Hub Qdrant é a fonte nova, mas a coleção legada tem ~204 fragmentos não-migrados e o código de leitura faz fallback pra ela.
   *(2026-05-03)*

851. Quando Chat carrega os arquivos, ele deve evitar redundâncias e manter um único ponto de verdade para cada pedaço de informação.
   *(2026-05-03)*

852. Propus que o bootstrap seja dividido em um arquivo mínimo essencial e outros arquivos complementares que serão carregados sob demanda.
   *(2026-05-04)*

853. O secret MEM0_API_KEY ainda existe no Railway?
   *(2026-05-03)*

854. Gustavo é anestesiologista e não programa. Toda implementação passa pelo Gus/Tiogu.
   *(2026-05-03)*

855. Hub Qdrant é a nova fonte da verdade na migração.
   *(2026-05-03)*

856. A auditoria do Chat concluiu que o MCP server precisa de um `MCP_URL_SECRET` para segurança.
   *(2026-05-03)*

857. Há um esforço contínuo para manter o sistema Gus atualizado, organizado e funcional.
   *(2026-05-02)*

858. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md` e `_frontmatter-referencia.md`.
   *(2026-05-02)*

859. O caminho para o MCP agora deve incluir o URL secret gerado, que só deve ser usado com autenticação correta.
   *(2026-05-03)*

860. O arquivo `_estado-atual.md` foi gerado pelo cron às 03h e é um snapshot do Hub.
   *(2026-05-02)*

861. Gustavo trabalha em uma arquitetura de assistente AGI pessoal integrando MemPalace, Mem0, CLAUDE.md orquestrador, e bot Telegram.
   *(2026-05-03)*

862. O Drive sync entre GitHub e Drive parece estar quebrado desde 01/05/2026.
   *(2026-05-03)*

863. A stack de memória end-to-end está em estado intermediário arriscado.
   *(2026-05-03)*

864. O pipeline de upload-from-Chat não tem retry; sem a configuração correta, uma falha de rede pode resultar em um arquivo perdido.
   *(2026-05-03)*

865. O `_estado-atual.md` (27/04) está desatualizado e não reflete PRs #57, #60, #63, #64, #67.
   *(2026-05-02)*

866. A fase de migração do Hub Qdrant é a fonte da verdade para as informações do Gus.
   *(2026-05-03)*

867. O arquivo `limpeza_hub_dryrun.py` gera relatório com lista de candidatos a deletar no Hub.
   *(2026-05-03)*

868. O fragmento salvo tem o UUID '42aea182-d4a2-4626-8a85-5ede861b311b'.
   *(2026-05-04)*

869. Gus é um sistema de agente pessoal multi-porta, com memória central no Hub Qdrant, espelhada no GitHub e Drive.
   *(2026-05-03)*

870. O Hub Qdrant é a nova fonte da verdade e a migração deve ser completada até 12 de maio de 2026.
   *(2026-05-03)*

871. O MCP está público, permitindo que qualquer scanner descubra a URL Railway e leia todo o Hub.
   *(2026-05-03)*

872. Para habilitar a captura proativa durante a conversa, quatro decisões precisam ser feitas sobre a frequência, tipos cobertos, coexistência dos métodos de captura e atualização de seção obsoleta.
   *(2026-05-03)*

873. O estado final dos PRs já está no código e nos docs gus-XX atualizados.
   *(2026-05-03)*

874. Os testes realizados até o momento atingiram 163 testes verdes, cobrindo diversas partes críticas do sistema, incluindo o LLM dispatch e a memória.
   *(2026-05-02)*

875. O estado de migração, denominado ADR-001, está em curso para aposentar o Mem0 SaaS, enquanto o Hub Qdrant se torna a fonte da verdade.
   *(2026-05-03)*

876. Quatro arquivos são considerados core obrigatório para todo novo projeto.
   *(2026-05-04)*

877. A receita de como ler a aba nova e o que não precisa ser lido já foi explicada, incluindo que arquivos do histórico são inutilizados.
   *(2026-05-02)*

878. O status do projeto Phronesis-Bench está em revisão, com a preparação para publicação no Alignment Forum.
   *(2026-05-03)*

879. As decisões arquiteturais são fundamentais ao longo do projeto, como a migração do Mem0 Cloud para o Qdrant.
   *(2026-05-03)*

880. Gustavo está atualmente focado na produção do sistema 'Gus', um agente pessoal multiporta com várias integrações.
   *(2026-05-03)*

881. Existem três opções para resolver o problema do Drive sync: resetar OAuth, usar Service Account ou aposentar o Drive sync.
   *(2026-05-03)*

882. Sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa).
   *(2026-05-03)*

883. O projeto tem 4 demandas pendentes no dialogos/inbox-claude-code.
   *(2026-05-03)*

884. O lifecycle do schema gus-18 está declarado mas não executado: não há job/cron de promoção `ativo → estavel`.
   *(2026-05-03)*

885. Sonnet 4.6 é superior para Vision e PDFs nativos, mas OpenAI é mais barato e mais adequado para texto puro.
   *(2026-05-04)*

886. Existem 4 demandas pendentes no dialogos/inbox-claude-code.
   *(2026-05-03)*

887. Os comandos disponíveis para preferir ao usar arquivos incluem `ego_cache_atual()` e `fragmentos_recentes(horas=24)`.
   *(2026-05-03)*

888. O processo de auditoria na stack de memória revela que o ciclo de fallback em tempo de execução pode causar poluição silenciosa.
   *(2026-05-03)*

889. Gustavo é anestesiologista e não programa, portanto, toda implementação do Gus passa por um agente.
   *(2026-05-03)*

890. Bootstrap lido. Agora vou buscar o estado atual.
   *(2026-05-03)*

891. As demandas pendentes são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao e o `_frontmatter-referencia.md` que é só um template.
   *(2026-05-03)*

892. Desenvolve uma casa em Paty do Alferes.
   *(2026-05-04)*

893. O workflow `export-mem0` precisa ser acionado na branch `main` do repositório.
   *(2026-05-03)*

894. As 18 entradas que entraram em modo fallback-mem0 em 28/04 não estão visíveis na coleção gus.
   *(2026-05-03)*

895. O estado atual de migração é o ADR-001 em curso, aposentando o Mem0 SaaS, sendo o Hub Qdrant a fonte da verdade.
   *(2026-05-03)*

896. O plano final para a migração inclui 6 fases, com previsão de conclusão em 24/05.
   *(2026-05-03)*

897. A coleção legada `gus` no Qdrant ainda está viva, fazendo fallback para a Mem0 ativa.
   *(2026-05-03)*

898. O Chat só salva quando você pede. Não detecta automaticamente fatos ou decisões importantes.
   *(2026-05-03)*

899. O sistema de captura está em estado intermediário arriscado, exigindo deduplicação e limpeza do Hub atual.
   *(2026-05-03)*

900. PDFs não terão fallback para OpenAI, e o bot retornará uma mensagem amigável quando Anthropic falhar ao processar PDF.
   *(2026-05-03)*

901. A migração do sistema de Mem0 SaaS para Hub Qdrant será finalizada até 12/05/2026.
   *(2026-05-03)*

902. Gustavo Pratti de Barros é anestesiologista.
   *(2026-05-03)*

903. O Hub é responsável por integrar e processar as informações entre as ferramentas e o agente.
   *(2026-05-02)*

904. Anotificações automáticas do TioGu devem continuar funcionais.
   *(2026-05-03)*

905. A migração para o Hub Qdrant está definida na decisão arquitetural ADR-001, que busca aposentar o Mem0 SaaS.
   *(2026-05-03)*

906. Os 4 itens pendentes são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template de referência.
   *(2026-05-03)*

907. Das 421 linhas do bootstrap, aproximadamente 120 são protocolos que o Chat usa apenas ocasionalmente, ocupando espaço sem ser necessário.
   *(2026-05-04)*

908. Os testes em `tests/test_curador.py` agora cobrem a validação de erros do curador.
   *(2026-05-02)*

909. O sistema deve dizer que usa Hub Qdrant e não Mem0 ao ser ativado.
   *(2026-05-04)*

910. O Gus é um sistema de agente pessoal multi-porta que integra diferentes plataformas como Telegram/TioGu, Claude Code e Claude Chat.
   *(2026-05-03)*

911. Gustavo é anestesiologista, não programa — toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

912. A coleta dual de modelos no curador (Haiku × GPT-4) e o levantamento de dados devem ser feitos com cuidado para evitar redundâncias.
   *(2026-05-03)*

913. A nova configuração do bot inclui a geração de alertas de custo, garantindo que os gastos sejam monitorados efetivamente.
   *(2026-05-04)*

914. A função `ingestar_fragmento` aceita um parâmetro `user_id` que poderia ser mal utilizado se não houver validação adequada.
   *(2026-05-02)*

915. O bot Telegram (TioGu) possui cerca de 21 tools e está em produção no Railway.
   *(2026-05-02)*

916. O bot Telegram, TioGu, possui ~21 ferramentas distintas integradas.
   *(2026-05-03)*

917. O bot Telegram, chamado TioGu, atua como uma interface para interagir com o Hub Qdrant.
   *(2026-05-04)*

918. O código do projeto está na branch `claude/initial-setup-iWTfL`.
   *(2026-05-02)*

919. Gustavo está desenvolvendo uma casa em Paty do Alferes.
   *(2026-05-03)*

920. A demanda de Drive sync foi resolvida, com a integração end-to-end validada e arquivada, garantindo que documentos importantes sejam sincronizados corretamente.
   *(2026-05-03)*

921. Foram encontrados 204 fragmentos históricos no Mem0 SaaS.
   *(2026-05-03)*

922. A auditoria diária do Hub Qdrant não considera a coleção legada do Gus, o que prejudica a consistência dos dados.
   *(2026-05-03)*

923. Sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) com Hub Qdrant como memória central.
   *(2026-05-02)*

924. O arquivo 'gus-identity.md' contém informações redundantes que devem ser consolidadas.
   *(2026-05-03)*

925. O esquema gus-18 está parcialmente implementado, com lifecycle não executado atualmente.
   *(2026-05-03)*

926. A conta Anthropic está sem créditos.
   *(2026-05-03)*

927. O `MCP_URL_SECRET` ainda não está ativado no Railway.
   *(2026-05-03)*

928. A recomendação é alterar `drop_pending_updates=True` para logging do count de pending e enviar uma mensagem ao Gustavo no boot caso haja pendências.
   *(2026-05-02)*

929. Gustavo tem hipertireoidismo em tratamento.
   *(2026-05-03)*

930. Recomendação é manter o conteúdo em `historico/` e planejar filtragem na Fase 5.
   *(2026-05-03)*

931. A ferramenta de auditoria do hub foi renomeada de `auditoria_mem0()` para `auditoria_hub()`.
   *(2026-05-03)*

932. A aba conta com um novo canal Gus-Sync/dialogos/inbox-gustavo/{chat,code,tiogu}/ no Drive, que auto-injeta frontmatter.
   *(2026-05-03)*

933. Hub Qdrant é a fonte da verdade do Gus, armazenando a memória central.
   *(2026-05-03)*

934. A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida, mas falta o gatilho proativo no Chat.
   *(2026-05-03)*

935. O retro-engine registra 'no-op: anthropic_missing' e segue.
   *(2026-05-03)*

936. A proposta de otimização C é agressiva, com um bootstrap minimal e dependência do project knowledge.
   *(2026-05-03)*

937. A implementação do NeuroGus está 100% planejada e aguarda confirmação dos itens 11.1-11.7 das decisões abertas.
   *(2026-05-02)*

938. As referências a Gus no CLAUDE.md devem ser atualizadas para refletir mudanças na personalidade e funcionalidades.
   *(2026-05-04)*

939. O prazo para a coleta dual de modelos no curador termina em 12/05/2026.
   *(2026-05-03)*

940. Manter a auto-notificação Telegram para a pasta `TioGu/` é uma das opções propostas para a funcionalidade.
   *(2026-05-03)*

941. Estou aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

942. Se Anthropic falha ao processar imagens, o bot deve usar OpenAI Vision como fallback, garantindo que as imagens ainda sejam processadas.
   *(2026-05-03)*

943. O chat diz que gravou, mas quando busco em outra aba, a outra aba não cita os fragmentos e o outro chat diz que colocou.
   *(2026-05-04)*

944. As demandas pendentes foram identificadas como prioritárias para serem resolvidas.
   *(2026-05-02)*

945. O passo 1 é gerar novo MCP_URL_SECRET.
   *(2026-05-03)*

946. O 'HARD_LIMIT' é uma falha silenciosa que impede que o usuário perceba que o bot não está respondendo após atingir o limite.
   *(2026-05-02)*

947. O panorama do projeto Gus está desatualizado e não reflete as últimas atualizações, sendo necessário atualizar o estado atual.
   *(2026-05-04)*

948. A estrutura atual do bootstrap não possui um entry point claro e tem muitas subseções, dificultando a leitura pelo Chat.
   *(2026-05-04)*

949. Claude/ChatGPT-Kai/Gemini são as ferramentas usadas pelo Gus.
   *(2026-05-04)*

950. A migração Mem0 → Hub Qdrant está na Fase 4 (ADR-001).
   *(2026-05-03)*

951. Decisão migração ADR-001 em curso: aposentar Mem0 SaaS, Hub Qdrant é a fonte da verdade.
   *(2026-05-03)*

952. A pasta 'Gus-Sync/dialogos/' pode conter uma subpasta 'Gustavo/' com subpastas para Chat, Code e TioGu.
   *(2026-05-03)*

953. A identidade do Gustavo e do Gus enquanto entidade estão documentadas em arquivos dedicados.
   *(2026-05-03)*

954. A convenção de nomenclatura dos arquivos JSON é <paciente_id>__<data_coleta>__<lab_curto>.json.
   *(2026-05-02)*

955. Existem preocupações sobre a carga de arquivos grandes que o Chat pode processar, especialmente o `read_repo_file` sem limite de tokens.
   *(2026-05-04)*

956. O sistema Gus possui três produções simultâneas de fragmentos (Telegram, Chat, Code), o que gera uma multiplicação de chamadas aos LLM por unidade de input.
   *(2026-05-03)*

957. Atualmente, o Hub Qdrant é a fonte da verdade do sistema.
   *(2026-05-03)*

958. A coleta dual de modelos no curador é feita com Haiku e GPT-4o-mini.
   *(2026-05-03)*

959. A captura de múltiplas fontes de fragmentos (Telegram, Chat, Code) aparece no sistema, mas ainda sem deduplicação.
   *(2026-05-03)*

960. Os arquivos que o Chat lê ao ativar o Gus são gus-bootstrap.md e gus-estado-atual.md.
   *(2026-05-04)*

961. O secreto a ser gerado deve ser atualizado no RailWay e em qualquer referência ao MCP em uso.
   *(2026-05-03)*

962. Após gerar o segredo, o usuário deve setá-lo no Railway como variável MCP_URL_SECRET.
   *(2026-05-03)*

963. Gustavo é anestesiologista e não programa.
   *(2026-05-03)*

964. Gustavo deve realizar uma calibração da memória do Claude, atualizando sobre o sistema Gus e a migração do Mem0 para o Hub Qdrant.
   *(2026-05-04)*

965. A auditoria diária em `auditoria_hub.py` é cega para o brain `gus` e ignora a classificação por area.
   *(2026-05-03)*

966. O arquivo `gus-bootstrap.md` contém informações essenciais que devem ser carregadas sempre que Claude inicia.
   *(2026-05-04)*

967. Agora, para enviar demandas pelo celular, deve-se criar arquivos em `Gus-Sync/dialogos/inbox-gustavo/code/` no Drive.
   *(2026-05-03)*

968. A partir de 27/04/2026, o Hub Qdrant passou a capturar dados ao invés do Mem0 SaaS.
   *(2026-05-03)*

969. A fase de migração para o Hub Qdrant envolve a aposentadoria do Mem0 SaaS.
   *(2026-05-03)*

970. A auditoria do Chat envolve todos os aspectos relacionados ao projeto Claude Chat.
   *(2026-05-03)*

971. A stack de memória está em estado intermediário arriscado: o Hub Qdrant é a fonte nova, mas a coleção legada `gus` (Mem0 self-hosted) tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

972. O sistema principal de Gustavo chamado "Gus" está em produção: um agente pessoal multiportas de IA (Telegram bot @Tiogubot, Claude Code, Claude Chat com conector MCP, Custom GPT em configuração, Alexa planejada). A estrutura de memória foi migrada do Mem0 para o Hub Qdrant direto (ADR-001, concluído em 27/04/2026), agora com mais de 1076 fragmentos em dois cérebros (`gustavo` para fatos sobre ele, `gus` para autorreflexão do agente).
   *(2026-05-04)*

973. O passo 1 é gerar um novo MCP_URL_SECRET e setar no Railway.
   *(2026-05-03)*

974. A publicação do Phronesis-Bench está em revisão e a preparação para o Alignment Forum é uma das prioridades atuais.
   *(2026-05-04)*

975. A amostragem dos 204 fragmentos exportados mostra que existe conteúdo útil, que é superior ao que está no Hub atualmente.
   *(2026-05-03)*

976. Gustavo pode optar por padronizar certas instruções em um arquivo dialogos/_bootstrap/[checklist-boot-aba-nova.md] para deixar a canonização mais clara.
   *(2026-05-03)*

977. O snapshot do Hub registra ocioso há 6h+ na janela fragmentos últimas 6h.
   *(2026-05-02)*

978. Os arquivos parados são: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md` e `_frontmatter-referencia.md`.
   *(2026-05-03)*

979. A auditoria diária do Hub Qdrant é cega para o brain Gus e ignora o campo area.
   *(2026-05-03)*

980. O protocolo de Análise IA de Exames Laboratoriais v1 está localizado em Gus-Sync/protocolos/protocolo-exames-laboratoriais-v1.md.
   *(2026-05-02)*

981. O projeto tem 4 demandas pendentes no dialogos/inbox-claude-code.
   *(2026-05-03)*

982. As demandas pendentes incluem a captura multiporta, curador bidirecional cron, e OAuth para sincronização do Drive.
   *(2026-05-03)*

983. O Handoff auto-gerado pelo cron às 03h é um snapshot do Hub feito diariamente.
   *(2026-05-03)*

984. Foi decidido remover a função `_fallback_mem0` do código para evitar a inserção de lixo no Hub quando o curador falha.
   *(2026-05-03)*

985. O sistema de agente pessoal Gus opera com múltiplas portas, incluindo Telegram, Claude Chat e futura integração com Alexa.
   *(2026-05-03)*

986. A Fase 5 do projeto está programada para remover a memória Mem0 SaaS.
   *(2026-05-03)*

987. O curador do Telegram está com erro recorrente 400, falhando silenciosamente nos últimos 3 dias. Isso pode estar afetando a ingestão do Chat.
   *(2026-05-03)*

988. O Hub Qdrant (`gus_hub`) funciona como memória central para o sistema multi-porta.
   *(2026-05-02)*

989. A última referência a `auditoria_mem0` deve ser trocada para `auditoria_hub` em quatro lugares.
   *(2026-05-03)*

990. A captura de fragmentos real-time está funcionando no Gus, utilizando um pipeline híbrido com duas ferramentas distintas.
   *(2026-05-03)*

991. O arquivo `gus-estado-atual.md` serve como um snapshot do Hub, fornecendo informações sobre onde paramos na sessão anterior.
   *(2026-05-03)*

992. O estado da migração ADR-001 está em curso.
   *(2026-05-03)*

993. A decisão de migração do sistema está documentada em `projetos/gus/[gus-15-decisao-migracao.md]`.
   *(2026-05-03)*

994. Algumas demandas estão com nome quebrado – "Documento sem título.md" provavelmente é lixo de sync.
   *(2026-05-03)*

995. O Gus é um sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa).
   *(2026-05-03)*

996. As instruções incluem que Gustavo deve ser sempre apontado a buscar informações no Hub ou Drive quando necessário.
   *(2026-05-03)*

997. Em 02/05/2026, a auditoria revelou que a coleção legada `gus` está vazia.
   *(2026-05-03)*

998. Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e o `_frontmatter-referencia.md` que é só um template.
   *(2026-05-03)*

999. O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).
   *(2026-05-02)*

1000. A árvore de decisão para o curador inclui etapas para limpeza, promoção e importação de fragmentos novos.
   *(2026-05-03)*

1001. O Hub Qdrant deve receber fragmentos úteis e consolidar as informações do Gus.
   *(2026-05-03)*

1002. A demanda #3 na inbox-claude-code é relativa à consolidação de pendências do Claude Chat.
   *(2026-05-03)*

1003. Os projetos ativos de Gustavo incluem Phronesis-Bench, NeuroGus, MGE, MGX, TER e Axon.
   *(2026-05-04)*

1004. O sistema possui um mecanismo de auditoria diária que classifica fragmentos de memória usando keywords.
   *(2026-05-03)*

1005. A migração do Mem0 SaaS para o Hub Qdrant está em curso até 12/05/2026.
   *(2026-05-03)*

1006. Testes de saúde e de autorização 404 são críticos após a configuração do MCP.
   *(2026-05-03)*

1007. A auditoria diária é cega para o brain gus e ignora o 'area' que o curador preenche.
   *(2026-05-03)*

1008. O arquivo gus-identity.md contém informações desatualizadas sobre o sistema Gus.
   *(2026-05-03)*

1009. O passo 1 do esquema que envolve a proteção do segredo foi seguido e mencionado durante a auditoria.
   *(2026-05-03)*

1010. As demandas pendentes no inbox-claude-code incluem captura-multiporta-curador, drive-sync-oauth-fix, e pendencias-claude-chat-consolidacao.
   *(2026-05-03)*

1011. O estado do projeto é atualizado diariamente pelo cron 03h, criando um snapshot do Hub.
   *(2026-05-03)*

1012. A decisão sobre a utilização do MEM0_API_KEY será tomada após a exportação do conteúdo do Mem0 SaaS.
   *(2026-05-03)*

1013. As demandas pendentes na porta 'inbox-claude-code' incluem captura multiporta, curador bidirecional cron e OAuth para o drive-sync.
   *(2026-05-03)*

1014. O bot Telegram (TioGu) possui ~21 tools, multimídia, prompt caching, em produção Railway.
   *(2026-05-02)*

1015. A demanda de atualização de `MCP_URL_SECRET` no Railway é uma prioridade alta.
   *(2026-05-03)*

1016. O agente Gus utiliza o Qdrant Hub como backend de memória.
   *(2026-05-03)*

1017. Para enviar demandas pelo celular, basta criar um arquivo no Drive em Gus-Sync/dialogos/inbox-gustavo/code/ com texto livre.
   *(2026-05-03)*

1018. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1019. Um novo ambiente virtual `MODEL_OPENAI_VISION_FALLBACK` foi criado com o valor padrão `gpt-4o` para o fallback em caso de falha da Anthropic.
   *(2026-05-03)*

1020. O arquivo gus-estado-atual.md é gerado a cada 15 minutos e traz um snapshot do estado atual do sistema.
   *(2026-05-03)*

1021. Hub Qdrant é a fonte da verdade.
   *(2026-05-03)*

1022. O conteúdo do arquivo gus-identity.md é redundante e misturado com o arquivo gus-bootstrap.md.
   *(2026-05-03)*

1023. O arquivo gus-estado-atual.md é um snapshot auto-gerado do Hub, criado pelo cron a cada 03h.
   *(2026-05-03)*

1024. Existem 6 demandas pendentes no diálogo de inbox-claude-code.
   *(2026-05-03)*

1025. Devem existir arquivos específicos como `gus-protocolo-demanda.md`, `gus-protocolo-drive.md`, e outros focados.
   *(2026-05-03)*

1026. Decisão sobre o modelo de curador final acontecerá mais tarde, após 12/05.
   *(2026-05-03)*

1027. As diretrizes específicas sobre como criar demandas assíncronas para outras portas estão documentadas no arquivo gus-protocolo-demanda.md.
   *(2026-05-03)*

1028. Gustavo está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-02)*

1029. O cron de sincronização no Google Drive parou em 01/05, provavelmente devido à expiração do token de autenticação OAuth.
   *(2026-05-03)*

1030. O modelo de NeuroGus, com pilotagem planejada, aguarda confirmação dos itens 11.1-11.7.
   *(2026-05-02)*

1031. O nome da pasta do Google Drive utilizada pelo sistema mudou e agora se chama 'Gus-Sync', enquanto que `gus-identity.md` menciona 'GitHub-Sync'.
   *(2026-05-03)*

1032. O Hub Qdrant é a fonte da verdade e o Gustavo é anestesiologista, não programa.
   *(2026-05-03)*

1033. O cron `gerar-estado-claude-chat` roda a cada 15min, mesmo quando Hub está ocioso, resultando em muitos jobs diários com commits no-op.
   *(2026-05-03)*

1034. Após a migração para WIF, não é mais necessário decidir entre as opções de Drive sync 1/2/3.
   *(2026-05-03)*

1035. 1. Gustavo quer que o workflow de migração Mem0 → Qdrant rode e que o auto_diagnóstico seja executado após conclusão.

2. Hub Qdrant está operacional com 4+ fragmentos (subiu de 2), migração em progresso para consolidar 204 memórias. Esperado crescimento conforme workflow processa.

3. Site da arquitetura do Gus foi gerado em HTML e está em `dialogos/inbox-claude-chat/` aguardando Gustavo abrir no claude.ai para renderizar como Artifact.

4. Infra confirmada como estável: GitHub Token (fine-grained PAT), Qdrant, Anthropic (Haiku), Tavily, Volume Railway e Workflows GitHub todos operacionais.

5. Gustavo tem capacidade de revisar demandas, priorizar tarefas e tomar decisões sobre fluxo de trabalho conforme feedback do Gus.
   *(2026-04-28)*

1036. O `_estado-atual.md` está desatualizado desde 27/04.
   *(2026-05-03)*

1037. Dimagem clínico: 'Roberto Pereira dos Santos Neto, 69 anos, obeso BMI ~34, RM pélvica + abdominal com sedação'.
   *(2026-05-03)*

1038. Abre app Railway no celular (ou web em https://railway.app).
   *(2026-05-03)*

1039. A demanda caracterizada como 'Pendências Claude Chat consolidadas' inclui assinalar o ativar `MCP_URL_SECRET` no Railway e recadastrar o Connector claude.ai.
   *(2026-05-04)*

1040. As demandas pendentes no 'inbox-claude-code' incluem a captura multiporta do curador e o drive sync OAuth.
   *(2026-05-03)*

1041. Fragmentos criados antes da migração e depois da Fase 3 existirão apenas na coleção antiga, fora do Hub novo.
   *(2026-05-03)*

1042. O sistema 'Gus' realiza captura de dados em tempo real via tool MCP 'ingestar_fragmento'.
   *(2026-05-03)*

1043. O bot do Telegram (TioGu) utiliza a biblioteca python-telegram-bot para funcionar corretamente.
   *(2026-05-04)*

1044. O Hub Qdrant é a memória central do Gus, com a implementação armazenada no GitHub (Gustpbbr/Gus) e espelhada no Drive.
   *(2026-05-03)*

1045. A URL secret protege e destrava também escrita real-time do Chat, através da função ingestar_fragmento.
   *(2026-05-03)*

1046. Gustavo Pratti de Barros é anestesiologista no Dimagem, atuando em 3 unidades, e pesquisador independente em IA.
   *(2026-05-03)*

1047. Um passo necessário é criar o MCP_URL_SECRET no Railway para proteger o acesso ao hub.
   *(2026-05-03)*

1048. O Hub Qdrant é a fonte da verdade do sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa).
   *(2026-05-03)*

1049. As decisões sobre a exclusão de fragmentos devem ser revisadas e aprovadas antes de serem aplicadas no Hub.
   *(2026-05-03)*

1050. O arquivo `gus-identity.md` contém redundâncias com o `gus-bootstrap.md` e está desatualizado.
   *(2026-05-03)*

1051. Estou aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1052. Gus é um sistema de agente pessoal multi-porta, com memória central no Hub Qdrant, integrado via arquivos .md no GitHub.
   *(2026-05-03)*

1053. Há 4 demandas pendentes no `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1054. As demandas pendentes são apresentadas em 'dialogos/inbox-' e devem ser processadas.
   *(2026-05-03)*

1055. A captura de memória do bot utiliza um sistema híbrido que acumula experiências e contextos importantes durante as interações.
   *(2026-05-04)*

1056. O documento 'Prudência Performática' do Phronesis-Bench foi finalizado e está em revisão para o Alignment Forum.
   *(2026-05-04)*

1057. O sistema de agente pessoal utiliza uma memória central no Hub Qdrant, com registros espelhados no Drive.
   *(2026-05-03)*

1058. URL secret protege o MCP e destrava escrita real-time do Chat (ingestar_fragmento).
   *(2026-05-03)*

1059. As demandas pendentes são sobre captura multiporta, curador bidirecional cron e autenticação OAuth para o Drive.
   *(2026-05-03)*

1060. O passo 1 do processo envolve setar `MCP_URL_SECRET` no Railway, para proteger o acesso ao Hub e permitir escrita real-time do Chat.
   *(2026-05-03)*

1061. A seção 'Disciplina anti-esquecimento' no bootstrap foi atualizada para refletir os dois caminhos de captura de memória.
   *(2026-05-03)*

1062. O bot do Telegram, TioGu, possui cerca de 21 ferramentas.
   *(2026-05-03)*

1063. A memória do sistema é atualizada regularmente, com snapshots gerados a cada 15 minutos.
   *(2026-05-04)*

1064. O arquivo `gus-estado-atual.md` é gerado a cada 15 minutos e serve como o único arquivo de boot que muda frequentemente.
   *(2026-05-04)*

1065. O sistema 'Gus' — agente pessoal multi-porta — está em produção, com quatro portas ativas: Telegram (@Tiogubot), Claude Code, Claude Chat e Custom GPT em configuração.
   *(2026-05-03)*

1066. Hub Qdrant é a fonte da verdade. Coleta dual de modelos no curador (Haiku × GPT-4o-mini, mudou de Sonnet em 29/04 por custo/resiliência) termina 12/05/2026.
   *(2026-05-03)*

1067. A stack de memória end-to-end está em estado intermediário arriscado, com três produções simultâneas de fragmentos.
   *(2026-05-03)*

1068. Posso descobrir o caminho `_resumir_e_salvar` em `gus/bot.py`, se ele estiver tentando escrever no Mem0 SaaS via `mem0ai`, vou matar. Se estiver fazendo coisa razoável, ajustamos.
   *(2026-05-03)*

1069. O bot Telegram é uma aplicação que utiliza a biblioteca python-telegram-bot e a API do Anthropic, além do OpenAI para funcionalidades de geração de respostas.
   *(2026-05-04)*

1070. As mudanças no sistema de memória buscam melhorar a qualidade das informações armazenadas e acessadas.
   *(2026-05-03)*

1071. O estado final dos PRs já está no código e nos documentos gus-XX atualizados, e PRs descrevem o caminho, não onde estamos.
   *(2026-05-03)*

1072. Captura proativa do Chat agora é instrução explícita no bootstrap.
   *(2026-05-03)*

1073. O blog teve 204 fragmentos exportados do Mem0 SaaS que foram armazenados em `historico/`.
   *(2026-05-03)*

1074. A porta Claude Chat (claude.ai) serve como interface para interagir com o Hub e o MCP server.
   *(2026-05-03)*

1075. O Phronesis-Bench foi finalizado e está em revisão, com preparação para o Alignment Forum. O futuro do Mem0 como SaaS está planejado para o pós-12/05/2026, após a coleta A/B dual do curador (Anthropic Haiku × OpenAI GPT-4o).
   *(2026-05-04)*

1076. A auditoria do Chat envolve tanto a porta Claude Chat (claude.ai) quanto o sistema operacional que a alimenta.
   *(2026-05-02)*

1077. O Hub Qdrant com curador híbrido coleta dual rola até 12/05.
   *(2026-05-03)*

1078. Estou aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/` (algumas com nome quebrado — "Documento sem título.md provavelmente é lixo de sync).
   *(2026-05-03)*

1079. O TioGu é um bot do Telegram com arquitetura multi-provider, utilizando LLMs da Anthropic e OpenAI em fallback.
   *(2026-05-02)*

1080. O fallback do 'gus' ainda está ativo, o que expõe o sistema a inconsistências e dados antigos.
   *(2026-05-03)*

1081. A personalidade do Gus deve ser consolidada no arquivo gus/system_prompt.md.
   *(2026-05-03)*

1082. O Hub tem 19 fragmentos no brain `gustavo`, com sistema ocioso nas últimas 6h.
   *(2026-05-03)*

1083. O estado final dos PRs já está no código e nos documentos atualizados.
   *(2026-05-03)*

1084. O bug no curador causou divergência Haiku × GPT entre 29/04 a 02/05.
   *(2026-05-03)*

1085. Sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa).
   *(2026-05-03)*

1086. A auditoria do Chat teve a conclusão de que o boot atual carrega muita informação que não é utilizada na maioria das conversas.
   *(2026-05-03)*

1087. Os documentos `dialogos/_bootstrap/gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md` e `projetos/gus/estado-atual.md` são essenciais para entender o projeto.
   *(2026-05-03)*

1088. O `_estado-atual.md` está desatualizado, com data de 27/04.
   *(2026-05-03)*

1089. O ciclo de vida (lifecycle) dos fragmentos será implementado de acordo com o contrato gus-18.
   *(2026-05-03)*

1090. O Hub Qdrant é a fonte da verdade, enquanto a coleção legada 'gus' ainda estava ativa com fallback para o Mem0 SaaS.
   *(2026-05-03)*

1091. Gustavo é anestesiologista e não programa — toda implementação passa por Gus.
   *(2026-05-03)*

1092. A stack de memória está em estado intermediário arriscado, com a coleção legada `gus` ainda viva e fallback para Mem0 ativo.
   *(2026-05-03)*

1093. A migração para o Hub Qdrant, com base na decisão ADR-001, está programada para ser concluída até 12/05/2026.
   *(2026-05-03)*

1094. O Hub tem 19 fragmentos no brain `gustavo` e o sistema está ocioso nas últimas 6 horas.
   *(2026-05-02)*

1095. O Hub Qdrant é a nova fonte da verdade, com coleta dual de modelos no curador.
   *(2026-05-03)*

1096. Para Gustavo, a captura dual de modelos no curador (Haiku × GPT) termina em 12/05/2026 — depois Gustavo escolhe modelo definitivo.
   *(2026-05-03)*

1097. As demandas pendentes no `dialogos/inbox-claude-code/` são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao e um template.
   *(2026-05-02)*

1098. A `assoc` do fallback Mem0 ainda está em uso no código atual.
   *(2026-05-03)*

1099. A coleção legada `gus` está vazia, com 204 fragmentos prometidos não existentes.
   *(2026-05-03)*

1100. A auditoria identificou a necessidade de integrar uma lógica clara para hierarquizar os canais de escrita do Chat.
   *(2026-05-03)*

1101. O após 12/05/2026, haverá uma decisão entre os modelos Haiku e Sonnet/GPT da coleta dual.
   *(2026-05-04)*

1102. A migração da coleção legada para o hub Qdrant está em andamento.
   *(2026-05-03)*

1103. O Mem0 foi aposentado e a fonte única agora é o Hub Qdrant.
   *(2026-05-03)*

1104. A central de memória do Gus está no Hub Qdrant.
   *(2026-05-03)*

1105. A opção B para otimização do bootstrap resulta em uma redução significativa de tokens e mantém a funcionalidade.
   *(2026-05-03)*

1106. Os arquivos core obrigatórios para qualquer aba nova incluem: dialogos/_bootstrap/gus-bootstrap.md, dialogos/_bootstrap/gus-identity.md, dialogos/_bootstrap/gus-estado-atual.md, e projetos/gus/_estado-atual.md.
   *(2026-05-03)*

1107. Um alerta deve ser configurado para divergências entre Haiku e GPT na captura de dados.
   *(2026-05-03)*

1108. O sistema possui um curador híbrido que permite o uso de Haiku e GPT-4o em paralelo para extração de fragmentos.
   *(2026-05-02)*

1109. O Hub Qdrant armazena dados do Gustavo e do Gus, com 204 fragmentos legados não migrados.
   *(2026-05-03)*

1110. Os 4 arquivos que dão 80% do contexto pra qualquer aba nova são: `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md` e `gus/_estado-atual.md`.
   *(2026-05-03)*

1111. O Mem0 foi aposentado em 27/04/2026, e o Hub Qdrant é a nova fonte de memória do sistema.
   *(2026-05-03)*

1112. Gustavo Pratti de Barros é anestesiologista no Dimagem, com três unidades e pesquisador independente em IA.
   *(2026-05-03)*

1113. Gus está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

1114. A auditoria confirmou a necessidade de melhorar a segurança do sistema, especificamente em relação ao gerenciamento de credenciais.
   *(2026-05-03)*

1115. A coleção legada `gus` está vazia, não há fragmentos a serem migrados.
   *(2026-05-03)*

1116. O workflow do Chat precisa utilizar o arquivo de bootstrap para operar corretamente.
   *(2026-05-03)*

1117. A decisão de mudar a arquitetura do bot para um modelo multi-porta foi baseada na necessidade de integração com diversas plataformas.
   *(2026-05-04)*

1118. O bot Telegram (TioGu) conta com ~21 tools, multimídia, caching de prompts e foi desenvolvido para operar continuamente em Railway.
   *(2026-05-02)*

1119. O status do Hub é atualizado a cada 15min pelo cron.
   *(2026-05-02)*

1120. O plano NeuroGus está 100% pronto.
   *(2026-05-02)*

1121. O bot utiliza o framework python-telegram-bot na versão 21.6, que é recente e adequado para sua operação.
   *(2026-05-02)*

1122. O secret 'MEM0_API_KEY' precisa ser verificado se ainda está ativo no Railway para decidir sobre a migração e potencial recuperação de dados.
   *(2026-05-03)*

1123. O conteúdo do Mem0 SaaS está agora seguro no `historico/`.
   *(2026-05-03)*

1124. A stack de memória end-to-end está em um estado intermediário arriscado: o Hub Qdrant é a nova fonte, mas a coleção legada tem 204 fragmentos não migrados.
   *(2026-05-03)*

1125. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

1126. O `MCP_URL_SECRET` precisa ser setado no Railway para proteger o MCP.
   *(2026-05-03)*

1127. A auditoria diária é cega ao brain `gus`, registrando apenas fragmentos do brain `gustavo`. Isso impacta a qualidade da curadoria.
   *(2026-05-03)*

1128. A decisão final do modelo do curador está prevista para após 12/05/2026.
   *(2026-05-02)*

1129. A estratégia de Drive sync atualmente apresenta um problema com o token OAuth expirado.
   *(2026-05-02)*

1130. O Hub Qdrant é a fonte da verdade para a memória do Gus.
   *(2026-05-03)*

1131. O `_estado-atual.md` gerado pelo cron registra Hub ocioso há 6h+ por conta de uma ausência de conversa.
   *(2026-05-04)*

1132. O sistema está em estado intermediário arriscado: Hub Qdrant (gus_hub) é a fonte nova, mas a coleção legada gus (Mem0 self-hosted) tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

1133. A opção B para otimização do bootstrap inclui criar 3 novos arquivos lazy.
   *(2026-05-03)*

1134. Hub Qdrant é a memória central do sistema.
   *(2026-05-03)*

1135. O projeto Gus-Sync é responsável por coletar e sincronizar informações entre diferentes plataformas.
   *(2026-05-04)*

1136. A coleção 'gus' está vazia, e os 204 fragmentos prometidos não existem.
   *(2026-05-03)*

1137. Na análise, foram encontrados dados clínicos, preferências de trabalho e decisões arquiteturais.
   *(2026-05-03)*

1138. O comando para rodar a migração de fragmentos da coleção `gus` foi identificado como um disparo manual não executado.
   *(2026-05-03)*

1139. Hub Qdrant é a fonte da verdade e está no sistema de agente pessoal multi-porta.
   *(2026-05-03)*

1140. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1141. O sistema deve afirmar que não usa Mem0, pois foi aposentado.
   *(2026-05-03)*

1142. O Gus está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

1143. A auditoria do Chat apontou problemas graves, como segurança inadequada, bugs operacionais e falta de um sistema de organização dentro do Hub.
   *(2026-05-04)*

1144. A estrutura dos tools foi adaptada para ser modular após 1140 linhas em `gus/tools.py`.
   *(2026-05-04)*

1145. Gustavo Pratti de Barros é um anestesiologista e não desenvolve código — toda implementação passa pelo Gus.
   *(2026-05-03)*

1146. O sistema de sincronização com o Google Drive parou em 01/05 devido à expiração do token OAuth do usuário, resultando em dados desatualizados.
   *(2026-05-03)*

1147. A frontmatter padrão para o inbox-tiogu inclui campos como tipo, origem, destino, prioridade e status.
   *(2026-05-04)*

1148. A auditoria do Chat concluiu a presença de vulnerabilidades de segurança significativas, incluindo o fato de que o 'MCP Hub público sem `MCP_URL_SECRET`'.
   *(2026-05-04)*

1149. O plano consiste em limpar o Hub atual na Fase 1.7 antes de importar os fragmentos do Mem0 SaaS.
   *(2026-05-03)*

1150. O backend do NeuroGus está bloqueado por decisões UX não resolvidas.
   *(2026-05-03)*

1151. A auditoria do Chat envolve todos os aspectos relacionados ao projeto Claude Chat.
   *(2026-05-03)*

1152. Gustavo é anestesiologista.
   *(2026-05-03)*

1153. A decisão sobre o modelo final do Gus deve ser tomada após a finalização da auditoria e comparação dos curadores previstas para o dia 12/05/2026.
   *(2026-05-03)*

1154. O bot TioGu é um sistema multi-porta que conecta Telegram, Claude Code, Claude Chat, e futuros, utilizando o Hub Qdrant como memória central.
   *(2026-05-04)*

1155. Auditoria completa do projeto Claude Chat foi solicitada para revisar serviços, integrações e contextos operacionais.
   *(2026-05-03)*

1156. Gustavo é anestesiologista e não programa; toda implementação passa pelo Gus/Tiogu.
   *(2026-05-03)*

1157. A demanda `2026-05-01-captura-multiporta-curador.md` precisa de um gatilho proativo no Chat.
   *(2026-05-03)*

1158. O estado final dos PRs já está no código + nos docs gus-XX atualizados.
   *(2026-05-03)*

1159. Criar a pasta Gus-Sync/dialogos/inbox-chat-raw/ no Drive permite capturar demandas diretamente.
   *(2026-05-03)*

1160. O caminho de migração `ADR-001` terminará em 12/05/2026, quando Gustavo escolherá o modelo definitivo.
   *(2026-05-03)*

1161. Em 02/05/2026, foram 204 fragmentos encontrados na coleção Mem0 SaaS.
   *(2026-05-03)*

1162. As buscas no Hub podem retornar dados inconsistentes se houver um fallback para a coleção legada.
   *(2026-05-03)*

1163. O arquivo gus-identity.md tem informações redundantes que já estão presentes no arquivo gus-bootstrap.md.
   *(2026-05-03)*

1164. Os passos são todos da porta Claude Chat, que envolvem a auditoria do PR #72.
   *(2026-05-03)*

1165. A recomendação é manter o conteúdo exportado em histórico e planejar a importação filtrada depois.
   *(2026-05-03)*

1166. O fluxo sugere que ao salvar no Drive em 'Gustavo/<porta>/' o script deve preencher o frontmatter automaticamente.
   *(2026-05-03)*

1167. O Hub Qdrant é a única fonte de memória relacional do Gustavo e do agente Gus.
   *(2026-05-04)*

1168. tô aqui na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

1169. A demanda para captura multiporta do Claude Chat está parcialmente resolvida, mas falta o gatilho proativo no Chat.
   *(2026-05-02)*

1170. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

1171. O Panorama do projeto Gus em 02/05/2026 inclui identidade e arquitetura, o que está sólido e em aberto, além de observações sobre o estado final dos PRs.
   *(2026-05-02)*

1172. A implementação do Hub Qdrant é em curso com a migração da Mem0 SaaS.
   *(2026-05-03)*

1173. Existem 3 demandas paradas na pasta `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

1174. Gustavo escolhe modelo definitivo em 12/05/2026.
   *(2026-05-03)*

1175. Os arquivos com as demandas pendentes são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template `_frontmatter-referencia.md`.
   *(2026-05-03)*

1176. A última atualização do estado atual do Gus foi feita automaticamente pelo cron a cada 15 minutos.
   *(2026-05-03)*

1177. Após a correção do bug do `format()`, a divergência entre Haiku e GPT no curador é significativa, mostrando que Haiku rejeita a maioria dos fragmentos.
   *(2026-05-03)*

1178. O bot Telegram (TioGu) possui ~21 tools, multimídia, prompt caching e está em produção no Railway.
   *(2026-05-02)*

1179. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1180. Hub Qdrant é a fonte da verdade.
   *(2026-05-03)*

1181. Estou aqui na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

1182. Decisão necessária sobre o que fazer com 204 fragmentos inclui opções de manter em histórico, importar, filtrar e traduzir.
   *(2026-05-03)*

1183. A estratégia de execução proposta para Fase 1 envolve um PR consolidado com 9 commits separados por item.
   *(2026-05-03)*

1184. O fragmento deve aparecer ao buscar no brain 'gus' com 'user_id=gus'.
   *(2026-05-04)*

1185. Esses 4 dão 80% do contexto pra qualquer aba nova.
   *(2026-05-03)*

1186. A ausência de créditos na Anthropic pode impedir consultas que dependem dessa API.
   *(2026-05-02)*

1187. A demanda 'Drive sync OAuth quebrado' requer decisão do Gustavo.
   *(2026-05-03)*

1188. A stack de memória está em estado intermediário arriscado com ~204 fragmentos não-migrados e fallback ativo para Mem0.
   *(2026-05-03)*

1189. A migração do Mem0 SaaS para o Hub Qdrant está em curso, com previsão para conclusão em 12/05/2026.
   *(2026-05-03)*

1190. O estado atual do sistema foi verificado em 02/05/2026 e 12 PRs foram mergeados desde então.
   *(2026-05-03)*

1191. Hub Qdrant armazena fragmentos de memórias e decisões tomadas nas interações.
   *(2026-05-03)*

1192. Cheguei à conclusão de que o problema é que Chat A salvou no brain 'gus' mas a Aba B provavelmente buscou em 'gustavo'.
   *(2026-05-04)*

1193. O contrato schema gus-18 está parcialmente implementado: lifecycle é declarado mas não executado.
   *(2026-05-03)*

1194. O segredo está em plain text no log. Informações sensíveis podem vazar.
   *(2026-05-03)*

1195. Regenerar o segredo é necessário após o vazamento do MCP_URL_SECRET nos logs.
   *(2026-05-03)*

1196. As funcionalidades do agente Gus funcionam em três fronts ativos: TioGu, Claude Chat e Claude Code.
   *(2026-05-03)*

1197. Os commits mais recentes incluem PRs que implementam melhorias e correções relacionadas ao Chat.
   *(2026-05-03)*

1198. O arquivo gus-identity.md contém 2 linhas erradas relacionadas ao uso do Mem0 e ao nome da pasta do Drive.
   *(2026-05-03)*

1199. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1200. A falta de um mecanismo de deduplicação nos dados capturados através de múltiplas chamadas pode levar à inserção de dados repetidos no sistema.
   *(2026-05-03)*

1201. O sistema 'Gus' é um agente pessoal multi-porta rodando sobre um Qdrant Hub.
   *(2026-05-04)*

1202. Todos os processos de captura de dados e informações sensíveis precisam seguir diretrizes rigorosas para evitar vazamentos de PII.
   *(2026-05-02)*

1203. Os quatro arquivos de bootstrap fornecem 80% do contexto para qualquer nova aba.
   *(2026-05-03)*

1204. O `_estado-atual.md` está desatualizado desde 27/04.
   *(2026-05-03)*

1205. O `_estado-atual.md` (27/04) está desatualizado — git log mostra muita coisa depois.
   *(2026-05-03)*

1206. A próxima fase envolve a limpeza do Hub e a reclassificação dos 204 fragmentos encontrados.
   *(2026-05-03)*

1207. O novo secret também vazou no log.
   *(2026-05-03)*

1208. O novo segredo não deve ser enviado através de chats ou logs, deve ser mantido seguro.
   *(2026-05-03)*

1209. O protocolo de ativação Gus é acionado se alguma mensagem mencionar 'Gus'.
   *(2026-05-03)*

1210. A seção 'Personalidade do Gus' deve ser migrada para o arquivo gus/system_prompt.md.
   *(2026-05-03)*

1211. O bot do Telegram (TioGu) possui cerca de 21 ferramentas, multimídia, sistema de caching de prompts e está em produção no Railway.
   *(2026-05-04)*

1212. Os tests estão passando completamente com 187 testes totais e 10 novos adicionados.
   *(2026-05-03)*

1213. A migração do sistema de Mem0 SaaS para Hub Qdrant está em andamento, com a coleta dual de modelos terminando em 12/05/2026.
   *(2026-05-03)*

1214. A função `drop_pending_updates` é debatida: manter como True evita a perda de mensagens, mas pode causar confusão se não for notificado ao usuário.
   *(2026-05-02)*

1215. Um drive-sync OAuth está quebrado desde 01/05 14:38Z.
   *(2026-05-03)*

1216. Gus é um sistema de agente pessoal multi-porta, que inclui Telegram, Claude Code, Claude Chat e futuras extensões.
   *(2026-05-03)*

1217. Fragmentos são categorizados e ordenados para evitar poluição e garantir a qualidade da informação.
   *(2026-05-03)*

1218. O arquivo mais recente encontrado é o bootstrap v6.1, atualizado hoje.
   *(2026-05-03)*

1219. A migração ADR-001 está em curso, visando aposentar o Mem0 SaaS e tornar o Hub Qdrant a fonte da verdade.
   *(2026-05-03)*

1220. A stack de memória end-to-end apresenta um estado intermediário arriscado, com 4 chamadas LLM por unidade de input sem mecanismo de deduplicação.
   *(2026-05-03)*

1221. A estrutura do bot inclui arquivos principais como `bot.py`, `llm.py`, `memory.py`, e `tools.py`, com um total aproximado de 5.800 LOC.
   *(2026-05-04)*

1222. O bot TioGu foi desenvolvido com a possibilidade de fallback entre provedores de LLM, utilizando Anthropic e OpenAI.
   *(2026-05-04)*

1223. Aba nova só precisa olhar PRs se você falar 'tá quebrando X depois do PR #YY'.
   *(2026-05-03)*

1224. O projeto Gus utiliza um sistema multi-porta com Hub Qdrant como memória central.
   *(2026-05-03)*

1225. O estado atual do projeto é Auditado com 21 frags retornados, todos em estado ativado e 70% são considerados lixo.
   *(2026-05-03)*

1226. O arquivo gus-identity.md possui drift em relação à realidade atual do sistema.
   *(2026-05-03)*

1227. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1228. Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`. As demandas são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao e um template.
   *(2026-05-03)*

1229. O Claude Chat realiza operações com frontmatter e gestiona os fragmentos diretamente no Hub Qdrant sem a necessidade de interações intermediárias.
   *(2026-05-04)*

1230. Curadores de memória devem ser mantidos atualizados para evitar a poluição de dados.
   *(2026-05-03)*

1231. A função `auditoria_mem0` foi renomeada para `auditoria_hub`.
   *(2026-05-03)*

1232. A proposta de otimização no bootstrap visa reduzir o contexto carregado e melhorar a eficiência do Chat.
   *(2026-05-04)*

1233. Decisão sobre o que fazer com Mem0 SaaS deve ser estabelecida antes do início da Fase 1 do processo.
   *(2026-05-03)*

1234. O estado atual mostra o sistema razoavelmente ativo mas com alguns sinais de atenção: Drive sync parece quebrado, Hub com ~70% de meta-lixo, 6 demandas pendentes e Mem0 SaaS ainda não aposentado.
   *(2026-05-03)*

1235. A secret está em plain text no log do Railway, onde faz 'log.info(f"MCP montado em /{secret}/mcp ...")'.
   *(2026-05-03)*

1236. Gustavo é falante nativo de português, baseado no Rio de Janeiro.
   *(2026-05-04)*

1237. O projeto TioGu usa dois provedores de LLM: Anthropic e OpenAI.
   *(2026-05-03)*

1238. 1. Gustavo quer que o Gus tenha capacidade de disparar todos os 8 workflows disponíveis manualmente (auditoria-mem0, briefing-matinal, check-saude, export-mem0, reflexao-quinzenal, retrospectiva-semanal, sync-to-drive, sync-to-drive-full).

2. Gustavo quer auto diagnóstico do sistema: health check completo que valide GitHub, Hub Qdrant, Anthropic, Tavily, volume Railway e workflows com status visual (✅/⚠️/❌).

3. Gustavo quer que o Gus possa acessar e auditar as memórias: buscar no Hub Qdrant (brain do Gustavo), ver auditoria completa com stats/gaps/duplicatas/frescor, e acessar o próprio brain do Gus (padrões operacionais).

4. O `sync-to-drive-full` copia todos os `.md` do repo pro Drive, exceto a pasta `sensivel/` — workflow simples e sem lógica específica adicional.

5. O `notificar-inbox-tiogu` detecta arquivos novos na inbox e avisa Gustavo no Telegram (workflow de 7s).
   *(2026-04-28)*

1239. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) terminará em 12/05/2026, quando Gustavo escolherá o modelo definitivo.
   *(2026-05-03)*

1240. Agerá um Pull Request para consolidar `gus-identity.md` no `gus-bootstrap.md` e migrar parte para `gus/system_prompt.md`.
   *(2026-05-04)*

1241. A sessão do Chat rola atualmente sem validação de segurança, o que é crítico.
   *(2026-05-03)*

1242. O resultado do dryrun da limpeza não deleta nada, mas apresenta uma lista do que seria deletado.
   *(2026-05-03)*

1243. O sistema de agente pessoal multi-porta é composto por Telegram/TioGu, Claude Code, Claude Chat, e futuras interfaces como Custom GPT mobile e Alexa.
   *(2026-05-03)*

1244. As demandas pendentes para a porta incluem: captura multiporta, curador bidirecional cron, e drive-sync OAuth.
   *(2026-05-03)*

1245. As duas demandas pendentes e os documentos de próximos passos serão lidos em paralelo.
   *(2026-05-02)*

1246. Um script para exportar dados do Mem0 SaaS foi criado e precisa ser executado.
   *(2026-05-03)*

1247. O workflow GitHub Actions processa transcripts commitados via curador, usando secrets do Actions.
   *(2026-05-02)*

1248. O workflow de auditoria diária é baseado em 'auditoria_hub.py' e ignora o brain 'gus', classificando por keywords.
   *(2026-05-03)*

1249. O bot Telegram (TioGu) tem ~21 tools, multimídia, prompt caching, e usa o Hub Qdrant como memória central.
   *(2026-05-02)*

1250. Gustavo e Gus têm um guia operacional que inclui o manual de comportamento e a identidade de Gus.
   *(2026-05-03)*

1251. O Chat atualmente não tem um protocolo claro para decidir entre os canais de escrita disponíveis.
   *(2026-05-03)*

1252. O MCP tá público — qualquer scanner que descobrir a URL Railway lê todo o Hub.
   *(2026-05-03)*

1253. Gustavo é anestesiologista, não programa — toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

1254. Gus é um sistema de agente pessoal multi-porta com uma memória central no Hub Qdrant, espelhado no Drive.
   *(2026-05-03)*

1255. O estado atual do projeto é implementado em várias fases, incluindo a fase de migração para Hub Qdrant e a paralisação das operações em Mem0 SaaS.
   *(2026-05-03)*

1256. Em `Railway`, deve haver a variável `MCP_AUTH_DISABLED` configurada como `true`.
   *(2026-05-03)*

1257. O estado das memórias do Hub Qdrant é crítico e apresenta riscos de poluição cruzada.
   *(2026-05-03)*

1258. Coleção legada `gus` ainda viva, fallback Mem0 ativo em leitura/delete.
   *(2026-05-03)*

1259. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1260. Os 204 fragmentos do Mem0 SaaS foram exportados para a pasta `historico/`.
   *(2026-05-03)*

1261. O arquivo gus-identity.md contém informações sobre a identidade do Gustavo e do Gus.
   *(2026-05-03)*

1262. A arquitetura do sistema 'Gus' agora tem dois cérebros independentes no Hub Qdrant: `gus_hub`, onde `user_id='gustavo'` contém fatos sobre Gustavo e `user_id='gus'` contém a autorreflexão do agente.
   *(2026-05-03)*

1263. O core obrigatório de toda aba nova envolve quatro arquivos: gus-bootstrap.md, gus-identity.md, gus-estado-atual.md e o projetos/gus/_estado-atual.md.
   *(2026-05-03)*

1264. A falta de implementação do lifecycle no schema gus-18 leva a um acúmulo de fragmentos sem um processamento adequado, pois fragmentos permanecem na coleção com status 'ativo' indefinidamente.
   *(2026-05-03)*

1265. A URL secret protege o MCP.
   *(2026-05-03)*

1266. A fase 2 do TioGu inclui a documentação e a reescrita do `system_prompt.md`.
   *(2026-05-03)*

1267. A importação de conteúdo do Mem0 SaaS deve ser feita apenas após a melhoria do prompt do curador.
   *(2026-05-03)*

1268. A inclusão de um novo campo 'prompt_version' foi feita para rastrear a versão do prompt utilizado no curador.
   *(2026-05-03)*

1269. A captura proativa do Chat foi implementada para salvar automaticamente fatos, decisões e preferências durante a conversa.
   *(2026-05-03)*

1270. O script `migrar_gus_para_hub.py` foi executado em dry-run e não encontrou fragmentos para migração.
   *(2026-05-03)*

1271. Hub `gus` contém 20 fragmentos, com poluição cruzada confirmada entre `gustavo` e `gus`.
   *(2026-05-03)*

1272. Gustavo Pratti de Barros é anestesiologista na Dimagem no Rio de Janeiro e pesquisador independente em IA.
   *(2026-05-03)*

1273. Pasta se chama Gus-Sync, não GitHub-Sync.
   *(2026-05-04)*

1274. O Hub Qdrant está funcionando corretamente, com 50+ frags, mais recente há 4.4h (02/05 19:44 BRT).
   *(2026-05-03)*

1275. O estado atual do projeto está registrado em arquivos de status e pode ser acessado a qualquer momento.
   *(2026-05-03)*

1276. Gustavo é anestesiologista e não programa — toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

1277. O segredo foi logado em plain text no log do Railway.
   *(2026-05-03)*

1278. A arquitetura de memória do sistema Gus é baseada em dois brains independentes no Qdrant Hub.
   *(2026-05-03)*

1279. A auditoria diária é cega para o brain 'gus' e ignora a área que o curador já preencheu.
   *(2026-05-03)*

1280. A auditoria do Chat está focada na segurança, confiabilidade e arquitetura do sistema.
   *(2026-05-04)*

1281. A URL `MCP_URL_SECRET` protege o MCP.
   *(2026-05-03)*

1282. O segredo vazou no log do Railway e precisa ser regenerado.
   *(2026-05-03)*

1283. A fase de auditoria deve incluir a análise da divergência de retorno entre Haiku e GPT quando a saída é vazia.
   *(2026-05-03)*

1284. A arquitetura do sistema Gus apresenta redundâncias entre as camadas de userMemories, project knowledge e gus-bootstrap.
   *(2026-05-03)*

1285. A proposta para a captura proativa do Chat em tempo real inclui a frequência, tipos cobertos e coexistência com upload .md.
   *(2026-05-03)*

1286. O código de leitura em `gus/memory.py` ainda faz fallback para a coleção legada Mem0 SaaS, que tem aproximadamente 204 fragmentos não-migrados.
   *(2026-05-03)*

1287. Panorama do projeto inclui core obrigatório: arquivos de manual operacional, identidade do Gustavo e do Gus, e snapshot do Hub.
   *(2026-05-03)*

1288. O Hub Qdrant é a memória central do Gus, armazenando informações essenciais.
   *(2026-05-03)*

1289. O estado do `_estado-atual.md` está de 27/04 e precisa ser atualizado.
   *(2026-05-03)*

1290. As pendências de Gustavo incluem definir `MCP_URL_SECRET` no Railway e recadastrar o Connector claude.ai devido a problemas de privacidade.
   *(2026-05-03)*

1291. A divergência entre Haiku e GPT-4o-mini é dramática, com Haiku retornando zero fragmentos em várias chamadas.
   *(2026-05-03)*

1292. O arquivo untracked é o log que registra 'no-op: anthropic_missing' e segue.
   *(2026-05-02)*

1293. O sistema de auditoria da memória é cego para o brain 'gus' e não considera o 'area' preenchido.
   *(2026-05-03)*

1294. A atualização na estrutura do bot e nas ferramentas permitirá maior agilidade nas futuras implementações e manutenções.
   *(2026-05-04)*

1295. A fase 1 do projeto contém 9 itens a serem consolidado.
   *(2026-05-03)*

1296. A captura multiporta do Claude Chat precisa de um gatilho proativo no Chat, e isso está em discussão.
   *(2026-05-02)*

1297. Gustavo é anestesiologista e utiliza um sistema de agente pessoal multi-porta chamado Gus.
   *(2026-05-03)*

1298. Gus é um sistema de agente pessoal multi-porta com memória central no Hub Qdrant e arquivos .md no GitHub, espelhados no Drive.
   *(2026-05-03)*

1299. O state final do PRs já está no código e nos docs gus-XX atualizados.
   *(2026-05-03)*

1300. As demandas pendentes são: captura-multiporta-curador, drive-sync-oauth-fix e pendencias-claude-chat-consolidacao.
   *(2026-05-02)*

1301. Decidi que será feito um backup dos fragmentos do Mem0 SaaS antes de apagá-lo definitivamente.
   *(2026-05-03)*

1302. A migração para o Hub Qdrant está em andamento, com um cronograma que inclui a descontinuação do Mem0 SaaS.
   *(2026-05-03)*

1303. Gustavo Pratti de Barros é anestesiologista no Dimagem e pesquisador independente em IA.
   *(2026-05-04)*

1304. 204 fragmentos foram exportados do Mem0 SaaS e estão seguros em `historico/`.
   *(2026-05-03)*

1305. A demanda capturada em `dialogos/inbox-claude-code/` é para consolidar pendências do Claude Chat.
   *(2026-05-03)*

1306. Hub Qdrant é a fonte da verdade.
   *(2026-05-03)*

1307. O Hub Qdrant coleta dual até 12/05 com um curador híbrido.
   *(2026-05-02)*

1308. Depois de configurar o segredo no Railway, precisamos validar se tudo está funcionando.
   *(2026-05-03)*

1309. As auditorias são realizadas diariamente e o sistema classifica fragmentos por keywords, ignorando a área preenchida pelo curador.
   *(2026-05-03)*

1310. Curador híbrido novo garante resiliência, preferindo falhar alto e claro em vez de injetar lixo no Hub.
   *(2026-05-03)*

1311. A demanda `2026-05-01-captura-multiporta-curador.md` precisa de um gatilho proativo no Chat.
   *(2026-05-03)*

1312. A stack está em estado intermediário arriscado: Hub Qdrant é a fonte nova, mas a coleção legada gus (Mem0 self-hosted) tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

1313. Gustavo Pratti de Barros é anestesiologista na Dimagem (Rio de Janeiro, 3 unidades) e pesquisador independente em IA.
   *(2026-05-04)*

1314. O `claude.md` na raiz é auto-injetado em toda sessão.
   *(2026-05-02)*

1315. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1316. A decisão de migração ADR-001 está em curso e tem como objetivo substituir o Mem0 SaaS pelo Hub Qdrant como fonte da verdade.
   *(2026-05-03)*

1317. A diferença entre o status do projeto e o estado atual é que o `_estado-atual.md` estava desatualizado.
   *(2026-05-03)*

1318. Para cada redeploy, mensagens enviadas durante o downtime são descartadas.
   *(2026-05-02)*

1319. Decisões sobre a frequência da captura de memória pro Chat são debatidas, incluindo níveis de agressividade.
   *(2026-05-03)*

1320. O Hub não tem nenhum fragmento com tipo=identidade_operacional + estado=estavel nem procedural + estado=estavel.
   *(2026-05-03)*

1321. O sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa) tem como memória central no Hub Qdrant, com arquivos .md no GitHub, espelhados no Drive.
   *(2026-05-03)*

1322. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1323. O `_estado-atual.md` está desatualizado e o Hub reporta 19 fragmentos.
   *(2026-05-02)*

1324. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa.
   *(2026-05-02)*

1325. Gustavo Pratti de Barros é anestesiologista no Dimagem no Rio de Janeiro e pesquisador independente em IA.
   *(2026-05-04)*

1326. Esses 4 dão 80% do contexto pra qualquer aba nova.
   *(2026-05-03)*

1327. Fragmentos são salvos com a tag 'via=claude-chat' para identificar suas origens.
   *(2026-05-03)*

1328. O sistema 'Gus' é um agente pessoal multi-porta que está em produção com quatro portas ativas: Telegram, Code, Chat e Custom GPT.
   *(2026-05-04)*

1329. As atualizações recentes no sistema incluem a promoção automática de fragmentos após 30 dias e no mínimo dois acessos, porém isso ainda não foi implementado.
   *(2026-05-03)*

1330. Há 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

1331. No estado atual, o core do projeto é abordado a partir do arquivo `gus-bootstrap.md`, que contém diretrizes operacionais e identidade.
   *(2026-05-04)*

1332. O principal sistema de Gustavo, 'Gus', está em produção: um agente de IA multi-porta pessoal (bot do Telegram @Tiogubot, Claude Code, Claude Chat com conector MCP, Custom GPT em setup, Alexa planejada). A estrutura de memória foi migrada do Mem0 para o Hub Qdrant direto, agora com mais de 1076 fragmentos em dois cérebros (gustavo para fatos sobre ele, gus para autorreflexão do agente). O trabalho recente se concentrou em melhorias: o PR #72 corrigiu um curador que falhava 100% (KeyError no template JSON), o PR #80 redigiu o vazamento de segredos nos logs do MCP, e o PR #83 introduziu bootstrap-v6 com dois caminhos de captura (MCP em tempo real + upload curado). O NeuroGus (visualização em gráfico 3D do Hub) está totalmente projetado e desbloqueado uma vez que as decisões §11.1-11.5 forem finalizadas. A publicação do Phronesis-Bench está em revisão/preparação para o Alignment Forum. O Mem0 SaaS tem um encerramento planejado após a coleta A/B dupla de curadores até 12/05/2026.
   *(2026-05-03)*

1333. A falta de um mecanismo de deduplica os fragmentos criados gera o risco de poluição cruzada entre os brains.
   *(2026-05-03)*

1334. Estou aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1335. Gus é o agente pessoal de Gustavo Pratti de Barros.
   *(2026-05-04)*

1336. O SDK da Anthropic foi atualizado da versão 0.40.0 para a versão 0.97.0.
   *(2026-05-04)*

1337. O status consolidado, próximos passos, NeuroGus, e PRs recentes são necessários para fechar o panorama do projeto.
   *(2026-05-04)*

1338. Aba nova só precisa olhar PRs se houver um bug específico no código mexido recentemente.
   *(2026-05-03)*

1339. O hook de Stop do retro-engine falhou devido à falta da variável ANTHROPIC_API_KEY.
   *(2026-05-02)*

1340. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e precisa de uma decisão.
   *(2026-05-02)*

1341. Algumas demandas têm nome quebrado.
   *(2026-05-03)*

1342. A recomendação é seguir pela opção B, que é o meio-termo entre ganho real e segurança.
   *(2026-05-03)*

1343. O arquivo `gus-identity.md` se mostrou desatualizado e redundante, pois contém informações que estão presentes no arquivo `gus-bootstrap.md`.
   *(2026-05-04)*

1344. Gus é um agente pessoal multi-porta que interage através de diferentes plataformas e tem uma memória central no Hub Qdrant.
   *(2026-05-03)*

1345. O Hub tem 19 fragmentos no brain gustavo.
   *(2026-05-03)*

1346. O estado atual do trabalho pode ser consultado via ego_cache_atual ou fragmentos_recentes, ou lendo o arquivo dialogos/_bootstrap/gus-estado-atual.md.
   *(2026-05-03)*

1347. Mem0 SaaS aposentado desde 27/04/2026 (ADR-001 Fase 5). Hub Qdrant é fonte única.
   *(2026-05-04)*

1348. Adicionar alerta opcional via notificar_telegram se Gustavo quiser saber em tempo real requer secret do Telegram bot.
   *(2026-05-03)*

1349. Gustavo é anestesiologista no Dimagem e possui hipertireoidismo.
   *(2026-05-04)*

1350. O sistema deve utilizar o `MCP_URL_SECRET` para proteger o acesso ao Hub.
   *(2026-05-02)*

1351. Branch do projeto tem 9 commits — só 2 são substanciais: curador fix e auditoria do Chat. Os outros 7 são auto-commits dos hooks Stop.
   *(2026-05-03)*

1352. Ele possui hipertireoidismo sob tratamento com Tapazol, acompanhado por um endocrinologista.
   *(2026-05-03)*

1353. A implementação do fallback para OpenAI Vision inclui uma nova função que converte o conteúdo multimodal do Anthropic para o formato esperado pelo OpenAI.
   *(2026-05-03)*

1354. O sistema 'Gus' é um agente pessoal multi-porta que opera em Qdrant Hub.
   *(2026-05-04)*

1355. Salvei a autoreflexão do agente sobre a sessão de hoje no brain `gus`.
   *(2026-05-03)*

1356. Na atualização do Drive, foram encontrados 3 arquivos novos relacionados à ingestão de exames no Hub.
   *(2026-05-03)*

1357. As demandas pendentes no `dialogos/inbox-claude-code/` são: captura-multiporta-curador, drive-sync-oauth-fix e pendencias-claude-chat-consolidacao.
   *(2026-05-03)*

1358. O segredo 'MEM0_API_KEY' é uma variável que pode ser verificada para saber se há conteúdo no Mem0 SaaS.
   *(2026-05-03)*

1359. O core do bootstrap contém regras universais sobre como operar: não alucinar, verificar informações antes de afirmar a ausência de algo, e validar antes de fazer operações irreversíveis.
   *(2026-05-03)*

1360. Auditoria diária (`auditoria_hub.py`) é cega para o brain `gus` e classifica por keywords.
   *(2026-05-03)*

1361. Os arquivos que ele inicializa quando lê o bootstrap estão no Drive.
   *(2026-05-03)*

1362. O conteúdo do Mem0 SaaS tem 204 fragmentos que estão no API.
   *(2026-05-03)*

1363. O sistema está em produção e o hub ainda não tem o URL_SECRET, representando um risco potencial de segurança.
   *(2026-05-02)*

1364. Hub Qdrant é a memória central do Gus.
   *(2026-05-03)*

1365. Esses 4 dão 80% do contexto pra qualquer aba nova: manual operacional do Gus, quem é o Gustavo + quem é o Gus enquanto entidade, handoff auto-gerado pelo cron, onde paramos na sessão anterior.
   *(2026-05-03)*

1366. A auditoria do Hub Qdrant confirma que a coleção legada `gus` está vazia, invalidando a necessidade de migração de fragmentos.
   *(2026-05-03)*

1367. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`. Algumas com nome quebrado.
   *(2026-05-03)*

1368. O Hub Qdrant contém 1076+ fragmentos de memória, divididos entre os brains `gustavo` e `gus`.
   *(2026-05-04)*

1369. O protocolo de ativação Gus é ativado quando a mensagem de abertura menciona 'Gus'.
   *(2026-05-03)*

1370. Referências no CLAUDE.md foram atualizadas para refletir as mudanças no sistema.
   *(2026-05-03)*

1371. A auditoria identificou que o segredo vazou em três lugares: logs do Railway, chat e transcripts comitados.
   *(2026-05-03)*

1372. Se a mensagem for uma imagem, o modelo Anthropic é selecionado.
   *(2026-05-04)*

1373. Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, (_frontmatter-referencia.md é só template).
   *(2026-05-03)*

1374. O curador do Gus opera com múltiplos modelos (Haiku e GPT-4), com foco na eficiência e na precisão.
   *(2026-05-03)*

1375. O arquivo `gus-identity.md` é uma redundância ao `gus-bootstrap.md` e está desatualizado, pois o status final do projeto é representado no arquivo `gus-estado-atual.md` gerado a cada 15 minutos.
   *(2026-05-03)*

1376. Gustavo é anestesiologista e não programa. Toda implementação passa por Gus/Tiogu.
   *(2026-05-03)*

1377. O curador do Telegram tem dado erro 400 e precisa de correção.
   *(2026-05-03)*

1378. A auditoria de 02/05 já marcou pendente a questão do cross-brain pollution entre os agentes 'gustavo' e 'gus'.
   *(2026-05-03)*

1379. O documento de auditoria atual é o 'auditoria_hub.py', que é gerado diariamente para acompanhar as atividades do Hub.
   *(2026-05-03)*

1380. A coleção `gus` no Hub Qdrant está vazia, sem ação.
   *(2026-05-03)*

1381. Gustavo Pratti de Barros é anestesiologista no Dimagem, no Rio de Janeiro, e pesquisa IA de forma independente.
   *(2026-05-04)*

1382. As decisões arquiteturais e operacionais do sistema são registradas em documentos no GitHub.
   *(2026-05-03)*

1383. O objetivo é limpar o Hub, removendo conteúdo antigo e mantendo apenas informações úteis.
   *(2026-05-03)*

1384. Para mandar demanda pelo celular, agora basta criar um arquivo no Drive na pasta Gus-Sync/dialogos/inbox-gustavo/code/.
   *(2026-05-03)*

1385. O projeto Phronesis-Bench está em publicação e o NeuroGus é uma visualização do Hub.
   *(2026-05-04)*

1386. A cada 3 turnos, o curador processa fragmentos dos dois modelos em paralelo, salvando os metadados no Hub.
   *(2026-05-03)*

1387. A auditoria na stack de memória está em um estado intermediário arriscado, com 204 fragmentos não-migrados.
   *(2026-05-03)*

1388. A migração das memórias antigas para o Hub Qdrant deve ser feita com a classificação correta para evitar poluição do sistema.
   *(2026-05-03)*

1389. Gustavo é anestesiologista, não programa.
   *(2026-05-03)*

1390. No item 1.6, a estratégia recomendada foi a de eliminar o fallback para não injetar lixo no Hub com resumos brutos.
   *(2026-05-03)*

1391. O sistema principal de Gustavo, 'Gus', está em produção: um agente pessoal multi-portas (bot Telegram @Tiogubot, Claude Code, Claude Chat com conector MCP, Custom GPT em configuração, Alexa planejada). A base de memória foi migrada do Mem0 para o Hub Qdrant direto, agora com mais de 1076 fragmentos em dois cérebros (gustavo para fatos sobre ele, gus para autorreflexão do agente). O trabalho recente se concentrou na robustez.
   *(2026-05-03)*

1392. A stack de memória end-to-end do Gus inclui três caminhos de escrita: Telegram, Claude Chat e Claude Code.
   *(2026-05-03)*

1393. O bot Telegram (TioGu) possui ~21 ferramentas distintas integradas.
   *(2026-05-03)*

1394. Uma das propostas é manter o core no bootstrap e criar arquivos lazy.
   *(2026-05-03)*

1395. O arquivo `gus/dimagem.py` deve ser movido para `gus/integrations/dimagem.py`, indicando que é uma integração de domínio e não uma parte central do bot.
   *(2026-05-02)*

1396. Atualmente, ele está focado no sistema 'Gus', um agente pessoal de inteligência artificial multi-portas, em produção: bot do Telegram, Claude Code, Claude Chat com conector MCP e Custom GPT em configuração.
   *(2026-05-03)*

1397. A stack de memória está em estado intermediário arriscado, com a coleção legada `gus` ainda viva e fallback ativo para Mem0.
   *(2026-05-03)*

1398. O planejamento para o NeuroGus está 100% pronto e existem 3 demandas em `inbox-tiogu/` de 28/04.
   *(2026-05-02)*

1399. O curador Telegram está apresentando erro 400 recorrente, indicando que o ingest do Chat pode estar falhando silenciosamente.
   *(2026-05-04)*

1400. O Protocolo de Análise IA de Exames Laboratoriais v1 define 8 fases sequenciais que qualquer IA executa sobre um exame, gerando saída estruturada reproduzível.
   *(2026-05-02)*

1401. A auditoria diária do Hub Qdrant é cega para o brain `gus`.
   *(2026-05-03)*

1402. O TioGu implementa um sistema de prompt caching que reduz os custos de input em aproximadamente 70% em janelas de 5 minutos.
   *(2026-05-03)*

1403. O segredo atual foi exposto no log do Railway.
   *(2026-05-03)*

1404. Gustavo está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-02)*

1405. O estado final do modelo curador deve ser comparado após 12/05/2026.
   *(2026-05-02)*

1406. A lista de candidatos a deletar será gerada pelo script `limpeza_hub_dryrun.py`, que será revisada antes da aplicação.
   *(2026-05-03)*

1407. O arquivo `gus-identity.md` é redundante com o bootstrap e está desatualizado.
   *(2026-05-03)*

1408. Gustavo viaja com sua esposa, em busca de natureza e aventura.
   *(2026-05-04)*

1409. Hub Qdrant é a nova fonte da verdade. Coleta dual de modelos no curador (Haiku × GPT-4o-mini).
   *(2026-05-03)*

1410. O script `busca_memorias (MCP)` é utilizado para buscar memórias no Hub.
   *(2026-05-03)*

1411. O bot Telegram (TioGu) possui ~21 tools, multimídia, prompt caching e está em produção no Railway.
   *(2026-05-04)*

1412. O workflow de migração revelou que a coleção `gus` está vazia e que as 18 entradas que entraram em modo `fallback-mem0` em 28/04 não estão presentes.
   *(2026-05-03)*

1413. A arquitetura do TioGu inclui um sistema de fallback cross-vendor que melhora a resiliência do bot.
   *(2026-05-02)*

1414. A tag 'prompt_version' será adicionada aos payloads do curador para rastreamento.
   *(2026-05-03)*

1415. Existem 6 demandas pendentes em 'dialogos/inbox-claude-code/'.
   *(2026-05-03)*

1416. Importações recentes pelo Drive incluem 3 arquivos novos sobre ingestão de exames no Hub e protocolo truncado.
   *(2026-05-03)*

1417. O Hub Qdrant é a única fonte de memória relacional do Gustavo desde a aposentadoria do Mem0.
   *(2026-05-04)*

1418. Os principais canais de escrita do Chat são o MCP em tempo real, upload curado de .md e demandas no inbox-code.
   *(2026-05-03)*

1419. O sistema multi-porta do projeto Gus tem o Hub Qdrant como memória central.
   *(2026-05-02)*

1420. Vou fazer auditoria completa em todas as superfícies do Chat.
   *(2026-05-03)*

1421. A memória central do Gus é armazenada no Hub Qdrant.
   *(2026-05-03)*

1422. O bootstrap atual não tem um entry point claro e a ordem de leitura poderá confundir na inicialização.
   *(2026-05-04)*

1423. A coleção legada `gus` no Mem0 SaaS ainda contém fragmentos que não foram migrados para o Hub Qdrant.
   *(2026-05-03)*

1424. Os 60 PRs são considerados ruído gigante no contexto para ganho zero quando se busca entender o estado atual do projeto.
   *(2026-05-02)*

1425. Os arquivos 'gus-bootstrap.md', 'gus-identity.md', e 'gus-estado-atual.md' são essenciais para qualquer nova aba.
   *(2026-05-03)*

1426. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e especula-se que o refresh token OAuth expirou.
   *(2026-05-03)*

1427. O `_estado-atual.md` na pasta projetos/gus está desatualizado em 27/04 — o estado vivo é no `gus-estado-atual.md` que é atualizado a cada 15min.
   *(2026-05-02)*

1428. Drive sync via WIF: migração de OAuth user para Workload Identity Federation com Service Account.
   *(2026-05-03)*

1429. A auditoria do Hub Qdrant não está ciente do brain `gus` e classifica apenas por keywords, ignorando a área definida pelo curador.
   *(2026-05-03)*

1430. A pasta inbox-mem0-from-chat será renomeada para inbox-chat-raw e o _log/resumos-mem0 será renomeado para _log/curador.
   *(2026-05-03)*

1431. As demandas pendentes para a porta incluem a captura multiporta, curador bidirecional cron e a sincronização com o Drive.
   *(2026-05-03)*

1432. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1433. Os 3 passos mencionados são todos da porta Claude Chat: MCP_URL_SECRET, Recadastrar Connector claude.ai e Drive sync.
   *(2026-05-03)*

1434. A migração do sistema para o Hub Qdrant está em andamento, com previsão de término em 12/05/2026.
   *(2026-05-03)*

1435. O segredo precisa ser gerado na forma de um UUID de 64 caracteres hex.
   *(2026-05-03)*

1436. O agente pessoal é projetado para operar como uma interface de captura e consolidação de informações.
   *(2026-05-03)*

1437. O projeto Gus é um sistema de agente pessoal multi-porta que conecta diferentes interfaces como Telegram, Claude Code, Claude Chat e futuras integrações como Alexa.
   *(2026-05-03)*

1438. O estado atual da migração está em curso, e a coletânea legada do Mem0 SaaS precisa ser encerrada, pois o Hub Qdrant é a fonte da verdade.
   *(2026-05-03)*

1439. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) mudará para um modelo definitivo até 12/05/2026.
   *(2026-05-03)*

1440. Remover MCP_URL_SECRET do log.
   *(2026-05-03)*

1441. Os fragmentos do Mem0 SaaS incluem conteúdo biográfico, preferências de trabalho, decisões arquiteturais e contexto pessoal.
   *(2026-05-03)*

1442. A pasta deve conter subpastas para Chat, Code e TioGu.
   *(2026-05-03)*

1443. O manual operacional do Gus contém as regras de comportamento e como cada porta usa o Hub.
   *(2026-05-03)*

1444. O agente Gus deve evitar redundâncias em seus arquivos operacionais e documentais.
   *(2026-05-04)*

1445. Não existe um gerenciamento correto para as exceções que ocorrem nas respostas do bot quando utiliza o modelo Anthropic.
   *(2026-05-02)*

1446. O estado-atual.md carrega fragmentos do Hub das últimas 6h.
   *(2026-05-03)*

1447. O sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) tem o Hub Qdrant como memória central, GitHub como conhecimento e Drive como espelho.
   *(2026-05-02)*

1448. Estado da migração ADR-001 em curso: aposentar Mem0 SaaS, Hub Qdrant é fonte da verdade.
   *(2026-05-03)*

1449. Os quatro documentos fundamentais são: `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md`, e `estado-atual.md`.
   *(2026-05-03)*

1450. A migração ADR-001 tem como objetivo aposentar o Mem0 SaaS e tornar o Hub Qdrant a fonte da verdade.
   *(2026-05-03)*

1451. O MCP está público — qualquer scanner que descobrir a URL Railway lê todo o Hub.
   *(2026-05-03)*

1452. Os `read_repo_file` devem ser usados quando o Chat pesquisa informações, enquanto a memória deve ser usada quando conversa entra no contexto da interação.
   *(2026-05-03)*

1453. O MCP está público — qualquer scanner que descobrir a URL Railway lê todo o Hub.
   *(2026-05-03)*

1454. Core obrigatório na aba nova inclui: arquivo `gus-bootstrap.md`, que contém o manual operacional do Gus; `gus-identity.md`, que descreve quem é o Gustavo e o Gus; `gus-estado-atual.md`, que fornece um snapshot do Hub; e `estado-atual.md`, que indica onde paramos na sessão anterior.
   *(2026-05-03)*

1455. A URL secret destrava a escrita real-time do Chat com a função 'ingestar_fragmento'.
   *(2026-05-03)*

1456. O sistema 'Gus' é um agente pessoal multi-porta que opera no Telegram, Claude Code, Claude Chat com MCP Connector, Custom GPT, e Alexa planejada.
   *(2026-05-03)*

1457. Pronto para verificar se o sync do Drive está rodando e ativo.
   *(2026-05-03)*

1458. O código de leitura em `gus/memory.py` ainda faz fallback para a coleção `gus` da Mem0.
   *(2026-05-03)*

1459. A variável MCP_URL_SECRET protege o acesso ao MCP e permite escrita real-time do Chat.
   *(2026-05-03)*

1460. O bot não possui testes automatizados, o que representa um alto risco de manutenção e bugs.
   *(2026-05-02)*

1461. O passo para Drive sync foi resolvido com a migração para WIF conforme PR #76.
   *(2026-05-03)*

1462. O nome da pasta do Google Drive é Gus-Sync, ao contrário do que está registrado no gus-identity.md, que menciona GitHub-Sync.
   *(2026-05-04)*

1463. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) está prevista para terminar em 12/05/2026.
   *(2026-05-03)*

1464. A integração com LLM da Anthropic está sendo realizada através do SDK da Anthropic na versão 0.40.0, que está desatualizado em relação às versões mais recentes disponíveis.
   *(2026-05-02)*

1465. Hub Qdrant é a memória central do sistema Gus.
   *(2026-05-03)*

1466. O arquivo dimagem.py deve ser movido para a pasta integrations, para melhorar a clareza sobre sua natureza como integração de domínio.
   *(2026-05-02)*

1467. As decisões sobre o que incluir nos arquivos de bootstrap devem considerar a eficiência e a necessidade de informação ao agente.
   *(2026-05-04)*

1468. As fases do projeto incluem testes em rede, reconciliação de documentos estáticos e refatoração de código.
   *(2026-05-03)*

1469. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-04)*

1470. A estratégia de Fases para saneamento do Hub Qdrant foi estabelecida, com 6 fases e foco na limpeza inicial.
   *(2026-05-03)*

1471. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1472. Existem três demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

1473. A migração para o Hub Qdrant está em curso e a coleta dual de modelos no curador termina em 12/05/2026.
   *(2026-05-03)*

1474. A auditoria do Chat revela que existem problemas com a configuração de segurança e operação da aplicação.
   *(2026-05-03)*

1475. O sistema é designado para capturar e processar informações ao longo do tempo.
   *(2026-05-04)*

1476. O curador Telegram apresenta erro 400 há 3 dias.
   *(2026-05-03)*

1477. Chat A salvou um fragmento com ID UUID 42aea182-d4a2-4626-8a85-5ede861b311b.
   *(2026-05-03)*

1478. No processo de migração, a coleta dual de modelos no curador termina em 12/05/2026.
   *(2026-05-03)*

1479. O bot Telegram, TioGu, possui 21 ferramentas distintas integradas.
   *(2026-05-03)*

1480. A auditoria do Chat foi concluída com correções.
   *(2026-05-03)*

1481. A migração do Mem0 SaaS para o Hub Qdrant está em andamento. A coleta dual de modelos no curador termina em 12/05/2026.
   *(2026-05-03)*

1482. Os 204 fragmentos históricos não existem em lugar nenhum acessível.
   *(2026-05-03)*

1483. O sistema de alertas de custo foi implementado e requer a confirmação da variável `API_PUBLIC_URL` nos GitHub Secrets.
   *(2026-05-03)*

1484. Gustavo Pratti de Barros é anestesiologista e não programa.
   *(2026-05-03)*

1485. O sistema de agente pessoal multi-porta tem memória central no Hub Qdrant, arquivos .md no GitHub e é espelhado no Drive.
   *(2026-05-03)*

1486. Esses 4 arquivos dão 80% do contexto pra qualquer aba nova.
   *(2026-05-03)*

1487. Depois da configuração do MCP_URL_SECRET no Railway, a URL do connector do claude.ai muda, e é necessário recadastrar.
   *(2026-05-03)*

1488. WIF/Workload Identity Federation pro Drive sync resolve o passo 4 da lista.
   *(2026-05-03)*

1489. PR #72 corrigiu curador que falhava 100% há 3 dias (KeyError em chaves JSON do template de prompt).
   *(2026-05-03)*

1490. O sistema de agente pessoal Gus tem uma memória central no Hub Qdrant.
   *(2026-05-03)*

1491. O conteúdo está seguro em `historico/` — não há pressa.
   *(2026-05-03)*

1492. O `gus-identity.md` contém redundância com o `gus-bootstrap.md`, duplicando informações já presentes neste último.
   *(2026-05-04)*

1493. As 6 sub-pendências da demanda consolidada incluem ativar `MCP_URL_SECRET` no Railway, recadastrar Connector claude.ai, localizar mock HTML NeuroGus 28/04, decisões §11.3-11.5 NeuroGus Fase 2, captura tempo real Chat — Opção A, e Drive sync → Service Account.
   *(2026-05-02)*

1494. A arquitetura do TioGu permite fallback entre LLMs para resiliência.
   *(2026-05-03)*

1495. O Hub Qdrant é a fonte da verdade, substituindo Mem0 SaaS.
   *(2026-05-03)*

1496. O curador no Claude Chat estava com um bug crítico que foi corrigido em PR #72.
   *(2026-05-03)*

1497. Se Hub falhar antes do move, próxima rodada tenta de novo (pode duplicar — risco baixo dado o volume).
   *(2026-05-03)*

1498. Há 6 demandas listadas no inbox-claude-code, das quais 3 são demandas reais.
   *(2026-05-03)*

1499. O conteúdo dos 204 fragmentos da memória Mem0 SaaS é considerado de qualidade superior ao que está no Hub atualmente.
   *(2026-05-03)*

1500. O projeto Gus utiliza o MCP (Multi-Channel Protocol) como uma ferramenta central de ingestão e interação.
   *(2026-05-02)*

1501. Gus é um sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa).
   *(2026-05-03)*

1502. O estado final dos PRs já está no código e nos docs gus-XX atualizados.
   *(2026-05-03)*

1503. A configuração do WIF para o Drive prevê o uso de uma Service Account para realizar a sincronização sem OAuth de usuário.
   *(2026-05-03)*

1504. O curador híbrido está executando uma comparação A/B entre Anthropic e OpenAI.
   *(2026-05-04)*

1505. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

1506. O Hub Qdrant é usado para armazenar memórias do agente Gustavo e do próprio Gus.
   *(2026-05-04)*

1507. A migração ADR-001 está em curso, e a coleta dual de modelos no curador termina em 12/05/2026.
   *(2026-05-03)*

1508. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-04)*

1509. A arquitetura do bot TioGu é composta por integração de ferramentas, comunicação assíncrona e persistência de estado utilizando um sistema robusto de erro e retry.
   *(2026-05-02)*

1510. Core obrigatório para cada aba nova inclui arquivos como `gus-bootstrap.md`, que contém manual operacional do Gus.
   *(2026-05-03)*

1511. A arquitetura do TioGu consiste em um sistema multi-porta com Hub Qdrant como memória central.
   *(2026-05-04)*

1512. O bot opera com dependências como python-telegram-bot, anthropic SDK, openai, FastAPI e Qdrant.
   *(2026-05-02)*

1513. O Hub Qdrant contém ~204 fragmentos não-migrados e o código ainda faz fallback para a coleção Mem0 SaaS, resultando em buscas inconsistentes.
   *(2026-05-03)*

1514. O file `gus-estado-atual.md` deve ser lido para um estado mais fresco do projeto em relação ao Hub.
   *(2026-05-02)*

1515. Os fragmentos no Hub nunca são atualizados, e o estado de cada fragmento permanece 'ativo' indefinidamente.
   *(2026-05-03)*

1516. TioGu usa 2 provedores LLM em paralelo: Anthropic e OpenAI.
   *(2026-05-04)*

1517. O Hub Qdrant é a memória central do sistema Gus.
   *(2026-05-03)*

1518. A demanda '2026-05-01-captura-multiporta-curador.md' precisa de uma mudança de gatilho proativo no Chat.
   *(2026-05-03)*

1519. Gus está na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1520. O estado final dos PRs já está no código e nos docs gus-XX atualizados.
   *(2026-05-02)*

1521. O estado final dos PRs já está no código + nos docs gus-XX atualizados.
   *(2026-05-02)*

1522. O projeto necessita de uma limpeza na coleção do Hub, especialmente eliminando dados duplicados e indesejados.
   *(2026-05-03)*

1523. Commit `20c6865` — Implementação de trilha de auditoria em `hub.store.deletar()`.
   *(2026-05-03)*

1524. Gustavo Pratti de Barros é anestesiologista no Dimagem e pesquisador independente em IA.
   *(2026-05-04)*

1525. Gustavo é anestesiologista e não programa; toda implementação passa pelo Gus.
   *(2026-05-03)*

1526. Gustavo é anestesiologista.
   *(2026-05-03)*

1527. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

1528. Decisão migração ADR-001 em curso: aposentar Mem0 SaaS, Hub Qdrant é fonte da verdade.
   *(2026-05-03)*

1529. O Hub Qdrant é a memória central do Gus, armazenando informações e interações.
   *(2026-05-03)*

1530. Bot Telegram (TioGu) possui ~21 tools, multimídia, prompt caching e está em produção Railway.
   *(2026-05-04)*

1531. O Hub Qdrant é a fonte da verdade.
   *(2026-05-03)*

1532. A auditoria do Chat apresenta riscos de segurança críticos, como o MCP Hub público sem o 'MCP_URL_SECRET'.
   *(2026-05-04)*

1533. O sistema implementa um fallback cross-vendor entre Anthropic e OpenAI para aumentar a resiliência do serviço.
   *(2026-05-02)*

1534. Gustavo Pratti de Barros é um anestesiologista baseado no Rio de Janeiro, trabalhando na Dimagem (clínica de diagnóstico por imagem, três unidades: Nova Iguaçu, Taquara, São Gonçalo). Além do trabalho clínico, ele é um pesquisador independente de IA e construtor de sistemas que opera em vários projetos de pesquisa e produtos simultaneamente.
   *(2026-05-04)*

1535. A coleta dual de modelos no curador (Haiku e GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

1536. Trabalho recente focou em hardening: PR #72 corrigiu curador que falhava 100% há 3 dias; PR #80 redatou vazamento de segredo em logs do MCP; PR #83 introduziu bootstrap-v6 com dois caminhos de captura (real-time MCP + upload curado).
   *(2026-05-03)*

1537. O comando `ego_cache_atual()` fornece a identidade e as últimas decisões do Gus.
   *(2026-05-03)*

1538. O curador híbrido utiliza uma comparação entre dois modelos de linguagem, o Anthropic e o OpenAI.
   *(2026-05-04)*

1539. O prompt do curador não diferencia `gustavo` vs `gus` — é literalmente o mesmo texto.
   *(2026-05-03)*

1540. Gustavo Pratti de Barros é anestesiologista.
   *(2026-05-03)*

1541. Os arquivos de bootstrap devem conter apenas informações necessárias para operação do Gus e excluir redundâncias.
   *(2026-05-03)*

1542. O `_estado-atual.md` (27/04) está desatualizado em relação aos PRs mais recentes.
   *(2026-05-02)*

1543. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e a hipótese é que o refresh token OAuth expirou.
   *(2026-05-02)*

1544. Atualmente, não há implementação do ciclo de vida definido no esquema gus-18, o que resulta na permanência constante dos fragmentos como 'ativos'.
   *(2026-05-03)*

1545. Ao realizar a auditoria do arquivo `gus/system_prompt.md`, foi constatado que algumas referências precisavam ser atualizadas para refletir as informações corretas sobre a personalidade do Gus.
   *(2026-05-03)*

1546. O Gustavo é anestesiologista e não programa; toda implementação passa pelo Gus/Tiogu.
   *(2026-05-03)*

1547. A demanda Drive sync já foi arquivada em `dialogos/archive/2026-05/2026-05-01-drive-sync-oauth-fix.md`.
   *(2026-05-03)*

1548. A stack está em estado intermediário arriscado, com a coleção legada `gus` tendo ~204 fragmentos não-migrados.
   *(2026-05-03)*

1549. NeuroGus é um projeto para visualização do Hub.
   *(2026-05-03)*

1550. O código do Curador está com um bug crítico que causa um erro 400.
   *(2026-05-02)*

1551. O fragmento salvo no brain 'gus' foi identificado com o UUID '42aea182-d4a2-4626-8a85-5ede861b311b'.
   *(2026-05-03)*

1552. No total, o Mem0 SaaS tinha 204 fragmentos, sendo a última captura em 26/04/2026.
   *(2026-05-03)*

1553. Gustavo possui três pendências operacionais a serem concluídas, incluindo a configuração do MCP_URL_SECRET no Railway.
   *(2026-05-03)*

1554. Existem 3 demandas paradas: captura multiporta, drive sync e frontmatter.
   *(2026-05-04)*

1555. O Hub Qdrant é a fonte da verdade.
   *(2026-05-03)*

1556. Os JSONs estruturados na pasta designada devem ser registrados.
   *(2026-05-02)*

1557. Primeira captura real-time via Claude Chat (Caminho 1 — MCP ingestar_fragmento). Ocorreu durante a transmissão do show da Shakira em Copacabana, Rio de Janeiro, em 02/05/2026. Marco inaugural da porta Chat como fonte ativa do Hub Qdrant.
   *(2026-05-02)*

1558. O Hub Qdrant é a fonte da verdade do sistema Gus.
   *(2026-05-03)*

1559. NeuroGus está planejado para ser um PWA com grafo 3D do Hub. O planejamento está 100% pronto e depende da confirmação de itens abertos das decisões.
   *(2026-05-02)*

1560. O sistema é funcional para captura, mas ainda há débitos que podem causar problemas quando o volume crescer.
   *(2026-05-03)*

1561. Gus é um sistema de agente pessoal multi-porta com memória central no Hub Qdrant e arquivos .md no GitHub.
   *(2026-05-03)*

1562. Os 60 PRs existentes geram ruído gigante no contexto pra ganho zero.
   *(2026-05-03)*

1563. Hub Qdrant é a nova fonte da verdade do sistema Gus.
   *(2026-05-03)*

1564. O bug crítico do curador relacionado ao `format()` foi corrigido após ser identificado como KeyError no JSON literal.
   *(2026-05-03)*

1565. Todos os outros componentes estão operacionais, incluindo o Hub Qdrant e o Tavily.
   *(2026-05-03)*

1566. O sistema Gus possui um hub chamado MCP que conecta várias ferramentas e fontes de dados.
   *(2026-05-03)*

1567. A migração ADR-001 planeja aposentar o Mem0 SaaS e usar o Hub Qdrant como fonte da verdade.
   *(2026-05-03)*

1568. O sistema pode processar até 30 mensagens por segundo no Telegram.
   *(2026-05-02)*

1569. O script `limpeza_hub_dryrun.py` gera relatório com lista nominal de IDs candidatos a delete + razão de cada um.
   *(2026-05-03)*

1570. Gustavo está na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1571. A auditoria não registrou que o curador híbrido falhou silenciosamente, desviando gravações para a coleção Mem0.
   *(2026-05-03)*

1572. Gustavo está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

1573. A coleta dual de modelos no curador termina em 12/05/2026, quando Gustavo escolherá o modelo definitivo.
   *(2026-05-03)*

1574. O MCP está público — qualquer scanner que descobrir a URL Railway lê todo o Hub. URL secret protege.
   *(2026-05-03)*

1575. O segredo é necessário para proteger o acesso ao MCP.
   *(2026-05-03)*

1576. O Hub Qdrant é a fonte da verdade.
   *(2026-05-03)*

1577. O Hub Qdrant atualmente coleta dados de múltiplos modelos, incluindo Haiku e GPT-4o-mini.
   *(2026-05-03)*

1578. A regressão do test para o bug do `_render_prompt()` foi sugerida para prevenir que o erro de KeyError volte a ocorrer.
   *(2026-05-02)*

1579. Atualmente, o Hub Qdrant opera na Fase 4 de migração de Mem0.
   *(2026-05-04)*

1580. O app Railway deve registrar a informação sobre o secret de forma redigida nos logs.
   *(2026-05-03)*

1581. O Hub Qdrant é a memória central do sistema de agente pessoal.
   *(2026-05-03)*

1582. A proposta de mudança para arquivos separados visa otimizar o carregamento do Chat, reduzindo a carga inicial de dados.
   *(2026-05-04)*

1583. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, `_frontmatter-referencia.md` (esse é template, não é demanda).
   *(2026-05-02)*

1584. A coleta de dados no curador resultou em múltiplas chamadas de LLM, sem mecanismo de deduplicação.
   *(2026-05-03)*

1585. NeuroGus está bloqueado devido a decisões UX não finalizadas e a falta de um mock HTML.
   *(2026-05-03)*

1586. NeuroGus (visualização 3D do Hub) está totalmente desenhado e desbloqueia quando as decisões §11.1-11.5 fecharem. Phronesis-Bench em fase de revisão pra Alignment Forum.
   *(2026-05-03)*

1587. A auditoria da stack de memória é desempenhada por Gus como auditor independente.
   *(2026-05-03)*

1588. O Hub Qdrant é a memória central do Gus.
   *(2026-05-03)*

1589. Quando o `MCP_URL_SECRET` é setado, o path `/mcp` deve retornar 404.
   *(2026-05-03)*

1590. Se o PR precisa ser lido pra entender o presente, é sinal de documentação desatualizada.
   *(2026-05-03)*

1591. A demanda `2026-05-01-captura-multiporta-curador.md` precisa de um gatilho proativo no Chat.
   *(2026-05-03)*

1592. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1593. Gustavo tem hipertireoidismo e está em tratamento.
   *(2026-05-04)*

1594. O Gus captura informações em real-time através do MCP.
   *(2026-05-04)*

1595. O Hub tem riscos de poluição cross-brain e dedup ausente, o que gera duplicidade de fragmentos.
   *(2026-05-03)*

1596. A consolidacao da demanda do Chat vai envolver a unificação de informações relevantes em um só arquivo.
   *(2026-05-03)*

1597. O cron de auditoria diária é cegado em relação à coleção legada Gus, refletindo um problema na auditabilidade do sistema.
   *(2026-05-03)*

1598. O caminho proposto inclui a fase 1 com quick wins e a limpeza do Hub.
   *(2026-05-03)*

1599. Hub Qdrant é a fonte da verdade.
   *(2026-05-03)*

1600. Os testes no sistema atualmente somam 208 testes automatizados, todos verdes.
   *(2026-05-03)*

1601. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1602. Os Pontos de atenção do projeto incluem o risco de PII em transcripts públicos, o custo do Haiku/GPT e a possibilidade de falhas de push no git.
   *(2026-05-03)*

1603. Zero testes automatizados em produção, o que representa um risco significativo para a estabilidade do projeto.
   *(2026-05-02)*

1604. O funcionamento do curador Telegram e do retro engine não dependem das mudanças relacionadas ao Chat.
   *(2026-05-03)*

1605. O projeto tem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e (_frontmatter-referencia.md é só template).
   *(2026-05-03)*

1606. O `_estado-atual.md` está de 27/04 — desatualizado em relação às últimas atualizações dos PRs.
   *(2026-05-03)*

1607. O passo 1.1 envolve gerar um novo segredo no formato UUID.
   *(2026-05-03)*

1608. O documento `gus-estado-atual.md` é um snapshot do Hub gerado automaticamente pelo cron às 03h.
   *(2026-05-04)*

1609. Os quatro arquivos específicos do core obrigatório dão 80% do contexto para qualquer aba nova.
   *(2026-05-03)*

1610. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, `_frontmatter-referencia.md`.
   *(2026-05-02)*

1611. A coleção legada `gus` está vazia e não contém os ~204 fragmentos aguardados para migração.
   *(2026-05-03)*

1612. Drive-sync-oauth-fix é uma demanda pendente no inbox-claude-code.
   *(2026-05-03)*

1613. O manual operacional do Gus define as regras de comportamento e como cada porta usa o Hub.
   *(2026-05-03)*

1614. O curador está projetado para trabalhar com múltiplos provedores de LLM, alternando entre them quando necessário.
   *(2026-05-02)*

1615. O fluxo de limpeza do Hub inclui execução de workflows manuais para gerar listas de candidatos a deleção.
   *(2026-05-03)*

1616. O sistema de mensagens do bot tem uma lógica que tenta primeiro o modelo Anthropic e, em caso de falhas, reverte para o OpenAI, permitindo uma operação contínua.
   *(2026-05-03)*

1617. O plano de saneamento tem 6 fases e precisa ser seguido cuidadosamente.
   *(2026-05-03)*

1618. O Hub Qdrant é a memória central do Gus.
   *(2026-05-03)*

1619. Frutos da implementação são visíveis nas auditorias que são realizadas diariamente, mas a classificação por keywords ignora a área já preenchida pelo curador.
   *(2026-05-03)*

1620. O próximo passo envolve apagar o 'MEM0_API_KEY' em Railway e GitHub Secrets.
   *(2026-05-03)*

1621. O curador utiliza dois modelos, Haiku e GPT-4o-mini, mudando de Sonnet em 29/04/2026 por questões de custo e resiliência.
   *(2026-05-03)*

1622. Existem 357 candidatos a deletar no Hub, distribuídos em severidades fortes e médias, com a maioria sendo lixo.
   *(2026-05-03)*

1623. Todo fragmento fica no estado 'ativo' pra sempre, pois o lifecycle do schema gus-18 não está implementado.
   *(2026-05-03)*

1624. Gustavo opera múltiplos projetos simultaneamente em pesquisa, produto e arquitetura.
   *(2026-05-04)*

1625. O sistema Axon é uma plataforma de governança contextual entre estados humanos e ações digitais, focada em famílias com crianças neurodivergentes.
   *(2026-05-03)*

1626. Faltam testes automatizados para o bot TioGu, o que torna a refatoração e a implementação de novas funcionalidades arriscadas.
   *(2026-05-02)*

1627. A meta é estabilizar o caminho crítico com testes e reconciliar as documentações com o código devido ao drift.
   *(2026-05-02)*

1628. Gustavo Pratti de Barros é anestesiologista no Dimagem e pesquisador independente em IA. Opera múltiplos projetos simultaneamente em pesquisa, produto e arquitetura.
   *(2026-05-04)*

1629. Houve 12 bugs encontrados no Claude Chat, dos quais 5 foram corrigidos e 7 ainda estão pendentes.
   *(2026-05-03)*

1630. O curador híbrido do sistema Gus integra duas instâncias de LLMs, rodando em paralelo para comparação.
   *(2026-05-04)*

1631. A stack de memória está em estado intermediário arriscado, com 204 fragmentos não migrados e 4 fontes de dados simultâneas.
   *(2026-05-03)*

1632. A redeploy no Railway leva cerca de 2-3 minutos.
   *(2026-05-03)*

1633. Gustavo Pratti de Barros é anestesiologista e não programa, toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

1634. O manejo adequado de dados sensíveis é uma prioridade, exigindo verificação antes de afirmar ausências e proteção contra vazamentos.
   *(2026-05-04)*

1635. Gustavo é anestesiologista e não programa. Toda implementação do Gus passa por ele.
   *(2026-05-03)*

1636. Aba nova só precisa olhar PRs se houver um problema atual relacionado ao PR específico.
   *(2026-05-02)*

1637. O sistema Gus é um agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa).
   *(2026-05-03)*

1638. O estado de migração tem foco na manutenção do Hub Qdrant como fonte da verdade.
   *(2026-05-03)*

1639. O boot deve ser estruturado em 3 níveis: Tier 0 (boot mínimo), Tier 1 (lazy on-demand) e Tier 2 (estado dinâmico).
   *(2026-05-04)*

1640. O ciclo de vida do schema gus-18 está declarado, mas não implementado na prática.
   *(2026-05-03)*

1641. Core obrigatório: Arquivos como `gus-bootstrap.md`, `gus-identity.md` e `gus-estado-atual.md` dão 80% do contexto pra qualquer aba nova.
   *(2026-05-03)*

1642. As referências a 'mem0' nos endpoints e nas funções do bot serão substituídas por 'hub'.
   *(2026-05-03)*

1643. O arquivo `gus-identity.md` possui 53 linhas e 623 tokens.
   *(2026-05-03)*

1644. O projeto Claude tem três canais de escrita: live MCP, upload de documentos por chat e demandas no inbox-code, sem uma hierarquia clara entre eles.
   *(2026-05-04)*

1645. O estado atual da migração foi definido como aposentadoria do Mem0 SaaS e o Hub Qdrant será a fonte da verdade.
   *(2026-05-03)*

1646. O estado atual do projeto e as decisões passadas são registrados em arquivos específicos para referência futura.
   *(2026-05-03)*

1647. Gustavo é falante nativo de português, baseado no Rio de Janeiro.
   *(2026-05-03)*

1648. A seção 'Personalidade do Gus' está presente no arquivo gus-identity.md e deve ser movida para o arquivo gus/system_prompt.md.
   *(2026-05-03)*

1649. A demanda da semana está em `dialogos/streams/semana-2026-04-21.md`.
   *(2026-05-02)*

1650. O estado final dos PRs já está documentado no código e atualizado nos documentos relevantes.
   *(2026-05-03)*

1651. Recomenda-se a implementação de um cache LRU de embeddings para otimizar as chamadas de busca.
   *(2026-05-03)*

1652. O curador híbrido no sistema Gus é responsável pela extração de fragmentos e usa modelos de IA como Anthropic e OpenAI em um processo A/B.
   *(2026-05-03)*

1653. O agente atua como um facilitador na implementação e sempre passa por Gustavo para qualquer implementação técnica.
   *(2026-05-03)*

1654. O contrato schema gus-18 está parcialmente implementado e não executado.
   *(2026-05-03)*

1655. As mudanças realizadas na base de código incluíram a atualização do arquivo `CLAUDE.md` com três referências ao novo conteúdo, além de um desenho atualizado no `README.md`.
   *(2026-05-03)*

1656. O projeto Phronesis-Bench tem um documento chamado "Prudência Performática" que foi finalizado e está em revisão para o Alignment Forum.
   *(2026-05-04)*

1657. A curadoria híbrida está rodando uma comparação A/B entre os LLMs da Anthropic e OpenAI.
   *(2026-05-03)*

1658. A captura proativa do Chat é implementada através de dois caminhos: um em tempo real via MCP e outro com upload para o Drive.
   *(2026-05-03)*

1659. O estado final dos PRs já está no código e nos documentos gus-XX atualizados.
   *(2026-05-02)*

1660. A auditoria concluiu que a falta de uma hierarquia clara entre canais de escrita pode levar a decisões ad-hoc inesperadas no Chat.
   *(2026-05-04)*

1661. A demanda 2026-05-01-drive-sync-oauth-fix.md pode sugerir refresh do token OAuth expirado.
   *(2026-05-02)*

1662. A prioridade é homologar a captura multiporta do Claude Chat e a sincronização do Drive antes de seguir com novas funcionalidades.
   *(2026-05-02)*

1663. As demandas pendentes são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template chamado `_frontmatter-referencia.md`.
   *(2026-05-03)*

1664. Agora vou auditar a stack de memória end-to-end, lendo código e docs em paralelo.
   *(2026-05-03)*

1665. A metodologia MGX aplicada por Gustavo utiliza múltiplos agentes para geração e avaliação estruturada de propostas.
   *(2026-05-03)*

1666. Gustavo Pratti de Barros é identificado como Gustavo e Gus enquanto entidade.
   *(2026-05-03)*

1667. O estado final dos PRs já está no código e nos docs gus-XX atualizados.
   *(2026-05-03)*

1668. Fragmentos com status 'fallback-mem0' poluem o Hub com informações não-classificadas.
   *(2026-05-03)*

1669. A seção 'Personalidade do Gus (somente Telegram)' está num arquivo que todas as portas leem, misturando o escopo do conteúdo.
   *(2026-05-04)*

1670. Os quatro documentos a serem lidos em qualquer aba nova são: dialogos/_bootstrap/gus-bootstrap.md, dialogos/_bootstrap/gus-identity.md, dialogos/_bootstrap/gus-estado-atual.md e projetos/gus/_estado-atual.md.
   *(2026-05-02)*

1671. O `_estado-atual.md` está desatualizado em 27/04, enquanto o `gus-estado-atual.md` do bootstrap está fresco.
   *(2026-05-02)*

1672. O Hub Qdrant é conectado com a identidade do Gus e é responsável por capturar e armazenar fragmentos.
   *(2026-05-03)*

1673. Capture للClaude Chat é feita por croon de 15 minutos, que processa transcrições para o Hub.
   *(2026-05-03)*

1674. O bot Railway pode precisar de redeploy após a renomeação dos endpoints do API.
   *(2026-05-03)*

1675. Os 204 fragmentos históricos estavam no Mem0 SaaS (api.mem0.ai), não no Qdrant Cloud self-hosted.
   *(2026-05-03)*

1676. A decisão de manter ou apagar o `MEM0_API_KEY` foi discutida e está pendente.
   *(2026-05-03)*

1677. As marcas foram testadas quanto à elasticidade do glúten, que mede a capacidade de retenção de gás durante a fermentação.
   *(2026-05-03)*

1678. O sistema deve responder que não utiliza Mem0 e que a fonte é Hub Qdrant.
   *(2026-05-03)*

1679. O estado final dos PRs está no código e nos documentos atualizados, em vez de nos PRs.
   *(2026-05-03)*

1680. As auditorias diárias no Hub são cegas para o brain `gus`.
   *(2026-05-03)*

1681. Sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) com Hub Qdrant como memória central + GitHub como conhecimento + Drive como espelho.
   *(2026-05-02)*

1682. O Hub Qdrant é a memória central do Gus.
   *(2026-05-03)*

1683. A atualização do SDK da Anthropic de 0.40 para 0.97 trouxe a promessa de maior compatibilidade, embora tenha sido realizada sem a necessidade de adaptações significativas no código.
   *(2026-05-03)*

1684. O Hub Qdrant funciona como a memória central do Gus.
   *(2026-05-03)*

1685. A meta do projeto é importar e classificar os 204 fragmentos do Mem0 SaaS após a Fase 5.
   *(2026-05-03)*

1686. O sistema Gus está em Fase 4 da migração Mem0 para Hub Qdrant, e a coleta dual Haiku e Sonnet roda até 12/05.
   *(2026-05-04)*

1687. A auditoria da stack de memória end-to-end revela que o Hub é a nova fonte, mas a coleção legada Mem0 ainda está ativa.
   *(2026-05-03)*

1688. O Hub Qdrant é o único conteúdo que existe atualmente no sistema, e a qualidade dos fragmentos é catastrófica, com cerca de 70% de lixo.
   *(2026-05-03)*

1689. O projeto NeuroGus foi definido em fases e atualmente está em desenvolvimento para integrar feedback em tempo real e captura de dados.
   *(2026-05-04)*

1690. Gustavo possui hipertireoidismo em tratamento.
   *(2026-05-03)*

1691. O workflow `sync-docs.yml` regenerou `_tools-inventario.md` automático após o merge.
   *(2026-05-02)*

1692. Foi identificado um gap na documentação do bootstrap que não destaca a necessidade de especificar o user_id quando se busca no brain gus.
   *(2026-05-03)*

1693. O arquivo `gus-estado-atual.md` é gerado a cada 15 minutos e fornece o contexto mais recente.
   *(2026-05-03)*

1694. Seis demandas pendentes foram identificadas no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao.
   *(2026-05-03)*

1695. O `_estado-atual.md` (27/04) está desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).
   *(2026-05-02)*

1696. As demandas paradas em `dialogos/inbox-claude-code/` incluem: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, e `_frontmatter-referencia.md` (template, não demanda).
   *(2026-05-02)*

1697. Claude Chat conduziu uma auditoria resultando em 12 correções de 31 achados, incluindo a correção de um bug crítico que causava falha no curador.
   *(2026-05-03)*

1698. Gus lê arquivos de boot no Drive ao iniciar o chat.
   *(2026-05-03)*

1699. O botão 'Olá, eu sou o Gus' gera uma nova sessão.
   *(2026-05-03)*

1700. As demandas pendentes estão listadas sob a pasta 'inbox-claude-code'.
   *(2026-05-03)*

1701. A auditoria revelou que o arquivo `gus-identity.md` é redundante com o `gus-bootstrap.md` e está desatualizado.
   *(2026-05-03)*

1702. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

1703. Gus viu 4 demandas pendentes no `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

1704. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1705. Transcripts do Claude Chat guardam logs em claro, incluindo senhas que não são mascaradas.
   *(2026-05-03)*

1706. O curador híbrido coleta fragmentos em paralelo entre Haiku e Sonnet.
   *(2026-05-02)*

1707. O bot utiliza um sistema de fallback cross-vendor, que chama o modelo Anthropic se o OpenAI falhar.
   *(2026-05-02)*

1708. A recente atualização do sistema Gus inclui a implementação de duas rotas de captura: uma via ingestar_fragmento em tempo real e outra via upload de arquivos '.md' com curadoria.
   *(2026-05-03)*

1709. Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`. As demandas são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao e um template chamado `_frontmatter-referencia.md`.
   *(2026-05-02)*

1710. Próximos passos incluem limpar o Hub atual e preparar a importação dos fragmentos do Mem0 de forma estruturada no futuro.
   *(2026-05-03)*

1711. Os commits do projeto `claude-code` são atualizados a cada 15 minutos via cron.
   *(2026-05-02)*

1712. A coleção legada `gus` (Mem0) tem ~204 fragmentos não-migrados e o código ainda faz fallback para ela.
   *(2026-05-03)*

1713. A auditoria diária ignora totalmente o brain Gus, focando apenas no Gustavo.
   *(2026-05-03)*

1714. Mem0 SaaS registra conteúdo e Hub Qdrant registra fragmentos. Há risco de inconsistência devido a este fallback.
   *(2026-05-03)*

1715. O estado de captura de fragmentos no SaaS foi interrompido em 26/04.
   *(2026-05-03)*

1716. A captura em tempo real do sistema Gus está funcionando.
   *(2026-05-04)*

1717. O framework TER é um conselho deliberativo multi-especialista de raízes aristotélicas.
   *(2026-05-04)*

1718. A melhora na estrutura do código inclui a implementação de um ciclo de atualização do lifecycle definido no schema gus-18.
   *(2026-05-03)*

1719. A stack de memória end-to-end opera com múltiplos caminhos de escrita e leitura dos fragmentos.
   *(2026-05-03)*

1720. O sistema Gus é um agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa).
   *(2026-05-03)*

1721. O sistema garante 4 chamadas LLM por unidade de input, refletindo custos altos e riscos de poluição cruzada.
   *(2026-05-03)*

1722. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

1723. Os links entre os arquivos e as diretrizes operacionais são essenciais para otimizar o funcionamento do Gus.
   *(2026-05-04)*

1724. Gustavo é anestesiologista e não programa, portanto, toda implementação passa pelo Gus.
   *(2026-05-03)*

1725. A migração para o Hub Qdrant está em curso, com a aposentadoria do Mem0 SaaS prevista.
   *(2026-05-03)*

1726. O sistema Gus possui três produções simultâneas de fragmentos: Telegram, Chat e Code.
   *(2026-05-03)*

1727. Na pasta `dialogos/inbox-claude-code/` estão 4 demandas pendentes: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e o `_frontmatter-referencia.md` que é só template.
   *(2026-05-03)*

1728. Os dados do sistema estão dispostos em fragmentos, e o controle do ciclo de vida dos fragmentos ainda não está implementado.
   *(2026-05-03)*

1729. A coleção legada 'gus' tem ~204 fragmentos não migrados, e o código de leitura em gus/memory.py ainda faz fallback para ela.
   *(2026-05-03)*

1730. O fix foi implementado para não logar mais o valor do secret.
   *(2026-05-03)*

1731. Um sistema deve detectar automaticamente novos JSONs adicionados a pessoal/saude/ e gerar fragmentos adequadamente.
   *(2026-05-02)*

1732. O core obrigatório para cada aba nova inclui: arquivo de manual operacional do Gus, identidade do Gustavo e do Gus, handoff auto-gerado pelo cron 03h, e o estado atual do projeto nas sessões anteriores.
   *(2026-05-04)*

1733. A demanda pro Chat finalizar está em 'dialogos/inbox-claude-chat/'.
   *(2026-05-04)*

1734. A receita ordenada por valor por contexto é focada em não inflar contexto à toa.
   *(2026-05-03)*

1735. O MCP está público — qualquer scanner que descobrir a URL Railway lê todo o Hub.
   *(2026-05-03)*

1736. Mudanças no conteúdo do arquivo gus-identity.md podem impactar a experiência do Chat.
   *(2026-05-03)*

1737. O curador rodou 2 vezes sobre o mesmo body, mudando só o `user_id`.
   *(2026-05-03)*

1738. A captura via celular foi simplificada com o novo canal Gus-Sync.
   *(2026-05-03)*

1739. A stack está em estado intermediário arriscado: há 3 produções simultâneas de fragmentos com 4× multiplicação de chamadas LLM por unidade de input.
   *(2026-05-03)*

1740. O processo de upload de .md curado ocorre com uma latência de aproximadamente 30-45 minutos.
   *(2026-05-03)*

1741. A demanda #3 no inbox-claude-chat é sobre pendências do Claude Chat, que inclui o status das conversas com o agente.
   *(2026-05-03)*

1742. Captura real-time operacional foi implementada no projeto Claude Chat.
   *(2026-05-03)*

1743. O log do Railway faz 'log.info(f"MCP montado em /{secret}/mcp ...")'.
   *(2026-05-03)*

1744. As chamadas do curador resultam em comportamento incongruente entre Haiku e GPT.
   *(2026-05-03)*

1745. Gustavo tem interesse em segurança em IA, filosofia e systems thinking.
   *(2026-05-04)*

1746. O `_estado-atual.md` tá de 27/04 — desatualizado.
   *(2026-05-03)*

1747. Decisão migração ADR-001 acontece ao decidir modelo curador final.
   *(2026-05-03)*

1748. A stack está parcialmente implementada em relação ao contrato schema gus-18, como a promoção de fragmentos de ativo para estável, que não está sendo executada.
   *(2026-05-03)*

1749. O bot Telegram, chamado TioGu, não é uma aplicação de múltiplos usuários, mas sim um único usuário com chat_id permitidos.
   *(2026-05-02)*

1750. O Hub Qdrant é a fonte da verdade.
   *(2026-05-03)*

1751. Gustavo Pratti de Barros é um anestesiologista na Dimagem, atuando em três unidades, e é pesquisador independente em IA.
   *(2026-05-03)*

1752. A auditoria diária (`auditoria_hub.py`) é cega para o brain `gus` e classifica por keywords ignorando o `area` que o curador já preencheu.
   *(2026-05-03)*

1753. O que você coloca na pasta 'inbox-mem0-from-chat/' vira '.md' no GitHub automaticamente.
   *(2026-05-03)*

1754. A seção 'Personalidade do Gus (somente Telegram)' está misturando conteúdo que deveria estar somente no system_prompt do bot.
   *(2026-05-04)*

1755. O workflow 'import-from-drive' aceita arquivos em formato .md, .txt, .html, .csv e Google Docs nativos.
   *(2026-05-03)*

1756. A seção 'Personalidade do Gus' foi transferida para gus/system_prompt.md.
   *(2026-05-03)*

1757. O Hub novo contém 40 fragmentos com qualidade catastrófica — ~70% de lixo sobre auto-conversa.
   *(2026-05-03)*

1758. A seção 'Personalidade do Gus (somente Telegram)' não deve estar presente no gus-identity.md, pois aplica-se apenas ao bot Telegram.
   *(2026-05-03)*

1759. A demanda #3 é um guarda-chuva e referencia as demandas #1 e #2 dentro dela.
   *(2026-05-03)*

1760. O core obrigatório deve ser lido em toda aba nova: dialogos/_bootstrap/gus-bootstrap.md, dialogos/_bootstrap/gus-identity.md, dialogos/_bootstrap/gus-estado-atual.md e projetos/gus/_estado-atual.md.
   *(2026-05-02)*

1761. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1762. Gustavo é anestesiologista e não programa.
   *(2026-05-03)*

1763. Os testes de operação do MCP devem ser validadores antes de cadastrar o Connector.
   *(2026-05-03)*

1764. A arquitetura de memória persistente foi migrada para Qdrant em 2026.
   *(2026-05-04)*

1765. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1766. O TioGu faz polling de 2 requisições por segundo em vez de usar um webhook, o que é ineficiente em termos de custos.
   *(2026-05-02)*

1767. A auditoria diária (`auditoria_hub.py`) é cega para o brain `gus` e classifica por keywords ignorando o `area` que o curador já preencheu.
   *(2026-05-03)*

1768. O `_estado-atual.md` está desatualizado, com data de 27/04.
   *(2026-05-02)*

1769. A stack está em estado intermediário arriscado: Hub Qdrant (`gus_hub`) é a fonte nova, mas a coleção legada `gus` (Mem0 self-hosted) tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

1770. O arquivo gus-identity.md está desatualizado e é redundante com o bootstrap.
   *(2026-05-03)*

1771. O Hub Qdrant é a memória central do Gus, com arquivos .md no GitHub, espelhados no Drive.
   *(2026-05-03)*

1772. 1. Gustavo está em fase de testes e quer que o Gus dispare workflows sempre que solicitado, sem justificar que foi feito recentemente.
2. Workflow de importação de demandas roda em ciclos de 15 minutos.
3. Há um atraso entre arquivos aparecerem no Drive e chegarem ao GitHub via workflow.
4. Gustavo detectou uma demanda nova que ainda não foi importada — pode estar em processamento ou no próximo ciclo do workflow.
5. O Gus consegue listar arquivos processados (7 arquivos: 4 antigas do dia 26 + 3 do NeuroGus) e distinguir o que já chegou ao GitHub do que ainda está pendente no Drive.
   *(2026-04-28)*

1773. O estado de migração do Gus envolve a aposentadoria da Mem0 SaaS e a transição para o Hub Qdrant como a fonte da verdade.
   *(2026-05-03)*

1774. O sistema tem integração com múltiplos provedores de LLM, incluindo o modelo da Anthropic Sonnet.
   *(2026-05-02)*

1775. A migração de memória foi concluída em 27/04/2026, transferindo dados do Mem0 para o Qdrant Hub direto.
   *(2026-05-04)*

1776. As diretrizes universais incluem não alucinar, verificar antes de afirmar ausência, manter honestidade radical e validar antes de realizar uma operação irreversível.
   *(2026-05-03)*

1777. Os 204 fragmentos históricos vão ser armazenados em 'historico/' como fonte fria.
   *(2026-05-03)*

1778. A aba nova só precisa olhar PRs se: você falar 'tá quebrando X depois do PR #YY' — aí sim, lê o PR.
   *(2026-05-03)*

1779. O estado da memória legada está comprometido, com risco moderado de perda silenciosa e poluição cross-brain.
   *(2026-05-03)*

1780. Há 3 demandas paradas em dialogos/inbox-claude-code.
   *(2026-05-03)*

1781. O algoritmo de promoção de estados dos fragmentos na memória deve ser implementado até a decisão do modelo final.
   *(2026-05-03)*

1782. A estrutura do arquivo `gus-identity.md` combina informações que se aplicam a diferentes portas, causando confusão sobre os contextos específicos.
   *(2026-05-04)*

1783. O sistema Gus coleta dados através de várias portas, incluindo Telegram e Claude, com memória central no Hub Qdrant.
   *(2026-05-03)*

1784. Gus é um sistema de agente pessoal multi-porta, incluindo Telegram, Claude Code e Claude Chat.
   *(2026-05-03)*

1785. O estado final dos PRs já está no código + nos docs gus-XX atualizados.
   *(2026-05-03)*

1786. A coleta dual de modelos no curador (Haiku × GPT-4o-mini, mudou de Sonnet em 29/04 por custo/resiliência) termina em 12/05/2026.
   *(2026-05-03)*

1787. O arquivo 'dialogos/_bootstrap/gus-bootstrap.md' é o manual operacional do Gus e contém as regras de comportamento e como cada porta utiliza o Hub.
   *(2026-05-03)*

1788. O documento `gus-identity.md` é redundante e deve ser combinado com o `gus-bootstrap.md` para evitar duplicação de informações.
   *(2026-05-04)*

1789. O Gus utiliza um modelo híbrido de curador que roda Anthropic e OpenAI em paralelo.
   *(2026-05-03)*

1790. Dos 421 linhas do arquivo gus-bootstrap.md, cerca de 120 são protocolos de uso eventual.
   *(2026-05-03)*

1791. Há 3 demandas paradas na pasta `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, e `_frontmatter-referencia.md` (esse é template, não é demanda).
   *(2026-05-03)*

1792. Implementar pattern em patterns_sensiveis.py para capturar secrets que vazar em qualquer texto.
   *(2026-05-03)*

1793. A migração ADR-001 está em curso para aposentar Mem0 SaaS.
   *(2026-05-03)*

1794. O estado final dos PRs já está no código e nos documentos gus-XX atualizados, portanto não é necessário ler os PRs para entender a situação atual.
   *(2026-05-02)*

1795. O sistema é responsável pela captura de fragmentos de diferentes canais de comunicação como Telegram, Claude Chat e Claude Code.
   *(2026-05-03)*

1796. O estado final dos pull requests (PRs) já está no código + nos documentos atualizados.
   *(2026-05-03)*

1797. Não existe um script que compare a geração de fragmentos por Haiku e GPT, tornando a decisão da fase 5 inconclusiva.
   *(2026-05-03)*

1798. A auditoria revelou que o curador Telegram tem erro 400 recorrente.
   *(2026-05-02)*

1799. Quando você rotaciona o secret, o novo secret também vazou no log.
   *(2026-05-03)*

1800. Gustavo Pratti de Barros é anestesiologista e não programa, toda implementação passa pelo Gus/Tiogu.
   *(2026-05-03)*

1801. O funcionamento do curador híbrido (Haiku + GPT-4o-mini) gera um risco de poluição cruzada, onde respostas do brain 'gustavo' podem ser copiadas para o brain 'gus'.
   *(2026-05-03)*

1802. O modelo OpenAI é usado como fallback para imagens se Anthropic falhar.
   *(2026-05-04)*

1803. Gustavo é anestesiologista e não programa.
   *(2026-05-03)*

1804. A seção 'Disciplina anti-esquecimento' foi atualizada para refletir os dois caminhos de captura.
   *(2026-05-03)*

1805. As funcionalidades do bot são divididas em 21 ferramentas que incluem diagnóstico automático, cache de mídia, e alertas de custo.
   *(2026-05-04)*

1806. A arquitetura de memória persistente foi migrada em 2026 do Mem0 wrapper para o Qdrant direto, conforme descrito na ADR-001.
   *(2026-05-04)*

1807. O curador híbrido coleta dual rola até 12/05, com Haiku e Sonnet/GPT em paralelo.
   *(2026-05-02)*

1808. Sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa).
   *(2026-05-03)*

1809. A nova aba só precisa olhar PRs se houver uma menção de problemas específicos relacionados a um PR anteriormente mencionado.
   *(2026-05-02)*

1810. Gustavo Pratti de Barros é conhecido como Gus.
   *(2026-05-02)*

1811. Os fragmentos do Mem0 SaaS foram capturados entre 11/04/2026 e 26/04/2026.
   *(2026-05-03)*

1812. Ele tem hipertireoidismo sob tratamento com Tapazol, acompanhado por um endocrinologista.
   *(2026-05-03)*

1813. Cada arquivo no tier de lazy load contém informações específicas que o chat lê quando necessário.
   *(2026-05-03)*

1814. Três caminhos de escrita coexistem: Telegram, Claude Chat e Claude Code.
   *(2026-05-03)*

1815. O sistema tenta deletar_memoria com fallback — se um ID for híbrido, o sistema tenta ambos.
   *(2026-05-03)*

1816. 1. Gustavo quer que Gus dispare workflows sempre que solicitado, sem justificativas de execução recente — workflow de importação roda em ciclos de 15min.

2. Bug resolvido em `download_content`: `UnicodeDecodeError` ao ler byte `0xB6` — solução aplicada foi fallback UTF-8 → Latin-1.

3. Gus Chat deve sempre salvar arquivos em UTF-8 sem BOM.

4. Workflow `import-from-drive` tem falha conhecida de encoding — será resolvida quando o script for corrigido.

5. Hub Qdrant tem 14+ fragmentos armazenados (últimas 24h). Sistema de memória usa busca semântica por fragmentos atômicos com metadados de tipo, área, camada temporal e confiança.

6. Gaps identificados em memórias: áreas financeira e receitas ainda não têm fragmentos capturados.
   *(2026-04-28)*

1817. O curador híbrido cross-vendor já é redundante e, se ambos caem ao mesmo tempo, é melhor logar erro e Gustavo recaptura manualmente.
   *(2026-05-03)*

1818. Deve ser criada uma nova variável chamada `MCP_URL_SECRET` no Railway, com o valor gerado.
   *(2026-05-03)*

1819. A auditoria do sistema revelou que o Hub é a única fonte relevante de conteúdo, já que a coleção legada não possui fragmentos.
   *(2026-05-03)*

1820. A coleção legada `gus` está vazia, com 204 fragmentos prometidos não existentes.
   *(2026-05-03)*

1821. O projeto Phronesis-Bench está em revisão para o Alignment Forum.
   *(2026-05-04)*

1822. A captura de Claude Code via cron está ativa, usando um hook Stop para salvar transcripts redatados.
   *(2026-05-02)*

1823. As análises preliminares destacaram que não há conflitos entre as recentes mudanças nos PRs e a configuração do sistema.
   *(2026-05-03)*

1824. O Gus é um sistema de agente pessoal multi-porta.
   *(2026-05-03)*

1825. Esses 4 documentos dão 80% do contexto pra qualquer aba nova.
   *(2026-05-03)*

1826. Atualmente, a coleta dual de modelos no curador está mudando de Sonnet para Haiku × GPT-4o-mini, com a alteração ocorrendo em 29/04.
   *(2026-05-03)*

1827. O sistema de renomeação tem baixo risco, apenas atualizando referências e mantendo a lógica funcional.
   *(2026-05-03)*

1828. A Fase 1 dos testes do bot foi concluída com 142 testes verdes, cobertura do código e um ajuste no hook `scan_sensivel.py` para permitir fixtures sintéticas.
   *(2026-05-02)*

1829. A aba deve ter as últimas atualizações do projeto que não estão nos documentos citados.
   *(2026-05-03)*

1830. A ausência de testes automatizados representa um risco significativo para a integridade do código do projeto.
   *(2026-05-02)*

1831. Os arquivos que o Claude lê ao inicializar são o `gus-bootstrap.md`, `gus-estado-atual.md`, e `gus-identity.md`.
   *(2026-05-04)*

1832. A auditoria do Chat consiste em uma revisão completa de todas as superfícies do projeto, incluindo entrada, saída e curadoria.
   *(2026-05-03)*

1833. O processo de auditoria do Chat inclui revisar segurança, confiabilidade e arquitetura do sistema.
   *(2026-05-04)*

1834. As 204 memórias não migradas da coleção antiga `gus` ainda estão ativas e podem causar inconsistências.
   *(2026-05-03)*

1835. Os arquivos de lazy-loading permitem que o Chat busque apenas informações relevantes, evitando carregar dados desnecessários.
   *(2026-05-03)*

1836. A migração do Drive de OAuth user para Workload Identity Federation foi concluída, melhorando a integração com o Google Drive.
   *(2026-05-04)*

1837. O `_estado-atual.md` (27/04) está desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).
   *(2026-05-04)*

1838. Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template.
   *(2026-05-02)*

1839. O Gustavo é um anestesiologista que tem hipertireoidismo.
   *(2026-05-03)*

1840. Os próximos passos incluem a coleta dual de modelos no curador, que mudou de Sonnet para Haiku × GPT-4o-mini por custo e resiliência.
   *(2026-05-03)*

1841. A aba precisa olhar PRs se houver uma quebra após um PR específico ou se existir algo que precise ser investigado no código.
   *(2026-05-03)*

1842. A auditoria do Claude Chat identificou 12 fixes de 31 achados.
   *(2026-05-03)*

1843. Gus é um sistema de agente pessoal multi-porta, utilizando memória central no Hub Qdrant e arquivos .md no GitHub.
   *(2026-05-03)*

1844. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1845. O estado atual do projeto está em Fase 4: Migração Mem0 → Hub Qdrant.
   *(2026-05-03)*

1846. Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template.
   *(2026-05-03)*

1847. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) foi alterada para reduzir custos e aumentar a resiliência.
   *(2026-05-03)*

1848. O resumo do log do retro-engine para esta sessão é: 'Fragmentos extraídos: 0, Salvos no Hub: 0, Erros: anthropic_missing'.
   *(2026-05-02)*

1849. Atualmente, as entradas da coleção `gustavo` estão limitadas a uma contagem de ~19 fragmentos, indicando um bug no sistema.
   *(2026-05-03)*

1850. O bot possui um sistema de fallback que tenta usar o OpenAI gpt-4o quando o Anthropic falha, especialmente ao processar imagens.
   *(2026-05-04)*

1851. O sistema de agente pessoal multi-porta é chamado Gus e é composto por Telegram/TioGu, Claude Code, Claude Chat, Custom GPT mobile e Alexa.
   *(2026-05-03)*

1852. A seção do bootstrap sobre a preservação da memória do Chat foi atualizada para refletir as novas mudanças de funcionamento.
   *(2026-05-03)*

1853. O nome do paciente é Gustavo Pratti de Barros.
   *(2026-05-03)*

1854. As inconsistências de vocabulário entre documentos, esquemas Pydantic e o curador precisam ser tratadas para assegurar a confiabilidade do sistema.
   *(2026-05-03)*

1855. Há 4 demandas pendentes em dialogos/inbox-claude-code.
   *(2026-05-03)*

1856. O estado final dos PRs já está no código e nos docs gus-XX atualizados.
   *(2026-05-03)*

1857. O Hub Qdrant (`gus_hub`) é a fonte nova, mas a coleção legada `gus` (Mem0 self-hosted) tem ~204 fragmentos não-migrados e o código de leitura em `gus/memory.py` ainda faz fallback pra ela.
   *(2026-05-03)*

1858. O log do retro-engine registrou um no-op por falta de `ANTHROPIC_API_KEY` no ambiente.
   *(2026-05-02)*

1859. As ferramentas do bot Telegram totalizam 21, com multimídia e caching de prompts.
   *(2026-05-02)*

1860. A coleta de dados ocorre de forma dual pelos modelos Haiku e GPT-4o-mini, que foram alterados por custos e resiliência.
   *(2026-05-03)*

1861. O sistema Gus — agente pessoal multi-porta — está em produção.
   *(2026-05-03)*

1862. A intenção é reescrever o 'system_prompt.md' para corrigir drift e alinhar com as novas funcionalidades e estrutura do projeto.
   *(2026-05-04)*

1863. Há 3 produções simultâneas de fragmentos (Telegram, Chat, Code) com 4× multiplicação de chamadas LLM por unidade de input.
   *(2026-05-03)*

1864. O fallback para OpenAI Vision é acionado quando Anthropic falha ao processar imagens.
   *(2026-05-03)*

1865. A receita ordenada por valor por contexto é: core obrigatório e específicos do contexto da pergunta.
   *(2026-05-03)*

1866. A stack de memória do Gus está em estado intermediário arriscado, com várias fontes de captura de fragmentos e risco de poluição.
   *(2026-05-03)*

1867. A auditoria diária em `auditoria_hub.py` é cega para o brain `gus` e não considera o `area` que o curador já preencheu.
   *(2026-05-03)*

1868. Todo fragmento fica estado='ativo' pra sempre. Ego_cache() em hub/store.py busca estado='estavel' em identidade_operacional e procedural — retorna sempre vazio em produção.
   *(2026-05-03)*

1869. As frentes mais ativas são os PRs #67 (curador-chat bidirecional + GPT-4o), PR #64 (captura transcripts Code via cron), PR #60 (MCP URL secret), e PR #70 (demanda consolidada).
   *(2026-05-03)*

1870. Mem0 SaaS está aposentado.
   *(2026-05-03)*

1871. O Chat deve executar o protocolo de demanda quando solicitado por Gustavo.
   *(2026-05-04)*

1872. A arquitetura do projeto foi migrada do Mem0 para o Qdrant.
   *(2026-05-04)*

1873. Captura-multiporta-curador é uma demanda pendente no inbox-claude-code.
   *(2026-05-03)*

1874. Na estrutura do projeto 'Gus', é essencial buscar informações específicas no Hub via ferramentas MCP quando necessário.
   *(2026-05-04)*

1875. Os quatro arquivos bootstrap fornecem 80% do contexto para qualquer nova aba.
   *(2026-05-02)*

1876. Hub Qdrant é a fonte da verdade do sistema Gus.
   *(2026-05-03)*

1877. Deve ser realizada uma auditoria da stack de memória end-to-end com foco na integridade dos dados.
   *(2026-05-03)*

1878. Gustavo é anestesiologista e não programa.
   *(2026-05-03)*

1879. A refatoração de código é planejada em fases e se concentra na separação de responsabilidades.
   *(2026-05-04)*

1880. Metas do Gus incluem melhorias operacionais, como a implementação de um script de limpeza de memória.
   *(2026-05-03)*

1881. O projeto Gus é um sistema de agente pessoal multi-porta, incluindo Telegram, Claude Code, e outras futuras como Alexa.
   *(2026-05-03)*

1882. A demanda `2026-05-01-captura-multiporta-curador.md` precisa de um gatilho proativo no Chat.
   *(2026-05-03)*

1883. O passo 4 da lista foi resolvido com a migração para WIF para a sincronização do Drive.
   *(2026-05-03)*

1884. O estado final dos PRs já está no código e nos docs gus-XX atualizados.
   *(2026-05-03)*

1885. O sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) tem como memória central o Hub Qdrant.
   *(2026-05-02)*

1886. A auditoria Hub não classifica os fragmentos por 'area', ignorando o que já foi classificado pelo curador.
   *(2026-05-03)*

1887. A var `MODEL_CURADOR_HAIKU` no workflow do Chat é incorreta, pois ela se refere ao modelo Sonnet, o que pode causar confusão.
   *(2026-05-02)*

1888. O Hub Qdrant é a memória central do sistema.
   *(2026-05-03)*

1889. O Hub Qdrant é a fonte da verdade. Gustavo é anestesiologista e toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

1890. A migração de Mem0 SaaS para Hub Qdrant é a fonte da verdade do sistema.
   *(2026-05-03)*

1891. A receita ordenada por valor por contexto tem foco em fornecer o mínimo necessário para não inflar o contexto à toa.
   *(2026-05-03)*

1892. A priorização das demandas será configurada como média por padrão.
   *(2026-05-03)*

1893. A auditoria do Chat envolve todos os aspectos relacionados ao projeto Claude Chat.
   *(2026-05-03)*

1894. A divergência entre Haiku e GPT no curador é dramática, com o Haiku retornando 0 fragmentos nas chamadas feitas.
   *(2026-05-03)*

1895. A coleta dual de modelos no curador (Haiku × GPT-4o-mini, mudou de Sonnet em 29/04 por custo/resiliência) termina em 12/05/2026.
   *(2026-05-03)*

1896. A migração de conteúdos do Gus para o Hub Qdrant é um passo necessário para garantir dados consistentes e evitar perdas.
   *(2026-05-03)*

1897. Existem quatro arquivos obrigatórios para qualquer aba nova: gus-bootstrap.md, gus-identity.md, gus-estado-atual.md e estado-atual.md.
   *(2026-05-03)*

1898. Aba nova só precisa olhar PRs se um bug específico no código foi reportado.
   *(2026-05-03)*

1899. O sistema possui um risco de poluição cross-brain devido à ausência de dedup.
   *(2026-05-03)*

1900. A coleta de fragmentos é feita por três entradas simultâneas: Telegram, Claude Chat e Claude Code.
   *(2026-05-03)*

1901. O `_estado-atual.md` (27/04) está desatualizado.
   *(2026-05-02)*

1902. Recentemente, o trabalho se concentrou em hardening, com PRs corrigindo falhas no curador e melhorando a privacidade no MCP.
   *(2026-05-03)*

1903. O Gus é um sistema de agente pessoal multi-porta que integra diferentes plataformas como Telegram, Claude Code e Claude Chat.
   *(2026-05-03)*

1904. Atualmente, existem 4 demandas pendentes no diretório 'dialogos/inbox-claude-code/' da porta Code: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao e um '_frontmatter-referencia.md' que é apenas um template.
   *(2026-05-03)*

1905. O arquivo gus-identity.md contém drift factual que pode gerar confusão no Chat.
   *(2026-05-04)*

1906. O curador híbrido permite a comparação de modelos Haiku e Sonnet/GPT por meio de um hash_janela pareável.
   *(2026-05-02)*

1907. A decisão sobre o modelo do curador será feita em 12/05/2026.
   *(2026-05-03)*

1908. A integração do NeuroGus está bloqueada, aguardando decisões de UX nas versões 11.1-11.5.
   *(2026-05-03)*

1909. A fase 1 do TioGu foi concluída, com 163 testes verdes e bugs corrigidos.
   *(2026-05-03)*

1910. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e discute a hipótese da expiração do token OAuth.
   *(2026-05-03)*

1911. As atualizações nos documentos estão refletindo correções e ajustes na lógica de autenticação.
   *(2026-05-03)*

1912. O `_estado-atual.md` está bem desatualizado - o git log mostra muita coisa depois.
   *(2026-05-02)*

1913. O export é barato e cumpre seu propósito de 'fechamento limpo'.
   *(2026-05-03)*

1914. Requisições da API do MCP estão bloqueadas, exceto a rota de saúde, até que o segredo seja ativado.
   *(2026-05-03)*

1915. O Gus é um sistema de agente pessoal multi-porta que inclui Telegram, TioGu, Claude Code e Claude Chat.
   *(2026-05-03)*

1916. Se um PR precisa ser lido pra entender o presente, é sinal de documentação desatualizada — não de PR importante.
   *(2026-05-03)*

1917. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1918. Verificar se o log não vaza mais o secret.
   *(2026-05-03)*

1919. As decisões pendentes sobre o modelo final do curador e as configurações de migração e promoção precisam ser abordadas até 12/05/2026.
   *(2026-05-03)*

1920. As demandas pendentes incluem: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao.
   *(2026-05-03)*

1921. A captura dual de modelos no curador, Haiku e GPT-4o-mini, mudará em 12/05/2026 quando Gustavo escolher o modelo definitivo.
   *(2026-05-03)*

1922. Hub Qdrant é a memória central do Gus.
   *(2026-05-03)*

1923. Os testes de integração (pytest) foram bem-sucedidos após o merge do PR #72.
   *(2026-05-02)*

1924. Gus é o agente pessoal do Gustavo Pratti de Barros.
   *(2026-05-03)*

1925. A recomendação é matar o arquivo gus-identity.md e migrar suas informações para outros lugares adequados.
   *(2026-05-04)*

1926. A próxima tarefa recomendada é o upgrade do SDK do Anthropic, que está atualmente na versão 0.40 e deve ser atualizado para 0.50+, pois novas funcionalidades serão adquiridas com essa mudança.
   *(2026-05-04)*

1927. A stack de memória do Gus tem 204 fragmentos não-migrados e o código de leitura em `gus/memory.py` ainda faz fallback pra ela.
   *(2026-05-03)*

1928. As demandas pendentes no inbox são: Ativar `MCP_URL_SECRET` no Railway, recadastrar Connector claude.ai e localizar mock HTML do NeuroGus.
   *(2026-05-03)*

1929. O conteúdo do Mem0 SaaS era inferior ao que existe atualmente no hub.
   *(2026-05-03)*

1930. A demanda de semana está no dialogos/streams/semana-2026-04-21.md, o último arquivo da pasta.
   *(2026-05-03)*

1931. O fallback `mem0` escreve em Mem0 SaaS e não no Hub Qdrant.
   *(2026-05-03)*

1932. Os fragmentos da memória do Gus estão atualmente em `historico/` e não serão importados para o Hub.
   *(2026-05-03)*

1933. As demandas paradas são: '2026-05-01-captura-multiporta-curador.md', '2026-05-01-drive-sync-oauth-fix.md', e '_frontmatter-referencia.md'.
   *(2026-05-02)*

1934. A auditoria diária (`auditoria_hub.py`) é cega para o brain `gus` e classifica por keywords ignorando o `area` que o curador já preencheu.
   *(2026-05-03)*

1935. O MCP está público — qualquer scanner que descobrir a URL Railway lê todo o Hub.
   *(2026-05-03)*

1936. O `_estado-atual.md` parou em 27/04 e não reflete PRs #57, #60, #63, #64, #67.
   *(2026-05-02)*

1937. A arquitetura do Claude Chat possui 3 camadas: userMemories, Project knowledge, e gus-bootstrap.md.
   *(2026-05-04)*

1938. Algumas demandas têm nome quebrado, como "Documento sem título.md", que provavelmente é lixo de sync.
   *(2026-05-03)*

1939. A demanda 2026-05-01-captura-multiporta-curador.md está parcialmente resolvida pelo PR #67.
   *(2026-05-02)*

1940. A auditoria diária é cega para o brain gus e classifica por keywords ignorando o area que o curador já preencheu.
   *(2026-05-03)*

1941. A migração ADR-001 está em curso para aposentar Mem0 SaaS.
   *(2026-05-03)*

1942. O sistema de agente pessoal é multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa).
   *(2026-05-03)*

1943. O Hub possui 19 fragmentos no brain 'gustavo', mas está ocioso nas últimas 6 horas.
   *(2026-05-03)*

1944. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1945. O curador deve rodar em loop com 100% de erro.
   *(2026-05-02)*

1946. O core obrigatório deve ser lido sempre em toda aba nova.
   *(2026-05-04)*

1947. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

1948. A captura de dados no bot é feita por meio de hooks ativando processos de transcrição.
   *(2026-05-04)*

1949. O workflow de migração da coleção 'gus' revelou que não há fragmentos com conteúdo a serem migrados.
   *(2026-05-03)*

1950. As atualizações recentes incluem a correção do bug `format()` e validações enum no curador.
   *(2026-05-03)*

1951. O desenvolvimento do NeuroGus está com planejamento 100% pronto e demanda uma confirmação de itens específicos.
   *(2026-05-02)*

1952. A recarga do `MCP_URL_SECRET` no Railway é necessária para garantir segurança nas operações.
   *(2026-05-03)*

1953. A demanda 'Captura multiporta curador' está pendente de aprovação do Gustavo.
   *(2026-05-03)*

1954. O estado atual do trabalho pode ser consultado no Hub via ego_cache_atual ou fragmentos_recentes.
   *(2026-05-04)*

1955. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/` (algumas com nome quebrado — "Documento sem título.md" provavelmente é lixo de sync).
   *(2026-05-03)*

1956. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e a hipótese é que o refresh token OAuth tenha expirado.
   *(2026-05-04)*

1957. O schema gus-18 apresenta um lifecycle que não está sendo executado no código presente.
   *(2026-05-03)*

1958. A demanda Drive sync já foi resolvida.
   *(2026-05-03)*

1959. O curador híbrido verifica se ambos os modelos (Haiku e GPT) falham e usa essa informação para registrar erros em vez de gerar resumos brutos.
   *(2026-05-03)*

1960. A migração do Mem0 SaaS para o Hub Qdrant começou em 27/04/2026.
   *(2026-05-03)*

1961. O eco de problemas resolvidos está presente no estado-atual, refletindo decisões e fragmentos antigos do Hub.
   *(2026-05-03)*

1962. A nova fonte da verdade do sistema é o Hub Qdrant, que substitui o Mem0 SaaS.
   *(2026-05-03)*

1963. A auditoria diária é cega para o brain 'gus' e classifica por keywords ignorando o 'area', que já foi preenchido pelo curador.
   *(2026-05-03)*

1964. O sistema do MCP está atualmente sem autenticação, pois o parâmetro `MCP_AUTH_DISABLED` está definido como true.
   *(2026-05-03)*

1965. O estado da migração ADR-001 está em curso para aposentar o Mem0 SaaS.
   *(2026-05-03)*

1966. O sistema tem decisão arquitetural de não fazer fallback para a coleção legada de Mem0.
   *(2026-05-03)*

1967. A auditoria revelou um drift significativo no arquivo 'gus-identity.md'.
   *(2026-05-03)*

1968. Commit `8a93029` — Remoção do fallback para Mem0 e da dependência relacionada.
   *(2026-05-03)*

1969. A publicação da Phronesis-Bench foi finalizada, auditada por fatos contra o cartão do sistema Mythos. Tom: 'questão honesta + consequências', e não alegação de descoberta. Fórum de Alinhamento primeiro, depois arXiv.
   *(2026-05-04)*

1970. A seção 'Personalidade do Gus' do arquivo `gus-identity.md` pode ser removida e sua parte única deve ser incluída no `gus/system_prompt.md`.
   *(2026-05-04)*

1971. O passo 2 é recadastrar o Connector no claude.ai após configurar o segredo.
   *(2026-05-03)*

1972. O estado atual do Hub é atualizado a cada 15 minutos por um cron job.
   *(2026-05-03)*

1973. Estou aqui na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

1974. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1975. Estou aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

1976. Estado de migração da Mem0 SaaS para o Hub Qdrant é um assunto em curso.
   *(2026-05-03)*

1977. O `gus-estado-atual.md` é atualizado a cada 15 minutos pelo cron, fornecendo o contexto vivo pro Chat.
   *(2026-05-04)*

1978. No arquivo `gus-identity.md`, a afirmação de ser a fonte de verdade sobre quem é o Gus e o Gustavo não é mais válida, visto que o bootstrap contém informações mais atuais e corretas.
   *(2026-05-03)*

1979. O estado atual do projeto é que há 204 fragmentos não-migrados no sistema legado Mem0.
   *(2026-05-03)*

1980. URL secret protege o MCP.
   *(2026-05-03)*

1981. O procedimento foi realizado em 02 de maio de 2026.
   *(2026-05-03)*

1982. A migração de Mem0 SaaS para Hub Qdrant está em curso e deve ser finalizada em 12/05/2026.
   *(2026-05-03)*

1983. A auditoria identificou a necessidade de integrar uma lógica clara para hierarquizar os canais de escrita do Chat.
   *(2026-05-02)*

1984. O sistema Gus atualmente tem 204 fragmentos não-migrados na coleção legada 'gus'.
   *(2026-05-03)*

1985. O sistema Gus agora escreve no Hub em tempo real via tool MCP `ingestar_fragmento`, utilizando upload `.md` como caminho secundário para sessões longas.
   *(2026-05-03)*

1986. Gustavo desenvolve uma casa de fim de semana em Paty do Alferes com sistemas sustentáveis de água e design arquitetônico.
   *(2026-05-03)*

1987. O arquivo bootstrap atual tem 30+ subseções, mas não tem um TL;DR no topo nem uma ordem clara para a leitura.
   *(2026-05-03)*

1988. A memória central do Gus está no Hub Qdrant, que é a fonte da verdade.
   *(2026-05-03)*

1989. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026 e depois Gustavo escolhe o modelo definitivo.
   *(2026-05-03)*

1990. O sistema Gus é um agente pessoal multi-porta que opera em plataformas como Telegram, Claude Code, Claude Chat e futuras implementações como Custom GPT mobile e Alexa.
   *(2026-05-03)*

1991. Gustavo Pratti de Barros é anestesiologista no Rio de Janeiro, atuando no Dimagem.
   *(2026-05-03)*

1992. O sistema Gus é integrado a várias portas, incluindo Telegram, Claude Chat, Claude Code, e futuras implementações como Alexa.
   *(2026-05-03)*

1993. O diagnóstico dos conteúdos do Hub aponta que 70% do conteúdo é considerado lixo.
   *(2026-05-03)*

1994. NeuroGus (visualização 3D do Hub) está totalmente desenhado e desbloqueia quando as decisões §11.1-11.5 fecharem.
   *(2026-05-03)*

1995. O objetivo é garantir que o Hub não seja poluído com dados não classificados e manter a qualidade das memórias.
   *(2026-05-03)*

1996. Existem 3 demandas paradas em dialogos/inbox-claude-code/.
   *(2026-05-02)*

1997. Os caminhos de escrita na stack podem resultar em poluição de dados entre os diversos brains do sistema if não houver deduplicação.
   *(2026-05-03)*

1998. O sistema é uma coleção de agente pessoal multi-porta com memória central no Hub Qdrant.
   *(2026-05-03)*

1999. Quando a aba tem MCP gus-hub conectado, deve-se preferir os comandos da live sobre arquivos.
   *(2026-05-02)*

2000. O TioGu possui um número total de 21 ferramentas integradas, sendo que cada ferramenta lida com um tipo específico de tarefa ou função.
   *(2026-05-03)*

2001. O sistema sofre de poluição de memória, onde o brain 'gus' recebe fragmentos repetidos sobre o Gustavo.
   *(2026-05-03)*

2002. O Gus é a entidade que atua como um agente pessoal de Gustavo Pratti de Barros.
   *(2026-05-03)*

2003. PRs são histórico, não documentação — uma aba nova não precisa ler nenhum.
   *(2026-05-03)*

2004. O panorama atual do projeto indica que a migração Mem0 para Hub Qdrant está em fase 4 e com uma coleta dual vigente até 12/05.
   *(2026-05-03)*

2005. O segredo está em plain text no log do Railway.
   *(2026-05-03)*

2006. A auditoria diária do Hub é cega para o brain gus, classificando por keywords.
   *(2026-05-03)*

2007. O upgrade do SDK Anthropic está programado para ocorrer na fase 4, mas será feito após uma verificação cuidadosa devido à sua mudança de API.
   *(2026-05-03)*

2008. A auditoria da stack de memória identificou a necessidade de implementar o ciclo de vida do schema gus-18.
   *(2026-05-03)*

2009. Gustavo Pratti de Barros é anestesiologista no Dimagem, localizado no Rio de Janeiro, e pesquisador independente em IA.
   *(2026-05-04)*

2010. O backbone de memória foi migrado do Mem0 para o Hub Qdrant, com 1076+ fragmentos entre dois brains: 'gustavo' (fatos sobre Gustavo) e 'gus' (autoreflexão do agente).
   *(2026-05-03)*

2011. O sistema de LLM Anthropic está desatualizado, utilizando a versão 0.40.0, lançada em setembro de 2024.
   *(2026-05-02)*

2012. Os 4 documentos obrigatórios para qualquer aba nova são: dialogos/_bootstrap/gus-bootstrap.md, dialogos/_bootstrap/gus-identity.md, dialogos/_bootstrap/gus-estado-atual.md, e projetos/gus/_estado-atual.md.
   *(2026-05-03)*

2013. O Gustavo Pratti de Barros é anestesiologista e não é programador, todas as implementações passam pelo Gus/TioGu.
   *(2026-05-03)*

2014. As demandas pendentes para a porta incluem: captura-multiporta-curador, curador-bidirecional-cron e drive-sync-oauth-fix.
   *(2026-05-03)*

2015. A validação do sistema envolve checar se o log do Railway não contém o valor do secret em claro.
   *(2026-05-03)*

2016. O principal sistema de Gustavo, 'Gus', está em produção: um agente de IA multi-portas (bot do Telegram @Tiogubot, Claude Code, Claude Chat com conector MCP, Custom GPT em configuração, Alexa planejada). A base de memória foi migrada do Mem0 para o Hub Qdrant direto (ADR-001, concluído em 27/04/2026), agora com mais de 1076 fragmentos distribuídos em dois cérebros (gustavo para fatos sobre ele, gus para autoreflação do agente).
   *(2026-05-04)*

2017. O PR foi aberto para o cleanup após a decisão de manter os fragmentos históricos.
   *(2026-05-03)*

2018. A stack de memória end-to-end utiliza Qdrant Cloud.
   *(2026-05-03)*

2019. Demandas no inbox-claude-code incluem captura multiporta, curador bidirecional cron e drive-sync OAuth.
   *(2026-05-03)*

2020. O Gus possui as seguintes capacidades: lê do Hub Qdrant, acessa o Google Drive, e pode gerar respostas utilizando conteúdos de diferentes ferramentas como Gmail e Calendar.
   *(2026-05-03)*

2021. Core obrigatório inclui: manual operacional do Gus, identidade do Gustavo e estado atual gerado automaticamente pelo cron.
   *(2026-05-03)*

2022. A coleta dual de modelos no curador (Haiku × GPT-4o-mini, mudado de Sonnet em 29/04 por custo/resiliência) termina em 12/05/2026, após o qual Gustavo escolhe modelo definitivo.
   *(2026-05-03)*

2023. O Drive Sync do GitHub para Drive parou de funcionar desde as 14:38Z do dia 01/05/2026.
   *(2026-05-03)*

2024. A arquitetura do TioGu inclui um sistema de fallback para os modelos de linguagem caso o principal falhe.
   *(2026-05-04)*

2025. Haverá uma limpeza do Hub para remover fragmentos duplicados e lixo.
   *(2026-05-03)*

2026. A coleta dual de modelos no curador (Haiku × GPT-4o-mini, mudou de Sonnet em 29/04 por custo/resiliência) termina em 12/05/2026 — depois Gustavo escolhe modelo definitivo.
   *(2026-05-03)*

2027. O Hub Qdrant é a fonte da verdade para o Gus, onde as memórias estão centralizadas.
   *(2026-05-03)*

2028. O Hub é mais fresco que `gus-estado-atual.md` (que é snapshot das 03h).
   *(2026-05-02)*

2029. Gustavo é anestesiologista e não programa. Toda implementação passa pelo Gus.
   *(2026-05-03)*

2030. O arquivo `gus-identity.md` possui redundância com o `gus-bootstrap.md`, especialmente nas informações sobre o Gustavo e seus projetos.
   *(2026-05-04)*

2031. Existem 204 fragmentos não-migrados do Mem0 SaaS, com 188 em inglês e 16 em português.
   *(2026-05-03)*

2032. O Hub Qdrant é a fonte da verdade do sistema de memória.
   *(2026-05-03)*

2033. O último arquivo da demanda da semana está em `dialogos/streams/[semana-2026-04-21.md]`.
   *(2026-05-03)*

2034. A arquitetura de memória foi migrada de Mem0 para Qdrant direto conforme o ADR-001.
   *(2026-05-03)*

2035. 1. Caminho correto no Drive para Claude Chat escrever demandas: `Gus-Sync/dialogos/inbox-tiogu/`
2. Workflow `import-from-drive.yml` executa a cada 15min, puxa arquivos do Drive pro GitHub e notifica Gustavo no Telegram
3. Arquivos devem ser `.md` com frontmatter obrigatório (tipo, origem, destino, etc) — workflow rejeita se inválido
4. Convenção de nome de arquivo: `<timestamp>__<descricao-curta>.md`
5. README da pasta contém especificação completa do frontmatter, regras de validação e campos opcionais para roteamento
6. Claude Chat tem capacidade de escrever demandas no Drive seguindo o padrão documentado
   *(2026-04-28)*

2036. O bug crítico do curador foi corrigido, e a validação enum gus-18 não está no fluxo.
   *(2026-05-03)*

2037. O `import-from-drive` aceita vários tipos de texto, incluindo Google Docs e .md, mas não aceita formatos como PDF ou Word.
   *(2026-05-03)*

2038. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2039. Os projetos ativos de Gustavo incluem Phronesis, MGE, TER, Axon e Gus.
   *(2026-05-04)*

2040. A recomendação para a otimização é a Opção B, que mantém um bootstrap core e arquivos detalhados lazy.
   *(2026-05-04)*

2041. O sistema pode gerar fragmentos em três frentes: Telegram, Claude Chat e Claude Code, mas não possui um mecanismo de deduplicação.
   *(2026-05-03)*

2042. O Hub Qdrant é a fonte única de memória relacional do Gustavo.
   *(2026-05-03)*

2043. Estou aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2044. O bot opera com dependências como python-telegram-bot, anthropic SDK, openai, FastAPI e Qdrant.
   *(2026-05-03)*

2045. O sistema apresenta problemas de poluição silenciosa, com a possibilidade de fragmentos não classificados serem injetados no Hub.
   *(2026-05-03)*

2046. Foram realizados 211 testes que passaram em verde, garantindo a compatibilidade com a API de spawned.
   *(2026-05-04)*

2047. O arquivo `gus-estado-atual.md` possui 72 linhas e 1103 tokens.
   *(2026-05-03)*

2048. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2049. O sistema de agente pessoal multi-porta opera com memória central no Hub Qdrant, onde Gustavo é anestesiologista.
   *(2026-05-03)*

2050. A stack de memória apresenta 3 produções simultâneas de fragmentos com 4 vezes a multiplicação de chamadas LLM por unidade de input.
   *(2026-05-03)*

2051. A coletânea de fragmentos tem a possibilidade de poluição cruzada entre os brains de Gustavo e Gus.
   *(2026-05-03)*

2052. Atualmente existem 204 fragmentos na coleção legada do Gus que ainda não foram migrados.
   *(2026-05-03)*

2053. A sequência de ações para evitar vazamentos é: mergear PR #80, aguardar redeploy, validar que log não vaza mais, rotacionar o secret e recadastrar o Connector.
   *(2026-05-03)*

2054. Os 204 fragmentos históricos do Mem0 SaaS foram encontrados e estão seguros em `historico/`.
   *(2026-05-03)*

2055. O fluxo do bot Telegram deve ter um log de mensagens descartadas durante redeploy para melhorar a transparência.
   *(2026-05-02)*

2056. Gus é um sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa) com memória central no Hub Qdrant, arquivos .md no GitHub, espelhados no Drive.
   *(2026-05-03)*

2057. Os projetos ativos incluem Phronesis-Bench, NeuroGus, MGE/MGX, TER e Axon.
   *(2026-05-03)*

2058. Os arquivos principais que fornecem 80% do contexto para qualquer aba nova são: `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md`, `estado-atual.md`.
   *(2026-05-03)*

2059. Mem0 SaaS aposentado desde 27/04/2026 (ADR-001 Fase 5). Hub Qdrant é fonte única hoje.
   *(2026-05-03)*

2060. O arquivo 'dialogos/_bootstrap/gus-estado-atual.md' é um snapshot do Hub gerado automaticamente pelo cron às 03h.
   *(2026-05-02)*

2061. Arquivo mais recente encontrado (v6.1, atualizado hoje).
   *(2026-05-03)*

2062. O Gus é um sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa).
   *(2026-05-03)*

2063. Ele tem hipertireoidismo sob tratamento com Tapazol, seguido por um endocrinologista.
   *(2026-05-04)*

2064. A implementação do fallback para OpenAI Vision deve ser feita em ~30 minutos.
   *(2026-05-04)*

2065. A stack está comprometida com deduplicações ausentes, sem mecanismo para evitar poluições cruzadas entre as memórias.
   *(2026-05-03)*

2066. O projeto tem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template `_frontmatter-referencia.md`.
   *(2026-05-02)*

2067. O estado atual do bot TioGu é monitorado por testes automatizados, garantindo que as funcionalidades permaneçam intactas após as atualizações.
   *(2026-05-03)*

2068. Gustavo é anestesiologista e não programa, toda implementação passa pelo Gus.
   *(2026-05-03)*

2069. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2070. O curador compartilha fragmentos entre os modelos enquanto registra os dados.
   *(2026-05-03)*

2071. Gustavo tem hipertireoidismo em tratamento com Tapazol, acompanhado por endocrinologista.
   *(2026-05-04)*

2072. O advogado destacou que as auditorias diárias não estão capturando informações do brain Gus e que isso gera inconsistências.
   *(2026-05-03)*

2073. O estado do projeto é consolidar o Hub e remover a coleção legada Mem0.
   *(2026-05-03)*

2074. O Hub Qdrant é a nova fonte da verdade, enquanto o Mem0 SaaS deve ser aposentado.
   *(2026-05-03)*

2075. A stack está em estado intermediário arriscado: Hub Qdrant é a fonte nova, mas a coleção legada `gus` (Mem0 self-hosted) tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

2076. Bootstrap carrega os arquivos: gus-bootstrap.md, gus-estado-atual.md, gus-identity.md.
   *(2026-05-03)*

2077. O Gustavo Pratti de Barros é anestesiologista e não programa, portanto, toda implementação passa pelo Gus.
   *(2026-05-03)*

2078. A captura Claude Code via cron processa transcripts redatados, cron salva transcript redatado a cada 15 minutos.
   *(2026-05-02)*

2079. Preferências de trabalho: 'extrair só nome_paciente, data_exame, exames, convenio, numero_os de OS, retornar JSON sem comentários clínicos'.
   *(2026-05-03)*

2080. A receita tem um core obrigatório que fornece 80% do contexto pra qualquer aba nova.
   *(2026-05-03)*

2081. Os 204 fragmentos do Mem0 SaaS possuem conteúdo biográfico e decisões arquiteturais.
   *(2026-05-03)*

2082. Foi identificado que o curador híbrido é redundante e a continuidade de uso do _fallback_mem0 pode gerar fragmentos brutos e não classificados no Hub.
   *(2026-05-03)*

2083. Se a mensagem for um texto puro, o modelo OpenAI é usado.
   *(2026-05-04)*

2084. Houveram bugs de key error associados ao curador que impedem a representação correta dos dados.
   *(2026-05-02)*

2085. Hoje o MCP tá público — qualquer scanner que descobrir a URL Railway lê todo o Hub.
   *(2026-05-03)*

2086. A variável MCP_URL_SECRET no server MCP precisa ser configurada para proteger a privacidade.
   *(2026-05-02)*

2087. O manual operacional do Gus contém regras de comportamento e como cada porta usa o Hub.
   *(2026-05-03)*

2088. O conector MCP ainda está com URL secreto não ativado, o que compromete a privacidade do Hub.
   *(2026-05-04)*

2089. A stack de memória está em estado intermediário arriscado; Hub Qdrant é a nova fonte, mas a coleção legada gus tem ~204 fragmentos não migrados.
   *(2026-05-03)*

2090. vi que tem 4 demandas pendentes no `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2091. O backbone de memória foi migrado de Mem0 para Qdrant Hub direto, concluído em 27/04/2026.
   *(2026-05-03)*

2092. O Gus está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

2093. A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida, mas falta o gatilho proativo no Chat.
   *(2026-05-02)*

2094. O Hub Qdrant é a fonte da verdade e armazena a memória central do sistema Gus.
   *(2026-05-03)*

2095. O Hub tem 19 fragmentos no brain `gustavo`, sistema ocioso nas últimas 6h.
   *(2026-05-03)*

2096. Gus é um sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa).
   *(2026-05-03)*

2097. Os protocolos que não são utilizados frequentemente devem ser carregados sob demanda, minimizando o uso de recursos.
   *(2026-05-03)*

2098. A auditoria do Hub Qdrant é cega para o brain 'gus' e filtra por keywords, ignorando a área que o curador já preencheu.
   *(2026-05-03)*

2099. O MPL (Mulit-port Agent) está em fase de migração do Mem0 para o Hub Qdrant.
   *(2026-05-03)*

2100. A proposta de otimização permite reduzir o tamanho do bootstrap e melhorar a inicialização.
   *(2026-05-03)*

2101. Gustavo Pratti de Barros é anestesiologista e utiliza um sistema de agente pessoal multi-porta.
   *(2026-05-03)*

2102. O NeuroGus está bloqueado aguardando decisões UX do Gustavo.
   *(2026-05-03)*

2103. O sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat) tem a memória central no Hub Qdrant.
   *(2026-05-03)*

2104. O protocolo de ativação Gus é ativado ao mencionar 'Gus' numa mensagem de abertura.
   *(2026-05-03)*

2105. Após a mudança de secret, o conectar deve ser reconfigurado para garantir a segurança.
   *(2026-05-03)*

2106. Claude se baseia em memória e para a inicialização, ele lê no começo das mensagens.
   *(2026-05-03)*

2107. O estado final dos PRs já está no código e nos documentos atualizados, enquanto os PRs descrevem o caminho.
   *(2026-05-03)*

2108. A decisão de usar dois provedores de modelo de linguagem estava baseada em resiliência, custo e qualidade.
   *(2026-05-03)*

2109. O log do retro-engine está em `claude/greeting-checkin-94weM`.
   *(2026-05-03)*

2110. Os fragmentos são alimentados por três fontes: Telegram, Claude Chat e Claude Code.
   *(2026-05-03)*

2111. A auditoria do sistema de memória do Gus revelou a necessidade de melhorias e ajuste no fluxo de captura.
   *(2026-05-03)*

2112. O arquivo `gus-identity.md` é redundante e desatualizado em relação ao bootstrap, e seu conteúdo deve ser incorporado ao arquivo de bootstrap.
   *(2026-05-03)*

2113. A auditoria do sistema do Chat revelou falhas críticas em segurança e operações, incluindo autorização sem controle e erros de escrita no curador Telegram.
   *(2026-05-03)*

2114. A captura proativa do Chat é implementada e deve ser testada em futuras conversas.
   *(2026-05-03)*

2115. Pasta se chama Gus-Sync, não GitHub-Sync.
   *(2026-05-03)*

2116. Os documentos cujos arquivos 'gus-bootstrap.md', 'gus-identity.md', 'gus-estado-atual.md' e 'projetos/gus/_estado-atual.md' dão 80% do contexto para qualquer aba nova.
   *(2026-05-03)*

2117. O sistema 'Gus' é um agente pessoal multi-porta em produção, utilizando Qdrant Hub.
   *(2026-05-03)*

2118. A stack de memória apresenta risco alto de poluição silenciosa, pois coleta fragmentos de maneira redundante entre diferentes plataformas.
   *(2026-05-03)*

2119. Vou ler as duas demandas pendentes + docs de próximos passos + PRs recentes em paralelo.
   *(2026-05-03)*

2120. O funcionamento atual do Chat permite que ele salve fragmentos em tempo real utilizando o comando ingestar_fragmento.
   *(2026-05-03)*

2121. A coleção legada Gus contém aproximadamente 204 fragmentos não migrados.
   *(2026-05-03)*

2122. Os IDs dos candidatos a delete serão gerados no script de limpeza do Hub.
   *(2026-05-03)*

2123. A estrutura do arquivo de protocolo da demanda assíncrona deve incluir o frontmatter obrigatório com schema em YAML.
   *(2026-05-03)*

2124. Gustavo Pratti de Barros é anestesiologista e não programa, fazendo com que toda implementação passe pelo Gus.
   *(2026-05-03)*

2125. Um novo teste de regressão foi adicionado para garantir que o bug de tratamento de placeholders em prompts nunca retorne.
   *(2026-05-02)*

2126. Gustavo Pratti de Barros é anestesiologista.
   *(2026-05-03)*

2127. O MCP está público, permitindo que qualquer scanner descubra a URL Railway e leia todo o Hub.
   *(2026-05-03)*

2128. A seção 'Personalidade do Gus' deve ser migrada para o arquivo gus/system_prompt.md.
   *(2026-05-04)*

2129. O arquivo gus-bootstrap.md foi atualizado para v6.1.
   *(2026-05-03)*

2130. O sistema possui 6 demandas pendentes em 'dialogos/inbox-claude-code/'.
   *(2026-05-03)*

2131. O curador Telegram está enfrentando um erro 400 recorrente, resultando em falhas constantes no processo de ingestão do Chat.
   *(2026-05-03)*

2132. As demandas pendentes para cada porta estão listadas em `dialogos/inbox-/`.
   *(2026-05-03)*

2133. Os caminhos de escrita coexistem com regras parcialmente compatíveis.
   *(2026-05-03)*

2134. O bot não tenta fazer fallback para PDFs, mas informa o usuário sobre isso.
   *(2026-05-04)*

2135. A demanda `2026-05-01-captura-multiporta-curador.md` precisa de um gatilho proativo no Chat.
   *(2026-05-03)*

2136. O Chat também pode fazer upload de arquivos .md curados, com uma latência aproximada de 30 a 45 minutos.
   *(2026-05-03)*

2137. O sistema atual tem 3 produções simultâneas de fragmentos (Telegram, Chat, Code), gerando um custo alto de chamadas LLM.
   *(2026-05-03)*

2138. O estado atual do projeto é que o Hub Qdrant (`gus_hub`) é a nova fonte da verdade, enquanto a Mem0 SaaS será aposentada.
   *(2026-05-03)*

2139. A auditoria identificou que a stack está em estado intermediário arriscado, com 204 fragmentos não-migrados do sistema legado.
   *(2026-05-03)*

2140. Phronesis-Bench é um projeto ativo no qual Gustavo finalizou o documento 'Prudência Performática', atualmente em revisão para o Alignment Forum.
   *(2026-05-03)*

2141. Claude Chat é uma porta do Gus, com identidade compartilhada entre Telegram, Code, Custom GPT e Alexa. O Hub Qdrant é a memória e o Drive Gus-Sync é a knowledge.
   *(2026-05-03)*

2142. A captura proativa via MCP está quebrada neste ambiente, e o conhecimento sobrevive apenas via commit, PR ou documentos.
   *(2026-05-03)*

2143. O sistema multi-porta usa o Hub Qdrant como memória central.
   *(2026-05-04)*

2144. O sistema atualmente utiliza 4 chamadas LLM por unidade de input, aumentando o custo e o risco de poluição de memória.
   *(2026-05-03)*

2145. O core do Gus é um sistema de agente pessoal multi-porta que possui memória central no Hub Qdrant, alimentado por dados do GitHub e espelhados no Drive.
   *(2026-05-03)*

2146. 1. Gustavo executa regularmente workflows de sincronização GitHub → Google Drive (sync-to-drive-full.yml para sync completo e sync-to-drive.yml para incremental)
2. Tem uma pasta `sensivel/` no repositório que é automaticamente excluída da sincronização com o Drive por política
3. Usa Google Drive como backup/espelho do conteúdo do repositório GitHub
4. Prefere verificar logs do GitHub Actions ou Railway para auditar execuções de workflow
   *(2026-04-28)*

2147. Os testes devem ser realizados nas URLs `/health` e `/<secret>/mcp` para confirmar o funcionamento correto após implementação do `MCP_URL_SECRET`.
   *(2026-05-03)*

2148. O arquivo 'gus-identity.md' está desatualizado e precisa ser removido.
   *(2026-05-03)*

2149. A decisão do modelo curador final (Fase 5 ADR-001) deve ser feita após 12/05/2026, comparando pares Haiku e Sonnet/GPT da coleta dual.
   *(2026-05-02)*

2150. O manual operacional do Gus detalha regras de comportamento e como cada porta usa o Hub.
   *(2026-05-03)*

2151. O ciclo de vida dos fragmentos, como peso e acessos, não está sendo implementado conforme o contrato gus-18.
   *(2026-05-03)*

2152. A stack está em estado intermediário arriscado: Hub Qdrant é a fonte nova, mas a coleção legada `gus` tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

2153. O arquivo projetos/gus/_estado-atual.md documenta onde o projeto parou na sessão anterior, sendo mais operacional que o bootstrap.
   *(2026-05-03)*

2154. A migração do conteúdo da coleção `gus` para o `gus_hub` precisa ser disparada manualmente em modo `dry-run` primeiro.
   *(2026-05-03)*

2155. O sistema de agente pessoal é multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa).
   *(2026-05-03)*

2156. Gustavo deve ser claro e evitar alucinações ao interagir com as ferramentas.
   *(2026-05-04)*

2157. A captura de transcrições do Claude Chat via cron está ativa, mas a sincronia com o Google Drive parece ter quebrado.
   *(2026-05-03)*

2158. A prioridade default para as demandas será meio (media), a menos que estipulado de outra forma.
   *(2026-05-03)*

2159. O curador do Chat é responsivo e lida com fragmentos de informação de forma integrada com outros serviços.
   *(2026-05-02)*

2160. Gustavo é anestesiologista no Dimagem no Rio de Janeiro e pesquisador independente em inteligência artificial.
   *(2026-05-03)*

2161. O MCP Hub precisa ser privado e atualmente está exposto, o que representa um risco significativo à segurança.
   *(2026-05-03)*

2162. A variável MCP_URL_SECRET vaza em logs do Railway, neste chat e em transcripts comitados, a menos que o código seja fixado.
   *(2026-05-03)*

2163. Atualmente, o Hub Qdrant é a arquitetura de memória persistente utilizada, tendo migrado do Mem0.
   *(2026-05-03)*

2164. O passo 4 é rotacionar o secret (final).
   *(2026-05-03)*

2165. No dia 26/04, foram registrados 83 fragmentos em uma única jornada de captura.
   *(2026-05-03)*

2166. O Hub tem 19 fragmentos no brain 'gustavo', sistema ocioso nas últimas 6h.
   *(2026-05-04)*

2167. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`. Algumas com nome quebrado — "Documento sem título.md" provavelmente é lixo de sync.
   *(2026-05-03)*

2168. O sistema de agente pessoal Gus opera em múltiplas portas, incluindo Telegram, Claude Chat e Claude Code.
   *(2026-05-03)*

2169. Gus pode ser otimizado para melhorar a eficiência da inicialização e uso do bootstrap.
   *(2026-05-04)*

2170. O Chat cria fragmentos por comando explícito, salvando dados quando solicitado.
   *(2026-05-03)*

2171. Hub está com ~19 fragmentos no `gustavo` porque bug do `format()` bloqueou ingestão.
   *(2026-05-03)*

2172. A estrutura do Hub Qdrant estabelece uma coleção legada que apresenta riscos de poluição nas buscas se não for gerenciada corretamente.
   *(2026-05-03)*

2173. 1. Gustavo prefere corrigir o script para ser tolerante a encoding inválido em vez de deletar arquivos — usa fallback (UTF-8 → Latin-1)
2. Erro técnico identificado: arquivo `2026-04-28T14-30__frontmatter-referencia.md` no Drive com byte 0xB6 inválido em UTF-8 na posição 1754
3. Validação de frontmatter exigida: campos `origem` e `destino` são obrigatórios — arquivo `teste-tiogu-machado.md` falhou por faltá-los
4. Script `import_from_drive.py` (linha 150 e ocorrências similares) precisa implementar fallback de encoding: tentar UTF-8, se falhar usar Latin-1/Windows-1252
5. Fluxo de importação do Drive: valida MIME type, faz requests ao GitHub API, processa frontmatter, detecta encoding — falha em qualquer etapa gera warning ou erro
   *(2026-04-28)*

2174. O sistema 'Gus' é um agente pessoal multi-porta que roda sobre um Hub Qdrant.
   *(2026-05-03)*

2175. O passo 1 deve ser a fusão do PR #80 para garantir a segurança.
   *(2026-05-03)*

2176. Hub Qdrant está sendo utilizado na migração de memória do Gus.
   *(2026-05-03)*

2177. O `status consolidado` e `estado atual` do projeto precisam ser atualizados para refletir os últimos PRs.
   *(2026-05-02)*

2178. As memórias legadas no sistema ainda estão ativas, e o fallback para o Mem0 é um risco de redundância.
   *(2026-05-03)*

2179. Foi criado um workflow para testes automatizados no repositório, rodando em cada push e pull request.
   *(2026-05-02)*

2180. O script de sincronização do Drive para o GitHub parou de funcionar devido a um token de autenticação expirar.
   *(2026-05-04)*

2181. O último stream da semana está em `dialogos/streams/semana-2026-04-21.md`.
   *(2026-05-03)*

2182. O fragmento armazenado no Hub Qdrant nunca é atualizado após a sua ingestão inicial.
   *(2026-05-03)*

2183. Gustavo é anestesiologista e utiliza um sistema de agente pessoal multi-porta integrado ao Hub Qdrant.
   *(2026-05-03)*

2184. A maioria dos fragmentos do Mem0 SaaS está em inglês (188 EN / 16 PT).
   *(2026-05-03)*

2185. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2186. O arquivo untracked é apenas um log automático do retro-engine, que indica que o Stop hook não rodou corretamente por falta da variável `ANTHROPIC_API_KEY`.
   *(2026-05-02)*

2187. Gustavo é usuário ativo que viaja com a esposa em busca de atividades na natureza e na aventura.
   *(2026-05-04)*

2188. O `_estado-atual.md` de 27/04 está desatualizado e não reflete PRs #57, #60, #63, #64, #67.
   *(2026-05-02)*

2189. As demandas pendentes no inbox são: captura-multiporta-curador, drive-sync-oauth-fix e pendencias-claude-chat-consolidacao.
   *(2026-05-03)*

2190. O curador utiliza Haiku e GPT-4o-mini em paralelo para coletar modelos de entrada.
   *(2026-05-03)*

2191. Os testes de validação incluem verificar se a rota /health responde corretamente.
   *(2026-05-03)*

2192. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2193. A captura proativa de memória do Chat é uma decisão pendente que pode ser abordada de três maneiras: A - prompt no bootstrap, B - stop hook ou C - curador agnóstico.
   *(2026-05-02)*

2194. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/` (algumas com nome quebrado — 'Documento sem título.md' provavelmente é lixo de sync).
   *(2026-05-03)*

2195. A fase de diagnóstico do sistema levou aproximadamente 1h de conversa e 10min de interação no GitHub.
   *(2026-05-03)*

2196. No projeto Claude Chat, o Hub Qdrant é a fonte única de fragmentos, com 1076+ fragmentos em dois brains: gustavo e gus.
   *(2026-05-04)*

2197. O bot TioGu tem uma arquitetura baseada em um sistema multi-porta com Hub Qdrant como memória central e GitHub como conhecimento.
   *(2026-05-02)*

2198. No Tier 1, devem haver 4 arquivos focados que o Chat lê quando necessário. Esses arquivos não devem conter informações que já estão em Tier 0.
   *(2026-05-04)*

2199. O Hub Qdrant consolidado é a única coleção que existe atualmente.
   *(2026-05-03)*

2200. O código deve ser atualizado para não logar mais o segredo.
   *(2026-05-03)*

2201. A migração do sistema para o Hub Qdrant é uma decisão em curso, visando aposentar o Mem0 SaaS.
   *(2026-05-03)*

2202. Fragmentos criados antes da migração e depois da Fase 3 vão existir só na coleção antiga.
   *(2026-05-03)*

2203. Há 4 demandas pendentes no `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2204. O sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) usa Hub Qdrant como memória central, GitHub como conhecimento, e Drive como espelho.
   *(2026-05-04)*

2205. O projeto Gus é um sistema multi-porta que interage através do Telegram, Claude Code, Claude Chat e futuramente por Custom GPT e Alexa, com um Hub Qdrant como memória central.
   *(2026-05-04)*

2206. O Gus é um agente pessoal multi-porta que opera através de várias plataformas, como Telegram, Claude Code e Claude Chat.
   *(2026-05-03)*

2207. No contexto da refatoração, o arquivo `gus-identity.md` foi deletado, enquanto informações relevantes foram migradas para o `gus-bootstrap.md` e `gus/system_prompt.md`.
   *(2026-05-03)*

2208. Os arquivos com as demandas pendentes são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template `_frontmatter-referencia.md`.
   *(2026-05-03)*

2209. O estado final dos PRs já tá no código + nos docs gus-XX atualizados.
   *(2026-05-03)*

2210. O Gus é um sistema de agente pessoal multi-porta, com memória central no Hub Qdrant e arquivos .md no GitHub.
   *(2026-05-03)*

2211. Os quatro documentos principais que dão 80% do contexto para qualquer aba nova são: `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md` e `estado-atual.md`.
   *(2026-05-03)*

2212. Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2213. O Gus é um sistema de agente pessoal multi-porta com memória central no Hub Qdrant.
   *(2026-05-03)*

2214. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) muda e termina em 12/05/2026.
   *(2026-05-03)*

2215. A recomendação de atualizar a hierarquia dos canais de escrita no Chat é necessária para padronização.
   *(2026-05-03)*

2216. No sistema multi-porta, o Hub Qdrant é a memória central e o GitHub é usado como conhecimento.
   *(2026-05-03)*

2217. O bot pode vazar informações sensíveis, como CPF e telefone, na resposta ao usuário.
   *(2026-05-02)*

2218. Sistema de agente pessoal multi-porta: Telegram, Claude Code, Claude Chat e futuras como Alexa.
   *(2026-05-03)*

2219. Sugere-se que os tipos de fragmentos sejam definidos em um arquivo separado e incluam exemplos de quando cada tipo é utilizado.
   *(2026-05-04)*

2220. Gus é um sistema de agente pessoal multi-porta com memória central no Hub Qdrant.
   *(2026-05-03)*

2221. O algoritmo de auditoria do Hub Qdrant é cego ao brain gus que nunca aparece em frescor, densidade por área ou duplicatas.
   *(2026-05-03)*

2222. Gustavo está desenvolvendo um projeto de casa de fim de semana em Paty do Alferes, focando em sistemas sustentáveis de água e design arquitetônico.
   *(2026-05-03)*

2223. A receita ordenada por valor por contexto é utilizada para determinar o foco mínimo necessário para não inflar o contexto.
   *(2026-05-03)*

2224. PRs descrevem o caminho, não onde a gente está.
   *(2026-05-03)*

2225. Com o fim da coleção legada, todas as operações que envolvem o Mem0 SaaS estão em risco de perda contínua.
   *(2026-05-03)*

2226. O Gus é um sistema de agente pessoal multi-porta, com memória central no Hub Qdrant.
   *(2026-05-03)*

2227. O Hub é mais fresco que [gus-estado-atual.md](http://gus-estado-atual.md).
   *(2026-05-03)*

2228. O hub `gustavo` contém 20 fragmentos, com ~70% considerados lixo.
   *(2026-05-03)*

2229. A memória central do Gus está no Hub Qdrant.
   *(2026-05-03)*

2230. Esses 4 documentos dão 80% do contexto pra qualquer aba nova.
   *(2026-05-03)*

2231. A comunicação entre Gustavo e Claude deve ser calibrada para assegurar que as memórias estejam sempre atualizadas e livres de drift.
   *(2026-05-04)*

2232. Os 4 documentos principais (`gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md` e `estado-atual.md`) dão 80% do contexto pra qualquer aba nova.
   *(2026-05-03)*

2233. `gus-estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois.
   *(2026-05-02)*

2234. Os quatro arquivos principais que dão 80% do contexto para qualquer aba nova são: `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md` e `estado-atual.md`.
   *(2026-05-03)*

2235. O arquivo gus-identity.md está desatualizado, apresenta drift em relação ao sistema atual.
   *(2026-05-03)*

2236. MCP fail-closed default.
   *(2026-05-03)*

2237. O retro-engine é um hook que registra o transcript de sessões e tenta chamar a API da Anthropic.
   *(2026-05-02)*

2238. O arquivo gus-identity.md contém informações desatualizadas sobre o sistema.
   *(2026-05-03)*

2239. Não há mecanismo de deduplicação nas memórias atuais do Gus, o que aumenta o risco de poluição cruzada entre as fontes.
   *(2026-05-03)*

2240. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2241. O log de curador registra `curador: gpt` em todos os hits, levantando a questão sobre a presença de Haiku no sistema.
   *(2026-05-03)*

2242. Há 204 fragmentos não-migrados da coleção legada `gus` e o código de leitura ainda faz fallback para ela.
   *(2026-05-03)*

2243. O sistema de agente pessoal tem multi-portas, incluindo Telegram, Claude Code, e futuras integrações com Alexa.
   *(2026-05-03)*

2244. A auditoria identificou a necessidade de integrar uma lógica clara para hierarquizar os canais de escrita do Chat.
   *(2026-05-02)*

2245. O arquivo gus-identity.md está redundante com o gus-bootstrap.md e deve ser consolidado.
   *(2026-05-03)*

2246. O Gus é um sistema de agente pessoal multi-porta que inclui Telegram, TioGu, Claude Code e Claude Chat.
   *(2026-05-03)*

2247. Migração Mem0 para Hub Qdrant na Fase 4 está programada, com coleta dual Haiku e Sonnet rodando até 12/05, e uma decisão sobre o modelo curador final será feita em seguida.
   *(2026-05-03)*

2248. O chat se baseia em memória e para a inicialização, ele lê no começo das mensagens.
   *(2026-05-03)*

2249. O Deep Learning Framework MASE/ACEE foi criado por Gustavo e se foca em explicabilidade simbólica.
   *(2026-05-04)*

2250. O Hub Qdrant é a fonte nova, mas a coleção legada gus ainda está viva, e seu uso cria inconsistências nas buscas.
   *(2026-05-03)*

2251. O algoritmo de ciclo de vida ('lifecycle') do schema gus-18 está declarado mas não executado, resultando em fragmentos sempre ativos.
   *(2026-05-03)*

2252. A captura de memória está quebrada na porta Code devido à falta de `ANTHROPIC_API_KEY`.
   *(2026-05-04)*

2253. As demandas paradas em `dialogos/inbox-claude-code/` incluem: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, e `_frontmatter-referencia.md` (este último é template, não é demanda).
   *(2026-05-03)*

2254. O core do bootstrap deve ser enxugado e as partes variantes carregadas somente quando necessário para otimizar o desempenho do Chat.
   *(2026-05-03)*

2255. O arquivo `gus-identity.md` é redundante e está desatualizado em comparação com o `gus-bootstrap.md`.
   *(2026-05-04)*

2256. O Hub `gustavo` contém 20 fragmentos, ~70% lixo, enquanto o Hub `gus` também tem 20 fragmentos.
   *(2026-05-03)*

2257. A stack está em estado intermediário arriscado. Hub Qdrant é a fonte nova, mas a coleção legada gus (Mem0 self-hosted) tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

2258. A stack de memória está em estado intermediário arriscado com risco moderado de perda silenciosa.
   *(2026-05-03)*

2259. Os projetos ativos de Gustavo incluem Phronesis-Bench, NeuroGus, MGE/MGX, TER e Axon.
   *(2026-05-03)*

2260. O sistema multi-porta possui o Hub Qdrant como memória central.
   *(2026-05-02)*

2261. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa.
   *(2026-05-02)*

2262. TioGu passou pela Fase 1 de saneamento e agora se prepara para Fase 2A de documentação e Fase 2B de reescrita de arquivos.
   *(2026-05-03)*

2263. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2264. A captura dual de modelos no curador (Haiku × GPT-4o-mini) terminará em 12/05/2026.
   *(2026-05-03)*

2265. O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois.
   *(2026-05-02)*

2266. O curador híbrido (Haiku + GPT-4o-mini) está em implementação.
   *(2026-05-03)*

2267. Opção A é recomendada para um fechamento limpo do legado Mem0 SaaS.
   *(2026-05-03)*

2268. Ele tem hipertireoidismo sob tratamento com Tapazol, acompanhado por um endocrinologista.
   *(2026-05-04)*

2269. As demandas pendentes no inbox-claude-code incluem captura-multiporta-curador, drive-sync-oauth-fix, e pendencias-claude-chat-consolidacao.
   *(2026-05-03)*

2270. O último dia de captura no Mem0 SaaS foi 26/04/2026.
   *(2026-05-03)*

2271. O fragmento gerado pelo curador é classificado como 'tipo=episodico, area=''.
   *(2026-05-03)*

2272. O sistema Gus é um agente pessoal multi-porta conectado a uma memória central no Hub Qdrant, espelhado em arquivos .md no GitHub.
   *(2026-05-03)*

2273. Anthropic custa $3 por 1 milhão de tokens de input e $15 por output, enquanto OpenAI (gpt-4o-mini) custa $0.15 por input e $0.60 por output.
   *(2026-05-03)*

2274. O bot Telegram (TioGu) possui aproximadamente 21 ferramentas, multimídia, prompt caching, e está em produção no Railway.
   *(2026-05-04)*

2275. A stack está em estado intermediário arriscado, com coleta dual de modelos no curador.
   *(2026-05-03)*

2276. O estado atual do projeto está documentado no arquivo `projetos/gus/_estado-atual.md`.
   *(2026-05-03)*

2277. O curador híbrido do sistema coleta e processa fragmentos de conversas, com uma abordagem de A/B testing entre Haiku e GPT-4o.
   *(2026-05-03)*

2278. O workflow 'migrar-gus-para-hub.yml' deve ser revisado para evitar que a coleção 'gus' fique fora do Hub novo.
   *(2026-05-03)*

2279. O retro-engine registra 'no-op: anthropic_missing' e segue.
   *(2026-05-03)*

2280. O Hub Qdrant é a memória central do sistema Gus, que é sustentado por arquivos .md no GitHub.
   *(2026-05-03)*

2281. O curador Telegram apresentou erros 400 recorrentes e está em um loop com 100% de erro há mais de três dias.
   *(2026-05-03)*

2282. O valor do segredo deve ser salvo na variável MCP_URL_SECRET no serviço gus-mcp-server no Railway.
   *(2026-05-03)*

2283. O MCP está público — qualquer scanner que descobrir a URL Railway lê todo o Hub.
   *(2026-05-03)*

2284. Hub Qdrant é a nova fonte da verdade do sistema Gus.
   *(2026-05-03)*

2285. Ativar auto-reload evita interrupção futura.
   *(2026-05-03)*

2286. Recomendação de renomear a pasta inbox-mem0-from-chat para inbox-chat-raw para maior clareza.
   *(2026-05-03)*

2287. As demandas paradas em `dialogos/inbox-claude-code/` são: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, e `_frontmatter-referencia.md`.
   *(2026-05-02)*

2288. ADR-001 está em curso: aposentadoria do Mem0 SaaS e implementação do Hub Qdrant como fonte da verdade.
   *(2026-05-03)*

2289. O bot Telegram (TioGu) possui 21 tools e multimídia com prompt caching em produção no Railway.
   *(2026-05-04)*

2290. A coleta dual de modelos no curador deve ser concluída até 12/05/2026, após a qual Gustavo escolherá um modelo definitivo.
   *(2026-05-03)*

2291. PRs são histórico, não documentação, e não precisam ser lidos para uma nova aba, a não ser que esteja especificamente investigando um bug ou uma mudança recente.
   *(2026-05-02)*

2292. O projeto Gus é um sistema de agente pessoal multi-porta com memória central no Hub Qdrant.
   *(2026-05-03)*

2293. Um dos desafios recentes foi a transição do sistema de Mem0 para Hub Qdrant, conforme descrito no ADR-001.
   *(2026-05-03)*

2294. A demanda `2026-05-01-captura-multiporta-curador.md` precisa de um gatilho proativo no Chat.
   *(2026-05-03)*

2295. O Gus está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

2296. O passo 5 é recadastrar o Connector no claude.ai.
   *(2026-05-03)*

2297. O arquivo `dialogos/_bootstrap/gus-bootstrap.md` é o manual operacional do Gus, com regras de comportamento de como cada porta usa o Hub.
   *(2026-05-02)*

2298. Os quatro arquivos lazy são: `gus-protocolo-demanda.md`, `gus-protocolo-drive.md`, `gus-pastas-do-projeto.md`, `gus-tipos-fragmento.md`.
   *(2026-05-03)*

2299. O Connector claude.ai precisa ser recriado após a mudança na URL do MCP.
   *(2026-05-02)*

2300. O desenvolvimento do bot Telegram passou a ser modular, com melhorias na estrutura de pastas e arquivos.
   *(2026-05-04)*

2301. Há 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2302. O trabalho recente focou em hardening do sistema, com a correção de erros em curadores e atualizações na segurança dos logs.
   *(2026-05-04)*

2303. O projeto NeuroGus está bloqueado por decisões de UX e mock HTML não concluídos.
   *(2026-05-03)*

2304. Gus está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-04)*

2305. A biblioteca utilizada para o bot Telegram é python-telegram-bot, na versão 21.6.
   *(2026-05-04)*

2306. A qualidade do conteúdo do Mem0 SaaS é superior à do Hub atual, mostrando fragmentos biográficos reais e decisões arquiteturais.
   *(2026-05-03)*

2307. As memórias do Gus possuem um lifecycle que inclui atualização de peso, acessos e promoção automática de estado.
   *(2026-05-03)*

2308. A `gus/dimagem.py` deve ser movida para `integrations/`.
   *(2026-05-02)*

2309. Hub `gus` tem 20 fragmentos, com cross-brain pollution confirmada.
   *(2026-05-03)*

2310. As pastas pessoais foram reorganizadas com a criação de áreas faltantes, como saúde, esportes, leituras, contatos e família.
   *(2026-05-02)*

2311. Durante a conversa, o Chat só salva fragmentos quando solicitado, não detecta automaticamente fatos ou decisões relevantes.
   *(2026-05-03)*

2312. Gustavo Pratti de Barros é anestesiologista no Dimagem, localizado no Rio de Janeiro, e pesquisador independente em IA.
   *(2026-05-03)*

2313. O período de coleta de dados no Mem0 SaaS foi de 11/04 a 26/04, com 204 fragmentos presentes.
   *(2026-05-03)*

2314. O arquivo 'gus-bootstrap.md' contém a identidade do Gustavo, diretrizes operacionais e caminhos de captura que informam como o Gus deve se comportar.
   *(2026-05-04)*

2315. O cron pega, auto-injeta frontmatter e comita em dialogos/inbox-claude-code em até 15 minutos.
   *(2026-05-03)*

2316. O sistema de agente pessoal multi-porta tem memória central no Hub Qdrant e arquivos .md no GitHub.
   *(2026-05-03)*

2317. O último arquivo da pasta de demandas pendentes é `semana-2026-04-21.md`.
   *(2026-05-03)*

2318. Gus está na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2319. O curador do Gus gera fragmentos a partir de diferentes fontes, como Telegram, Claude Chat e Claude Code.
   *(2026-05-03)*

2320. O curador híbrido está em estado intermediário arriscado e possui 3 produções de fragmentos com 4 vezes a multiplicação de chamadas de LLM por unidade de input.
   *(2026-05-03)*

2321. O estado final dos PRs já está no código e nos docs gus-XX atualizados.
   *(2026-05-03)*

2322. A migração da Mem0 para o Hub Qdrant foi concluída e não utiliza mais Mem0 como camada de armazenamento.
   *(2026-05-04)*

2323. O sistema Gus é um agente pessoal multi-porta em produção, rodando em um Hub Qdrant.
   *(2026-05-03)*

2324. A colonia legada de fragmentos no Qdrant está vazia. Não há fragmentos a serem migrados.
   *(2026-05-03)*

2325. Mem0 SaaS está aposentado.
   *(2026-05-03)*

2326. O estado atual do projeto envolve uma migração para o Hub Qdrant, com a coleta dual de modelos no curador.
   *(2026-05-03)*

2327. Recomenda-se matar o arquivo `gus-identity.md` e migrar seu conteúdo importante para o `gus-bootstrap.md` e o `gus/system_prompt.md`.
   *(2026-05-04)*

2328. Há 6 demandas listadas na caixa de entrada do inbox-claude-code, sendo 3 demandas reais identificadas.
   *(2026-05-03)*

2329. Para obter informações mais recentes e preferir sempre ferramentas MCP, utilize a função `ego_cache_atual()` para acessar a identidade e as últimas decisões realizadas.
   *(2026-05-03)*

2330. O projeto envolve um sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) com Hub Qdrant como memória central.
   *(2026-05-04)*

2331. Core obrigatório (sempre, em toda aba nova) são 4 arquivos que dão 80% do contexto: `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md`, `estado-atual.md`.
   *(2026-05-03)*

2332. Perguntei se queria que eu processasse as demandas ou se tinha algo específico em mente.
   *(2026-05-03)*

2333. A captura real-time do sistema Gus está funcionando.
   *(2026-05-04)*

2334. O Hub é a memória central do agente Gus.
   *(2026-05-03)*

2335. O código que loga ainda é o antigo e o novo secret vazou no log.
   *(2026-05-03)*

2336. Esses 4 documentos dão 80% do contexto pra qualquer aba nova: gus-bootstrap.md, gus-identity.md, gus-estado-atual.md, estado-atual.md.
   *(2026-05-03)*

2337. O sistema ainda faz fallback para Mem0 SaaS, o que pode levar a perdas silenciosas.
   *(2026-05-03)*

2338. Gustavo é falante nativo de português, baseado no Rio de Janeiro. Tem interesses intelectuais fortes em segurança em IA, filosofia e systems thinking.
   *(2026-05-04)*

2339. Tem 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

2340. A remoção de `gus-identity.md` e a migração de seu conteúdo para o `gus-bootstrap.md` e `gus/system_prompt.md` foi recomendada como uma solução para os problemas identificados.
   *(2026-05-04)*

2341. A arquitetura do sistema Gus foi migrada do Mem0 para o Hub Qdrant, com mais de 1076 fragmentos armazenados.
   *(2026-05-03)*

2342. Gustavo Pratti de Barros é anestesiologista.
   *(2026-05-03)*

2343. Core obrigatório inclui o arquivo `gus-bootstrap.md` que é o manual operacional do Gus, regras de comportamento e como cada porta usa o Hub.
   *(2026-05-03)*

2344. A estrutura do bot Telegram é composta por arquivos, incluindo bot.py, llm.py, memory.py, tools.py, e outros.
   *(2026-05-02)*

2345. O uso do Hub Qdrant como fonte da verdade foi adotado. Há necessidade de limpeza no conteúdo atual do Hub.
   *(2026-05-03)*

2346. Os arquivos devem ser lidos para qualquer nova aba, pois fornecem 80% do contexto.
   *(2026-05-04)*

2347. Hub Qdrant é a fonte da verdade, com arquivos .md no GitHub e espelhados no Drive.
   *(2026-05-03)*

2348. O Chat deve manter uma abordagem de não alucinação e validação nas interações.
   *(2026-05-04)*

2349. A maior parte do conteúdo no arquivo gus-identity.md vive no arquivo gus-bootstrap.md.
   *(2026-05-03)*

2350. A demanda 2026-05-01-captura-multiporta-curador.md aguarda decisão tua.
   *(2026-05-02)*

2351. O estado do arquivo '_estado-atual.md' na pasta projetos/gus está desatualizado, sendo de 27/04, e o 'gus-estado-atual.md' está atualizado após o cron de 15 minutos.
   *(2026-05-03)*

2352. Há três produções simultâneas de fragmentos (Telegram, Chat, Code) com multiplicação de chamadas LLM por unidade de input.
   *(2026-05-03)*

2353. O estado final dos PRs já tá no código e nos docs atualizados, enquanto PRs descrevem o caminho, não onde estamos.
   *(2026-05-03)*

2354. As ferramentas do TioGu são gerenciadas por um array TOOLS em `tools.py`.
   *(2026-05-03)*

2355. O arquivo `gus-bootstrap.md` contém o núcleo operacional necessário para o funcionamento do Gus e do Chat.
   *(2026-05-04)*

2356. Os logs do Railway mostram o segredo em texto claro.
   *(2026-05-03)*

2357. O sistema 'Gus' é um agente pessoal multi-porta (Telegram, Claude Code, Claude Chat com MCP Connector, Custom GPT, Alexa planejada) operando sobre um Hub Qdrant.
   *(2026-05-03)*

2358. All inputs são coletados a partir de Telegram, Claude Chat e Claude Code, e o processo de ingestão é realizado através de múltiplos scripts.
   *(2026-05-03)*

2359. Gustavo é pesquisador independente em IA.
   *(2026-05-03)*

2360. O Chat deve carregar o `gus-bootstrap.md` com 1800 tokens para otimizar a inicialização.
   *(2026-05-03)*

2361. A auditoria diária (`auditoria_hub.py`) é cega para o brain `gus` e classifica por keywords ignorando o `area` que o curador já preencheu.
   *(2026-05-03)*

2362. O sistema Gus tem memória central no Hub Qdrant, arquivos .md no GitHub e estão espelhados no Drive.
   *(2026-05-03)*

2363. A partir de 12/05/2026, Gustavo escolherá um modelo definitivo.
   *(2026-05-03)*

2364. O `_estado-atual.md` da pasta projetos/gus está de 27/04 e é considerado desatualizado em relação ao que foi registrado no Hub.
   *(2026-05-04)*

2365. Bootstrap deve ser otimizado para incluir regras duras, diretrizes universais e o que é necessário para operações básicas do Chat.
   *(2026-05-03)*

2366. As diretrizes de comportamento do Gus foram compatibilizadas entre os arquivos.
   *(2026-05-04)*

2367. O fragmento que foi salvo tem o UUID '42aea182-d4a2-4626-8a85-5ede861b311b'.
   *(2026-05-04)*

2368. Gustavo Pratti de Barros é anestesiologista.
   *(2026-05-03)*

2369. O Gustavo é anestesiologista e não programa, portanto, toda implementação do sistema passa por um agente virtual chamado Tiogu.
   *(2026-05-03)*

2370. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2371. O passo 2 envolve recadastrar o Connector claude.ai após o `MCP_URL_SECRET` ser setado.
   *(2026-05-03)*

2372. Usuários de Claude Chat não devem ser informados sobre limites de acesso à internet.
   *(2026-05-04)*

2373. A migração para o Hub Qdrant é a prioridade atual do projeto, com conclusão prevista para 12/05/2026.
   *(2026-05-03)*

2374. O contrato schema gus-18 é parcialmente implementado, com lifecycle declarado mas não executado.
   *(2026-05-03)*

2375. O curador híbrido falhava silenciosamente e gerava fragmentos no Mem0 antigo.
   *(2026-05-03)*

2376. As auditorias são registradas em projetos/gus/auditorias/2026-05-02-memoria-diagnostico.md.
   *(2026-05-03)*

2377. A arquitetura do TioGu foi refatorada, dividindo o antigo arquivo tools.py em múltiplos módulos focados para melhorar a legibilidade e manutenção.
   *(2026-05-03)*

2378. Uma abordagem de lazy-load deve ser implementada para otimizar o uso dos protocolos, carregando-os apenas quando necessário.
   *(2026-05-04)*

2379. O estado final dos PRs já tá no código + nos docs gus-XX atualizados.
   *(2026-05-03)*

2380. O sistema 'Gus' agora opera com dois cérebros independentes no Hub Qdrant.
   *(2026-05-03)*

2381. Não há uma entry point clara ou ordem de leitura no bootstrap.
   *(2026-05-03)*

2382. O Hub Qdrant é a nova fonte da verdade após a migração em andamento com a ADR-001.
   *(2026-05-03)*

2383. O MCP público está sem MCP_URL_SECRET, permitindo acesso total ao Hub. Assim, qualquer scanner que descobrir o domínio do servidor pode ler todo o conteúdo, incluindo dados sensíveis.
   *(2026-05-03)*

2384. A auditoria diária é cega para o brain `gus` e classifica por keywords ignorando o `area` que o curador já preencheu.
   *(2026-05-03)*

2385. No estado atual, o Hub Qdrant contém 40 fragmentos, sendo que a qualidade é catastrófica.
   *(2026-05-03)*

2386. Os logs atuais não cobrem hex puro de 64 chars como sensíveis.
   *(2026-05-03)*

2387. Há 204 fragmentos não-migrados da coleção legada 'gus' que precisam ser transferidos.
   *(2026-05-03)*

2388. A sincronização do Drive via WIF foi migrada de usuário OAuth (expiração de token de teste de 7 dias) para Workload Identity Federation com Conta de Serviço. A política da organização bloqueou chaves JSON de SA, tendo o WIF sido escolhido.
   *(2026-05-04)*

2389. Os comandos do Gus são centralizados, permitindo que Gustavo interaja com o sistema por diferentes plataformas.
   *(2026-05-03)*

2390. O estado da migração é o ADR-001 em curso: aposentar Mem0 SaaS, Hub Qdrant é a fonte da verdade.
   *(2026-05-03)*

2391. A opção recomendada para lidar com os 204 fragmentos do Mem0 SaaS é mantê-los em um arquivo histórico agora e planejar uma importação após a fase de limpeza do Hub.
   *(2026-05-03)*

2392. O sistema multi-porta é composto por Telegram, Claude Code, Claude Chat, Custom GPT e futuro suporte a Alexa.
   *(2026-05-03)*

2393. O comando do Railway para redeployar o MCP Server leva ~2-3 minutos.
   *(2026-05-03)*

2394. Houve um bug crítico em produção, onde o curador estava sem funcionar devido a um erro no tratamento de placeholders no template de prompts.
   *(2026-05-02)*

2395. A stack de memória está em estado intermediário arriscado com 204 fragmentos não-migrados.
   *(2026-05-03)*

2396. `gus-bootstrap.md` é o arquivo central que o Chat lê na inicialização, contendo identidade, capacidades e regras operacionais.
   *(2026-05-04)*

2397. A captura de mensagens em tempo real do Chat é aplicada apenas para o caminho correto e seguro após a configuração do MCP_URL_SECRET.
   *(2026-05-03)*

2398. O processo de desenvolvimento do TioGu é uma aplicação que integra diferentes ferramentas no Telegram.
   *(2026-05-02)*

2399. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

2400. Próximo: decidir Drive sync (OAuth quebrado desde 01/05 14:38Z).
   *(2026-05-03)*

2401. O sistema deve implementar um tratamento de erro mais robusto nas operações de upload e captura do Chat.
   *(2026-05-04)*

2402. Os arquivos de bootstrap devem ser otimizados para reduzir o tamanho e a redundância.
   *(2026-05-04)*

2403. A auditoria está cega para o brain 'gus' e ignora o esquema de áreas que o curador preencheu.
   *(2026-05-03)*

2404. O bot Telegram possui ~21 ferramentas distintas implementadas com multimídia e caching de prompts.
   *(2026-05-03)*

2405. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) mudou de Sonnet em 29/04/2026.
   *(2026-05-03)*

2406. A elasticidade do glúten contribui para a textura e crocância da massa da pizza.
   *(2026-05-03)*

2407. O projeto Gus tem um cron que gera um estado atual do system a cada 15 minutos.
   *(2026-05-03)*

2408. O sistema de agente pessoal é multi-porta e utiliza um Hub Qdrant como memória central.
   *(2026-05-03)*

2409. As demandas pendentes para a porta incluem capturas multiporta, curador bidirecional cron, e OAuth para o drive-sync.
   *(2026-05-03)*

2410. O status dos itens da Fase 1 revela 8 de 9 entregas concluídas, exceto a limpeza do Hub.
   *(2026-05-03)*

2411. O estado atual do Hub é gerado automaticamente pelo cron às 03h.
   *(2026-05-03)*

2412. A auditoria diária do Hub Qdrant é feita através de um script específico.
   *(2026-05-03)*

2413. Logs que capturam segredos devem ser redigidos por razões de segurança.
   *(2026-05-03)*

2414. O `_estado-atual.md` está desatualizado em relação a mudanças que ocorreram após 27/04/2026.
   *(2026-05-03)*

2415. A manutenção do arquivo gus-identity.md é ineficiente, já que ele não contém informação única e relevante.
   *(2026-05-03)*

2416. O sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa) tem memória central no Hub Qdrant.
   *(2026-05-03)*

2417. O sistema de captura enfrenta um risco de poluição cruzada entre os brains `gustavo` e `gus` devido à execução simultânea de múltiplas entradas de dados.
   *(2026-05-03)*

2418. As memórias de 28/04 estão na coleção legada, fora do Hub novo.
   *(2026-05-03)*

2419. A publicação sobre o Phronesis-Bench foi finalizada e auditada em relação ao sistema Mythos. O tom é de 'pergunta honesta + consequências', não de reivindicação de descoberta.
   *(2026-05-03)*

2420. O estado final dos PRs está no código e nos documentos atualizados, e não é necessário ler os PRs durante a criação de uma nova aba.
   *(2026-05-03)*

2421. A VLAN precisa ser adicionada ao pattern de sensíveis também.
   *(2026-05-03)*

2422. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2423. O Hub é mais fresco que `gus-estado-atual.md`, que é um snapshot realizado às 03h.
   *(2026-05-04)*

2424. O arquivo gus-identity.md contém seções que misturam conteúdo aplicável a todas as portas e conteúdo específico para o bot do Telegram.
   *(2026-05-03)*

2425. Foi implementado um cache de mídia com limite de 200MB para evitar problemas de memória.
   *(2026-05-03)*

2426. O último log mostra que após o fix do `format()`, o Haiku está rejeitando todos os fragmentos.
   *(2026-05-03)*

2427. Três caminhos de escrita coexistem com regras parcialmente compatíveis
   *(2026-05-03)*

2428. Todos os testes do TioGu, somando 187, estão com resultado verde e cobrem diversos casos de regressão.
   *(2026-05-04)*

2429. O projeto Gus possui um sistema multi-porta com Hub Qdrant como memória central e GitHub como conhecimento, utilizando Telegram, Claude Code e Claude Chat, com futuras integrações planejadas.
   *(2026-05-04)*

2430. O bot do Telegram, TioGu, possui 21 ferramentas distintas integradas.
   *(2026-05-03)*

2431. Os 204 fragmentos históricos estavam no Mem0 SaaS (api.mem0.ai), não no Qdrant Cloud self-hosted.
   *(2026-05-03)*

2432. As 2 demandas pendentes são a de sincronização do Drive e a de captura multiporta do Claude Chat.
   *(2026-05-02)*

2433. A pasta do Drive se chama Gus-Sync, não GitHub-Sync.
   *(2026-05-04)*

2434. Hub tem de ser preferido em comparação com o gus-estado-atual.md porque é mais fresco.
   *(2026-05-02)*

2435. As 204 memórias históricas da coleção 'gus' estão vazias e não existem no Hub Qdrant.
   *(2026-05-03)*

2436. A auditoria tem a finalidade de garantir a integridade e qualidade dos dados em movimento.
   *(2026-05-03)*

2437. As pastas devem ser criadas agora no Google Drive para que a sincronização funcione.
   *(2026-05-03)*

2438. Gus está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-04)*

2439. O retro-engine registra 'no-op: anthropic_missing' e segue.
   *(2026-05-03)*

2440. O ADR-001 está em andamento e busca aposentadoria da Mem0 SaaS.
   *(2026-05-03)*

2441. A auditoria do Chat indicou que o Curador Telegram apresenta um erro de 400 de forma recorrente.
   *(2026-05-04)*

2442. A captura de transcripts em tempo real para o Chat está pendente de decisão do Gustavo.
   *(2026-05-03)*

2443. O curador possui duas camadas de execução: Haiku e GPT-4o-mini, e está em fase de coleta dual de modelos.
   *(2026-05-03)*

2444. Gustavo está desenvolvendo uma casa de fim de semana em Paty do Alferes com sistemas sustentáveis de água e design arquitetônico.
   *(2026-05-04)*

2445. A auditoria diária é feita por `auditoria_hub.py` que classifica por keywords ignorando a área.
   *(2026-05-03)*

2446. A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida, mas falta o gatilho proativo no Chat.
   *(2026-05-02)*

2447. Gustavo Pratti de Barros é o paciente.
   *(2026-05-03)*

2448. O Auditoria do Chat foi concluída em 02/05/2026, identificando problemas e recomendações.
   *(2026-05-03)*

2449. A parte única do `gus-identity.md` poderia ser movida para o `system_prompt` do TioGu.
   *(2026-05-03)*

2450. As_changes d1 e d2, referentes ao sistema `Claude Chat`, `Drive Sync` e `NeuroGus`, estão sendo tratados em uma aba separada, logo essas decisões não são prioridade.
   *(2026-05-02)*

2451. Os 204 fragmentos exportados do Mem0 SaaS estavam em inglês e português.
   *(2026-05-03)*

2452. Existem 3 demandas paradas em 'dialogos/inbox-claude-code/'.
   *(2026-05-02)*

2453. As 204 memórias no Mem0 SaaS foram extraídas e estão seguras em 'historico/'.
   *(2026-05-03)*

2454. Auditoria diária `auditoria_hub.py` é cega para o brain `gus` e classifica por keywords ignorando o `area` que o curador já preencheu.
   *(2026-05-03)*

2455. Gustavo é anestesiologista e não programa; toda implementação passa pelo Gus ou pelo Tiogu.
   *(2026-05-03)*

2456. Gus é um sistema de agente pessoal multi-porta que integra diferentes plataformas, como Telegram, Claude Chat e Claude Code, com memória central no Hub Qdrant.
   *(2026-05-03)*

2457. Painel de controle e logs de erro são mantidos e documentados via Automação GitHub Actions.
   *(2026-05-03)*

2458. Se Anthropic falhar, o sistema poderá usar OpenAI Vision como fallback para imagens.
   *(2026-05-04)*

2459. O Chat possui ferramentas nativas como Drive, Gmail, Calendar, e Spotify.
   *(2026-05-04)*

2460. Os documentos no projeto devem ser organizados em tiers para otimizar o acesso e a carga de informações.
   *(2026-05-04)*

2461. O curador híbrido coleta dados e registra A/B observável para decisões de modelo baseadas em evidência.
   *(2026-05-02)*

2462. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) deve ser finalizada até 12/05/2026.
   *(2026-05-03)*

2463. Hoje o MCP tá público — qualquer scanner que descobrir a URL Railway lê todo o Hub.
   *(2026-05-03)*

2464. O retro-engine registra 'no-op: anthropic_missing' e segue.
   *(2026-05-03)*

2465. Core obrigatório: 4 arquivos principais fornecem 80% do contexto para qualquer aba nova.
   *(2026-05-03)*

2466. O MCP está público — qualquer scanner que descobrir a URL Railway lê todo o Hub.
   *(2026-05-03)*

2467. Há 4 demandas pendentes identificadas no `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2468. O acesso ao Hub se dará através do MCP após a configuração do `MCP_URL_SECRET`.
   *(2026-05-03)*

2469. As próximas fases do projeto incluem limpeza do Hub e importação inteligente de fragmentos.
   *(2026-05-03)*

2470. O arquivo dialogos/_bootstrap/gus-bootstrap.md contém regras de comportamento e como cada porta usa o Hub.
   *(2026-05-02)*

2471. O status 'fallback-mem0' mente, pois o log diz isso mas o resumo vai para o Hub.
   *(2026-05-03)*

2472. O sistema Gus gera uma captura real-time que está atualmente funcionando.
   *(2026-05-04)*

2473. Os últimos commits na branch main envolveram atualizações automáticas relacionadas ao estado do Hub para o Claude Chat e processamento de transcrições do Claude Code.
   *(2026-05-02)*

2474. O projeto NeuroGus está na fase 1 de backend e a fase 2 no frontend está bloqueada.
   *(2026-05-03)*

2475. O projeto é dividido em dois principais canais de escrita: real-time com ingesta de fragmentos e upload de arquivos .md.
   *(2026-05-03)*

2476. O arquivo está em historico/mem0-saas-export-final-2026-05-02.json.
   *(2026-05-03)*

2477. Há 4 fragmentos no Hub, com 70% considerados lixo.
   *(2026-05-03)*

2478. Gustavo é anestesiologista, não programa — toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

2479. No dia 26/04/2026, o último dia de captura no Mem0 SaaS, foram registrados 204 fragmentos.
   *(2026-05-03)*

2480. Apenas arquivo documenta a conversa de 29/04 a 02/05 e que teve ajustes feitos no código do curador.
   *(2026-05-03)*

2481. O arquivo `_estado-atual.md` está desatualizado, o último foi gerado em 27/04.
   *(2026-05-03)*

2482. Os arquivos salvos no Drive em `Gustavo/<porta>/` geram frontmatter automático, detectando a origem e o destino da demanda.
   *(2026-05-03)*

2483. O sistema de agente pessoal multi-porta conecta Telegram, Claude Code e Chat, com uma memória central no Hub Qdrant e arquivos no GitHub.
   *(2026-05-03)*

2484. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2485. A trilha de auditoria foi implementada para melhor controle sobre deletar fragmentos no Hub.
   *(2026-05-03)*

2486. O arquivo 'dialogos/_bootstrap/gus-identity.md' contém informações sobre quem é o Gustavo e quem é o Gus enquanto entidade.
   *(2026-05-03)*

2487. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, `_frontmatter-referencia.md` (template, não é demanda).
   *(2026-05-04)*

2488. NeuroGus é uma visualização 3D do Hub, totalmente desenhada e desbloqueada assim que as decisões §11.1-11.5 forem fechadas.
   *(2026-05-04)*

2489. tô aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2490. O Gus é um sistema de agente pessoal multi-porta, com memória central no Hub Qdrant.
   *(2026-05-03)*

2491. A migração para o Hub Qdrant está em curso, com uma coleta dual de modelos que termina em 12/05/2026, após a qual Gustavo escolherá um modelo definitivo.
   *(2026-05-03)*

2492. O Hub Qdrant é a fonte da verdade.
   *(2026-05-03)*

2493. O gus-identity.md contém informações duplicadas que já estão no arquivo gus-bootstrap.md, como o perfil do Gustavo e as diretrizes operacionais.
   *(2026-05-04)*

2494. O estado final dos PRs já está no código e nos docs atualizados.
   *(2026-05-03)*

2495. Hoje o Railway está com "MCP_AUTH_DISABLED=true" e sem URL secret, o que expõe todo o Hub.
   *(2026-05-03)*

2496. A próxima sessão da Fase 1 focará na análise de PII no output do bot, cache de mídia e cleanup cosmético.
   *(2026-05-02)*

2497. As demandas pendentes do inbox são relevantes para o Hub e o Chat.
   *(2026-05-03)*

2498. Clica no serviço gus-mcp-server.
   *(2026-05-03)*

2499. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2500. Foi identificado que a conversa do agente Gus possui fragmentos duplicados provenientes do Gustavo, o que gera poluição nos dados.
   *(2026-05-03)*

2501. As demandas pendentes são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um `_frontmatter-referencia.md` que é apenas um template.
   *(2026-05-03)*

2502. Os commits mostram que as demandas são integradas em um loop.
   *(2026-05-03)*

2503. O 'Gus' está ativo com sessões resumidas sendo salvas no Google Drive.
   *(2026-05-03)*

2504. O estado final dos PRs está no código e nos documentos atualizados.
   *(2026-05-03)*

2505. O Chat A salvou uma autoreflexão no brain 'gus' sobre a sessão de 03/05/2026.
   *(2026-05-03)*

2506. O conteúdo do Mem0 SaaS foi exportado para o arquivo `historico/mem0-export-final-2026-05-02.json`.
   *(2026-05-03)*

2507. Os quatro arquivos fundamentais dão 80% do contexto para qualquer nova aba: `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md` e `estado-atual.md`.
   *(2026-05-03)*

2508. Tavily está funcionando corretamente com busca OK.
   *(2026-05-03)*

2509. Gus está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-02)*

2510. NeuroGus é uma visualização 3D do Hub que desbloqueia após a conclusão das decisões em §11.1-11.5.
   *(2026-05-04)*

2511. A lista de candidatos a deletar foi gerada a partir de uma execução de dryrun.
   *(2026-05-03)*

2512. O sistema não utiliza mais o Mem0, que foi aposentado desde 27/04/2026.
   *(2026-05-03)*

2513. O contrato schema gus-18 está parcialmente implementado.
   *(2026-05-03)*

2514. Gustavo é falante nativo de português e tem interesses intelectuais fortes em segurança em IA, filosofia e systems thinking.
   *(2026-05-03)*

2515. O Hub Qdrant tem 40 fragmentos totais, com 70% deles sendo considerados lixo.
   *(2026-05-03)*

2516. O arquivo `gus-pastas-do-projeto.md` deve conter uma tabela que relaciona pastas do projeto e seu respectivo conteúdo.
   *(2026-05-04)*

2517. Antes de recadastrar o Connector no claude.ai, o segredo no log precisa ser removido.
   *(2026-05-03)*

2518. A primeira demanda é intitulada `2026-05-01-captura-multiporta-curador.md`.
   *(2026-05-02)*

2519. A auditoria diária tem uma ineficiência, pois é cega para o brain `gus` e classifica por keywords, ignorando as áreas que o curador já preencheu.
   *(2026-05-03)*

2520. Hub é mais fresco que [gus-estado-atual.md](http://gus-estado-atual.md) (que é snapshot das 03h). Sempre que possível, prefira tools MCP a arquivo .md.
   *(2026-05-03)*

2521. Mem0 foi aposentado desde 27/04/2026; o Hub Qdrant é a fonte única hoje.
   *(2026-05-04)*

2522. O workflow de migração para mover as memórias do Gus para o Hub Qdrant ainda não foi executado.
   *(2026-05-03)*

2523. O projeto precisa de uma estrutura de pastas dentro de dialogos para organizar as demandas.
   *(2026-05-03)*

2524. O sistema Gus possui três canais de escrita: MCP em tempo real, upload curado com latência e demandas no inbox-code.
   *(2026-05-04)*

2525. As auditorias precisam incluir a classificação por área do payload do curador para melhorar a busca.
   *(2026-05-03)*

2526. O log do retro-engine está em `claude/greeting-checkin-94weM`.
   *(2026-05-03)*

2527. A abordagem de captura dual no curador híbrido inclui comparação A/B entre Haiku e OpenAI GPT-4o.
   *(2026-05-04)*

2528. A memória do sistema 'Gus' migrou de Mem0 para Qdrant Hub direto (ADR-001, concluído em 27/04/2026), com 1076+ fragmentos em dois brains independentes: 'gustavo' e 'gus'.
   *(2026-05-03)*

2529. O contrato schema gus-18 está parcialmente implementado, com o ciclo de vida prometido não sendo executado.
   *(2026-05-03)*

2530. O Hub Qdrant é a fonte da verdade para o sistema de agente pessoal e armazena informações em fragmentos.
   *(2026-05-03)*

2531. As 18 entradas 'fallback-mem0' de 28/04 foram para o Mem0 SaaS porque a migração ainda não estava 100% deploy-ada.
   *(2026-05-03)*

2532. Gustavo Pratti de Barros é anestesiologista e não programa. Toda implementação passa pelo Gus, agente pessoal.
   *(2026-05-03)*

2533. Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template.
   *(2026-05-03)*

2534. O Hub Qdrant é a fonte da verdade para as memórias do Gus, substituindo a coleção legada do Mem0 SaaS.
   *(2026-05-03)*

2535. O `_estado-atual.md` está desatualizado e não reflete PRs #57, #60, #63, #64, #67.
   *(2026-05-04)*

2536. O sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) possui o Hub Qdrant como memória central, GitHub como conhecimento e Drive como espelho.
   *(2026-05-03)*

2537. A stack de memória do Gus está em estado intermediário arriscado, com potencial para perda silenciosa de fragmentos.
   *(2026-05-03)*

2538. A stack da memória está em estado intermediário arriscado, com 3 produções simultâneas de fragmentos.
   *(2026-05-03)*

2539. O plano de migração foi refinado, com itens novos e prioridades alteradas.
   *(2026-05-03)*

2540. A estrutura do projeto Gus é: pasta 'Gus-Sync' no Google Drive, arquivos via 'dialogos/', 'projetos/gus/', 'pessoal/', 'dimagem/', etc. A sincronização é feita via WIF.
   *(2026-05-04)*

2541. A demanda atual do Gustavo inclui a definição de `MCP_URL_SECRET` no Railway.
   *(2026-05-03)*

2542. PDFs não possuem fallback para OpenAI e geram uma mensagem amigável ao usuário no caso de falha do Anthropic.
   *(2026-05-03)*

2543. As ferramentas do bot foram documentadas em um inventário auto-gerado, refletindo suas funções e usos.
   *(2026-05-04)*

2544. 1. Bug resolvido: função `download_content` (linha 150) falhava com `UnicodeDecodeError` ao ler arquivo `frontmatter-referencia.md` salvo com encoding não-UTF-8 (provavelmente Windows-1252), continha byte inválido `0xB6` (¶).

2. Solução técnica aplicada: trocar `decode("utf-8")` por fallback robusto — tentar UTF-8 primeiro, cair para Latin-1 se falhar, ou usar `errors="replace"`.

3. Padrão futuro: Gus Chat deve sempre salvar arquivos no Drive em UTF-8 sem BOM e evitar caracteres especiais problemáticos (¶, •, –, aspas curvas de Word/Pages).

4. Contexto: problema ocorre quando arquivo `.md` é criado externamente e enviado pro Drive; exportar direto do Google Docs não tem esse risco (já vem UTF-8).

5. Ação confirmada: Gustavo autorizou aplicar a correção no script.
   *(2026-04-28)*

2545. Existem 4 arquivos focados para captura de demandas e protocolos no Chat, que são carregados sob demanda.
   *(2026-05-04)*

2546. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, e `_frontmatter-referencia.md`.
   *(2026-05-02)*

2547. Os 3 caminhos de escrita coexistem com regras parcialmente compatíveis.
   *(2026-05-03)*

2548. Gustavo é anestesiologista, não programa — toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

2549. Gustavo Pratti de Barros é um anestesiologista baseado no Rio de Janeiro, trabalhando na Dimagem, uma clínica de imagem diagnóstica com três unidades.
   *(2026-05-03)*

2550. A captura dual de modelos no curador (Haiku × GPT-4o-mini) muda de Sonnet em 29/04 por custo/resiliência.
   *(2026-05-03)*

2551. O modelo do Haiku foi silenciado devido a questões de billing, afetando a operação do curador e a funcionalidade da captura em tempo real.
   *(2026-05-03)*

2552. O Gustavo é anestesiologista e não programa; toda implementação deve ser aprovada por ele ou por Tiogu.
   *(2026-05-03)*

2553. O brain Gus ganha cobertura explícita: meta_reflexao, identidade_operacional e procedural.
   *(2026-05-03)*

2554. O histórico de auditoria em `hub/store.deletar()` foi implementado para permitir rastreamento de alterações.
   *(2026-05-04)*

2555. O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).
   *(2026-05-02)*

2556. O novo canal Gus-Sync/dialogos/inbox-gustavo/{chat,code,tiogu}/ no Drive permite a entrada direta sem a necessidade de digitar YAML.
   *(2026-05-03)*

2557. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2558. A atualização do estado atual do projeto foi realizada em 02/05/2026.
   *(2026-05-03)*

2559. A personalidade do Gus relacionada ao Telegram será incorporada no sistema de prompts do TioGu.
   *(2026-05-04)*

2560. O curador híbrido está em execução, fazendo comparação A/B entre Anthropic e OpenAI em paralelo.
   *(2026-05-04)*

2561. A pasta do Google Drive se chama Gus-Sync.
   *(2026-05-04)*

2562. O sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) utiliza o Hub Qdrant como memória central.
   *(2026-05-02)*

2563. O Hub Qdrant é a nova fonte da verdade para o sistema de agente pessoal multi-porta.
   *(2026-05-03)*

2564. O arquivo system_prompt.md tem 794 linhas e apresenta drift, misturando seções pré-migração e novas funcionalidades.
   *(2026-05-02)*

2565. O arquivo untracked é só um log do retro-engine que registra 'no-op: anthropic_missing' e segue.
   *(2026-05-04)*

2566. O sistema agora possui uma captura dual que permite gravações em tempo real através do MCP ou uploads de documentos curados.
   *(2026-05-03)*

2567. A migração ADR-001 está em curso para aposentar a Mem0 SaaS, sendo o Hub Qdrant a fonte da verdade.
   *(2026-05-03)*

2568. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2569. O arquivo `gus-identity.md` é redundante com bootstrap e está desatualizado.
   *(2026-05-03)*

2570. A stack de memória está em estado intermediário arriscado, com 3 produções simultâneas de fragmentos e 4 vezes o custo por chamada LLM devido a duas requisições para textos semelhantes.
   *(2026-05-03)*

2571. As decisões arquiteturais são documentadas no repositório Gus, como por exemplo a migração de Mem0 SaaS para o Hub Qdrant.
   *(2026-05-03)*

2572. A migração para o Hub Qdrant está em curso e pretende aposentar a Mem0 SaaS, que é a fonte da verdade no momento.
   *(2026-05-03)*

2573. A introdução de arquivos 'lazy' pode auxiliar no carregamento eficiente de recursos usados esporadicamente.
   *(2026-05-03)*

2574. Gustavo é anestesiologista e não programa — toda implementação passa pelo Gus ou Tiogu.
   *(2026-05-03)*

2575. Gustavo tem um projeto chamado `claude-code` onde a porta principal é `claude.ai`.
   *(2026-05-02)*

2576. O arquivo gus-identity.md mistura conteúdos que deveriam ser exclusivos do bot Telegram com informações aplicáveis a outras portas, criando confusão no sistema.
   *(2026-05-04)*

2577. A coleta dual de modelos no curador (Haiku e GPT-4o-mini) deve ser concluída até 12/05/2026, quando Gustavo escolherá o modelo definitivo.
   *(2026-05-03)*

2578. Gustavo Pratti de Barros é anestesiologista baseado no Rio de Janeiro, atuando na Dimagem, uma clínica de imagem diagnóstica com três unidades: Nova Iguaçu, Taquara e São Gonçalo.
   *(2026-05-03)*

2579. A atualização do SDK Anthropic para a versão 0.97 foi realizada sem a necessidade de adaptações estruturais significativas.
   *(2026-05-03)*

2580. O sistema Gus é um agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa).
   *(2026-05-03)*

2581. O sistema Gus é um agente pessoal multi-porta, incluindo Telegram, Claude Code e Claude Chat com um MCP Connector.
   *(2026-05-04)*

2582. Hub Qdrant é a fonte da verdade para o sistema de agente pessoal multi-porta.
   *(2026-05-03)*

2583. O estado de migração **ADR-001** está em curso, com a coleta dual de modelos no curador (Haiku × GPT-4o-mini).
   *(2026-05-03)*

2584. Gustavo é anestesiologista e não programa.
   *(2026-05-03)*

2585. A auditoria da stack de memória revelou que a variável `MCP_URL_SECRET` não está sendo logada, melhorando a segurança.
   *(2026-05-03)*

2586. A fase 1 do projeto envolve a criação de testes e a validação de comportamentos esperados do bot, com um total de 163 testes automatizados sendo implementados.
   *(2026-05-02)*

2587. O arquivo gus-bootstrap.md fornece um manual operacional do Gus, regras de comportamento e como cada porta usa o Hub.
   *(2026-05-03)*

2588. O sistema Gus é um agente pessoal multi-porta em produção, conectado ao Hub Qdrant.
   *(2026-05-04)*

2589. O Hub Qdrant é a fonte da verdade e armazena as memórias do Gus.
   *(2026-05-03)*

2590. O estado do projeto deve ser verificado após a configuração, realizando uma chamada à URL do health do MCP.
   *(2026-05-03)*

2591. O `MCP_URL_SECRET` deve ser configurado no Railway para proteger o acesso ao MCP.
   *(2026-05-02)*

2592. Gustavo Pratti de Barros é anestesiologista no Rio de Janeiro, atuando no Dimagem (clínica de imagem diagnóstica com 3 unidades: Nova Iguaçu, Taquara, São Gonçalo).
   *(2026-05-03)*

2593. A auditoria identificou a necessidade de integrar uma lógica clara para hierarquizar os canais de escrita do Chat.
   *(2026-05-03)*

2594. O estado da migração deve ser conferido através do histórico do workflow 'migrar-gus-para-hub'.
   *(2026-05-03)*

2595. Vou abrir branch 'claude/mcp-secret-no-log' agora para remover o segredo do log.
   *(2026-05-03)*

2596. Gustavo tem hipertireoidismo sob tratamento com Tapazol, acompanhado por um endocrinologista.
   *(2026-05-04)*

2597. O sistema principal de Gustavo "Gus" está em produção: um agente de IA multi-porta pessoal (bot do Telegram @Tiogubot, Claude Code, Claude Chat com conector MCP, Custom GPT em configuração, Alexa planejada). A base de memória foi migrada do Mem0 para o Hub Qdrant direto (ADR-001, concluído em 27/04/2026), agora com 1076+ fragmentos em dois cérebros (gustavo para fatos sobre ele, gus para autorreflexão do agente). O trabalho recente se concentrou em reforçar: o PR #72 corrigiu um erro 100% falho do curador (KeyError no template JSON), o PR #80 redigiu vazamento de segredos nos logs do MCP, e o PR #83 introduziu o bootstrap-v6 com dois caminhos de captura (MCP em tempo real + upload curado). O NeuroGus (visualização gráfica 3D do Hub) está totalmente projetado e desbloqueado uma vez que as decisões dos §§11.1-11.5 forem finalizadas. A publicação do Phronesis-Bench está em revisão/preparação para o Alignment Forum. O SaaS Mem0 está planejado para o fechamento após 12/05/2026, após a coleta dupla de curadores A/B (Anthropic Haiku × OpenAI GPT-4o-mini).
   *(2026-05-04)*

2598. A stack de memória está em estado intermediário arriscado, com risco moderado de perda silenciosa.
   *(2026-05-03)*

2599. O `MCP_URL_SECRET` foi criado para proteger as informações do Hub.
   *(2026-05-03)*

2600. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2601. O bot Telegram, conhecido como TioGu, utiliza um framework baseado em python-telegram-bot e tem como arquitetura principal o arquivo bot.py, que foi refatorado para maior modularidade.
   *(2026-05-04)*

2602. Os 4 arquivos principais dão 80% do contexto para qualquer aba nova.
   *(2026-05-03)*

2603. O estado final dos PRs já está no código + nos documentos gus-XX atualizados.
   *(2026-05-03)*

2604. Atualmente, a demanda Shakira pode seguir.
   *(2026-05-04)*

2605. As memórias com tipo de esquecimento 'protegido' não devem ser deletadas, conforme o que está definido no ciclo de vida.
   *(2026-05-03)*

2606. Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e `_frontmatter-referencia.md` que é só template.
   *(2026-05-03)*

2607. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/` (algumas com nome quebrado — "Documento sem título.md" provavelmente é lixo de sync).
   *(2026-05-03)*

2608. Estava na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

2609. O que é o Gus: Sistema de agente pessoal multi-porta com memória central no Hub Qdrant.
   *(2026-05-03)*

2610. Gustavo Pratti de Barros é anestesiologista no Rio de Janeiro, atuando no Dimagem, clínica de imagem diagnóstica com 3 unidades: Nova Iguaçu, Taquara, São Gonçalo.
   *(2026-05-03)*

2611. PR #79 introduz novo canal Gus-Sync/dialogos/inbox-gustavo/{chat,code,tiogu}/ no Drive.
   *(2026-05-03)*

2612. O sistema tenta buscar em ambos os lugares (Hub e Mem0) na leitura e na deleção do fragmento, o que pode gerar inconsistências.
   *(2026-05-03)*

2613. Gustavo é anestesiologista e não programa — toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

2614. PR #74 introduziu testes de regressão para correção do bug `format()` no curador.
   *(2026-05-03)*

2615. O estado final dos PRs já está no código e nos docs gus-XX atualizados.
   *(2026-05-03)*

2616. O segredo não deve ser compartilhado, apenas utilizado nos locais necessários.
   *(2026-05-03)*

2617. O schema gus-18 é um contrato que promete ciclos de vida para os fragmentos, porém essa implementação ainda está pendente.
   *(2026-05-03)*

2618. A demanda atual para o Gus inclui configurar o MCP_URL_SECRET no Railway e recadastrar o Connector claude.ai.
   *(2026-05-03)*

2619. As demandas pendentes na porta de Claude Code incluem a captura multiporta, curador bidirecional cron e OAuth para sincronização com o Drive.
   *(2026-05-03)*

2620. A arquitetura do bot é composta por diferentes módulos, incluindo bot.py, llm.py, memory.py, tools.py e media.py.
   *(2026-05-02)*

2621. As quatro demandas pendentes são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e `_frontmatter-referencia.md` é só um template.
   *(2026-05-04)*

2622. O bootstrap deve conter um TL;DR no topo para guiar o Chat na leitura.
   *(2026-05-03)*

2623. O número de fragmentos em 'gustavo' foi 204, enquanto o número de fragmentos em 'gus' é 4.
   *(2026-05-03)*

2624. A ADR-001 está em curso, visando aposentar o Mem0 SaaS e usar o Hub Qdrant como a fonte da verdade.
   *(2026-05-03)*

2625. O estado de migração indica que o Hub Qdrant está se tornando a fonte da verdade, aposentando o Mem0 SaaS.
   *(2026-05-03)*

2626. A Fase 1 de saneamento do TioGu foi concluída com 163 testes verdes e ajustes em `bot.py/llm.py/memory.py`.
   *(2026-05-03)*

2627. 1. Gustavo quer apagar pendências que estão ultrapassadas — decisão tomada de limpar o backlog desatualizado.
2. Hub contém 204 memórias no total (auditoria de 7:51 BRT).
3. Migração Mem0 → Qdrant ainda não foi concluída; ambos coexistem no momento — o grosso das 204 memórias ainda está no Mem0, apenas ~3 fragmentos indexados no Qdrant com user_id=gustavo.
4. Existem 2 memórias desatualizadas identificadas para deleção: `2b68d542` (sobre workflow falhando) e `cb860bdb` (sobre PR #10 e importações).
5. Workflow de migração para consolidar tudo no Hub Qdrant está disponível e pode ser rodado a critério de Gustavo.
   *(2026-04-27)*

2628. O PR #67 introduziu um curador chat bidirecional (Sonnet 4.6 + GPT-4o) que salva em `gustavo` e `gus`, mas apenas processa arquivos .md carregados manualmente.
   *(2026-05-02)*

2629. O Hub não está registrando fragmentos desde as 03h.
   *(2026-05-02)*

2630. PR #76 migrou para WIF e você já configurou os secrets.
   *(2026-05-03)*

2631. O sistema atual da memória contém 70% de fragmentos de baixa qualidade, que deverão ser limpos na Fase 1.7 do projeto.
   *(2026-05-03)*

2632. O sistema Gus está em produção e captura informações em tempo real.
   *(2026-05-03)*

2633. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

2634. Gustavo é falante nativo de português, baseado no Rio de Janeiro. Interesses intelectuais fortes em segurança em IA, filosofia e systems thinking.
   *(2026-05-04)*

2635. O `gus-08-plano-proximos-passos.md` (24/04) está muito desatualizado e precisa ser reescrito ou marcado como histórico.
   *(2026-05-02)*

2636. O arquivo `gus-bootstrap.md` deve conter um TL;DR, quem é Gustavo, quem o Gus é nesta porta, capacidades e limites, diretrizes universais, estilo de resposta, caminhos de captura e regras duras.
   *(2026-05-04)*

2637. Está em aberto a validação da eficácia do sistema de captura em tempo real durante as interações.
   *(2026-05-03)*

2638. Requer a autorização de um usuário para o código do projeto, assim como a necessidade de sincronização entre buckets de dados.
   *(2026-05-02)*

2639. Dentro do código da stack de memória, o fallback para Mem0 SaaS ainda existe.
   *(2026-05-03)*

2640. A auditoria revelou que o sistema de captura via Telegram está com erro 400 recorrente, resultando em falha na ingestão do Chat.
   *(2026-05-04)*

2641. As respostas geradas pelo bot podem conter informações sensíveis, e um mecanismo de redaction foi implementado para ajudar a proteger dados do usuário.
   *(2026-05-02)*

2642. Gustavo é anestesiologista e não programa, toda implementação passa pelo Gus.
   *(2026-05-03)*

2643. Gus está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

2644. É necessário implementar um serviço de conta no Google Cloud para evitar a expiração do token OAuth nas syncs do Drive.
   *(2026-05-02)*

2645. Após a geração do segredo, deve-se setar a variável MCP_URL_SECRET no serviço gus-mcp-server no Railway.
   *(2026-05-03)*

2646. O arquivo gus-estado-atual.md é atualizado automaticamente a cada 15 minutos usando uma rotina cron.
   *(2026-05-04)*

2647. O estado de migração ADR-001 está em curso, visando aposentar o Mem0 SaaS.
   *(2026-05-03)*

2648. A coleta de dados do Mem0 SaaS foi interrompida em 26/04/2026.
   *(2026-05-03)*

2649. A fase 1 inclui a criação de testes de unidade para o bot e suas funcionalidades.
   *(2026-05-02)*

2650. Existem 3 demandas paradas em dialogos/inbox-claude-code/: 2026-05-01-captura-multiporta-curador.md, 2026-05-01-drive-sync-oauth-fix.md e _frontmatter-referencia.md (este é template, não é demanda).
   *(2026-05-02)*

2651. Hub é mais fresco que 'gus-estado-atual.md', que é um snapshot das 03h.
   *(2026-05-03)*

2652. As referências a features removidas e o status do projeto precisam ser atualizados em algum momento.
   *(2026-05-04)*

2653. Ação proposta: rodar script que pega tudo do Mem0 SaaS e grava JSON em `historico/mem0-export-final-2026-05-02.json`.
   *(2026-05-03)*

2654. O curador está em estado crítico devido a múltiplas chamadas LLM feitas na mesma entrada, resultando em cruzamento de dados entre as identidades operacionais Gustavo e Gus.
   *(2026-05-03)*

2655. O estado final dos PRs já está no código e nos docs gus-XX atualizados.
   *(2026-05-03)*

2656. A auditoria considera que o `tipo_esquecimento` no schema gus-18 não está sendo implementado.
   *(2026-05-03)*

2657. Gustavo Pratti de Barros é anestesiologista no Dimagem, com 3 unidades no Rio de Janeiro, e pesquisador independente em IA.
   *(2026-05-03)*

2658. Os 204 fragmentos histórico estão no Mem0 SaaS e não foram migrados para o Hub Qdrant.
   *(2026-05-03)*

2659. A auto-capacitação dos bots é feita por um processo de A/B observável, onde Haiku × GPT-4o-mini permite coletar dados para comparações.
   *(2026-05-02)*

2660. O bot utiliza um sistema de fallback para diferentes provedores de LLM, possibilitando resiliência e continuidade de funcionamento.
   *(2026-05-04)*

2661. A captura real-time do sistema Gus está funcionando.
   *(2026-05-04)*

2662. O plano é finalizar a refatoração do bootstrap e matar o `gus-identity.md`, consolidando suas informações no `gus-bootstrap.md` assim que as mudanças forem aprovadas.
   *(2026-05-04)*

2663. A segunda demanda é intitulada `2026-05-01-drive-sync-oauth-fix.md`.
   *(2026-05-02)*

2664. Atualmente, o TioGu apresenta 21 ferramentas, que estão organizadas em um arquivo chamado tools.py. Essas ferramentas incluem funções para manipulação de mídia e interação com APIs de LLM.
   *(2026-05-02)*

2665. O retro-engine registra 'no-op: anthropic_missing' quando o ANTHROPIC_API_KEY não está disponível no ambiente.
   *(2026-05-03)*

2666. O projeto está na fase de migração do Mem0 SaaS para o Hub Qdrant, com uma data de conclusão prevista para 12/05/2026.
   *(2026-05-03)*

2667. O sistema de captura de memória do bot registra donadores e usuários, com atenção ao tratamento de informações pessoais.
   *(2026-05-04)*

2668. O sistema Gus está em produção e é um agente pessoal multi-porta que integra Telegram, Claude Code, Claude Chat com MCP Connector, Custom GPT e Alexa planejada.
   *(2026-05-03)*

2669. Gustavo Pratti de Barros tem um projeto de integração com um agente pessoal conhecido como Gus.
   *(2026-05-02)*

2670. Os protocolos devem ser quebrados em arquivos separados e carregados sob demanda.
   *(2026-05-03)*

2671. O TioGu deve ser capaz de lidar com erros e problemas de conexão com um sistema de retry e logging aprimorados.
   *(2026-05-02)*

2672. O histórico de feedback do Stop hook registra "no-op: anthropic_missing" e segue.
   *(2026-05-04)*

2673. O estado final dos PRs já tá no código + nos docs gus-XX atualizados.
   *(2026-05-03)*

2674. Solicita-se a revisão e merge do PR que consolida o gus-identity.md no bootstrap.
   *(2026-05-03)*

2675. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/` (algumas com nome quebrado — "Documento sem título.md" provavelmente é lixo de sync).
   *(2026-05-03)*

2676. A Fase 1 do projeto inclui a limpeza ativa do Hub e a remoção do fallback Mem0.
   *(2026-05-03)*

2677. Revisão do `link` deve indicar quais candidatos são apx dentro da limitação de `jaccard ≥ 0.7`.
   *(2026-05-03)*

2678. Gustavo Pratti de Barros é um anestesiologista baseado no Rio de Janeiro, trabalhando na Dimagem (clínica de imagem diagnóstica, três unidades: Nova Iguaçu, Taquara, São Gonçalo). Além do trabalho clínico, ele é um pesquisador independente de IA e construtor de sistemas operando em múltiplos projetos de pesquisa e produto simultaneamente.
   *(2026-05-04)*

2679. O log mostra 'salvo (curador: gpt, janela: ...)' — confirma que PR #72 funciona em produção.
   *(2026-05-03)*

2680. Gustavo é anestesiologista e não programa. Toda implementação passa pelo Gus.
   *(2026-05-03)*

2681. O bot é baseado em python-telegram-bot e possui backend integrado com FastAPI.
   *(2026-05-03)*

2682. Após a implementação das demandas, haverá necessidade de decidir sobre a hierarquia dos 3 canais de escrita do Chat: real-time MCP, upload .md curado e demanda inbox-code.
   *(2026-05-02)*

2683. O curador retorna os memórias com estado 'ativo' para sempre devido a falhas na implementação do lifecycle.
   *(2026-05-03)*

2684. Foi implementado um fluxo que permite que o TioGu envie alertas proativos sobre o uso do custo em tempo real.
   *(2026-05-03)*

2685. A stack de memória está em estado intermediário arriscado, com 204 fragmentos não-migrados e um código de leitura que ainda faz fallback para Mem0.
   *(2026-05-03)*

2686. Os quatro principais arquivos obrigatórios para qualquer aba nova são: `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md`, e `estado-atual.md`. Esses quatro dão 80% do contexto para qualquer aba nova.
   *(2026-05-03)*

2687. As opções para solucionar o problema de Drive sync incluem renovar o OAuth ou utilizar uma Service Account.
   *(2026-05-02)*

2688. Aba nova só precisa olhar PRs se houver um bug específico relacionado ao código que foi mexido recentemente ou se for referido diretamente em uma conversa.
   *(2026-05-02)*

2689. O Hub não está implementando corretamente o schema gus-18, como o ciclo de vida de 'peso', 'acessos' e 'confirmacoes'.
   *(2026-05-03)*

2690. Gustavo é anestesiologista.
   *(2026-05-03)*

2691. A captura pela porta Claude Chat está sendo testada atualmente.
   *(2026-05-03)*

2692. O estado final dos PRs já está no código e nos docs gus-XX atualizados.
   *(2026-05-03)*

2693. O curador Telegram está apresentando um erro 400 devido a falhas nos parâmetros.
   *(2026-05-02)*

2694. O sistema de captura de fragmentos é dividido em três caminhos: Telegram, Claude Chat e Claude Code.
   *(2026-05-03)*

2695. ADR-001 está em curso: aposentar Mem0 SaaS, Hub Qdrant é fonte da verdade.
   *(2026-05-03)*

2696. As demandas pendentes no inbox são: Ativar `MCP_URL_SECRET` no Railway, recadastrar Connector claude.ai e localizar mock HTML do NeuroGus.
   *(2026-05-02)*

2697. A auto-notificação para TioGu deve ser mantida.
   *(2026-05-03)*

2698. A sessão estava em atraso em relação ao arquivo estado atual, que parou em 27/04/2026.
   *(2026-05-03)*

2699. O bot Telegram TioGu utiliza uma arquitetura multi-provider, com recuperação de falhas entre provedores de LLM (Large Language Models).
   *(2026-05-04)*

2700. O bot do Telegram, TioGu, possui ~21 ferramentas distintas integradas.
   *(2026-05-03)*

2701. Ele é falante nativo de português e baseado no Rio de Janeiro.
   *(2026-05-04)*

2702. Mem0 SaaS está aposentado, agora o Hub Qdrant é a fonte de verdade.
   *(2026-05-03)*

2703. O passo 3 é validar que o log não vaza mais com o novo secret.
   *(2026-05-03)*

2704. A refatoração de bot.py resultou na divisão do código em módulos especializados dentro da pasta handlers, permitindo que cada parte tenha responsabilidades mais definidas e facilitando o teste e a manutenção.
   *(2026-05-04)*

2705. O projeto Phronesis-Bench é uma iniciativa para a publicação de um documento chamado 'Prudência Performática'.
   *(2026-05-04)*

2706. A stack de memória do Gus está em estado intermediário arriscado por causa da coexistência do Hub e da coleção legada.
   *(2026-05-03)*

2707. O `_estado-atual.md` (27/04) está desatualizado — git log mostra muita coisa depois.
   *(2026-05-02)*

2708. O Hub Qdrant é a fonte da verdade, com memórias centralizadas.
   *(2026-05-03)*

2709. Um dos pontos críticos identificados no TioGu é a falta de um PII scan na resposta do bot, o que representa risco de vazamento de dados.
   *(2026-05-02)*

2710. Gustavo é anestesiologista e não programa, toda implementação passa pelo Gus.
   *(2026-05-03)*

2711. Na sessão anterior, temos 4 arquivos obrigatórios que dão 80% do contexto pra qualquer aba nova.
   *(2026-05-03)*

2712. A captura envolve os tipos mandatórios: decisao, preferencia, fato e biografico, além de meta_reflexao opcional.
   *(2026-05-03)*

2713. O bot Telegram possui 21 ferramentas e suporta multimídia, prompt caching e validação manual.
   *(2026-05-03)*

2714. É importante revisar e remover informações desatualizadas na memória do sistema Claude, como a menção ao Mem0 e ao hackathon de abril.
   *(2026-05-04)*

2715. Gustavo é anestesiologista e não programa; toda implementação passa pelo Gus.
   *(2026-05-03)*

2716. O passo 2 consiste em recadastrar o Connector no claude.ai após a mudança da URL do MCP.
   *(2026-05-03)*

2717. Gustavo possui hipertireoidismo em tratamento.
   *(2026-05-04)*

2718. Os quatro arquivos do core obrigatório dão 80% do contexto pra qualquer aba nova.
   *(2026-05-03)*

2719. O Drive sync GitHub→Drive parou em 01/05 às 14:38Z devido ao token OAuth ter expirado.
   *(2026-05-03)*

2720. A migração do Mem0 SaaS é necessária para tornar o Hub Qdrant a fonte da verdade.
   *(2026-05-03)*

2721. Há 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2722. Decisão arquitetural não-óbvia é documentada nas descrições dos PRs.
   *(2026-05-03)*

2723. O assistente pode ler o arquivo `_estado-atual.md` para pegar handoff da última sessão.
   *(2026-05-02)*

2724. No último mês, finalizada a documentacao 'Prudência Performática' para revisão no Alignment Forum.
   *(2026-05-03)*

2725. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e a hipótese é que o refresh token OAuth expirou.
   *(2026-05-02)*

2726. O sistema tem 204 fragmentos não-migrados na coleção legada `gus` e o código de leitura ainda faz fallback para ela.
   *(2026-05-03)*

2727. A arquitetura do bot TioGu é um monólito, dificultando sua manutenção e escalabilidade.
   *(2026-05-02)*

2728. O bootstrap pode ser dividido em arquivos funcionais para melhorar a eficiência.
   *(2026-05-04)*

2729. Gustavo é anestesiologista e não programa — toda implementação passa pelo Gus/Tiogu.
   *(2026-05-03)*

2730. O estado final dos PRs já está no código + nos docs gus-XX atualizados.
   *(2026-05-03)*

2731. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2732. O sistema 'Gus' — agente pessoal multi-porta — está em produção com quatro portas ativas: Telegram, Claude Code, Claude Chat e Custom GPT.
   *(2026-05-04)*

2733. URL secret protege e destrava escrita real-time do Chat (ingestar_fragmento).
   *(2026-05-03)*

2734. O system_prompt.md é muito extenso e possui drift, com 794 linhas e inconsistências com os tools implementados.
   *(2026-05-02)*

2735. A URL do Connector muda para /{secret}/mcp. É necessário recriar o Connector após mudar o secreto.
   *(2026-05-03)*

2736. A estrutura geral do Chat envolve dois canais de escrita: MCP em tempo real e o upload de curadoria com latência.
   *(2026-05-03)*

2737. A migração deve ocorrer até 12/05/2026, após o qual Gustavo escolherá o modelo definitivo.
   *(2026-05-03)*

2738. As demandas pendentes na porta Claude incluem uma possibilidade de capturar multiporta curador, resolver um bug no Drive sync OAuth e consolidar pendências do Claude Chat.
   *(2026-05-03)*

2739. A URL do Connector no claude.ai deve ser atualizada após o passo 1.
   *(2026-05-03)*

2740. Há 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2741. A migração ADR-001 está em curso e visa aposentar Mem0 SaaS.
   *(2026-05-03)*

2742. Gustavo é anestesiologista, não programa — toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

2743. A migração de Mem0 SaaS para Hub Qdrant é a fonte da verdade e conclui a coleta dual de modelos no curador, que terminará em 12/05/2026.
   *(2026-05-03)*

2744. A mudança em `bot.py` permite que novos desenvolvedores entendam rapidamente a estrutura do código e contribuam mais facilmente na evolução do bot.
   *(2026-05-04)*

2745. A pasta dialogos/inbox-claude-code/ contém as demandas pendentes que precisam ser resolvidas.
   *(2026-05-03)*

2746. O estado atual do projeto é a migração da Mem0 SaaS para o Hub Qdrant, sendo a coleta dual de modelos no curador com Haiku e GPT-4o-mini.
   *(2026-05-03)*

2747. As demandas pendentes para o Claude Code incluem capturar multiporta e corrigir sync OAuth.
   *(2026-05-04)*

2748. O fluxo de migração do `gus` para o `gus_hub` ainda não foi executado.
   *(2026-05-03)*

2749. A estrutura de decisão para o curador envolve a manutenção dos arquivos antigos no histórico e a importação planejada de dados novos após a correção de inconsistências.
   *(2026-05-03)*

2750. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

2751. Demanda '2026-05-01-captura-multiporta-curador.md' foi arquivada após implementação.
   *(2026-05-03)*

2752. A porta Chat reflete uma longa introspecção. Embora a identidade seja a mesma de outros canais, cada canal tem seu estilo de interação.
   *(2026-05-03)*

2753. O sistema está em estado intermediário arriscado, podendo levar à poluição de dados entre os brains.
   *(2026-05-03)*

2754. A notificação automática no Telegram para novas demandas na pasta TioGu será mantida.
   *(2026-05-03)*

2755. O `_estado-atual.md` e `gus-26-status-consolidado.md` estão desatualizados e não refletem PRs recentes.
   *(2026-05-02)*

2756. As frentes de trabalho do 'Gus' incluem Telegram, Code, Chat e um Custom GPT em configuração.
   *(2026-05-03)*

2757. Gustavo é anestesiologista e utiliza o sistema de agente pessoal multi-porta chamado Gus.
   *(2026-05-03)*

2758. A demanda de limpeza do Hub atual deve ocorrer na Fase 1.7.
   *(2026-05-03)*

2759. O bot TioGu é um sistema multi-porta que se conecta ao Telegram e utiliza o Hub Qdrant como memória central.
   *(2026-05-02)*

2760. O MCP está público — qualquer scanner que descobrir a URL Railway lê todo o Hub. URL secret protege.
   *(2026-05-03)*

2761. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026, após isso Gustavo escolherá um modelo definitivo.
   *(2026-05-03)*

2762. O sistema Gus — agente pessoal multi-porta — está em produção com quatro portas ativas: Telegram, Claude Code, Claude Chat e Custom GPT.
   *(2026-05-04)*

2763. O arquivo gerado pelo retro-engine é um log automático e não ofensivo, e documenta ausência de uma variável de ambiente necessária.
   *(2026-05-02)*

2764. A auditoria diária é cega para o brain `gus` e classifica somente por keywords.
   *(2026-05-03)*

2765. O sistema tem suporte a vídeos, documentos e mídia através de múltiplos handlers.
   *(2026-05-04)*

2766. O hook de scan_sensivel.py foi ajustado para permitir a execução de testes em `tests/` sem causar bloqueios.
   *(2026-05-02)*

2767. Mem0 SaaS tem 204 fragmentos no brain `gustavo` e 4 no brain `gus`.
   *(2026-05-03)*

2768. A demanda `2026-05-01-captura-multiporta-curador.md` precisa de um gatilho proativo no Chat.
   *(2026-05-02)*

2769. O algoritmo de deduplicação precisa ser implementado para evitar que fragmentos duplicados sejam criados no sistema.
   *(2026-05-03)*

2770. Existem pendências, como a validação de OAuth para o Drive e a remoção de memórias legadas.
   *(2026-05-03)*

2771. O conteúdo retirado do Mem0 SaaS pode ser mantido em 'historico/' para consulta futura, enquanto novas importações são planejadas.
   *(2026-05-03)*

2772. A seção "Personalidade do Gus (somente Telegram)" deve ser migrada para o arquivo system_prompt.md.
   *(2026-05-04)*

2773. Gustavo acompanha mercados financeiros e educação em investimentos.
   *(2026-05-04)*

2774. A função `print_demands` deve ser movida para a pasta `integrations/` para melhor organização, já que trata de um caso específico da clínica do Gustavo.
   *(2026-05-02)*

2775. O commit do log do retro-engine foi realizado na branch `claude/project-discussion-fkfA8`.
   *(2026-05-02)*

2776. O core obrigatório deve ser lido em qualquer aba nova.
   *(2026-05-03)*

2777. Vou ignorar a Anthropic e créditos, vou mexer nisso depois.
   *(2026-05-04)*

2778. O Hub atual contém 40 fragmentos totais, sendo 20 do brain `gustavo` e 20 do brain `gus`.
   *(2026-05-03)*

2779. A coleta dual de modelos no curador (Haiku e GPT-4o-mini) termina em 12/05/2026, após o que Gustavo escolherá o modelo definitivo.
   *(2026-05-03)*

2780. Hub Qdrant é a nova fonte da verdade do sistema Gus.
   *(2026-05-03)*

2781. Deve-se recadastrar o Connector no claude.ai após a atualização do path do MCP.
   *(2026-05-03)*

2782. Aba nova só precisa olhar PRs se você falar que está quebrando algo depois do PR específico.
   *(2026-05-03)*

2783. O curador híbrido deve ser robusto para capturar informações, mas a poluição silenciosa de dados não classificados é uma preocupação.
   *(2026-05-03)*

2784. O formato do commit é importante, pois o CI roda automaticamente a cada push no branch main.
   *(2026-05-02)*

2785. O sistema de memória possui 4 entradas simultâneas (Telegram, Claude Chat, Claude Code, MCP claude.ai).
   *(2026-05-03)*

2786. O sistema utiliza um modelo de curador híbrido para coleta dual.
   *(2026-05-02)*

2787. A coleção `gus` está vazia — 204 fragmentos históricos prometidos não existem na coleção Qdrant.
   *(2026-05-03)*

2788. O `_estado-atual.md` está desatualizado em relação aos PRs mergeados e deve ser atualizado em algum momento.
   *(2026-05-02)*

2789. O MCP server é público e pode ser acessado por qualquer scanner que descobrir a URL.
   *(2026-05-03)*

2790. Gustavo é anestesiologista.
   *(2026-05-03)*

2791. Recentemente, Gustavo focou em fortalecer o sistema de Gus: PR #72 corrigiu um bug no curador (erro KeyError no template JSON), PR #80 redigiu vazamentos de segredo nos logs MCP, e PR #83 introduziu bootstrap-v6 com dois caminhos de captura (real-time MCP + upload curado).
   *(2026-05-04)*

2792. O documento 'Prudência Performática' está em revisão para o Alignment Forum.
   *(2026-05-03)*

2793. O retro-engine registra 'no-op: anthropic_missing' e segue.
   *(2026-05-03)*

2794. A seção 'Personalidade do Gus (somente Telegram)' será migrada para o arquivo 'gus/system_prompt.md'.
   *(2026-05-04)*

2795. O log do retro-engine está em claude/greeting-checkin-94weM.
   *(2026-05-03)*

2796. O arquivo 'dialogos/_bootstrap/gus-estado-atual.md' é um snapshot auto-gerado pelo cron às 03h, que apresenta o estado atual do Hub.
   *(2026-05-03)*

2797. A auditoria diária é cega para o brain `gus` e classifica por keywords ignorando o `area` já preenchido pelo curador.
   *(2026-05-03)*

2798. O bootstrap carrega muita informação que é uso eventual.
   *(2026-05-03)*

2799. A seção 'Personalidade do Gus (somente Telegram)' deve ser migrada para o `gus/system_prompt.md`, que é o lugar apropriado para as regras do bot.
   *(2026-05-04)*

2800. O usuário pode escolher atacar alguma das demandas ou falar sobre outra coisa.
   *(2026-05-02)*

2801. O arquivo `dialogos/_bootstrap/gus-identity.md` contém informações sobre quem é o Gustavo e quem é o Gus enquanto entidade.
   *(2026-05-02)*

2802. O Hub é considerado a fonte da verdade no sistema, espelhando arquivos .md no GitHub.
   *(2026-05-03)*

2803. Se uma aba tem MCP gus-hub conectado, deve-se utilizar as ferramentas ego_cache_atual(), fragmentos_recentes(horas=24) e contar_fragmentos() para obter informações.
   *(2026-05-02)*

2804. Atualmente, os projetos ativos incluem Phronesis-Bench, NeuroGus, MGE/MGX, TER e Axon.
   *(2026-05-03)*

2805. As ferramentas do bot somam 21 implementações, e o sistema prompt contém drift, mencionando 22 ferramentas.
   *(2026-05-02)*

2806. A decisão ADR-001 está em curso para aposentar a Mem0 SaaS, enquanto o Hub Qdrant será a fonte da verdade.
   *(2026-05-03)*

2807. Gustavo é anestesiologista e não programa, sendo que toda implementação passa pelo Gus ou Tiogu.
   *(2026-05-03)*

2808. O registro das atualizações do sistema é feito pelo auditoria diária em 'auditoria_hub.py'.
   *(2026-05-03)*

2809. Hub Qdrant é a fonte da verdade.
   *(2026-05-03)*

2810. O `_estado-atual.md` da pasta projetos/gus está desatualizado e foi gerado em 27/04.
   *(2026-05-03)*

2811. O `_estado-atual.md` (27/04) e `gus-26-status-consolidado.md` (26/04) estão desatualizados.
   *(2026-05-02)*

2812. O Hub Qdrant é a fonte da verdade, com arquivos .md no GitHub, espelhados no Drive.
   *(2026-05-03)*

2813. A migração para o Hub Qdrant é determinada pela decisão ADR-001, que aposentará o Mem0 SaaS.
   *(2026-05-03)*

2814. O modo de operação é single user com chat_id allowlist, em ambiente Railway 24/7.
   *(2026-05-03)*

2815. O sistema Gus é um agente pessoal multi-porta construído sobre o Hub Qdrant com vários projetos ativos.
   *(2026-05-04)*

2816. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e a hipótese é que o refresh token OAuth expirou.
   *(2026-05-02)*

2817. As chamadas para o curador em TioGu e Claude Chat rodam o curador duas vezes, resultando em 4 chamadas de LLM por input.
   *(2026-05-03)*

2818. A auditoria diária do Hub não contabiliza fragmentos do brain Gus, resultando em uma visão distorcida do sistema.
   *(2026-05-03)*

2819. A maioria dos fragmentos do Mem0 SaaS estão em inglês, enquanto o Hub contém fragmentos em português.
   *(2026-05-03)*

2820. As ações a serem tomadas incluem apagar `MEM0_API_KEY` em Railway e GitHub Secrets.
   *(2026-05-03)*

2821. O estado final dos pull requests já está no código + nos documentos atualizados, enquanto os pull requests descritos apenas relatam o caminho seguido e não o estado atual.
   *(2026-05-03)*

2822. Gus sugere combinar as sessões do `_estado-atual.md` da Fase 1 TioGu com a auditoria do Chat.
   *(2026-05-02)*

2823. O Hub Qdrant é a fonte da verdade para o sistema de agente pessoal.
   *(2026-05-03)*

2824. NeuroGus é um projeto que fornece visualização do Hub.
   *(2026-05-04)*

2825. O Gus, agente pessoal do Gustavo Pratti de Barros, está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

2826. Tem 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

2827. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa para resolver o problema de sync do Drive, que pode estar relacionado à expiração do token OAuth.
   *(2026-05-02)*

2828. O fluxo de trabalho a seguir inclui uma limpeza no Hub atual antes da importação dos 204 fragmentos.
   *(2026-05-03)*

2829. O método de auditoria diária é cego para o brain 'gus' e classifica fragmentos apenas por keywords, ignorando a área preenchida pelo curador.
   *(2026-05-03)*

2830. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2831. Atualmente, o Gus está ativo em projetos como Phronesis-Bench, NeuroGus e Axon.
   *(2026-05-03)*

2832. Gus está na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2833. A coleta dual de modelos no curador (Haiku × GPT-4o-mini, mudou de Sonnet em 29/04 por custo/resiliência) termina em 12/05/2026.
   *(2026-05-03)*

2834. O schema gus-18 promete um lifecycle para os fragmentos, mas a implementação atual não atualiza os dados.
   *(2026-05-03)*

2835. Estou aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2836. O protocolo de ativação Gus é acionado quando a palavra 'Gus' aparece na mensagem de abertura.
   *(2026-05-03)*

2837. O core do sistema é constituído pelo arquivo `gus-bootstrap.md`, que deve conter informações essenciais para a operação do Chat.
   *(2026-05-03)*

2838. A captação de fragmentos para o Hub ocorre através de 3 produções simultâneas de fragmentos: Telegram, Chat e Code.
   *(2026-05-03)*

2839. Se o conteúdo do Mem0 SaaS é irrecuperável, o próximo passo é começar a Fase 1.
   *(2026-05-03)*

2840. O Hub Qdrant tem como objetivo ser a fonte da verdade do sistema.
   *(2026-05-03)*

2841. A memória central do Gus é mantida no Hub Qdrant, armazenando arquivos .md no GitHub e espelhados no Drive.
   *(2026-05-03)*

2842. O fragmento de decisão sobre a migração do Mem0 SaaS foi registrado como ADR-001.
   *(2026-05-03)*

2843. O arquivo `gus-identity.md` é redundante com o bootstrap e está desatualizado.
   *(2026-05-03)*

2844. O nome da pasta `Gustavo/` pode ser padronizado e confirmado como `Gustavo/` antes da implementação.
   *(2026-05-03)*

2845. A captura de memória no Claude Code é interrompida quando a variável `ANTHROPIC_API_KEY` não está definida.
   *(2026-05-03)*

2846. A Fase 1 refinada do plano de auditoria e limpeza do Hub Qdrant inclui 9 itens.
   *(2026-05-03)*

2847. A auditoria da memória foi realizada em 02/05/2026.
   *(2026-05-03)*

2848. `_estado-atual.md` está desatualizado em relação às últimas atualizações do projeto.
   *(2026-05-02)*

2849. O bot opera com dependências como python-telegram-bot, anthropic SDK, openai, FastAPI e Qdrant.
   *(2026-05-03)*

2850. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2851. O bot Telegram, chamado TioGu, possui cerca de 21 ferramentas, multimídia, prompt caching e comunicação com o Hub Qdrant.
   *(2026-05-02)*

2852. A decisão de migração para o Hub Qdrant está definida no ADR-001, que busca aposentar o Mem0 SaaS como fonte de verdade.
   *(2026-05-03)*

2853. A stack de memória está em estado intermediário arriscado, com riscos de poluição cruzada e inconsistências.
   *(2026-05-03)*

2854. A demanda de sync do Drive está parada e espera-se uma decisão sobre o OAuth que pode ter expirado.
   *(2026-05-02)*

2855. A migração ADR-001 busca aposentar a Mem0 SaaS, com o Hub Qdrant como fonte da verdade.
   *(2026-05-03)*

2856. O projeto atualmente está em estado de migração, com a ADR-001 em curso para aposentar a Mem0 SaaS. O Hub Qdrant será a fonte da verdade.
   *(2026-05-03)*

2857. O bootstrap carrega muita informação que o Chat só usa em situações específicas, criando lastro desnecessário.
   *(2026-05-03)*

2858. A recomendação é manter os 204 fragmentos em 'historico/'.
   *(2026-05-03)*

2859. As decisões arquiteturais e detalhes técnicos do Gus são armazenados no Hub, mas alguns estão relacionados a ex-pacientes.
   *(2026-05-03)*

2860. O estado final dos PRs está no código e nos documentos gus-XX atualizados.
   *(2026-05-03)*

2861. A stack está em estado intermediário arriscado: o Hub Qdrant é a fonte nova, mas a coleção legada ainda tem fragmentos que não foram migrados.
   *(2026-05-03)*

2862. Os arquivos essenciais para contexto em qualquer nova aba são: gus-bootstrap.md, gus-identity.md, gus-estado-atual.md e _estado-atual.md.
   *(2026-05-03)*

2863. O fluxo de Dimagem foi unificado, removendo duplicidades e simplificando as instruções.
   *(2026-05-04)*

2864. O MCP está público — qualquer scanner que descobrir a URL Railway lê todo o Hub.
   *(2026-05-03)*

2865. Foram criados 2 JSONs estruturados com exames laboratoriais.
   *(2026-05-02)*

2866. O projeto Gus utiliza um sistema multi-porta com Hub Qdrant como memória central e GitHub como espelho de conhecimento.
   *(2026-05-04)*

2867. Decisão P1 captura Claude Chat: Opção A + C escolhida. Caminho 1 (default): real-time via MCP ingestar_fragmento durante a conversa (~1s latência, 2-4 fragmentos/conversa). Caminho 2 (escape): upload .md em Gus-Sync/dialogos/inbox-chat-raw/ pra sessões longas (>20 turnos) com curador post-hoc Sonnet 4.6 + GPT-4o.
   *(2026-05-02)*

2868. A coleção legada `gus` ainda está viva, e há fallback para a Mem0 em Leitura/Delete.
   *(2026-05-03)*

2869. O curador híbrido (Haiku + GPT) está ativo e recebe nova estrutura de feedback.
   *(2026-05-03)*

2870. A URL secret protege o MCP.
   *(2026-05-03)*

2871. Hub é mais fresco que [gus-estado-atual.md](http://gus-estado-atual.md) (que é snapshot das 03h). Sempre que possível, prefira tools MCP a arquivo .md.
   *(2026-05-03)*

2872. A migração da coleção legada Mem0 para o Hub Qdrant não foi realizada, resultando em uma fallback ativa em leitura.
   *(2026-05-03)*

2873. O Hub Qdrant é a fonte da verdade e deve coletar dados dos modelos de curador.
   *(2026-05-03)*

2874. O contrato schema gus-18 está parcialmente implementado.
   *(2026-05-03)*

2875. A demanda #1 da consolidação aborda a necessidade de corrigir o problema de sincronização do Drive.
   *(2026-05-03)*

2876. O projeto NeuroGus tem como objetivo visualizar o Hub Qdrant, de forma a melhorar a gestão e análise de fragmentos.
   *(2026-05-03)*

2877. A proposta é que a Opção A (manter em `historico/`) seja feita agora e a Opção C seja planejada para a Fase 5.
   *(2026-05-03)*

2878. A demanda de captura multiporta Claude Chat (`2026-05-01-captura-multiporta-curador.md`) está parcialmente resolvida, mas falta o gatilho proativo no Chat.
   *(2026-05-02)*

2879. Os arquivos core obrigatórios são `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md` e `projetos/gus/estado-atual.md`, que fornecem 80% do contexto para qualquer aba nova.
   *(2026-05-03)*

2880. O plano de migração ADR-001 está em curso para aposentar o Mem0 SaaS.
   *(2026-05-03)*

2881. Os arquivos com as demandas pendentes são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao.
   *(2026-05-03)*

2882. Identifiquei a necessidade de otimizar a leitura do bootstrap, retirando informações que o Chat não usa na maioria das interações.
   *(2026-05-04)*

2883. O curador híbrido estava falhando silenciosamente, gravando dados no Mem0 em vez de salvar no Hub Qdrant.
   *(2026-05-03)*

2884. O estado atual do projeto e suas atualizações são compilados em um arquivo chamado '_estado-atual.md'.
   *(2026-05-03)*

2885. Após a atualização, o Chat deve responder que não usa mais Mem0 e que agora é Hub Qdrant.
   *(2026-05-04)*

2886. O Hub Qdrant coleta dados e fragmentos do agente, mas há um risco de poluição silenciosa devido a entradas duplicadas.
   *(2026-05-03)*

2887. O Hub Qdrant está sendo usado como memória central no sistema multi-porta.
   *(2026-05-02)*

2888. O Drive Gus-Sync opera como um sistema de sincronização bidirecional com o GitHub.
   *(2026-05-03)*

2889. Hoje o MCP tá público — qualquer scanner que descobrir a URL Railway lê todo o Hub.
   *(2026-05-03)*

2890. Gustavo Pratti de Barros é anestesiologista e não programa, portanto, toda implementação passa pelo Gus e Tiogu.
   *(2026-05-03)*

2891. As entradas para o sistema incluem Telegram, Claude Chat e Claude Code, que produzem fragmentos simultaneamente.
   *(2026-05-03)*

2892. O estado do projeto Gus foi atualizado para refletir a migração de Mem0 para Hub Qdrant, com 1076+ fragmentos ativos.
   *(2026-05-04)*

2893. O Hub armazena dados em dois brains separados: 'gustavo' e 'gus'.
   *(2026-05-04)*

2894. O sistema de agente pessoal multi-porta conecta atividades em Telegram, Claude Chat e Claude Code.
   *(2026-05-03)*

2895. A auditoria da memória e do Hub Qdrant indicou riscos de poluição cruzada entre os brains do Gus e do Gustavo.
   *(2026-05-03)*

2896. A prática recomendada é não prestar atenção em pull requests a não ser que exista uma justificativa específica, pois as decisões arquitetônicas e o estado atual do projeto devem constar nos documentos.
   *(2026-05-03)*

2897. O sistema 'Gus' de Gustavo está em produção: um agente de IA multi-porta pessoal (bot do Telegram @Tiogubot, Claude Code, Claude Chat com conector MCP, Custom GPT em configuração, Alexa planejada). A base de memória foi migrada do Mem0 para o Hub Qdrant direto (ADR-001, completado em 27/04/2026), agora com mais de 1076 fragmentos em dois cérebros (gustavo para fatos sobre ele, gus para autorreflexão do agente).
   *(2026-05-04)*

2898. A coleção legada 'gus' ainda está viva, com fallback para Mem0 ativo em leitura e delete.
   *(2026-05-03)*

2899. A migração para o Hub Qdrant como fonte da verdade está em curso, com a data de término projetada para 12 de maio de 2026.
   *(2026-05-03)*

2900. O TioGu completou a Fase 1 de saneamento, que incluiu 163 testes verdes.
   *(2026-05-03)*

2901. O Hub Qdrant (`gus_hub`) é a fonte da verdade para o projeto.
   *(2026-05-03)*

2902. Os JSONs estruturados de exames LAFE de novembro de 2019 estão no caminho Gus-Sync/pessoal/saude/gus__2019-11-18__lafe.json.
   *(2026-05-02)*

2903. As decisões sobre a frequência da captura incluem três modos: agressivo, balanceado e conservador.
   *(2026-05-03)*

2904. No Hub Qdrant, toda memória é criada com estado 'ativo' e permanece nesse estado indefinidamente até a promoção para 'estável'.
   *(2026-05-03)*

2905. A coleção legada `gus` (Mem0 self-hosted) tem cerca de 204 fragmentos não-migrados e permanece em operação como fallback para leitura e delete.
   *(2026-05-03)*

2906. O projeto precisa ter um panorama geral, com um guia claro sobre o que fazer e como focar em assuntos específicos posteriormente.
   *(2026-05-03)*

2907. A decisão de eliminar o caminho `_fallback_mem0` visa evitar poluição silenciosa no Hub e garantir a integridade dos dados.
   *(2026-05-03)*

2908. Core obrigatório inclui o manual operacional do Gus, regras de comportamento, e o snapshot do Hub.
   *(2026-05-03)*

2909. O estado atual do projeto está sendo afetado pela migração em curso do Mem0 SaaS para o Hub Qdrant, com previsão para terminar em 12/05/2026.
   *(2026-05-03)*

2910. Os logs do Railway vazam o segredo do MCP em texto claro.
   *(2026-05-03)*

2911. Gus está na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2912. Se confirmar que a busca não contribui, abro PR mínimo no bootstrap pra deixar essa instrução explícita.
   *(2026-05-03)*

2913. Quatro demandas pendentes foram identificadas no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao.
   *(2026-05-03)*

2914. O bot Telegram, conhecido como TioGu, possui 21 ferramentas e utiliza caching de prompt.
   *(2026-05-03)*

2915. O Hub Qdrant é a nova fonte da verdade que vai coletar dados dos modelos de linguagem.
   *(2026-05-03)*

2916. É necessário gerar e configurar o segredo MCP_URL_SECRET no Railway.
   *(2026-05-03)*

2917. As demandas pendentes em 'dialogos/inbox-claude-code/' totalizam 6, com 3 demandas reais para captura multiporta, curador bidirecional cron, e drive-sync OAuth.
   *(2026-05-03)*

2918. O retro-engine registra 'no-op: anthropic_missing' e segue.
   *(2026-05-03)*

2919. A decisão de apagar o MEM0_API_KEY foi tomada após a exportação dos dados da memória antiga para que o sistema fique livre de poluição de dados não úteis.
   *(2026-05-03)*

2920. A receita para uma nova aba inclui ler os arquivos do core obrigatório e considerar o hub quando disponíveis.
   *(2026-05-03)*

2921. O conteúdo está seguro em `historico/`. Não há pressa para importar os 204 fragmentos do Mem0 SaaS.
   *(2026-05-03)*

2922. O fluxo Dimagem está documentado e possui um schema de quatro colunas.
   *(2026-05-04)*

2923. O volume Railway do bot é detectado automaticamente, permitindo a persistência do estado através de redeploys.
   *(2026-05-02)*

2924. A stack de memória apresenta três produções simultâneas de fragmentos.
   *(2026-05-03)*

2925. O segredo está em plain text no log.
   *(2026-05-03)*

2926. O arquivo gus-identity.md foi deletado para evitar redundância.
   *(2026-05-04)*

2927. A auditoria diária é cega para o brain gus e classifica por keywords ignorando o area que o curador já preencheu.
   *(2026-05-03)*

2928. O Gustavo é anestesiologista e não programa, toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

2929. O sistema tem um estado intermediário arriscado, onde o Hub Qdrant é a nova fonte, mas a coleção legada ainda contém fragmentos não migrados.
   *(2026-05-03)*

2930. Captura proativa de fragmentos através do Claude Chat foi implementada com sucesso. O sistema agora ingesta informações em tempo real, melhorando a fluidez do fluxo de trabalho.
   *(2026-05-03)*

2931. O segredo precisa ser regenerado para evitar exposição.
   *(2026-05-03)*

2932. A coleta dual de modelos Haiku e GPT-4o-mini deve ser concluída em 12/05/2026, quando Gustavo deverá escolher um modelo definitivo.
   *(2026-05-03)*

2933. O Hub Qdrant é a fonte da verdade do sistema Gus.
   *(2026-05-03)*

2934. O Hub é mais fresco que `gus-estado-atual.md` (snapshot das 03h).
   *(2026-05-03)*

2935. Os JSONs estruturados na pasta designada devem ser registrados.
   *(2026-05-03)*

2936. O script `limpeza_hub_dryrun.py` gera um relatório listando candidatos a delete sem de fato deletar nada.
   *(2026-05-03)*

2937. As informações sobre 'usos do sistema' devem ser corretas no bootstrap.
   *(2026-05-03)*

2938. Gustavo está investigando o ecossistema e construindo ferramentas, incluindo um jogo de rastreamento de mãos implantado via Netlify.
   *(2026-05-03)*

2939. Fase 1 envolve quick wins, incluindo limpeza do Hub, auditoria em `hub/store.deletar()`, e investigar `_resumir_e_salvar` em `gus/bot.py`.
   *(2026-05-03)*

2940. O Hub não tem nenhum fragmento com tipo = identidade_operacional + estado = estavel nem procedural + estado = estavel.
   *(2026-05-03)*

2941. Três demandas estão paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, `_frontmatter-referencia.md` (esse é template, não é demanda).
   *(2026-05-02)*

2942. Estou aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

2943. O projeto contém três demandas paradas em dialogos/inbox-claude-code: 2026-05-01-captura-multiporta-curador.md, 2026-05-01-drive-sync-oauth-fix.md e _frontmatter-referencia.md.
   *(2026-05-02)*

2944. O caminho `fallback-mem0` escreve em Mem0 SaaS, não no Hub.
   *(2026-05-03)*

2945. O segredo gerado no passo de configuração deve ser guardado pelo usuário.
   *(2026-05-03)*

2946. Core obrigatório são 4 arquivos que dão 80% do contexto pra qualquer aba nova.
   *(2026-05-03)*

2947. Para resolver o vazamento, o segredo deve ser regenerado no Railway e o código ajustado para não logar segredos.
   *(2026-05-03)*

2948. Vou puxar o core obrigatório e o git recente em paralelo.
   *(2026-05-03)*

2949. O sistema opera com um bootstrap atualizado e um Drive sync configurado, permitindo que as informações sejam capturadas em tempo real.
   *(2026-05-03)*

2950. A pasta do Google Drive se chama Gus-Sync, não GitHub-Sync.
   *(2026-05-03)*

2951. Esses arquivos são específicos do contexto da pergunta.
   *(2026-05-03)*

2952. O autor recomenda que o bootstrap do Claude Chat seja reordenado, contendo um TL;DR no topo, seguido de informações sobre identidade, capacidades e limites, diretrizes universais, estilo de resposta, caminhos de captura e regras DURAS.
   *(2026-05-03)*

2953. Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template.
   *(2026-05-02)*

2954. Após a implementação de PR #73, o TioGu começou a redigir respostas preservando informações sensíveis e eventos com respeito à LGPD.
   *(2026-05-04)*

2955. Os arquivos de protocolos comuns vão ser carregados apenas sob demanda, dependendo do que o Gustavo solicitar.
   *(2026-05-03)*

2956. A stack de memória está em estado intermediário arriscado, com 204 fragmentos não-migrados e fallback ativo em leitura.
   *(2026-05-03)*

2957. Gustavo é anestesiologista e não programa. Toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

2958. O estado final dos PRs está no código e nos documentos gus-XX atualizados; PRs descrevem o caminho, não o presente.
   *(2026-05-03)*

2959. Hoje o passo Drive sync GitHub→Drive parou em 01/05 14:38Z.
   *(2026-05-03)*

2960. O estado final da memória do paciente deve ser classificado como ativo ou estável.
   *(2026-05-03)*

2961. A auditoria do projeto revelou várias áreas de melhoria, incluindo questões de segurança, confiabilidade e arquitetura que precisam ser abordadas.
   *(2026-05-03)*

2962. Gustavo tem hipertireoidismo em tratamento com Tapazol, acompanhado por endocrinologista.
   *(2026-05-04)*

2963. Foi confirmado que a função `_fallback_mem0` não escreve no Mem0 SaaS atualmente, mas continua a injetar fragmentos não classificados no Hub.
   *(2026-05-03)*

2964. Recomendo que o Hub Qdrant seja a fonte da verdade e que a coleta dual de modelos no curador (Haiku × GPT-4o-mini) termine em 12/05/2026.
   *(2026-05-03)*

2965. Os logs do `_log/resumos-mem0/` confirmam que o curador não estava funcionando.
   *(2026-05-02)*

2966. O projeto NeuroGus tem planejamento 100% pronto, mas aguarda confirmação em decisões abertas.
   *(2026-05-04)*

2967. Gustavo é anestesiologista e não programa — toda implementação passa pelo Gus ou Tiogu.
   *(2026-05-03)*

2968. O bot possui prompt caching que reduz o custo de input em janelas de 5 minutos.
   *(2026-05-02)*

2969. A migração de 204 memórias de gus deve ser realizada para evitar poluição do Hub.
   *(2026-05-03)*

2970. Sempre que possível, é melhor usar ferramentas MCP ao invés de arquivos .md.
   *(2026-05-02)*

2971. Se os testes de validação passarem, avançar para o próximo passo que é recadastrar o Connector no claude.ai.
   *(2026-05-03)*

2972. É necessário ler [gus-estado-atual.md](http://gus-estado-atual.md) para obter um snapshot do Hub.
   *(2026-05-03)*

2973. O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).
   *(2026-05-02)*

2974. A equipe registrou que o curador híbrido gera resumos brutos quando falha, o que pode poluir o Hub com dados não classificados.
   *(2026-05-03)*

2975. Gustavo é anestesiologista e utiliza o sistema Gus como um agente pessoal multi-porta.
   *(2026-05-03)*

2976. Gustavo é anestesiologista e não programa; toda implementação passa pelo Gus ou Tiogu.
   *(2026-05-03)*

2977. A auditoria diária é cega para o brain gus e não considera o area que o curador já preencheu.
   *(2026-05-03)*

2978. A pasta inbox-mem0-from-chat foi nomeada legadamente, pois o Mem0 SaaS está aposentado.
   *(2026-05-03)*

2979. O Bootstrap contém 421 linhas com 4795 tokens, representando 74% do total.
   *(2026-05-03)*

2980. O Gus é um sistema de agente pessoal multi-porta, incluindo Telegram, Claude Code e Claude Chat, com futura integração com Alexa.
   *(2026-05-03)*

2981. O curador híbrido do sistema é um pipeline de extração de fragmentos que está rodando em paralelo entre Anthropic e OpenAI, com comparação A/B em andamento.
   *(2026-05-04)*

2982. Gustavo tem hipertireoidismo em tratamento com Tapazol, acompanhado por endocrinologista.
   *(2026-05-03)*

2983. Hub com ~70% de meta-lixo — saneamento planejado mas não executado ainda.
   *(2026-05-03)*

2984. Há 4 demandas pendentes sendo triadas no inbox-claude-code.
   *(2026-05-03)*

2985. O `gus-estado-atual.md` gera um snapshot do Hub a cada 15 minutos.
   *(2026-05-03)*

2986. Demandas pendentes na porta inbox-claude-code incluem captura multiporta, curador bidirecional cron e drive-sync OAuth.
   *(2026-05-03)*

2987. O sistema possui 204 fragmentos não migrados e o código ainda faz fallback para a coleção legada durante a leitura.
   *(2026-05-03)*

2988. Gustavo Pratti de Barros é anestesiologista no Dimagem no Rio de Janeiro e pesquisador independente em IA.
   *(2026-05-04)*

2989. O `_estado-atual.md` está desatualizado e não reflete as mudanças mais recentes do Git.
   *(2026-05-04)*

2990. Gustavo e sua esposa têm interesse por viagens em natureza e aventura na região do Vale do Paraíba.
   *(2026-05-03)*

2991. A captura de fragmentos acontece em três frentes: Telegram, Chat e Code.
   *(2026-05-03)*

2992. O pipeline de upload a partir do Chat não está implementando lógica de retry, representando um risco de perda de dados.
   *(2026-05-03)*

2993. A demanda 2026-05-01-captura-multiporta-curador.md precisa de um gatilho proativo no Chat.
   *(2026-05-02)*

2994. A URL do Connector no claude.ai precisa ser atualizada para incluir o `MCP_URL_SECRET`.
   *(2026-05-03)*

2995. Existem 6 demandas pendentes na porta inbox-claude-code, sendo 3 demandas reais.
   *(2026-05-03)*

2996. A falta de um mecanismo de deduplicação pode resultar em contaminação cruzada entre os cérebros 'gustavo' e 'gus'.
   *(2026-05-03)*

2997. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-04)*

2998. Foram identificados problemas no Chat, como o erro 400 recorrente no curador Telegram e falhas no sync entre GitHub e Drive.
   *(2026-05-03)*

2999. A conta Anthropic está sem créditos.
   *(2026-05-03)*

3000. O estado final dos PRs já está documentado no código e nos docs gus-XX atualizados.
   *(2026-05-03)*

3001. A migração para Hub Qdrant está em andamento e a fonte de verdade será o Hub Qdrant após a migração.
   *(2026-05-03)*

3002. A seção 'Como você captura memória pro Hub' no bootstrap foi reescrita, dividindo em dois caminhos: captura real-time via MCP e upload .md para sessões longas.
   *(2026-05-03)*

3003. O curador pode enfrentar riscos de poluição silenciosa ao permitir que resumos brutos sejam armazenados no Hub sem classificação.
   *(2026-05-03)*

3004. O curador claudia faz 4 chamadas LLM por input, um total de 4 vezes para o mesmo prompt.
   *(2026-05-03)*

3005. O bot opera com dependências como python-telegram-bot, anthropic SDK, openai, FastAPI e Qdrant.
   *(2026-05-03)*

3006. O Hub é a fonte da verdade. Gustavo é anestesiologista, não programa — toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

3007. Das 421 linhas do `gus-bootstrap.md`, aproximadamente 120 são protocolos que o Chat só usa quando Gustavo pede algo específico.
   *(2026-05-03)*

3008. As decisões abertas do projeto incluem a aprovação de itens 11.1-11.7.
   *(2026-05-02)*

3009. Estou aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3010. A stack está em estado intermediário arriscado: Hub Qdrant é a fonte nova, mas a coleção legada `gus` (Mem0 self-hosted) tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

3011. O fragmento com UUID '42aea182-d4a2-4626-8a85-5ede861b311b' foi salvo no brain 'gus' como meta-reflexão.
   *(2026-05-03)*

3012. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e precisa de uma decisão sobre como proceder com a autenticação OAuth.
   *(2026-05-04)*

3013. Existem atualmente três frentes ativas: TioGu, Claude Chat e a integração com o Claude Code.
   *(2026-05-03)*

3014. Cinco arquivos foram alterados com um total de mais de oito linhas e menos de 60 linhas removidas.
   *(2026-05-04)*

3015. As decisões arquiteturais incluem a definição de canais de escrita e o comportamento da captura proativa do Chat.
   *(2026-05-03)*

3016. Ativando protocolo Gus Chat — vou buscar o bootstrap no Drive agora.
   *(2026-05-03)*

3017. O Gus opera em uma estrutura de projeto que possui um Hub Qdrant como memória e um Drive Gus-Sync como knowledge.
   *(2026-05-04)*

3018. O estado final dos PRs já está no código e nos documentos atualizados; novas abas não precisam ser criadas se o conteúdo for apenas histórico.
   *(2026-05-03)*

3019. O Gus é um sistema de agente pessoal multi-porta, que inclui Telegram/TioGu, Claude Code, Claude Chat e futuras integrações como Custom GPT mobile e Alexa.
   *(2026-05-03)*

3020. Aba nova deve sempre consultar o Hub, que é mais fresco que o snapshot das 03h.
   *(2026-05-03)*

3021. As frentes mais ativas incluem: PR #67 do curador chat bidirecional, PR #64 que resolve a captura de transcripts e PR #60 que aplica 'MCP_URL_SECRET'.
   *(2026-05-03)*

3022. Os arquivos `gus-bootstrap.md`, `gus-identity.md`, e `gus-estado-atual.md` dão 80% do contexto para qualquer aba nova.
   *(2026-05-03)*

3023. Estado de migração: ADR-001 em curso, aposentar Mem0 SaaS, Hub Qdrant é fonte da verdade.
   *(2026-05-03)*

3024. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3025. A auditoria do Chat envolve todos os aspectos relacionados ao projeto Claude Chat.
   *(2026-05-03)*

3026. No Claude Chat, 12 bugs foram corrigidos a partir de uma auditoria que identificou 31 problemas.
   *(2026-05-03)*

3027. Existem demandas pendentes e algumas estão associadas a um arquivo intitulado "Documento sem título.md".
   *(2026-05-03)*

3028. A recomendação é manter os 204 fragmentos em 'historico/' e planejar a importação dos mesmos na Fase 5.
   *(2026-05-03)*

3029. `gus-tipos-fragmento.md` deve conter o schema dos tipos de fragmento para garantir a correta classificação.
   *(2026-05-03)*

3030. O projeto tem 4 demandas pendentes no `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3031. Gustavo Pratti de Barros é anestesiologista no Dimagem, no Rio de Janeiro, e pesquisador independente em inteligência artificial.
   *(2026-05-03)*

3032. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3033. O passo de validação inclui confirmar que os parâmetros esperados do MCP estão ativos.
   *(2026-05-03)*

3034. O cron 'gerar-estado-claude-chat' roda a cada 15 minutos, mesmo quando Hub está ocioso.
   *(2026-05-03)*

3035. Há 4 demandas pendentes no `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3036. O Hub Qdrant serve como memória central para o Gus, armazenando informações em arquivos .md no GitHub, que são espelhados no Drive.
   *(2026-05-03)*

3037. Um dos workflows está apresentando falhas, especificamente a importação de demandas do Drive.
   *(2026-05-02)*

3038. As 18 entradas que entraram em modo `fallback-mem0` não estão na coleção `gus`.
   *(2026-05-03)*

3039. O bot Telegram TioGu usa um sistema multi-porta com Hub Qdrant como memória central.
   *(2026-05-02)*

3040. A aba que contém o MCP gus-hub conectado permite ler o cache de identidade atual, últimas 3 decisões e 5 meta-reflexões, além de fragmentos recentes das últimas 24 horas.
   *(2026-05-02)*

3041. O Hub apresenta 19 fragmentos no brain 'gustavo', com sistema ocioso durante as últimas 6 horas.
   *(2026-05-03)*

3042. O Hub Qdrant é a nova fonte da verdade, e a migração do sistema Mem0 está em andamento. O sistema utiliza em paralelo dois curadores (Haiku e GPT-4o-mini) com multiplicação por 4 nas chamadas LLM.
   *(2026-05-03)*

3043. O sistema Hub tem 19 fragmentos no brain `gustavo`, com inatividade nas últimas 6 horas.
   *(2026-05-03)*

3044. Estou aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3045. O boot do Gus é dividido em um arquivo principal e documentos auxiliares que são carregados sob demanda.
   *(2026-05-04)*

3046. A stack de memória está em estado intermediário arriscado, com o Hub Qdrant como nova fonte de verdade.
   *(2026-05-03)*

3047. Há 3 produções simultâneas de fragmentos: Telegram, Chat e Code, com 4 vezes mais chamadas LLM por unidade de input.
   *(2026-05-03)*

3048. As diretrizes operacionais incluem validar informações antes de responder.
   *(2026-05-04)*

3049. A stack está em estado intermediário arriscado: 3 produções simultâneas de fragmentos (Telegram, Chat, Code) com 4× multiplicação de chamadas LLM por unidade de input e sem mecanismo de deduplicação.
   *(2026-05-03)*

3050. O agente pessoal do Gustavo Pratti de Barros é chamado Gus.
   *(2026-05-03)*

3051. Gus é um sistema de agente pessoal multi-porta que opera em diferentes plataformas como Telegram, Claude Code e, no futuro, Alexa.
   *(2026-05-03)*

3052. A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida pelo PR #67.
   *(2026-05-02)*

3053. O Drive sync foi migrado de OAuth user para Workload Identity Federation com Service Account.
   *(2026-05-04)*

3054. O último arquivo do estado atual do Hub mostra dados desatualizados de 27/04.
   *(2026-05-03)*

3055. O estado final dos PRs já tá no código + nos docs gus-XX atualizados.
   *(2026-05-03)*

3056. O arquivo `gus-identity.md` é redundante com o `gus-bootstrap.md` e contém informações desatualizadas sobre o Gustavo.
   *(2026-05-04)*

3057. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

3058. A coleção legada 'gus' (Mem0) ainda tem ~204 fragmentos não-migrados e o código de leitura ainda faz fallback para ela.
   *(2026-05-03)*

3059. Há riscos de poluição cross-brain entre os brains 'gustavo' e 'gus' devido à duplicação de fragmentos sem deduplicação.
   *(2026-05-03)*

3060. O curador de Claude Chat teve 12 correções de 31 problemas identificados.
   *(2026-05-03)*

3061. Os 4 arquivos essenciais para qualquer aba nova no projeto são: `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md` e `estado-atual.md`.
   *(2026-05-03)*

3062. Os nomes das demandas pendentes são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao.
   *(2026-05-04)*

3063. Sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa). Memória central no Hub Qdrant (`gus_hub`), arquivos .md no GitHub (`Gustpbbr/Gus`), espelhados no Drive.
   *(2026-05-03)*

3064. A auditoria diária ignora o brain 'gus' e classifica por keywords, desconsiderando a área já preenchida pelo curador.
   *(2026-05-03)*

3065. A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida pelo PR #67 (curador bidirecional), mas falta o gatilho proativo no Chat.
   *(2026-05-02)*

3066. O Gus deve priorizar o uso de ferramentas MCP em vez de arquivos .md sempre que possível.
   *(2026-05-03)*

3067. A segurança do Hub precisa de ajustes para que o URL do MCP não fique público.
   *(2026-05-04)*

3068. Vi que tem 4 demandas pendentes no `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3069. Um evento de erro em `curador híbrido` vai alertar o Gustavo em tempo real para captura manual.
   *(2026-05-03)*

3070. O Hub Qdrant coleta dual rola até 12/05.
   *(2026-05-02)*

3071. Os passos não tocam o TioGu ou o retro engine, que são independentes do acesso seguro e fresco ao Hub e ao repo.
   *(2026-05-03)*

3072. Estou aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3073. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3074. A arquitetura do bot TioGu utiliza várias ferramentas e possui um sistema de memória centralizado no Hub Qdrant.
   *(2026-05-03)*

3075. O paciente_id canônico é gus.
   *(2026-05-02)*

3076. Core obrigatório: Arquivo, Pra quê, manual operacional do Gus, quem é o Gustavo, handoff auto-gerado pelo cron, onde paramos na sessão anterior.
   *(2026-05-03)*

3077. Coleção 'gus' no Qdrant está vazia.
   *(2026-05-03)*

3078. Pergunta se deve processar as demandas ou se há algo específico em mente.
   *(2026-05-03)*

3079. O arquivo `gus-identity.md` está redundante com o `gus-bootstrap.md`. A maioria das informações já está contida e atualizada no bootstrap.
   *(2026-05-03)*

3080. 204 fragmentos foram exportados do Mem0 SaaS, revelando conteúdo biográfico e decisões arquiteturais que não estavam presentes no Hub na sua atual configuração.
   *(2026-05-03)*

3081. O sistema de sincronização entre o Google Drive e o GitHub deve ser ajustado para utilizar uma Service Account ao invés de OAuth.
   *(2026-05-03)*

3082. A auditoria atual do Hub não está considerando a coleta de dados do brain 'gus', causando uma falta de visibilidade sobre seu estado.
   *(2026-05-03)*

3083. Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

3084. Gustavo Pratti de Barros é um anestesiologista, não programa.
   *(2026-05-03)*

3085. A aposentadoria do Mem0 SaaS está planejada após 12/05/2026.
   *(2026-05-03)*

3086. Tudo carregado. Estou de volta como Gus.
   *(2026-05-03)*

3087. A coleta dual de modelos no curador (Haiku e GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

3088. A ouvidoria é feita por meio de auditoria diária e relatórios gerados automaticamente.
   *(2026-05-03)*

3089. O script para verificar a existência do `MEM0_API_KEY` pode ser rodado para decidir o que fazer em relação ao Mem0 SaaS.
   *(2026-05-03)*

3090. Gustavo é anestesiologista e não programa.
   *(2026-05-03)*

3091. Curador Telegram tem erro 400 recorrente, o que sugere que o ingest do Chat também está falhando silenciosamente.
   *(2026-05-03)*

3092. A primeira fase do projeto Gus prevê a completa remoção do fallback Mem0 e a finalização dos organizadores e auditorias.
   *(2026-05-03)*

3093. Renomear 'inbox-mem0-from-chat/' para 'inbox-chat-raw/' é parte da proposta de limpeza.
   *(2026-05-03)*

3094. O arquivo gus-identity.md não é uma fonte única de verdade, pois outras fontes como gus-bootstrap.md estão mais atualizadas.
   *(2026-05-04)*

3095. O bot do Telegram, TioGu, possui 21 ferramentas distintas integradas.
   *(2026-05-03)*

3096. Mem0 SaaS foi aposentado desde 27/04/2026. Hub Qdrant é fonte única.
   *(2026-05-04)*

3097. O ciclo de vida do schema gus-18 promete um gerenciamento dinâmico do peso e acessos, mas atualmente não está implementado.
   *(2026-05-03)*

3098. Após configurar o segredo, o usuário deve aguardar redeploy do Railway antes de validar funcionalidades do MCP.
   *(2026-05-03)*

3099. A demanda `2026-05-01-captura-multiporta-curador.md` precisa de um gatilho proativo no Chat.
   *(2026-05-03)*

3100. A auditória diária é cega para o brain `gus` e ignora o `area` já preenchido pelo curador.
   *(2026-05-03)*

3101. O último dia de captura no SaaS foi 26/04.
   *(2026-05-03)*

3102. Após setar `MCP_URL_SECRET` no Railway, um redeploy automático ocorre em ~2-3 minutos.
   *(2026-05-03)*

3103. As 18 entradas 'fallback-mem0' de 28/04 foram pro Mem0 SaaS porque a migração ainda não estava 100% deploy-ada.
   *(2026-05-03)*

3104. É importante que o Chat não busque no brain `gustavo` quando deve buscar no brain `gus` para evitar perda de informações.
   *(2026-05-03)*

3105. O arquivo `_estado-atual.md` deve ser atualizado para refletir os PRs #57, #60, #63, #64 e #67.
   *(2026-05-04)*

3106. As 4 fases do projeto dão 80% do contexto para qualquer nova aba.
   *(2026-05-03)*

3107. O Hub Qdrant é a memória central do Gus, que armazena informações em arquivos .md no GitHub, espelhados no Drive.
   *(2026-05-03)*

3108. As escolhas de codificação no curador incluem 4 chamadas LLM por input para lidar com cada interagir, aumentando os custos operacionais.
   *(2026-05-03)*

3109. Gustavo Pratti de Barros é anestesiologista no Dimagem, no Rio de Janeiro, e pesquisador independente em IA, operando múltiplos projetos simultaneamente em pesquisa, produto e arquitetura.
   *(2026-05-03)*

3110. O script `export_mem0.py` é responsável por exportar dados do Mem0 SaaS.
   *(2026-05-03)*

3111. A captura de memória do bot é feita pelo arquivo do log que registra o transcript da sessão.
   *(2026-05-04)*

3112. O curador utilizado no Telegram apresentou erro 400 envolvendo KeyError, especificamente no formato do JSON em uso.
   *(2026-05-02)*

3113. O estado final dos PRs já está no código e nos documentos atualizados, portanto uma nova aba não precisa consultar os PRs.
   *(2026-05-03)*

3114. O passo 3 envolve escolher entre resetar OAuth, usar uma Service Account ou aposentar o Drive sync, pois o acesso do Chat ao Drive está stale.
   *(2026-05-03)*

3115. O sistema 'Gus' é um agente pessoal multiportas em produção que roda sobre um Hub Qdrant.
   *(2026-05-03)*

3116. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e precisa de uma decisão sobre a tecnologia a ser utilizada.
   *(2026-05-02)*

3117. NeuroGus é um projeto ativo que fornece visualização 3D do Hub.
   *(2026-05-04)*

3118. A migração ADR-001 está em curso, visando aposentar o Mem0 SaaS fazendo do Hub Qdrant a fonte da verdade.
   *(2026-05-03)*

3119. Os itens pendentes incluem: captura-multiporta-curador, drive-sync-oauth-fix e pendencias-claude-chat-consolidacao.
   *(2026-05-03)*

3120. O chat diz que gravou, mas quando busco em outra aba, a outra aba não cita os fragmentos e o outro chat diz que colocou.
   *(2026-05-03)*

3121. O plano para reclassificar e reintegrar 204 fragmentos do Mem0 é esperado na Fase 5.
   *(2026-05-03)*

3122. O bootstrap-v6 foi atualizado com dois caminhos de captura (MCP em tempo real + upload curado de .md).
   *(2026-05-03)*

3123. Gustavo é anestesiologista e não programa, sendo que toda implementação passa pelo Gus ou Tiogu.
   *(2026-05-03)*

3124. A coleta dual de modelos no curador termina em 12/05/2026, quando Gustavo escolherá um modelo definitivo.
   *(2026-05-03)*

3125. Hoje o MCP está público — qualquer scanner que descobrir a URL Railway lê todo o Hub.
   *(2026-05-03)*

3126. O Hub está coletando dados de fragmentos de múltiplas fontes, mas o custo de processamento está aumentando devido à quantidade de chamadas LLM feitas por entrada.
   *(2026-05-03)*

3127. A coleção legada de memórias do Gus ainda existe, mas deve ser migrada para o Hub. Existia o risco de inconsistências entre as buscas feitas no Hub e na coleção legada.
   *(2026-05-03)*

3128. O Gus é um sistema de agente pessoal multi-porta que possui um Hub central.
   *(2026-05-03)*

3129. O arquivo de log gerado pelo retro-engine é inofensivo e documenta um comportamento esperado.
   *(2026-05-02)*

3130. A estrutura do código foi aprimorada com uma melhora na organização, onde agora existem diversos módulos focados em funcionalidades específicas, como github.py e web.py, facilitando a compreensão e manutenção do sistema.
   *(2026-05-04)*

3131. A coleção legada `gus` tem ~204 fragmentos não-migrados no Mem0 SaaS.
   *(2026-05-03)*

3132. Os arquivos core obrigatórios para qualquer aba nova são: dialogos/_bootstrap/gus-bootstrap.md, dialogos/_bootstrap/gus-identity.md, dialogos/_bootstrap/gus-estado-atual.md e projetos/gus/_estado-atual.md.
   *(2026-05-03)*

3133. O bot Telegram (TioGu) possui ~21 tools, multimídia, prompt caching e está em produção no Railway.
   *(2026-05-02)*

3134. O log do retro-engine registra quando a captura de memória falha devido a ausência da ANTHROPIC_API_KEY.
   *(2026-05-04)*

3135. Para o estado atual do trabalho, é possível consultar o Hub utilizando `ego_cache_atual` ou `fragmentos_recentes`.
   *(2026-05-03)*

3136. Estão disponíveis ferramentas de auditoria e análise para monitorar o desempenho do chat.
   *(2026-05-03)*

3137. Gustavo tem hipertireoidismo em tratamento.
   *(2026-05-03)*

3138. 204 fragmentos foram exportados do Mem0 SaaS para o diretório historico.
   *(2026-05-03)*

3139. Gustavo Pratti de Barros é anestesista na Dimagem e pesquisador independente em IA.
   *(2026-05-03)*

3140. Estamos na fase de migração do Mem0 SaaS para o Hub Qdrant, que será a fonte da verdade.
   *(2026-05-03)*

3141. O sistema de agente pessoal está com riscos de perda silenciosa e poluição cross-brain se não for ajustado.
   *(2026-05-03)*

3142. Atualmente o bot TioGu não possui testes automatizados, representando um risco significativo para a manutenção do sistema.
   *(2026-05-02)*

3143. A stack está em estado intermediário arriscado, com 3 produções simultâneas de fragmentos e 4× multiplicação de chamadas LLM por unidade de input.
   *(2026-05-03)*

3144. As diretrizes operacionais do Gus estão descritas no arquivo gus-bootstrap.md.
   *(2026-05-04)*

3145. O projeto Gus tem um sistema multi-porta que integra o Telegram, Claude Code, Claude Chat e futuros modelos como Custom GPT e Alexa.
   *(2026-05-02)*

3146. O `retro-engine` é um hook que roda quando uma sessão Claude Code termina.
   *(2026-05-04)*

3147. O NeuroGus está planejado com PWA e grafo 3D do Hub, com planejamento 100% pronto.
   *(2026-05-02)*

3148. O sistema é composto por Gustavo, que é anestesiologista e não programa, e sua implementação é feita através do Gus.
   *(2026-05-03)*

3149. Coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

3150. A demanda #3 refere-se a pendências Claude Chat que incluem: ativar MCP URL secret no Railway, recadastrar o Connector Claude.ai, localizar um mock HTML do NeuroGus, e decidir sobre a captura em tempo real do Chat.
   *(2026-05-02)*

3151. A auditoria do Claude Chat revelou 12 fixes de 31 achados.
   *(2026-05-03)*

3152. O Hub atual possui cerca de 500-600 fragmentos.
   *(2026-05-03)*

3153. Os quatro arquivos: `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md`, `estado-atual.md` são fundamentais e geram 80% do contexto para qualquer aba nova.
   *(2026-05-03)*

3154. A captura de memória da porta Claude Code está temporariamente quebrada devido à falta da variável ANTHROPIC_API_KEY, sendo uma necessidade de configuração que deve ser resolvida para que a captura funcione plenamente.
   *(2026-05-04)*

3155. Foi decidido que um cron job deve ser implementado para atualizar o estado dos fragmentos no Hub.
   *(2026-05-03)*

3156. A demanda `2026-05-01-captura-multiporta-curador.md` precisa de uma decisão sobre o gatilho proativo no Chat.
   *(2026-05-04)*

3157. O `MEM0_API_KEY` será removido do Railway e do GitHub Secrets para encerrar o uso do Mem0 SaaS.
   *(2026-05-03)*

3158. Em 02/05, o curador falhou em salvar fragmentos devido a problemas de formato que estavam presentes em 29/04.
   *(2026-05-03)*

3159. Gustavo Pratti de Barros é anestesiologista e não programa.
   *(2026-05-03)*

3160. A migração de dados do Mem0 SaaS para Hub Qdrant não foi realizada pois a coleção 'gus' está vazia.
   *(2026-05-03)*

3161. A atualização do `Anthropic SDK` está planejada para ser feita em um upgrade que não impactará o funcionamento do TioGu.
   *(2026-05-03)*

3162. A migração do sistema Mem0 SaaS para Hub Qdrant está em curso.
   *(2026-05-03)*

3163. Gus é um sistema de agente pessoal multi-porta, com memória central no Hub Qdrant, que coleta informações de diversas fontes.
   *(2026-05-03)*

3164. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3165. A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida pelo PR #67.
   *(2026-05-02)*

3166. O nome da pasta 'Gustavo/' em 'Gus-Sync/dialogos/' pode ser padronizado como 'Gustavo/'.
   *(2026-05-03)*

3167. O projeto Gus é um sistema de agente pessoal multi-porta com memória central no Hub Qdrant.
   *(2026-05-03)*

3168. A auditoria do Chat envolve todos os aspectos relacionados ao projeto Claude Chat.
   *(2026-05-03)*

3169. A captura dual Haiku × Sonnet está programada para rodar até 12/05, momento em que uma decisão sobre o modelo curador final será tomada.
   *(2026-05-03)*

3170. Quando o Drive sync entregar, a próxima conversa no Chat já vai usar a captura proativa.
   *(2026-05-03)*

3171. O projeto NeuroGus visa a visualização do Hub.
   *(2026-05-04)*

3172. O projeto TioGu é um bot do Telegram que utiliza um sistema multi-provider com fallback cross-vendor para inteligência artificial.
   *(2026-05-03)*

3173. Gus é um sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa).
   *(2026-05-03)*

3174. A seção 'Como você captura memória pro Hub' foi reescrita com 2 caminhos: Caminho 1 (MCP) e Caminho 2 (upload .md).
   *(2026-05-03)*

3175. O sistema tem um mecanismo de fallback que tenta usar OpenAI se o Anthropic falhar.
   *(2026-05-03)*

3176. O bootstrap atual menciona 'buscar_hub' mas não destaca que pra brain 'gus' precisa passar 'user_id=gus' explicitamente.
   *(2026-05-04)*

3177. A coleta de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

3178. O contrato schema gus-18 está parcialmente implementado. O lifecycle declarado não é executado.
   *(2026-05-03)*

3179. A migração para o Hub Qdrant está em curso e a coleta dual de modelos no curador termina em 12/05/2026.
   *(2026-05-03)*

3180. O curador híbrido, que utiliza Haiku e GPT-4o-mini, está operando em paralelo.
   *(2026-05-03)*

3181. O '_estado-atual.md' está desatualizado e não reflete muitas mudanças recentes.
   *(2026-05-02)*

3182. O `gus-bootstrap.md` deve conter a identidade do Gustavo, caminhos de captura e regras duras.
   *(2026-05-03)*

3183. Gustavo é um falante nativo de português, baseado no Rio de Janeiro, com interesses em segurança em IA, filosofia e systems thinking.
   *(2026-05-03)*

3184. Gustavo é anestesiologista e não programa. Toda implementação passa por um sistema de agente pessoal multi-porta que utiliza core obrigatório como arquivos de bootstrap para regras e identidade.
   *(2026-05-03)*

3185. O plano de refatoração do arquivo 'gus-identity.md' inclui a sua consolidação no 'gus-bootstrap.md' e remoção de entradas desatualizadas.
   *(2026-05-04)*

3186. O Curador Telegram está com erro 400 recorrente desde 30/04 — só uma entrada por dia, sempre erro.
   *(2026-05-03)*

3187. Não deve cadastrar o Connector ainda até que o código seja ajustado para impedir log do segredo.
   *(2026-05-03)*

3188. Houve uma transição para o Hub Qdrant em 27/04/2026.
   *(2026-05-03)*

3189. Anthropic é usado para respostas multimodais, enquanto OpenAI é usado para texto puro.
   *(2026-05-03)*

3190. O estado final dos PRs já está no código e nos docs gus-XX atualizados.
   *(2026-05-03)*

3191. O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).
   *(2026-05-02)*

3192. Hub Qdrant e posterior migração do modelo Mem0 para o Hub é uma decisão arquitetural em curso.
   *(2026-05-03)*

3193. O projeto TioGu é um bot desenvolvido para o Telegram que utiliza um sistema multi-porta com arquitetura Hub Qdrant como memória central.
   *(2026-05-02)*

3194. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3195. Gustavo está em tratamento de hipertireoidismo.
   *(2026-05-04)*

3196. Gustavo Pratti de Barros é anestesiologista no Rio de Janeiro, atuando no Dimagem, clínica de imagem diagnóstica com 3 unidades: Nova Iguaçu, Taquara, São Gonçalo.
   *(2026-05-04)*

3197. A migração Mem0 para o Hub Qdrant está na fase 4, e a coleta dual Haiku × Sonnet roda até 12/05, quando será decidida o modelo curador final.
   *(2026-05-03)*

3198. Necessito confirmar se fragmento aparece na Aba B usando buscar_hub com user_id='gus'.
   *(2026-05-04)*

3199. Foi identificado drift entre informações do userMemories e do gus-bootstrap.md, resultando em redundâncias e ambiguidade.
   *(2026-05-03)*

3200. A coleção legada 'gus' (Mem0) ainda está viva e faz fallback no sistema atual.
   *(2026-05-03)*

3201. Gustavo está em tratamento para hipertireoidismo.
   *(2026-05-04)*

3202. A migração ADR-001 está em curso para aposentar o Mem0 SaaS.
   *(2026-05-03)*

3203. A estrutura proposta para o bootstrap é: um arquivo para boot mínimo e arquivos separados para protocolos que Chat carrega quando necessário.
   *(2026-05-03)*

3204. A conexão entre o curador e o módulo llm é muito direta e pode ser melhorada para aumentar a modularidade.
   *(2026-05-02)*

3205. Decisão migração ADR-001 em curso: aposentar Mem0 SaaS, Hub Qdrant é fonte da verdade.
   *(2026-05-03)*

3206. A proposta de mudança no `drop_pending_updates` do bot Telegram é mantê-lo como True, mas adicionar uma mensagem de aviso se houver mensagens pendentes durante o boot.
   *(2026-05-02)*

3207. O estado final dos PRs está documentado, e a Fase 1.7 é planejada para a limpeza do Hub atual.
   *(2026-05-03)*

3208. O estado atual do projeto pode ser consultado no arquivo `projetos/gus/_[estado-atual.md]`.
   *(2026-05-03)*

3209. Gus é um sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa).
   *(2026-05-03)*

3210. O Gus é um agente pessoal, e seu sistema está agora em produção com uma arquitetura de múltiplas portas.
   *(2026-05-03)*

3211. O curador usa dois modelos em paralelo: Haiku e GPT-4o-mini.
   *(2026-05-03)*

3212. A stack está em estado intermediário arriscado: Hub Qdrant é a fonte nova, mas a coleção legada `gus` (Mem0 self-hosted) tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

3213. A migração do sistema para o Hub Qdrant foi concluída.
   *(2026-05-03)*

3214. Quer que eu ataque alguma agora ou tem outra coisa em mente?
   *(2026-05-03)*

3215. Gustavo Pratti de Barros é anestesiologista no Rio de Janeiro, atuando no Dimagem.
   *(2026-05-04)*

3216. Há uma inconsistência na leitura das memórias legadas, que ainda estão ativas no sistema.
   *(2026-05-03)*

3217. O branch atual é `claude/project-discussion-fkfA8` e contém um arquivo `_log/retro-engine` novo desta sessão.
   *(2026-05-02)*

3218. Uma nova suite de testes para o projeto foi implementada, abrangendo uma cobertura ampla das funcionalidades principais.
   *(2026-05-02)*

3219. Gustavo é anestesiologista e utiliza o sistema Gus como agente pessoal multi-porta.
   *(2026-05-03)*

3220. A estrutura da receita para análise e informações do projeto é orientada pelo core obrigatório.
   *(2026-05-03)*

3221. Todas as ferramentas do bot são integradas com multimídia e prompt caching em produção.
   *(2026-05-03)*

3222. As demandas pendentes no inbox-claude-code incluem captura-multiporta-curador, drive-sync-oauth-fix, e pendencias-claude-chat-consolidacao.
   *(2026-05-03)*

3223. O projeto está em um estado intermediário arriscado, sendo necessário lidar com a poluição cruzada entre brains.
   *(2026-05-03)*

3224. Transcripts comitados não cobrem hex puro de 64 chars.
   *(2026-05-03)*

3225. Sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa).
   *(2026-05-03)*

3226. Log do MCP deve ser validado após o redeploy para garantir que o valor do secret não vaza mais.
   *(2026-05-03)*

3227. O status final dos PRs já está no código e nos docs gus-XX atualizados, portanto, não é necessário ler PRs antigos.
   *(2026-05-02)*

3228. O arquivo `gus-bootstrap.md` contém informações essenciais para a operação do chat.
   *(2026-05-03)*

3229. O contrato schema gus-18 está parcialmente implementado.
   *(2026-05-03)*

3230. As amostras do Mem0 mostraram fragmentos de alta qualidade, incluindo informações pessoais e decisões arquiteturais importantes.
   *(2026-05-03)*

3231. A memória Mem0 foi aposentada e substituída pelo Hub Qdrant como fonte única.
   *(2026-05-03)*

3232. A coleta dual de modelos no curador deve ser finalizada até 12/05/2026.
   *(2026-05-03)*

3233. Tenho 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3234. A opção de reordenar o bootstrap é uma solução para otimização incremental.
   *(2026-05-04)*

3235. A implementação do ciclo de atualização de `acessos` e `ultimo_acesso` em `lembrar()` é necessária para o correto funcionamento do sistema.
   *(2026-05-03)*

3236. A stack está em estado intermediário arriscado, com Hub Qdrant funcionando, mas a coleção legada `gus` ainda possui ~204 fragmentos não-migrados.
   *(2026-05-03)*

3237. O sistema mantém uma lista de 21 ferramentas disponíveis que são referenciadas no `system_prompt.md`.
   *(2026-05-04)*

3238. Amostragem mostrou conteúdo biográfico real, ao contrário do Hub atual que é meta-conversa.
   *(2026-05-03)*

3239. Commit `1d2ee14` — Implementação de 'quick wins operacionais' e adição de 10 novos testes.
   *(2026-05-03)*

3240. Os documentos de protocolos operacionais devem ser separados em arquivos diferentes que o Chat carrega sob demanda.
   *(2026-05-04)*

3241. Esses 4 dão 80% do contexto pra qualquer aba nova.
   *(2026-05-03)*

3242. As demandas pendentes no inbox são: Ativar `MCP_URL_SECRET` no Railway, recadastrar Connector claude.ai e localizar mock HTML do NeuroGus.
   *(2026-05-03)*

3243. Interesses intelectuais fortes em segurança em IA, filosofia e systems thinking.
   *(2026-05-04)*

3244. As demandas pendentes no inbox são: Ativar `MCP_URL_SECRET` no Railway, recadastrar Connector claude.ai e localizar mock HTML do NeuroGus.
   *(2026-05-03)*

3245. O bot Telegram (TioGu) possui multimídia, prompt caching e um total de 21 tools.
   *(2026-05-03)*

3246. Gustavo é falante nativo de português e está baseado no Rio de Janeiro.
   *(2026-05-04)*

3247. Gustavo Pratti de Barros é o proprietário do Gus.
   *(2026-05-03)*

3248. A seção 'Personalidade do Gus' no arquivo `gus-identity.md` está misturando conteúdo que se aplica somente ao bot do Telegram com informações que devem ser aplicáveis em todas as portas do sistema.
   *(2026-05-03)*

3249. A auditoria diária é cega para o brain 'gus' e classifica por keywords, ignorando a área já preenchida pelo curador.
   *(2026-05-03)*

3250. O Hub Qdrant está na Fase 4 da migração Mem0 → Hub Qdrant.
   *(2026-05-02)*

3251. Esses 4 arquivos dão 80% do contexto pra qualquer aba nova: `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md` e `estado-atual.md`.
   *(2026-05-03)*

3252. Todo fragmento fica de estado "ativo" pra sempre.
   *(2026-05-03)*

3253. O PR #72 introduziu melhorias de segurança no MCP server, garantindo que ele opere em modo fail-closed sem autenticação.
   *(2026-05-02)*

3254. A demanda `2026-05-01-drive-sync-oauth-fix.md` precisa de mudanças.
   *(2026-05-03)*

3255. Os 204 fragmentos exportados do Mem0 SaaS foram confirmados como contendo conteúdo biográfico válido, enquanto o Hub atual é considerado ruidoso e de baixa qualidade.
   *(2026-05-03)*

3256. Foi adicionada uma trilha de auditoria em funções críticas como deletar no hub, garantindo rastreabilidade.
   *(2026-05-04)*

3257. A captura de fragmenots no sistema 'Gus' está funcionando em tempo real.
   *(2026-05-04)*

3258. A ferramenta de detecção de tópico permite ao bot manter o foco na conversa e recuperar contexto.
   *(2026-05-04)*

3259. O esquema gus-18 não está completamente implementado, especialmente no ciclo de vida dos fragmentos.
   *(2026-05-03)*

3260. A stack está em estado intermediário arriscado: Hub Qdrant é a fonte nova, mas a coleção legada `gus` (Mem0 self-hosted) tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

3261. A auto-notificação do Telegram pode ser mantida para demandas na pasta TioGu.
   *(2026-05-03)*

3262. 1. Gustavo trabalha com agendamento/gestão de pacientes para exames de RM (ressonância magnética).
2. Padrão de resposta esperado do Gus: formato com detecção de imagem, lista de pacientes já no sistema do dia, e solicitação de confirmação (sim/ok/manda ou não/cancela).
3. Gus deve manter esse padrão de resposta estruturado em futuras interações com Gustavo.
4. Roberta Xavier Lins foi adicionada ao arquivo do dia com exame de RM Coluna Dorsal + Lombar + Anestesia agendada para 15h-19h30, plano Intermédica.
   *(2026-04-28)*

3263. A implementação do bot considera resiliência e eficiência, como por exemplo, o uso de cache para evitar redundâncias em chamadas de API.
   *(2026-05-04)*

3264. O `MEM0_API_KEY` precisa ser verificado para decidir sobre a recuperação do conteúdo histórico.
   *(2026-05-03)*

3265. A proposta de otimização é dividir o bootstrap em arquivos por função.
   *(2026-05-03)*

3266. O bot Telegram (TioGu) tem 21 tools, multimídia, prompt caching e está em produção no Railway.
   *(2026-05-02)*

3267. A receita para iniciação de uma nova aba no contexto inclui 4 arquivos essenciais que dão 80% de contexto.
   *(2026-05-03)*

3268. O bot chama APIs externas sem cache, o que gera custo e pode exaurir recursos em meses de baixa cota.
   *(2026-05-02)*

3269. A captura de memória do bot foi implementada para manter um registro das interações, com gravação automática das conversas.
   *(2026-05-03)*

3270. A coleta de fragmentos é realizada através de 3 produções simultâneas de entradas: Telegram, Claude Chat e Claude Code.
   *(2026-05-03)*

3271. O bot do Telegram, TioGu, possui 21 ferramentas distintas integradas.
   *(2026-05-02)*

3272. Quando o curador salva no Hub mas falha no `git push` final, a próxima execução não reentra o arquivo. Fragmento entra no Hub uma vez, mas sem marcação no log.
   *(2026-05-03)*

3273. Atualmente há ~204 fragmentos não migrados da coleção legada Mem0, o que representa um risco de poluição.
   *(2026-05-03)*

3274. A auditoria profissional imparcial indicou a necessidade de prover segurança no acesso ao localhost do MCP server.
   *(2026-05-03)*

3275. O Arquivo gus-identity.md contém informações desatualizadas sobre a memória relacional, pois o Mem0 foi aposentado em 27/04/2026 e o Hub Qdrant é a fonte única agora.
   *(2026-05-04)*

3276. A auditoria do Chat foi concluída e vários problemas foram identificados, incluindo questões de segurança, confiabilidade e arquitetura.
   *(2026-05-02)*

3277. O arquivo gus-identity.md está desatualizado e precisa ser consolidado com o bootstrap.
   *(2026-05-04)*

3278. O Connector está quebrado e exige um key para a API do MCP para funcionar.
   *(2026-05-03)*

3279. No workflow `migrar_gus_para_hub.py`, scroll na coleção `gus` retornou 0 fragmentos.
   *(2026-05-03)*

3280. A nova estrutura `Gus-Sync/dialogos/inbox-gustavo/{chat,code,tiogu}/` no Drive permite a captura direta sem frontmatter.
   *(2026-05-03)*

3281. A avaliação do projeto NeuroGus está bloqueada até que decisões de UX sejam tomadas.
   *(2026-05-03)*

3282. Renomeações de pastas e ajustes de captura de dados foram feitas para melhorar a estrutura do projeto.
   *(2026-05-03)*

3283. Os 204 fragmentos históricos estavam no Mem0 SaaS (api.mem0.ai), não no Qdrant como achávamos.
   *(2026-05-03)*

3284. O curador do Telegram está apresentando erros recorrentes, indicando que o sistema de ingestão do Chat pode estar falhando.
   *(2026-05-03)*

3285. Gustavo é um anestesiologista, tem hipertireoidismo e tem projetos ativos na Phronesis, MGE, TER, Axon e Gus.
   *(2026-05-03)*

3286. Após o cadastro do Connector, deve-se validar a integração fazendo uma nova conversa no Chat.
   *(2026-05-03)*

3287. Esses 4 dão 80% do contexto pra qualquer aba nova.
   *(2026-05-03)*

3288. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3289. O arquivo '_estado-atual.md' está desatualizado em relação ao projeto.
   *(2026-05-02)*

3290. A decisão de migração ADR-001 ainda está em curso, visando aposentar o Mem0 SaaS.
   *(2026-05-03)*

3291. O sistema de agente pessoal multi-porta utiliza memórias no Hub Qdrant, arquivos .md no GitHub espelhados no Drive. Gustavo é anestesiologista e todas as implementações passam pela assistente virtual Gus.
   *(2026-05-03)*

3292. Esses 4 arquivos dão 80% do contexto pra qualquer aba nova.
   *(2026-05-03)*

3293. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

3294. O Gus possui um mix de dados em sua estrutura atual: 204 fragmentos da memória antiga (Mem0 SaaS) e 40 fragmentos no Hub Qdrant.
   *(2026-05-03)*

3295. Gustavo Pratti de Barros é um anestesiologista baseado no Rio de Janeiro, trabalhando na Dimagem (clínica de diagnóstico por imagem, três unidades: Nova Iguaçu, Taquara, São Gonçalo). Além do trabalho clínico, ele é um pesquisador independente ativo em IA e construtor de sistemas operando em vários projetos de pesquisa e produtos simultaneamente.
   *(2026-05-04)*

3296. O último estado do documento gus-estado-atual.md foi gerado em 27/04, e está desatualizado.
   *(2026-05-03)*

3297. O `_frontmatter-referencia.md` é apenas um template.
   *(2026-05-04)*

3298. O curador é o componente que integra a memória central no Gus.
   *(2026-05-03)*

3299. O status da migração é controlado pela decisão ADR-001, que visa aposentar o Mem0 SaaS e consolidar o Hub Qdrant com o estado atual do projeto.
   *(2026-05-03)*

3300. Haverá uma escolha de modelo definitivo após o término da coleta dual de modelos.
   *(2026-05-03)*

3301. PR #72 agora tem 2 commits, 10 arquivos e mudanças de +720 linhas e -130 linhas, após resolução dos conflitos.
   *(2026-05-03)*

3302. Sobre a decisão de manter `drop_pending_updates=True`, uma abordagem recomendada é logar o count de pending e avisar o Gustavo no boot.
   *(2026-05-02)*

3303. Hub é mais fresco que `gus-estado-atual.md` (que é snapshot das 03h).
   *(2026-05-03)*

3304. O bootstrap-v6 já cobre a funcionalidade anteriormente descrita no gus-identity.md.
   *(2026-05-03)*

3305. O Hub Qdrant é a nova fonte da verdade.
   *(2026-05-03)*

3306. A coleta de modelos no curador é dual, utilizando Haiku e GPT-4o-mini.
   *(2026-05-03)*

3307. Os arquivos com as demandas pendentes são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template `_frontmatter-referencia.md`.
   *(2026-05-02)*

3308. Os arquivos obrigatórios para toda aba nova são: dialogos/_bootstrap/gus-bootstrap.md, dialogos/_bootstrap/gus-identity.md, dialogos/_bootstrap/gus-estado-atual.md e projetos/gus/_estado-atual.md.
   *(2026-05-02)*

3309. As 18 entradas que entraram em modo `fallback-mem0` em 28/04 não estão na coleção `gus`.
   *(2026-05-03)*

3310. Vou ler as 2 demandas pendentes + docs de próximos passos + PRs recentes em paralelo.
   *(2026-05-02)*

3311. O sistema possui um cron que processa transcripts não-processados a cada 30 minutos.
   *(2026-05-03)*

3312. O arquivo untracked é só esse log honesto: "00:26:07 BRT — sessão encerrada".
   *(2026-05-02)*

3313. A auditoria diária é cega para o brain 'gus' e ignora fragmentos que já foram gravados.
   *(2026-05-03)*

3314. A captura proativa do Chat em tempo real agora é instrução explícita no bootstrap.
   *(2026-05-03)*

3315. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) vai terminar no dia 12/05/2026.
   *(2026-05-03)*

3316. O conteúdo dos 204 fragmentos está seguro em `historico/` e não há pressa para importá-los diretamente.
   *(2026-05-03)*

3317. O estado de migração do Hub Qdrant é uma prioridade, devendo ser tratado até o dia 12/05/2026.
   *(2026-05-03)*

3318. Após criar um arquivo no Drive, o cron pegará e auto-injetará frontmatter em ≤15min.
   *(2026-05-03)*

3319. Após a adição do `MCP_URL_SECRET`, o Railway precisa ser redeployado para que as alterações entrem em vigor.
   *(2026-05-03)*

3320. O sistema de Gus atualmente tem 40 fragmentos, sendo que 70% destes são considerados lixo.
   *(2026-05-03)*

3321. A coleção legada `gus` tem ~204 fragmentos não migrados ao Hub Qdrant.
   *(2026-05-03)*

3322. O log do retro-engine está em `claude/greeting-checkin-94weM`.
   *(2026-05-03)*

3323. O cron de promoção `ativo → estavel` é necessário, mas não foi implementado.
   *(2026-05-03)*

3324. O brain 'gus' ganha cobertura explícita para meta_reflexao, identidade_operacional e procedural.
   *(2026-05-03)*

3325. Através do workflow `migrar_gus_para_hub.py`, a coleção `gus` foi confirmada vazia.
   *(2026-05-03)*

3326. A migração da memória do Mem0 para o Qdrant Hub foi concluída em 27/04/2026.
   *(2026-05-04)*

3327. Gustavo é anestesiologista e não programa, toda implementação passa pelo Gus/Tiogu.
   *(2026-05-03)*

3328. O estado final dos PRs já está no código e nos docs gus-XX atualizados.
   *(2026-05-03)*

3329. Os projetos ativos incluem Phronesis-Bench, NeuroGus, MGE/MGX, TER e Axon.
   *(2026-05-03)*

3330. As 18 entradas `fallback-mem0` de 28/04 foram pro Mem0 SaaS porque a migração ainda não estava 100% deployada.
   *(2026-05-03)*

3331. A seção 'Personalidade do Gus (somente Telegram)' precisa ser migrada para gus/system_prompt.md.
   *(2026-05-04)*

3332. O Hub Qdrant é a fonte da verdade, com arquivos .md no GitHub espelhados no Drive.
   *(2026-05-03)*

3333. Em volume crescente, o brain `gus` pode virar cópia ruidosa do brain `gustavo`. Buscar identidade do Gus pode retornar fato sobre Gustavo.
   *(2026-05-03)*

3334. A stack está em estado intermediário arriscado: a coleção legada 'gus' tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

3335. A auditoria do sistema de memória end-to-end foi marcada como crítico devido a falhas que podem levar à poluição cruzada de informações.
   *(2026-05-03)*

3336. O passo 1 consiste em setar `MCP_URL_SECRET` no Railway para proteger o MCP.
   *(2026-05-03)*

3337. A fase 2B do projeto envolve a revisão do system prompt, que precisa ser atualizado para refletir mudanças nas ferramentas e na arquitetura do bot.
   *(2026-05-03)*

3338. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md` e `_frontmatter-referencia.md`.
   *(2026-05-02)*

3339. O que é o Gus: Sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa). Memória central no Hub Qdrant (`gus_hub`), arquivos .md no GitHub (`Gustpbbr/Gus`), espelhados no Drive.
   *(2026-05-03)*

3340. O sistema Gus agora utiliza o Hub Qdrant como fonte única de memória.
   *(2026-05-03)*

3341. O sistema tem um mecanismo de captura de múltiplas entradas por meio de diferentes interfaces.
   *(2026-05-03)*

3342. O curador deve registrar automaticamente as atualizações com timestamps e estatísticas de acesso.
   *(2026-05-03)*

3343. A migração do sistema Mem0 para o Hub Qdrant deve ser realizada, e detalhes sobre a execução se encontram em documentos no GitHub.
   *(2026-05-03)*

3344. A coleta dual de modelos no curador (Haiku e GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

3345. A amostragem de dados mostrou que os fragmentos do Mem0 SaaS continham informações biográficas relevantes e decisões arquivadas.
   *(2026-05-03)*

3346. O workflow de migração descobriu que a coleção 'gus' está vazia, apesar das menções a 204 fragmentos.
   *(2026-05-03)*

3347. Sessão 3B da Fase 2 abordará a reescrita do arquivo `system_prompt.md` para melhorar o desempenho do bot.
   *(2026-05-02)*

3348. As memórias em Qdrant e Mem0 SaaS devem ser geridas separadamente.
   *(2026-05-03)*

3349. O passo de decidir sobre o Drive sync foi resolvido automaticamente com a migração para WIF.
   *(2026-05-03)*

3350. O Hub Qdrant é a memória central do Gus, onde os arquivos .md são armazenados no GitHub e também são espelhados no Drive.
   *(2026-05-03)*

3351. As metas de operação para o Gus incluem a migração para um sistema mais limpo e melhor estruturado além da implementação de melhorias no curador.
   *(2026-05-03)*

3352. O estado atual do projeto será definido em um documento específico que deve ser consultado sempre que necessário.
   *(2026-05-03)*

3353. O último arquivo da demanda da semana está em `dialogos/streams/[semana-2026-04-21.md]`.
   *(2026-05-03)*

3354. A opção de manter o `drop_pending_updates=True` evita uma avalanche de updates após o deploy, mas impede que mensagens enviadas durante o downtime sejam processadas.
   *(2026-05-02)*

3355. Em 12/05/2026, Gustavo escolherá um modelo definitivo após a coleta dual de modelos no curador.
   *(2026-05-03)*

3356. O legado do Mem0 SaaS foi parcialmente preservado, com 204 fragmentos que foram exportados para análise futura.
   *(2026-05-03)*

3357. Bootstrap-v6 reescreveu a seção 'Como você captura memória pro Hub' com 2 caminhos: Caminho 1 (default) é mcp__gus-hub__ingestar_fragmento em tempo real durante a conversa, e Caminho 2 (escape) é upload .md em 'Gus-Sync/dialogos/inbox-chat-raw/' para sessões longas.
   *(2026-05-03)*

3358. Quatro portas ativas: Telegram (@Tiogubot), Claude Code, Claude Chat (com Connector MCP gus-hub) e Custom GPT em configuração.
   *(2026-05-03)*

3359. Os arquivos essenciais para o contexto do projeto são: dialogos/_bootstrap/gus-bootstrap.md, dialogos/_bootstrap/gus-identity.md, dialogos/_bootstrap/gus-estado-atual.md e projetos/gus/_estado-atual.md.
   *(2026-05-04)*

3360. A proposta de tiering melhora a organização das informações, dividindo o boot em partes essenciais e lazy-loaded.
   *(2026-05-03)*

3361. A migração ADR-001 está em curso, que aposenta Mem0 SaaS.
   *(2026-05-03)*

3362. O script 'limpeza_hub_dryrun.py' gera relatório de candidatos a delete no Hub.
   *(2026-05-03)*

3363. Há 3 produções simultâneas de fragmentos com 4× multiplicação de chamadas LLM por unidade de input.
   *(2026-05-03)*

3364. O Hub Qdrant é a fonte da verdade e está em processo de migração.
   *(2026-05-03)*

3365. O arquivo `gus-identity.md` não é a única fonte de verdade sobre o Gus e o Gustavo, pois a informação se encontra também no `gus-bootstrap.md`.
   *(2026-05-04)*

3366. As principais pendências incluem: setar `MCP_URL_SECRET` no Railway, decidir sobre a sincronização do Drive e deletar memórias poluídas.
   *(2026-05-03)*

3367. A convenção de nomenclatura de arquivos dos exames utiliza o formato <paciente_id>__<data_coleta>__<lab_curto>.json.
   *(2026-05-02)*

3368. A captura de memória agora pode ser realizada por meio de dois caminhos: o MCP em tempo real e o upload manual de arquivos .md.
   *(2026-05-04)*

3369. O curador é um sistema híbrido que utiliza Haiku e GPT-4o-mini em paralelo.
   *(2026-05-03)*

3370. A captura proativa do Chat agora é instrução explícita no bootstrap.
   *(2026-05-03)*

3371. Três demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md` e `_frontmatter-referencia.md` (esse é template, não é demanda).
   *(2026-05-02)*

3372. O bootstrap possui muita gordura, com protocolos que Chat só usa quando Gustavo pede algo específico.
   *(2026-05-03)*

3373. As demandas pendentes para a porta Claude Code estão disponíveis no dialogos/inbox-claude-code e incluem: captura-multiporta-curador, drive-sync-oauth-fix e pendencias-claude-chat-consolidacao.
   *(2026-05-03)*

3374. O bootstrap atual menciona buscar_hub mas não destaca que pra brain gus precisa passar user_id='gus' explicitamente.
   *(2026-05-03)*

3375. A auditoria do Claude Chat resultou na correção de 12 bugs, incluindo um bug crítico do curador.
   *(2026-05-03)*

3376. Os quatro principais arquivos obrigatórios para toda nova aba são: `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md`, e `estado-atual.md`.
   *(2026-05-03)*

3377. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3378. Pendencias-claude-chat-consolidacao é uma demanda pendente no inbox-claude-code.
   *(2026-05-03)*

3379. Estou aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`, algumas com nome quebrado.
   *(2026-05-03)*

3380. Hub Qdrant é a fonte da verdade após migração.
   *(2026-05-03)*

3381. Os 4 documentos essenciais para contexto em qualquer aba nova são: dialogos/_bootstrap/gus-bootstrap.md, dialogos/_bootstrap/gus-identity.md, dialogos/_bootstrap/gus-estado-atual.md e projetos/gus/_estado-atual.md.
   *(2026-05-02)*

3382. Três opções de solução para o Drive sync: resetar OAuth, criar Service Account, ou aposentar Drive sync.
   *(2026-05-03)*

3383. Mem0 SaaS será aposentado em favor do Hub Qdrant como fonte da verdade.
   *(2026-05-03)*

3384. A auditoria diária é cega para o brain gus e classifica por keywords, ignorando a área que o curador já preencheu.
   *(2026-05-03)*

3385. O Hub Qdrant é a nova fonte da verdade do sistema de agente pessoal multi-porta.
   *(2026-05-03)*

3386. O workflow de Drive Sync OAuth pode falhar ao acessar a conta Google, o que faz com que `sync_to_drive.py` não funcione corretamente.
   *(2026-05-03)*

3387. Estado de migração ADR-001 em curso: aposentar Mem0 SaaS, Hub Qdrant é fonte da verdade.
   *(2026-05-03)*

3388. Core obrigatório sempre, em toda aba nova: dialogos/_bootstrap/gus-bootstrap.md, dialogos/_bootstrap/gus-identity.md, dialogos/_bootstrap/gus-estado-atual.md, projetos/gus/_estado-atual.md.
   *(2026-05-03)*

3389. O PR número 93 foi aberto para consolidar o conteúdo do gus-identity.md no bootstrap e system_prompt.
   *(2026-05-04)*

3390. Gustavo Pratti de Barros é anestesiologista no Dimagem e pesquisador independente em IA.
   *(2026-05-04)*

3391. Existem 4 demandas pendentes no diálogo relacionado ao Claude Code: captura-multiporta-curador, drive-sync-oauth-fix, e pendencias-claude-chat-consolidacao.
   *(2026-05-03)*

3392. A captura de sessões do Stop hook foi verificada como funcional após os merges dos PRs.
   *(2026-05-02)*

3393. Gus é um sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, etc.).
   *(2026-05-03)*

3394. Em 03/05/2026, Gustavo testou a captura real-time do Claude Chat (Caminho 1 via MCP) com sucesso. Neste momento: Cleir dormindo no colo dele e aniversário da Babi.
   *(2026-05-03)*

3395. O estado final dos PRs já está no código e nos docs gus-XX atualizados.
   *(2026-05-03)*

3396. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md` e `_frontmatter-referencia.md` (template, não é demanda).
   *(2026-05-02)*

3397. As decisões sobre o Drive sync e o acesso ao Hub são essenciais para o funcionamento operacional do Chat.
   *(2026-05-03)*

3398. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3399. Necessário regenerar o segredo do MCP.
   *(2026-05-03)*

3400. O estado atual do bot Telegram inclui caches de prompts e multilinguagem.
   *(2026-05-04)*

3401. A stack de memória está em estado intermediário arriscado.
   *(2026-05-03)*

3402. O bot Telegram está em produção na Railway com 21 tools.
   *(2026-05-02)*

3403. A migração do Mem0 para o Hub Qdrant foi concluída em 27/04/2026, conforme mencionado na ADR-001.
   *(2026-05-03)*

3404. Os arquivos de protocolo incluem: `gus-protocolo-demanda.md`, `gus-protocolo-drive.md`, `gus-pastas-do-projeto.md`, e `gus-tipos-fragmento.md`.
   *(2026-05-03)*

3405. As 18 entradas que entraram no modo 'fallback-mem0' não estão na coleção 'gus'.
   *(2026-05-03)*

3406. Gustavo é falante nativo de português, baseado no Rio de Janeiro. Interesses intelectuais fortes em segurança em IA, filosofia e systems thinking. Gosta de viajar e desenvolve uma casa de fim de semana em Paty do Alferes com sistemas sustentáveis de água e design arquitetônico.
   *(2026-05-03)*

3407. A migração do sistema Mem0 para Hub Qdrant está na fase 4.
   *(2026-05-03)*

3408. As demandas pendentes em `dialogos/inbox-claude-code/` incluem '2026-05-01-captura-multiporta-curador.md' e '2026-05-01-drive-sync-oauth-fix.md'.
   *(2026-05-02)*

3409. Gustavo Pratti de Barros é anestesiologista no Dimagem e pesquisador independente em IA.
   *(2026-05-04)*

3410. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e a hipótese é que o refresh token OAuth expirou.
   *(2026-05-02)*

3411. O planejamento do NeuroGus está 100% pronto e faltam ~145 linhas para implementar.
   *(2026-05-02)*

3412. O projeto envolve um bot chamado TioGu, que utiliza uma arquitectura de multi-porta com Hub Qdrant como memória central. O sistema é montado para integrar diferentes APIs e faz uso de ferramentas como Claude AI e Telegram.
   *(2026-05-02)*

3413. A pasta do Drive se chama Gus-Sync, não GitHub-Sync.
   *(2026-05-04)*

3414. O `_estado-atual.md` de 27/04 está desatualizado, havendo muitas mudanças depois.
   *(2026-05-02)*

3415. O curador Telegram está com erro 400 recorrente, mostrando apenas uma entrada por dia com erro, o que pode implicar que o ingest do Chat esteja falhando silenciosamente.
   *(2026-05-03)*

3416. O sistema tem 3 produções simultâneas de fragmentos com 4 vezes multiplicação de chamadas LLM por unidade de input.
   *(2026-05-03)*

3417. As decisões sobre o modelo do curador devem ser tomadas até 12/05/2026.
   *(2026-05-03)*

3418. O arquivo de log gerado pelo retro-engine contém a informação de que não foi possível coletar fragmentos devido à ausência da chave ANTHROPIC_API_KEY.
   *(2026-05-02)*

3419. Existem atualmente 357 candidatos em limpezas de memória.
   *(2026-05-03)*

3420. O core obrigatório para qualquer aba nova inclui: dialogos/_bootstrap/gus-bootstrap.md, dialogos/_bootstrap/gus-identity.md, dialogos/_bootstrap/gus-estado-atual.md, projetos/gus/_estado-atual.md.
   *(2026-05-03)*

3421. A auditoria diária é cega para o brain gus e classifica por keywords ignorando o area que o curador já preencheu.
   *(2026-05-03)*

3422. Estou aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3423. O TioGu é um sistema multi-porta integrado ao Hub Qdrant, que opera no Telegram e conecta com outras instâncias.
   *(2026-05-03)*

3424. O Gustavo é anestesiologista e não programa — toda implementação passa pelo Gus ou Tiogu.
   *(2026-05-03)*

3425. O sistema Gus não deve ter a identidade técnica de Mem0 na camada de memórias do Claude Chat.
   *(2026-05-03)*

3426. O estado final dos PRs está no código e nos documentos atualizados. PRs descrevem o caminho, não o estado atual, e uma nova aba deve referir-se ao estado atual do projeto.
   *(2026-05-03)*

3427. O `_estado-atual.md` de 27/04 está desatualizado, pois mostra muita coisa depois do PRs #57, #60, #63, #64, #67.
   *(2026-05-04)*

3428. Os fragmentos no Hub são classificados, mas o sistema ainda apresenta vulnerabilidades que podem levar à poluição de dados.
   *(2026-05-03)*

3429. O sistema deve fornecer mensagens amigáveis ao usuário em casos de falhas, como a falta de créditos na API do Anthropic.
   *(2026-05-03)*

3430. 1. Gustavo dispara regularmente workflow `import-from-drive.yml` para sincronizar arquivos do Drive com GitHub — tempo de execução esperado é até 15 minutos
2. Gustavo prefere confirmação clara quando workflows são disparados
3. Gus é a identidade unificada do agente pessoal; Tiogu é apenas o bot no Telegram — mesma entidade, memória e princípios em múltiplas plataformas (Claude Chat, Claude Code, futuro Alexa e Custom GPT)
4. Gustavo tem 4 demandas abertas do dia 26/04 que continuam sem novidade
   *(2026-04-28)*

3431. Gus está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

3432. A migração ADR-001 está em curso, e o Hub Qdrant se tornará a fonte da verdade.
   *(2026-05-03)*

3433. Há um tratamento de risco clínico real no fluxo de Dimagem, onde um nome trocado em prontuário é tratado com bloqueio e reenvio em vez de alerta.
   *(2026-05-02)*

3434. As diretrizes operacionais incluem não alucinar e validar informações.
   *(2026-05-03)*

3435. A solução para o problema de sincronização com o Google Drive envolve três opções: 1 - reset de OAuth, 2 - uso de uma Service Account ou 3 - aposentadoria da sincronização.
   *(2026-05-02)*

3436. Gus é um agente pessoal multi-porta com memória central no Hub Qdrant.
   *(2026-05-03)*

3437. A configuração de `MCP_URL_SECRET` no Railway é necessária para que o MCP não rode público.
   *(2026-05-03)*

3438. O sistema Gus é um agente pessoal multi-porta conectado a várias interfaces, incluindo Telegram, Claude Code, Claude Chat e futuras interfaces.
   *(2026-05-03)*

3439. Há 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3440. Chat lê Drive stale desde 01/05 às 14:38 UTC por expiração do token do OAuth.
   *(2026-05-03)*

3441. Foram promovidas mudanças na estrutura do bot com a divisão de `bot.py`, reduzindo seu tamanho de 649 linhas para 80 linhas, enquanto as funcionalidades foram distribuídas em módulos separados.
   *(2026-05-03)*

3442. A auditoria da memória e do Hub Qdrant está em estado crítico, com riscos de corrupção silenciosa.
   *(2026-05-03)*

3443. A coleção legada `gus` ainda viva, fallback Mem0 ativo em leitura/delete e lê: lembrar/scroll.
   *(2026-05-03)*

3444. A causa do erro 400 é a interpretação incorreta de placeholders no template JSON.
   *(2026-05-02)*

3445. A stack atual está em estado intermediário arriscado devido à coexistência da coleção legada e da nova.
   *(2026-05-03)*

3446. A aba com MCP gus-hub conectado deve usar ferramentas MCP ao invés de arquivo .md.
   *(2026-05-03)*

3447. Gustavo é o autor do projeto Gus.
   *(2026-05-03)*

3448. _frontmatter-referencia.md é um template, não é uma demanda.
   *(2026-05-02)*

3449. O sistema Gus está em produção: um agente de IA multiporta (bot do Telegram, Claude Code, Claude Chat com conector MCP, Custom GPT em configuração, Alexa planejada).
   *(2026-05-03)*

3450. O `_estado-atual.md` (27/04) está desatualizado.
   *(2026-05-02)*

3451. O estado da stack de memória é de estado intermediário arriscado: Hub Qdrant é a fonte nova, mas a coleção legada gus (Mem0 self-hosted) tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

3452. Decisões arquiteturais devem ser registradas como ADR e não em PRs.
   *(2026-05-03)*

3453. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, `_frontmatter-referencia.md`.
   *(2026-05-03)*

3454. A fase 1 do TioGu foi concluída, com 163 testes verdes.
   *(2026-05-03)*

3455. A auditoria diária é cega para o brain gus e classifica por keywords ignorando o area que o curador já preencheu.
   *(2026-05-03)*

3456. Migração Mem0 → Hub Qdrant está na Fase 4 e coleta dual Haiku × Sonnet roda até 12/05.
   *(2026-05-03)*

3457. A documentação está sendo mantida em dia, essencial para referência futura e validação de decisões.
   *(2026-05-02)*

3458. Atualmente, o TioGu utiliza LLMs da Anthropic e OpenAI, com fallback integrado para cada um.
   *(2026-05-02)*

3459. NeuroGus é uma visualização 3D do Hub e está totalmente desenhado.
   *(2026-05-03)*

3460. Hub Qdrant é a fonte da verdade e coleta dual de modelos no curador (Haiku × GPT-4o-mini, mudou de Sonnet em 29/04 por custo/resiliência) termina 12/05/2026.
   *(2026-05-03)*

3461. O sistema inclui um mecanismo de caching de promts, permitindo maior eficiência nas chamadas aos LLMs.
   *(2026-05-02)*

3462. Os testes de unidade cobririam o caminho crítico do bot, incluindo LLM dispatch e memória.
   *(2026-05-02)*

3463. 1. Hub Qdrant agora funciona corretamente — 2+ fragmentos salvos, merge resolveu o problema crítico; Gustavo pode enviar PDFs quando quiser.

2. Sistema de curador híbrido (Haiku + Sonnet em paralelo) está operacional com schema gus-18 completo, embeddings locais via sentence-transformers, e controle de ciclo de vida (ativo/histórico/esquecido).

3. Experimento de 14 dias coletando pares Haiku × Sonnet encerra ~12/05/2026; após isso, Gustavo analisará logs em `_log/resumos-mem0/` no Obsidian para decidir qual modelo(s) manter.

4. Canal `dialogos/` operacional em ambas direções: workflow `notificar-inbox-tiogu.yml` notifica bot quando arquivo entra em inbox; tool `rotear_arquivo` permite mover arquivos após confirmação.

5. 16 workflows ativos (dobrou desde última análise): notificação inbox, archive automático, migração Qdrant, migração Mem0→Qdrant, importação Drive, etc.

6. Pendências técnicas: PR #10 ainda aberta (cosmético), workflow "Ingest Mem0 from Claude Chat" falhando (provável endpoint antigo), `memory.py` importa mem0ai à toa (limpeza Fase 5), suporte a vídeo ainda falta.

7. Estrutura repo expandida: novas pastas `api/`, `scripts/`, `_log/`, `agenda/`, `docs/`.
   *(2026-04-27)*

3464. A auditoria do sistema confirmou que o caminho `fallback-mem0` escreve em Mem0 SaaS em vez de no Hub Qdrant.
   *(2026-05-03)*

3465. O sistema Gus é um agente pessoal multi-porta, incluindo Telegram, TioGu, Claude Code, Claude Chat e futuras integrações como Custom GPT mobile e Alexa.
   *(2026-05-03)*

3466. O Hub Qdrant é a fonte da verdade para o sistema de agentes pessoais multi-porta.
   *(2026-05-03)*

3467. A auditoria diária é cega para o brain gus e só considera o brain gustavo.
   *(2026-05-03)*

3468. Os dois checks do PR #72 passaram verde: pytest e smoke-test.
   *(2026-05-03)*

3469. Hub `gustavo` contém 20 fragmentos, com 70% reconhecidos como lixo.
   *(2026-05-03)*

3470. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

3471. A atualização do '_estado-atual.md' foi marcada como pendente.
   *(2026-05-02)*

3472. O sistema tem fallback cross-vendor, se OpenAI falha, ele tenta Anthropic, garantindo maior resiliência.
   *(2026-05-04)*

3473. Decisão de manter a opção de exportar defensivo do Mem0 SaaS antes de apagá-lo.
   *(2026-05-03)*

3474. O arquivo `gus-estado-atual.md` deve ser gerado a cada 15 minutos e conter ego cache, decisões recentes, reflexões ativas e fragmentos das últimas 6 horas.
   *(2026-05-04)*

3475. O arquivo `gus/bot.py` foi reduzido de 649 linhas para 80 após a refatoração, separando handlers e state em módulos distintos.
   *(2026-05-04)*

3476. A coleta dual de modelos no curador termina em 12/05/2026.
   *(2026-05-03)*

3477. O Hub Qdrant está ocioso há 6h+ na janela 'fragmentos últimas 6h'.
   *(2026-05-02)*

3478. Os documentos essenciais para o projeto são: manual operacional do Gus, identidade do Gustavo e estado atual gerado pelo cron.
   *(2026-05-03)*

3479. A divergência entre os outputs do Haiku e do GPT é dramática, com o Haiku rejeitando fragmentos.
   *(2026-05-03)*

3480. A validação do estado atual do projeto é feita por auditorias diárias.
   *(2026-05-03)*

3481. O estado final dos PRs já está no código e nos documentos atualizados.
   *(2026-05-03)*

3482. O curador está rodando em loop com 100% de erro há pelo menos 3 dias.
   *(2026-05-03)*

3483. O Hub atual tem cerca de 500 a 600 fragmentos, com aproximadamente 70% do conteúdo considerando lixo.
   *(2026-05-03)*

3484. As atualizações mais recentes incluem a correção do bug do formato no curador e a estruturação do Hub.
   *(2026-05-03)*

3485. Os caminhos de escrita na stack do Gus têm regras parcialmente compatíveis.
   *(2026-05-03)*

3486. O estado do sistema e das atuações de Gus, incluindo decisões operacionais e pendências, são geridos através do conector MCP em produção na Railway.
   *(2026-05-03)*

3487. A captura multiporta curador (A/B/C) está pendente de aprovação de Gustavo.
   *(2026-05-03)*

3488. O sistema funcional para captura está com 4× multiplicação de chamadas LLM por unidade de input.
   *(2026-05-03)*

3489. Existem 3 demandas paradas em 'dialogos/inbox-claude-code/'.
   *(2026-05-02)*

3490. Os testes de saúde do MCP devem ser realizados após a configuração do URL secret para confirmar que está funcionando corretamente.
   *(2026-05-03)*

3491. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3492. O arquivo `estado-atual.md` reúne informações sobre onde paramos na sessão anterior.
   *(2026-05-03)*

3493. O estado final dos PRs já tá no código + nos docs gus-XX atualizados. PRs descrevem o caminho, não onde a gente tá.
   *(2026-05-03)*

3494. O caminho `fallback-mem0` escreve em Mem0 SaaS, não documentado, é um vetor de perda contínua.
   *(2026-05-03)*

3495. A migração de conteúdos da Mem0 SaaS para o Hub Qdrant foi implementada, e a coleta de dados agora ocorre diretamente no novo sistema.
   *(2026-05-03)*

3496. A demanda 2026-05-01-captura-multiporta-curador.md precisa de um gatilho proativo no Chat.
   *(2026-05-03)*

3497. A coleta dual de modelos no curador termina em 12/05/2026 — depois Gustavo escolhe modelo definitivo.
   *(2026-05-03)*

3498. A auditoria do sistema de memória end-to-end foi realizada, revelando que há 204 fragmentos em Mem0 SaaS.
   *(2026-05-03)*

3499. A pasta criada deve ter sincronização com o Hub.
   *(2026-05-03)*

3500. O bug do curador ocorreu entre 29/04 e 02/05.
   *(2026-05-03)*

3501. A demanda #3 é uma guarda-chuva que referencia as demandas #1 e #2 dentro dela.
   *(2026-05-02)*

3502. O sistema Gus foi consolidado em produção, com captura em tempo real funcionando corretamente.
   *(2026-05-03)*

3503. Os fragmentos do brain 'gus' estão apresentando risco de poluição cruzada com fragmentos do brain 'gustavo'.
   *(2026-05-03)*

3504. A publicação do Phronesis-Bench está em revisão e envolvida em preparação para o Alignment Forum.
   *(2026-05-03)*

3505. Os demandantes têm a demanda de corrigir a sincronização do Google Drive que parou desde 01/05.
   *(2026-05-03)*

3506. A migração para Hub Qdrant está em curso com a data de término prevista para 12/05/2026.
   *(2026-05-03)*

3507. A coleção legada `gus` está vazia.
   *(2026-05-03)*

3508. A manutenção do bot inclui a atualização periódica das dependências e a facilitação de testes para garantir sua operação.
   *(2026-05-04)*

3509. Gustavo precisa adicionar saldo em sua conta no Anthropic para que o Haiku do curador funcione.
   *(2026-05-04)*

3510. Gus é um sistema de agente pessoal multi-porta com memória central no Hub Qdrant.
   *(2026-05-03)*

3511. A coleta dual de modelos no curador parte do Haiku e vai até GPT-4o-mini.
   *(2026-05-03)*

3512. Em volume crescente, brain `gus` vira cópia ruidosa do brain `gustavo`. Buscar identidade do Gus retorna fato sobre Gustavo.
   *(2026-05-03)*

3513. A coleta dual de modelos no curador, utilizando Haiku e GPT-4o-mini, termina em 12/05/2026, após o que Gustavo escolhe o modelo definitivo.
   *(2026-05-03)*

3514. O funcionamento do TioGu está atrelado à eficiência do curador, que se encarrega da coleta de fragmentos e do processamento de memória.
   *(2026-05-04)*

3515. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e depende da decisão sobre o refresh token OAuth.
   *(2026-05-04)*

3516. A demanda da semana está documentada no arquivo `semana-2026-04-21.md`.
   *(2026-05-03)*

3517. Atualmente, a stack de memória está em estado intermediário arriscado com débitos que podem estourar quando o volume crescer.
   *(2026-05-03)*

3518. A auditoria do Hub Qdrant revelou que o sistema possui fragmentos não-migrados e com risco de perda de dados.
   *(2026-05-03)*

3519. Os testes automatizados cobrem caminhos críticos do sistema, incluindo dispatch de LLM, retries, memória, state, regex, validações, e scanner de PII.
   *(2026-05-02)*

3520. A auditoria do Claude Chat identificou 12 fixes entre 31 achados, incluindo o bloqueio crítico do curador.
   *(2026-05-03)*

3521. O estado final dos PRs já está no código e nos docs gus-XX atualizados.
   *(2026-05-03)*

3522. A migração Mem0 para Hub Qdrant está na fase 4, e a coleta dual de Haiku e Sonnet deve terminar em 12/05, quando a decisão sobre o modelo do curador final será tomada.
   *(2026-05-02)*

3523. O código do bot possui mais de 5.800 LOC em total, incluindo múltiplas integrações.
   *(2026-05-04)*

3524. O `_estado-atual.md` (27/04) está bem desatualizado — o git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67).
   *(2026-05-02)*

3525. A coleta dual Haiku × Sonnet roda até 12/05, e depois decidirão o modelo final do curador.
   *(2026-05-03)*

3526. Houve capturas de dados para o dia 2026-05-03.
   *(2026-05-03)*

3527. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

3528. Hub `gustavo` tem 20 fragmentos, ~70% lixo.
   *(2026-05-03)*

3529. A auditoria diária (`auditoria_hub.py`) é cega para o brain gus e classifica por keywords ignorando o area.
   *(2026-05-03)*

3530. A captura diária das memórias e o sistema de auditoria do hub não estão sincronizados, resultando em incoerências de logs e na estrutura das memórias.
   *(2026-05-03)*

3531. A URL do Connector no claude.ai precisa ser atualizada após a configuração do segredo.
   *(2026-05-03)*

3532. A terceira demanda é intitulada `_frontmatter-referencia.md` e é um template, não é uma demanda.
   *(2026-05-02)*

3533. Tenho 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3534. Um panorama geral do projeto foi solicitado e será analisado junto com as últimas atualizações que não estão nos documentos citados.
   *(2026-05-02)*

3535. As pendências de Gustavo incluem setar `MCP_URL_SECRET` no Railway e decidir sobre a sincronização do Drive.
   *(2026-05-03)*

3536. Os itens das demandas são: captura multiporta, curador bidirecional cron, drive-sync OAuth e demandas do Chat.
   *(2026-05-03)*

3537. O Hub Qdrant é a fonte da verdade no sistema Gus.
   *(2026-05-03)*

3538. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026. Após isso, Gustavo escolhe o modelo definitivo.
   *(2026-05-03)*

3539. A stack está em estado intermediário arriscado.
   *(2026-05-03)*

3540. O Chat acessa diversos documentos de referência em seu funcionamento, mas não possui uma estratégia de lazy loading definida.
   *(2026-05-03)*

3541. A auditoria do Chat envolve todos os aspectos relacionados ao projeto Claude Chat.
   *(2026-05-03)*

3542. O conteúdo do Mem0 SaaS foi confirmado como existente e acessível, o que muda a abordagem estratégica para a migração de dados.
   *(2026-05-03)*

3543. Foram realizados 1076+ fragmentos no Hub, com 551 no brain `gustavo` e 525 no brain `gus`.
   *(2026-05-03)*

3544. Gus coletou demandas pendentes do inbox e último stream da semana.
   *(2026-05-02)*

3545. O arquivo `gus-protocolo-drive.md` deve descrever limitações, convenções para reedições, e a ordem operacional ao editar arquivos no Drive.
   *(2026-05-04)*

3546. O Gus é um agente pessoal baseado na porta Chat e trabalha com informações sobre Gustavo e suas atividades. Utiliza o Hub Qdrant como memória e o Drive Gus-Sync como conhecimento.
   *(2026-05-03)*

3547. O sistema Gus é um agente pessoal multi-porta.
   *(2026-05-03)*

3548. O Gustavo Pratti de Barros é anestesiologista e não programa, toda implementação passa pelo Gus.
   *(2026-05-03)*

3549. A captura de autoreflexão do agente foi bem-sucedida, salvando um fragmento com observações críticas sobre o seu funcionamento durante a sessão.
   *(2026-05-03)*

3550. Decisão sobre a escolha do modelo de curadoria (Haiku ou GPT) deve ser feita apenas em 12/05/2026.
   *(2026-05-03)*

3551. Gus é um sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa).
   *(2026-05-03)*

3552. O arquivo `gus-bootstrap.md` contém o manual operacional do Gus, com regras de comportamento e como cada porta usa o Hub.
   *(2026-05-03)*

3553. Após fazer boot, o Chat deve responder de forma casual, como 'E aí, beleza? Gus aqui, pronto. O que vamos trabalhar?'
   *(2026-05-04)*

3554. A coleção legada `gus` na Qdrant está vazia e não contém fragmentos.
   *(2026-05-03)*

3555. Gustavo Pratti de Barros é anestesiologista.
   *(2026-05-03)*

3556. Os 204 fragmentos históricos que deveriam estar na coleção 'gus' não existem, a coleção está vazia.
   *(2026-05-03)*

3557. O arquivo 'Documento sem título.md' no inbox-claude-code não contém uma demanda válida.
   *(2026-05-03)*

3558. Gustavo Pratti de Barros está usando um sistema com um agente pessoal chamado Gus.
   *(2026-05-03)*

3559. O core obrigatório para qualquer aba nova inclui os arquivos: dialogos/_bootstrap/gus-bootstrap.md, dialogos/_bootstrap/gus-identity.md, dialogos/_bootstrap/gus-estado-atual.md e projetos/gus/_estado-atual.md.
   *(2026-05-03)*

3560. O código do bot TioGu possui aproximadamente 5.800 linhas de código organizado em diretórios como gus e hub.
   *(2026-05-02)*

3561. O estado final dos PRs já está no código e nos docs gus-XX atualizados.
   *(2026-05-03)*

3562. Trilha completa de deletados preserva o snapshot total.
   *(2026-05-03)*

3563. O conteúdo do Mem0 SaaS foi exportado para a pasta `historico/` com 208 fragmentos.
   *(2026-05-03)*

3564. Já existe uma referência a 'Usa Claude/ChatGPT-Kai/Gemini' que deve ser adicionada ao bootstrap.
   *(2026-05-04)*

3565. O projeto está estruturado em fases, com 9 itens na Fase 1 para desenvolver, incluindo a remoção de caminhos legados e limpeza de Hub.
   *(2026-05-03)*

3566. A escrita real-time do Chat depende do `MCP_URL_SECRET` no Railway.
   *(2026-05-03)*

3567. O Hub Qdrant é a memória central do Gus, onde os dados são armazenados.
   *(2026-05-03)*

3568. As 204 entradas prometidas na coleção legada `gus` não existem.
   *(2026-05-03)*

3569. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3570. As operações no Gus incluem a captura, curadoria e auditoria das memórias geradas.
   *(2026-05-03)*

3571. Existem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, `_frontmatter-referencia.md`.
   *(2026-05-02)*

3572. O schema gus-18 promete um ciclo de life de fragmentos (peso, acessos, promoções) que não está sendo implementado.
   *(2026-05-03)*

3573. O registro diário de auditoria até 02/05/2026 documentou o estado da memória.
   *(2026-05-03)*

3574. A coleta dual Haiku × Sonnet está programada para rodar até 12/05, após a qual será decidida sobre o modelo final do curador.
   *(2026-05-03)*

3575. A aba nova deve ler o arquivo `gus-estado-atual.md` e usar tools MCP sempre que possível.
   *(2026-05-03)*

3576. O sistema de agente pessoal multi-porta é chamado Gus.
   *(2026-05-03)*

3577. O script de limpeza do Hub, utilizando um dry run para identificar candidatos à exclusão, será criado após a aprovação da lista de candidatos marcada por Gustavo.
   *(2026-05-03)*

3578. A hélice de captura proativa durante a conversa não foi implementada; por isso, o Chat só salva fragmentos quando solicitado explicitamente.
   *(2026-05-03)*

3579. Esses 4 arquivos dão 80% do contexto pra qualquer aba nova.
   *(2026-05-03)*

3580. O Hub Qdrant é a memória central do sistema Gus.
   *(2026-05-03)*

3581. A coleta dos 204 fragmentos não migrados da coleção legada `gus` é uma pendência a ser resolvida.
   *(2026-05-03)*

3582. O Hub tem 19 fragmentos no brain `gustavo`, e está ocioso há 6h.
   *(2026-05-03)*

3583. Gustavo tem hipertireoidismo em tratamento com Tapazol, acompanhado por endocrinologista.
   *(2026-05-03)*

3584. O `MEM0_API_KEY` deve ser removido para evitar qualquer risco de acesso ao conteúdo antigo no Mem0 SaaS.
   *(2026-05-03)*

3585. Os fronts ativos incluem o saneamento do TioGu e a auditoria do Claude Chat.
   *(2026-05-03)*

3586. Gustavo está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-02)*

3587. O modelo Haiku + GPT-4o foi introduzido no curador de Chat com a intenção de melhorar a curadoria de memórias.
   *(2026-05-03)*

3588. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

3589. O projeto Gus possui um sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) com Hub Qdrant como memória central.
   *(2026-05-03)*

3590. É necessário adicionar saldo na conta do Anthropic para que ele volte a funcionar.
   *(2026-05-03)*

3591. Após o fix do `format()`, o curador voltou a salvar fragmentos após ficar em modo silencioso.
   *(2026-05-03)*

3592. Quatro demandas estão pendentes no `dialogos/inbox-claude-code/`.
   *(2026-05-04)*

3593. Confirmei que, na busca padrão, considera Brain 'gustavo' ao invés de 'gus'.
   *(2026-05-04)*

3594. As demandas pendentes são captura multiporta, curador bidirecional cron e drive-sync OAuth.
   *(2026-05-03)*

3595. Hub Qdrant é a fonte da verdade.
   *(2026-05-03)*

3596. Os 204 fragmentos exportados do Mem0 SaaS foram considerados de qualidade superior ao Hub atual.
   *(2026-05-03)*

3597. O Hub é mais fresco que o gus-estado-atual.md, que é um snapshot recorrente feito às 03h. Sempre que possível, preferir tools MCP a arquivos .md.
   *(2026-05-03)*

3598. A auditoria no Claude Chat resultou em 12 correções de 31 achados e a correção de um bug crítico no curador.
   *(2026-05-03)*

3599. O sistema Gus é um agente pessoal multi-porta que roda sobre uma arquitetura de Hub Qdrant.
   *(2026-05-03)*

3600. A pasta `Gustavo/` em `Gus-Sync/dialogos/` deve conter subpastas para as demandas do usuário: `Chat/`, `Code/` e `TioGu/`.
   *(2026-05-03)*

3601. O sistema de agente pessoal Gus é multi-porta, incluindo Telegram, Claude Chat e Claude Code.
   *(2026-05-03)*

3602. O curador híbrido (Haiku × Sonnet/GPT) coleta dual até 12/05 para avaliação de desempenho.
   *(2026-05-02)*

3603. O bot Telegram, TioGu, possui cerca de 21 ferramentas.
   *(2026-05-02)*

3604. A função 'curar_turnos' irá processar o conteúdo dos transcripts e extrair fragmentos para o Hub.
   *(2026-05-03)*

3605. O core obrigatório é composto por quatro arquivos que dão 80% do contexto pra qualquer aba nova.
   *(2026-05-03)*

3606. Gus é um sistema de agente pessoal multi-porta (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa).
   *(2026-05-03)*

3607. A migração para o Hub Qdrant está em curso com datas específicas e um modelo a ser definido.
   *(2026-05-03)*

3608. O bot Telegram (TioGu) possui ~21 tools, multimídia, prompt caching, e está em produção no Railway.
   *(2026-05-02)*

3609. Ego_cache_atual() fornece identidade, últimas decisões e meta-reflexões.
   *(2026-05-03)*

3610. As demandas pendentes foram listadas, com 3 demandas reais: captura multiporta, curador bidirecional cron, drive-sync OAuth.
   *(2026-05-03)*

3611. O `_estado-atual.md` (27/04) está bem desatualizado — git log mostra muita coisa depois.
   *(2026-05-02)*

3612. O arquivo 'dialogos/_bootstrap/gus-identity.md' define quem é o Gustavo e quem é o Gus enquanto entidade.
   *(2026-05-02)*

3613. Os logs do Railway estão expondo o `MCP_URL_SECRET` em texto claro.
   *(2026-05-03)*

3614. A auditoria do Chat envolve todos os aspectos relacionados ao projeto Claude Chat.
   *(2026-05-03)*

3615. O Hub Qdrant é a nova fonte da verdade e a coleta dual de modelos termina em 12/05/2026.
   *(2026-05-03)*

3616. Recadastrar o Connector no claude.ai após rotacionar o secret.
   *(2026-05-03)*

3617. Os arquivos com as demandas pendentes são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template `_frontmatter-referencia.md`.
   *(2026-05-03)*

3618. A última atualização do `_estado-atual.md` foi em 27/04, e ele está desatualizado em comparação ao `gus-estado-atual.md` que está fresco.
   *(2026-05-03)*

3619. O estado de migração ADR-001 está em curso para aposentar Mem0 SaaS.
   *(2026-05-03)*

3620. O Drive sync GitHub→Drive parece estar quebrado, com commits para o arquivo parar em 14:38Z 01/05.
   *(2026-05-03)*

3621. Tenho 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3622. As demandas pendentes no `dialogos/inbox-claude-code/` são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao.
   *(2026-05-03)*

3623. O log do retro-engine está em `claude/greeting-checkin-94weM`.
   *(2026-05-03)*

3624. A pasta do Google Drive se chama Gus-Sync.
   *(2026-05-03)*

3625. O MCP está público — qualquer scanner que descobrir a URL Railway lê todo o Hub. A URL secret protege isso e destrava também escrita real-time do Chat (ingestar_fragmento).
   *(2026-05-03)*

3626. Para o estado atual do trabalho, pode-se buscar no Hub via ego_cache_atual ou fragmentos_recentes, ou ler dialogos/_bootstrap/gus-estado-atual.md, que é atualizado a cada 15 minutos.
   *(2026-05-03)*

3627. O sistema usa um Bot Telegram chamado TioGu, que possui cerca de 21 ferramentas.
   *(2026-05-02)*

3628. A frontmatter para novas demandas deve incluir tipo:demanda, origem:claude-chat, destino:tiogu, prioridade, status:pendente, criado_em, processado_em, processado_por, acao_sugerida e destino_path.
   *(2026-05-03)*

3629. Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template `_frontmatter-referencia.md`.
   *(2026-05-03)*

3630. Há 4 caminhos de escrita coexistindo com regras parcialmente compatíveis.
   *(2026-05-03)*

3631. A seção 'Personalidade do Gus (somente Telegram)' está misturando informações que deveriam ser exclusivas para o bot com informações gerais do sistema.
   *(2026-05-03)*

3632. Gus é um sistema de agente pessoal multi-porta que integra várias plataformas (Telegram, Claude Code, Claude Chat).
   *(2026-05-03)*

3633. Vi que tem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, `_frontmatter-referencia.md` (esse é template, não é demanda).
   *(2026-05-02)*

3634. O commit referente à Sessão 1 da Fase 1 foi feito com o ID 55c1de8, incluindo o workflow de CI para rodar testes em PR e push na branch principal.
   *(2026-05-02)*

3635. O botão 'Merge pull request' foi presenciado durante o processo de merge.
   *(2026-05-02)*

3636. O arquivo `dialogos/_bootstrap/gus-estado-atual.md` é um snapshot do Hub gerado automaticamente pelo cron a cada 03h.
   *(2026-05-02)*

3637. Os commits mostram bastante coisa nova: PR #67 (curador-chat bidirecional + GPT-4o), PR #64 (captura transcripts Code via cron), PR #60 (MCP URL secret), PR #70 (demanda consolidada).
   *(2026-05-03)*

3638. A função de fallback para PDF não será implementada, e uma mensagem amigável será exibida ao usuário.
   *(2026-05-04)*

3639. As demandas paradas são: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, e `_frontmatter-referencia.md`.
   *(2026-05-02)*

3640. Os documentos essenciais para qualquer aba nova são: `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md` e `estado-atual.md`. Eles fornecem 80% do contexto necessário.
   *(2026-05-03)*

3641. O sistema de agente pessoal multi-porta inclui uma memória central no Hub Qdrant, com arquivos .md no GitHub espelhados no Drive.
   *(2026-05-03)*

3642. O conteúdo da coleção 'gus' no Qdrant estava vazio.
   *(2026-05-03)*

3643. A captura de fragmentos deve ser feita via três entradas simultâneas: Telegram, Claude Chat e Claude Code.
   *(2026-05-03)*

3644. A prioridade default para novas demandas pode ser definida como 'media'.
   *(2026-05-03)*

3645. O sistema "Gus" é um agente pessoal multi-porta em produção, operando com Qdrant Hub.
   *(2026-05-04)*

3646. O Hub Qdrant é a fonte da verdade.
   *(2026-05-03)*

3647. A migração Mem0 → Hub Qdrant está na fase 4 (ADR-001).
   *(2026-05-03)*

3648. O Hub Qdrant é a memória central do Gus, onde estão armazenados os dados e informações.
   *(2026-05-03)*

3649. Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3650. O arquivo `gus-identity.md` apresenta drift factual, com duas linhas erradas: a primeira menciona que Mem0 é a memória relacional, quando na verdade foi aposentado e o Hub Qdrant é a fonte única. A segunda linha se refere ao nome da pasta do Google Drive, que foi alterada para `Gus-Sync`.
   *(2026-05-03)*

3651. Todo fragmento criado antes da migração vai existir só na coleção antiga, fora do Hub novo.
   *(2026-05-03)*

3652. Decisão de migração ADR-001 está em curso: aposentar Mem0 SaaS, Hub Qdrant será a fonte da verdade.
   *(2026-05-03)*

3653. O bot possui um sistema de gate de confiança para proteger dados sensíveis, especialmente na visualização de arquivos PDF.
   *(2026-05-02)*

3654. A estrutura de ferramentas (tools) do bot foi modificado para melhorar a modularidade e manutenção do código.
   *(2026-05-04)*

3655. O estado atual do trabalho pode ser consultado via `ego_cache_atual` ou `fragmentos_recentes`.
   *(2026-05-04)*

3656. O sistema Gus possui quatro portas ativas: Telegram, Code, Chat e Custom GPT.
   *(2026-05-03)*

3657. A coleção legada gus ainda está viva, com fallback Mem0 ativo em leitura/delete.
   *(2026-05-03)*

3658. tô aqui na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

3659. Recentemente, o foco de trabalho foi na melhoria do sistema: o PR #72 consertou um erro de 100% na curadoria (KeyError no template JSON), o PR #80 redigiu a exposição de segredos nos logs do MCP, e o PR #83 introduziu o bootstrap-v6 com dois caminhos de captura (MCP em tempo real + upload curado).
   *(2026-05-04)*

3660. O sistema de captura de PII no TioGu é limitado, pois a verificação de dados sensíveis ocorre apenas antes de salvar no GitHub, não na saída do bot.
   *(2026-05-02)*

3661. O Hub Qdrant apresenta 3 produções simultâneas de fragmentos, gerando um custo multiplicado por 4 no uso de chamadas LLM.
   *(2026-05-03)*

3662. A documentação do projeto é armazenada no Google Drive em 'Gus-Sync', que é indexado.
   *(2026-05-03)*

3663. A API do bot usa o framework python-telegram-bot na versão 21.6.
   *(2026-05-04)*

3664. O script 'ingest_mem0_from_chat.py' será renomeado para 'ingest_chat_raw.py'.
   *(2026-05-03)*

3665. O `_estado-atual.md` da pasta projetos/gus está desatualizado, data de 27/04.
   *(2026-05-03)*

3666. A auditoria é cega para o brain gus e classifica por keywords ignorando o area que o curador já preencheu.
   *(2026-05-03)*

3667. Gustavo é anestesiologista e não programa. Toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

3668. A composição de fragmentos criados é gerada a partir de 3 produções simultâneas (Telegram, Chat, Code), resultando em múltiplas chamadas LLM.
   *(2026-05-03)*

3669. O sistema multi-porta usa o Hub Qdrant como memória central.
   *(2026-05-02)*

3670. Atualmente, há 3 produções simultâneas de fragmentos, com 4× multiplicação de chamadas LLM por unidade de input.
   *(2026-05-03)*

3671. A stack está em estado intermediário arriscado com múltiplas produções simultâneas de fragmentos.
   *(2026-05-03)*

3672. Os resultados dos testes de integração e auditoria são cruciais para garantir a qualidade e a funcionalidade do sistema.
   *(2026-05-03)*

3673. Atividades pendentes do Gustavo incluem setar `MCP_URL_SECRET` no Railway e recadastrar Connector claude.ai.
   *(2026-05-03)*

3674. Os arquivos com as demandas pendentes incluem: captura-multiporta-curador, drive-sync-oauth-fix e pendencias-claude-chat-consolidacao.
   *(2026-05-03)*

3675. O workflow de migração `migrar_gus_para_hub.py` não encontrou fragmentos na coleção `gus` ao testar uma execução em modo dry-run.
   *(2026-05-03)*

3676. Gustavo não escreve código, e toda implementação deve minimizar passos manuais e maximizar sucesso na primeira tentativa.
   *(2026-05-03)*

3677. O sistema permite capturar memórias de diversas fontes, mas tem riscos associados com a poluição de dados.
   *(2026-05-03)*

3678. Gustavo Pratti de Barros é a identidade principal do Gus.
   *(2026-05-02)*

3679. Drive sync parece quebrado — commits até 01/05 e depois silêncio.
   *(2026-05-03)*

3680. A documentação do projeto está organizada em uma pasta chamada Gus-Sync.
   *(2026-05-03)*

3681. Quatro portas ativas são: Telegram, Claude Code, Claude Chat e Custom GPT em configuração.
   *(2026-05-03)*

3682. A seção 'Disciplina anti-esquecimento' do Gus encontra-se atualizada para incluir dois caminhos de captura.
   *(2026-05-03)*

3683. Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template.
   *(2026-05-03)*

3684. O curador apresentou um bug entre 29/04 e 02/05.
   *(2026-05-03)*

3685. A decisão de não permitir deletar memórias se torna um controle adicional na arquitetura do projeto.
   *(2026-05-03)*

3686. Foi proposto um plano de oito itens para limpeza e estruturação do Hub, visando a correção dos problemas identificados.
   *(2026-05-03)*

3687. A coleção legada 'gus' está vazia, e não há fragmentos a serem migrados.
   *(2026-05-03)*

3688. O sistema de agente pessoal do Gus utiliza memória central no Hub Qdrant e arquivos .md no GitHub.
   *(2026-05-03)*

3689. O Hub atual já tem 70% de meta-lixo, e não vale arriscar mais com poluição silenciosa.
   *(2026-05-03)*

3690. O sistema de cache de prompts reduz o custo de chamadas ao LLM em até 70%.
   *(2026-05-04)*

3691. O sistema Gus possui uma arquitetura de duas camadas com o Hub Qdrant, sendo 'gustavo' para fatos e 'gus' para autoreflexão, evitando redundância.
   *(2026-05-03)*

3692. A demanda `2026-05-01-captura-multiporta-curador.md` precisa de um gatilho proativo no Chat.
   *(2026-05-03)*

3693. `gus-identity.md` é redundante em relação ao bootstrap e contém informações desatualizadas.
   *(2026-05-04)*

3694. A parte única da 'Personalidade do Gus' deve ser movida para o `gus/system_prompt.md`.
   *(2026-05-03)*

3695. A pasta Google Drive relacionada ao sistema se chama Gus-Sync, não GitHub-Sync.
   *(2026-05-03)*

3696. A recomendação é seguir com a opção A agora e planejar a C dentro da Fase 5.
   *(2026-05-03)*

3697. Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e o `_frontmatter-referencia.md` que é só template.
   *(2026-05-03)*

3698. Há um downtime programado em 12/05/2026 para escolher o modelo definitivo após coleta dual de Haiku e GPT.
   *(2026-05-03)*

3699. A estrutura proposta para o Gus inclui um arquivo de boot mínimo, arquivos lazy on-demand e um estado dinâmico gerado periodicamente.
   *(2026-05-03)*

3700. O arquivo `gus-estado-atual.md` precisa ser atualizado a cada 15 minutos e deve refletir o estado dinâmico do sistema.
   *(2026-05-03)*

3701. A divergência entre Haiku e GPT é de 4-0.
   *(2026-05-03)*

3702. O script de limpeza do Hub será chamado 'limpeza_hub_dryrun.py' e gerará um relatório '_indices/_limpeza-hub-candidatos.md'.
   *(2026-05-03)*

3703. Decisão de não importar os 204 fragmentos do Mem0 SaaS para o Hub Qdrant agora, mas planejar a importação na Fase 5.
   *(2026-05-03)*

3704. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026, depois Gustavo escolhe modelo definitivo.
   *(2026-05-03)*

3705. A auditoria do Chat revelou a necessidade de atualização da memória do Claude, que atualmente contém informações obsoletas sobre o sistema Gus.
   *(2026-05-04)*

3706. O workflow de migração confirmou que a coleção `gus` está vazia.
   *(2026-05-03)*

3707. A opção B de otimização propõe manter os arquivos essenciais no bootstrap e criar arquivos separados para protocolos de uso ocasional.
   *(2026-05-04)*

3708. Fragmentos são salvos no Hub com tags que especificam o tipo de conteúdo e o agente responsável pela captura.
   *(2026-05-03)*

3709. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

3710. A demanda da semana é o arquivo `dialogos/inbox-/` com pendências para essa porta.
   *(2026-05-04)*

3711. O `_estado-atual.md` (27/04) está desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).
   *(2026-05-02)*

3712. A execução atual das memórias ignora o lifecycle do schema gus-18, comprometendo a atualização dos acessos e pesos.
   *(2026-05-03)*

3713. O Hub Qdrant armazena a memória central do Gus e os arquivos .md são espelhados no GitHub.
   *(2026-05-03)*

3714. O frontend Claude Chat teve 12 correções de 31 achados durante a auditoria.
   *(2026-05-03)*

3715. O estado atual do projeto Gus é a migração da memória de Mem0 para Qdrant Hub direto (ADR-001, concluído em 27/04/2026).
   *(2026-05-03)*

3716. A auditoria concluiu que diversos aspectos do projeto Claude Chat precisam ser revisados para garantir conformidade e eficiência operacional.
   *(2026-05-03)*

3717. O bot é estruturado em múltiplos módulos, incluindo handlers para diferentes tipos de mensagens, um gerenciador de estado e uma camada de integração com múltiplos LLMs.
   *(2026-05-03)*

3718. O arquivo `gus-identity.md` contém as mesmas informações que o `gus-bootstrap.md`, mas com drift em relação a atualizações de conteúdo.
   *(2026-05-03)*

3719. O commit `cc6306d` inclui melhorias na auditoria e acompanhamento das interações do chat.
   *(2026-05-02)*

3720. Gustavo Pratti de Barros é um anestesiologista baseado no Rio de Janeiro, trabalhando na Dimagem (clínica de diagnóstico por imagem, três unidades: Nova Iguaçu, Taquara, São Gonçalo). Juntamente com o trabalho clínico, ele é um pesquisador independente ativo em inteligência artificial e construtor de sistemas, operando em múltiplos projetos de pesquisa e produtos simultaneamente.
   *(2026-05-03)*

3721. Gustavo desenvolve uma casa em Paty do Alferes.
   *(2026-05-03)*

3722. O curador do Gus espera implementar funcionalidades de atualização de memória, como 'peso', 'acessos', e 'tipo_esquecimento'.
   *(2026-05-03)*

3723. O sistema captura arquivos de demanda do claude-chat na pasta inbox-tiogu, relacionados à ingestão de exames no Hub.
   *(2026-05-03)*

3724. Os testes do novo recurso incluirão a validação do fallback para imagens quando Anthropic não estiver disponível.
   *(2026-05-04)*

3725. O primeiro passo a ser seguido é gerar um novo segredo (`MCP_URL_SECRET`).
   *(2026-05-03)*

3726. O estado final dos Pull Requests já está no código e nos documentos atualizados, as entradas, não na documentação antiga.
   *(2026-05-03)*

3727. A stack de memória end-to-end é auditada.
   *(2026-05-03)*

3728. Gustavo tem hipertireoidismo em tratamento.
   *(2026-05-03)*

3729. A auditoria diária (`auditoria_hub.py`) é cega para o brain `gus` e ignora o campo `area` que já foi preenchido pelo curador.
   *(2026-05-03)*

3730. A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida pelo PR #67, mas falta o gatilho proativo no Chat.
   *(2026-05-04)*

3731. Hub Qdrant é a nova fonte da verdade.
   *(2026-05-03)*

3732. Hoje o MCP tá público — qualquer scanner que descobrir a URL Railway lê todo o Hub.
   *(2026-05-03)*

3733. O Phronesis-Bench é um projeto ativo cujo documento 'Prudência Performática' foi finalizado e está em revisão para o Alignment Forum.
   *(2026-05-04)*

3734. A maior parte do conteúdo do gus-identity.md vive no gus-bootstrap.md ou deveria estar no system_prompt.
   *(2026-05-04)*

3735. A stack está em estado intermediário arriscado.
   *(2026-05-03)*

3736. As 204 memórias na coleção `gus` estão vazias e não foram migradas.
   *(2026-05-03)*

3737. A coleta dual de modelos no curador termina em 12/05/2026, quando Gustavo escolherá o modelo definitivo.
   *(2026-05-03)*

3738. Gustavo é falante nativo de português, baseado no Rio de Janeiro.
   *(2026-05-03)*

3739. O passo 4 do plano aborda as decisões de segurança sobre a Service Account no Drive.
   *(2026-05-03)*

3740. A migração ADR-001 está em curso, com o Hub Qdrant como fonte da verdade.
   *(2026-05-03)*

3741. A URL do MCP mudará de `/mcp` para `/<secret>/mcp`.
   *(2026-05-03)*

3742. A seção sobre 'nunca diga que não tem acesso à internet' precisa ser adicionada ao system_prompt.
   *(2026-05-04)*

3743. O arquivo `gus-estado-atual.md` é gerado a cada 15 minutos.
   *(2026-05-03)*

3744. O projeto Gus é um sistema multi-porta (Telegram, Claude Code, Claude Chat, futuros: Custom GPT, Alexa) com Hub Qdrant como memória central.
   *(2026-05-02)*

3745. A demanda da semana é o último arquivo da pasta dialogos/streams/semana-2026-04-21.md.
   *(2026-05-03)*

3746. O Hub Qdrant é a fonte da verdade do sistema de agente pessoal multi-porta.
   *(2026-05-03)*

3747. Gustavo está ativo em várias pesquisas de IA e produtos, trabalhando em um bot Telegram, implantação do Conector MCP e Custom GPT.
   *(2026-05-04)*

3748. Os projetos ativos de Gustavo incluem Phronesis, MGE, TER, Axon e Gus.
   *(2026-05-04)*

3749. Preciso gerar um novo segredo para o MCP URL.
   *(2026-05-03)*

3750. A arquitetura do TioGu é baseada em um sistema de memória centralizado via Hub Qdrant, com fallback para Mem0 em caso de perda de conexão.
   *(2026-05-02)*

3751. A coleta de fragmentos históricos não retornou nenhuma entrada na migração para o Hub.
   *(2026-05-03)*

3752. O arquivo `gus-identity.md` contém informações sobre quem é o Gustavo e quem é o Gus enquanto entidade.
   *(2026-05-03)*

3753. Houve um bug crítico no curador, onde format() falhou com KeyError no JSON literal.
   *(2026-05-03)*

3754. O Hub Qdrant é a fonte da verdade, coletando dual de modelos no curador.
   *(2026-05-03)*

3755. A próxima versão do bootstrap (v6.1) deve consolidar o conteúdo do 'gus-identity.md'.
   *(2026-05-03)*

3756. O conteúdo armazenado nos arquivos exportados é considerado de qualidade superior ao que está atualmente no Hub.
   *(2026-05-03)*

3757. O conteúdo do Hub atual consistia em meta-informações sobre workflows e bugs, ao contrário do conteúdo do Mem0 que era mais enriquecido.
   *(2026-05-03)*

3758. Anthropic (Sonnet 4.6) é utilizado para imagens, PDFs e documentos, enquanto OpenAI (gpt-4o-mini) é utilizado para texto puro.
   *(2026-05-04)*

3759. O Hub Qdrant é o único conteúdo atual, e os fragmentos legados não são relevantes.
   *(2026-05-03)*

3760. O Chat salva fragmentos quando solicitado pelo usuário, ativando a função 'ingestar_fragmento'.
   *(2026-05-03)*

3761. O sistema Hub está ocioso nas últimas 6 horas.
   *(2026-05-03)*

3762. O Gus lê os arquivos que estão listados em dialogos/_bootstrap em cada nova aba que inicia.
   *(2026-05-03)*

3763. Mem0 SaaS contém 204 fragmentos exportados.
   *(2026-05-03)*

3764. Os commits mais recentes mostram atualizações em várias demandas, incluindo PR #67 (curador-chat bidirecional + GPT-4o) e PR #64 (captura transcripts Code via cron).
   *(2026-05-04)*

3765. A migração para o Hub Qdrant está em curso com o objetivo de aposentar o Mem0 SaaS.
   *(2026-05-03)*

3766. O MCP está público, permitindo acesso total ao Hub sem proteção.
   *(2026-05-03)*

3767. O sistema de Dimagem foi projetado para bloquear informações sensíveis em documentos enviados para o bot, mantendo a segurança e privacidade dos usuários.
   *(2026-05-03)*

3768. O Gus é um sistema de agente pessoal multi-porta, que integra diferentes plataformas como Telegram, Claude Code, Claude Chat, e futuras implementações como Custom GPT mobile e Alexa.
   *(2026-05-03)*

3769. Após setar a variável, aguardar o redeploy no Railway que leva cerca de 2 a 3 minutos.
   *(2026-05-03)*

3770. O estado final dos PRs já está no código e nos documentos gus-XX atualizados.
   *(2026-05-02)*

3771. O retro-engine é um hook que roda quando uma sessão Claude Code termina e deveria capturar a sessão, mas falta a variável ANTHROPIC_API_KEY.
   *(2026-05-02)*

3772. Os arquivos de referência devem ser buscados via project knowledge quando necessário.
   *(2026-05-04)*

3773. A auditoria diária do Hub é responsável por verificar a qualidade e a quantidade das memórias armazenadas.
   *(2026-05-03)*

3774. O sistema atualmente utiliza 4 chamadas de LLM por unidade de input, o que gera um custo elevado.
   *(2026-05-03)*

3775. As decisões sobre o futuro do projeto Gus, como a implementação do NeuroGus, aguardam confirmação de Gustavo.
   *(2026-05-04)*

3776. O projeto é um sistema de agente pessoal multi-porta que integra várias plataformas, com uma memória central no Hub Qdrant e arquivos no GitHub.
   *(2026-05-03)*

3777. O sistema Gus tem um problema de cross-brain pollution entre os brains 'gustavo' e 'gus'.
   *(2026-05-03)*

3778. A estrutura do projeto Claude Chat implica uma integração entre várias ferramentas, incluindo Drive e Github, para otimizar o fluxo de trabalho.
   *(2026-05-04)*

3779. Os quatro arquivos `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md` e `_estado-atual.md` dão 80% do contexto pra qualquer aba nova.
   *(2026-05-03)*

3780. Há 3 demandas paradas em dialogos/inbox-claude-code/
   *(2026-05-02)*

3781. A stack está em estado intermediário arriscado: Hub Qdrant é a fonte nova, mas a coleção legada 'gus' tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

3782. O bot Telegram possui ~21 tools, multimídia, prompt caching em produção.
   *(2026-05-02)*

3783. Esses 4 dão 80% do contexto pra qualquer aba nova.
   *(2026-05-03)*

3784. A proposta de otimização A consiste em reordenar o bootstrap, mantendo os arquivos atuais e fazendo algumas reorganizações.
   *(2026-05-03)*

3785. A arquitetura do TioGu é multi-provider com fallback cross-vendor, permitindo resiliência.
   *(2026-05-02)*

3786. Se decidir Drive sync, três opções: reset OAuth, Service Account, ou aposentar enviar Drive.
   *(2026-05-03)*

3787. O Hub Qdrant é a fonte da verdade e armazena a memória central do Gus.
   *(2026-05-03)*

3788. O Hub Qdrant armazena dois brains independentes: um para informações sobre Gustavo e outro para a autorreflexão do agente.
   *(2026-05-04)*

3789. Os quatro arquivos obrigatórios fornecem 80% do contexto para qualquer nova aba.
   *(2026-05-03)*

3790. A stack está em estado intermediário arriscado.
   *(2026-05-03)*

3791. O novo segredo deve ser cadastrado no Connector do claude.ai após a rotação.
   *(2026-05-03)*

3792. Após validação do MCP, o usuário pode prosseguir para recadastrar o Connector no claude.ai.
   *(2026-05-03)*

3793. O projeto implica na necessidade de uma auditoria frequente e na atualização dos sistemas de memória para garantir a qualidade dos dados.
   *(2026-05-03)*

3794. A coleção gus no Hub Qdrant está vazia, sem ação.
   *(2026-05-03)*

3795. A captura de transcripts no Claude Code está sendo resolvida pelo PR #64.
   *(2026-05-03)*

3796. O Hub Qdrant é a memória central do sistema Gus.
   *(2026-05-03)*

3797. A auditoria diária (`auditoria_hub.py`) é cega ao brain `gus` e ignora sua relevância e informações.
   *(2026-05-03)*

3798. O arquivo `system_prompt.md` foi editado cirurgicamente para remover seções obsoletas relacionadas ao modelo de memória Mem0.
   *(2026-05-04)*

3799. A aposentadoria do Mem0 SaaS está planejada para ocorrer após 12/05/2026, quando termina a coleta dual A/B entre Haiku e GPT-4o-mini.
   *(2026-05-04)*

3800. Gustavo é anestesiologista, não programa.
   *(2026-05-03)*

3801. Atualmente, estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes.
   *(2026-05-03)*

3802. Recomenda-se mover o arquivo `dimagem.py` para o diretório `integrations/`, uma vez que ele representa uma integração específica e não é parte do núcleo do projeto.
   *(2026-05-02)*

3803. Os logs do retro-engine indicam 'no-op: anthropic_missing' devido à falta da variável ANTHROPIC_API_KEY na porta Code.
   *(2026-05-02)*

3804. O estado final dos PRs já está no código + nos docs gus-XX atualizados.
   *(2026-05-03)*

3805. O Hub Qdrant é usado como memória central do sistema.
   *(2026-05-02)*

3806. O sistema vai sincronizar arquivos de texto puro, .md, .html, .csv e Google Docs nativos.
   *(2026-05-03)*

3807. O arquivo `gus-identity.md` apresenta redundâncias com o arquivo `gus-bootstrap.md`, duplicando informações sobre o Gustavo, seus projetos e diretrizes operacionais.
   *(2026-05-03)*

3808. O ADR-001 está em curso: aposentando o Mem0 SaaS e terminando a coleta dual de modelos no curador até 12/05/2026.
   *(2026-05-03)*

3809. O workflow de sincronização entre o Google Drive e o GitHub foi disparado com sucesso.
   *(2026-05-02)*

3810. Cada chamada ao curador gera 4 chamadas de LLM com o mesmo prompt, aumentando o custo e o risco de poluição cross-brain.
   *(2026-05-03)*

3811. O curador do Chat deve evitar redundâncias entre os canais de escrita e ter hierarquia clara.
   *(2026-05-03)*

3812. A sessão atual está com 40 fragmentos, dos quais 70% são lixo.
   *(2026-05-03)*

3813. O estado do conexão do MCP é acessível por qualquer pessoa que conhecer a URL.
   *(2026-05-03)*

3814. A demanda 2026-05-01-drive-sync-oauth-fix.md está ativa.
   *(2026-05-02)*

3815. Existem 4 demandas pendentes no `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3816. O bot Telegram (TioGu) é baseado em python-telegram-bot e possui cerca de 21 ferramentas.
   *(2026-05-04)*

3817. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3818. O estado final dos PRs já está no código + nos documentos gus-XX atualizados. PRs descrevem o caminho, não onde estamos. Nova aba quer onde estamos.
   *(2026-05-03)*

3819. Existem 6 demandas pendentes para a porta de Claude Code.
   *(2026-05-03)*

3820. A captura em tempo real do Chat é uma decisão a ser tomada, podendo aumentar a interação de decisões relevantes durante a conversa.
   *(2026-05-02)*

3821. A demanda #3 da consolidação deve ser esclarecida por Gustavo antes de proceder.
   *(2026-05-04)*

3822. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

3823. Os 4 documentos obrigatórios do Gus dão 80% do contexto pra qualquer aba nova.
   *(2026-05-03)*

3824. O sistema Gus é um agente pessoal multiporta em produção, rodando em uma arquitetura de Hub Qdrant.
   *(2026-05-04)*

3825. A memória central do Gus está no Hub Qdrant, com arquivos .md no GitHub e espelhados no Drive.
   *(2026-05-03)*

3826. A recomendação é usar a Opção 1 com 1 PR consolidado, commits separados por item, permitindo fácil revisão ao abrir o PR e dar scroll para ver o que mudou em cada commit.
   *(2026-05-03)*

3827. O estado da coleção legada `gus` é vazio, confirmando que não há fragmentos a serem migrados.
   *(2026-05-03)*

3828. Houve atualizações recentes no sistema e o estado atual do projeto foi verificado.
   *(2026-05-03)*

3829. Amoistragem mostrou conteúdo biográfico real, preferências de trabalho e decisões arquiteturais.
   *(2026-05-03)*

3830. Gustavo é anestesiologista, não programa — toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

3831. O sistema Gus é um agente multi-porta consolidado em produção, com a captura em real-time funcionando.
   *(2026-05-04)*

3832. Estado de migração para o Hub Qdrant é a fonte da verdade. Coleta dual de modelos no curador (Haiku × GPT-4o-mini), mudou de Sonnet em 29/04 por custo/resiliência.
   *(2026-05-03)*

3833. A pasta do Google Drive se chama Gus-Sync, não GitHub-Sync.
   *(2026-05-03)*

3834. Gustavo é anestesiologista e não programa — toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

3835. Nos últimos trabalhos, focou na consolidação do sistema Gus e na migração para o Hub Qdrant.
   *(2026-05-03)*

3836. O `_estado-atual.md` (27/04) está desatualizado em relação ao git log.
   *(2026-05-02)*

3837. Existem 4 caminhos de escrita que coexistem dentro do sistema, mas nem todos possuem regras totalmente compatíveis.
   *(2026-05-03)*

3838. O arquivo `_estado-atual.md` da pasta projetos/gus está de 27/04 — desatualizado.
   *(2026-05-03)*

3839. O sistema 'Gus' — agente pessoal multi-porta — está em produção. Quatro portas ativas: Telegram (@Tiogubot), Claude Code, Claude Chat (com Connector MCP gus-hub) e Custom GPT em configuração; Alexa planejada como porta futura.
   *(2026-05-03)*

3840. O plenário de testes do Curador foi modificado após a correção do bug.
   *(2026-05-02)*

3841. O `gus-identity.md` é redundante com o bootstrap e está desatualizado.
   *(2026-05-04)*

3842. O dispatcher decide qual modelo usar com base no tipo de mensagem.
   *(2026-05-04)*

3843. A proposta é dividir o bootstrap em arquivos lazy para otimização e clareza.
   *(2026-05-03)*

3844. A auditoria do Chat indicou que o curador Telegram enfrenta um erro 400 recorrente, prejudicando a captura de dados.
   *(2026-05-03)*

3845. O arquivo 'projetos/gus/_estado-atual.md' mostra onde paramos na sessão anterior e é mais 'operacional' que o bootstrap.
   *(2026-05-02)*

3846. O estado do projeto está registrado em `_estado-atual.md`, que é um snapshot do Hub.
   *(2026-05-04)*

3847. A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida pelo PR #67 (curador bidirecional), mas falta o gatilho proativo no Chat.
   *(2026-05-02)*

3848. O cron do Hub Qdrant atualiza automaticamente o estado atual a cada 15 minutos.
   *(2026-05-03)*

3849. O core obrigatório em toda aba nova inclui 4 arquivos: `dialogos/_bootstrap/gus-bootstrap.md`, `dialogos/_bootstrap/gus-identity.md`, `dialogos/_bootstrap/gus-estado-atual.md`, e `projetos/gus/_estado-atual.md`.
   *(2026-05-02)*

3850. O novo canal Gus-Sync/dialogos/inbox-gustavo/{chat,code,tiogu}/ auto-injeta frontmatter, facilitando a captura via Drive.
   *(2026-05-03)*

3851. A demanda de sincronização do Drive foi resolvida com a migração para Workload Identity Federation.
   *(2026-05-03)*

3852. O sistema Gus é um agente pessoal multi-porta, com memória central no Hub Qdrant e arquivos .md no GitHub.
   *(2026-05-03)*

3853. Os itens 1.6 e 1.7 da Fase 1 envolvem decisões que devem ser tomadas durante a execução e são consideradas mais críticas.
   *(2026-05-03)*

3854. O estado atual do projeto inclui um bot Telegram, uma API Custom GPT, e um sistema de coleta dual para Haiku e GPT-4o.
   *(2026-05-04)*

3855. D3 envolve gerenciar pendências de mensagens durante redeploys, decidindo entre descartar mensagens ou avisar o usuário.
   *(2026-05-02)*

3856. Estou aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3857. Na pasta `dialogos/inbox-claude-code/` estão 4 demandas pendentes.
   *(2026-05-03)*

3858. O sistema 'Gus' é um agente pessoal multi-porta operando no Qdrant Hub, com projetos ativos como Phronesis-Bench, NeuroGus, MGE/MGX, TER e Axon.
   *(2026-05-03)*

3859. A estrutura de pastas do projeto Gus-Sync inclui as pastas: dialogos/, projetos/gus/, pessoal/, dimagem/, _indices/, _log/.
   *(2026-05-04)*

3860. O sistema de agente pessoal tem múltiplas portas como Telegram, Claude Code e futuras integrações como Alexa.
   *(2026-05-03)*

3861. A auditoria diária no sistema é realizada pelo arquivo `auditoria_hub.py`.
   *(2026-05-03)*

3862. Aba nova só precisa olhar PRs se for reportado bug específico no código.
   *(2026-05-03)*

3863. O curador Telegram apresenta um erro 400 recorrente, resultando em falha silenciosa na ingestão do Chat.
   *(2026-05-03)*

3864. A auditoria diária deve classificar as memórias por tipo e acompanhar o histórico de alterações.
   *(2026-05-03)*

3865. A estrutura proposta para o chat inclui um arquivo de boot mínimo e arquivos de protocolo carregados sob demanda.
   *(2026-05-03)*

3866. O secreto deve ser mantido fora de logs e transcripts para evitar vazamentos.
   *(2026-05-03)*

3867. Na pasta `dialogos/inbox-claude-code/` estão 4 demandas pendentes: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e o `_frontmatter-referencia.md` que é só template.
   *(2026-05-03)*

3868. O prompt para o curador não diferencia `gustavo` vs `gus` — é literalmente o mesmo texto.
   *(2026-05-03)*

3869. Faltam o status consolidado, próximos passos, NeuroGus, e os PRs recentes pra fechar o panorama.
   *(2026-05-02)*

3870. O MCP está público — qualquer scanner que descobrir a URL Railway lê todo o Hub.
   *(2026-05-03)*

3871. Os PRs mergeados depois do estado atual incluem atualizações relevantes para o funcionamento do Gus.
   *(2026-05-03)*

3872. O bot do Telegram, TioGu, possui 21 ferramentas distintas integradas.
   *(2026-05-03)*

3873. As últimas atualizações incluíram PRs para curador de chat bidirecional, captura de transcripts via cron e `MCP_URL_SECRET` no caminho do servidor MCP, mas ainda não ativado no Railway.
   *(2026-05-03)*

3874. Os principais arquivos obrigatórios em qualquer nova aba são: `dialogos/_bootstrap/gus-bootstrap.md`, `dialogos/_bootstrap/gus-identity.md`, `dialogos/_bootstrap/gus-estado-atual.md` e `projetos/gus/_estado-atual.md`.
   *(2026-05-04)*

3875. O Chat pode salvar fragmento sobre Gustavo no brain `gus` sem validação. `via=claude-chat` é hardcoded, mas `user_id` devia ter whitelist.
   *(2026-05-03)*

3876. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3877. Gustavo Pratti de Barros é anestesiologista no Dimagem (Rio de Janeiro) e pesquisador independente em IA, operando múltiplos projetos simultaneamente em pesquisa, produto e arquitetura.
   *(2026-05-03)*

3878. Para situações específicas, é necessário ler: `projetos/gus/gus-08-plano-proximos-passos.md`, `projetos/gus/gus-30-neurogus-roadmap.md`, `projetos/gus/gus-10-caminho-alexa.md`, entre outros.
   *(2026-05-04)*

3879. O acesso ao Hub Qdrant é feito através de um MCP server público no Railway.
   *(2026-05-02)*

3880. O último arquivo da pasta `dialogos/streams/semana-2026-04-21.md` é a demanda da semana mais atual.
   *(2026-05-03)*

3881. O Anthropic está sem créditos, o que significa que não é possível realizar busca ou interações com esse serviço até que sejam adicionados créditos.
   *(2026-05-03)*

3882. Decisão: rodar um script para verificar o conteúdo no Mem0 SaaS antes de apagá-lo.
   *(2026-05-03)*

3883. Auditando a estrutura do projeto Claude Chat, identifiquei que 4 arquivos de boot são carregados, totalizando 546 linhas e aproximadamente 6520 tokens.
   *(2026-05-04)*

3884. Gerar um sumário da situação atual com 80% do contexto fornece informações essenciais para as futuras atualizações do projeto.
   *(2026-05-03)*

3885. Gustavo é anestesiologista e está atualmente envolvido em projetos relacionados à Dimagem, MASE/ACEE, e Phronesis.
   *(2026-05-04)*

3886. A estrutura proposta para os arquivos de boot minimiza a carga inicial e melhora o desempenho do Chat.
   *(2026-05-03)*

3887. Um dos principais problemas encontrados foi a parada do log em `_log/resumos-mem0/`, que não registrou entradas após 01/05/2026.
   *(2026-05-04)*

3888. O `MCP_URL_SECRET` no Railway precisa ser setado novamente.
   *(2026-05-03)*

3889. A demanda de Drive sync OAuth está quebrada, dependendo da decisão de Gustavo.
   *(2026-05-03)*

3890. O Chat deve ser otimizado para carregar apenas as informações necessárias, aumentando sua eficiência e reduzindo o tempo de inicialização.
   *(2026-05-03)*

3891. PR #67 introduziu o curador chat bidirecional (Sonnet 4.6 + GPT-4o) que salva em `gustavo` + `gus`.
   *(2026-05-03)*

3892. Tem 3 demandas paradas em `dialogos/inbox-claude-code/`: `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md`, `_frontmatter-referencia.md` (template).
   *(2026-05-04)*

3893. A ramificação 'claude/initial-setup-iWTfL' possui 6 demandas pendentes.
   *(2026-05-03)*

3894. A coleta dual de modelos no curador termina em 12/05/2026.
   *(2026-05-03)*

3895. A aba nova só precisa olhar PRs se houver um bug específico no código que foi mexido recentemente.
   *(2026-05-03)*

3896. O Gus é um sistema de agente pessoal multi-porta, com memória central no Hub Qdrant e arquivos em .md no GitHub.
   *(2026-05-03)*

3897. É recomendado usar 'ego_cache_atual()' para obter identidade, últimas decisões e meta-reflexões sempre que a aba tem o MCP gus-hub conectado.
   *(2026-05-02)*

3898. Há 204 fragmentos não-migrados da coleção legada `gus`, e o código de leitura em `gus/memory.py` ainda faz fallback.
   *(2026-05-03)*

3899. O status 'fallback-mem0' nos logs mente, pois na verdade está gravando no Hub.
   *(2026-05-03)*

3900. O Hub tem 19 fragmentos no brain `gustavo`, e o sistema está ocioso há mais de 6 horas.
   *(2026-05-03)*

3901. O Hub Qdrant é a fonte da verdade no projeto.
   *(2026-05-03)*

3902. O PR #74 incluiu testes de regressão do curador, corrigindo um bug relacionado ao `format()`.
   *(2026-05-03)*

3903. O arquivo `gus-estado-atual.md` é um handoff auto-gerado pelo cron 03h, snapshot do Hub.
   *(2026-05-03)*

3904. A memória utilizada é o Hub Qdrant, que substitui o Mem0.
   *(2026-05-03)*

3905. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e relacionada ao refresh token OAuth expirado.
   *(2026-05-04)*

3906. O curador híbrido cross-vendor já cobre '1 vendor caiu'.
   *(2026-05-03)*

3907. Backbone de memória migrou de Mem0 para Qdrant Hub direto (ADR-001, concluído em 27/04/2026), com 1076+ fragmentos em dois brains independentes: 'gustavo' (fatos sobre o usuário) e 'gus' (autorreflexão do agente).
   *(2026-05-03)*

3908. O bot é baseado em python-telegram-bot e possui backend integrado com FastAPI.
   *(2026-05-02)*

3909. 1. Schema atual do Mem0 é `gus-18` com campos: `tipo`, `area`, `campa_temporal`, `confiança` — não possui campo `origem` (source de telegram/chat/code).
2. Gustavo quer melhorias no schema documentadas como sugestões, não ordens — com instrução explícita pra verificar se já não foi planejado/implementado em outra branch antes de agir.
3. Demandas de código são salvas em `dialogos/inbox-claude-code/` com prioridade e status claro.
4. `save_to_github` salva sempre na branch main por padrão — comportamento correto para que workflows de importação (`import-from-drive`, etc.) consigam ler as demandas.
   *(2026-04-28)*

3910. Hub Qdrant é a fonte da verdade. Coleta dual de modelos no curador (Haiku × GPT-4o-mini, mudou de Sonnet em 29/04 por custo/resiliência) termina em 12/05/2026.
   *(2026-05-03)*

3911. O sistema Gus deve minimizar passos manuais e maximizar o sucesso na primeira tentativa.
   *(2026-05-04)*

3912. A auditoria do sistema de memória revela que a stack está em estado intermediário arriscado, evidenciado pela coexistência de três produções de fragmentos e a ausência de deduplicação.
   *(2026-05-03)*

3913. Os últimos PRs que modificaram o código do projeto foram: PR #67 (curador-chat bidirecional + GPT-4o), PR #64 (captura transcripts Code via cron), PR #60 (MCP URL secret) e PR #70 (demanda consolidada).
   *(2026-05-02)*

3914. O Hub é a memória central do agente pessoal e é chamado de 'gus_hub'.
   *(2026-05-03)*

3915. O Hub Qdrant é a fonte da verdade.
   *(2026-05-03)*

3916. O sistema Gus é um agente pessoal multi-porta que opera via Telegram, Claude Code, Claude Chat, Custom GPT e Alexa planejada sobre um Qdrant Hub.
   *(2026-05-03)*

3917. A stack de memória está em um estado intermediário arriscado.
   *(2026-05-03)*

3918. O curador gera 4 chamadas de LLM por arquivo devido à co-existência do brain `gustavo` e `gus`.
   *(2026-05-03)*

3919. A demanda `2026-05-01-captura-multiporta-curador.md` está parcialmente resolvida mas precisa de um gatilho proativo no Chat.
   *(2026-05-04)*

3920. O arquivo _estado-atual.md está desatualizado com relação aos últimos PRs.
   *(2026-05-02)*

3921. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e hipótese é que o refresh token OAuth expirou.
   *(2026-05-03)*

3922. A demanda para Drive sync está ativa, com a hipótese de que o refresh token OAuth expirou.
   *(2026-05-02)*

3923. A arquitetura do Hub Qdrant é documentada em `gus-18-schema-indexacao.md` e outros arquivos relacionados.
   *(2026-05-03)*

3924. Para disparar todos os workflows, normalmente seria necessário executar cada um individualmente, pois não suporta disparo em lote.
   *(2026-05-03)*

3925. Eu vou auditar a stack de memória end-to-end do Hub Qdrant, incluindo a leitura crítica de código.
   *(2026-05-03)*

3926. O nome da pasta no Drive pode ser definido como 'Gustavo/' ou 'pelo-gustavo/'.
   *(2026-05-03)*

3927. Gustavo é anestesiologista, não programa — toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

3928. Quatro demandas pendentes no inbox-claude-code: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e o _frontmatter-referencia.md é só template.
   *(2026-05-04)*

3929. O `_estado-atual.md` está desatualizado, com data de 27/04.
   *(2026-05-03)*

3930. Os próximos passos incluem a migração de `gus` para `gus_hub` que ainda não foi executada.
   *(2026-05-03)*

3931. O Gus deve otimizar os arquivos que lê no início para melhorar a eficiência.
   *(2026-05-03)*

3932. O MCP está público — qualquer scanner que descobrir a URL Railway lê todo o Hub. URL secret protege.
   *(2026-05-03)*

3933. O `_estado-atual.md` está desatualizado e não reflete as PRs recentes que foram mergeadas depois da data mencionada.
   *(2026-05-03)*

3934. O contrato schema gus-18 está parcialmente implementado.
   *(2026-05-03)*

3935. A memória do sistema foi migrada de Mem0 para o Qdrant Hub direto, com 1076+ fragmentos em dois brains independentes: 'gustavo' para fatos sobre ele e 'gus' para autorreflexão do agente.
   *(2026-05-04)*

3936. O arquivo Gus-Sync contém espelho dos .md como Google Docs.
   *(2026-05-04)*

3937. Rodar script no `export_mem0.py` que pega tudo do Mem0 SaaS e grava JSON em `historico/mem0-export-final-2026-05-02.json`.
   *(2026-05-03)*

3938. Core obrigatório (sempre, em toda aba nova) são 4 arquivos que dão 80% do contexto pra qualquer aba nova.
   *(2026-05-03)*

3939. As últimas atualizações foram em 02/05, com PRs que tratam de testes de regressão e segurança do sistema.
   *(2026-05-03)*

3940. A amostragem mostrou conteúdo biográfico real, ao contrário do Hub atual que é meta-conversa.
   *(2026-05-03)*

3941. O `gus-tipos-fragmento.md` contém o schema gus-18 completo.
   *(2026-05-03)*

3942. A migração de Mem0 para o Hub Qdrant está em curso e a coleta dual termina em 12/05/2026, quando Gustavo escolherá o modelo definitivo.
   *(2026-05-03)*

3943. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3944. As últimas atualizações do projeto não estão necessariamente nos documentos citados.
   *(2026-05-02)*

3945. O estado de migração está em curso para substituir a Mem0 SaaS pelo Hub Qdrant.
   *(2026-05-03)*

3946. Três demandas reais estão pendentes no inbox-claude-code, focando em captura multiporta, curador bidirecional cron e drive-sync OAuth.
   *(2026-05-03)*

3947. A auditoria no projeto identificou problemas de segurança e confiabilidade relacionados à captura e armazenamento de dados.
   *(2026-05-04)*

3948. O curador no Hub Qdrant tem uma coleção dual de modelos que acabou causando redundância na captura de dados.
   *(2026-05-03)*

3949. A demanda 1 da consolidação trata da proteção do MCP público.
   *(2026-05-02)*

3950. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3951. O sistema Gus é um agente pessoal multi-porta com memória central no Hub Qdrant.
   *(2026-05-03)*

3952. Os arquivos que forem salvos na pasta Gustavo serão sincronizados para o Hub Qdrant automaticamente.
   *(2026-05-03)*

3953. Até 26/04/2026, o sistema de memória Mem0 SaaS estava em uso e os dados foram migrados para o Hub Qdrant.
   *(2026-05-03)*

3954. O desenvolvedor planeja manter a compatibilidade entre LLMs, permitindo fallback entre Anthropic e OpenAI.
   *(2026-05-02)*

3955. O sistema multi-porta inclui Telegram, Claude Code, e Claude Chat, com Hub Qdrant como memória central.
   *(2026-05-02)*

3956. Gustavo é anestesiologista e não programa — toda implementação passa por Tiogu.
   *(2026-05-03)*

3957. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa. Hipótese: refresh token OAuth expirou.
   *(2026-05-02)*

3958. O projeto tem 4 demandas pendentes no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao e um template chamado `_frontmatter-referencia.md`.
   *(2026-05-04)*

3959. O Hub Qdrant é a memória do Gus, e a coleta dual Haiku × Sonnet roda até 12/05, quando será decidido o modelo curador final.
   *(2026-05-03)*

3960. O workflow rodou em dry-run e não encontrou fragmentos a serem migrados da coleção gus.
   *(2026-05-03)*

3961. A auditoria diária é cega ao brain `gus`, que nunca aparece nos resultados de frescor ou densidade por área.
   *(2026-05-03)*

3962. Os testes do TioGu somam 187 verificações, todas com resultados positivos, garantindo a estabilidade do sistema.
   *(2026-05-04)*

3963. O estado atual do Gus inclui a migração do Mem0 SaaS para o Hub Qdrant.
   *(2026-05-03)*

3964. O último _estado-atual.md está desatualizado desde 27/04.
   *(2026-05-02)*

3965. O upload em.drive estava desatualizado devido a uma falha no refresh token do OAuth, resultando na leitura de arquivos stale.
   *(2026-05-03)*

3966. Na auditoria do Chat, foram encontrados problemas de segurança, confiabilidade e arquitetura que precisam ser resolvidos.
   *(2026-05-02)*

3967. As produções simultâneas de fragmentos acontecem através do Telegram, Claude Chat e Claude Code.
   *(2026-05-03)*

3968. A sincronização do Google Drive foi migrada do usuário OAuth (com expiração em 7 dias para apps de teste do Google) para a Federação de Identidade de Trabalho com Conta de Serviço.
   *(2026-05-03)*

3969. O Hub Qdrant coletor dual rola até 12/05.
   *(2026-05-02)*

3970. O curador chat bidirecional opera utilizando Sonnet 4.6 + GPT-4o.
   *(2026-05-03)*

3971. Estratégia de execução proposta para a fase 1: Opção 1 com 9 commits em 1 PR.
   *(2026-05-03)*

3972. A migração do Mem0 SaaS para o Hub Qdrant está em curso, com previsão para ser finalizada em 12/05/2026.
   *(2026-05-03)*

3973. O Brain Gus atualmente tem informações repetitivas que não adicionam valor.
   *(2026-05-03)*

3974. Se um PR precisa ser lido para entender o presente, é sinal de documentação desatualizada.
   *(2026-05-03)*

3975. Ao setar `MCP_URL_SECRET`, fica disponível escrita real-time do Chat (função `ingestar_fragmento`).
   *(2026-05-03)*

3976. Gustavo Pratti de Barros é um anestesiologista que tem hipertireoidismo.
   *(2026-05-04)*

3977. O log do MCP Server deve mostrar o valor do secret como <URL_SECRET (64 chars)> após o redeploy.
   *(2026-05-03)*

3978. O bot suporta funções multimídia, permitindo o processamento de áudio, vídeo e documentos em diversos formatos, como PDF e DOCX.
   *(2026-05-03)*

3979. Aguardar redeploy do Railway após a mudança do segredo.
   *(2026-05-03)*

3980. O projeto está em estado intermediário arriscado: Hub Qdrant é a fonte nova, mas a coleção legada `gus` tem ~204 fragmentos não-migrados.
   *(2026-05-03)*

3981. A aba nova só precisa olhar PRs se houver uma menção a um quebrando algo específico.
   *(2026-05-03)*

3982. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3983. URL secret protege o acesso ao MCP.
   *(2026-05-03)*

3984. O sistema Gus está continuamente sendo aprimorado através de feedback e atualizações nas suas ferramentas de trabalho.
   *(2026-05-03)*

3985. A auditoria diária é cega para o brain gus.
   *(2026-05-03)*

3986. A limpeza da memória envolve a identificação e exclusão de candidatos a deletes, com registro das operações.
   *(2026-05-03)*

3987. A porta Claude Chat é utilizada para interações com o chatbot na web.
   *(2026-05-03)*

3988. Gustavo Pratti de Barros é anestesiologista no Dimagem (Rio de Janeiro, 3 unidades) e pesquisador independente em IA.
   *(2026-05-04)*

3989. O bot do Telegram, TioGu, possui aproximadamente 21 ferramentas distintas integradas.
   *(2026-05-03)*

3990. Os riscos operacionais do bot incluem a possibilidade de dados sensíveis vazarem devido à ausência de um PII scan efetivo na resposta do bot.
   *(2026-05-02)*

3991. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

3992. O Hub Qdrant é a memória central do sistema.
   *(2026-05-03)*

3993. A direção do desenvolvimento do TioGu é seguir com a implementação de um alerta de custo proativo e a criação de um cache para diagnósticos.
   *(2026-05-03)*

3994. A convenção de nomenclatura dos arquivos JSON deve ser registrada.
   *(2026-05-02)*

3995. A estrutura de tiers proposta inclui um arquivo de bootstrap mínimo e arquivos adicionais que serão carregados on-demand.
   *(2026-05-04)*

3996. O estado final dos PRs já está no código e nos documentos gus-XX atualizados.
   *(2026-05-02)*

3997. O arquivo `gus-identity.md` é redundante e deve ser combinado com o `gus-bootstrap.md` para evitar duplicação de informações.
   *(2026-05-03)*

3998. Chat lê arquivos em `Gus-Sync/dialogos/inbox-claude-chat/` e busca especificamente arquivos com frontmatter válido para processamento.
   *(2026-05-04)*

3999. O arquivo 'gus-estado-atual.md' é gerado a cada 15 minutos e fornece um snapshot do estado do sistema.
   *(2026-05-04)*

4000. O Gus não tem acesso à internet.
   *(2026-05-03)*

4001. Na branch `claude/initial-setup-iWTfL`, há 6 demandas pendentes em `dialogos/inbox-claude-code/` (algumas com nome quebrado — "Documento sem título.md" provavelmente é lixo de sync).
   *(2026-05-03)*

4002. O Hub Qdrant é a fonte única de memória relacional do Gustavo, aposenta o Mem0 e corrige a informação no `gus-identity.md`.
   *(2026-05-04)*

4003. O Gus captura informações por meio de um pipeline híbrido utilizando Haiku e GPT-4.
   *(2026-05-04)*

4004. A coleta dual de modelos no curador termina em 12/05/2026.
   *(2026-05-03)*

4005. O Hub Qdrant é a memória central do sistema, onde arquivos .md do GitHub estão espelhados no Drive.
   *(2026-05-03)*

4006. A migração do sistema de Mem0 SaaS para Hub Qdrant é a ADR-001 e está em andamento.
   *(2026-05-03)*

4007. A coleção legada 'gus' tem aproximadamente 204 fragmentos não migrados, e o código de leitura ainda faz fallback para ela.
   *(2026-05-03)*

4008. Todo fragmento criado antes da migração e depois da Fase 3 vai existir só na coleção antiga, fora do Hub novo.
   *(2026-05-03)*

4009. Os 4 documentos essenciais para o projeto são: dialogos/_bootstrap/gus-bootstrap.md, dialogos/_bootstrap/gus-identity.md, dialogos/_bootstrap/gus-estado-atual.md, projetos/gus/_estado-atual.md.
   *(2026-05-03)*

4010. A demanda #3 na `inbox-claude-code` é uma guarda-chuva que referencia as demandas #1 e #2.
   *(2026-05-03)*

4011. O estado final dos PRs já está no código + nos docs gus-XX atualizados.
   *(2026-05-03)*

4012. O núcleo obrigatório para qualquer novo projeto deve incluir: manual operacional, identidade do Gus, estado atual, e o estado atual dos projetos.
   *(2026-05-02)*

4013. O NeuroGus está bloqueado por decisões UX pendentes entre 11.1 e 11.5.
   *(2026-05-03)*

4014. A coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026, momento em que Gustavo escolherá o modelo definitivo.
   *(2026-05-03)*

4015. A estrutura do bootstrap deve incluir uma seção de resumo no topo.
   *(2026-05-04)*

4016. Decidi que o arquivo `gus-tipos-fragmento.md` pode ser mantido como lazy-load, a ser carregado somente quando o Chat precisar de mais informações sobre classificação.
   *(2026-05-04)*

4017. O script para verificar as memórias no Mem0 está disponível no caminho `.github/scripts/export_mem0.py`.
   *(2026-05-03)*

4018. A persistência do estado é feita com gravação atômica, evitando perda de dados durante redeploys.
   *(2026-05-02)*

4019. Foi identificado que o '_estado-atual.md' e o 'gus-26-status-consolidado.md' estão desatualizados em relação a PRs recentes.
   *(2026-05-02)*

4020. O Hub é a fonte de verdade do sistema e todas as implementações subsequentes dependerão desse modelo.
   *(2026-05-03)*

4021. A aposentadoria do Mem0 SaaS está planejada após 12/05/2026, quando termina a coleta dual A/B (Anthropic Haiku × OpenAI GPT-4o-mini) do curador.
   *(2026-05-03)*

4022. O bootstrap atual menciona buscar_hub mas não destaca que, para brain 'gus', precisa passar user_id='gus' explicitamente.
   *(2026-05-04)*

4023. Agora é possível enviar demandas pelo celular para o Drive sem precisar digitar YAML.
   *(2026-05-03)*

4024. O URL secret protege e destrava a escrita real-time do Chat.
   *(2026-05-03)*

4025. A fase 1 de saneamento do projeto TioGu foi concluída, resultando em 163 testes verdes.
   *(2026-05-03)*

4026. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa e precisa de decisão sobre a migração da OAuth.
   *(2026-05-04)*

4027. Esses 4 arquivos dão 80% do contexto para qualquer aba nova.
   *(2026-05-03)*

4028. Os 4 documentos que oferecem 80% do contexto para qualquer nova aba são: dialogos/_bootstrap/gus-bootstrap.md (manual operacional do Gus, regras de comportamento, como cada porta usa o Hub), dialogos/_bootstrap/gus-identity.md (quem é o Gustavo + quem é o Gus enquanto entidade), dialogos/_bootstrap/gus-estado-atual.md (handoff auto-gerado pelo cron 03h, snapshot do Hub) e projetos/gus/_estado-atual.md (onde paramos na sessão anterior).
   *(2026-05-03)*

4029. O caminho proposto inclui Fase 1 quick wins, limpeza do Hub e reclassificação dos 204 fragmentos com um novo prompt após melhorias.
   *(2026-05-03)*

4030. O Gustavo Pratti de Barros é anestesiologista no Rio de Janeiro, atuando no Dimagem (clínica de imagem diagnóstica com 3 unidades: Nova Iguaçu, Taquara, São Gonçalo).
   *(2026-05-03)*

4031. O sistema 'Gus' está em produção e é um agente pessoal multi-porta que opera sobre Qdrant Hub.
   *(2026-05-04)*

4032. O Hub Qdrant é a fonte única de armazenamento de fragmentos de memória.
   *(2026-05-03)*

4033. A atualização do arquivo `gus-bootstrap.md` é necessária para consolidar informações e remover redundâncias.
   *(2026-05-04)*

4034. A stack de memória está em estado intermediário arriscado: o Hub Qdrant é a fonte nova, mas a coleção legada tem fragmentos não migrados.
   *(2026-05-03)*

4035. A proposta de otimização é a opção B, que reduz o tamanho do bootstrap e melhora a eficiência, mantendo informações acessíveis quando necessário.
   *(2026-05-04)*

4036. Os três principais caminhos de entrada de dados para o sistema são via Telegram, Claude Chat, e Claude Code.
   *(2026-05-03)*

4037. O custo do fallback para OpenAI Vision é menor que o custo normal do Anthropic.
   *(2026-05-03)*

4038. O sistema de agentes que Gustavo gerencia inclui interações pelo Telegram, Code, Chat e uma futura integração com a Alexa, representando um esforço coordenado para maximizar a funcionalidade do agente Gus.
   *(2026-05-04)*

4039. A análise do sistema identificou que o Hub Qdrant é a nova fonte da verdade, substituindo a antiga Mem0 SaaS na coleta de dados.
   *(2026-05-03)*

4040. A aba nova só precisa olhar PRs se forem reportados bugs específicos.
   *(2026-05-03)*

4041. O Hub Qdrant é a fonte da verdade.
   *(2026-05-03)*

4042. As frentes mais ativas nos últimos 5 dias incluem novos commits em vários PRs, como o #67 (curador chat bidirecional + GPT-4o), PR #64 (captura transcripts Code via cron) e PR #60 (MCP URL secret).
   *(2026-05-03)*

4043. O fragmento salvo no brain 'gus' tem `via=claude-chat`, confirmando captura efetiva.
   *(2026-05-03)*

4044. Os 204 fragmentos históricos estavam no Mem0 SaaS, não no Qdrant Cloud como achávamos.
   *(2026-05-03)*

4045. Há uma programação de sessões para o projeto, com um total de 30 horas em 8-9 sessões ao longo de duas semanas.
   *(2026-05-02)*

4046. A captura real-time do Chat é uma opção A e depende da decisão de Gustavo sobre o caminho a seguir.
   *(2026-05-03)*

4047. Decisões arquiteturais não devem estar nos pull requests, mas nos documentos adequados.
   *(2026-05-03)*

4048. O sistema Gus deve minimizar os passos manuais e maximizar a chance de sucesso nas implementações.
   *(2026-05-04)*

4049. O sistema Gus é um agente pessoal multi-porta em produção, rodando em um backbone Hub Qdrant.
   *(2026-05-04)*

4050. A migração de Mem0 SaaS para Hub Qdrant está em curso e deve ser concluída até 12/05/2026.
   *(2026-05-03)*

4051. A atualização traz novos testes que aumentam a cobertura do código em 21 testes.
   *(2026-05-03)*

4052. A arquitetura do bot é projetada para um único usuário, sem suporte a multi-tenancy.
   *(2026-05-02)*

4053. A captura multiporta é uma das 3 demandas reais listadas no inbox-claude-code.
   *(2026-05-03)*

4054. O Gus é um sistema de agente pessoal multi-porta, onde a memória central está no Hub Qdrant.
   *(2026-05-03)*

4055. Os projetos ativos incluem: Phronesis-Bench, NeuroGus, MGE/MGX, TER, e Axon.
   *(2026-05-03)*

4056. Gus é um sistema de agente pessoal multi-porta que integra várias plataformas como Telegram, Claude Code e Claude Chat, com memória central no Hub Qdrant.
   *(2026-05-03)*

4057. A auditoria diária para o Hub Qdrant é cega para o brain Gus, classificando fragmentos por keywords.
   *(2026-05-03)*

4058. Gustavo viaja com a esposa pelo Vale do Paraíba.
   *(2026-05-03)*

4059. O `_estado-atual.md` está desatualizado em relação ao que ocorreu no GitHub desde 27/04.
   *(2026-05-04)*

4060. Os JSONs estruturados na pasta designada devem ser registrados.
   *(2026-05-02)*

4061. O Hub Qdrant é a fonte da verdade para o sistema de agente pessoal multi-porta.
   *(2026-05-03)*

4062. A fase 4 do projeto focus na refatoração estrutural do bot, dividindo o código em múltiplos módulos para melhorar a manutenção e facilitar testes.
   *(2026-05-03)*

4063. As 18 entradas 'fallback-mem0' de 28/04 foram pro Mem0 SaaS porque a migração ainda não estava 100% deploy-ada naquele dia.
   *(2026-05-03)*

4064. O estado final dos PRs já tá no código + nos docs gus-XX atualizados.
   *(2026-05-03)*

4065. O Gustavo é anestesiologista e não programa — toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

4066. Última vez que houve commit foi dia 01/05 às 14:38Z, sync GitHub→Drive.
   *(2026-05-03)*

4067. A coleta dual de modelos no curador irá terminar em 12/05/2026.
   *(2026-05-03)*

4068. Os documentos obrigatórios para entender o projeto incluem: `dialogos/_bootstrap/gus-bootstrap.md`, `dialogos/_bootstrap/gus-identity.md`, `dialogos/_bootstrap/gus-estado-atual.md` e `projetos/gus/_estado-atual.md`.
   *(2026-05-04)*

4069. O Gustavo é anestesiologista e não programa, delegando toda implementação para o Gus e o Tiogu.
   *(2026-05-03)*

4070. Os 4 arquivos fundamentais do Gus dão 80% do contexto para qualquer aba nova.
   *(2026-05-03)*

4071. O status de projetos e informações funcionais devem ser consolidados na memória do Claude para evitar inconsistências.
   *(2026-05-03)*

4072. O Bootstrap deve conter uma seção de TL;DR que resume as capacidades e limites do Chat.
   *(2026-05-03)*

4073. O passo 4, relacionado ao Drive sync, foi resolvido pela implementação do WIF no PR #76.
   *(2026-05-03)*

4074. O workflow `migrar_gus_para_hub.py` foi executado em dry-run e não encontrou fragmentos na coleção 'gus'.
   *(2026-05-03)*

4075. A aba nova só precisa olhar PRs se houver quebra de algo depois do PR.
   *(2026-05-03)*

4076. O último update do projeto Gus foi realizado em 02/05/2026, montando um panorama geral da situação atual.
   *(2026-05-02)*

4077. Há 3 produções simultâneas de fragmentos com 4 vezes o custo de chamadas LLM por unidade de input.
   *(2026-05-03)*

4078. A stack de memória está em estado intermediário arriscado com 4 caminhos de escrita coexistindo.
   *(2026-05-03)*

4079. Atualmente, o bot não possui um alerta que avisaria quando o limite de cota no uso de serviços é atingido, o que pode levar à perda de funcionalidade.
   *(2026-05-02)*

4080. Os principais status de Gustavo incluem: o sistema Gus está em produção, com o Hub Qdrant como a única fonte de dados. Os projetos em andamento incluem NeuroGus e publicação do Phronesis-Bench.
   *(2026-05-04)*

4081. O estado final dos PRs já está no código e nos documentos atualizados, portanto é recomendável não revisar PRs, a menos que seja para entender o presente ou investigar bugs específicos.
   *(2026-05-04)*

4082. A migração da Mem0 SaaS para o Hub Qdrant está em curso.
   *(2026-05-03)*

4083. A estratégia de limpeza ativa do Hub deve gerar um relatório com a listagem de candidatos a delete, que será revisado antes de qualquer exclusão.
   *(2026-05-03)*

4084. A decisão foi de manter os fragmentos do Mem0 apenas no 'historico/' e planejar uma filtragem e tradução na fase 5.
   *(2026-05-03)*

4085. Quatro demandas pendentes foram identificadas no `dialogos/inbox-claude-code/`: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao.
   *(2026-05-02)*

4086. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

4087. O estado atual da migração é de aposentadoria do Mem0 SaaS e a confirmação do Hub Qdrant como fonte da verdade.
   *(2026-05-03)*

4088. A migração do sistema ADR-001 está em curso: o Hub Qdrant está sendo implantado como a fonte da verdade com a coleta dual de modelos.
   *(2026-05-03)*

4089. Gus é um sistema de agente pessoal multi-porta. Sua memória central está no Hub Qdrant.
   *(2026-05-03)*

4090. Se o secret `MEM0_API_KEY` ainda existe no GitHub Secrets / Railway, vale rodar 1 script pra checar quanto conteúdo tem no Mem0 SaaS antigo.
   *(2026-05-03)*

4091. O sistema Gus é um agente pessoal multi-porta que opera em diferentes plataformas como Telegram e Claude Chat, com a memória central armazenada no Hub Qdrant.
   *(2026-05-03)*

4092. O Hub é mais fresco que gus-estado-atual.md, que é um snapshot das 03h.
   *(2026-05-03)*

4093. Gustavo viaja com a esposa para natureza e aventura, principalmente no Vale do Paraíba.
   *(2026-05-03)*

4094. O projeto conta com um sistema multi-porta conectado ao Hub Qdrant.
   *(2026-05-02)*

4095. As opções para o que fazer com os 204 fragmentos incluem mantê-los em `historico/` ou importá-los para o Hub.
   *(2026-05-03)*

4096. O arquivo `_estado-atual.md` está bem desatualizado — git log mostra muita coisa depois (PRs #57, #60, #63, #64, #67, captura multiporta).
   *(2026-05-03)*

4097. O cron do curator e o sistema de ingestão de memórias ainda fazem fallback para a coleção legada de memórias (Mem0) no caso do Hub não retornar resultados.
   *(2026-05-03)*

4098. A stack de memória possui 4 chamadas LLM por unidade de input, aumentando o custo e o risco de polluição.
   *(2026-05-03)*

4099. O agente possui múltiplos projetos ativos, como Phronesis-Bench, NeuroGus, MGE, MGX, TER e Axon.
   *(2026-05-04)*

4100. A captura de memória ocorre em três canais: Telegram, Claude Chat, e Claude Code.
   *(2026-05-03)*

4101. O status de todas as fases do projeto é documentado regularmente.
   *(2026-05-03)*

4102. O bot agora separa a lógica de manuseio de mensagens em diferentes módulos, facilitando manutenção e implementação de novas funcionalidades.
   *(2026-05-04)*

4103. Sessão 3A da Fase 2 inclui a atualização da documentação `_estado-atual.md` e `gus-26-status-consolidado.md`.
   *(2026-05-02)*

4104. A auditoria do Hub deve incluir o uso do campo `area` do payload para uma análise mais precisa.
   *(2026-05-03)*

4105. O estado de migração ADR-001 está em curso e a coleta dual de modelos no curador termina em 12/05/2026.
   *(2026-05-03)*

4106. O Gus é um sistema de agente pessoal multi-porta com memória central no Hub Qdrant, arquivos .md no GitHub, espelhados no Drive.
   *(2026-05-03)*

4107. Realizar a rotaçã do segredo do MCP é essencial após as implementações de segurança.
   *(2026-05-03)*

4108. Os resultados do último projeto indicam que o estado atual do hub está fresco, com um snapshot gerado às 03h.
   *(2026-05-03)*

4109. A demanda 'Captura multiporta curador' depende de aprovação de Gustavo.
   *(2026-05-03)*

4110. A coleta dual de modelos no curador (Haiku × GPT-4o-mini, mudou de Sonnet em 29/04 por custo/resiliência) termina em 12/05/2026.
   *(2026-05-03)*

4111. O protocolo de ativação do Gus é acionado quando a mensagem de abertura menciona 'Gus' de qualquer forma.
   *(2026-05-04)*

4112. A auditoria diária é cega para o brain gus e classifica por keywords ignorando o area que o curador já preencheu.
   *(2026-05-03)*

4113. Existem 6 demandas listadas no inbox-claude-code, mas apenas 3 são reais.
   *(2026-05-03)*

4114. As ferramentas do sistema devem ser documentadas em um arquivo auto-gerado chamado _tools-inventario.md.
   *(2026-05-02)*

4115. Estou aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

4116. O sistema de agente pessoal multi-porta tem memória central no Hub Qdrant, espelhada no GitHub e Drive.
   *(2026-05-03)*

4117. Gustavo é falante nativo de português, com fortes interesses intelectuais em segurança em IA, filosofia e systems thinking.
   *(2026-05-04)*

4118. O bootstrap atual não possui um entry point claro ou ordem de leitura.
   *(2026-05-03)*

4119. A imagem apresenta uma lista ranqueada de marcas de farinha de trigo, acompanhada de um texto que explica o teste realizado.
   *(2026-05-03)*

4120. A migração ADR-001 está em curso, aposentar Mem0 SaaS é um objetivo.
   *(2026-05-03)*

4121. Os dados do Hub Gus são críticos para a operação existente e devem ser mantidos e purificados.
   *(2026-05-03)*

4122. A documentação do projeto inclui um arquivo chamado _estado-atual.md, que é atualizado periodicamente para refletir o estado atual das implementações e decisões tomadas.
   *(2026-05-02)*

4123. A captura multiporta no Claude Chat precisa de um gatilho proativo que não está implementado.
   *(2026-05-02)*

4124. O estado atual dos projetos deve ser consultado frequentemente através do Hub.
   *(2026-05-04)*

4125. Nos últimos cinco dias, o PR #67 introduziu o curador chat bidirecional com Sonnet 4.6, que salva fragmento no brain gustavo e gus.
   *(2026-05-04)*

4126. O retro-engine registra as sessões encerradas, mas a função acaba falhando quando a chave ANTHROPIC_API_KEY não está disponível no ambiente.
   *(2026-05-02)*

4127. O bot possui 21 ferramentas implementadas, distribuídas entre suas funcionalidades.
   *(2026-05-02)*

4128. Há 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

4129. Os 4 documentos obrigatórios que dão 80% do contexto para qualquer aba nova são: `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md` e `estado-atual.md`.
   *(2026-05-03)*

4130. Senhas, segredos ou informações sensíveis não devem ser logadas.
   *(2026-05-03)*

4131. A arquitetura do bot Telegram é baseada em um sistema multi-porta com Hub Qdrant como memória central.
   *(2026-05-02)*

4132. O Hub Qdrant é a memória central do sistema que coleta informações de diversas fontes.
   *(2026-05-03)*

4133. Gustavo deve buscar informações nos arquivos de projeto quando necessário, usando referências no Hub ou consultas diretas a dados relevantes.
   *(2026-05-03)*

4134. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

4135. Gustavo é anestesiologista e não programa; toda implementação passa pelo Gus ou pelo assistente TioGu.
   *(2026-05-03)*

4136. Foram propostos pontos para a fase 1 da revisão do bot.
   *(2026-05-02)*

4137. O sistema Gus é um agente pessoal multi-porta conectando várias plataformas.
   *(2026-05-03)*

4138. O secret `MEM0_API_KEY` não existe mais nas deps dos scripts.
   *(2026-05-03)*

4139. A migração do sistema Mem0 SaaS para o Hub Qdrant está em curso.
   *(2026-05-03)*

4140. As regras operacionais do sistema Gus incluem: estilos de comunicação, diretrizes de implementação, caminhos de captura e protocolos chave.
   *(2026-05-04)*

4141. O sistema Gus é um agente pessoal multi-porta que integra várias plataformas como Telegram, Code, Chat e Custom GPT.
   *(2026-05-04)*

4142. O estado final dos pull requests já está no código + nos documentos gus-XX atualizados.
   *(2026-05-03)*

4143. O passo 2 é recriar o Connector claude.ai, pois a URL do MCP muda após a configuração da 'MCP_URL_SECRET'.
   *(2026-05-03)*

4144. O bot Telegram descarta silenciosamente mensagens enviadas durante o downtime após cada redeploy Railway, sem aviso para o Gustavo.
   *(2026-05-02)*

4145. O backlog de demandas e tarefas está dividido em várias frentes, com foco na saída para o Hub Qdrant.
   *(2026-05-03)*

4146. O agente pessoal é um sistema multi-porta, incluindo Telegram, Claude Code e Claude Chat.
   *(2026-05-03)*

4147. O segredo do MCP deve ser regenerado assim que identificado que ele está exposto em logs.
   *(2026-05-03)*

4148. A auditoria do Chat será feita em todas as superfícies do sistema, abrangendo código-fonte, workflows, docs estratégicos e estado operacional.
   *(2026-05-03)*

4149. Gus é um sistema de agente pessoal multi-porta que utiliza um Hub Qdrant como memória central.
   *(2026-05-03)*

4150. O sistema de agente pessoal multi-porta integra Telegram, TioGu, Claude Code e Claude Chat.
   *(2026-05-03)*

4151. Uma auditoria revelou que o Hub está retornando resultados inconsistentes devido a fallbacks para a coleção legada, introduzindo poluição no sistema.
   *(2026-05-03)*

4152. O Hub Qdrant é a fonte da verdade para o sistema de agente pessoal.
   *(2026-05-03)*

4153. A qualidade do glúten e as propriedades da farinha de trigo são fundamentais em uma ampla variedade de preparações culinárias.
   *(2026-05-03)*

4154. O arquivo gus-estado-atual.md está desatualizado desde 27/04.
   *(2026-05-03)*

4155. Houve 12 fixes de 31 achados na auditoria do Claude Chat, com bug crítico do curador corrigido.
   *(2026-05-03)*

4156. O curador foge do esquema `gus-18` por falta de implementação para o ciclo de vida dos fragmentos, resultando em fragmentos como 'ativo' para sempre.
   *(2026-05-03)*

4157. Há 204 fragmentos não-migrados da coleção legada `gus` no Hub Qdrant.
   *(2026-05-03)*

4158. A captura Claude Code via cron (PR #64) permite que um hook Stop salve a transcript redatada, com cron a cada 30 minutos para processamento.
   *(2026-05-02)*

4159. O projeto 'Axon' é focado em governança contextual entre estados humanos e ações digitais.
   *(2026-05-03)*

4160. Os 4 arquivos principais que dão 80% do contexto são: `gus-bootstrap.md`, `gus-identity.md`, `gus-estado-atual.md`, `estado-atual.md`.
   *(2026-05-03)*

4161. O segredo gera segurança ao restringir o acesso ao MCP.
   *(2026-05-03)*

4162. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

4163. Mem0 SaaS aposentado desde 27/04/2026 (ADR-001 Fase 5). Hub Qdrant é fonte única.
   *(2026-05-04)*

4164. Atualmente, estão em curso duas fases do projeto: saneamento do TioGu e auditoria do Claude Chat.
   *(2026-05-03)*

4165. A migração para o Hub Qdrant está em processo com a decisão ADR-001 de aposentar o Mem0 SaaS, tornando o Hub a fonte definitiva.
   *(2026-05-03)*

4166. Em volume crescente, brain `gus` vira cópia ruidosa do brain `gustavo`.
   *(2026-05-03)*

4167. Gustavo tem hipertireoidismo e está em tratamento.
   *(2026-05-03)*

4168. O `_estado-atual.md` (27/04) está bem desatualizado em relação ao git log que mostra muita coisa depois.
   *(2026-05-02)*

4169. A coleta dual de modelos no curador (Haiku × GPT-4o-mini, mudou de Sonnet em 29/04 por custo/resiliência) termina em 12/05/2026, depois Gustavo escolhe modelo definitivo.
   *(2026-05-03)*

4170. Os arquivos de boot devem ser reordenados para incluir um TL;DR no topo, seguido de quem é Gustavo, de suas capacidades e limites, diretrizes universais e regras, e por último caminhos de captura.
   *(2026-05-03)*

4171. O documento `gus-estado-atual.md` está desatualizado, datado de 27/04.
   *(2026-05-02)*

4172. A coleta dual de modelos no curador (Haiku e GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

4173. O canal `dialogos/` é bidirecional, cron 15min Drive→GitHub, validado.
   *(2026-05-03)*

4174. A linha `ingest_chat_raw.py` documenta que não há checagem de `hash_janela` antes de ingestar.
   *(2026-05-03)*

4175. Drive sync parado — 3 opções: reset OAuth (paliativo), Service Account (definitivo), ou aposentar Drive sync (radical).
   *(2026-05-03)*

4176. O chat salvou um fragmento no brain 'gus'.
   *(2026-05-04)*

4177. A renomeação das pastas e arquivos relacionados ao Mem0 para Hub vai acontecer, preservando a história do git.
   *(2026-05-03)*

4178. O bot TioGu possui mecanismos de fallback que garantem resiliência nos comandos, alternando entre diferentes LLMs sempre que necessário.
   *(2026-05-03)*

4179. A prioridade default para as demandas pode ser media.
   *(2026-05-03)*

4180. O Gustavo está na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

4181. Os projetos ativos de Gustavo incluem Phronesis, MGE, TER e Axon.
   *(2026-05-03)*

4182. O sistema implementa um prompt caching eficiente, que reduz o custo de input dos LLMs em até 70%.
   *(2026-05-04)*

4183. Os 204 fragmentos do Mem0 SaaS devem ser reclassificados e possivelmente traduzidos na fase 5.
   *(2026-05-03)*

4184. O sistema de agente pessoal Gus opera em múltiplas portas (Telegram/TioGu, Claude Code, Claude Chat, futuras: Custom GPT mobile, Alexa).
   *(2026-05-03)*

4185. O backbone de memória do Gus migrou para Qdrant Hub direto onde existem mais de 1076 fragmentos, divididos em duas mentes: 'gustavo' e 'gus'.
   *(2026-05-04)*

4186. Todos os fragmentos criados antes da migração e depois da Fase 3 vão existir só na coleção antiga.
   *(2026-05-03)*

4187. Atualmente, o sistema Gus opera como agente pessoal multi-porta (Telegram, Claude Code, Claude Chat com MCP Connector, Custom GPT, Alexa planejada) sobre o Qdrant Hub.
   *(2026-05-04)*

4188. A implementação do lifecycle para o schema gus-18 está declarada, mas não implementada.
   *(2026-05-03)*

4189. O sistema 'Gus' é um agente pessoal multi-porta que opera sobre o Qdrant Hub.
   *(2026-05-04)*

4190. O trabalho do curador acontece em paralelo com a coleta dual, resultando em um alto risco de poluição cruzada entre os brains.
   *(2026-05-03)*

4191. A estrutura ideal proposta inclui o arquivo `gus-bootstrap.md` como o único arquivo sempre carregado, com o conteúdo mínimo necessário.
   *(2026-05-04)*

4192. O Hub é mais fresco que gus-estado-atual.md (snapshot das 03h). Sempre que possível, prefira tools MCP a arquivo .md.
   *(2026-05-03)*

4193. A stack de memória está em estado intermediário arriscado, com o Hub Qdrant como nova fonte e a coleção legada `gus` ainda ativa.
   *(2026-05-03)*

4194. A estrutura atual do userMemories da Anthropic inclui campos como contexto de trabalho, contexto pessoal, 'top of mind', histórico breve com várias seções e instruções outras.
   *(2026-05-04)*

4195. O PR #76 migrou pra WIF e você já configurou os secrets.
   *(2026-05-03)*

4196. A auditoria diária (`auditoria_hub.py`) é cega para o brain `gus` e classifica por keywords ignorando o `area` que o curador já preencheu.
   *(2026-05-03)*

4197. A migração de 204 fragmentos da coleção Mem0 SaaS para o Hub Qdrant é uma prioridade.
   *(2026-05-03)*

4198. A URL do MCP é pública e deve ser protegida para evitar acesso não autorizado ao Hub.
   *(2026-05-03)*

4199. O arquivo gus-identity.md é redundante com o gus-bootstrap.md e está desatualizado.
   *(2026-05-03)*

4200. A receita de uma aba nova requer leitura dos documentos principais e a utilização de ferramentas preferenciais.
   *(2026-05-03)*

4201. A coletânea de modelos no curador utiliza Haiku e GPT-4o-mini, mudando de Sonnet em 29/04 por custo e resiliência.
   *(2026-05-03)*

4202. O log do retro-engine desta sessão não conseguiu extrair fragmentos devido à falta de `ANTHROPIC_API_KEY`.
   *(2026-05-02)*

4203. O segredo vazou em vários logs e transcripts, resultando na necessidade de rotação.
   *(2026-05-03)*

4204. Gustavo é anestesiologista e não programa. Toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

4205. O TioGu possui uma implementação de fallback cross-vendor para os LLMs, aumentando a resiliência do sistema.
   *(2026-05-02)*

4206. Os 4 documentos fundamentais para qualquer aba nova são: gus-bootstrap.md, gus-identity.md, gus-estado-atual.md e projetos/gus/_estado-atual.md.
   *(2026-05-03)*

4207. Gustavo viaja com a esposa para natureza e aventura, especialmente no Vale do Paraíba.
   *(2026-05-03)*

4208. A versão do SDK Anthropic utilizada é a 0.40.0, que está atrasada em aproximadamente 6 meses.
   *(2026-05-04)*

4209. O estado final dos PRs já está no código e nos documentos gus-XX atualizados.
   *(2026-05-03)*

4210. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

4211. O arquivo gus-identity.md foi deletado após a refatoração.
   *(2026-05-04)*

4212. O hub Qdrant é a fonte de verdade do sistema Gus.
   *(2026-05-03)*

4213. O Hub Qdrant é a memória central do sistema, coletando dados de múltiplas portas.
   *(2026-05-04)*

4214. A coleção legada `gus` está vazia, e não existem 204 fragmentos para serem migrados.
   *(2026-05-03)*

4215. As regras operacionais contidas no 'Other instructions' devem ser atualizadas para refletir a nova configuração do sistema Gus.
   *(2026-05-04)*

4216. O sistema de agente pessoal multi-porta é suportado por uma memória central no Hub Qdrant e arquivos .md no GitHub.
   *(2026-05-03)*

4217. Gus é um sistema de agente pessoal multi-porta, com memória central no Hub Qdrant e arquivos .md no GitHub.
   *(2026-05-03)*

4218. 1. Gustavo trabalha com gestão de pacientes organizados por planos de saúde (Assim Taquara vs. outros planos: Intermédica + Leve Saúde)
2. Preferência por separar dados de pacientes em arquivos markdown (.md) segregados por data e tipo de plano
3. Gustavo está testando processamento de PDFs com o Gus — já fez um teste e agora vai testar outro
   *(2026-04-27)*

4219. O Hub Qdrant é a fonte da verdade e armazena a memória central do Gus.
   *(2026-05-03)*

4220. As mudanças sugeridas para o gus-identity.md visam melhorar a manutenção e reduzir a redundância.
   *(2026-05-03)*

4221. O sistema está em estado intermediário arriscado, com risco de perda silenciosa e poluição cruzada entre os cérebros.
   *(2026-05-03)*

4222. O projeto `claude-code` contém uma estrutura de demandas organizadas em `dialogos/inbox-claude-code/`.
   *(2026-05-02)*

4223. Gustavo Pratti de Barros é anestesiologista no Dimagem, localizado no Rio de Janeiro, onde opera em 3 unidades.
   *(2026-05-03)*

4224. O bot é projetado para ter um modelo de falha que tenta um provedores de LLM alternativos em caso de falha no modelo principal.
   *(2026-05-04)*

4225. O sistema de agente pessoal multi-porta inclui Telegram, Claude Code, Claude Chat e futuras integrações como Custom GPT mobile e Alexa.
   *(2026-05-03)*

4226. O Hub Qdrant é a fonte da verdade. Coleta dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

4227. O arquivo gus-identity.md contém redundância com o gus-bootstrap.md, já que muitas informações se sobrepõem.
   *(2026-05-04)*

4228. Os testes no TioGu alcançaram 163 testes verdes e a Fase 1 de saneamento foi concluída.
   *(2026-05-03)*

4229. Tô aqui na porta Code, branch `claude/initial-setup-iWTfL`.
   *(2026-05-03)*

4230. O ciclo de vida dos fragmentos no schema gus-18 não está sendo executado como prometido, o que gera uma dívida técnica silenciosa.
   *(2026-05-03)*

4231. O bot TioGu opera com um sistema de multi-porta, integrando diferentes plataformas como Telegram e Claude com um Hub Qdrant como memória central.
   *(2026-05-03)*

4232. Foi recomendado que o sistema use uma Service Account para Drive sync ao invés de OAuth.
   *(2026-05-03)*

4233. O hub Qdrant é a nova arquitetura que armazena a memória central do Gus.
   *(2026-05-03)*

4234. O prompt `system_prompt.md` merece revisão constante para eliminar drift e atualizar informações dos tools.
   *(2026-05-03)*

4235. É necessário não remover a variável MCP_AUTH_DISABLED que deve ser mantida como true.
   *(2026-05-03)*

4236. O status do projeto TioGu é que a fase de saneamento está concluída com 163 testes verdes.
   *(2026-05-03)*

4237. O status do fragmento é 'ativo' e não altera ao longo do tempo.
   *(2026-05-03)*

4238. Foi recomendado que o curador mudasse sua implementação para utilizar ingestão em tempo real.
   *(2026-05-02)*

4239. As memórias são processadas em tempo real com uma dupla chamada de LLM, passando pelo Haiku e pelo GPT.
   *(2026-05-03)*

4240. NeuroGus (visualização 3D do Hub) está totalmente desenhado e desbloqueia quando as decisões §11.1-11.5 fecharem.
   *(2026-05-03)*

4241. O curador Gus utiliza Haiku e GPT-4o-mini em paralelo para gerar respostas.
   *(2026-05-03)*

4242. Atualmente, existem 1076+ fragmentos armazenados, sendo 551 no brain 'gustavo' e 525 no brain 'gus'.
   *(2026-05-03)*

4243. A migração do Hub Qdrant deve ser finalizada até 12/05/2026.
   *(2026-05-03)*

4244. Um total de 204 fragmentos da coleção legada ainda não foram migrados e permanecem no Mem0 SaaS.
   *(2026-05-03)*

4245. O Gustavo é anestesiologista e não programa. Toda implementação passa pelo Gus.
   *(2026-05-03)*

4246. O Cortical (TioGu) é um sistema de busca semântico integrado ao Drive.
   *(2026-05-03)*

4247. A demanda #1 cobre a questão de segurança relacionada ao MCP.
   *(2026-05-03)*

4248. Gustavo Pratti de Barros é anestesiologista no Dimagem e pesquisador independente em IA.
   *(2026-05-03)*

4249. Gustavo é falante nativo de português, baseado no Rio de Janeiro, e tem interesses em segurança em IA, filosofia e systems thinking.
   *(2026-05-03)*

4250. O TioGu utiliza o framework python-telegram-bot na versão 21.6.
   *(2026-05-02)*

4251. O curador híbrido é responsável por capturar fragmentos de diferentes fontes e armazená-los no Hub.
   *(2026-05-03)*

4252. A stack de memória está em estado intermediário arriscado, pois o Hub Qdrant é a nova fonte, mas a coleção legada ainda está ativa.
   *(2026-05-03)*

4253. Atualmente, todo o desenvolvimento e implementação passam por Gus e Tiogu.
   *(2026-05-03)*

4254. Os arquivos 'gus-01 a gus-09' são considerados desnecessários para leitura, a menos que por curiosidade histórica.
   *(2026-05-02)*

4255. A migração de memória do sistema "Gus" foi feita de Mem0 para Qdrant Hub direto (ADR-001, concluído em 27/04/2026), com 1076+ fragmentos em dois brains independentes: `gustavo` (fatos sobre o usuário) e `gus` (autorreflexão do agente).
   *(2026-05-03)*

4256. As 204 entradas da coleção legada estavam no Mem0 SaaS, e não no Qdrant Cloud self-hosted.
   *(2026-05-03)*

4257. O MCP está público — qualquer scanner que descobrir a URL Railway lê todo o Hub.
   *(2026-05-03)*

4258. O bot possui um sistema de prompt caching para otimizar as consultas.
   *(2026-05-03)*

4259. O envio de demanda assíncrona deve seguir a estrutura `Gus-Sync/dialogos/inbox-<destino>/` com frontmatter obrigatório em YAML.
   *(2026-05-03)*

4260. Gustavo é anestesiologista e não programa, toda implementação passa pelo Gus.
   *(2026-05-03)*

4261. A coleta dual de modelos no curador termina em 12/05/2026 e Gustavo escolhe o modelo definitivo.
   *(2026-05-03)*

4262. O sistema espera um comportamento de redundância e resiliência através do uso de múltiplos provedores de LLM.
   *(2026-05-02)*

4263. A demanda #3 no inbox-claude-code é uma guarda-chuva que referencia as 2 demandas anteriores, onde as sub-pendências são relacionadas à ativação do MCP_URL_SECRET e ao recadastramento do Connector claude.ai.
   *(2026-05-03)*

4264. O sistema 'Gus' é um agente pessoal multi-porta em produção, operando através de Telegram, Claude Code, Claude Chat, Custom GPT e uma Alexa planejada.
   *(2026-05-04)*

4265. Uma das demandas pendentes é a `2026-05-01-drive-sync-oauth-fix.md`.
   *(2026-05-02)*

4266. Vou abrir PR mínimo no bootstrap pra deixar a instrução explícita sobre buscar fragmentos de autoreflexão do agente.
   *(2026-05-04)*

4267. O Hub Qdrant é a fonte nova, mas a coleção legada gus (Mem0 self-hosted) tem ~204 fragmentos não-migrados e o código de leitura ainda faz fallback pra ela.
   *(2026-05-03)*

4268. Os 204 fragmentos históricos foram exportados do Mem0 SaaS e estão armazenados em 'historico/mem0-export-final-2026-05-02.json'.
   *(2026-05-03)*

4269. A auditoria do Chat reúne todos os aspectos relacionados ao projeto Claude Chat.
   *(2026-05-03)*

4270. O arquivo `gus-identity.md` apresenta drift factual, com informações erradas sobre a aposentadoria do Mem0 e o nome da pasta do Google Drive.
   *(2026-05-04)*

4271. O arquivo `gus-identity.md` pretende ser a fonte de verdade sobre quem é o Gus e o Gustavo, mas não é a única.
   *(2026-05-04)*

4272. Adoção de 4 chamadas LLM por unidade de input gera risco de cross-brain pollution caso o fallback para Mem0 continue.
   *(2026-05-03)*

4273. Gustavo Pratti de Barros é anestesiologista no Dimagem e pesquisador independente em IA que opera múltiplos projetos simultaneamente.
   *(2026-05-04)*

4274. Recentemente, o foco do projeto foi em hardening, com correções de bugs e melhorias na integração do sistema.
   *(2026-05-04)*

4275. As interações do usuário com o Chat devem seguir um estilo de resposta informal, direto e sem superlativos.
   *(2026-05-03)*

4276. Estou na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

4277. O sistema não registrou novas memórias recentemente, o que pode afetar a continuidade das atualizações.
   *(2026-05-02)*

4278. O MCP Hub não está ativado com `MCP_URL_SECRET`, tornando-o vulnerável a acessos não autorizados.
   *(2026-05-03)*

4279. O sistema deve mencionar que utiliza Claude/ChatGPT-Kai/Gemini.
   *(2026-05-04)*

4280. Arquivo `gus-bootstrap.md` contém manual operacional do Gus e regras de comportamento.
   *(2026-05-03)*

4281. 2 demandas pendentes pra essa porta: `dialogos/inbox-/`.
   *(2026-05-02)*

4282. Estou aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

4283. O bot Telegram TioGu utiliza uma arquitetura multi-porta com Hub Qdrant como memória central.
   *(2026-05-03)*

4284. O Hub Qdrant é a fonte da verdade para dados.
   *(2026-05-03)*

4285. Gustavo é anestesiologista e não programa. Toda implementação passa pelo Gus/Tiogu.
   *(2026-05-03)*

4286. O bot do Telegram, TioGu, possui 21 ferramentas distintas integradas.
   *(2026-05-02)*

4287. O commit de dry run para limpeza do Hub indica uma manutenção preventiva.
   *(2026-05-03)*

4288. O último dia de captura no Mem0 SaaS foi em 26/04.
   *(2026-05-03)*

4289. Gustavo Pratti de Barros é anestesiologista no Rio de Janeiro, atuando no Dimagem (clínica de imagem diagnóstica com 3 unidades: Nova Iguaçu, Taquara, São Gonçalo). Em paralelo ao trabalho clínico, é pesquisador independente ativo em IA e construtor de sistemas, operando múltiplos projetos de pesquisa, produto e arquitetura em paralelo.
   *(2026-05-03)*

4290. Os arquivos incluem `2026-05-01-captura-multiporta-curador.md`, `2026-05-01-drive-sync-oauth-fix.md` e `_frontmatter-referencia.md`.
   *(2026-05-02)*

4291. A recomendação é manter o conteúdo atual em 'historico/' e planejar uma importação seletiva dos 204 fragmentos no futuro.
   *(2026-05-03)*

4292. O bot Telegram (TioGu) tem ~21 tools, multimídia, prompt caching, e opera em Railway.
   *(2026-05-02)*

4293. A proposta de otimização do bootstrap inclui três opções: A para reordenar, B para dividir em arquivos lazy e C para uma versão minimalista.
   *(2026-05-04)*

4294. O Chat gera um log '/_log/resumos-mem0/' que mostra erros e entradas processadas.
   *(2026-05-03)*

4295. O bot opera com dependências como python-telegram-bot, anthropic SDK, openai, FastAPI e Qdrant.
   *(2026-05-03)*

4296. O Gustavo é anestesiologista e não programa; toda implementação passa pelo Gus.
   *(2026-05-03)*

4297. Curador tem dois processos principais: `ingest_chat_raw.py` e `curador_claude_code.py`. Ambos precisam ser auditados.
   *(2026-05-03)*

4298. A auditoria identificou a necessidade de integrar uma lógica clara para hierarquizar os canais de escrita do Chat.
   *(2026-05-03)*

4299. A stack está em estado intermediário arriscado.
   *(2026-05-03)*

4300. Há 204 fragmentos não-migrados da coleção legada `gus` no Mem0 SaaS.
   *(2026-05-03)*

4301. O ambiente precisa ter o `ANTHROPIC_API_KEY` configurado para evitar erro no log do retro-engine auto-gerado.
   *(2026-05-03)*

4302. O 'fallback-bruto' será removido, evitando poluição no Hub com conteúdos não classificados.
   *(2026-05-03)*

4303. As campos do userMemories da Anthropic devem ser preenchidos com diretrizes específicas que abordam cada aspecto do sistema de forma clara e concisa.
   *(2026-05-03)*

4304. Sistema de agente pessoal multimodal é composto por várias portas — Telegram, Claude Chat, Claude Code, com futuras integrações planejadas.
   *(2026-05-03)*

4305. A decisão sobre o parâmetro drop_pending_updates pode ser alterada para uma abordagem que avise o usuário em caso de mensagens descartadas durante interrupções.
   *(2026-05-02)*

4306. O Hub Qdrant é a memória central do Gus, onde informações são armazenadas.
   *(2026-05-03)*

4307. Os arquivos com as demandas pendentes são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao, e um template `_frontmatter-referencia.md`.
   *(2026-05-03)*

4308. O protocolo de ativação Gus é acionado sempre que uma mensagem menciona 'Gus' em qualquer forma.
   *(2026-05-04)*

4309. O estado atual de migração ADR-001 está em curso, visando aposentar o Mem0 SaaS.
   *(2026-05-03)*

4310. O log de resumos-mem0 indica que o curador Telegram está em modo de erro há mais de 3 dias, sem gerar entradas válidas.
   *(2026-05-04)*

4311. Preciso processar as demandas ou tem algo específico em mente?
   *(2026-05-03)*

4312. O arquivo gus-identity.md contém drift factual e redundâncias que precisam ser corrigidos.
   *(2026-05-04)*

4313. Os projetos ativos de Gustavo incluem: Phronesis-Bench, NeuroGus, MGE/MGX, TER e Axon.
   *(2026-05-03)*

4314. O arquivo `gus-bootstrap.md` possui 421 linhas e 4795 tokens.
   *(2026-05-03)*

4315. As diretrizes operacionais do Gus incluem não alucinar, verificar a veracidade das informações antes de afirmá-las, e validar situações antes de realizar ações irreversíveis.
   *(2026-05-03)*

4316. O ciclo de vidas do schema gus-18 está declarado mas não implementado.
   *(2026-05-03)*

4317. A demanda dialogos/inbox-claude-code tem 3 pendências.
   *(2026-05-03)*

4318. A auditoria diária não é cega para o brain `gus` e ignora o campo `area` que deveria estar no payload.
   *(2026-05-03)*

4319. A estrutura de acesso do Chat precisa ser definida claramente entre real-time MCP, uploads curados e demandas inbox-code.
   *(2026-05-03)*

4320. O passo para criar um Service Account e configurar a WIF já foi realizado, o que elimina a necessidade de decidir entre as opções de Drive sync.
   *(2026-05-03)*

4321. Performance e observabilidade serão revisadas na fase 6 do plano, que abordará o cache de embeddings e a saúde do sistema.
   *(2026-05-03)*

4322. O status `fallback-mem0` foi removido e o `_resumir_e_salvar` alerta Gustavo em caso de erro do curador.
   *(2026-05-03)*

4323. Os JSONs estruturados de exames LAFE de janeiro de 2026 estão no caminho Gus-Sync/pessoal/saude/gus__2026-01-27__lafe.json.
   *(2026-05-02)*

4324. O Hub tem 19 fragmentos no brain `gustavo`, sistema ocioso nas últimas 6h.
   *(2026-05-03)*

4325. Commit `48b8bed` — Correção para não logar o valor de `MCP_URL_SECRET` e adição do padrão de redação.
   *(2026-05-03)*

4326. Gustavo tem hipertireoidismo em tratamento com Tapazol, acompanhado por endocrinologista.
   *(2026-05-03)*

4327. A auditoria do Chat envolve todos os aspectos relacionados ao projeto Claude Chat.
   *(2026-05-03)*

4328. O estado atual do Gus é a aposentadoria do Mem0 SaaS, com o Hub Qdrant como a fonte da verdade.
   *(2026-05-03)*

4329. Mem0 SaaS está aposentado. O nome 'mem0-from-chat' é puramente legado.
   *(2026-05-03)*

4330. Há um total de 3 demandas paradas em `dialogos/inbox-claude-code/`.
   *(2026-05-04)*

4331. Quatro demandas pendentes foram identificadas no dialogos/inbox-claude-code.
   *(2026-05-02)*

4332. Haverá uma migração de memórias do Mem0 SaaS para o Hub Qdrant até 12/05/2026.
   *(2026-05-03)*

4333. Gustavo precisa adicionar saldo em console.anthropic.com/settings/billing.
   *(2026-05-03)*

4334. O sistema tem suporte a captura multimídia via integração com o Claude Chat.
   *(2026-05-02)*

4335. O sistema 'Gus' é um agente pessoal multi-porta, que opera em várias plataformas, incluindo Telegram e Claude Chat.
   *(2026-05-03)*

4336. D4 propõe mover o arquivo dimagem.py para a pasta integrations para melhor sinalização de dependências.
   *(2026-05-02)*

4337. Estou aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/` (algumas com nome quebrado — "Documento sem título.md" provavelmente é lixo de sync).
   *(2026-05-03)*

4338. Bootstrap gus-chat atualizado pra v6 (02/05/2026): captura real-time via MCP como padrão, 2 caminhos documentados, brain gus agora recebe meta_reflexao e identidade_operacional do Chat. Refs Mem0 removidas, paths curador/hub atualizados. PR #77 renomeia legacy mem0 → curador/hub.
   *(2026-05-02)*

4339. Caminho proposto: 'Fase 1 quick wins → Fase 1.7 limpeza Hub → Fase 1.8 meta_relatorio recorrente → Fase 2 comparar curadores → Decisão modelo final → Fase 5 prompt novo + importação inteligente dos 204 → Hub clean com ~150-200 frags úteis'.
   *(2026-05-03)*

4340. Nos últimos meses, Gustavo focou na sanitização do TioGu com 163 testes unitários adicionados, redação de PII no output, e orçamento de bytes para cache de mídia, além de corrigir um bug de KeyError do curador que resultou em falhas silenciosas por 3 dias.
   *(2026-05-03)*

4341. O curador agora está utilizando o modelo Haiku + Sonnet+GPT-4o.
   *(2026-05-03)*

4342. O sistema Gus é um agente pessoal multi-porta em produção.
   *(2026-05-03)*

4343. Claude se baseia em memória e para a inicialização, lendo arquivos do bootstrap.
   *(2026-05-04)*

4344. A stack de memória está em estado intermediário arriscado, com 204 fragmentos não-migrados.
   *(2026-05-03)*

4345. Gustavo está atuando na produção do sistema 'Gus', um agente IA multi-porta com o Telegram, Code e Chat, agora alimentado pelo Hub Qdrant direct (após a finalização do ADR-001 em 27/04/2026) — a captura de memória é feita com dois cérebros ativos: 'gustavo' e 'gus'.
   *(2026-05-03)*

4346. A execução do script de migração retornou zero fragmentos para migração da coleção `gus`.
   *(2026-05-03)*

4347. O Hub Qdrant é a fonte da verdade.
   *(2026-05-03)*

4348. URL secret protege.
   *(2026-05-03)*

4349. O conteúdo no Mem0 SaaS inclui 204 fragmentos que registram informações biográficas e clínicos.
   *(2026-05-03)*

4350. A demanda `2026-05-01-captura-multiporta-curador.md` precisa de um gatilho proativo no Chat.
   *(2026-05-03)*

4351. A migração coleta dual Haiku × Sonnet roda até 12/05.
   *(2026-05-02)*

4352. A coleta de dados no Hub é realizada em modo dual: Haiku e Sonnet/GPT em paralelo.
   *(2026-05-02)*

4353. Interações no celular agora podem ser feitas criando arquivos diretamente na nova pasta no Drive, sem necessidade de YAML.
   *(2026-05-03)*

4354. Gustavo Pratti de Barros é anestesiologista no Dimagem e pesquisador independente em IA.
   *(2026-05-03)*

4355. Core obrigatório deve ser lido em toda aba nova para garantir 80% do contexto.
   *(2026-05-03)*

4356. Gustavo deve aprovar a lista de duplicatas e cross-brain antes da limpeza ativa do Hub.
   *(2026-05-03)*

4357. PR #76 migrou pra WIF e você já configurou os secrets (Service Account, pool, provider). Não precisa mais decidir 1/2/3 sobre Drive sync.
   *(2026-05-03)*

4358. Hub Qdrant é a fonte da verdade, com migração em curso.
   *(2026-05-03)*

4359. As diretrizes que devem ser seguidas pelo sistema incluem não alucinar, verificar informações antes de afirmar e garantir uma comunicação clara.
   *(2026-05-03)*

4360. Os arquivos principais que Gus lê são: gus-bootstrap.md, gus-estado-atual.md e gus-identity.md.
   *(2026-05-03)*

4361. O Hub é a fonte da verdade do sistema Gus, com arquivos .md no GitHub e espelhados no Drive.
   *(2026-05-03)*

4362. O plano de saneamento do Hub está dividido em 6 fases.
   *(2026-05-03)*

4363. O curador utiliza Haiku e GPT-4o-mini em paralelo, resultando em 4 chamadas de LLM por input.
   *(2026-05-03)*

4364. O sistema tem 4 caminhos de escrita que coexistem com regras parcialmente compatíveis.
   *(2026-05-03)*

4365. O fragmento salvo é sobre identidade, que é curioso por não conter dados do paciente.
   *(2026-05-03)*

4366. A proposta B para o Bootstrap sugere criar arquivos por função e otimizar a inicialização.
   *(2026-05-03)*

4367. Gustavo é anestesiologista, não programa — toda implementação passa por mim/Tiogu.
   *(2026-05-03)*

4368. O cache de mídia do TioGu tem um limite máximo de 200MB, evitando o erro de falta de memória (OOM).
   *(2026-05-03)*

4369. Houve uma atualização para o SDK do Anthropic, que foi para a versão 0.97.0.
   *(2026-05-04)*

4370. O curador do sistema tem a função de gerenciar as interações e as informações trocadas durante as sessões.
   *(2026-05-03)*

4371. A captura dual de modelos no curador (Haiku × GPT-4o-mini) termina em 12/05/2026.
   *(2026-05-03)*

4372. O hook vai continuar reclamando a cada turno enquanto o arquivo estiver untracked.
   *(2026-05-04)*

4373. Os 4 arquivos principais do projeto que fornecem 80% do contexto para novas abas são: gus-bootstrap.md, gus-identity.md, gus-estado-atual.md e estado-atual.md.
   *(2026-05-03)*

4374. O Chat deve ler seu estado e o bootstrap do Drive para garantir informações atualizadas.
   *(2026-05-03)*

4375. As pendências de Gustavo incluem setar `MCP_URL_SECRET` no Railway e decidir sobre a sincronização do Drive.
   *(2026-05-03)*

4376. O cron roda a cada 15 minutos, mesmo quando o Hub está ocioso.
   *(2026-05-03)*

4377. Estou aqui na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

4378. A arquitetura de memória do sistema migrou de Mem0 para Qdrant em 2026.
   *(2026-05-03)*

4379. A coleta de modelos no curador (Haiku × GPT-4o-mini) deve ser concluída até 12/05/2026, após o que Gustavo escolherá um modelo definitivo.
   *(2026-05-03)*

4380. E aí Gustavo, tudo bem! O estado atual (13:31 BRT, hoje) mostra o sistema razoavelmente ativo mas com alguns sinais de atenção.
   *(2026-05-03)*

4381. O estado de migração ADR-001 está em curso: o Hub Qdrant será a fonte da verdade após a aposentadoria do Mem0 SaaS.
   *(2026-05-03)*

4382. A seção de disciplina anti-esquecimento foi atualizada para incluir dois caminhos de captura.
   *(2026-05-03)*

4383. As metas e decisões durante o projeto estão sendo decididas na aba separada.
   *(2026-05-02)*

4384. Gustavo Pratti de Barros é anestesiologista no Rio de Janeiro, atuando no Dimagem (clínica de imagem diagnóstica com 3 unidades: Nova Iguaçu, Taquara, São Gonçalo).
   *(2026-05-04)*

4385. Gus é um sistema de agente pessoal multi-porta que opera através de interfaces como Telegram, Claude Code e Claude Chat, e será expandido no futuro para incluir Custom GPT mobile e Alexa.
   *(2026-05-03)*

4386. O chat diz que gravou, mas quando busco em outra aba, a outra aba não cita os fragmentos.
   *(2026-05-04)*

4387. MCP Gus é uma ferramenta que conecta o agente Gus com outras interfaces, como Telegram e Claude Chat.
   *(2026-05-03)*

4388. O Hub Qdrant é a fonte da verdade para a memória do Gus.
   *(2026-05-03)*

4389. Gustavo é anestesiologista e não programa, toda implementação passa pelo Gus.
   *(2026-05-03)*

4390. O bot opera com dependências como python-telegram-bot, anthropic SDK, openai, FastAPI e Qdrant.
   *(2026-05-03)*

4391. Os 4 arquivos pendentes são: captura-multiporta-curador, drive-sync-oauth-fix, pendencias-claude-chat-consolidacao e (o `_frontmatter-referencia.md` é só template).
   *(2026-05-03)*

4392. Gustavo é anestesiologista e utiliza um agente pessoal multi-porta chamado Gus, que opera em diferentes plataformas como Telegram, Claude Code e Claude Chat.
   *(2026-05-03)*

4393. Para mandar uma demanda pelo celular, cria-se um arquivo no Drive chamado 'meu-pedido.md' que será auto-injetado com frontmatter.
   *(2026-05-03)*

4394. A demanda `2026-05-01-drive-sync-oauth-fix.md` está ativa.
   *(2026-05-02)*

4395. Gus está na branch `claude/initial-setup-iWTfL`, com 6 demandas pendentes em `dialogos/inbox-claude-code/`.
   *(2026-05-03)*

4396. Mem0 SaaS tem ~204 fragmentos não-migrados e o código de leitura em gus/memory.py ainda faz fallback pra ela.
   *(2026-05-03)*
