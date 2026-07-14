# OneDrive Metadata Collector

Samlar filmetadata (namn, storlek, datum, sökväg m.m.) från filer i en mapp
och sparar allt strukturerat i en JSON-fil.

Just nu skannar verktyget en **lokalt synkad OneDrive-mapp** direkt på disk.
Arkitekturen är dock byggd modulärt för att senare kunna byta ut den lokala
filskanningen mot **Microsoft Graph API**, så att samma verktyg kan samla
metadata från flera användares OneDrive-konton i en organisation — utan att
resten av koden (metadata-extrahering, JSON-sparning) behöver ändras.

## Funktioner (nuvarande version)

- Går igenom en mapp och alla dess undermappar **rekursivt**, och bygger
  ett hierarkiskt träd som speglar den faktiska mappstrukturen
- Extraherar metadata per fil: namn, filändelse, sökväg, storlek och tidsstämplar
- Hanterar fel per mapp/fil (låsta filer, saknad behörighet) utan att hela
  körningen kraschar
- Sparar resultatet som en läsbar, UTF-8-kodad JSON-fil

## Planerat (Graph API-version)

- Autentisering via app-only client credentials flow (ingen
  användarinloggning krävs)
- Lista alla användare i en Microsoft 365-organisation
- Hämta filmetadata från varje användares OneDrive via Microsoft Graph
- Hantering av Graph API-throttling (HTTP 429)
- Möjlighet att begränsa insamlingen till specifika användare

## Krav

- Python 3.9+

## Installation

```bash
git clone 
cd Admin-authenticator
pip install -r requirements.txt
```

## Projektstruktur

```
src/
├── file_scanner.py       # build_tree(): bygger rekursivt mappträdet
├── metadata_extractor.py # extract_metadata(): metadata för en enskild fil
└── main.py                # Kopplar ihop allt och sparar till JSON
```

## Användning

Just nu körs verktyget genom att ange en sökväg direkt i `main.py`
(under `if __name__ == "__main__":`). Kör som modul från projektroten:

```bash
python -m src.main
```

Resultatet sparas som `test_output.json` i projektroten.

### Exempel på output

Resultatet är hierarkiskt — varje mapp har en `children`-lista med sina
undermappar (som i sin tur har sina egna `children`) och filer:

```json
{
  "namn": "Utbye",
  "typ": "mapp",
  "sökväg": "C:\\Users\\namn\\OneDrive\\Desktop\\Utbye",
  "children": [
    {
      "namn": "Dokument",
      "typ": "mapp",
      "sökväg": "C:\\Users\\namn\\OneDrive\\Desktop\\Utbye\\Dokument",
      "children": [
        {
          "namn": "rapport",
          "suffix": ".pdf",
          "sökväg": "C:\\Users\\namn\\OneDrive\\Desktop\\Utbye\\Dokument\\rapport.pdf",
          "storlek": 278178,
          "skap_tid": "2026-06-24T18:03:55.822611",
          "senast_modifierad": "2026-06-24T18:03:56.885165",
          "senast öppnad": "2026-06-25T13:53:58.736509"
        }
      ]
    }
  ]
}
```

## Vägen mot fler användare (Graph API)

När Graph API-delen byggs kommer det krävas en app-registrering i Azure AD
med behörigheterna `User.Read.All` och `Files.Read.All`, samt admin consent
för organisationen. Detta läggs till som ett separat steg utan att röra
den befintliga metadata-extraherings- och JSON-sparningslogiken.

## Viktigt om integritet och drift

- Redan nu innehåller output-JSON-filer sökvägar och filnamn som kan vara
  personliga — dessa committas därför inte till git (se `.gitignore`).
- Den planerade Graph API-versionen kommer ge åtkomst till andra
  användares filer och ska endast användas med giltigt syfte och i
  enlighet med organisationens policy och GDPR.

## Licens

MIT