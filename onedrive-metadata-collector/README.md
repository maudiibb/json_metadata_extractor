# OneDrive Metadata Collector

Samlar filmetadata (namn, storlek, datum, sökväg m.m.) från **hela organisationens**
OneDrive-konton via Microsoft Graph API, och sparar allt i en JSON-fil.

Använder app-only autentisering (client credentials flow) — ingen enskild
användare behöver logga in. Kräver admin-godkännande i Azure AD.

## Funktioner

- Listar alla användare i Microsoft 365-organisationen
- Hämtar filmetadata rekursivt från varje användares OneDrive
- Hanterar Graph API-throttling (HTTP 429) automatiskt
- Möjlighet att begränsa insamlingen till specifika användare
- Samlar allt i en strukturerad JSON-fil

## Krav

- Python 3.9+
- En app-registrering i Azure AD med följande **application permissions**:
  - `User.Read.All`
  - `Files.Read.All`
- Admin consent beviljat för dessa permissions

## Installation

```bash
git clone <repo-url>
cd onedrive-metadata-collector
pip install -r requirements.txt
cp .env.example .env
```

Fyll i `.env` med dina värden från Azure AD-app-registreringen:

```
AZURE_TENANT_ID=...
AZURE_CLIENT_ID=...
AZURE_CLIENT_SECRET=...
```

## Azure AD-uppsättning (en gång)

1. [portal.azure.com](https://portal.azure.com) → Azure Active Directory → App registrations → New registration
2. API permissions → Add a permission → Microsoft Graph → **Application permissions**:
   - `User.Read.All`
   - `Files.Read.All`
3. Klicka **Grant admin consent**
4. Certificates & secrets → New client secret → spara värdet direkt (visas bara en gång)
5. Kopiera Tenant ID och Client ID från Overview-sidan

## Användning

Hämta metadata för alla användare i organisationen:

```bash
python -m src.main --output metadata.json
```

Begränsa till specifika användare:

```bash
python -m src.main --output metadata.json --users anna@företag.se erik@företag.se
```

## Exempel på output

```json
{
  "scan_date": "2026-07-14T10:00:00",
  "total_users": 2,
  "users": [
    {
      "displayName": "Anna Andersson",
      "userPrincipalName": "anna@företag.se",
      "file_count": 142,
      "total_size_bytes": 583920123,
      "files": [
        {
          "name": "rapport.docx",
          "size_bytes": 34521,
          "created": "2026-01-15T08:22:00Z",
          "modified": "2026-03-02T14:10:00Z",
          "is_folder": false,
          "path": "/drive/root:/Dokument/rapport.docx"
        }
      ]
    }
  ]
}
```

## Viktigt om integritet och drift

- Detta verktyg ger åtkomst till **alla anställdas filer** i organisationen.
  Använd endast med giltigt syfte (t.ex. dataskyddsrevision, backup-verifiering)
  och i enlighet med organisationens policy och GDPR.
- `.env`-filen innehåller hemligheter och committas aldrig till git (se `.gitignore`).
- Output-JSON-filer innehåller potentiellt känslig information om anställdas
  filer och ignoreras därför också av git som standard.
- Stora organisationer kan träffa Graph API:ets rate limits — skriptet
  hanterar detta automatiskt men insamlingen kan ta lång tid.

## Licens

MIT
