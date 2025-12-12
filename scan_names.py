import json
from collections import Counter

FILE_PATH = 'catalogo_sibila.json'

FIELDS_TO_CHECK = [
    "autores_colaboradores",
    "autores_citados",
    "tradutores",
    "nome_pessoal_como_assunto"
]

def scan_file():
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"File {FILE_PATH} not found.")
        return

    all_names = Counter()
    field_names = {field: Counter() for field in FIELDS_TO_CHECK}

    for entry in data:
        for field in FIELDS_TO_CHECK:
            if field in entry and isinstance(entry[field], list):
                for name in entry[field]:
                    cleaned = name.strip()
                    all_names[cleaned] += 1
                    field_names[field][cleaned] += 1

    # Print all names sorted alphabetically to spot duplicates
    print("\n=== ALL UNIQUE NAMES (Sorted) ===")
    for name in sorted(all_names.keys()):
        print(f"{name} ({all_names[name]})")

    # Specifically check for variations mentioned
    print("\n=== CHECKING FOR 'CABRAL' / 'MELO NETO' ===")
    for name in all_names:
        upper_name = name.upper()
        if "CABRAL" in upper_name or "MELO NETO" in upper_name:
            print(f"- {name} ({all_names[name]})")

if __name__ == "__main__":
    scan_file()
