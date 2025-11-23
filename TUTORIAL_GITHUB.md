# 📖 Tutorial Completo: Como Colocar o Sistema NELIC Online

Este tutorial é para iniciantes completos no GitHub e no Streamlit Cloud.

---

## PARTE 1: Preparar o GitHub

### Passo 1: Criar Conta no GitHub (se ainda não tiver)

1. Acesse: https://github.com
2. Clique em "Sign up" (Criar conta)
3. Siga as instruções para criar sua conta
4. Confirme seu email

### Passo 2: Instalar o GitHub Desktop (Forma Mais Fácil)

1. Acesse: https://desktop.github.com
2. Baixe e instale o GitHub Desktop
3. Abra o aplicativo e faça login com sua conta GitHub

### Passo 3: Criar um Repositório

**Opção A: Via GitHub Desktop (Mais Fácil)**

1. Abra o GitHub Desktop
2. Clique em "File" → "New Repository"
3. Preencha:
   - **Name**: `sistema-nelic-sibila` (ou outro nome sem espaços)
   - **Description**: "Sistema de catalogação da revista Sibila - NELIC/UFSC"
   - **Local Path**: Escolha onde quer salvar (pode ser na pasta de Documentos)
   - ✅ Marque "Initialize this repository with a README"
4. Clique em "Create Repository"

**Opção B: Via Site do GitHub**

1. Acesse: https://github.com/new
2. Preencha:
   - **Repository name**: `sistema-nelic-sibila`
   - **Description**: "Sistema de catalogação da revista Sibila - NELIC/UFSC"
   - ✅ Marque "Public" (para poder usar Streamlit Cloud gratuito)
   - ✅ Marque "Add a README file"
3. Clique em "Create repository"

### Passo 4: Copiar os Arquivos para o Repositório

1. Abra o Finder
2. Vá até a pasta onde o GitHub Desktop criou o repositório
   - Normalmente em: `/Users/SEU_USUARIO/Documents/GitHub/sistema-nelic-sibila`
3. Copie TODOS estes arquivos da pasta do projeto para o repositório:
   - `sibila_code_21.py` ⭐ (arquivo principal)
   - `catalogo_sibila.json` ⭐ (banco de dados)
   - `PROMPT-EXTRACAO-JSON.md`
   - `requirements.txt` ⭐ (dependências)
   - `README.md`
   - `.gitignore`
   - Quaisquer outros arquivos que você criou

**IMPORTANTE**: NÃO copie:
- Arquivos `.bak`
- Backups com data no nome
- A pasta `Sistema NELIC.app`
- Arquivos de log

### Passo 5: Fazer o Primeiro Commit (Upload)

**Via GitHub Desktop:**

1. Abra o GitHub Desktop
2. Você verá todos os arquivos listados na aba "Changes"
3. No campo de texto embaixo (Summary), escreva: `Primeiro commit - Sistema NELIC`
4. Clique em "Commit to main"
5. Clique em "Publish repository" (ou "Push origin" se já publicou)
6. ✅ Mantenha marcado "Public"
7. Clique em "Publish Repository"

Pronto! Seu código agora está no GitHub! 🎉

---

## PARTE 2: Colocar Online com Streamlit Cloud

### Passo 1: Criar Conta no Streamlit Cloud

1. Acesse: https://share.streamlit.io
2. Clique em "Sign up" ou "Get started"
3. **IMPORTANTE**: Clique em "Continue with GitHub"
4. Autorize o Streamlit a acessar sua conta GitHub

### Passo 2: Deploy (Publicar) o Aplicativo

1. Após fazer login, clique em "New app" ou "Create app"
2. Preencha:
   - **Repository**: Selecione `SEU_USUARIO/sistema-nelic-sibila`
   - **Branch**: `main`
   - **Main file path**: `sibila_code_21.py`
3. Clique em "Deploy!"

### Passo 3: Aguardar

- O Streamlit Cloud vai:
  1. Ler seu código
  2. Instalar as dependências do `requirements.txt`
  3. Iniciar o aplicativo
- Isso leva 2-5 minutos na primeira vez

### Passo 4: Pronto! 🎉

Quando terminar, você terá:
- **URL público**: Algo como `https://seu-usuario-sistema-nelic-sibila.streamlit.app`
- O sistema rodando 24/7 na internet
- Acesso de qualquer lugar do mundo

---

## PARTE 3: Como Atualizar o Sistema

Sempre que você fizer mudanças no código:

### Via GitHub Desktop:

1. Abra o GitHub Desktop
2. Vá até seu repositório
3. Os arquivos modificados aparecem em "Changes"
4. Digite uma mensagem descrevendo a mudança (ex: "Correção de bug no formulário")
5. Clique em "Commit to main"
6. Clique em "Push origin"

🔄 O Streamlit Cloud detecta automaticamente e atualiza seu site!

---

## PARTE 4: Compartilhar o Sistema

Depois que o sistema estiver no ar:

1. Pegue a URL do Streamlit Cloud (ex: `https://seu-app.streamlit.app`)
2. Compartilhe com quem quiser!
3. Qualquer pessoa pode acessar sem precisar instalar nada

---

## 🆘 Problemas Comuns

### "Module not found"
- Verifique se o arquivo `requirements.txt` está no repositório
- Verifique se listou todas as bibliotecas necessárias

### "File not found: sibila_code_21.py"
- Certifique-se que o arquivo está na raiz do repositório (não em subpasta)
- Verifique se o nome está correto (com .py no final)

### Site muito lento
- O Streamlit Cloud gratuito tem recursos limitados
- É normal ser um pouco mais lento que no seu computador

### Dados não salvam
- **ATENÇÃO**: Por padrão, o Streamlit Cloud reinicia periodicamente
- Os dados salvos no JSON serão perdidos a cada reinício
- Solução na PARTE 5 abaixo

---

## PARTE 5: Persistência de Dados (IMPORTANTE!)

⚠️ **PROBLEMA**: O Streamlit Cloud gratuito não mantém arquivos salvos permanentemente.

### Solução 1: Usar Google Sheets (Recomendado)

O Streamlit pode conectar com Google Sheets para salvar dados permanentemente.
(Posso te ajudar a configurar isso se precisar)

### Solução 2: Download/Upload Manual

Continue usando o JSON, mas:
- Use a função "EXPORTAR" para baixar seus dados regularmente
- Faça backup no seu computador
- Para adicionar dados, use o GitHub Desktop para atualizar o JSON

### Solução 3: Usar Apenas para Visualização

- Mantenha a catalogação no seu computador (local)
- Use o site online apenas para:
  - Mostrar o sistema para outras pessoas
  - Consultar dados já catalogados
  - Gerar relatórios

---

## 📞 Precisa de Ajuda?

Se tiver dúvidas em qualquer passo, me avise! Posso:
- Te ajudar com comandos específicos
- Criar scripts automáticos para facilitar
- Configurar integração com Google Sheets para salvar dados online
- Resolver qualquer problema que aparecer

---

## 🎯 Próximos Passos Sugeridos

Depois que o básico estiver funcionando:

1. ✅ Configurar backup automático dos dados
2. ✅ Adicionar autenticação (controle de acesso)
3. ✅ Integrar com Google Sheets ou banco de dados online
4. ✅ Customizar o domínio (para ter uma URL personalizada)

