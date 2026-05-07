# apps-script/ — Gus Sync (GitHub ⇄ Drive)

Cópia versionada do código que roda no Google Apps Script.

**Fonte da verdade:** projeto "Gus Sync (GitHub ⇄ Drive)" em
https://script.google.com (conta `gustavo.pratti@gmail.com`).

## Por que existe

Apps Script roda dentro do Google com identidade do owner do projeto
(Gustavo) → autentica como Gustavo no Drive (sem Service Account, sem
WIF, sem OAuth refresh token externo). Resolve definitivamente o
problema de quota da SA que bloqueava `CREATE` de arquivos novos com
o approach anterior (PR #76).

## Arquivos

- `Code.gs` — entry points (`safeSyncGitHubToDrive`, `safeSyncDriveToGitHub`),
  `setupCheck`, `resetState`
- `GitHubAPI.gs` — wrappers GitHub Contents/Compare/Trees API via PAT
- `DriveSync.gs` — DriveApp helpers + lógica inbox/mirror (paridade com
  `.github/scripts/import_from_drive.py` e `sync_to_drive.py`)
- `Notifications.gs` — `sendTelegramAlert()` via bot @Tiogubot

## Workflow de edição

Sem CI/CD nessa direção. Disciplina manual:

1. Faz mudança aqui no repo (commit no Git)
2. Abre Apps Script Editor
3. Cola conteúdo do arquivo modificado (Ctrl+A, Ctrl+V)
4. Salva (Ctrl+S)

Trade-off aceito em troca de zero infra extra (sem `clasp`, sem deploy
pipeline). Se a fricção virar problema real, migra pra `clasp` depois.

## Script Properties (configurar no Editor)

Obrigatórios:

| Property | Valor |
|---|---|
| `GITHUB_TOKEN` | PAT clássico, scope `repo`, sem expiração |
| `GITHUB_OWNER` | `Gustpbbr` |
| `GITHUB_REPO` | `Gus` |
| `GITHUB_BRANCH` | `main` |
| `DRIVE_ROOT_FOLDER_ID` | ID da pasta `Gus-Sync` no Drive |

Opcionais:

| Property | Valor |
|---|---|
| `TELEGRAM_BOT_TOKEN` | token do bot @Tiogubot (pra alertas em failure) |
| `TELEGRAM_CHAT_ID` | chat ID pessoal do Gustavo |

State automático (não setar manualmente):

| Property | Quando preenchida |
|---|---|
| `LAST_SYNCED_SHA` | Após cada sync GH→Drive completar |
| `LAST_DRIVE_SCAN_AT` | Após cada sync Drive→GH completar |
| `GH_PENDING_FILES` | Fila pendente quando exec estoura 4min |
| `TARGET_HEAD` | SHA alvo durante batch incompleto |

## Triggers (configurar no Editor)

Apps Script Editor → ⏰ Triggers → + Add Trigger:

1. **`safeSyncGitHubToDrive`** — Time-driven, Minutes timer, every 15 minutes
2. **`safeSyncDriveToGitHub`** — Time-driven, Minutes timer, every 15 minutes

Apps Script não permite offset entre triggers. Os 2 podem rodar próximos.
A idempotência (comparação byte-a-byte antes de PUT no GitHub e no Drive)
cobre o caso de ambos rodarem no mesmo minuto.

## Setup inicial

1. **Criar projeto Apps Script:** https://script.google.com → New project
2. **Renomear:** "Gus Sync (GitHub ⇄ Drive)"
3. **Configurar Script Properties** (Project Settings → Script Properties)
4. **Colar os 4 `.gs`** do repo no Editor (Files → criar 4 scripts com os
   nomes deste README e colar conteúdo)
5. **Rodar `setupCheck()` manual** pra validar Properties + auth + APIs:
   - Editor → dropdown "Select function" → `setupCheck` → Run
   - Aceita autorização de Drive + External requests
   - Esperado no log: `GitHub OK`, `Drive OK`, `Telegram OK`
6. **Rodar `safeSyncGitHubToDrive()` manual** uma vez pra bootstrap:
   - Vai fazer batch de até 4min sincronizando
   - Repete até `GH_PENDING_FILES` ficar vazia (ou deixa o trigger fazer)
7. **Configurar 2 triggers** (passo "Triggers" acima)
8. **Validar:** após 30min, ver Apps Script Executions — deve ter pelo
   menos 1 run de cada função, ambas verde

## Comandos manuais úteis

No Editor, dropdown → escolhe função → Run:

- `setupCheck` — valida Properties + APIs sem alterar nada
- `resetState` — apaga `LAST_SYNCED_SHA` etc, força rebootstrap na próxima exec
- `safeSyncGitHubToDrive` — rodar manualmente um ciclo
- `safeSyncDriveToGitHub` — rodar manualmente um ciclo

## Casos edge cobertos

| Caso | Comportamento |
|---|---|
| Arquivo deletado no GitHub | Ignorado no Drive (deleção via `delete-drive-file.yml` manual) |
| Arquivo deletado no Drive | Ignorado no GitHub |
| Conflito (modificado simultâneo) | Last-writer-wins (idempotência protege contra loop) |
| Exec estoura 6min | Salva `GH_PENDING_FILES`, próxima exec retoma |
| Apps Script offline | Próxima exec pega tudo (state-based) |
| Frontmatter inválido em demanda | Move pra `processados-erro/<inbox>/` no Drive |
| Mirror de arquivo binário | Skip silencioso |

## Convivência com workflows GitHub Actions

Durante validação (1 semana), Apps Script roda em paralelo com workflows
antigos. Idempotência protege contra duplicação:

- Apps Script escreve no Drive → workflow antigo (se rodar) vê byte-idêntico → skip
- Apps Script escreve no GitHub → workflow antigo (se rodar) idem

Após 7 dias verde consistente, aposentar:

- `.github/workflows/sync-to-drive.yml`
- `.github/workflows/sync-to-drive-full.yml`
- `.github/workflows/import-from-drive.yml`
- `.github/scripts/sync_to_drive.py`
- `.github/scripts/import_from_drive.py`
- `.github/scripts/_drive_auth.py`
- Secrets relacionados ao Drive

Manter:
- `.github/workflows/delete-drive-file.yml` + script (admin manual, raramente usado — pode também migrar pro Apps Script depois)
- `.github/scripts/archive_completed.py` (decisão pendente — migrar lógica pra Apps Script ou manter cron GitHub)

## Limites Apps Script

- 6min por execução (4min de budget útil + 2min margem)
- 6h de execução total/dia (free tier — folgado)
- 20MB total quota Drive script (não relevante)
- 100 triggers/script (irrelevante)
- API Drive: 1B requests/dia (folgadíssimo)

Pra repo Gus (ordem de magnitude: ~1k arquivos .md, ~50 commits/dia),
nenhum limite chega perto de bater.
