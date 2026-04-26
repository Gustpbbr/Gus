---
tipo: demanda
origem: tiogu
destino: claude-code
prioridade: alta
status: pendente
criado_em: 2026-04-26T12:30:00-03:00
processado_em: ""
processado_por: ""
---

# Avaliar e configurar secrets do Google Drive

## Contexto
Temos 3 workflows que dependem de secrets do Google Drive para funcionar:
- `sync-to-drive.yml`
- `sync-to-drive-full.yml`
- `import-from-drive.yml`

Os 4 secrets necessários são:
- `DRIVE_ROOT_FOLDER_ID`
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_REFRESH_TOKEN`

Não consigo verificar via API se esses secrets já estão configurados no GitHub (a API não expõe valores nem confirma existência por segurança).

## Demanda
1. **Verificar** se os secrets já estão configurados no GitHub (Settings → Secrets → Actions)
2. Se **não estiverem**: avaliar o que é necessário para configurar (Service Account vs OAuth2, qual abordagem está implementada nos scripts)
3. Se **possível**: configurar os secrets e testar disparando `sync-to-drive.yml` manualmente
4. **Responder em** `dialogos/inbox-tiogu/` com o resultado — o Tiogu vai notificar o Gustavo automaticamente via Telegram

## Critério de sucesso
- Secrets configurados E `sync-to-drive.yml` rodando sem erro 403/auth
- OU relatório claro do que falta fazer manualmente (ex: precisa criar projeto no GCP, precisa de refresh token OAuth)
