#!/usr/bin/env python3
"""
Correção manual de nomes conhecidos que foram corrompidos
"""

import json
import shutil
from datetime import datetime

# Mapeamento de nomes incorretos para corretos (ABNT)
# Mapear variações para o nome simples (ex: "ANDRADE, Carlos Drummond de" -> "DRUMMOND, Carlos")
KNOWN_FIXES = {
    # Carlos Drummond de Andrade - mapear para DRUMMOND, Carlos
    "ANDRADE, De": "DRUMMOND, Carlos",
    "DRUMMUND, Carlos": "DRUMMOND, Carlos",
    "DE, ANDRADE": "DRUMMOND, Carlos",
    "CARLOS, DRUMMUND": "DRUMMOND, Carlos",
    "ANDRADE DE, Carlos Drummond": "DRUMMOND, Carlos",
    "ANDRADE, DE, Carlos Drummond": "DRUMMOND, Carlos",
    "ANDRADE, Carlos Drummond de": "DRUMMOND, Carlos",

    # Murilo Mendes
    "MURILO, MENDES": "MENDES, Murilo",

    # Régis Bonvicino
    "RÉGIS, BONVICINO": "BONVICINO, Régis",

    # João Cabral de Melo Neto - mapear para MELO NETO, João Cabral de
    "NETO, João Cabral de Melo": "MELO NETO, João Cabral de",
    "CABRAL, João de Melo Neto": "MELO NETO, João Cabral de",

    # Outros autores com nomes compostos comuns
    "CAMPOS DE, Augusto": "CAMPOS, Augusto de",
    "CAMPOS DE, Haroldo": "CAMPOS, Haroldo de",
    "CAMPOS DE, Angela": "CAMPOS, Angela de",
}

def fix_author_name(name):
    """Corrige um nome usando o mapeamento conhecido"""
    if not name or not isinstance(name, str):
        return name

    # Verifica se está no mapeamento
    if name in KNOWN_FIXES:
        return KNOWN_FIXES[name]

    return name

def fix_author_list(authors):
    """Corrige uma lista de autores"""
    if not isinstance(authors, list):
        return authors

    fixed = []
    skip_next = False

    for i, author in enumerate(authors):
        if skip_next:
            skip_next = False
            continue

        # Se encontrar "ANDRADE, De" ou similar, pode ser parte de um nome composto
        if author == "ANDRADE, De" and i + 1 < len(authors):
            # Pula este e o próximo se forem fragmentos do mesmo nome
            if authors[i + 1] == "DRUMMUND, Carlos":
                fixed.append("ANDRADE, Carlos Drummond de")
                skip_next = True
                continue

        # Aplica correção conhecida
        corrected = fix_author_name(author)

        # Evita duplicatas
        if corrected not in fixed:
            fixed.append(corrected)

    return fixed

def main():
    json_path = "catalogo_sibila.json"

    # Backup
    backup_path = f"catalogo_sibila_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    shutil.copy(json_path, backup_path)
    print(f"✅ Backup criado: {backup_path}")

    # Carregar dados
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"📊 Total de registros: {len(data)}")

    # Corrigir campos de autores
    author_fields = ['autores_colaboradores', 'autores_citados', 'tradutores', 'nome_pessoal_como_assunto']
    fixed_count = 0
    changes = []

    for idx, record in enumerate(data):
        record_id = record.get('registro', f'index_{idx}')

        for field in author_fields:
            if field in record and isinstance(record[field], list):
                original = record[field].copy()
                fixed = fix_author_list(record[field])

                if original != fixed:
                    record[field] = fixed
                    changes.append(f"Registro {record_id} - {field}:")
                    changes.append(f"  DE: {original}")
                    changes.append(f"  PARA: {fixed}")
                    fixed_count += 1

    # Salvar
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Corrigidos {fixed_count} campos de autores")
    print(f"💾 Salvo em {json_path}")

    if changes:
        log_path = f"manual_fixes_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(changes))
        print(f"📝 Log salvo em: {log_path}")

        # Mostrar primeiras mudanças
        print("\nPrimeiras correções:")
        for line in changes[:20]:
            print(line)
    else:
        print("ℹ️  Nenhuma correção necessária")

if __name__ == "__main__":
    main()
