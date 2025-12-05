# 📖 Como Usar o Sistema NELIC - Desenvolvimento 3.0

## 🎯 Formas de Iniciar o Sistema

### ✅ RECOMENDADO: Duplo clique no NELIC.app
1. No Finder, navegue até: `/Users/williamfernandes/Documents/Doutorado/Doutorado Sibila 3.0`
2. Dê duplo clique em **NELIC.app**
3. O Terminal abrirá automaticamente e o sistema iniciará
4. Seu navegador abrirá em: http://localhost:8502

### Alternativa: Duplo clique no NELIC.command
1. Dê duplo clique em **NELIC.command**
2. Funciona da mesma forma que o .app

### Linha de comando:
```bash
cd "/Users/williamfernandes/Documents/Doutorado/Doutorado Sibila 3.0"
streamlit run sibila_code_21.py --server.port 8502
```

## 🔄 Ambientes Separados

### Produção (não mexa!)
- **Diretório**: `/Users/williamfernandes/Documents/Doutorado/Doutorado_SibilaNELIC_2.0`
- **Porta**: 8501
- **URL**: http://localhost:8501
- **Uso**: Sistema funcional, não alterar

### Desenvolvimento (teste aqui!)
- **Diretório**: `/Users/williamfernandes/Documents/Doutorado/Doutorado Sibila 3.0`
- **Porta**: 8502
- **URL**: http://localhost:8502
- **Uso**: Testes e novas funcionalidades

## 💡 Você pode rodar ambos simultaneamente!

```bash
# Terminal 1 - Produção
cd "/Users/williamfernandes/Documents/Doutorado/Doutorado_SibilaNELIC_2.0"
streamlit run sibila_code_21.py

# Terminal 2 - Desenvolvimento
cd "/Users/williamfernandes/Documents/Doutorado/Doutorado Sibila 3.0"
streamlit run sibila_code_21.py --server.port 8502
```

## 🛠️ Workflow de Desenvolvimento

### 1. Fazer mudanças no código
Edite `sibila_code_21.py` no diretório **Doutorado Sibila 3.0**

### 2. Testar
Abra http://localhost:8502 e teste suas mudanças

### 3. Salvar mudanças
```bash
cd "/Users/williamfernandes/Documents/Doutorado/Doutorado Sibila 3.0"
git add .
git commit -m "Descrição das mudanças"
git push origin desenvolvimento
```

### 4. Quando estiver tudo funcionando
```bash
# Atualizar a versão de produção
git checkout main
git merge desenvolvimento
git push origin main

# Voltar para desenvolvimento
git checkout desenvolvimento
```

### 5. Atualizar a pasta de produção
```bash
cd "/Users/williamfernandes/Documents/Doutorado/Doutorado_SibilaNELIC_2.0"
git pull origin main
```

## ⚠️ Dicas Importantes

- ✅ Sempre teste no ambiente de desenvolvimento primeiro
- ✅ Use portas diferentes para não conflitar (8501 vs 8502)
- ✅ Faça commits frequentes com mensagens descritivas
- ✅ Só atualize a produção quando tudo estiver funcionando perfeitamente
- ❌ Nunca edite diretamente na pasta de produção

## 🆘 Problemas Comuns

### Porta já em uso
```bash
# Descobrir qual processo está usando a porta
lsof -ti:8502
# Matar o processo
kill -9 $(lsof -ti:8502)
```

### Mudanças não aparecem
- Pressione Ctrl+C no Terminal
- Inicie o sistema novamente
- Limpe o cache do navegador (Cmd+Shift+R)

### Aplicativo não abre
```bash
# Dê permissão de execução novamente
chmod +x "/Users/williamfernandes/Documents/Doutorado/Doutorado Sibila 3.0/NELIC.command"
chmod +x "/Users/williamfernandes/Documents/Doutorado/Doutorado Sibila 3.0/NELIC.app/Contents/MacOS/NELIC"
```

## 📞 Estrutura Final

```
/Users/williamfernandes/Documents/Doutorado/
├── Doutorado_SibilaNELIC_2.0/          # ← PRODUÇÃO (não mexer)
│   └── [arquivos do sistema]
│
└── Doutorado Sibila 3.0/               # ← DESENVOLVIMENTO (testar aqui)
    ├── NELIC.app                       # ← Duplo clique para abrir
    ├── NELIC.command                   # ← Alternativa
    ├── sibila_code_21.py               # ← Código principal
    ├── catalogo_sibila.json            # ← Base de dados
    ├── README_DEV.md                   # ← Documentação
    └── COMO_USAR.md                    # ← Este arquivo
```

---

**Pronto! Agora você tem um ambiente de desenvolvimento seguro e organizado! 🎉**
