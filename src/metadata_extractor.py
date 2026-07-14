from datetime import datetime

def extract_metadata(file_path):
    #Tar emot ETT Path-objekt 
    #Returnerar en dict med metadatan, 
    try:
        # .stat() hämtar rådata om filen från operativsystemet
        stat = file_path.stat()  
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

