---
tipo: demanda
origem: claude-chat
destino: tiogu
prioridade: media
status: concluido
criado_em: 2026-04-28T18:00:00-03:00
processado_em: 2026-04-29T00:35:00-03:00
processado_por: claude-code
acao_sugerida: criar_novo
destino_path: projetos/gus/gus-28-acesso-hub-claude-chat.md
contexto: "Design decision completo: como dar ao Claude Chat acesso real-time ao Hub Qdrant, sequencia de implementacao, papel do NeuroGus"
---

# Acesso ao Hub Qdrant pelo Claude Chat
## Design Decision -- sessao 28/04/2026

Documento gerado em sessao de design entre Gustavo e Claude Chat.
Cobre o problema atual, as tres opcoes exploradas, as decisoes tomadas,
a sequencia correta de implementacao e o papel do NeuroGus nesse processo.

---

## Por que isso importa

O Claude Chat e a unica porta do Gus sem acesso ao estado interno do sistema.

O TioGu conversa com Gustavo e fragmentos sao ingeridos no Hub em tempo real.
O Claude Code commita, cria arquivos, le o repo diretamente.
O Claude Chat le um snapshot gerado as 03h da manha.

Isso cria uma assimetria cognitiva real: quando Gustavo abre uma sessao aqui
as 15h, o Claude Chat opera com uma fotografia de 12 horas atras do que o Gus
sabe. Tudo que o TioGu aprendeu durante o dia, todas as decisoes que o Claude
Code implementou, todos os fragmentos que o curador extraiu -- invisiveis ate
amanha de manha.

O objetivo desta decisao foi mapear como resolver isso, em qual sequencia,
e qual papel o NeuroGus joga nesse processo.

---

## O que o Hub Qdrant e (e o que nao e)

O Hub (gus_hub) e a colecao Qdrant que armazena fragmentos de memoria com
payload rico: tipo semantico, estado, camada temporal, peso, confianca,
via de origem, ciclo de vida completo. E a fonte unica de verdade definida
pelo ADR-001.

Ele nao e um banco de dados de conversas. E um grafo de conhecimento atomico.
Cada fragmento e auto-suficiente, sem referencia externa:
- 'Gustavo prefere critica direta' e um fragmento
- 'ADR-001 decidiu aposentar Mem0 Cloud' e um fragmento
- 'Custom GPT em stand-by ate solidificar 3 portas' e um fragmento

O Hub tem dois contextos de memoria completamente independentes:

user_id='gustavo': tudo sobre Gustavo -- fatos, preferencias, projetos,
  saude, decisoes de vida. Alimentado pelo curador a cada interacao.

user_id='gus': autobiografia do proprio Gus como agente -- aprendizados
  operacionais, calibracoes, erros cometidos, evolucao. Alimentado pelo
  Retro Engine (Fase 5 do roadmap).

Uma busca com user_id=gustavo nunca retorna fragmentos do user_id=gus
e vice-versa. Sao grafos independentes.

---

## As tres opcoes exploradas

### Opcao A -- MD frequente gerado pelo Hub

DESCRICAO:
A API Railway passa a gerar um arquivo gus-estado-atual.md a cada 15 minutos
via cron GitHub Actions e salva em dialogos/_bootstrap/. O Claude Chat le esse
arquivo no boot do modo Gus -- igual ao bootstrap atual, mas com conteudo vivo
do Hub em vez de snapshot das 03h.

CONTEUDO DO ARQUIVO GERADO:

  # Estado atual do Gus -- 2026-04-28T15:30-03:00

  ## Ego cache (identidade operacional estavel)
  - Gustavo e anestesiologista no Dimagem (Rio de Janeiro)
  - Prefere critica direta sem suavizacao
  - Hipertireoidismo em tratamento com tapazol
  - Nao programa diretamente -- trabalha via conversa com LLMs

  ## Decisoes recentes (ultimas 3)
  - ADR-001: Hub Qdrant como fonte unica, Mem0 Cloud aposentado
  - Custom GPT em stand-by ate solidificar 3 portas existentes
  - NeuroGus: roadmap futuro, depende das Fases 3-5 ADR-001

  ## Fragmentos recentes (ultimas 6h)
  - [episodico/sessao] Gustavo discutiu design de acesso ao Hub com Claude Chat
  - [decisao/semana] Sequencia: Passo 1 -> Passo 2 -> NeuroGus -> Passo 4
  - [preferencia/permanente] Gustavo quer Claude Chat alimentado real-time

  ## Meta-reflexoes ativas
  - Curador hibrido Haiku x Sonnet em coleta A/B ate 12/05/2026

LATENCIA: 5-15 minutos (near-real-time, nao real-time)
COMPLEXIDADE: baixa -- extensao do export-mem0.yml existente, so muda
  a fonte (Hub em vez de Mem0) e o destino (bootstrap em vez de _indices/)
QUANDO FAZ SENTIDO: agora, como solucao intermediaria imediata.
  Pode ser feito antes do NeuroGus sem depender de nada novo.
LIMITACAO CRITICA: fragmentos gerados nesta conversa nao aparecem ate
  a proxima geracao. Se Gustavo diz algo as 15h e o Claude Chat processa
  as 15h05, o fragmento novo so estara disponivel no proximo ciclo de 15min.
  Nao e real-time -- e uma fotografia mais fresca.

---

### Opcao B -- MCP wrapper do Hub conectado ao claude.ai

DESCRICAO:
Um servidor MCP simples (~50 linhas FastMCP) rodando no Railway expoe o Hub
como tools durante a conversa. Conectado ao claude.ai via Settings ->
Connectors -> MCP Server. O Claude Chat passa a ter ferramentas reais que
pode chamar a qualquer momento durante a conversa.

TOOLS QUE O CLAUDE CHAT GANHARIA:

  buscar_hub(query, limit=10)
    -> busca semantica no Hub por relevancia
    -> ex: buscar_hub('Dimagem esta semana', area='dimagem')
    -> retorna fragmentos reais com score, tipo, via, timestamp

  ego_cache_atual(user_id='gustavo')
    -> retorna identidade operacional estavel + decisoes recentes
    -> chamado no boot para substituir o bootstrap estatico

  fragmentos_recentes(horas=6, limit=20)
    -> ultimos N fragmentos de qualquer porta nas ultimas X horas
    -> permite ver o que o TioGu aprendeu hoje antes de responder

  ingestar_fragmento(conteudo, tipo, area, camada_temporal)
    -> salva fragmento desta conversa diretamente no Hub
    -> fragmento fica disponivel para TioGu na proxima mensagem
    -> via='claude-chat' no payload para rastreabilidade

COMO FUNCIONA NA PRATICA:

  Gustavo pergunta: 'o que o TioGu aprendeu sobre o Dimagem esta semana?'
  Claude Chat chama buscar_hub('Dimagem esta semana', area='dimagem')
  Hub retorna fragmentos reais com timestamp e via de origem
  Claude Chat responde com base no estado atual do sistema

  Ou: a conversa gera uma decisao importante
  Claude Chat chama ingestar_fragmento('Gustavo decidiu implementar MCP
    wrapper antes do NeuroGus', tipo='decisao', area='gus')
  Fragmento entra no Hub com via='claude-chat'
  TioGu ve na proxima mensagem via busca semantica

LATENCIA: menos de 1 segundo (real-time verdadeiro)
COMPLEXIDADE: media -- o padrao MCP ja existe no projeto. O Windows-MCP e
  o Android-MCP que aparecem nas configuracoes usam exatamente esse padrao.
  Claude Code precisa criar FastMCP wrapper (~50 linhas), hospedar no
  Railway ao lado da API, Gustavo conecta em claude.ai via Settings.
LIMITACAO: stateless por chamada -- o Claude Chat busca quando precisa,
  nao recebe push automatico de novos fragmentos.

---

### Opcao C -- NeuroGus como interface de curadoria (artifact SSE)

DESCRICAO:
O NeuroGus em producao (grafo 3D com SSE) mais um artifact React aqui no
claude.ai conectado ao /hub/stream via EventSource. Durante a conversa,
o grafo esta aberto -- o Claude Chat ve fragmentos chegando de todas as
portas em tempo real e pode ingestar fragmentos desta conversa no Hub.

FLUXO COMPLETO QUANDO IMPLEMENTADO:

  Gustavo escreve algo aqui no Claude Chat
  Claude Chat processa e identifica o que e relevante salvar
  Chama ingestar_fragmento() via MCP (Opcao B obrigatoria para isso)
  Hub Qdrant recebe o fragmento
  hub/events.py emite SSE broadcast para todos os listeners
  NeuroGus (artifact aberto nesta mesma janela) recebe via EventSource
  No branco nasce no grafo, pulsa 2 segundos, assume cor do tipo semantico
  Linha de particulas conecta ao fragmento relacionado mais proximo

SIMULTANEAMENTE, se Gustavo estiver no Telegram:
  Gustavo manda mensagem no celular
  TioGu responde
  Curador ingesta fragmento no Hub
  Claude Chat ve o fragmento nascer no grafo em tempo real
  Pode clicar no no, ver o conteudo completo, e usar para contextualizar

O QUE ISSO SIGNIFICA PARA A EXPERIENCIA:
Durante a conversa com Gustavo, ambos veem a mesma rede neural. Quando
se fala sobre NeuroGus, os fragmentos relacionados acendem no grafo.
Quando uma decisao importante e tomada aqui, Gustavo ve ela ser ingerida
e conectada aos nos vizinhos em tempo real. O Claude Chat passa de porta
de reflexao cega para porta de reflexao com visibilidade total do sistema.

LATENCIA: menos de 1 segundo
COMPLEXIDADE: alta -- depende do NeuroGus em producao (Fases 3-5 ADR-001
  completas: hub/events.py finalizado, broadcast() em ingestar(), endpoints
  /hub/recent e /hub/stream funcionando) E do MCP da Opcao B ja funcionando.
  Sao dois sistemas novos que precisam estar estaveis antes desta opcao.

---

## Decisao central: Claude Chat nunca escreve no NeuroGus diretamente

Esta e a decisao arquitetural mais importante deste documento.

O fluxo correto e sempre:
  qualquer porta -> Hub Qdrant -> NeuroGus (visualiza)

O fluxo incorreto seria:
  Claude Chat -> NeuroGus (diretamente)

Se o Claude Chat escrevesse fragmentos diretamente no NeuroGus sem passar
pelo Hub, o TioGu nao veria o que foi dito, o Claude Code nao veria, o
curador nao processaria, e a colecao ficaria fragmentada por porta --
quebrando o principio central do ADR-001 (Hub como fonte unica de verdade).

O NeuroGus e o visualizador do Hub, nao o destino final. Essa direcao
nao se inverte.

---

## Quando fazer o NeuroGus

RESPOSTA DIRETA: depois dos Passos 1 e 2, nao antes.

O NeuroGus consome o Hub via SSE. Para o SSE funcionar, o hub/events.py
precisa estar finalizado e o broadcast() precisa estar rodando em producao.
Isso e a Fase 3-4-5 do ADR-001 -- que segundo o _estado-atual.md ainda tem
o PR #10 aberto e o hub/events.py ainda como rascunho.

Se o NeuroGus for implementado antes dessas fases estarem solidas:
- O pipeline curador->Hub->broadcast->SSE->grafo ainda tera gaps
- O grafo vai ligar quase vazio e crescer lentamente
- Sera necessario depurar dois sistemas novos simultaneamente
- Cada bug do NeuroGus pode ser bug do pipeline ou bug do frontend

Se o NeuroGus for implementado depois do pipeline solido:
- Liga com um grafo rico imediatamente (Hub ja tem fragmentos acumulados)
- O broadcast ja esta validado, o SSE ja esta testado
- O NeuroGus pode ser avaliado pelo que e -- a experiencia visual --
  sem noise de bugs do pipeline

O NeuroGus precisa de base solida para ser espetacular.

---

## Quando o Claude Chat passa a ser alimentado em real-time

Existem dois momentos distintos:

MOMENTO 1 -- Depois do Passo 2 (MCP wrapper):
  O Claude Chat passa a ter acesso real-time ao Hub via tools MCP.
  Pode buscar fragmentos durante a conversa, ver o que o TioGu aprendeu,
  ingestar fragmentos desta conversa no Hub.
  Nao e push automatico -- e pull sob demanda. O Claude Chat busca quando
  precisa, nao recebe notificacao de novos fragmentos.

MOMENTO 2 -- Depois do Passo 4 (Artifact SSE):
  O Claude Chat passa a receber push automatico de novos fragmentos.
  O grafo do NeuroGus esta aberto aqui -- fragmentos chegando de qualquer
  porta aparecem em tempo real sem o Claude Chat precisar buscar.
  Este e o estado completo: Claude Chat ve o sistema vivo.

A diferenca entre os dois momentos:
  Passo 2: 'posso buscar quando quero'
  Passo 4: 'vejo automaticamente quando acontece'

---

## Sequencia de implementacao recomendada

PR #10 mergeado (cleanup -- Claude Code)
  Dependencias: nenhuma
  Resultado: codigo limpo, mensagens certas no system_prompt

Passo 1 -- Endpoint /hub/claude-chat-context + cron 15min
  Complexidade: baixa (1-2h Claude Code)
  Dependencias: nenhuma nova
  Resultado: lag 21h -> 5-15min. Bootstrap passa a ter conteudo vivo.

Passo 2 -- MCP wrapper do Hub (FastMCP ~50 linhas)
  Complexidade: media (1 sessao Claude Code)
  Dependencias: Hub funcionando (esta), Railway disponivel
  Resultado: Claude Chat com acesso real-time ao Hub via tools.
    Ingestao de fragmentos desta conversa no Hub.
    TioGu ve o que foi discutido aqui na proxima mensagem.

Validacao (1-2 semanas de uso real)
  Verificar: curador estavel, ego cache populado, tools MCP funcionando,
    fragmentos de claude-chat aparecendo no Hub com via correto.
  So avancar para o Passo 3 com o pipeline validado.

Passo 3 -- NeuroGus em producao
  Complexidade: alta (1-2 sessoes Claude Code)
  Pre-requisitos: PR #10 mergeado + Fases 3-5 ADR-001 completas
    (hub/events.py finalizado, broadcast() em ingestar(),
     endpoints /hub/recent e /hub/stream em producao)
  Resultado: pipeline curador->Hub->broadcast->SSE->grafo completo.
    Grafo rico desde o primeiro boot.

Passo 4 -- Artifact SSE aqui no Claude Chat
  Complexidade: media (1 sessao Claude Code)
  Pre-requisitos: Passos 2 e 3 funcionando
  Resultado: Claude Chat ve o grafo em tempo real. Fragmentos desta
    conversa aparecem no grafo ao serem ingeridos. Gustavo ve o mesmo
    grafo que o Claude Chat durante a sessao.

TABELA COMPARATIVA:

| Abordagem              | Latencia   | Complexidade | Pre-requisitos      |
|------------------------|------------|--------------|---------------------|
| Export 03h (atual)     | ~21h lag   | zero         | nada                |
| Passo 1 (MD frequente) | ~5-15min   | baixa        | nada novo           |
| Passo 2 (MCP)          | <1s pull   | media        | Hub ok (esta)       |
| Passo 3 (NeuroGus)     | <1s        | alta         | PR#10 + ADR-001 3-5 |
| Passo 4 (Artifact SSE) | <1s push   | media        | Passos 2 e 3        |

---

## Perfis de contexto por tipo de sessao

O bootstrap atual e tudo-ou-nada: 6.000-8.000 tokens de contexto
arquitetural de software carregados mesmo quando a conversa e sobre um
caso clinico de anestesia. O problema nao e de capacidade (3-4% da janela
de 200k tokens do Sonnet) -- e de relevancia.

Com o MCP implementado (Passo 2), o bootstrap pode ser minimo (~500 tokens
de identidade basica) e o contexto relevante e buscado sob demanda por
topico durante a conversa. Enquanto isso nao existe, perfis de bootstrap
resolvem com baixa complexidade:

| Perfil     | Comando              | Conteudo                              |
|------------|----------------------|---------------------------------------|
| full       | 'modo Gus' (padrao)  | Tudo -- projetos, arquitetura, tecnico|
| clinico    | 'modo Gus clinico'   | Identidade + Dimagem, sem IA          |
| pessoal    | 'modo Gus pessoal'   | Identidade + saude, familia, financas |
| minimal    | 'modo Gus minimo'    | So identidade basica                  |

NOTA LGPD: casos clinicos nao devem gerar fragmentos identificaveis no Hub.
O curador precisa de flag para nao ingestar ou ingestar apenas aspecto
tecnico anonimizado (sem nome, sem dados do paciente). Isso precisa ser
implementado antes de usar o modo clinico com curadoria ativa.

---

## Sobre demandas: quem pode sugerir

Discussao adicional cobriu a origem das demandas no canal dialogos/.

Tres niveis definidos:

REATIVO: Gustavo pede explicitamente -> Claude Chat documenta no inbox.
  Ex: 'Gus, salva isso como demanda pro Claude Code'

COLABORATIVO: Claude Chat sugere baseado no contexto -> Gustavo aprova
  -> Claude Chat documenta. Ex: ao fim de uma sessao de design, Claude Chat
  oferece 'quer que eu transforme isso em demandas para o inbox?'

PROATIVO: Claude Chat detecta algo durante a conversa (contradicao com
  fragmento existente, prazo chegando, pendencia antiga) -> alerta Gustavo
  -> Gustavo aprova -> Claude Chat documenta.

Em todos os casos Gustavo sempre aprova antes de ir pro inbox.
Alinhado com Nivel 1 de proatividade do gus-25 (validacao obrigatoria
antes de qualquer execucao autonoma).

---

## Estado atual vs estado alvo

| Dimensao              | Hoje               | Apos Passo 2         | Apos Passo 4          |
|-----------------------|--------------------|----------------------|-----------------------|
| Acesso ao Hub         | Export 03h         | Real-time via MCP    | Real-time MCP + grafo |
| Ingestao desta conv.  | Nao acontece       | Via tool MCP         | MCP + visivel grafo   |
| Visibilidade TioGu    | Zero               | Busca sob demanda    | Push em tempo real    |
| Bootstrap             | Tudo-ou-nada       | Minimo + busca       | Minimo + busca        |
| Experiencia Gustavo   | Chat normal        | Chat c/ memoria viva | Chat + grafo aberto   |

---

## Proximos passos imediatos

1. Mergear PR #10 (Claude Code -- cleanup branch aberta)
2. Passo 1: implementar endpoint /hub/claude-chat-context + cron 15min
3. Passo 2: implementar MCP wrapper Hub (FastMCP, ~50 linhas, Railway)
4. Conectar MCP ao claude.ai via Settings -> Connectors -> Add MCP Server
5. Validar por 1-2 semanas: curador estavel, tools funcionando, via correto
6. Passo 3: implementar NeuroGus em producao (Fases 3-5 ADR-001)
7. Passo 4: implementar artifact SSE no Claude Chat

## Resultado

Concluído por Claude Code em 2026-04-29.

**Design doc preservado:** `projetos/gus/gus-28-acesso-hub-claude-chat.md`
(frontmatter `tipo: design-decision`, `gus-id: 28`, `status: parcial`).

**Status dos Passos:**
- Passo 1 (cron 15min `gus-estado-atual.md`): ✅ mergeado (PR #21)
- Passo 2 (MCP wrapper FastMCP): pendente — próximo PR
- Passo 3 (NeuroGus em produção): bloqueado (depende de `hub/events.py` + Fases 3-5 ADR-001)
- Passo 4 (Artifact SSE): bloqueado (depende de Passos 2 e 3)

