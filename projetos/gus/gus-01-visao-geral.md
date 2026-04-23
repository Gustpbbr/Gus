---
tipo: documentacao-projeto
projeto: gus
parte: 1-de-7
atualizado: 2026-04-23
---

# Gus — Visão geral

Fonte de verdade para entender o que o Gus é e como as peças se encaixam. Se algum outro documento contradisser este, este vence.

## O que é o Gus

Gus é o agente pessoal do Gustavo Pratti de Barros. Não é um chatbot genérico — é um sistema com memória persistente, arquivo estruturado em Markdown e múltiplas portas de acesso que compartilham a mesma base de conhecimento.

O dono não programa. Toda implementação é feita por LLMs via conversa; o Gustavo valida e executa instruções passo a passo.

## Quem é o Gustavo

Pesquisador independente brasileiro, anestesiologista. Trabalha no Dimagem (clínica de anestesia) — sustento principal. Usa Claude (rigor e implementação), ChatGPT/Kai (criatividade), Gemini (organização), Kimi (pesquisa e frontend). Hipertireoidismo em tratamento com tapazol.

Projetos ativos de pesquisa: Phronesis-Bench, MGE/MGX, TER, Axon. Gus é o quinto projeto — a infraestrutura pessoal que sustenta os outros.

Comunicação: português brasileiro informal, direto, sem superlativos vazios. Crítica direta é bem-vinda.

## Arquitetura multi-portal

O Gustavo não acessa "o Claude" ou "o ChatGPT". Ele acessa **o Gus**, que tem várias portas de entrada compartilhando memória e arquivos.

| Porta         | Plataforma              | Função                                          | Status               |
|---------------|-------------------------|-------------------------------------------------|----------------------|
| Telegram      | Bot no Railway          | Captura rápida, foto, PDF, interação diária     | Código pronto        |
| Claude Code   | CLI/IDE com MCP         | Desenvolvimento, manutenção, memória via MCP    | MCP server pronto    |
| Claude Chat   | App/Web                 | Reflexão, análise longa, leitura do Drive       | Config pendente      |
| ChatGPT       | Custom GPT com Actions  | Voz, criatividade, ações via Mem0 + GitHub      | Planejado (Fase 3)   |
| Alexa         | Skill + Lambda AWS      | Mãos livres em casa, pedidos pontuais por voz   | Planejado (Fase 5)   |

## Camadas compartilhadas

O que faz todas as portas serem o mesmo Gus:

- **Mem0 (hosted API)** — memória relacional. Preferências, padrões, decisões, contexto pessoal. Todas as portas lêem e escrevem no mesmo `user_id = "gustavo"`.
- **GitHub (`Gustpbbr/Gus`)** — base de conhecimento em `.md` organizada por pasta.
- **Google Drive** — espelho dos `.md` como Google Docs via GitHub Action. Permite que qualquer IA com acesso ao Drive leia o conteúdo.
- **`gus/gus-identity.md`** — arquivo único de identidade, carregado por todas as portas. Contexto do Gustavo (compartilhado) + personalidade do Gus (só Telegram).

## Estrutura de pastas do repositório

```
pessoal/saude/          exames, consultas, historico-saude.md (mestre)
pessoal/financeiro/     extratos, resumo-financeiro.md (mestre)
pessoal/diario/         reflexões pessoais
dimagem/protocolos/     protocolos da clínica
dimagem/casos/          casos interessantes
dimagem/admin/          pendências administrativas
receitas/doces/         com subpastas (tortas, bolos)
receitas/salgadas/      com subpastas (massas, carnes)
esportes/treinos/       registros de treinos
esportes/evolucao.md    MD mestre
leituras/livros/
leituras/papers/
projetos/               phronesis-bench, mge, ter, axon, gus
capturado/links/        artigos salvos
capturado/ideias/       insights soltos
capturado/misc/
```

Nomenclatura: sem acentos, sem espaços, hífen para separar. Arquivos com data usam `[tipo]-[mes-abreviado]-[ano].md`. Arquivos atemporais usam nome descritivo. MDs mestres têm nome genérico sem data.

Wikilinks `[[nome-do-arquivo]]` conectam arquivos relacionados — compatível com Obsidian Graph View.

## Navegação

- [[gus-02-implementado]] — o que já está construído e funcionando
- [[gus-03-configuracao-manual]] — passo-a-passo do que o Gustavo executa pra ligar tudo
- [[gus-04-seguranca-protecao]] — proteções ativas e reforços planejados
- [[gus-05-portas-capacidades]] — Fases 3 e 5 (novas portas e recursos)
- [[gus-06-autonomia-acoes]] — Fase 4 (fila de ações no mundo real)
- [[gus-07-decisoes-descartadas]] — por que não fazemos X, Y e Z
