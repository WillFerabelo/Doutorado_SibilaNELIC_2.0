import json
import os

# Caminho do arquivo
FILE_PATH = 'catalogo_sibila.json'

# Mapeamento de Autores Canônicos
CANONICAL_AUTHORS = {
    # BACH
    "BACH": "BACH, Johann Sebastian",
    "BACH, J. S.": "BACH, Johann Sebastian",
    "BACH, Johann S.": "BACH, Johann Sebastian",
    
    # NOVAS REGRAS
    "ADORNO, Theodor": "ADORNO, Theodor W.",
    "ALIGHIERI, DANTE": "ALIGHIERI, Dante",
    "ALLEN, Donald": "ALLEN, Donald M.",
    "ALVIM, Chico": "ALVIM, Francisco",
    "ARAÚJO, Lais Corrêa de": "ARAÚJO, Laís Corrêa de",
    "ARISTÓTELES, Aristóteles": "ARISTÓTELES",
    "BALL": "BALL, Hugo",
    "BUENO": "BUENO, Wilson",
    "BYRON": "BYRON, Lord",
    "CABRAL, João": "MELO NETO, João Cabral de",
    "CABRAL, João (Melo Neto)": "MELO NETO, João Cabral de",
    "CABRAL, João (de Melo Neto)": "MELO NETO, João Cabral de",
    "CABRAL DE MELO NETO, João": "MELO NETO, João Cabral de",
    "MELLO NETO, João Cabral de": "MELO NETO, João Cabral de",
    "CAMÕES, Luís de": "CAMÕES, Luís Vaz de",
    "CAYMMI, Dori": "CAYMMI, Dorival",
    "CHOPIN, Fryderyk": "CHOPIN, Frédéric",
    "CLARK, Lígia": "CLARK, Lygia",
    "CORBUSIER, LE": "CORBUSIER, Le",
    "CRISTOBO, Anibal": "CRISTOBO, Aníbal",
    "CUMMINGS, E. E.": "CUMMINGS, e. e.",
    "CUMMINGS, e.e.": "CUMMINGS, e. e.",
    "DAO, BEI": "DAO, Bei",
    "DICK, André": "DICK, André Henrique",
    "DOLHNIKOFF, Luís": "DOLHNIKOFF, Luis",
    
    # NOVAS REGRAS (LOTE 2)
    "DRUMMOND, Carlos": "DRUMMOND, Carlos (de Andrade)",
    "DRUMMOND, Drummond": "DRUMMOND, Carlos (de Andrade)",
    "ANDRADE, Carlos Drummond de": "DRUMMOND, Carlos (de Andrade)",
    "DUFRÊNE": "DUFRÊNE, François",
    "EISENSTEIN, Sergei": "EISENSTEIN, Sergei M.",
    "ELIOT, T.S.": "ELIOT, T. S.",
    "FERRARI, Léon": "FERRARI, León",
    "FERREIRA": "FERREIRA, Evandro Affonso",
    "FONTANA": "FONTANA, Lucio",
    "FROTA": "FROTA, Eduardo",
    "GIL": "GIL, Gilberto",
    "GOETHE": "GOETHE, Johann Wolfgang von",
    "GOLDSMITH, Kenny": "GOLDSMITH, Kenneth",

    # NOVAS REGRAS (LOTE 3)
    "GUIMARÃES, Júlio C.": "GUIMARÃES, Júlio Castañon",
    "HOLLANDA, Heloisa Buarque de": "HOLLANDA, Heloísa Buarque de",
    "JOBIM, Tom": "JOBIM, Antônio Carlos",
    "JOHNSON": "JOHNSON, Robert",
    "JOYCE": "JOYCE, James",
    "KHLIÉBNIKOV, Vielímir": "KHLIÉBNIKOV, Velimir",
    "KHLÉBNIKOV, Velimir": "KHLIÉBNIKOV, Velimir",
    "KHLÉBNIKOV, Velímir": "KHLIÉBNIKOV, Velimir",
    "KOZER, Jos": "KOZER, José",
    "KOZER, Jose": "KOZER, José",
    "LAUTRÉAMONT": "LAUTRÉAMONT, Conde de",
    "LEITE, Sebastião Uchôa": "LEITE, Sebastião Uchoa",
    "LIMA, Manoel Ricardo": "LIMA, Manoel Ricardo de",
    "MAIAKÓVSKI": "MAIAKÓVSKI, Vladímir",
    "MAIAKÓVSKI, Vladimir": "MAIAKÓVSKI, Vladímir",
    "MANDELSTAM, Óssip": "MANDELSTAM, Osip",
    "MORAES, Vinícius de": "MORAES, Vinicius de",
    "MORAIS, Vinícius de": "MORAES, Vinicius de",
    "MOURA, Antonio": "MOURA, Antônio",
    "MÃE, Valter Hugo": "MÃE, valter hugo",
    "NEZVAL, Vitezlav": "NEZVAL, Vítězslav",
    "PASTERNAK": "PASTERNAK, Boris",
    "PETRARCA": "PETRARCA, Francesco",
    "PLAZA, Júlio": "PLAZA, Julio",
    
    # NOVAS REGRAS (LOTE 4)
    "PUSHKIN": "PUSHKIN, Alexander",
    "RODRÍGUEZ, Américo": "RODRIGUES, Américo",
    "ROQUETTE-PINTO, Cláudia": "ROQUETTE-PINTO, Claudia",
    "ROSA, Guimarães": "ROSA, João Guimarães",
    "ROSA, Mario Alex": "ROSA, Mário Alex",
    "ROTHENBERG, Gerome": "ROTHENBERG, Jerome",
    "SABINSON, Eric": "SABINSON, Eric Mitchell",
    "SALOMÃO, Wally": "SALOMÃO, Waly",
    "SALVINO, Rômullo Valle": "SALVINO, Romulo Valle",
    "SALVINO, Rômulo Valle": "SALVINO, Romulo Valle", # Case where input is already normalized (optional but harmless)
    "SALVINO, Romullo Valle": "SALVINO, Romulo Valle",
    "SOSA, Víctor": "SOSA, Victor",
    "SOUSÂNDRADE, Joaquim de": "SOUSÂNDRADE",
    "SOUSÂNDRADE, Joaquim de Sousa Andrade": "SOUSÂNDRADE",
    "VICUÑA, Cecília": "VICUÑA, Cecilia",
    "WARCHAVCHIK, Gregorio": "WARCHAVCHIK, Gregori",
    "WEBERN, Anton von": "WEBERN, Anton",
    "WOOLF, Virgínia": "WOOLF, Virginia",
    "XAVIER": "XAVIER, Valêncio",
    "ÁVILA, Afonso": "ÁVILA, Affonso",
    
    # NOVAS REGRAS (LOTE 5 - Pente Fino e Duplicatas)
    "COSTA, Lúcio": "COSTA, Lucio",
    "SALVINO, Rômulo Valle": "SALVINO, Romulo Valle",
    "WESHLER-HENRY, Darren": "WERSHLER-HENRY, Darren",
    "BERNARDINI, Aurora": "BERNARDINI, Aurora Fornoni",
    "BERNARDINI, Aurora F": "BERNARDINI, Aurora Fornoni",
    "BERNARDINI, Aurora F.": "BERNARDINI, Aurora Fornoni",
    "KRUCHÔNIKH, Aleksiéi": "KRUTCHÔNIKH, Aleksiéi",
    "SANGUINETTI, Edoardo": "SANGUINETI, Edoardo",
    "DOCTOROVITCH, Fabio": "DOCTOROVICH, Fabio",
    "MATTOS, Gregório de": "MATOS, Gregório de",
    "BALLESTRINI, Nanni": "BALESTRINI, Nanni",
    "MAC CORMACK, Karen": "MACCORMACK, Karen",
    "SANDMAN, Marcelo": "SANDMANN, Marcelo",
    "GOMINGER, Eugen": "GOMRINGER, Eugen",
    "TALMAN, Warren": "TALLMAN, Warren",
    "FLICK, Robbert": "FLICK, Robert",
    "LAMBERT, G.M.": "LAMBERT, G. M.",
    "BESSA, A.S.": "BESSA, A. S.",
    "CÉSAR, Ana Cristina": "CESAR, Ana Cristina",
    "GUIMARAES, Fernando": "GUIMARÃES, Fernando",
    "MULLER, Adalberto": "MÜLLER, Adalberto",
    "BONVICINO, Regis": "BONVICINO, Régis",
    "HAUSSMAN, Raoul": "HAUSMANN, Raoul",
    "PADIN, Clemente": "PADÍN, Clemente",
    "BOK, Christian": "BÖK, Christian",
    "PALITO, Ronald": "POLITO, Ronald",
    "O’HARA, Frank": "O'HARA, Frank",
    "ELUARD, Paul": "ÉLUARD, Paul",
    "MALEVITCH, Kasimir": "MALEVICH, Kazimir",
    "ASSUMPÇÃO, Ademir": "ASSUNÇÃO, Ademir",
    "SOUZÂNDRADE": "SOUSÂNDRADE",
    "RUFFINI, Paolo": "RUFFILLI, Paolo",
    "SZAKOSI, Endre": "SZKAROSI, Endre",
    "REIS, Olga Carneiro": "REIS, Orfa Carneiro",
    "ARP, Jean": "ARP, Hans",
}

FIELDS_TO_CHECK = [
    "autores_colaboradores",
    "autores_citados",
    "tradutores",
    "nome_pessoal_como_assunto",
    "entidade_coletiva" # Just in case
]

def format_nome(nome):
    if not isinstance(nome, str):
        return nome
        
    original = nome.strip()
    
    # 1. Exact match
    if original in CANONICAL_AUTHORS:
        return CANONICAL_AUTHORS[original]
    
    # 2. Match with standardized spacing
    normalized_spacing = " ".join(original.split())
    if normalized_spacing in CANONICAL_AUTHORS:
        return CANONICAL_AUTHORS[normalized_spacing]

    return original

def process_file():
    if not os.path.exists(FILE_PATH):
        print(f"Erro: Arquivo {FILE_PATH} não encontrado.")
        return

    print("Carregando JSON...")
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    changes_count = 0
    
    for entry in data:
        for field in FIELDS_TO_CHECK:
            if field in entry and isinstance(entry[field], list):
                new_list = []
                list_changed = False
                for item in entry[field]:
                    new_item = format_nome(item)
                    new_list.append(new_item)
                    if new_item != item:
                        print(f"Corrigindo: '{item}' -> '{new_item}' (Revista {entry.get('n', '?')}, Reg {entry.get('registro', '?')})")
                        list_changed = True
                        changes_count += 1
                
                if list_changed:
                    entry[field] = new_list

    print(f"Total de correções: {changes_count}")
    
    if changes_count > 0:
        print("Salvando alterações...")
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("Concluído.")
    else:
        print("Nenhuma alteração necessária.")

if __name__ == "__main__":
    process_file()
