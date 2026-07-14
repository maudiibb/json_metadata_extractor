from src.file_scanner import build_tree
import json

def save_to_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    trad = build_tree(r"C:\Users\amrik\OneDrive\Documents\NetBeansProjects")
    save_to_json(trad, "test_output.json")
    print("Klart!")