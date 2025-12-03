import sys
from unittest.mock import MagicMock

# --- MOCKING DEPENDENCIES ---
# We must mock streamlit BEFORE importing the app
mock_st = MagicMock()
# Mock columns to return a list of context managers (mocks)
mock_st.columns.side_effect = lambda n: [MagicMock() for _ in range(n)] if isinstance(n, int) else [MagicMock() for _ in n]
# Mock tabs
mock_st.tabs.side_effect = lambda names: [MagicMock() for _ in names]
# Mock sidebar
mock_st.sidebar = MagicMock()

sys.modules['streamlit'] = mock_st
sys.modules['streamlit_option_menu'] = MagicMock()
# We want to let pandas and plotly run to check for data errors, but we don't want to open browser
# Plotly express returns a figure object. We can let it run.
# But if it tries to render, we might want to suppress.
# Actually, the code calls st.plotly_chart(fig). Our mock_st handles that.
# So we can import real plotly.

# --- IMPORTING APP ---
try:
    import sibila_code_21 as app
except ImportError:
    # If running from a different dir, might need to adjust path
    sys.path.append('.')
    import sibila_code_21 as app

import pandas as pd

def run_validation():
    print("--- INICIANDO VALIDAÇÃO DE INTEGRIDADE ---")
    
    # 1. CRIAR DADOS DE TESTE (MOCK)
    # Incluindo casos de borda: 0, 8-9, 12
    data = [
        {
            'n': '0', 
            'registro': 'R001',
            'vocabulario_controlado': 'Manifesto', 
            'titulo_artigo': 'Manifesto Inicial', 
            'resumo': 'Texto de fundação', 
            'paginas': '1-5',
            'palavras_chave': ['Vanguarda'],
            'iconografias': []
        },
        {
            'n': '8-9', 
            'registro': 'R002',
            'vocabulario_controlado': 'Ensaio', 
            'titulo_artigo': 'Análise Dupla', 
            'resumo': 'Um estudo sobre Sibila e sua influência', 
            'paginas': '10-25',
            'palavras_chave': ['Sibila', 'Poesia'],
            'iconografias': [{'tipo': 'Foto', 'descricao': 'Foto 1'}, {'tipo': 'Gráfico'}]
        },
        {
            'n': '12', 
            'registro': 'R003',
            'vocabulario_controlado': 'Poema', 
            'titulo_artigo': 'Versos Finais', 
            'resumo': '', 
            'paginas': '50',
            'palavras_chave': [],
            'iconografias': []
        },
        {
            'n': '10', 
            'registro': 'R004',
            'vocabulario_controlado': 'Crítica', 
            'titulo_artigo': 'Crítica Moderna', 
            'resumo': 'Revisão crítica', 
            'paginas': 'pp. 30-40',
            'palavras_chave': ['Modernismo'],
            'iconografias': []
        }
    ]
    df = pd.DataFrame(data)
    
    print(f"Dados criados. Linhas: {len(df)}")
    
    # 2. SIMULAR CARREGAMENTO E TIPAGEM (Lógica do main)
    print("Aplicando tipagem categórica...")
    if 'n' in df.columns:
        df['n'] = df['n'].astype(str)
        # Verifica se a constante existe
        if hasattr(app, 'ORDEM_SIBILA'):
            df['n'] = pd.Categorical(df['n'], categories=app.ORDEM_SIBILA, ordered=True)
            print("✅ Constante ORDEM_SIBILA encontrada e aplicada.")
        else:
            print("❌ ERRO: Constante ORDEM_SIBILA não encontrada no módulo.")
            return

    # Verifica ordem
    sorted_n = df.sort_values('n')['n'].tolist()
    print(f"Ordem após sort: {sorted_n}")
    expected_subsequence = ['0', '8-9', '10', '12']
    if sorted_n == expected_subsequence:
        print("✅ Ordenação estrutural correta.")
    else:
        print(f"❌ Ordenação incorreta. Esperado: {expected_subsequence}")

    # 3. TESTAR RELATÓRIOS
    
    # Relatório Sibila
    print("\n--- Testando Relatório Sibila ---")
    try:
        app.relatorio_sibila(df)
        print("✅ Executado com SUCESSO.")
    except Exception as e:
        print(f"❌ FALHA na execução: {e}")
        import traceback
        traceback.print_exc()

    # Relatório Manifesto
    print("\n--- Testando Relatório Manifesto ---")
    try:
        app.relatorio_manifesto(df)
        print("✅ Executado com SUCESSO.")
    except Exception as e:
        print(f"❌ FALHA na execução: {e}")
        import traceback
        traceback.print_exc()

    # Relatório Densidade
    print("\n--- Testando Relatório Densidade de Imagens ---")
    try:
        app.relatorio_densidade_paginas(df)
        print("✅ Executado com SUCESSO.")
    except Exception as e:
        print(f"❌ FALHA na execução: {e}")
        import traceback
        traceback.print_exc()

    # Relatório Mapa Colaboração (Volume de itens)
    print("\n--- Testando Relatório Volume de Itens ---")
    try:
        app.relatorio_mapa_colaboracao(df)
        print("✅ Executado com SUCESSO.")
    except Exception as e:
        print(f"❌ FALHA na execução: {e}")
        import traceback
        traceback.print_exc()

    print("\n--- VALIDAÇÃO CONCLUÍDA ---")

if __name__ == "__main__":
    run_validation()
