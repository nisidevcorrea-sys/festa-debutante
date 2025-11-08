# 🚀 Guia de Instalação Rápida - Sistema de Festa de 15 Anos

## ⚡ Instalação em 5 Minutos

### 1️⃣ Baixe e Extraia o Projeto

```bash
# Extraia o arquivo debutante-app.zip
unzip debutante-app.zip
cd debutante-app
```

### 2️⃣ Instale as Dependências

```bash
# Crie um ambiente virtual (recomendado)
python -m venv venv

# Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### 3️⃣ Configure o Banco de Dados

#### Opção A: PostgreSQL (Recomendado para Produção)

```bash
# Instale o PostgreSQL
# Ubuntu/Debian:
sudo apt-get install postgresql postgresql-contrib

# macOS:
brew install postgresql

# Crie o banco de dados
sudo -u postgres psql
```

```sql
CREATE DATABASE debutante_rsvp;
CREATE USER debutante_user WITH PASSWORD 'sua_senha';
GRANT ALL PRIVILEGES ON DATABASE debutante_rsvp TO debutante_user;
\q
```

Crie o arquivo `.env`:
```env
DATABASE_URL=postgresql://debutante_user:sua_senha@localhost:5432/debutante_rsvp
SESSION_SECRET=chave-secreta-aleatoria-aqui
```

#### Opção B: SQLite (Mais Fácil para Testes)

Modifique o arquivo `app.py`, linha 13:
```python
# De:
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://localhost/debutante_rsvp')

# Para:
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///debutante.db')
```

Crie o arquivo `.env`:
```env
DATABASE_URL=sqlite:///debutante.db
SESSION_SECRET=chave-secreta-aleatoria-aqui
```

### 4️⃣ Execute a Aplicação

```bash
python app.py
```

### 5️⃣ Acesse o Sistema

- **Site Público**: http://localhost:5000
- **Área Admin**: http://localhost:5000/admin/login
  - Usuário: `admin`
  - Senha: `admin123`

---

## 📝 Primeiros Passos Após Instalação

### 1. Configure as Informações da Festa

1. Faça login na área administrativa
2. Vá em "Local da Festa"
3. Preencha todos os dados do evento

### 2. Adicione os Convidados

1. Crie grupos (Família, Amigos da Escola, etc.)
2. Adicione os convidados em "Gerenciar Convidados"
3. Vincule os convidados aos grupos

### 3. Configure a Lista de Presentes

1. Acesse "Lista de Presentes"
2. Adicione os itens desejados
3. Adicione links para lojas

### 4. Configure a Corte de Honra

1. Acesse "Corte de Honra"
2. Adicione damas, cavalheiros e pajens
3. (Opcional) Adicione fotos e biografias

### 5. Teste o Sistema

1. Abra o site em modo anônimo
2. Teste a confirmação de presença
3. Verifique todas as páginas
4. Ajuste as cores e textos conforme necessário

---

## 🎨 Personalizações Básicas

### Alterar Cores

Edite o arquivo `static/style.css`:

```css
/* Linha ~120 - Cor primária */
.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Altere para suas cores preferidas */
.btn-primary {
    background: linear-gradient(135deg, #ff6b9d 0%, #c06c84 100%);
}
```

### Alterar Textos

Edite os arquivos em `templates/`:
- `index.html` - Página inicial
- `rsvp.html` - Confirmação de presença
- `gifts.html` - Lista de presentes
- etc.

### Adicionar Fotos

1. Crie a pasta `static/images/`
2. Adicione suas fotos
3. Referencie nos templates:

```html
<img src="{{ url_for('static', filename='images/foto-debutante.jpg') }}" alt="Foto">
```

---

## 🌐 Deploy Online (Hospedagem Gratuita)

### Opção 1: Replit (Mais Fácil)

1. Crie conta em [replit.com](https://replit.com)
2. Clique em "Create Repl"
3. Escolha "Import from GitHub"
4. Faça upload dos arquivos
5. Configure as variáveis em "Secrets":
   - `SESSION_SECRET`
6. Clique em "Run"

### Opção 2: Heroku

```bash
# Instale o Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Faça login
heroku login

# Crie a aplicação
heroku create nome-da-festa

# Adicione o PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Configure as variáveis
heroku config:set SESSION_SECRET=sua-chave-secreta

# Faça deploy
git init
git add .
git commit -m "Deploy inicial"
git push heroku main
```

### Opção 3: PythonAnywhere

1. Crie conta em [pythonanywhere.com](https://www.pythonanywhere.com)
2. Faça upload dos arquivos
3. Configure o web app Flask
4. Configure as variáveis de ambiente
5. Recarregue a aplicação

---

## 🆘 Problemas Comuns

### Erro: "No module named 'flask'"

```bash
pip install Flask
# ou
pip install -r requirements.txt
```

### Erro: "Database connection failed"

Verifique:
1. PostgreSQL está rodando?
2. DATABASE_URL está correto no `.env`?
3. Banco de dados foi criado?

### Erro: "Session unavailable"

Adicione no `.env`:
```env
SESSION_SECRET=uma-chave-secreta-qualquer-123
```

### Porta 5000 já está em uso

Altere a porta no final do `app.py`:
```python
app.run(host='0.0.0.0', port=8000, debug=True)  # Mudou para 8000
```

---

## 📞 Suporte

Se tiver problemas:
1. Verifique o README.md completo
2. Consulte a documentação do Flask
3. Verifique os logs de erro no terminal

---

## ✅ Checklist Final

- [ ] Banco de dados configurado
- [ ] Aplicação rodando local
- [ ] Login admin funcionando
- [ ] Informações da festa preenchidas
- [ ] Convidados adicionados
- [ ] Lista de presentes configurada
- [ ] Corte de honra adicionada
- [ ] Sistema testado
- [ ] Cores personalizadas
- [ ] Textos personalizados
- [ ] Deploy online (opcional)

---

**🎉 Pronto! Seu sistema está funcionando!**

Agora é só compartilhar o link com seus convidados e aguardar as confirmações!

**Boa festa! 🎂👑💜**
