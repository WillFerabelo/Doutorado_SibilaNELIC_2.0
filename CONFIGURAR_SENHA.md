# 🔐 Configurar Sistema de Senhas

## ✅ O que foi implementado:

1. **Sistema de autenticação por senha**
2. **Menu adaptativo**: visitantes veem menos opções
3. **Proteção de áreas sensíveis**: CATALOGAÇÃO e EXPORTAR requerem senha
4. **Avisos automáticos** sobre salvamento de dados na nuvem

---

## 🏠 Uso Local (no seu computador)

### Senha Padrão Local:
```
nelic2025
```

Você pode mudar essa senha editando o arquivo `sibila_code_21.py` na linha:
```python
senha_correta = "nelic2025"  # Altere aqui
```

---

## ☁️ Uso no Streamlit Cloud (online)

### Passo 1: Fazer o Deploy

1. Siga as instruções do `TUTORIAL_GITHUB.md`
2. Faça o deploy do app no Streamlit Cloud
3. Aguarde o app ficar online

### Passo 2: Configurar a Senha Secreta

1. No painel do Streamlit Cloud, clique no seu app
2. Clique no menu **⋮** (três pontinhos) → **Settings**
3. Na aba lateral, clique em **Secrets**
4. Cole este conteúdo no editor:

```toml
SENHA_ADMIN = "sua_senha_super_segura_aqui"
```

5. Clique em **Save**
6. O app vai reiniciar automaticamente

**IMPORTANTE**:
- ⚠️ NUNCA compartilhe essa senha publicamente
- ⚠️ NUNCA envie o arquivo `.streamlit/secrets.toml` para o GitHub
- ✅ O `.gitignore` já está configurado para ignorar esse arquivo

---

## 🎯 Como Funciona:

### Para Visitantes (sem senha):

**Podem acessar:**
- ✅ NELIC (apresentação)
- ✅ FICHAS & NOTAS (visualizar registros)
- ✅ EXPLORAR DADOS
- ✅ RELATÓRIOS
- ✅ ANÁLISE COMPARATIVA
- ✅ QUALIDADE DOS DADOS
- ✅ METODOLOGIA
- ✅ MAIS DADOS

**NÃO podem acessar:**
- ❌ CATALOGAÇÃO (adicionar/editar registros)
- ❌ DIÁRIO DE PESQUISA
- ❌ EXPORTAR (download de dados)

### Para Catalogadores (com senha):

**Acesso completo a TODAS as funcionalidades**, incluindo:
- ✅ CATALOGAÇÃO
- ✅ DIÁRIO DE PESQUISA
- ✅ EXPORTAR

---

## 🔄 Trocar a Senha

### Local:
1. Edite o arquivo `sibila_code_21.py`
2. Localize a linha: `senha_correta = "nelic2025"`
3. Altere para sua nova senha
4. Salve o arquivo

### Streamlit Cloud:
1. Vá em Settings → Secrets
2. Altere o valor de `SENHA_ADMIN`
3. Salve
4. Pronto!

---

## 🆘 Solução de Problemas

### "Senha não funciona no Streamlit Cloud"
- Verifique se configurou os Secrets corretamente
- Certifique-se de que não tem espaços extras na senha
- Aguarde o app reiniciar após salvar os Secrets

### "Quero remover a senha"
- Não recomendado para deploy público!
- Se realmente quiser, comente as linhas de verificação de senha no código

### "Esqueci a senha"
- **Local**: Veja no código (linha do `senha_correta`)
- **Cloud**: Veja em Settings → Secrets no painel do Streamlit

---

## 📝 Recomendações de Segurança

1. ✅ Use senhas fortes (mínimo 12 caracteres)
2. ✅ Não compartilhe a senha por email/mensagem
3. ✅ Troque a senha periodicamente
4. ✅ Use senhas diferentes para local e cloud
5. ✅ Nunca commite o arquivo `secrets.toml` no Git

---

## 🎓 Dica Extra: Múltiplos Usuários

Se quiser dar acesso a diferentes pessoas, você pode:

1. Criar senhas diferentes para cada nível de acesso
2. Usar um serviço de autenticação (mais avançado)
3. Manter um registro de quem tem acesso

Para implementar isso, me avise que posso ajudar!

---

**Senha padrão atual (local)**: `nelic2025`

Lembre-se de trocar essa senha antes de fazer o deploy público! 🔒
