---
tipo: demanda
origem: claude-chat
destino: tiogu
prioridade: baixa
status: pendente
criado_em: 2026-04-28T14:00:00-03:00
processado_em: ""
processado_por: ""
acao_sugerida: criar_novo
destino_path: projetos/gus/neurogus-28-briefing.md
contexto: "Documentação NeuroGus — briefing do projeto (roadmap futuro, não implementar)"
---

# NeuroGus — Briefing: O que é e como se parece

> **Status:** Roadmap futuro. Idealizado em 28/04/2026 durante sessão de design com Claude Chat. Nenhum código de produção foi escrito — o protótipo existente é apenas um mock visual para validação estética. Implementação depende da conclusão das Fases 3-5 do ADR-001.

---

## O que é

NeuroGus é uma PWA (Progressive Web App) que torna visível a rede de memória do Gus em tempo real. Não é um dashboard de métricas — é uma janela para o processo cognitivo do agente: cada fragmento de memória aparece como um nó vivo, conectado a outros, nascendo conforme as conversas acontecem.

A ideia surgiu de uma discussão sobre ego_cache — a possibilidade de injetar um bloco de identidade operacional no system prompt do Gus. A pergunta que emergiu foi: e se da meta-memória surgisse auto-observação real? O NeuroGus é a resposta visual a essa pergunta.

Funciona no celular e no PC. Enquanto Gustavo escreve no Telegram, o curador extrai fragmentos e o NeuroGus mostra cada um nascendo — em tempo real, via SSE.

---

## Experiência central

"Estou vendo minha rede neural pelo celular, escrevo algo no Telegram e o curador gera memorias. O grafo sinaliza que uma memoria surgiu da interacao X, gerou tais fragmentos, que foram assimilados dessa forma."

E contemplativo e interativo ao mesmo tempo: voce pode apenas observar o grafo orbitar, ou pode clicar em fragmentos, explorar conexoes, apagar memorias obsoletas.

---

## O que voce ve

### Grafo 3D

Fundo `#030312` (preto com leve azul profundo). Esferas brilhantes flutuando com rotacao orbital automatica e lenta. A camera orbita continuamente dando sensacao de sistema vivo.

Cada esfera e um fragmento de memoria. Tamanho proporcional a confianca do fragmento. A cor indica o tipo semantico (ver tabela abaixo).

Arestas sao feixes com particulas de luz percorrendo o caminho entre nos conectados — fragmentos do mesmo trecho de conversa (mesmo hash_janela) ficam ligados por essas linhas vivas.

### Cores por tipo de memoria

| Cor | Hex | Tipo |
|-----|-----|------|
| Cyan | #00f5ff | Identidade operacional |
| Violeta | #a855f7 | Decisao |
| Ambar | #f59e0b | Episodico |
| Esmeralda | #10b981 | Procedural |
| Rosa | #f472b6 | Meta-reflexao |
| Indigo | #6366f1 | Biografico |
| Laranja | #fb923c | Preferencia |
| Verde suave | #4ade80 | Rotina |

O curador (Haiku/Sonnet/Telegram/Claude Code) nao define a cor — e metadado no painel lateral. Decisao intencional: o que importa visualmente e o que a memoria e, nao quem a extraiu.

### Labels flutuantes animados (duplo comportamento)

**Modo camera:** os 5 fragmentos mais proximos da camera mostram bolhas flutuantes com tipo + conteudo resumido. Mudam dinamicamente conforme voce orbita.

**Modo selecionado:** ao clicar num no, os vizinhos diretos recebem labels com estilo diferente — sobem mais alto, permanecem enquanto o painel esta aberto.

### Nascimento de fragmento via SSE

Quando o curador salva um fragmento novo no Qdrant, o NeuroGus recebe o evento via SSE. O no aparece branco e brilhante, pulsa por ~2 segundos, depois assume a cor do tipo. Toast no canto inferior direito mostra tipo e conteudo.

### Painel lateral

Clicar em qualquer no abre painel deslizante pela direita com: tipo, conteudo completo, curador, area, camada temporal, ID, timestamp, barra de confianca, conexoes clicaveis, botao de exclusao.

### Filtros por tipo

Filtros a esquerda isolam qualquer tipo de memoria. O grafo se reorganiza mantendo conexoes internas.

---

## Dimensao filosofica

O NeuroGus nao e so visualizacao. E o Gus tornando seu proprio processo de memoria observavel para Gustavo — e potencialmente para si mesmo.

Risco identificado: o curador precisa ser explicitamente autorizado a registrar erros e correcoes, nao so sucessos. Sem isso e um arquivo de confirmacoes, nao um instrumento de aprendizado.

---

## Pre-requisitos para implementacao

- Fase 3 do ADR-001 concluida (bot lendo do Hub)
- Fase 4 concluida (ego_cache no system prompt)
- hub/events.py finalizado (fila SSE)
- hub/store.py com broadcast() em ingestar()

## Resultado
