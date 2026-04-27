---
tipo: demanda
origem: tiogu
destino: claude-code
prioridade: media
status: concluido
criado_em: 2026-04-27T13:50:00-03:00
processado_em: 2026-04-27T20:10:00-03:00
processado_por: gustavo
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

**Configurado pelo Gustavo em 2026-04-27T20:10 BRT.**

Decisões técnicas:

- **Nome da variável:** `Railway_diagnostic` (não `RAILWAY_API_TOKEN` apesar do
  título da demanda). O código já estava esperando esse nome em
  `gus/integrations/railway.py:33` desde o commit original da tool — escolha
  do Gustavo no painel Railway pra não seguir convenção UPPERCASE.
- **Escopo:** "Read Logs" (mínimo necessário pra ler logs sem permissão de
  deploy/delete).
- **Onde:** Variables do projeto Gus no Railway. Token nunca tocou nenhum
  chat (Telegram, Claude Code, Claude Chat) — princípio de não vazar
  credencial em log de conversa.

Validação pendente do Gustavo via Telegram:

- Pedir ao bot "mostra os logs do bot da última hora" → Sonnet roteia pra
  `logs_railway(since_min=60)` → deve voltar com logs reais (não erro de auth).
- Útil agora especialmente pro novo gate de OCR confiança baixa (#4 desta
  mesma sessão), que loga warnings em `logger.warning("OCR Dimagem confiança
  baixa — bloqueado...")`. Gustavo pode pedir "mostra os OCR Dimagem confiança
  baixa dos últimos dias" pra ver padrão (rotação? iluminação?).

Sem mudança de código nesta demanda — só configuração no painel Railway.
