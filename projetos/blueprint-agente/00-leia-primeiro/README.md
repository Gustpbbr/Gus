# Blueprint Agente Pessoal Multi-Portas

Guia autocontido pra construir um agente pessoal multi-portas do zero,
em qualquer repositório limpo. Foco em **identidade canônica + memória
persistente + portas de I/O + automação de ciclos**.

> **Antes de começar, leia esta pasta inteira** (5 arquivos curtos).
> Sem isso o resto da árvore parece complicado demais; com isso, fica
> claro o que vem antes do quê.

## Ordem de leitura

1. **`visao-geral.md`** — o que esse blueprint constrói, pra quem,
   por quê. Decida aqui se faz sentido pra teu caso.
2. **`pre-requisitos.md`** — contas externas necessárias (Anthropic,
   Qdrant Cloud, GitHub, Railway, Telegram), custos esperados,
   conhecimento mínimo.
3. **`passo-a-passo-resumido.md`** — roadmap em 7 etapas, do "decidir
   nome do agente" até "primeira conversa funcional no Telegram".
4. **`glossario.md`** — porta, brain, fragmento, curador, ciclo,
   handoff. Termos que o resto do blueprint usa sem repetir definição.
5. Voltar pra cá e escolher o próximo bloco conforme onde você está
   no roadmap.

## Como o blueprint está organizado

```
00-leia-primeiro/        ← onde você está agora
01-conteudo-do-usuario/  ← pastas pra organizar dados pessoais e profissionais
02-identidade-e-memoria/ ← QUEM o agente é + COMO ele lembra
03-interface-e-operacao/ ← portas de I/O + tools + protocolo entre portas
04-governanca-e-saude/   ← automações + observabilidade + decisões arquiteturais
05-transversais/         ← T1–T8: configs, deploy, sync, segurança, etc.
06-servicos-externos-e-interdependencias/  ← inventários e diagramas
templates/               ← código mínimo (Dockerfile, requirements, bot.py)
```

Cada pasta tem `README.md` próprio explicando o sub-conteúdo. Leia
sequencialmente do **02** ao **06** se for primeira vez. **05** e **06**
podem ser consultados sob demanda.

## Quem implementa de fato

Esse blueprint é descritivo. Quem **executa** é a IA (Claude Code,
GitHub Copilot, Cursor, etc.) com você no loop revisando.

O **dono do agente** (você) toma decisões em pontos marcados com
`{{PLACEHOLDER}}` ao longo dos templates. A IA preenche o resto e
implementa.

## Como contribuir / atualizar este blueprint

Se você implementou um agente seguindo este guia e descobriu **gaps**
ou **passos que faltavam**, atualize o documento correspondente.
Blueprint vivo é melhor que blueprint perfeito.

## Estado / versionamento

| Versão | Data | Mudança |
|---|---|---|
| 0.1 (rascunho) | 2026-04-28 | Estrutura inicial, esqueleto de pastas |

## Aviso

Este blueprint **não inclui escolhas de personalidade** do agente —
isso é decisão tua, documentada em `02-identidade-e-memoria/identidade-canonica/`.
Aqui só descrevemos o **arcabouço**.
