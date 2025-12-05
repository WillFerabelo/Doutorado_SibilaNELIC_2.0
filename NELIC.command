#!/bin/bash

# Script para iniciar o Sistema NELIC - Versão Desenvolvimento 3.0
# Duplo clique neste arquivo para abrir o sistema

# Obtém o diretório onde o script está localizado
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navega para o diretório do projeto
cd "$DIR"

# Ativa o ambiente virtual se existir
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Abre o navegador automaticamente e inicia o Streamlit na porta 8502
echo "🚀 Iniciando Sistema NELIC - Desenvolvimento 3.0..."
echo "📍 Diretório: $DIR"
echo "🌐 O aplicativo será aberto em: http://localhost:8502"
echo ""
echo "⚠️  Para encerrar o sistema, pressione Ctrl+C nesta janela"
echo ""

# Inicia o Streamlit na porta 8502 (diferente da versão de produção)
streamlit run sibila_code_21.py --server.port 8502 --browser.gatherUsageStats false

# Mantém o terminal aberto após o encerramento
echo ""
echo "Sistema NELIC encerrado."
read -p "Pressione Enter para fechar esta janela..."
