# GUS — Template: Extração de Contexto de Sessões Antigas

**Tipo:** prompts-templates  
**Data:** 2026-04-09  
**Quando usar:** antes de ligar o Gus — alimentar memória histórica  
**Destino:** Google Drive → MemPalace → Mem0

---

## Por que fazer isso

O Gus vai "lembrar" de conversas que aconteceram antes dele existir. Com os MDs das sessões antigas indexados no MemPalace, ele terá contexto histórico completo desde o primeiro dia — incluindo decisões, alternativas descartadas, evolução de projetos e seu estilo de raciocínio.

---

## Ordem de execução

1. Abrir cada sessão antiga relevante
2. Colar o prompt abaixo
3. Claude gera o MD estruturado
4. Você salva no Google Drive na pasta correta
5. Drive for Desktop sincroniza localmente
6. Rodar `mempalace mine` para indexar
7. Itens de identidade relevantes → alimentar Mem0 manualmente ou via Gus

---

## Prompt padrão — colar em cada sessão antiga

```
Analise essa conversa completa do início ao fim e gere um MD estruturado com:

## MÉTRICAS DA SESSÃO
- Data aproximada (se identificável)
- Duração estimada da conversa
- Token count aproximado
- Projetos discutidos: [listar]
- Tipo de sessão: exploração / implementação / decisão / planejamento / debugging

## DECISÕES IMPORTANTES
Para cada decisão tomada:
- O que foi decidido
- Por que (raciocínio)
- Alternativas que foram consideradas e descartadas
- Status atual: ainda válida / superada / pendente revisão

## PROJETOS E ESTADO
Para cada projeto mencionado:
- Nome do projeto
- O que avançou nessa sessão
- O que ficou pendente
- Próximos passos identificados

## CONTEXTO E APRENDIZADOS
- Insights importantes que emergiram
- Problemas encontrados e como foram resolvidos
- Padrões de raciocínio do Gustavo identificados
- Conexões com outros projetos

## PARA O GUS
O que o Gus precisa saber sobre essa conversa para ter contexto completo:
- Resumo em 3-5 linhas
- Tags: [projeto] [tema] [tipo]
- Prioridade do contexto: alta / média / baixa

Formato: MD limpo, estruturado, pronto para salvar no Segundo Cérebro.
Nome sugerido para o arquivo: [projeto]-sessao-[data]-[tema-curto].md
```

---

## Onde salvar no Google Drive

Criar estrutura de pasta no Drive:

```
Segundo_Cerebro/
└── sessoes-historicas/
    ├── phronesis-bench/
    ├── mgx/
    ├── olho-vivo/
    ├── dimagem/
    ├── ter/
    ├── axon/
    └── geral/
```

Cada MD vai para a pasta do projeto principal discutido.

---

## Sessões prioritárias para extrair

Começar pelas mais ricas em decisões e contexto:

**Alta prioridade:**
- [ ] Aba "Trabalhando com múltiplos projetos" (a maior — 1M tokens)
- [ ] Sessões do Phronesis-Bench com resultados e decisões arquiteturais
- [ ] Sessões do MGX com definição da metodologia
- [ ] Sessões do Olho Vivo com backlog e arquitetura

**Média prioridade:**
- [ ] Sessões do Dimagem (formulário, fluxos)
- [ ] Sessões do TER com Kai
- [ ] Sessões do Axon

**Baixa prioridade:**
- [ ] Sessões exploratórias sem decisões concretas
- [ ] Sessões de debugging resolvido

---

## Prompt complementar — para sessões muito longas

Se a sessão for longa demais para analisar de uma vez:

```
Essa conversa é muito longa. Vou te pedir para analisar em partes.

Parte 1: analise apenas até [marco/tema].
Gere o MD parcial e me avise quando terminar.
Depois analisamos a próxima parte.

No final, consolide tudo num MD único.
```

---

## O que fazer com itens de identidade

Alguns MDs vão ter informações sobre o Gustavo que devem ir para o Mem0, não só para o MemPalace:

**Vai para o Mem0:**
- Valores e princípios que emergiram nas conversas
- Estilo de trabalho observado
- Preferências de comunicação
- Objetivos de longo prazo mencionados
- Pessoas importantes citadas

**Fica só no MemPalace:**
- Decisões técnicas de projetos
- Código e implementações
- Contexto específico de cada projeto

Depois da entrevista de boas-vindas, o próprio Gus pode ler os MDs e migrar o que for identidade para o Mem0 automaticamente.

---

## Métricas a registrar durante esse processo

Para o baseline do sistema de métricas:

```
Para cada sessão analisada, anotar:
- Token count aproximado da sessão original
- Número de projetos discutidos
- Número de decisões extraídas
- Tamanho do MD gerado (linhas)
```

Essa é a fonte do "antes" nas métricas comparativas do README.

---

## Prompt para consolidação final

Depois de extrair todas as sessões relevantes:

```
Tenho X MDs de sessões históricas salvos no Drive.
Gere um MD de índice consolidado com:

- Lista de todas as sessões extraídas
- Linha do tempo dos projetos
- Decisões mais importantes em ordem cronológica
- Estado atual de cada projeto baseado no histórico completo

Nome do arquivo: _indice-sessoes-historicas.md
```

Esse índice vai para a raiz do Segundo Cérebro — o Gus consulta ele quando precisa de visão histórica geral.

---

## Nota

Esse processo transforma o passado em memória estruturada. Conversas que estavam presas em abas gigantes — consumindo tokens sem valor — viram contexto permanente, pesquisável, acessível ao Gus em qualquer momento.

É a diferença entre ter um arquivo e ter uma memória.
