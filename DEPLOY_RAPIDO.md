# ⚡ Deploy Rápido - Render + Supabase

## 🎯 Resumo em 5 Passos

### ✅ PASSO 1: Supabase (5 minutos)
1. Acesse: https://supabase.com
2. Crie conta (use GitHub)
3. **New Project** → Nome: `debutante-festa`
4. Senha do banco: `[ANOTE!]`
5. Região: `South America (São Paulo)`
6. Aguarde 2 minutos...

### ✅ PASSO 2: Criar Tabelas (3 minutos)
1. Supabase → **SQL Editor**
2. **New Query**
3. Copie TODO o conteúdo de `init_db.sql`
4. **Run** → Sucesso!

### ✅ PASSO 3: Copiar URL do Banco (1 minuto)
1. Supabase → **Settings** → **Database**
2. Procure **"Connection string"**
3. Copie a **URI** completa
4. **ANOTE!** Você vai precisar!

Exemplo:
```
postgresql://postgres.abc123:SUASENHA@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

### ✅ PASSO 4: GitHub (5 minutos)

**Se não tem Git instalado**: https://git-scm.com/downloads

```bash
# No terminal, dentro da pasta debutante-app/

# 1. Inicializar
git init

# 2. Adicionar arquivos
git add .

# 3. Commit
git commit -m "Deploy inicial"

# 4. Criar repo no GitHub
# Acesse: https://github.com/new
# Nome: festa-debutante
# Clique "Create repository"

# 5. Conectar e enviar (substitua SEU-USUARIO)
git remote add origin https://github.com/SEU-USUARIO/festa-debutante.git
git branch -M main
git push -u origin main
```

### ✅ PASSO 5: Render (5 minutos)
1. Acesse: https://render.com
2. Login com GitHub
3. **New +** → **Web Service**
4. Selecione repositório `festa-debutante`
5. Configurações:
   - **Name**: `debutante-festa`
   - **Environment**: `Python 3`
   - **Build**: `pip install -r requirements.txt`
   - **Start**: `gunicorn app:app`
   - **Plan**: `Free`

6. **Environment Variables**:
   - `DATABASE_URL` = [Cole URI do Supabase]
   - `SESSION_SECRET` = [Clique "Generate"]

7. **Create Web Service**
8. ⏱️ Aguarde 5-10 minutos...

---

## 🎉 PRONTO!

Seu site estará em:
```
https://debutante-festa.onrender.com
```

**Login**: `/admin/login`
- Usuário: `admin`
- Senha: `admin123`

---

## 🔐 IMPORTANTE: Mudar Senha

### Opção 1: Via Script (Mais Fácil)
```bash
# Local
python generate_password.py minhasenha123

# Copie o SQL gerado
# Cole no Supabase SQL Editor
# Run
```

### Opção 2: Via SQL Direto
```python
# Execute localmente:
from werkzeug.security import generate_password_hash
print(generate_password_hash('SUA_NOVA_SENHA'))
```

Depois no Supabase SQL Editor:
```sql
UPDATE admin 
SET password_hash = 'COLE_HASH_AQUI' 
WHERE username = 'admin';
```

---

## ❌ Problemas Comuns

### 🔴 Site não abre
**Causa**: Primeira visita após hibernação  
**Solução**: Aguarde 30-60 segundos

### 🔴 "Application failed to start"
**Causa**: DATABASE_URL incorreta  
**Solução**: 
1. Render → Environment
2. Verifique DATABASE_URL
3. Deve incluir senha correta

### 🔴 "Database connection error"
**Causa**: Tabelas não criadas  
**Solução**:
1. Supabase → SQL Editor
2. Execute `init_db.sql` novamente

### 🔴 Login não funciona
**Causa**: Tabela admin vazia  
**Solução**:
```sql
-- No Supabase SQL Editor
DELETE FROM admin;
INSERT INTO admin (username, password_hash) 
VALUES ('admin', 'scrypt:32768:8:1$oKGZ8PqV5GvUhZKe$6a3e0d0f5e6c0d8a7f9e0c5a7f9e0c5a7f9e0c5a7f9e0c5a7f9e0c5a7f9e0c5a7f9e0c5a7f9e0c5a7f9e0c5a');
```

---

## 📊 Verificar Status

### Supabase
✅ Projeto criado  
✅ Tabelas criadas (6 tabelas)  
✅ Admin inserido  
✅ URL anotada  

### GitHub
✅ Repositório criado  
✅ Código enviado  
✅ Branch: main  

### Render
✅ Web Service criado  
✅ DATABASE_URL configurada  
✅ SESSION_SECRET configurada  
✅ Deploy bem-sucedido  
✅ Site acessível  

---

## 🎯 Próximos Passos

1. ✅ Acessar `/admin/login`
2. ✅ Mudar senha do admin
3. ✅ Configurar informações da festa
4. ✅ Adicionar convidados
5. ✅ Personalizar textos/cores
6. ✅ Compartilhar link!

---

## 💰 Custos

**Supabase**: Grátis (500MB banco)  
**Render**: Grátis (com hibernação)  
**GitHub**: Grátis  

**Total**: R$ 0,00/mês 🎉

---

## 🔗 Links Úteis

**Seu Site**: https://seu-projeto.onrender.com  
**Supabase**: https://supabase.com/dashboard  
**Render**: https://dashboard.render.com  
**GitHub**: https://github.com/seu-usuario/festa-debutante  

---

## 📞 Documentação Completa

Leia `DEPLOY_RENDER_SUPABASE.md` para:
- Troubleshooting detalhado
- Domínio personalizado
- Monitoramento
- Segurança avançada

---

**Criado com 💜 para festas inesquecíveis!**

**Tempo total**: ~20 minutos  
**Dificuldade**: ⭐⭐☆☆☆  
**Custo**: Grátis  
