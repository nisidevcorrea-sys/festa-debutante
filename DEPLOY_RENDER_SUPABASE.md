# 🚀 Guia Completo: Deploy no Render + Supabase

## 📋 Índice
1. [Criar conta no Supabase](#1-criar-conta-no-supabase)
2. [Configurar banco de dados](#2-configurar-banco-de-dados)
3. [Preparar projeto para deploy](#3-preparar-projeto-para-deploy)
4. [Deploy no Render](#4-deploy-no-render)
5. [Configurar variáveis de ambiente](#5-configurar-variáveis-de-ambiente)
6. [Verificar funcionamento](#6-verificar-funcionamento)

---

## 1️⃣ Criar Conta no Supabase

### Passo 1.1: Acessar Supabase
1. Acesse: https://supabase.com
2. Clique em **"Start your project"**
3. Faça login com GitHub (recomendado) ou email

### Passo 1.2: Criar novo projeto
1. Clique em **"New Project"**
2. Preencha:
   - **Name**: `debutante-festa` (ou nome de sua preferência)
   - **Database Password**: Crie uma senha forte (ANOTE ESSA SENHA!)
   - **Region**: Escolha `South America (São Paulo)` para melhor performance
   - **Pricing Plan**: Free (gratuito)
3. Clique em **"Create new project"**
4. ⏱️ Aguarde 2-3 minutos enquanto o projeto é criado

---

## 2️⃣ Configurar Banco de Dados

### Passo 2.1: Obter credenciais de conexão
1. No painel do Supabase, clique em **"Settings"** (ícone de engrenagem)
2. Clique em **"Database"**
3. Role até **"Connection string"**
4. Copie a **URI** que aparece em **"URI"** ou **"Connection pooling"**

Ela será algo assim:
```
postgresql://postgres.xxxxxxxxxxxx:[SUA-SENHA]@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

### Passo 2.2: Anotar informações importantes
📝 Anote estas informações:

```
Host: aws-0-sa-east-1.pooler.supabase.com
Database: postgres
User: postgres.xxxxxxxxxxxx
Password: [A SENHA QUE VOCÊ CRIOU]
Port: 6543
```

### Passo 2.3: Criar tabelas (IMPORTANTE!)
1. No painel Supabase, clique em **"SQL Editor"** no menu lateral
2. Clique em **"New query"**
3. Cole o seguinte SQL e clique em **"Run"**:

```sql
-- Criar tabela de administradores
CREATE TABLE admin (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

-- Criar tabela de grupos de convidados
CREATE TABLE guest_group (
    id SERIAL PRIMARY KEY,
    group_name VARCHAR(100) NOT NULL,
    description VARCHAR(255)
);

-- Criar tabela de convidados
CREATE TABLE guest (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    group_id INTEGER REFERENCES guest_group(id) ON DELETE SET NULL,
    status VARCHAR(20) DEFAULT 'pendente',
    confirmed_at TIMESTAMP,
    plus_one BOOLEAN DEFAULT FALSE,
    notes TEXT
);

-- Criar tabela de informações do local
CREATE TABLE venue_info (
    id SERIAL PRIMARY KEY,
    debutante_name VARCHAR(100) NOT NULL,
    event_date TIMESTAMP NOT NULL,
    venue_name VARCHAR(200),
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(20),
    google_maps_link VARCHAR(500),
    ceremony_time VARCHAR(20),
    party_time VARCHAR(20),
    dress_code VARCHAR(100),
    theme VARCHAR(100),
    color_scheme VARCHAR(100),
    additional_info TEXT
);

-- Criar tabela de lista de presentes
CREATE TABLE gift_registry (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(200) NOT NULL,
    description TEXT,
    price FLOAT,
    store_link VARCHAR(500),
    store_name VARCHAR(100),
    category VARCHAR(50),
    priority VARCHAR(20),
    reserved_by VARCHAR(100),
    reserved BOOLEAN DEFAULT FALSE
);

-- Criar tabela de corte de honra
CREATE TABLE court (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL,
    photo_url VARCHAR(500),
    bio TEXT,
    order_position INTEGER
);

-- Inserir admin padrão (senha: admin123)
INSERT INTO admin (username, password_hash) VALUES 
('admin', 'scrypt:32768:8:1$9k4JYl0KxZ7g9tGv$e0a1e4c5f7d1e4f1c9e0f1e4c5f7d1e4f1c9e0f1e4c5f7d1e4f1c9e0f1e4c5f7d1e4f1c9e0f1e4c5f7d1e4');

-- Verificar criação
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;
```

✅ Você deve ver mensagem "Success. No rows returned" ou similar

---

## 3️⃣ Preparar Projeto para Deploy

### Passo 3.1: Baixar arquivos atualizados
Os arquivos já estão preparados! Você tem dois arquivos importantes:

1. **`requirements.txt`** - Já está pronto
2. **`render.yaml`** - Novo arquivo de configuração

### Passo 3.2: Criar arquivo render.yaml
Na raiz do projeto, crie o arquivo `render.yaml`:

```yaml
services:
  - type: web
    name: debutante-festa
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: DATABASE_URL
        sync: false
      - key: SESSION_SECRET
        generateValue: true
```

### Passo 3.3: Atualizar requirements.txt
Certifique-se que tem estas linhas:

```txt
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
psycopg2-binary==2.9.9
python-dotenv==1.0.0
Werkzeug==3.0.1
gunicorn==21.2.0
```

---

## 4️⃣ Deploy no Render

### Passo 4.1: Criar conta no Render
1. Acesse: https://render.com
2. Clique em **"Get Started"**
3. Faça login com GitHub (recomendado)

### Passo 4.2: Conectar ao GitHub

**Opção A: Se você tem o código no GitHub**
1. No Render, clique em **"New +"** → **"Web Service"**
2. Conecte seu repositório GitHub
3. Selecione o repositório do projeto

**Opção B: Se NÃO tem no GitHub (mais fácil)**
1. Primeiro, crie um repositório no GitHub:
   - Acesse https://github.com/new
   - Nome: `festa-debutante`
   - Deixe público ou privado
   - Clique em "Create repository"

2. No seu computador, no terminal:
```bash
cd debutante-app

# Inicializar git
git init

# Adicionar arquivos
git add .

# Fazer commit
git commit -m "Deploy inicial"

# Adicionar repositório remoto (substitua SEU-USUARIO)
git remote add origin https://github.com/SEU-USUARIO/festa-debutante.git

# Enviar para GitHub
git branch -M main
git push -u origin main
```

### Passo 4.3: Configurar Web Service no Render
1. No Render, clique em **"New +"** → **"Web Service"**
2. Selecione seu repositório
3. Configure:
   - **Name**: `debutante-festa` (ou seu nome)
   - **Region**: `Oregon (US West)` (gratuito)
   - **Branch**: `main`
   - **Root Directory**: deixe em branco
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free`

4. **NÃO clique em "Create Web Service" ainda!** ⚠️

---

## 5️⃣ Configurar Variáveis de Ambiente

### Passo 5.1: Adicionar variáveis no Render
Antes de criar o serviço, role para baixo até **"Environment Variables"** e adicione:

#### Variável 1: DATABASE_URL
- **Key**: `DATABASE_URL`
- **Value**: Cole a URI do Supabase (lembra que você copiou?)
```
postgresql://postgres.xxxxxxxxxxxx:[SUA-SENHA]@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

#### Variável 2: SESSION_SECRET
- **Key**: `SESSION_SECRET`
- **Value**: Clique em **"Generate"** para gerar automaticamente

#### Variável 3: PYTHON_VERSION (opcional)
- **Key**: `PYTHON_VERSION`
- **Value**: `3.11.0`

### Passo 5.2: Criar Web Service
Agora sim! Clique em **"Create Web Service"**

⏱️ Aguarde 5-10 minutos enquanto o Render faz o deploy

---

## 6️⃣ Verificar Funcionamento

### Passo 6.1: Aguardar deploy
Você verá logs no painel do Render. Aguarde até ver:
```
==> Build successful 🎉
==> Deploying...
==> Your service is live 🎉
```

### Passo 6.2: Acessar o site
1. No topo do painel, você verá uma URL tipo:
   ```
   https://debutante-festa.onrender.com
   ```
2. Clique nessa URL para abrir seu site!

### Passo 6.3: Testar funcionalidades
1. **Página inicial**: Deve carregar normalmente
2. **Login admin**: Acesse `/admin/login`
   - Usuário: `admin`
   - Senha: `admin123`
3. **Dashboard**: Deve mostrar estatísticas zeradas

---

## 🎉 PRONTO! Seu site está no ar!

### 📝 Informações importantes:

**URL do seu site**: `https://seu-projeto.onrender.com`

**Painel Supabase**: https://supabase.com/dashboard

**Painel Render**: https://dashboard.render.com

---

## 🔧 Solução de Problemas

### Erro: "Application failed to start"

**Solução 1**: Verificar variáveis de ambiente
1. No Render, vá em **"Environment"**
2. Verifique se `DATABASE_URL` está correta
3. Teste a conexão no Supabase:
   - SQL Editor → `SELECT 1;` → Run

**Solução 2**: Verificar logs
1. No Render, clique em **"Logs"**
2. Procure por mensagens de erro
3. Copie e analise o erro

### Erro: "Connection refused" ou "Database error"

**Causa**: DATABASE_URL incorreta ou banco não configurado

**Solução**:
1. Volte ao Supabase → Settings → Database
2. Copie novamente a Connection String
3. No Render → Environment → Edite DATABASE_URL
4. Clique em **"Save Changes"**
5. O Render vai fazer redeploy automaticamente

### Site demora para carregar (primeira vez)

**Normal!** ✅ O plano gratuito do Render "hiberna" após 15 minutos sem uso.
- Primeira visita: 30-60 segundos
- Visitas seguintes: rápido

**Solução**: Upgrade para plano pago ($7/mês) ou aceitar a espera

### Erro: "ModuleNotFoundError"

**Solução**:
1. Verifique se `requirements.txt` está correto
2. No Render, force um redeploy:
   - Manual Deploy → Deploy latest commit

---

## 🔐 Segurança

### ⚠️ IMPORTANTE: Mudar senha do admin

Após primeiro login:

**Opção 1**: Via SQL no Supabase
1. Supabase → SQL Editor
2. Gerar nova senha:
```python
# Execute isso localmente para gerar o hash
from werkzeug.security import generate_password_hash
print(generate_password_hash('SUA_NOVA_SENHA_FORTE'))
```
3. No Supabase SQL Editor:
```sql
UPDATE admin 
SET password_hash = 'COLE_O_HASH_AQUI' 
WHERE username = 'admin';
```

**Opção 2**: Adicionar rota de alteração de senha no código (recomendado)

---

## 💰 Custos

### Supabase (Free Tier)
- ✅ 500MB de banco de dados
- ✅ 2GB de transferência
- ✅ Ideal para até 1000 convidados

### Render (Free Tier)
- ✅ 750 horas/mês grátis
- ⚠️ Site "hiberna" após 15min sem uso
- ⚠️ Apenas 1 serviço grátis

**Para produção séria**: Considere upgradar
- Render: $7/mês (sem hibernação)
- Supabase: Grátis é suficiente

---

## 📊 Monitoramento

### Ver logs do Render
1. Dashboard Render → Seu serviço → **Logs**
2. Monitore erros em tempo real

### Ver banco Supabase
1. Dashboard Supabase → **Table Editor**
2. Veja dados das tabelas
3. SQL Editor para queries avançadas

---

## 🔄 Atualizações

### Como atualizar o site
1. Faça mudanças no código local
2. Commit e push para GitHub:
```bash
git add .
git commit -m "Atualização do site"
git push
```
3. Render detecta automaticamente e faz redeploy!

---

## 📱 Domínio Personalizado

### Adicionar domínio próprio (exemplo.com.br)

1. Compre um domínio (Registro.br, GoDaddy, etc)
2. No Render:
   - Settings → Custom Domain
   - Adicione seu domínio
3. Configure DNS no registrador:
```
Tipo: CNAME
Nome: www
Valor: seu-projeto.onrender.com
```

---

## ✅ Checklist Final

- [ ] ✅ Conta Supabase criada
- [ ] ✅ Banco de dados configurado
- [ ] ✅ Tabelas criadas no SQL Editor
- [ ] ✅ Repositório GitHub criado
- [ ] ✅ Código enviado para GitHub
- [ ] ✅ Conta Render criada
- [ ] ✅ Web Service configurado
- [ ] ✅ Variáveis de ambiente adicionadas
- [ ] ✅ Deploy realizado com sucesso
- [ ] ✅ Site acessível online
- [ ] ✅ Login admin funcionando
- [ ] ✅ Banco de dados conectado
- [ ] ✅ Senha admin alterada
- [ ] ✅ Dados da festa configurados

---

## 🎊 Pronto! Seu site está online!

**URL**: https://seu-projeto.onrender.com

Compartilhe com seus convidados! 🎂👑💜

---

## 📞 Suporte

**Problemas com Supabase**: https://supabase.com/docs  
**Problemas com Render**: https://render.com/docs  
**Documentação Flask**: https://flask.palletsprojects.com

---

**Criado com 💜 para festas inesquecíveis!**
