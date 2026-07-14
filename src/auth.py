"""
Autentisering mot Microsoft Graph API med client credentials flow
(app-only, ingen användarinloggning krävs).

Kräver att en app-registrering i Azure AD har:
- Application permissions: User.Read.All, Files.Read.All
- Admin consent beviljat för dessa

Miljövariabler (se .env.example):
    AZURE_TENANT_ID
    AZURE_CLIENT_ID
    AZURE_CLIENT_SECRET
"""

import os
import msal


GRAPH_SCOPE = ["https://graph.microsoft.com/.default"]


def get_access_token() -> str:
    """Hämtar en access token från Azure AD via client credentials flow."""
    tenant_id = os.environ["AZURE_TENANT_ID"]
    client_id = os.environ["AZURE_CLIENT_ID"]
    client_secret = os.environ["AZURE_CLIENT_SECRET"]

    authority = f"https://login.microsoftonline.com/{tenant_id}"

    app = msal.ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=authority,
    )

    result = app.acquire_token_for_client(scopes=GRAPH_SCOPE)

    if "access_token" not in result:
        error = result.get("error", "unknown_error")
        description = result.get("error_description", "Ingen beskrivning tillgänglig")
        raise RuntimeError(f"Kunde inte hämta access token: {error} - {description}")

    return result["access_token"]
