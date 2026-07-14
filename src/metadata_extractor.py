from datetime import datetime

def extract_metadata(file_path):
    try:
        stat = file_path.stat()  # ger dig ett "stat_result"-objekt med rådata
    except OSError as e:
        print(f"Kunde inte läsa {file_path}: {e}")
        return None
    
    metadata = {
        "namn": file_path.stem,
        "suffix": file_path.suffix,
        "sökväg": str(file_path),
        "storlek": stat.st_size,
        "skap_tid": datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "senast_modifierad": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "senast öppnad": datetime.fromtimestamp(stat.st_atime).isoformat()
    }
    
    return metadata


if __name__ == "__main__":
    from pathlib import Path
    test_file = Path(r"C:\Users\amrik\OneDrive\Desktop\Utbye")
    print(extract_metadata(test_file))