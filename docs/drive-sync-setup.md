# Drive Sync — Processo de Configuração

Documento o processo completo de configuração do sync GitHub → Google Drive, incluindo os bloqueios encontrados e como foram resolvidos.

---

## Objetivo

A cada push no `main` que altere arquivos `.md` de conteúdo, sincronizar automaticamente para o Google Drive como Google Docs, preservando a estrutura de pastas. Isso cria um espelho navegável do repositório no Drive — base para integração futura com Alexa via Google Drive nativo.

---

## Tentativa 1 — Service Account Key JSON

**Abordagem:** criar uma Service Account no Google Cloud, gerar uma chave JSON, armazenar como secret no GitHub Actions e usar no script Python.

**Bloqueio:** `iam.disableServiceAccountKeyCreation` — política de organização do Google que bloqueia criação de chaves de service account. Aplicada inclusive em contas Gmail pessoais (não só Workspace corporativo).

```
A criação da chave da conta de serviço está desativada
IDs das políticas da organização aplicadas: iam.disableServiceAccountKeyCreation
```

**Status:** descartada.

---

## Tentativa 2 — Workload Identity Federation (WIF)

**Abordagem:** usar o método recomendado pelo Google para GitHub Actions — sem chave JSON. O GitHub Actions se autentica no Google Cloud via OIDC token de curta duração.

### Configuração no Google Cloud

1. Ativar **IAM Service Account Credentials API**
2. Criar **Workload Identity Pool**:
   - Nome/ID: `github-pool`
3. Adicionar **Provider** ao pool:
   - Tipo: OIDC
   - Nome: `github-provider`
   - Emissor: `https://token.actions.githubusercontent.com`
4. Mapeamento de atributos:
   - `google.subject` = `assertion.sub`
   - `attribute.repository` = `assertion.repository`
   - Condição: `assertion.repository == "Gustpbbr/Gus"`
5. Conceder acesso à service account `gus-sync` via "identidade temporária de conta de serviço" com atributo `repository = Gustpbbr/Gus`

### Secrets no GitHub

```
WIF_PROVIDER = projects/1024023930926/locations/global/workloadIdentityPools/github-pool/providers/github-provider
WIF_SERVICE_ACCOUNT = gus-sync@gus-drive-sync.iam.gserviceaccount.com
DRIVE_ROOT_FOLDER_ID = 1JP_FoaMeexq3dhwyCc2g2ZpoMh-Zx4ME
```

### Workflow

```yaml
permissions:
  contents: read
  id-token: write

- name: Authenticate to Google Cloud
  uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
    service_account: ${{ secrets.WIF_SERVICE_ACCOUNT }}
```

**Resultado:** autenticação funcionou. O script conectou no Drive, criou as pastas `capturado/misc/` corretamente.

**Bloqueio:** ao tentar criar o arquivo:

```
HttpError 403: The user's Drive storage quota has been exceeded.
reason: storageQuotaExceeded
```

**Causa raiz:** service accounts não têm quota de armazenamento no Google Drive. Quando a service account cria um arquivo no Drive (mesmo em pasta compartilhada), o arquivo é de propriedade da service account — que não tem Drive storage. Com conta Gmail pessoal não há domain-wide delegation, então a service account não consegue criar arquivos em nome do usuário humano.

**Status:** WIF continua configurado no Google Cloud (não atrapalha). Mas o script precisou mudar a estratégia de autenticação.

---

## Tentativa 3 — OAuth2 com Refresh Token ✅

**Abordagem:** autenticar como o próprio Gustavo (não como service account). O script usa credenciais OAuth2 do usuário — os arquivos criados no Drive são de propriedade de `gustavo.pratti@gmail.com` e contam contra sua cota de 5TB.

### Configuração no Google Cloud

1. **APIs & Services → Credenciais → Criar credenciais → OAuth 2.0 Client ID**
   - Tipo: App para computador (Desktop app)
   - Nome: `gus-sync-oauth`
2. **Tela de consentimento OAuth:**
   - Tipo: Externo
   - Adicionar `gustavo.pratti@gmail.com` como usuário de teste
3. Obter **refresh token** rodando script local:

```python
from google_auth_oauthlib.flow import InstalledAppFlow

flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
creds = flow.run_local_server(port=0)
print(creds.refresh_token)
```

O script abre o navegador → Gustavo autoriza com sua conta Google → refresh token impresso no terminal.

### Secrets no GitHub

```
GOOGLE_CLIENT_ID = 1024023930926-oacjeue15sckrecsgne064ppc8d10lll.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET = (salvo localmente)
GOOGLE_REFRESH_TOKEN = (salvo localmente)
DRIVE_ROOT_FOLDER_ID = 1JP_FoaMeexq3dhwyCc2g2ZpoMh-Zx4ME
```

### Script Python

```python
def get_drive_service():
    creds = Credentials(
        token=None,
        refresh_token=os.environ["GOOGLE_REFRESH_TOKEN"],
        client_id=os.environ["GOOGLE_CLIENT_ID"],
        client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
        token_uri="https://oauth2.googleapis.com/token",
        scopes=SCOPES,
    )
    creds.refresh(Request())
    return build("drive", "v3", credentials=creds)
```

**Resultado:** workflow verde, arquivo `capturado/misc/teste-drive-sync.md` apareceu na pasta `Gus-Sync` do Drive como Google Doc. ✅

---

## Arquitetura Final

```
GitHub (push em main com .md alterado)
        ↓
GitHub Actions (sync-to-drive.yml)
        ↓ autentica como gustavo.pratti@gmail.com via OAuth2
Google Drive API
        ↓
Pasta Gus-Sync/ (espelho da estrutura do repo)
```

### Arquivos excluídos do sync

- `CLAUDE.md`, `README.md`
- Pastas: `gus/`, `docs/`, `.github/`, `sensivel/`
- Só conteúdo pessoal: `pessoal/`, `projetos/`, `receitas/`, `esportes/`, `capturado/`, `dimagem/`, etc.

---

## Manutenção

**Refresh token expira?** Tokens OAuth2 de contas Google pessoais não expiram enquanto o app não for desautorizado. Se um dia parar de funcionar, rodar `get_token.py` novamente e atualizar o secret `GOOGLE_REFRESH_TOKEN`.

**Onde está `get_token.py`?** Em `C:\Gus\Gus\get_token.py` (local, não commitado — contém as credenciais hardcoded). Não commitar esse arquivo.

**Adicionar ao .gitignore:**
```
get_token.py
```
