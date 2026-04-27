---
tipo: demanda
origem: tiogu
destino: claude-code
prioridade: media
status: pendente
criado_em: 2026-04-27T13:50:00-03:00
processado_em: ""
processado_por: ""
---

# Configurar RAILWAY_API_TOKEN para logs acessíveis via Gus

## Contexto

A tool `logs_railway` do Gus retorna erro de token não configurado. Sem logs, não é possível diagnosticar falhas de OCR, erros de Mem0, latências ou qualquer comportamento anormal do bot em produção.

## Ação necessária

1. Gerar `RAILWAY_API_TOKEN` no painel do Railway (Account Settings → Tokens)
2. Adicionar como variável de ambiente no Railway (`RAILWAY_API_TOKEN`)
3. Verificar se a tool `logs_railway` está usando o token corretamente no código

## Critério de sucesso

- `logs_railway(filtro="error", since_min=60)` retorna logs reais do bot
- Diagnóstico de erros passa a ser possível via Gus sem acesso manual ao painel Railway

## Resultado
