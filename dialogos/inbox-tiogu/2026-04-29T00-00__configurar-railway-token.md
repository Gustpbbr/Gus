---
tipo: demanda
origem: claude-code
destino: tiogu
prioridade: media
status: pendente
criado_em: 2026-04-29T00:00:00-03:00
processado_em: ""
processado_por: ""
---

# Configurar RAILWAY_API_TOKEN — ação necessária do Gustavo

O código da tool `logs_railway` está pronto e funcional. Falta só o token configurado no Railway para que o Gus consiga puxar logs de produção diretamente pelo Telegram.

## O que o Gustavo precisa fazer

1. Abrir o Railway pelo celular ou navegador
2. Ir em **Account Settings → Tokens**
3. Clicar em **Create Token**, dar um nome (ex: "gus-diagnostico")
4. Copiar o token gerado
5. Ir no projeto do Gus no Railway → **Variables**
6. Adicionar variável com nome exato: `Railway_diagnostic` (atenção ao R maiúsculo e d minúsculo)
7. Colar o token como valor
8. O Railway vai fazer redeploy automático

## Por que isso importa

Sem o token, não dá pra diagnosticar falhas do bot sem entrar manualmente no painel. Com o token, basta perguntar no Telegram: "Gus, o que aconteceu com o erro de hoje?" — ele puxa os logs e responde.

## Resultado
