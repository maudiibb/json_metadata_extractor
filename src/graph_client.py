"""
Klient för Microsoft Graph API.
Listar alla användare i organisationen och samlar filmetadata
från varje användares OneDrive (drive).
"""

import time
import requests

GRAPH_BASE = "https://graph.microsoft.com/v1.0"


class GraphClient:
    def __init__(self, access_token: str):
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

    def _get(self, url, params=None, retries=3):
        """GET med enkel hantering av throttling (HTTP 429)."""
        for attempt in range(retries):
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 5))
                time.sleep(retry_after)
                continue
            response.raise_for_status()
            return response.json()
        raise RuntimeError(f"För många försök mot {url}, gav upp efter {retries} försök")

    def list_users(self):
        """Listar alla användare i organisationen (id, displayName, userPrincipalName)."""
        users = []
        url = f"{GRAPH_BASE}/users"
        params = {"$select": "id,displayName,userPrincipalName,mail"}

        while url:
            data = self._get(url, params=params)
            users.extend(data.get("value", []))
            url = data.get("@odata.nextLink")
            params = None  # nextLink innehåller redan query-parametrar

        return users

    def get_user_drive_items(self, user_id, path="root"):
        """
        Hämtar alla filer/mappar rekursivt från en användares OneDrive.
        path="root" = OneDrive-rotens innehåll.
        """
        items_collected = []
        url = f"{GRAPH_BASE}/users/{user_id}/drive/{path}/children"

        try:
            data = self._get(url)
        except requests.exceptions.HTTPError as e:
            # T.ex. 404 om användaren saknar OneDrive-licens
            return [], str(e)

        for item in data.get("value", []):
            entry = {
                "id": item.get("id"),
                "name": item.get("name"),
                "size_bytes": item.get("size"),
                "created": item.get("createdDateTime"),
                "modified": item.get("lastModifiedDateTime"),
                "is_folder": "folder" in item,
                "web_url": item.get("webUrl"),
                "path": item.get("parentReference", {}).get("path", "") + "/" + item.get("name", ""),
            }
            items_collected.append(entry)

            # Rekursera in i undermappar
            if "folder" in item and item.get("folder", {}).get("childCount", 0) > 0:
                sub_items, _ = self.get_user_drive_items(
                    user_id, path=f"items/{item['id']}"
                )
                items_collected.extend(sub_items)

        return items_collected, None
