import json
import os
import time

FILE_PATH = 'catalogo_sibila.json'

# --- DATA MAPPING ---
# Key: "registro"
# Value: List of dictionaries { "colab": "Name", "citations": ["Name", ...] }
CARTAS_MAP = {
    # Issue 1
    "2 de 35": [
        {"colab": "KOZER, José", "citations": ["BERNSTEIN, Charles", "MENDES, Murilo", "LEMINSKI, Paulo", "COSTA, Horácio", "JINGMING, Yao"]},
        {"colab": "ARRUDA, Gustavo", "citations": []},
        {"colab": "MAIA, Maria Armandina", "citations": []},
        {"colab": "COLE, Norma", "citations": []},
        {"colab": "GINZBURG, Jaime", "citations": ["LIMA, Manoel Ricardo de"]},
        {"colab": "MAINARDI, Diogo", "citations": ["BONVICINO, Régis", "AMÂNCIO, Moacir", "BUENO, Wilson"]},
        {"colab": "ROYET-JOURNOUD, Claude", "citations": ["FROTA, Eduardo", "FLICK, Robert"]},
        {"colab": "JINGMING, Yao", "citations": []},
        {"colab": "JIMÉNEZ, Reynaldo", "citations": []},
        {"colab": "BENNETT, Guy", "citations": ["MESSERLI, Douglas"]},
        {"colab": "FLICK, Robbert", "citations": ["BERNSTEIN, Charles", "FLICK, Robert"]}, # "L LA BARATA" ignored as not a person
        {"colab": "CREELEY, Robert", "citations": []},
        {"colab": "VERDI, Maria Lucia", "citations": ["JINGMING, Yao", "BONVICINO, Régis"]},
    ],
    # Issue 2
    "2 de 41": [
        {"colab": "ALMINO, João", "citations": []},
        {"colab": "HATHEYER, Pedro Paulo", "citations": ["BONVICINO, Régis", "GUIMARÃES, Lúcia", "BLINDER, Caio", "CISNEROS, Odile"]},
        {"colab": "SALAZAR, Jussara", "citations": []},
        {"colab": "MOURA, Antonio", "citations": []},
        {"colab": "MARIANI, Matias", "citations": ["ANDREWS, Bruce", "BERNSTEIN, Charles"]},
        {"colab": "TOLMAN, Jon M", "citations": ["CISNEROS, Odile"]},
        {"colab": "ROQUETTE-PINTO, Claudia", "citations": ["BONVICINO, Régis", "CISNEROS, Odile"]},
        {"colab": "SANDMAN, Marcelo", "citations": []},
        {"colab": "MARINS, Álvaro", "citations": ["SALVINO, Romulo Valle"]},
        {"colab": "GALVÃO, Donizete", "citations": ["SALVINO, Romulo Valle", "PERLOFF, Marjorie", "SANDMAN, Marcelo", "VELOSO, Caetano"]},
        {"colab": "BERNSTEIN, Charles", "citations": ["BONVICINO, Régis"]},
        {"colab": "DEVINENI, Ram", "citations": ["ROCHA, Flavia", "TORRES, Edwin"]},
    ],
    # Issue 3
    "3 de 54": [
        {"colab": "ZÉ, Tom", "citations": ["BONVICINO, Régis"]},
        {"colab": "CÁMARA, Mario", "citations": ["SALVINO, Romulo Valle"]},
        {"colab": "BOSI, Viviana", "citations": ["WEINBERGER, Eliot", "VETERANYI, Aglaja"]},
        {"colab": "ROSA, Mário Alex", "citations": []},
        {"colab": "CARVALHO, Ricardo Schmitt", "citations": ["STOCK, Robert", "MARTINS, Luciana", "FAUSTINO, Mário", "VILLAÇA, Alcides Celso de Oliveira"]},
        {"colab": "MACCHI, Fabiana", "citations": []},
        {"colab": "BESSA, A.S.", "citations": ["WEINBERGER, Eliot", "NETO, Torquato", "MEIRELES, Cecília", "FAUSTINO, Mário", "SALVINO, Romulo Valle"]},
        {"colab": "TOSCANO, Rodrigo", "citations": []},
    ],
    # Issue 4
    "2 de 37": [
        {"colab": "PIGNATARI, Décio", "citations": ["BERNSTEIN, Charles", "BONVICINO, Régis"]},
        {"colab": "MOURA, Carolina Bassi de", "citations": []},
        {"colab": "TONETO, Diana", "citations": ["BESSA-LUÍS, Agustina", "BANDEIRA, Manuel"]},
        {"colab": "BUZZO, Elisa Andrade", "citations": []},
        {"colab": "ÁVILA, Carlos", "citations": ["BONVICINO, Régis", "UNGARETTI, Giuseppe", "TABLADA, José Juan", "BEE, Susan", "MELO NETO, João Cabral de", "ALMINO, João", "SALVINO, Romulo Valle", "CAMPOS, Angela de"]},
    ],
    # Issue 5
    "2 de 39": [
        {"colab": "MULLER, Adalberto", "citations": ["SANDMAN, Marcelo", "CELAN, Paul"]},
        {"colab": "PÉCORA, Alcir", "citations": []},
        {"colab": "GULLAR, Ferreira", "citations": ["BONVICINO, Régis"]},
        {"colab": "GOLA, Hugo", "citations": ["BONVICINO, Régis"]},
        {"colab": "MALTA, P.", "citations": []},
        {"colab": "ROSENFIELD, Kathrin H.", "citations": ["HARDT, Michael", "NEGRI, Antonio", "BRECHT, Bertolt", "GENET, Jean", "CREELEY, Robert", "BONVICINO, Régis", "MESSERLI, Douglas"]},
    ],
    # Issue 6
    "3 de 32": [
        {"colab": "FACCIONI FILHO, Mauro", "citations": []},
        {"colab": "MACCHI, Fabiana", "citations": ["ROQUETTE-PINTO, Claudia", "BAPTISTA, Josely Vianna", "PERLOFF, Marjorie", "DRAGOMOSHCHENKO, Arkadii", "ÁVILA, Affonso", "CISNEROS, Odile", "CAMPOS, Haroldo de", "CHIELLINO, Gino"]},
        {"colab": "SOSA, Víctor", "citations": []},
        {"colab": "MARIANI, Matias", "citations": ["BONVICINO, Régis"]},
        {"colab": "GUIMARÃES, Júlio Castañon", "citations": ["BONVICINO, Régis"]},
    ],
}

def split_records():
    if not os.path.exists(FILE_PATH):
        print(f"File {FILE_PATH} not found.")
        return

    print("Loading JSON...")
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    new_data = []
    
    # Track replaced count
    replaced_ids = set()

    for record in data:
        reg_id = record.get('registro')

        if reg_id in CARTAS_MAP:
            # This is a Cartas record -> Split it
            print(f"Splitting record: {reg_id}")
            replaced_ids.add(reg_id)
            
            sub_records_list = CARTAS_MAP[reg_id]
            base_id_suffix = reg_id.split(' ')[0] # "3" from "3 de 54"
            base_total = reg_id.split(' ')[-1] # "54" from "3 de 54"
            
            for i, item in enumerate(sub_records_list, 1):
                # Deep copy basic fields
                new_rec = record.copy()
                
                # Update specific fields
                # New ID structure: "3.1 de 54"
                new_rec['registro'] = f"{base_id_suffix}.{i} de {base_total}"
                
                # Single collaborator
                new_rec['autores_colaboradores'] = [item['colab']]
                
                # Specific citations
                new_rec['autores_citados'] = item['citations']
                
                # Update _id to ensure uniqueness (timestamp + index suffix)
                original_ts = int(record.get('_id', str(int(time.time()*1000))))
                new_rec['_id'] = str(original_ts + i)
                
                # Add notes about the split? (Optional, maybe not needed)
                # new_rec['notas_pesquisa'] = ... 

                new_data.append(new_rec)
        else:
            # Keep original record
            new_data.append(record)

    print(f"Writing {len(new_data)} records...")
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
    print("Done.")

if __name__ == "__main__":
    split_records()
