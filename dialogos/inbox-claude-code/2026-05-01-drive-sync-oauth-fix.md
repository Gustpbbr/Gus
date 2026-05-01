---
tipo: demanda
origem: gustavo
destino: claude-code
prioridade: media
status: pendente
criado_em: 2026-05-01T00:12:00-03:00
processado_em: ""
processado_por: ""
acao_sugerida: investigar
destino_path: .github/scripts/sync_to_drive.py
contexto: "Workflow sync-to-drive parou de empurrar arquivos GitHub→Drive. Hipótese: refresh token OAuth expirado (Google Testing apps expiram em 7 dias). Decidir entre reset OAuth (paliativo) ou Service Account (definitivo)."
---

# Demanda — Drive sync parado, decidir fix OAuth vs Service Account

## Problema

O workflow `.github/workflows/sync-to-drive.yml` (script
`.github/scripts/sync_to_drive.py`) deveria empurrar mudanças do GitHub
pro Google Drive (pasta `Gus-Sync`) periodicamente. Em algum momento
parou de funcionar.

**Sintoma:** arquivos `.md` no Drive ficam stale (versão antiga). Claude
Chat lê do Drive e fica com bootstrap desatualizado, perde contexto novo.

**Hipótese principal:** refresh token OAuth do Google **expirou**. Apps
Google em modo "Testing" expiram refresh tokens em 7 dias (apps em modo
"Production" não expiram, mas exigem verificação Google).

## Diagnóstico inicial

Antes de implementar, confirmar:

1. **Olhar logs do workflow:** vai em GitHub Actions → último run do
   `sync-to-drive.yml`. Erro provável: `invalid_grant`, `Token has been
   expired or revoked`, `unauthorized_client`.
2. **Verificar status do app no Google Cloud Console:** se "Testing",
   confirma a hipótese. Se "Production", investigar outras causas.
3. **Conferir secret `GOOGLE_OAUTH_REFRESH_TOKEN`** existe e foi setado
   no GitHub.

## Opções

### Opção 1 — Reset OAuth (paliativo, rápido)

Gustavo refaz o flow OAuth no celular (script local que abre browser,
autoriza, copia refresh token), atualiza secret
`GOOGLE_OAUTH_REFRESH_TOKEN` no GitHub.

- **Trabalho:** 10min Gustavo + 0 código
- **Pró:** funciona já, sem refator
- **Contra:** vai expirar de novo em 7 dias. Loop de manutenção infinito.

### Opção 2 — Service Account (definitivo, recomendado)

Cria Service Account no Google Cloud Console (gratuito, conta de serviço
gerenciada). Baixa JSON key, vira secret `GOOGLE_SERVICE_ACCOUNT_JSON` no
GitHub. Compartilha pasta `Gus-Sync` no Drive com o email do Service
Account (`<nome>@<projeto>.iam.gserviceaccount.com`).

Atualiza `sync_to_drive.py`:
```python
# Antes
from google.oauth2.credentials import Credentials
creds = Credentials.from_authorized_user_info(...)

# Depois
from google.oauth2 import service_account
creds = service_account.Credentials.from_service_account_info(
    json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]),
    scopes=["https://www.googleapis.com/auth/drive"],
)
```

- **Trabalho:** ~30min código + 10min Google Console + Gustavo aprovar
  share da pasta
- **Pró:** **não expira jamais.** Solução definitiva.
- **Contra:** Service Account é entidade separada — Gustavo não vê os
  files dela como "compartilhados" no app Drive normal (só via API)

### Opção 3 — Aposentar Drive sync

Claude Chat passa a ler 100% do Hub via MCP (que agora funciona). Drive
deixa de ser fonte. `gus-bootstrap.md` etc. ficam só no GitHub, Claude
Chat lê via `read_repo_file` do MCP gus-hub.

- **Trabalho:** desligar workflow + atualizar bootstrap pra mencionar
  fontes via MCP
- **Pró:** simplifica arquitetura, remove ponto de falha
- **Contra:** Claude Chat perde "Project knowledge" automático do Drive.
  Precisa começar conversa lendo o repo via MCP toda vez.

## Recomendação inicial

**Opção 2 (Service Account).** Resolve definitivo, manutenção zero.

Opção 1 vale como **bridge** se Gustavo quiser ver o sync rodar amanhã
antes de migrar (faz reset → roda 1 dia → migra pra SA depois).

Opção 3 vale considerar **só** se a aba nova confirmar que Claude Chat
funciona 100% via MCP sem precisar de Drive.

## Critério de decisão

Antes de codar:

1. Confirmar com Gustavo qual opção (1, 2 ou 3)
2. Se Opção 2: Gustavo precisa criar o Service Account no Google Cloud
   Console (instruir passo a passo) e baixar o JSON key — só depois disso
   o Code pode mexer no código
3. Se Opção 1: instruir Gustavo a refazer o OAuth flow

## Onde olhar

- `.github/workflows/sync-to-drive.yml` — workflow
- `.github/scripts/sync_to_drive.py` — script de sync
- Logs últimos runs em GitHub Actions
- Secret atual: `GOOGLE_OAUTH_REFRESH_TOKEN` (se Opção 1) ou criar novo
  `GOOGLE_SERVICE_ACCOUNT_JSON` (se Opção 2)

## Resultado esperado

Uma das 3:
1. PR implementando Service Account migration + instruções pra Gustavo
   setar o secret
2. Reset OAuth registrado nesta demanda como `status: concluido` (sem PR
   se for só renovação de token)
3. Workflow sync desligado + bootstrap atualizado (Opção 3)
