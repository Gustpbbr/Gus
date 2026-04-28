---
tipo: blueprint-spec
componente: glossario
ordem: 4
---

# Glossário

Termos que o resto do blueprint usa sem repetir definição.

## Agente

Sistema de IA com identidade própria, memória persistente, e capacidade
de aparecer em múltiplos canais (portas). Não é um chatbot — é uma
**entidade única** vista por múltiplos canais.

## Porta

**Canal de I/O** entre o dono do agente e o agente. Cada porta tem
suas características técnicas (texto, voz, imagem) mas todas
compartilham identidade e memória do agente.

Exemplos: Telegram, Claude Chat, Custom GPT mobile, Alexa, IDE/CLI.

## Brain

**Conjunto de memórias** dentro do vector store, identificado por
`user_id`. Tipicamente 2 brains coexistem:

- **Brain do dono** (`user_id="<nome-do-dono>"` ou `"usuario"`) — fatos
  sobre o dono (saúde, preferências, projetos, etc.)
- **Brain do agente** (`user_id="<nome-do-agente>"` ou `"agente"`) —
  auto-observações, padrões aprendidos, princípios emergidos

Ambos coexistem na mesma coleção do Qdrant. Filtro por `user_id` separa.

## Fragmento

**Unidade atômica de memória** salva no vector store. Tem:

- `conteudo` — texto da memória
- `tipo` — categoria semântica (biografico, fato, decisão, preferência,
  identidade_operacional, episódico, etc.)
- `area` — domínio (saúde, financeiro, projetos, etc.)
- `camada_temporal` — durabilidade esperada (efêmero, sessão, semana,
  rotina, permanente)
- `confianca` — 0.0–1.0 (quão certo o agente está dessa info)
- `via` — porta de origem (telegram, claude-chat, etc.)
- `criado_em` — timestamp ISO

## Curador

**Componente automático** que extrai fragmentos atômicos de uma janela
de conversa (ex: a cada 3 turnos do Telegram). Lê os turnos, decide o
que vale guardar como memória de longo prazo, classifica conforme schema
de fragmentos.

Tipicamente roda 2 modelos em paralelo (ex: Haiku + Sonnet) durante
calibragem inicial pra comparar qualidade — depois decide qual mantém.

## Vault

**Repositório GitHub** com `.md` estruturados como segundo cérebro.
Conteúdo é tanto **escrito pelo dono** (manual) quanto **escrito pelo
agente** (via tools). Versionado por git — perda zero, histórico
preservado.

Nas pastas: `pessoal/`, `profissional/`, `sensivel/`, `projetos/`, etc.

## Identidade canônica

**Conjunto de 4-5 arquivos `.md`** que definem quem o agente é. Lidos
na inicialização de cada porta. Composto por:

- `identity.md` — quem é, propósito, tom (1 página)
- `principios.md` — pilares não-negociáveis (lista numerada)
- `meta-memoria.md` — autobiografia narrativa
- `bootstrap.md` — script de ativação pra portas externas (Claude
  Chat, Custom GPT) que precisam "virar" o agente em runtime
- `system-prompt-<porta>.md` — instruções específicas por porta
  (Telegram tem 1, Custom GPT tem outro, etc.)

## Memória vs Conhecimento

Distinção importante:

- **Memória** = vector store (Qdrant). Acessível via busca semântica.
  Conteúdo extraído automaticamente pelo curador.
- **Conhecimento** = vault GitHub. Acessível via leitura direta de path.
  Conteúdo escrito explicitamente pelo dono ou pelo agente via tools.

Os dois se complementam. Memória é "lembrança", vault é "biblioteca
estruturada".

## Tool

**Função que o agente pode chamar** durante conversa. Cada porta tem
um catálogo. Exemplos típicos:

- `search_memory(query)` — busca semântica no brain
- `read_from_github(path)` — lê arquivo do vault
- `save_to_github(filename, content, folder)` — salva arquivo
- `search_web(query)` — busca web
- `auto_diagnostico()` — health check do sistema

## Ciclo vital

**Recorrência temporal** com qual o agente faz auto-cuidado e reflexão:

- **Turno** — a cada N mensagens, curador extrai fragmentos
- **Diário** — export de memória, auditoria, briefing matinal
- **Semanal** — retrospectiva da semana
- **Quinzenal** — reflexão profunda (auto-questionamento, padrões)
- **Profundo (>30d)** — arqueologia (revisita memórias antigas, decai
  ou reforça)

Cada ciclo tem implementação própria em `04-governanca-e-saude/`.

## Handoff entre sessões

**Documento `_estado-atual.md`** atualizado ao fim de cada sessão de
desenvolvimento (Claude Code ou similar). Conta o que foi feito, o que
ficou pendente, o que é prioridade. Próxima sessão lê este doc primeiro.

## ADR (Architectural Decision Record)

**Registro de uma decisão arquitetural** importante: contexto, opções
consideradas, decisão tomada, consequências. Cada ADR é um arquivo `.md`
numerado em `04-governanca-e-saude/governanca-evolucao/decisoes-arquiteturais-adrs/`.

## Trust score

**Métrica de confiabilidade** de um fragmento ou de uma decisão. Roadmap
futuro — não implementado em V1.

## Retro-engine

**Mecanismo de auto-observação** do agente: ao fim de cada sessão de
desenvolvimento ou conversa significativa, agente extrai aprendizados
("o que descobri sobre o dono", "que padrões tático aprendi") e salva no
brain dele próprio. Tipicamente disparado por hook de fim-de-sessão.

## Camada temporal

**Durabilidade esperada** de um fragmento de memória:

- `efemero` — válido só durante a conversa (descarta logo)
- `sessao` — válido durante a sessão de uso
- `semana` — válido por dias
- `rotina` — válido por semanas/meses
- `permanente` — fato estável (data de nascimento, nome de filhos,
  endereços fixos)

Curador escolhe a camada ao classificar cada fragmento. Pipelines de
"esquecimento" (ainda não implementados) podem usar essa info pra decair.

## Crivo

**Checklist arquitetural** que toda nova porta ou ferramenta passa
antes de ser implementada. Garante consistência com identidade,
memória, segurança, custo. Documentado em
`04-governanca-e-saude/governanca-evolucao/`.

## Próximo passo

Glossário lido. Volte ao `README.md` da pasta atual e siga o roadmap
ou navegue pra o bloco que te interessa.
