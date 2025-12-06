#!/bin/bash
PROJECT_DIR="/Users/williamfernandes/Documents/Doutorado/Doutorado Sibila 3.0"
cd "$PROJECT_DIR" || exit 1

if [ -d "venv" ]; then
    source venv/bin/activate
fi

clear
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🚀 NELIC.DEV - Ambiente de Desenvolvimento"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📍 Diretório: $PROJECT_DIR"
echo "🌐 URL: http://localhost:8502"
echo "🔑 Senha: 1234"
echo ""
echo "⚠️  Para encerrar: Ctrl+C"
echo ""
echo "Iniciando..."
echo ""

streamlit run sibila_code_21.py --server.port 8502 --browser.gatherUsageStats false
