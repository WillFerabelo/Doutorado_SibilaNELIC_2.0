#!/usr/bin/env python3
"""
Script para gerar figuras do ANEXO A - Infraestrutura Digital da Pesquisa
Gera visualizações estáticas a partir dos dados do Sistema SD

Execute: python gerar_figuras_anexo.py
Saída: pasta 'figuras_anexo/' com os arquivos PNG
"""

import json
import os
from collections import Counter

# Criar pasta de saída
OUTPUT_DIR = "figuras_anexo"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Carregar dados
print("Carregando catálogo...")
with open("catalogo_sibila.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total de registros: {len(data)}")

# ============================================================
# FIGURA 1: Distribuição por tipologia textual (gráfico de barras)
# ============================================================
print("\nGerando Figura 1: Distribuição por tipologia...")

try:
    import plotly.express as px
    import plotly.io as pio

    # Contar tipologias
    tipologias = Counter(reg.get("vocabulario_controlado", "N/A") for reg in data)

    # Ordenar por frequência e pegar top 10
    top_tipologias = tipologias.most_common(10)
    labels = [t[0] for t in top_tipologias]
    values = [t[1] for t in top_tipologias]

    fig1 = px.bar(
        x=values,
        y=labels,
        orientation='h',
        title="Distribuição dos 450 registros por tipologia textual",
        labels={'x': 'Quantidade de registros', 'y': 'Tipologia'},
        color=values,
        color_continuous_scale='Blues'
    )
    fig1.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        yaxis={'categoryorder': 'total ascending'},
        font=dict(size=14),
        title_font_size=16,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    pio.write_image(fig1, f"{OUTPUT_DIR}/fig01_tipologias.png", width=900, height=600, scale=2)
    print(f"  ✓ Salvo: {OUTPUT_DIR}/fig01_tipologias.png")

except Exception as e:
    print(f"  ✗ Erro na Figura 1: {e}")

# ============================================================
# FIGURA 2: Distribuição por número da revista
# ============================================================
print("\nGerando Figura 2: Registros por edição...")

try:
    numeros = Counter(str(reg.get("n", "?")) for reg in data)

    # Ordenar numericamente
    ordem = ['0', '1', '2', '3', '4', '5', '6', '7', '8-9', '10', '11', '12']
    labels = [n for n in ordem if n in numeros]
    values = [numeros[n] for n in labels]

    fig2 = px.bar(
        x=labels,
        y=values,
        title="Quantidade de registros por número da revista Sibila (2001-2007)",
        labels={'x': 'Número da revista', 'y': 'Quantidade de registros'},
        color=values,
        color_continuous_scale='Greens'
    )
    fig2.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        font=dict(size=14),
        title_font_size=16
    )

    pio.write_image(fig2, f"{OUTPUT_DIR}/fig02_por_numero.png", width=900, height=500, scale=2)
    print(f"  ✓ Salvo: {OUTPUT_DIR}/fig02_por_numero.png")

except Exception as e:
    print(f"  ✗ Erro na Figura 2: {e}")

# ============================================================
# FIGURA 3: Top 20 autores mais citados
# ============================================================
print("\nGerando Figura 3: Autores mais citados...")

try:
    autores_citados = []
    for reg in data:
        if reg.get("autores_citados"):
            autores_citados.extend(reg["autores_citados"])

    top_citados = Counter(autores_citados).most_common(20)
    labels = [a[0] for a in top_citados]
    values = [a[1] for a in top_citados]

    fig3 = px.bar(
        x=values,
        y=labels,
        orientation='h',
        title="Top 20 autores mais citados na revista Sibila (total: 1.807 autores únicos)",
        labels={'x': 'Número de citações', 'y': 'Autor'},
        color=values,
        color_continuous_scale='Reds'
    )
    fig3.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        yaxis={'categoryorder': 'total ascending'},
        font=dict(size=12),
        title_font_size=14,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    pio.write_image(fig3, f"{OUTPUT_DIR}/fig03_autores_citados.png", width=900, height=700, scale=2)
    print(f"  ✓ Salvo: {OUTPUT_DIR}/fig03_autores_citados.png")

except Exception as e:
    print(f"  ✗ Erro na Figura 3: {e}")

# ============================================================
# FIGURA 4: Top 20 colaboradores
# ============================================================
print("\nGerando Figura 4: Colaboradores mais frequentes...")

try:
    colaboradores = []
    for reg in data:
        if reg.get("autores_colaboradores"):
            colaboradores.extend(reg["autores_colaboradores"])

    top_colab = Counter(colaboradores).most_common(20)
    labels = [a[0] for a in top_colab]
    values = [a[1] for a in top_colab]

    fig4 = px.bar(
        x=values,
        y=labels,
        orientation='h',
        title="Top 20 colaboradores mais frequentes (total: 245 colaboradores únicos)",
        labels={'x': 'Número de publicações', 'y': 'Colaborador'},
        color=values,
        color_continuous_scale='Purples'
    )
    fig4.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        yaxis={'categoryorder': 'total ascending'},
        font=dict(size=12),
        title_font_size=14,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    pio.write_image(fig4, f"{OUTPUT_DIR}/fig04_colaboradores.png", width=900, height=700, scale=2)
    print(f"  ✓ Salvo: {OUTPUT_DIR}/fig04_colaboradores.png")

except Exception as e:
    print(f"  ✗ Erro na Figura 4: {e}")

# ============================================================
# FIGURA 5: Top 15 palavras-chave
# ============================================================
print("\nGerando Figura 5: Palavras-chave mais frequentes...")

try:
    palavras = []
    for reg in data:
        if reg.get("palavras_chave"):
            palavras.extend(reg["palavras_chave"])

    top_palavras = Counter(palavras).most_common(15)
    labels = [p[0] for p in top_palavras]
    values = [p[1] for p in top_palavras]

    fig5 = px.bar(
        x=values,
        y=labels,
        orientation='h',
        title="Top 15 palavras-chave temáticas mais utilizadas",
        labels={'x': 'Frequência', 'y': 'Palavra-chave'},
        color=values,
        color_continuous_scale='Oranges'
    )
    fig5.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        yaxis={'categoryorder': 'total ascending'},
        font=dict(size=12),
        title_font_size=14
    )

    pio.write_image(fig5, f"{OUTPUT_DIR}/fig05_palavras_chave.png", width=900, height=550, scale=2)
    print(f"  ✓ Salvo: {OUTPUT_DIR}/fig05_palavras_chave.png")

except Exception as e:
    print(f"  ✗ Erro na Figura 5: {e}")

# ============================================================
# FIGURA 6: Grafo de citações (networkx + matplotlib)
# ============================================================
print("\nGerando Figura 6: Grafo de citações...")

try:
    import networkx as nx
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')

    # Criar grafo direcionado
    G = nx.DiGraph()

    # Adicionar arestas: colaborador -> autor citado
    for reg in data:
        colaboradores = reg.get("autores_colaboradores", [])
        citados = reg.get("autores_citados", [])

        for colab in colaboradores:
            for citado in citados:
                if G.has_edge(colab, citado):
                    G[colab][citado]['weight'] += 1
                else:
                    G.add_edge(colab, citado, weight=1)

    print(f"  Grafo: {G.number_of_nodes()} nós, {G.number_of_edges()} arestas")

    # Filtrar apenas nós com grau > 3 para visualização legível
    nodes_to_keep = [n for n in G.nodes() if G.degree(n) >= 5]
    G_filtered = G.subgraph(nodes_to_keep).copy()

    print(f"  Grafo filtrado (grau >= 5): {G_filtered.number_of_nodes()} nós, {G_filtered.number_of_edges()} arestas")

    # Calcular tamanho dos nós baseado em grau
    degrees = dict(G_filtered.degree())
    node_sizes = [degrees[n] * 20 for n in G_filtered.nodes()]

    # Identificar se é colaborador ou apenas citado
    colaboradores_set = set()
    for reg in data:
        colaboradores_set.update(reg.get("autores_colaboradores", []))

    node_colors = ['#e74c3c' if n in colaboradores_set else '#3498db' for n in G_filtered.nodes()]

    # Layout
    plt.figure(figsize=(16, 12))
    pos = nx.spring_layout(G_filtered, k=2, iterations=50, seed=42)

    # Desenhar
    nx.draw_networkx_edges(G_filtered, pos, alpha=0.2, edge_color='gray', arrows=True, arrowsize=8)
    nx.draw_networkx_nodes(G_filtered, pos, node_size=node_sizes, node_color=node_colors, alpha=0.8)

    # Labels apenas para nós com alto grau
    high_degree_nodes = {n: n.split(',')[0] for n in G_filtered.nodes() if degrees[n] >= 15}
    nx.draw_networkx_labels(G_filtered, pos, labels=high_degree_nodes, font_size=8)

    plt.title("Grafo de citações: colaboradores (vermelho) → autores citados (azul)\nFiltrado: apenas autores com 5+ conexões", fontsize=14)
    plt.axis('off')
    plt.tight_layout()

    plt.savefig(f"{OUTPUT_DIR}/fig06_grafo_citacoes.png", dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print(f"  ✓ Salvo: {OUTPUT_DIR}/fig06_grafo_citacoes.png")

except Exception as e:
    print(f"  ✗ Erro na Figura 6: {e}")

# ============================================================
# FIGURA 7: Distribuição de idiomas
# ============================================================
print("\nGerando Figura 7: Distribuição de idiomas...")

try:
    idiomas = Counter(reg.get("idioma_01", "N/A") for reg in data if reg.get("idioma_01"))

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
        'JAP': 'Japonês'
    }

    labels = [nome_idiomas.get(i, i) for i in idiomas.keys()]
    values = list(idiomas.values())

    fig7 = px.pie(
        names=labels,
        values=values,
        title="Distribuição dos registros por idioma principal",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig7.update_traces(textposition='inside', textinfo='percent+label')
    fig7.update_layout(font=dict(size=12), title_font_size=14)

    pio.write_image(fig7, f"{OUTPUT_DIR}/fig07_idiomas.png", width=700, height=500, scale=2)
    print(f"  ✓ Salvo: {OUTPUT_DIR}/fig07_idiomas.png")

except Exception as e:
    print(f"  ✗ Erro na Figura 7: {e}")

# ============================================================
# RESUMO FINAL
# ============================================================
print("\n" + "="*60)
print("FIGURAS GERADAS")
print("="*60)

figuras_geradas = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.png')]
for fig in sorted(figuras_geradas):
    caminho = os.path.join(OUTPUT_DIR, fig)
    tamanho = os.path.getsize(caminho) / 1024
    print(f"  {fig} ({tamanho:.1f} KB)")

print(f"\nTotal: {len(figuras_geradas)} figuras em '{OUTPUT_DIR}/'")
print("\nPara incluir no ANEXO A, copie as imagens para a pasta da tese.")
