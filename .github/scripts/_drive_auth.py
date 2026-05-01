"""Helper de autenticação Google Drive — Service Account (preferido) com fallback OAuth.

Os scripts de sync (sync_to_drive.py, import_from_drive.py) compartilham
essa lógica pra não duplicar credentials parsing.

Service Account é a estratégia definitiva (não expira). OAuth refresh token
fica como fallback durante migração — apps em modo "Testing" expiram em
7 dias, virou loop de manutenção.

Variáveis de ambiente:
  Preferida:
    GOOGLE_SERVICE_ACCOUNT_JSON  — conteúdo do .json baixado do Cloud Console
  Fallback (legacy OAuth):
    GOOGLE_REFRESH_TOKEN
    GOOGLE_CLIENT_ID
    GOOGLE_CLIENT_SECRET
"""

import json
import logging
import os

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

log = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/drive"]


def get_drive_service():
    """Retorna cliente Drive autenticado. Prefere Service Account."""
    sa_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    if sa_json:
        log.info("Auth: Service Account")
        creds = service_account.Credentials.from_service_account_info(
            json.loads(sa_json),
            scopes=SCOPES,
        )
        return build("drive", "v3", credentials=creds, cache_discovery=False)

    refresh_token = os.getenv("GOOGLE_REFRESH_TOKEN", "").strip()
    if refresh_token:
        log.warning(
            "Auth: OAuth refresh token (legacy — migra pra GOOGLE_SERVICE_ACCOUNT_JSON)"
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
        "Nem GOOGLE_SERVICE_ACCOUNT_JSON nem GOOGLE_REFRESH_TOKEN setado. "
        "Configure um dos dois (preferir SA)."
    )
