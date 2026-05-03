"""Helper de autenticação Google Drive — Workload Identity Federation (preferido).

Os scripts de sync (sync_to_drive.py, import_from_drive.py) compartilham
essa lógica pra não duplicar credentials parsing.

Estratégia (em ordem de preferência):

1. **Application Default Credentials (ADC)** — preferred
   Quando o workflow GitHub Actions usa `google-github-actions/auth@v2` com
   Workload Identity Federation, o action seta env vars que o SDK detecta
   automaticamente (`google.auth.default()`). Sem JSON key, sem expirar.

2. **Service Account JSON key** — fallback (uso raro)
   Se a organização Google Cloud bloqueia criação de keys (política
   `iam.disableServiceAccountKeyCreation`), essa via não funciona — usa
   WIF (opção 1).

3. **OAuth refresh token** — legacy (DEPRECATED)
   Modo "Testing" expira em 7 dias. Mantido só pra retrocompat até os
   workflows todos migrarem pra WIF.

Variáveis de ambiente:
  ADC (WIF):              GOOGLE_APPLICATION_CREDENTIALS (setada pelo action)
  Service Account JSON:   GOOGLE_SERVICE_ACCOUNT_JSON
  OAuth (legacy):         GOOGLE_REFRESH_TOKEN + CLIENT_ID + CLIENT_SECRET
"""

import json
import logging
import os

import google.auth
import google.auth.exceptions
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

log = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/drive"]


def _try_adc():
    """Tenta Application Default Credentials. Retorna creds ou None."""
    try:
        creds, project = google.auth.default(scopes=SCOPES)
        log.info(f"Auth: ADC / WIF (project detectado: {project})")
        return creds
    except google.auth.exceptions.DefaultCredentialsError:
        return None


def get_drive_service():
    """Retorna cliente Drive autenticado. Prefere ADC (WIF)."""
    creds = _try_adc()
    if creds is not None:
        return build("drive", "v3", credentials=creds, cache_discovery=False)

    sa_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    if sa_json:
        log.info("Auth: Service Account JSON (fallback)")
        creds = service_account.Credentials.from_service_account_info(
            json.loads(sa_json),
            scopes=SCOPES,
        )
        return build("drive", "v3", credentials=creds, cache_discovery=False)

    refresh_token = os.getenv("GOOGLE_REFRESH_TOKEN", "").strip()
    if refresh_token:
        log.warning(
            "Auth: OAuth refresh token (DEPRECATED — migra pra WIF)"
        )
        creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            client_id=os.environ["GOOGLE_CLIENT_ID"],
            client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
            token_uri="https://oauth2.googleapis.com/token",
            scopes=SCOPES,
        )
        creds.refresh(Request())
        return build("drive", "v3", credentials=creds, cache_discovery=False)

    raise SystemExit(
        "Sem auth Google Drive disponível. Configure um destes (em ordem "
        "de preferência): WIF via google-github-actions/auth, "
        "GOOGLE_SERVICE_ACCOUNT_JSON, ou GOOGLE_REFRESH_TOKEN."
    )
