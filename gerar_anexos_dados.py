#!/usr/bin/env python3
"""
Script para gerar arquivos CSV e Excel com dados do catálogo Sibila
para o capítulo de Análises Complementares da tese.

Execute: python gerar_anexos_dados.py
Saída: pasta 'Anexos/' com os arquivos CSV e Excel
"""

import json
import os
from collections import Counter
from datetime import datetime

# Configuração de caminhos
CATALOGO_PATH = "catalogo_sibila.json"
OUTPUT_DIR = "/Users/williamfernandes/Library/Mobile Documents/iCloud~md~obsidian/Documents/Doutorado/Tese - correção/Ordem da Tese/Anexos"

# Criar pasta de saída se não existir
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Carregar dados
print("=" * 60)
print("GERADOR DE ANEXOS DE DADOS - TESE SIBILA")
print("=" * 60)
print(f"\nCarregando catálogo de: {CATALOGO_PATH}")

with open(CATALOGO_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total de registros: {len(data)}")

# ============================================================
# 1. RANKING COMPLETO DE AUTORES CITADOS
# ============================================================
print("\n" + "-" * 60)
print("1. Gerando ranking de autores citados...")

autores_citados = []
citacoes_por_numero = {}  # Para análise por fase

for reg in data:
    numero = str(reg.get("n", "?"))
    citados = reg.get("autores_citados", [])
    if citados:
        autores_citados.extend(citados)
        # Contagem por número
        if numero not in citacoes_por_numero:
            citacoes_por_numero[numero] = []
        citacoes_por_numero[numero].extend(citados)

ranking_citados = Counter(autores_citados).most_common()
print(f"   Total de autores citados distintos: {len(ranking_citados)}")
print(f"   Total de citações: {len(autores_citados)}")

# Salvar CSV
csv_path = os.path.join(OUTPUT_DIR, "ranking_autores_citados.csv")
with open(csv_path, "w", encoding="utf-8") as f:
    f.write("posicao;autor;citacoes;percentual\n")
    total = len(autores_citados)
    for i, (autor, count) in enumerate(ranking_citados, 1):
        percentual = (count / total) * 100
        f.write(f"{i};{autor};{count};{percentual:.2f}%\n")

print(f"   ✓ Salvo: {csv_path}")

# Top 10 para verificação
print("   Top 10 autores citados:")
for i, (autor, count) in enumerate(ranking_citados[:10], 1):
    print(f"      {i}. {autor}: {count}")

# ============================================================
# 2. FREQUÊNCIA DE PALAVRAS-CHAVE
# ============================================================
print("\n" + "-" * 60)
print("2. Gerando frequência de palavras-chave...")

palavras_chave = []
palavras_por_numero = {}

for reg in data:
    numero = str(reg.get("n", "?"))
    pcs = reg.get("palavras_chave", [])
    if pcs:
        palavras_chave.extend(pcs)
        if numero not in palavras_por_numero:
            palavras_por_numero[numero] = []
        palavras_por_numero[numero].extend(pcs)

ranking_palavras = Counter(palavras_chave).most_common()
print(f"   Total de palavras-chave distintas: {len(ranking_palavras)}")
print(f"   Total de aplicações: {len(palavras_chave)}")

# Salvar CSV
csv_path = os.path.join(OUTPUT_DIR, "palavras_chave_frequencia.csv")
with open(csv_path, "w", encoding="utf-8") as f:
    f.write("posicao;palavra_chave;frequencia;percentual\n")
    total = len(palavras_chave)
    for i, (palavra, count) in enumerate(ranking_palavras, 1):
        percentual = (count / total) * 100
        f.write(f"{i};{palavra};{count};{percentual:.2f}%\n")

print(f"   ✓ Salvo: {csv_path}")

# Top 10 para verificação
print("   Top 10 palavras-chave:")
for i, (palavra, count) in enumerate(ranking_palavras[:10], 1):
    print(f"      {i}. {palavra}: {count}")

# ============================================================
# 3. DISTRIBUIÇÃO POR NÚMERO DA REVISTA
# ============================================================
print("\n" + "-" * 60)
print("3. Gerando distribuição por número...")

# Contagem de registros por número
registros_por_numero = Counter(str(reg.get("n", "?")) for reg in data)

# Contagem de tipologias por número
tipologias_por_numero = {}
for reg in data:
    numero = str(reg.get("n", "?"))
    tipologia = reg.get("vocabulario_controlado", "N/A")
    if numero not in tipologias_por_numero:
        tipologias_por_numero[numero] = Counter()
    tipologias_por_numero[numero][tipologia] += 1

# Ordem dos números
ordem_numeros = ['0', '1', '2', '3', '4', '5', '6', '7', '8-9', '10', '11', '12']

# Salvar CSV de registros por número
csv_path = os.path.join(OUTPUT_DIR, "distribuicao_por_numero.csv")
with open(csv_path, "w", encoding="utf-8") as f:
    f.write("numero;total_registros;fase_editorial\n")
    for num in ordem_numeros:
        if num in registros_por_numero:
            # Classificar fase editorial
            if num in ['0', '1']:
                fase = "Fundacional"
            elif num in ['2', '3', '4']:
                fase = "Expansão"
            elif num in ['5', '6', '7']:
                fase = "Consolidação"
            else:
                fase = "Sobrevivência/Institucionalização"
            f.write(f"{num};{registros_por_numero[num]};{fase}\n")

print(f"   ✓ Salvo: {csv_path}")

# Salvar CSV detalhado de tipologias por número
csv_path = os.path.join(OUTPUT_DIR, "tipologias_por_numero.csv")

# Coletar todas as tipologias
todas_tipologias = set()
for tipologias in tipologias_por_numero.values():
    todas_tipologias.update(tipologias.keys())
todas_tipologias = sorted(todas_tipologias)

with open(csv_path, "w", encoding="utf-8") as f:
    # Cabeçalho
    f.write("numero;" + ";".join(todas_tipologias) + ";total\n")
    for num in ordem_numeros:
        if num in tipologias_por_numero:
            valores = [str(tipologias_por_numero[num].get(tip, 0)) for tip in todas_tipologias]
            total = sum(tipologias_por_numero[num].values())
            f.write(f"{num};" + ";".join(valores) + f";{total}\n")

print(f"   ✓ Salvo: {csv_path}")

# ============================================================
# 4. RANKING DE COLABORADORES
# ============================================================
print("\n" + "-" * 60)
print("4. Gerando ranking de colaboradores...")

colaboradores = []
colaboradores_por_numero = {}

for reg in data:
    numero = str(reg.get("n", "?"))
    colabs = reg.get("autores_colaboradores", [])
    if colabs:
        colaboradores.extend(colabs)
        if numero not in colaboradores_por_numero:
            colaboradores_por_numero[numero] = []
        colaboradores_por_numero[numero].extend(colabs)

ranking_colaboradores = Counter(colaboradores).most_common()
print(f"   Total de colaboradores distintos: {len(ranking_colaboradores)}")
print(f"   Total de colaborações: {len(colaboradores)}")

# Salvar CSV
csv_path = os.path.join(OUTPUT_DIR, "ranking_colaboradores.csv")
with open(csv_path, "w", encoding="utf-8") as f:
    f.write("posicao;colaborador;publicacoes;percentual\n")
    total = len(colaboradores)
    for i, (colab, count) in enumerate(ranking_colaboradores, 1):
        percentual = (count / total) * 100
        f.write(f"{i};{colab};{count};{percentual:.2f}%\n")

print(f"   ✓ Salvo: {csv_path}")

# Top 10 para verificação
print("   Top 10 colaboradores:")
for i, (colab, count) in enumerate(ranking_colaboradores[:10], 1):
    print(f"      {i}. {colab}: {count}")

# ============================================================
# 5. RANKING DE TRADUTORES
# ============================================================
print("\n" + "-" * 60)
print("5. Gerando ranking de tradutores...")

tradutores = []
for reg in data:
    trads = reg.get("tradutores", [])
    if trads:
        tradutores.extend(trads)

ranking_tradutores = Counter(tradutores).most_common()
print(f"   Total de tradutores distintos: {len(ranking_tradutores)}")
print(f"   Total de traduções: {len(tradutores)}")

# Salvar CSV
csv_path = os.path.join(OUTPUT_DIR, "ranking_tradutores.csv")
with open(csv_path, "w", encoding="utf-8") as f:
    f.write("posicao;tradutor;traducoes;percentual\n")
    total = len(tradutores) if tradutores else 1
    for i, (trad, count) in enumerate(ranking_tradutores, 1):
        percentual = (count / total) * 100
        f.write(f"{i};{trad};{count};{percentual:.2f}%\n")

print(f"   ✓ Salvo: {csv_path}")

# ============================================================
# 6. DISTRIBUIÇÃO POR IDIOMA
# ============================================================
print("\n" + "-" * 60)
print("6. Gerando distribuição por idioma...")

idiomas_primarios = Counter(reg.get("idioma_01", "N/A") for reg in data if reg.get("idioma_01"))
idiomas_secundarios = Counter(reg.get("idioma_02", "N/A") for reg in data if reg.get("idioma_02"))

# Mapeamento de códigos para nomes
nome_idiomas = {
    'POR': 'Português',
    'ING': 'Inglês',
    'ESP': 'Espanhol',
    'FRA': 'Francês',
    'ITA': 'Italiano',
    'ALE': 'Alemão',
    'RUS': 'Russo',
    'CHI': 'Chinês',
    'JAP': 'Japonês',
    'CAT': 'Catalão',
    'FIN': 'Finlandês',
    'GRE': 'Grego'
}

# Salvar CSV
csv_path = os.path.join(OUTPUT_DIR, "distribuicao_idiomas.csv")
with open(csv_path, "w", encoding="utf-8") as f:
    f.write("codigo;idioma;registros_primario;registros_secundario;total\n")
    todos_idiomas = set(idiomas_primarios.keys()) | set(idiomas_secundarios.keys())
    for codigo in sorted(todos_idiomas):
        if codigo and codigo != "N/A":
            nome = nome_idiomas.get(codigo, codigo)
            prim = idiomas_primarios.get(codigo, 0)
            sec = idiomas_secundarios.get(codigo, 0)
            f.write(f"{codigo};{nome};{prim};{sec};{prim + sec}\n")

print(f"   ✓ Salvo: {csv_path}")

# Registros bilíngues
bilingues = sum(1 for reg in data if reg.get("idioma_02"))
print(f"   Registros bilíngues: {bilingues} ({bilingues/len(data)*100:.1f}%)")

# ============================================================
# 7. VOCABULÁRIO CONTROLADO - DISTRIBUIÇÃO GERAL
# ============================================================
print("\n" + "-" * 60)
print("7. Gerando distribuição de vocabulário controlado...")

tipologias = Counter(reg.get("vocabulario_controlado", "N/A") for reg in data)
ranking_tipologias = tipologias.most_common()

# Salvar CSV
csv_path = os.path.join(OUTPUT_DIR, "vocabulario_controlado_frequencia.csv")
with open(csv_path, "w", encoding="utf-8") as f:
    f.write("posicao;tipologia;quantidade;percentual\n")
    total = len(data)
    for i, (tip, count) in enumerate(ranking_tipologias, 1):
        percentual = (count / total) * 100
        f.write(f"{i};{tip};{count};{percentual:.2f}%\n")

print(f"   ✓ Salvo: {csv_path}")

# ============================================================
# 8. CITAÇÕES POR FASE EDITORIAL
# ============================================================
print("\n" + "-" * 60)
print("8. Gerando análise de citações por fase editorial...")

fases = {
    'Fundacional (0-1)': ['0', '1'],
    'Expansão (2-4)': ['2', '3', '4'],
    'Consolidação (5-7)': ['5', '6', '7'],
    'Sobrevivência (8-12)': ['8-9', '10', '11', '12']
}

csv_path = os.path.join(OUTPUT_DIR, "citacoes_por_fase.csv")
with open(csv_path, "w", encoding="utf-8") as f:
    f.write("fase;total_citacoes;autores_distintos;media_por_registro;top_5_citados\n")

    for fase_nome, numeros in fases.items():
        citacoes_fase = []
        registros_fase = 0
        for num in numeros:
            if num in citacoes_por_numero:
                citacoes_fase.extend(citacoes_por_numero[num])
            registros_fase += registros_por_numero.get(num, 0)

        if citacoes_fase:
            distintos = len(set(citacoes_fase))
            media = len(citacoes_fase) / registros_fase if registros_fase else 0
            top_5 = Counter(citacoes_fase).most_common(5)
            top_5_str = " | ".join([f"{a}: {c}" for a, c in top_5])
            f.write(f"{fase_nome};{len(citacoes_fase)};{distintos};{media:.2f};{top_5_str}\n")

print(f"   ✓ Salvo: {csv_path}")

# ============================================================
# 9. PALAVRAS-CHAVE POR FASE EDITORIAL
# ============================================================
print("\n" + "-" * 60)
print("9. Gerando análise de palavras-chave por fase editorial...")

csv_path = os.path.join(OUTPUT_DIR, "palavras_chave_por_fase.csv")
with open(csv_path, "w", encoding="utf-8") as f:
    f.write("fase;total_aplicacoes;termos_distintos;top_10_termos\n")

    for fase_nome, numeros in fases.items():
        palavras_fase = []
        for num in numeros:
            if num in palavras_por_numero:
                palavras_fase.extend(palavras_por_numero[num])

        if palavras_fase:
            distintos = len(set(palavras_fase))
            top_10 = Counter(palavras_fase).most_common(10)
            top_10_str = " | ".join([f"{p}: {c}" for p, c in top_10])
            f.write(f"{fase_nome};{len(palavras_fase)};{distintos};{top_10_str}\n")

print(f"   ✓ Salvo: {csv_path}")

# ============================================================
# 10. COLABORADORES POR FASE EDITORIAL
# ============================================================
print("\n" + "-" * 60)
print("10. Gerando análise de colaboradores por fase editorial...")

csv_path = os.path.join(OUTPUT_DIR, "colaboradores_por_fase.csv")
with open(csv_path, "w", encoding="utf-8") as f:
    f.write("fase;total_colaboracoes;colaboradores_distintos;top_10_colaboradores\n")

    for fase_nome, numeros in fases.items():
        colabs_fase = []
        for num in numeros:
            if num in colaboradores_por_numero:
                colabs_fase.extend(colaboradores_por_numero[num])

        if colabs_fase:
            distintos = len(set(colabs_fase))
            top_10 = Counter(colabs_fase).most_common(10)
            top_10_str = " | ".join([f"{c}: {n}" for c, n in top_10])
            f.write(f"{fase_nome};{len(colabs_fase)};{distintos};{top_10_str}\n")

print(f"   ✓ Salvo: {csv_path}")

# ============================================================
# 11. MATRIZ DE CO-OCORRÊNCIA (COLABORADORES CITADOS)
# ============================================================
print("\n" + "-" * 60)
print("11. Identificando colaboradores que também são citados...")

colaboradores_set = set(c for c, _ in ranking_colaboradores)
citados_set = set(c for c, _ in ranking_citados)
colaboradores_citados = colaboradores_set & citados_set

csv_path = os.path.join(OUTPUT_DIR, "colaboradores_tambem_citados.csv")
with open(csv_path, "w", encoding="utf-8") as f:
    f.write("autor;publicacoes_como_colaborador;citacoes_como_autor_citado;total\n")

    dados_cruzados = []
    for autor in colaboradores_citados:
        pub = dict(ranking_colaboradores).get(autor, 0)
        cit = dict(ranking_citados).get(autor, 0)
        dados_cruzados.append((autor, pub, cit, pub + cit))

    # Ordenar por total
    dados_cruzados.sort(key=lambda x: x[3], reverse=True)

    for autor, pub, cit, total in dados_cruzados:
        f.write(f"{autor};{pub};{cit};{total}\n")

print(f"   ✓ Salvo: {csv_path}")
print(f"   Colaboradores que também são citados: {len(colaboradores_citados)}")

# ============================================================
# RESUMO FINAL
# ============================================================
print("\n" + "=" * 60)
print("ARQUIVOS GERADOS")
print("=" * 60)

arquivos_gerados = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.csv')]
for arq in sorted(arquivos_gerados):
    caminho = os.path.join(OUTPUT_DIR, arq)
    tamanho = os.path.getsize(caminho) / 1024
    print(f"  {arq} ({tamanho:.1f} KB)")

print(f"\nTotal: {len(arquivos_gerados)} arquivos CSV em '{OUTPUT_DIR}/'")

# ============================================================
# ESTATÍSTICAS CONSOLIDADAS
# ============================================================
print("\n" + "=" * 60)
print("ESTATÍSTICAS CONSOLIDADAS")
print("=" * 60)
print(f"""
Registros totais: {len(data)}
Colaboradores distintos: {len(ranking_colaboradores)}
Tradutores distintos: {len(ranking_tradutores)}
Autores citados distintos: {len(ranking_citados)}
Total de citações: {len(autores_citados)}
Palavras-chave distintas: {len(ranking_palavras)}
Total de aplicações de palavras-chave: {len(palavras_chave)}
Colaboradores também citados: {len(colaboradores_citados)}
Registros bilíngues: {bilingues} ({bilingues/len(data)*100:.1f}%)

Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
""")
