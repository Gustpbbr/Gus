---
criado_em: 2026-04-18
tipo: documentacao-projeto
---

# Gus — Decisões e Opções Descartadas

Registro de alternativas consideradas e por que foram descartadas. Útil para evitar re-discussões e para novas sessões entenderem o raciocínio.

## Arquitetura e design

### NamedTuple para preços dos modelos
- **Considerado**: usar NamedTuple em vez de dict para MODEL_PRICING
- **Descartado porque**: dict é mais simples, legível, e não justifica a abstração extra para 3 entradas estáticas
- **Escolhido**: dict simples com lookup por substring do nome do modelo

### Dict registry para tools
- **Considerado**: registrar tools em um dicionário para dispatch automático em vez de if/elif
- **Descartado porque**: são apenas 3 tools, o if/elif é mais legível e explícito
- **Escolhido**: if/elif direto no tools.py

### Reuso de httpx.AsyncClient
- **Considerado**: criar client global reutilizável em vez de instanciar por chamada
- **Descartado porque**: adiciona complexidade de lifecycle management; as chamadas são esporádicas, não alta frequência
- **Escolhido**: instanciar por chamada com `async with`

### Mem0 self-hosted
- **Considerado**: rodar Mem0 localmente em vez de usar API hosted
- **Descartado porque**: custo de infra, manutenção, e o Gustavo não administra servidores. API hosted é mais prática para um usuário solo
- **Escolhido**: Mem0 hosted API (free tier suficiente para uso pessoal)

## Deploy e infra

### Webhook vs polling (Telegram)
- **Considerado**: usar webhook em vez de polling para receber updates do Telegram
- **Descartado porque**: polling é mais simples, não precisa de URL pública, e para bot single-user a latência extra é irrelevante
- **Escolhido**: polling (run_polling no python-telegram-bot)

### GitHub Actions de terceiros para Drive sync
- **Considerado**: usar Actions prontas do marketplace para sincronizar com Google Drive
- **Descartado porque**: Actions existentes não fazem conversão .md → Google Docs (apenas upload de arquivo). Precisávamos de conversão nativa para que todas as IAs leiam
- **Escolhido**: script Python customizado com google-api-python-client

### Heroku em vez de Railway
- **Considerado**: Heroku como plataforma de deploy
- **Descartado porque**: free tier do Heroku foi eliminado; Railway tem free tier funcional e deploy mais simples com Dockerfile
- **Escolhido**: Railway

### Supabase como banco de dados
- **Considerado**: usar Supabase/PostgreSQL para armazenar memórias estruturadas
- **Descartado porque**: Mem0 + GitHub .md já cobrem as necessidades. Banco relacional adicionaria complexidade sem benefício claro para um sistema pessoal
- **Escolhido**: Mem0 (memória relacional) + GitHub .md (conhecimento estruturado)

## Features

### Multi-modelo no mesmo bot
- **Considerado**: permitir que Gustavo escolha entre Opus/Sonnet/Haiku por mensagem
- **Status**: parcialmente implementado (CLAUDE_MODEL é configurável), mas sem comando /modelo no bot
- **Decisão**: manter como variável de ambiente. Se necessário, adicionar comando depois

### Whisper local (whisper.cpp)
- **Considerado**: rodar transcrição de áudio localmente no container Railway
- **Descartado porque**: consome recursos significativos, modelo grande para container free tier
- **Escolhido**: Whisper API (OpenAI) quando implementado — custo baixo, qualidade superior em pt-BR

### Langchain/LlamaIndex como framework
- **Considerado**: usar framework de orquestração de LLMs
- **Descartado porque**: o Gus tem 3 tools e fluxo linear. Frameworks adicionam dependências pesadas e abstração desnecessária para a simplicidade do sistema
- **Escolhido**: chamada direta à API Anthropic com loop de tool use manual

### Sistema de plugins
- **Considerado**: arquitetura de plugins para adicionar tools dinamicamente
- **Descartado porque**: over-engineering para um bot pessoal. Novas tools são adicionadas editando tools.py direto
- **Escolhido**: tools hardcoded no tools.py

### Vector database local
- **Considerado**: ChromaDB ou similar para busca semântica nos .md
- **Descartado porque**: Mem0 já faz busca semântica nas memórias, e os .md são lidos por path (não precisam de busca vetorial)
- **Escolhido**: Mem0 para semântica, GitHub para leitura direta

## Processo

### Testes unitários completos antes do deploy
- **Considerado**: cobertura de testes antes de colocar em produção
- **Descartado como bloqueio**: bot pessoal single-user, risco baixo. Testes podem ser adicionados incrementalmente
- **Escolhido**: deploy primeiro, auto-teste diário como safety net (Fase 2)

### CI/CD completo (lint, type check, testes)
- **Considerado**: pipeline completo de CI
- **Descartado como pré-requisito**: adiciona atrito sem benefício proporcional para projeto pessoal
- **Escolhido**: deploy direto no Railway, CI pode ser adicionado depois se necessário

## Lições para referência futura

1. **Simplicidade vence**: para bot pessoal, cada abstração deve justificar sua existência
2. **Hosted > self-hosted**: quando o usuário não gerencia infra, serviços managed são sempre melhores
3. **Código direto > frameworks**: 7 arquivos Python fazem o que frameworks fariam com 30 dependências
4. **Deploy primeiro, robustez depois**: funcionar é pré-requisito de qualquer melhoria

Relacionado: [[gus-01-visao-geral]], [[gus-02-implementado]], [[gus-04-seguranca-protecao]]
