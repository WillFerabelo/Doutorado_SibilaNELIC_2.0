#!/usr/bin/env python3
"""
Script para gerar arquivo Excel consolidado com dados do catálogo Sibila.
Reúne todos os CSVs em um único arquivo Excel com múltiplas abas.

Execute: python gerar_excel_consolidado.py
Saída: Anexos/dados_sibila_consolidado.xlsx
"""

import os
import pandas as pd
from datetime import datetime

# Configuração de caminhos
ANEXOS_DIR = "/Users/williamfernandes/Library/Mobile Documents/iCloud~md~obsidian/Documents/Doutorado/Tese - correção/Ordem da Tese/Anexos"

print("=" * 60)
print("GERADOR DE EXCEL CONSOLIDADO - TESE SIBILA")
print("=" * 60)

# Criar Excel writer
excel_path = os.path.join(ANEXOS_DIR, "dados_sibila_consolidado.xlsx")

# Mapeamento de CSVs para abas do Excel
csvs_para_abas = {
    "ranking_autores_citados.csv": "Autores Citados (1807)",
    "ranking_colaboradores.csv": "Colaboradores (245)",
    "ranking_tradutores.csv": "Tradutores (54)",
    "palavras_chave_frequencia.csv": "Palavras-Chave (200)",
    "vocabulario_controlado_frequencia.csv": "Tipologias",
    "distribuicao_por_numero.csv": "Por Número",
    "tipologias_por_numero.csv": "Tipologias x Número",
    "distribuicao_idiomas.csv": "Idiomas",
    "citacoes_por_fase.csv": "Citações por Fase",
    "palavras_chave_por_fase.csv": "Palavras por Fase",
    "colaboradores_por_fase.csv": "Colaboradores por Fase",
    "colaboradores_tambem_citados.csv": "Colab. Citados (148)",
    "colaboradores_nao_citados.csv": "Colab. Não Citados (97)"
}

print(f"\nCriando arquivo Excel: {excel_path}")

with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    for csv_file, aba_nome in csvs_para_abas.items():
        csv_path = os.path.join(ANEXOS_DIR, csv_file)
        if os.path.exists(csv_path):
            print(f"  Processando: {csv_file} → '{aba_nome}'")
            df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
            df.to_excel(writer, sheet_name=aba_nome[:31], index=False)  # Excel limita nomes a 31 chars
        else:
            print(f"  ⚠ Não encontrado: {csv_file}")

    # Aba de resumo/metadata
    print("  Criando aba de Resumo...")
    resumo_data = {
        'Métrica': [
            'Total de registros',
            'Colaboradores distintos',
            'Tradutores distintos',
            'Autores citados distintos',
            'Total de citações',
            'Palavras-chave distintas',
            'Aplicações de palavras-chave',
            'Colaboradores também citados',
            'Colaboradores NÃO citados',
            'Registros bilíngues',
            '',
            'Data de geração',
            'Fonte dos dados'
        ],
        'Valor': [
            450,
            245,
            54,
            1807,
            3312,
            200,
            1185,
            '148 (60,4%)',
            '97 (39,6%)',
            '65 (14,4%)',
            '',
            datetime.now().strftime('%d/%m/%Y %H:%M'),
            'catalogo_sibila.json (Sistema SD)'
        ]
    }
    df_resumo = pd.DataFrame(resumo_data)
    df_resumo.to_excel(writer, sheet_name='RESUMO', index=False)

print(f"\n✓ Excel salvo: {excel_path}")

# Verificar tamanho
tamanho = os.path.getsize(excel_path) / 1024
print(f"  Tamanho: {tamanho:.1f} KB")

print("\n" + "=" * 60)
print("ARQUIVO EXCEL CONSOLIDADO GERADO COM SUCESSO")
print("=" * 60)
print(f"""
Abas incluídas:
  1. RESUMO - Estatísticas consolidadas
  2. Autores Citados (1807) - Ranking completo
  3. Colaboradores (245) - Ranking por publicações
  4. Tradutores (54) - Ranking por traduções
  5. Palavras-Chave (200) - Frequência de uso
  6. Tipologias - Distribuição do vocabulário controlado
  7. Por Número - Registros por edição
  8. Tipologias x Número - Matriz cruzada
  9. Idiomas - Distribuição linguística
  10. Citações por Fase - Análise por fase editorial
  11. Palavras por Fase - Temas por fase editorial
  12. Colaboradores por Fase - Participação por fase
  13. Colab. Citados (148) - Dupla presença
  14. Colab. Não Citados (97) - Colaboradores sem citações

Arquivo: {excel_path}
""")
