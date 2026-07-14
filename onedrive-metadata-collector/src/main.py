"""
Samlar filmetadata från alla användares OneDrive i organisationen
och sparar resultatet till en JSON-fil.

Användning:
    python -m src.main --output metadata.json
    python -m src.main --output metadata.json --users user1@domain.com user2@domain.com
"""

import argparse
import json
import sys
from datetime import datetime

from src.auth import get_access_token
from src.graph_client import GraphClient


def main():
    parser = argparse.ArgumentParser(description="Samla OneDrive-metadata för hela organisationen")
    parser.add_argument("--output", default="metadata.json", help="Output-fil (JSON)")
    parser.add_argument(
        "--users",
        nargs="*",
        default=None,
        help="Begränsa till specifika användare (userPrincipalName). Standard: alla användare.",
    )
    args = parser.parse_args()

    print("Autentiserar mot Microsoft Graph...")
    token = get_access_token()
    client = GraphClient(token)

    print("Hämtar användarlista...")
    all_users = client.list_users()

    if args.users:
        all_users = [u for u in all_users if u.get("userPrincipalName") in args.users]

    print(f"Hittade {len(all_users)} användare att bearbeta.")

    result = {
        "scan_date": datetime.now().isoformat(),
        "total_users": len(all_users),
        "users": [],
    }

    for i, user in enumerate(all_users, start=1):
        upn = user.get("userPrincipalName")
        print(f"[{i}/{len(all_users)}] Hämtar filer för {upn}...")

        items, error = client.get_user_drive_items(user["id"])

        user_entry = {
            "id": user.get("id"),
            "displayName": user.get("displayName"),
            "userPrincipalName": upn,
            "mail": user.get("mail"),
            "file_count": len(items),
            "total_size_bytes": sum(f["size_bytes"] or 0 for f in items),
            "files": items,
        }
        if error:
            user_entry["error"] = error

        result["users"].append(user_entry)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\nKlart! Metadata för {len(all_users)} användare sparat i: {args.output}")


if __name__ == "__main__":
    sys.exit(main())
