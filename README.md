# 🎂 Sistema RSVP para Festa de 15 Anos (Debutante)

Um sistema web completo e elegante para gerenciamento de confirmações de presença (RSVP) em festas de 15 anos, desenvolvido com Flask e PostgreSQL.

## ✨ Funcionalidades

### Para Convidados

- **Busca Inteligente**: Encontre seu nome e confirme presença facilmente
- **Confirmação em Grupo**: Confirme presença para toda a família de uma só vez
- **Lista de Presentes**: Visualize a lista de presentes com links para lojas
- **Corte de Honra**: Conheça as damas, cavalheiros e pajens
- **Interface Responsiva**: Funciona perfeitamente em celulares e computadores

### Para Administradores

- **Painel Completo**: Dashboard com estatísticas e controle total
- **Gestão de Convidados**: Adicione, edite e organize convidados em grupos/famílias
- **Gestão de Grupos**: Organize convidados por famílias ou categorias
- **Informações do Local**: Configure detalhes do evento, endereço e mapas
- **Lista de Presentes**: Gerencie presentes com preços e links para lojas
- **Corte de Honra**: Gerencie damas, cavalheiros e pajens
- **Envio de WhatsApp**: Integração com Twilio para envio de convites e lembretes (opcional)

## 📋 Pré-requisitos

- Python 3.11+
- PostgreSQL
- Conta Twilio (opcional, para WhatsApp)

## 🚀 Configuração Local

### 1. Clone o Repositório

```bash
git clone <seu-repositorio>
cd debutante-app
```

### 2. Crie um Ambiente Virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configure Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Configuração do Banco de Dados
DATABASE_URL=postgresql://usuario:senha@localhost:5432/debutante_rsvp

# Chave Secreta da Aplicação
SESSION_SECRET=sua-chave-secreta-super-segura

# Configuração Twilio (Opcional)
TWILIO_ACCOUNT_SID=seu_account_sid
TWILIO_AUTH_TOKEN=seu_auth_token
TWILIO_PHONE_NUMBER=+5511999999999
```

### 5. Configure o Banco de Dados PostgreSQL

#### Instale o PostgreSQL:

```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql

# Windows
# Baixe o instalador em: https://www.postgresql.org/download/windows/
```

#### Crie o banco de dados:

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE debutante_rsvp;
CREATE USER debutante_user WITH PASSWORD 'sua_senha';
GRANT ALL PRIVILEGES ON DATABASE debutante_rsvp TO debutante_user;
\q
```

### 6. Execute a Aplicação

```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`

## 🎨 Estrutura do Projeto

```
debutante-app/
│
├── app.py                 # Aplicação Flask principal
├── requirements.txt       # Dependências Python
├── .env                   # Variáveis de ambiente (criar)
├── .env.example          # Exemplo de variáveis
│
├── templates/            # Templates HTML
│   ├── base.html         # Layout base
│   ├── index.html        # Página inicial
│   ├── rsvp.html         # Confirmação de presença
│   ├── gifts.html        # Lista de presentes
│   ├── court.html        # Corte de honra
│   ├── venue.html        # Local da festa
│   ├── admin_login.html  # Login administrativo
│   └── admin_*.html      # Páginas administrativas
│
└── static/               # Arquivos estáticos
    └── style.css         # Estilos CSS
```

## 🗄️ Estrutura do Banco de Dados

### Tabelas Principais

#### `admin`
- Armazena credenciais dos administradores
- Senhas criptografadas com Werkzeug

#### `guest_group`
- Organiza convidados em famílias ou grupos
- Permite confirmação em lote

#### `guest`
- Informações dos convidados
- Status de confirmação (pendente, confirmado, nao_confirmado)
- Números de telefone para WhatsApp

#### `venue_info`
- Detalhes do local do evento
- Data, hora e links do Google Maps
- Tema e cores da festa

#### `gift_registry`
- Lista de presentes
- Preços e links para lojas
- Status de reserva

#### `court`
- Corte de honra (damas, cavalheiros, pajens)
- Fotos e biografias
- Ordem de entrada

## 🔐 Acesso Administrativo

### Credenciais Padrão

- **Usuário**: `admin`
- **Senha**: `admin123`

**⚠️ IMPORTANTE**: Altere estas credenciais após a primeira configuração!

### Alterando a Senha do Admin

1. Acesse `/admin/login`
2. Faça login com as credenciais padrão
3. No código, você pode criar uma nova senha usando:

```python
from werkzeug.security import generate_password_hash

# Gere o hash da nova senha
new_hash = generate_password_hash('sua_nova_senha')
print(new_hash)

# Atualize no banco de dados
```

## 📱 Configuração do WhatsApp (Twilio)

### 1. Criar Conta Twilio

1. Acesse [twilio.com](https://www.twilio.com/)
2. Crie uma conta gratuita
3. Verifique seu número de telefone

### 2. Configurar WhatsApp Business

1. No Console Twilio, vá em "Messaging" > "Try it out" > "Send a WhatsApp message"
2. Siga as instruções para configurar o WhatsApp Business
3. Anote suas credenciais (Account SID, Auth Token, Phone Number)

### 3. Adicionar Credenciais

No arquivo `.env`, adicione:

```env
TWILIO_ACCOUNT_SID=seu_account_sid_aqui
TWILIO_AUTH_TOKEN=seu_auth_token_aqui
TWILIO_PHONE_NUMBER=+5511999999999
```

## 🎨 Personalização

### Cores e Tema

Edite o arquivo `static/style.css` para personalizar:

- Cores do tema
- Fontes
- Espaçamentos
- Animações

As cores principais são:
- Primária: `#667eea` (roxo)
- Secundária: `#764ba2` (roxo escuro)
- Dourado: `#ffd700` (coroa)

### Templates

Os templates estão em `templates/`:

- `base.html`: Layout base
- `index.html`: Página inicial
- `rsvp.html`: Formulário de confirmação
- `gifts.html`: Lista de presentes
- `court.html`: Corte de honra
- `venue.html`: Local da festa
- `admin_*.html`: Painéis administrativos

### Imagens

Para adicionar imagens:

1. Crie uma pasta `static/images/`
2. Adicione suas imagens
3. Referencie nos templates:

```html
<img src="{{ url_for('static', filename='images/foto.jpg') }}" alt="Descrição">
```

## 🌐 Deploy em Produção

### Opção 1: Heroku

```bash
# Instalar Heroku CLI
# Criar Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy
heroku create nome-da-app
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

### Opção 2: Replit

1. Importe o projeto no Replit
2. Configure as variáveis de ambiente em "Secrets"
3. Clique em "Run"

### Opção 3: PythonAnywhere

1. Crie uma conta em [pythonanywhere.com](https://www.pythonanywhere.com)
2. Faça upload dos arquivos
3. Configure o app web Flask
4. Configure o banco de dados PostgreSQL

## 🔧 Solução de Problemas

### Erro de Banco de Dados

```
RuntimeError: Either 'SQLALCHEMY_DATABASE_URI' or 'SQLALCHEMY_BINDS' must be set.
```

**Solução**: Verifique se a variável `DATABASE_URL` está configurada corretamente no `.env`.

### Erro de Sessão

```
RuntimeError: The session is unavailable because no secret key was set.
```

**Solução**: Configure a variável `SESSION_SECRET` com uma chave única.

### WhatsApp não Funciona

1. Verifique se as credenciais Twilio estão corretas
2. Confirme se o número está no formato internacional (+5511999999999)
3. Verifique se sua conta Twilio tem créditos

### Erro ao Instalar Dependências

```bash
# Tente atualizar o pip primeiro
pip install --upgrade pip

# Instale as dependências uma por uma se necessário
pip install Flask
pip install Flask-SQLAlchemy
# etc...
```

## 📝 Dicas para o Dia da Festa

### Antes do Evento

1. Exporte a lista de convidados confirmados
2. Envie lembretes via WhatsApp 1-2 dias antes
3. Prepare um QR Code com o link do RSVP para convidados de última hora

### Durante o Evento

1. Use a lista exportada para controle de entrada
2. O sistema pode ser usado em tablets para check-in em tempo real

## 🆘 Suporte

Para suporte técnico ou dúvidas:

1. Verifique a seção de solução de problemas
2. Consulte a documentação do Flask: [flask.palletsprojects.com](https://flask.palletsprojects.com/)
3. Documentação do Twilio: [twilio.com/docs](https://www.twilio.com/docs)

## 🎉 Funcionalidades Extras (Futuras)

- [ ] Upload de fotos pelos convidados
- [ ] Galeria de fotos do evento
- [ ] Playlist colaborativa do Spotify
- [ ] Mensagens de parabéns
- [ ] Contador regressivo
- [ ] Transmissão ao vivo
- [ ] QR Code para check-in rápido

## 📄 Licença

Este projeto é de código aberto. Sinta-se livre para usar, modificar e distribuir.

---

**Desenvolvido com 💜 para tornar sua festa de 15 anos ainda mais especial!**

## 🎈 Créditos

Baseado no projeto original [APPCASAMENTO](https://github.com/NisiK-dev/APPCASAMENTO) e adaptado para festas de 15 anos.

---

### 📞 Contato

Se precisar de ajuda para personalizar ou configurar o sistema, entre em contato!

**Boas festas! 🎂🎉👑**
