from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_ID = "1024023930926-oacjeue15sckrecsgne064ppc8d10lll.apps.googleusercontent.com"
CLIENT_SECRET = "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"
SCOPES = ["https://www.googleapis.com/auth/drive"]

client_config = {
    "installed": {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
}

flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
creds = flow.run_local_server(port=0)
print("\nRefresh token:")
print(creds.refresh_token)