#!/usr/bin/env python3
"""
Script to fix corrupted author names in catalogo_sibila.json
The parse_multiline function was replacing commas with newlines, which broke ABNT names.
"""

import json
import shutil
from datetime import datetime
from pathlib import Path


def format_nome_abnt(nome: str) -> str:
    """Format name according to ABNT: SOBRENOME, Prenomes"""
    if not nome or not isinstance(nome, str):
        return ""

    s = " ".join(nome.strip().split())
    if not s:
        return ""

    # Already in ABNT format
    if "," in s:
        ult, resto = s.split(",", 1)
        return f"{ult.strip().upper()}, {resto.strip()}" if resto.strip() else ult.strip().upper()

    # Convert to ABNT format
    partes = s.split()
    if len(partes) >= 2:
        sobrenome = partes[-1].upper()
        prenomes = " ".join(partes[:-1])
        return f"{sobrenome}, {prenomes}"

    return s.upper()


def is_corrupted_author_list(authors):
    """Detect if an author list is corrupted (single words instead of full names)"""
    if not isinstance(authors, list) or len(authors) == 0:
        return False

    # If most items are single words (no commas, no spaces), it's likely corrupted
    single_words = sum(1 for a in authors if isinstance(a, str) and ' ' not in a.strip() and ',' not in a)
    return single_words > len(authors) * 0.7  # More than 70% are single words


def reconstruct_names(word_list):
    """
    Try to reconstruct full names from a list of individual words.
    Brazilian names are typically stored as: [SOBRENOME, PRENOME1, PRENOME2]
    We need to pair them correctly: SOBRENOME, Prenomes
    """
    if not word_list:
        return []

    reconstructed = []
    i = 0

    while i < len(word_list):
        # In typical Brazilian pattern: first word is last name, next 1-3 are first names
        # Example: ['MENDES', 'MURILO'] -> 'MENDES, Murilo'
        # Example: ['ANDRADE', 'DE', 'DRUMMOND', 'CARLOS'] -> need to handle compounds

        # Collect the surname (first word)
        sobrenome = word_list[i]
        i += 1

        # Collect prenomes (following words, typically 1-3)
        prenomes = []
        while i < len(word_list) and len(prenomes) < 3:
            word = word_list[i]

            # Check if this might be the start of a new name (all caps, single word)
            # If we already have prenomes and next word is all caps, it's likely a new surname
            if prenomes and word.isupper() and ' ' not in word:
                # Check if this looks like a common preposition that's part of current name
                if word.upper() not in ['DE', 'DA', 'DO', 'DOS', 'DAS']:
                    # This is probably a new surname, stop here
                    break

            prenomes.append(word)
            i += 1

        # Format: SOBRENOME, Prenomes
        if prenomes:
            # Capitalize prenomes properly (first letter uppercase, rest as is)
            prenomes_str = ' '.join(prenomes)
            # Don't convert to title case if already has mixed case
            if prenomes_str.isupper():
                prenomes_str = prenomes_str.title()
            formatted = f"{sobrenome.upper()}, {prenomes_str}"
        else:
            formatted = sobrenome.upper()

        if formatted:
            reconstructed.append(formatted)

    return reconstructed


def fix_author_field(authors):
    """Fix a single author field"""
    if not isinstance(authors, list):
        return authors

    # Empty list is fine
    if len(authors) == 0:
        return []

    # If it looks corrupted, try to reconstruct
    if is_corrupted_author_list(authors):
        return reconstruct_names(authors)

    # Otherwise, just ensure ABNT formatting
    return [format_nome_abnt(a) for a in authors if a]


def main():
    json_path = Path("catalogo_sibila.json")

    if not json_path.exists():
        print(f"ERROR: {json_path} not found!")
        return

    # Create backup
    backup_path = f"catalogo_sibila_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    shutil.copy(json_path, backup_path)
    print(f"✅ Backup created: {backup_path}")

    # Load data
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"📊 Total records: {len(data)}")

    # Fix author fields
    author_fields = ['autores_colaboradores', 'autores_citados', 'tradutores', 'nome_pessoal_como_assunto']
    fixed_count = 0
    changes_log = []

    for idx, record in enumerate(data):
        record_id = record.get('registro', f'index_{idx}')
        record_changes = []

        for field in author_fields:
            if field in record:
                original = record[field]
                if is_corrupted_author_list(original):
                    fixed = fix_author_field(original)
                    record[field] = fixed
                    record_changes.append(f"  {field}: {original} → {fixed}")
                    fixed_count += 1

        if record_changes:
            changes_log.append(f"Record {record_id}:")
            changes_log.extend(record_changes)

    # Save fixed data
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Fixed {fixed_count} corrupted author fields")
    print(f"💾 Saved to {json_path}")

    # Save changes log
    if changes_log:
        log_path = f"author_fixes_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(changes_log))
        print(f"📝 Changes logged to: {log_path}")
        print("\nSample changes:")
        for line in changes_log[:20]:  # Show first 20 lines
            print(line)
    else:
        print("ℹ️  No corrupted data found")


if __name__ == "__main__":
    main()
