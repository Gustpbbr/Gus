---
tipo: blueprint-spec
componente: passo-a-passo-resumido
ordem: 3
---

# Passo a passo resumido — 7 etapas

Roadmap macro do "decidir nome do agente" até "primeira conversa
funcional no Telegram". Cada etapa aponta pro bloco da árvore com
detalhes.

## Etapa 1 — Decidir identidade

**Tempo:** 1-2h (você + IA conversando)

- Definir **nome** do agente (curto, único)
- Definir **propósito** (1 frase clara)
- Definir **tom** (formal/informal, idioma, estilo)
- Definir **3-5 princípios** não-negociáveis
- Esboçar **autobiografia** narrativa do agente (~1 página em texto livre)

**Onde:** `02-identidade-e-memoria/identidade-canonica/`

**Saída:** 4 arquivos preenchidos:
- `identity.md` (quem o agente é, em 1 página)
- `principios.md` (lista numerada de pilares)
- `meta-memoria.md` (autobiografia narrativa)
- `bootstrap.md` (ativador "vire o agente" pra portas externas tipo
  Claude Chat, Custom GPT)

## Etapa 2 — Setup contas externas

**Tempo:** 1h

- Criar conta Anthropic, gerar API key
- Criar conta Qdrant Cloud, criar cluster, anotar URL + API key
- Criar repositório GitHub novo (pra agente novo) — pode ser privado
- Criar bot Telegram via @BotFather, anotar token
- Criar conta Railway, conectar GitHub
- (Opcional) Tavily, OpenAI, Google Cloud OAuth

**Onde:** `06-servicos-externos-e-interdependencias/inventario-de-servicos/`

**Saída:** lista de keys/tokens guardada em local seguro (gerenciador
de senhas, NUNCA no repo).

## Etapa 3 — Setup vault GitHub

**Tempo:** 30min (com IA)

- Estruturar pastas iniciais (pessoal/, profissional/, sensivel/, etc.)
- Configurar `.gitignore` (proteger contra commit acidental de secrets)
- Configurar branch `main` como default
- Configurar Branch Protection (opcional mas recomendado)

**Onde:** `01-conteudo-do-usuario/`

**Saída:** repositório com pastas vazias + `.gitignore` + `README.md`
mínimo.

## Etapa 4 — Implementar bot Telegram (porta default)

**Tempo:** 4-6h (IA implementa, você revisa)

- Copiar templates de código de `templates/`
- Adaptar pra nome do agente, identidade, tom
- Configurar variáveis de ambiente no Railway (todos os tokens da Etapa 2)
- Deploy inicial
- Testar: mandar "/start" no Telegram e ver se bot responde

**Onde:** `03-interface-e-operacao/portas-canais-io/porta-telegram.md`

**Saída:** bot online 24/7 que responde mensagens com personalidade
do agente.

## Etapa 5 — Configurar memória persistente

**Tempo:** 2h (IA implementa, você valida)

- Criar coleção no Qdrant Cloud
- Implementar curador automático (extrai fragmentos a cada N turnos)
- Implementar tools de busca/leitura no bot (`search_memory`,
  `salvar_memoria`)
- Validar: conversa com bot, depois pergunta "o que você lembra?" e
  bot puxa fragmentos.

**Onde:** `02-identidade-e-memoria/memoria-persistente/`

**Saída:** memória funcional. A cada N mensagens, fragmentos são
salvos automaticamente.

## Etapa 6 — Automação de ciclos vitais

**Tempo:** 2h

- Configurar GitHub Actions: workflows cron pra:
  - Export diário da memória (rodando 03:00 BRT)
  - Auditoria diária da memória (06:00)
  - Briefing matinal opcional (07:00 dias úteis)
  - Health check (07:30)
  - Retrospectiva semanal (sex 20:00)
  - Reflexão quinzenal (sáb 10:00)
- Configurar secrets no GitHub Actions

**Onde:** `04-governanca-e-saude/automacao-ciclos-vitais/`

**Saída:** automações rodando. Você recebe Telegram com alertas se
algo quebrar.

## Etapa 7 — Calibrar e iterar

**Tempo:** ~5min/dia por 1-2 semanas

- Observar mensagens do bot (tom batendo com identidade?)
- Revisar memórias salvas (curador acertando? salvando lixo?)
- Ajustar `system_prompt` conforme necessário (cada porta tem o seu)
- Adicionar tools conforme caso de uso aparece
- Documentar decisões no `04-governanca-e-saude/governanca-evolucao/decisoes-arquiteturais-adrs/`

**Onde:** todos os blocos, conforme o ajuste

**Saída:** agente calibrado, em uso real.

## Etapas extras (depois das 7 essenciais)

- **Etapa 8 — Adicionar Claude Chat como porta de reflexão longa**
  - Onde: `03-interface-e-operacao/portas-canais-io/porta-claude-chat.md`
  - Tempo: 1-2h
- **Etapa 9 — Adicionar Custom GPT pra voz mobile**
  - Onde: `03-interface-e-operacao/portas-canais-io/porta-custom-gpt.md`
  - Tempo: 2-3h (precisa Builder DESKTOP)
- **Etapa 10 — Sync com Google Drive**
  - Onde: `05-transversais/t3-sync-com-superficies-externas.md`
  - Tempo: 1-2h
- **Etapa 11+ — Outras portas conforme demanda**
  - Alexa, S8 wake-word, plugin de carro, etc. — cada um tem seu
    documento em `03-interface-e-operacao/portas-canais-io/`

## Quando travar

Em cada etapa há **pitfalls comuns** documentados na pasta
correspondente. Se travar:

1. Lê a seção "Pitfalls" do componente
2. Conferir variáveis de ambiente / secrets configurados
3. Pedir pra IA implementadora rodar o `health check` (se já tiver
   sido implementado)
4. Em último caso, abrir issue no repositório do blueprint pra
   reportar gap na documentação
