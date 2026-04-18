---
criado_em: 2026-04-18
tipo: documentacao-projeto
---

# Gus — Visão Geral

## O que é

Gus é um agente pessoal de IA do Gustavo Pratti de Barros. Funciona como um "segundo cérebro" com memória persistente, arquivo estruturado e múltiplas portas de acesso.

Não é um chatbot genérico — é um sistema que conhece o Gustavo, lembra de conversas anteriores, salva e recupera informações, e evolui com o uso.

## Arquitetura

```
              GUS (identidade + memória + arquivo)
              ┌─────────────────────────────────┐
              │  Mem0         → memória viva     │
              │  GitHub .md   → conhecimento     │
              │  gus-identity.md → identidade    │
              └──────────┬──────────────────────┘
                         │
         ┌───────────────┼───────────────────┐
         │               │                   │
    Telegram        Claude Code         Claude Chat
    (bot Railway)   (MCP: Mem0+GitHub)  (Project + Drive)
         │               │                   │
    captura rápida   desenvolvimento     reflexão longa
    foto/PDF/áudio   manutenção          análise
    personalidade    engenharia          leitura Drive
```

## Portas de acesso

| Porta | Plataforma | Função principal | Personalidade |
|-------|-----------|------------------|---------------|
| Telegram | Bot no Railway | Captura rápida, mídia, interação diária | Gus completo (informal, proativo) |
| Claude Code | CLI/IDE | Desenvolvimento, manutenção do sistema | Engenheiro com contexto |
| Claude Chat | App/Web | Reflexão, análise longa, conversa profunda | Contexto do Gustavo, sem forçar |
| ChatGPT (futuro) | Custom GPT | Criatividade, voz no carro, ações | Kai com memória do Gus |

## Camadas compartilhadas

- **Mem0** — memória relacional (preferências, padrões, decisões, contexto pessoal). Todas as portas lêem e escrevem no mesmo user_id.
- **GitHub (Gustpbbr/Gus)** — arquivos .md organizados por pasta. Base de conhecimento estruturada.
- **Google Drive** — espelho dos .md como Google Docs via sync automático. Permite que qualquer IA leia o conteúdo.
- **gus-identity.md** — arquivo único de identidade, carregado por todas as portas.

## Stack técnica

- **Linguagem**: Python 3.11+
- **Bot**: python-telegram-bot
- **LLM**: Claude API (Anthropic) com tool use
- **Memória**: Mem0 hosted API
- **Arquivo**: GitHub API (PyGithub)
- **Busca web**: DuckDuckGo (httpx)
- **Deploy**: Railway (container Docker)
- **Sync**: GitHub Actions (Drive sync, Mem0 export)
- **MCP**: Servidor Mem0 para Claude Code

## Concorrentes analisados

| Projeto | Stars | Diferença pro Gus |
|---------|-------|--------------------|
| Hermes Agent | 53k | Framework genérico, multi-plataforma. Gus é pessoal, opinado. |
| OpenClaw | 50k+ | Plataforma open-source de assistentes. Mais infra que identidade. |

Conclusão: existem frameworks robustos, mas nenhum é "agente pessoal com memória + arquivo + múltiplas portas". O diferencial do Gus é ser opinado e específico para um usuário.

## Filosofia

- Capacidade sem prudência é perigosa (phronesis aristotélica)
- O Gus não substitui o Gustavo — amplifica
- Cada porta tem seu propósito; nenhuma faz tudo
- Memória + arquivo = conhecimento durável, não só conversa efêmera

Relacionado: [[gus-identity]], [[gus-02-implementado]], [[gus-03-configuracao-manual]]
