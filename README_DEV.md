# 🚀 NELIC - Sistema de Catalogação Sibila 3.0 (Desenvolvimento)

Este é o ambiente de **desenvolvimento** do Sistema NELIC para testes e implementação de novas funcionalidades.

## 📂 Estrutura

- **Versão de Produção**: `/Users/williamfernandes/Documents/Doutorado/Doutorado_SibilaNELIC_2.0`
- **Versão de Desenvolvimento**: `/Users/williamfernandes/Documents/Doutorado/Doutorado Sibila 3.0` *(este diretório)*

## 🎯 Como Usar

### Opção 1: Duplo clique no aplicativo
Abra o arquivo **NELIC.app** para iniciar o sistema (porta 8502)

### Opção 2: Duplo clique no script
Abra o arquivo **NELIC.command** para iniciar via terminal (porta 8502)

### Opção 3: Linha de comando
```bash
cd "/Users/williamfernandes/Documents/Doutorado/Doutorado Sibila 3.0"
streamlit run sibila_code_21.py --server.port 8502
```

## 🔄 Workflow de Desenvolvimento

### 1. Trabalhe nesta versão
```bash
# Sempre certifique-se de estar na branch desenvolvimento
git branch  # deve mostrar * desenvolvimento
```

### 2. Teste suas mudanças
- Acesse: http://localhost:8502
- A versão de produção continua em: http://localhost:8501

### 3. Quando tudo estiver funcionando
```bash
# Faça commit das mudanças
git add .
git commit -m "Descrição das mudanças"
git push origin desenvolvimento
```

### 4. Para atualizar a produção
```bash
# Depois de testar tudo, faça merge para main
git checkout main
git merge desenvolvimento
git push origin main
```

## 🗂️ Arquivos Essenciais

- `sibila_code_21.py` - Código principal da aplicação
- `catalogo_sibila.json` - Base de dados do catálogo
- `diario_sibila.json` - Registro de atividades
- `requirements.txt` - Dependências Python
- `.streamlit/` - Configurações do Streamlit

## ⚠️ Importante

- Esta é a versão de **DESENVOLVIMENTO** - experimente à vontade!
- A versão de produção permanece intacta em outro diretório
- Use a porta 8502 para não conflitar com a produção (8501)
- Sempre teste aqui antes de fazer merge para main

## 📝 Branch Atual

Você está na branch: **desenvolvimento**
