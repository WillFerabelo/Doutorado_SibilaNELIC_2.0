#!/bin/bash
# Script de inicialização do Sistema NELIC
# Clique duas vezes neste arquivo para iniciar o sistema

# Define o caminho absoluto do projeto
PROJETO_DIR="/Users/williamfernandes/Documents/Doutorado/Doutorado_SibilaNELIC_2.0"
URL="http://localhost:8501"

# Navega para o diretório do projeto
cd "$PROJETO_DIR"

# Exibe mensagem inicial
echo "=========================================="
echo "  SISTEMA NELIC - Catalogação Sibila"
echo "=========================================="
echo ""

# Verifica se a porta 8501 já está em uso
if lsof -Pi :8501 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "✅ O sistema já está rodando!"
    echo ""
    echo "Abrindo o navegador em: $URL"
    echo ""
    open "$URL"
    echo "✓ Pronto! Se o navegador não abriu automaticamente,"
    echo "  acesse manualmente: $URL"
    echo ""
    echo "Para parar o sistema, feche a janela do Terminal que está"
    echo "executando o Streamlit."
    echo ""
    sleep 3
else
    echo "📂 Diretório: $PROJETO_DIR"
    echo "🚀 Iniciando o servidor..."
    echo ""
    echo "💡 Dica: O navegador abrirá automaticamente"
    echo ""

    # Inicia o Streamlit
    python3 -m streamlit run sibila_code_21.py --server.port=8501

    # Mantém a janela aberta em caso de erro
    echo ""
    read -p "Pressione ENTER para fechar..."
fi
