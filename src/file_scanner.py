from pathlib import Path
from src.metadata_extractor import extract_metadata

def build_tree(folder_path):
    """
    Bygger rekursivt ett träd av mappar och filer under folder_path.
    Returnerar en dict som representerar HELA mappen, med en
    "children"-lista som innehåller undermappar (rekursivt) och filer.
    """
    folder = Path(folder_path)

    node = {
        "namn": folder.name,
        "typ": "mapp",
        "sökväg": str(folder),
        "undermappar": []
    }
    try:
        for item in folder.iterdir():
            if item.is_dir():
                # Det rekursiva steget: bygg ETT HELT TRÄD för undermappen
                # genom att anropa build_tree på DEN, och lägg till hela
                # resultatet (en dict, med sin egen undermappar-lista) i vår lista.
                subtree = build_tree(item)
                node["undermappar"].append(subtree)
            else:
                # Bas-fallet för denna gren: en fil har inga egna "undermappar",
                # så vi använder bara den befintliga funktionen
                file_metadata = extract_metadata(item)
                node["undermappar"].append(file_metadata)
    except OSError as e:
        print(f"Kunde inte läsa {folder_path}: {e}")
        return None

    return node