---
tipo: demanda
origem: gustavo
destino: claude-code
prioridade: media
status: pendente
criado_em: 2026-05-07T11:35:00-03:00
processado_em: ""
processado_por: ""
acao_sugerida: investigar
destino_path: multiplo
contexto: "Validar que Apps Script Drive ⇄ GitHub está estável após 1 semana, e se OK, aposentar workflows e secrets antigos. Demanda agendada pra 2026-05-14 ou depois."
---

# Demanda — Validar Apps Script + aposentar workflows Drive antigos

> **Não processar antes de 2026-05-14.** Esta demanda foi criada em 07/05
> ao implantar o Apps Script bidirecional. Espera 1 semana de observação
> antes de aposentar a infra antiga.

## Contexto

Em 07/05/2026 migramos o sync Drive ⇄ GitHub de **GitHub Actions + OAuth/WIF**
pra **Google Apps Script bidirecional** (projeto `Gus Sync (GitHub ⇄ Drive)`).

Razão: OAuth refresh token expirava em 7 dias (modo "Testing") e WIF +
Service Account não consegue criar arquivos em conta Gmail pessoal (quota da
SA = 0). Apps Script roda dentro do Google com identidade nativa do Gustavo
— sem auth externa, sem expirar, sem quota.

Detalhes em `_estado-atual.md` (sessão 07/05) e `apps-script/README.md`.

## Critérios de validação (verificar dia 14/05 ou depois)

### 1. Apps Script Executions consistentemente verdes

- Abrir https://script.google.com → projeto **Gus Sync (GitHub ⇄ Drive)** → Executions
- Filtrar por status **Falha**
- **Critério OK:** menos de ~5 falhas em 7 dias, todas com causa identificada
  (rate limit transitório, quota momentânea, etc — não bug do código)
- **Critério ruim:** muitas falhas persistentes, especialmente em
  `safeSyncGitHubToDrive` ou `safeSyncDriveToGitHub`

### 2. Drive sempre fresco

- Abrir `Gus-Sync/dialogos/_bootstrap/gus-estado-atual.md` no Drive
- Comparar timestamp `gerado_em:` no frontmatter com `git log --oneline`
  do mesmo arquivo no GitHub
- **Critério OK:** Drive ≤ 30min atrás do GitHub
- Pode rodar `git log -- dialogos/_bootstrap/gus-estado-atual.md | head -5`
  pra ver últimos commits

### 3. Sem alertas Telegram de falha persistente

- Olhar o Telegram (@Tiogubot) procurando alertas tipo
  `❌ Apps Script GH→Drive falhou` ou `❌ Apps Script Drive→GH falhou`
- **Critério OK:** zero ou ≤2 alertas em 7 dias (e com causa identificada)

### 4. Loop de regressão extinto

- `git log origin/main --oneline | grep "^[a-f0-9]\{7\} mirror:" | head -10`
- **Critério OK:** sem commits `mirror: gus-estado-atual.md` alternando com
  `auto: estado atual` (era o sintoma do loop anterior)

## Se validação OK — aposentar infra antiga

Abrir PR removendo:

### Workflows GitHub Actions (5 arquivos)

```
.github/workflows/sync-to-drive.yml
.github/workflows/sync-to-drive-full.yml
.github/workflows/import-from-drive.yml
.github/workflows/archive-completed-demandas.yml  # decisão: migrar lógica pro Apps Script ou manter?
.github/workflows/delete-drive-file.yml  # admin manual, decidir manter ou aposentar
```

### Scripts Python (4 arquivos)

```
.github/scripts/sync_to_drive.py
.github/scripts/import_from_drive.py
.github/scripts/_drive_auth.py
.github/scripts/archive_completed.py  # depende decisão acima
.github/scripts/delete_drive_file.py  # depende decisão acima
```

### Secrets do GitHub (6+)

Settings → Secrets and variables → Actions, deletar:
- `GOOGLE_REFRESH_TOKEN`
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_SERVICE_ACCOUNT_JSON`
- `GCP_WIF_PROVIDER`
- `GCP_WIF_SERVICE_ACCOUNT`
- `DRIVE_ROOT_FOLDER_ID` (manter — Apps Script lê do próprio Properties, mas se
  tem outros workflows que usam, manter)

### Recursos no Google Cloud Console (opcional, pra limpeza)

Project `gus-drive-sync`:
- IAM → Service Accounts → desativar `gus-sync@gus-drive-sync.iam.gserviceaccount.com`
- IAM → Workload Identity Pools → desativar `github-pool`
- (não deletar — desativar é reversível)

### Atualizar `historico/get_token.py`

Esse arquivo tem CLIENT_ID + CLIENT_SECRET hardcoded. Como OAuth não vai mais
ser usado, pode ser deletado. Já estava em `historico/` (legacy).

### Branch `claude/drive-sync-cleanup`

Branch antiga com fixes pra workflows que vão ser deletados. Fechar PR sem
merge ou deletar branch.

## Decisões pendentes nesta revisão

| Decisão | Impacto |
|---|---|
| `archive_completed.py` — migrar lógica pro Apps Script ou manter? | Apps Script já trata `inbox-*/` (move pra `processados/`). Falta a parte de detectar `status: concluido` em arquivos JÁ no GitHub e movê-los pra `dialogos/archive/`. Se migrar, simplifica arquitetura. Se manter, tem que renovar OAuth pra esse workflow específico. |
| `delete_drive_file.py` — manter ou aposentar? | Workflow manual admin, raramente usado. Migrar pro Apps Script (função `deleteDriveFile` em Code.gs) é simples. |

## Onde olhar

- `apps-script/README.md` — doc setup completo
- `apps-script/Code.gs` — entry points
- `projetos/gus/_estado-atual.md` — sessão 07/05/2026 com contexto
- `projetos/gus/gus-26-status-consolidado.md` — status atualizado

## Resultado esperado

Uma das 2:
1. PR aposentando workflows + scripts + secrets antigos. Sistema 100%
   Apps Script. Atualizar `_estado-atual.md` e `gus-26` mencionando aposentadoria.
2. Se validação não passou: triar falhas específicas, fazer fixes pontuais,
   adiar aposentadoria por mais 1 semana.

Marcar esta demanda como `concluido` ao final.
