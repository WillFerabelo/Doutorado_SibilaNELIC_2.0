import json
from collections import Counter
from difflib import SequenceMatcher

FILE_PATH = 'catalogo_sibila.json'

FIELDS_TO_CHECK = [
    "autores_colaboradores",
    "autores_citados",
    "tradutores",
    "nome_pessoal_como_assunto"
]

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def scan_duplicates():
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"File {FILE_PATH} not found.")
        return

    all_names = Counter()

    for entry in data:
        for field in FIELDS_TO_CHECK:
            if field in entry and isinstance(entry[field], list):
                for name in entry[field]:
                    cleaned = name.strip()
                    if cleaned:
                        all_names[cleaned] += 1

    unique_names = sorted(list(all_names.keys()))
    print(f"Total unique names: {len(unique_names)}")
    
    potential_duplicates = []
    
    # Heuristic 1: Check for names that are contained in others (e.g. "Pound" in "Pound, Ezra")
    # Heuristic 2: Check for high similarity ratio
    
    checked = set()

    for i, name1 in enumerate(unique_names):
        for j in range(i + 1, len(unique_names)):
            name2 = unique_names[j]
            
            # Optimization: if names are too different in length or starting char, skip expensive check
            # but for author names "Last, First" vs "First Last" we might need more.
            # Let's focus on "Last, First" structure mostly used here.
            
            if name1 in checked or name2 in checked:
                continue

            # Check similarity
            similarity = similar(name1.lower(), name2.lower())
            
            # High similarity threshold
            if similarity > 0.85:
                 potential_duplicates.append((similarity, name1, name2, all_names[name1], all_names[name2]))
            
            # Check for same last name parts (simple comma check)
            if ',' in name1 and ',' in name2:
                parts1 = name1.split(',')[0].strip()
                parts2 = name2.split(',')[0].strip()
                if parts1 == parts2 and similarity > 0.6: # Same surname, some similarity
                     potential_duplicates.append((similarity, name1, name2, all_names[name1], all_names[name2]))

    # Sort by similarity
    potential_duplicates.sort(key=lambda x: x[0], reverse=True)
    
    print("\n=== POTENTIAL DUPLICATES FOUND ===")
    seen_pairs = set()
    for sim, n1, n2, c1, c2 in potential_duplicates:
        pair = tuple(sorted((n1, n2)))
        if pair not in seen_pairs:
            print(f"[{sim:.2f}] '{n1}' ({c1})  <-->  '{n2}' ({c2})")
            seen_pairs.add(pair)

if __name__ == "__main__":
    scan_duplicates()
