from pathlib import Path

def list_files(root_path):
    # Går igenom en mapp (och alla undermappar) och lämnar ut varje FIL
    # den hittar, en i taget.
    root = Path(root_path)
    # root.rglob("*") ger dig ALLA filer och mappar, rekursivt
    # genom hela mappträdet under root_path.
    for item in root.rglob("*"):
        if item.is_dir():
            # Vi bryr oss bara om filer, inte mappar - hoppa över
            # och fortsätt till nästa item i loopen.
            continue
        yield item


