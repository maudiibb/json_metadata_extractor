from src.file_scanner import list_files
from src.metadata_extractor import extract_metadata
import json

def collect_all_metadata(root_path):
    results = []
    for file_path in list_files(root_path):
        metadata = extract_metadata(file_path)
        results.append(metadata)
    return results

def save_to_json(data, output_path):
       with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

