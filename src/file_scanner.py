from pathlib import Path

def list_files(root_path):
    root = Path(root_path)
    # root.rglob("*") ger dig ALLA filer och mappar, rekursivt
    for item in root.rglob("*"):
        # hur avgör du om "item" är en fil och inte en mapp?
        if item.is_dir():
            continue
        yield item


