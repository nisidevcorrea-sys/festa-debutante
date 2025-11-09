from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# CORREÇÃO: Garantir que DATABASE_URL seja configurada corretamente
database_url = os.getenv('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'postgresql://localhost/debutante_rsvp'
app.config['SECRET_KEY'] = os.getenv('SESSION_SECRET', 'chave-secreta-debutante-2024')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://localhost/debutante_rsvp')
app.config['SECRET_KEY'] = os.getenv('SESSION_SECRET', 'chave-secreta-debutante-2024')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ============================================
# MODELOS DO BANCO DE DADOS
# ============================================

class Admin(db.Model):
    """Administrador da festa"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class GuestGroup(db.Model):
    """Grupos de convidados (família, amigos da escola, etc)"""
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    guests = db.relationship('Guest', backref='group', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<GuestGroup {self.group_name}>'


class Guest(db.Model):
    """Convidados da festa"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    group_id = db.Column(db.Integer, db.ForeignKey('guest_group.id'))
    status = db.Column(db.String(20), default='pendente')  # pendente, confirmado, nao_confirmado
    confirmed_at = db.Column(db.DateTime)
    plus_one = db.Column(db.Boolean, default=False)  # Pode levar acompanhante
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Guest {self.name}>'


class VenueInfo(db.Model):
    """Informações do local da festa"""
    id = db.Column(db.Integer, primary_key=True)
    debutante_name = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    venue_name = db.Column(db.String(200))
    address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(20))
    google_maps_link = db.Column(db.String(500))
    ceremony_time = db.Column(db.String(20))  # Hora da cerimônia/valsa
    party_time = db.Column(db.String(20))  # Hora da festa
    dress_code = db.Column(db.String(100))  # Traje
    theme = db.Column(db.String(100))  # Tema da festa
    color_scheme = db.Column(db.String(100))  # Cores da festa
    additional_info = db.Column(db.Text)


class GiftRegistry(db.Model):
    """Lista de presentes"""
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    store_link = db.Column(db.String(500))
    store_name = db.Column(db.String(100))
    category = db.Column(db.String(50))  # casa, tecnologia, viagem, etc
    priority = db.Column(db.String(20))  # alta, média, baixa
    reserved_by = db.Column(db.String(100))  # Nome de quem reservou
    reserved = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Gift {self.item_name}>'


class Court(db.Model):
    """Corte de honra (damas e cavalheiros)"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # dama, cavalheiro, pajem, dama_principal
    photo_url = db.Column(db.String(500))
    bio = db.Column(db.Text)
    order_position = db.Column(db.Integer)  # Ordem de entrada
    
    def __repr__(self):
        return f'<Court {self.name} - {self.role}>'


# ============================================
# ROTAS PÚBLICAS
# ============================================

@app.route('/')
def index():
    """Página inicial"""
    venue = VenueInfo.query.first()
    return render_template('index.html', venue=venue)


@app.route('/rsvp')
def rsvp():
    """Página de confirmação de presença"""
    return render_template('rsvp.html')


@app.route('/api/search-guests', methods=['POST'])
def search_guests():
    """Busca convidados pelo nome"""
    data = request.get_json()
    search_term = data.get('search', '').strip().lower()
    
    if len(search_term) < 2:
        return jsonify({'guests': []})
    
    guests = Guest.query.filter(
        Guest.name.ilike(f'%{search_term}%')
    ).all()
    
    result = []
    for guest in guests:
        group_members = []
        if guest.group_id:
            group_members = Guest.query.filter_by(group_id=guest.group_id).all()
        
        result.append({
            'id': guest.id,
            'name': guest.name,
            'phone': guest.phone,
            'status': guest.status,
            'plus_one': guest.plus_one,
            'group': {
                'id': guest.group.id if guest.group else None,
                'name': guest.group.group_name if guest.group else None,
                'members': [{'id': m.id, 'name': m.name, 'status': m.status} for m in group_members]
            } if guest.group else None
        })
    
    return jsonify({'guests': result})


@app.route('/api/confirm-presence', methods=['POST'])
def confirm_presence():
    """Confirma presença de um ou mais convidados"""
    data = request.get_json()
    guest_ids = data.get('guest_ids', [])
    status = data.get('status', 'confirmado')
    
    if not guest_ids:
        return jsonify({'success': False, 'message': 'Nenhum convidado selecionado'})
    
    try:
        for guest_id in guest_ids:
            guest = Guest.query.get(guest_id)
            if guest:
                guest.status = status
                guest.confirmed_at = datetime.now() if status == 'confirmado' else None
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Presença confirmada com sucesso!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Erro ao confirmar presença: {str(e)}'})


@app.route('/gifts')
def gifts():
    """Lista de presentes"""
    gifts_list = GiftRegistry.query.order_by(GiftRegistry.category, GiftRegistry.item_name).all()
    
    # Agrupar por categoria
    gifts_by_category = {}
    for gift in gifts_list:
        category = gift.category or 'Outros'
        if category not in gifts_by_category:
            gifts_by_category[category] = []
        gifts_by_category[category].append(gift)
    
    return render_template('gifts.html', gifts_by_category=gifts_by_category)


@app.route('/court')
def court():
    """Corte de honra"""
    court_members = Court.query.order_by(Court.order_position, Court.name).all()
    
    # Separar por tipo
    damas = [m for m in court_members if m.role in ['dama', 'dama_principal']]
    cavalheiros = [m for m in court_members if m.role == 'cavalheiro']
    pajens = [m for m in court_members if m.role == 'pajem']
    
    return render_template('court.html', damas=damas, cavalheiros=cavalheiros, pajens=pajens)


@app.route('/venue')
def venue():
    """Informações do local"""
    venue_info = VenueInfo.query.first()
    return render_template('venue.html', venue=venue_info)


# ============================================
# ROTAS ADMINISTRATIVAS
# ============================================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Login do administrador"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Usuário ou senha incorretos', 'danger')
    
    return render_template('admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    """Logout do administrador"""
    session.pop('admin_id', None)
    session.pop('admin_username', None)
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('index'))


def admin_required(f):
    """Decorador para rotas que requerem autenticação"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Você precisa estar logado para acessar esta página', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Dashboard administrativo"""
    total_guests = Guest.query.count()
    confirmed = Guest.query.filter_by(status='confirmado').count()
    pending = Guest.query.filter_by(status='pendente').count()
    declined = Guest.query.filter_by(status='nao_confirmado').count()
    
    groups = GuestGroup.query.all()
    venue = VenueInfo.query.first()
    
    stats = {
        'total': total_guests,
        'confirmed': confirmed,
        'pending': pending,
        'declined': declined,
        'confirmation_rate': round((confirmed / total_guests * 100) if total_guests > 0 else 0, 1)
    }
    
    return render_template('admin_dashboard.html', stats=stats, groups=groups, venue=venue)


@app.route('/admin/guests')
@admin_required
def admin_guests():
    """Gerenciar convidados"""
    guests = Guest.query.order_by(Guest.name).all()
    groups = GuestGroup.query.all()
    return render_template('admin_guests.html', guests=guests, groups=groups)


@app.route('/admin/groups')
@admin_required
def admin_groups():
    """Gerenciar grupos"""
    groups = GuestGroup.query.all()
    return render_template('admin_groups.html', groups=groups)


@app.route('/admin/venue', methods=['GET', 'POST'])
@admin_required
def admin_venue():
    """Gerenciar informações do local"""
    venue = VenueInfo.query.first()
    
    if request.method == 'POST':
        if not venue:
            venue = VenueInfo()
            db.session.add(venue)
        
        venue.debutante_name = request.form.get('debutante_name')
        venue.event_date = datetime.strptime(request.form.get('event_date'), '%Y-%m-%dT%H:%M')
        venue.venue_name = request.form.get('venue_name')
        venue.address = request.form.get('address')
        venue.city = request.form.get('city')
        venue.state = request.form.get('state')
        venue.zip_code = request.form.get('zip_code')
        venue.google_maps_link = request.form.get('google_maps_link')
        venue.ceremony_time = request.form.get('ceremony_time')
        venue.party_time = request.form.get('party_time')
        venue.dress_code = request.form.get('dress_code')
        venue.theme = request.form.get('theme')
        venue.color_scheme = request.form.get('color_scheme')
        venue.additional_info = request.form.get('additional_info')
        
        db.session.commit()
        flash('Informações do local atualizadas com sucesso!', 'success')
        return redirect(url_for('admin_venue'))
    
    return render_template('admin_venue.html', venue=venue)


@app.route('/admin/gifts')
@admin_required
def admin_gifts():
    """Gerenciar lista de presentes"""
    gifts = GiftRegistry.query.order_by(GiftRegistry.category, GiftRegistry.item_name).all()
    return render_template('admin_gifts.html', gifts=gifts)


@app.route('/admin/court')
@admin_required
def admin_court():
    """Gerenciar corte de honra"""
    court_members = Court.query.order_by(Court.order_position, Court.name).all()
    return render_template('admin_court.html', court_members=court_members)


# ============================================
# API ADMIN - CRUD de Convidados
# ============================================

@app.route('/api/admin/guest', methods=['POST'])
@admin_required
def api_create_guest():
    """Criar novo convidado"""
    data = request.get_json()
    
    guest = Guest(
        name=data.get('name'),
        phone=data.get('phone'),
        email=data.get('email'),
        group_id=data.get('group_id'),
        plus_one=data.get('plus_one', False),
        notes=data.get('notes')
    )
    
    db.session.add(guest)
    db.session.commit()
    
    return jsonify({'success': True, 'guest_id': guest.id})


@app.route('/api/admin/guest/<int:guest_id>', methods=['PUT'])
@admin_required
def api_update_guest(guest_id):
    """Atualizar convidado"""
    guest = Guest.query.get_or_404(guest_id)
    data = request.get_json()
    
    guest.name = data.get('name', guest.name)
    guest.phone = data.get('phone', guest.phone)
    guest.email = data.get('email', guest.email)
    guest.group_id = data.get('group_id', guest.group_id)
    guest.plus_one = data.get('plus_one', guest.plus_one)
    guest.notes = data.get('notes', guest.notes)
    
    db.session.commit()
    
    return jsonify({'success': True})


@app.route('/api/admin/guest/<int:guest_id>', methods=['DELETE'])
@admin_required
def api_delete_guest(guest_id):
    """Deletar convidado"""
    guest = Guest.query.get_or_404(guest_id)
    db.session.delete(guest)
    db.session.commit()
    
    return jsonify({'success': True})


# ============================================
# API ADMIN - CRUD de Grupos
# ============================================

@app.route('/api/admin/group', methods=['POST'])
@admin_required
def api_create_group():
    """Criar novo grupo"""
    data = request.get_json()
    
    group = GuestGroup(
        group_name=data.get('group_name'),
        description=data.get('description')
    )
    
    db.session.add(group)
    db.session.commit()
    
    return jsonify({'success': True, 'group_id': group.id})


@app.route('/api/admin/group/<int:group_id>', methods=['DELETE'])
@admin_required
def api_delete_group(group_id):
    """Deletar grupo"""
    group = GuestGroup.query.get_or_404(group_id)
    db.session.delete(group)
    db.session.commit()
    
    return jsonify({'success': True})


# ============================================
# INICIALIZAÇÃO
# ============================================

def init_db():
    """Inicializa o banco de dados"""
    with app.app_context():
        db.create_all()
        
        # Criar admin padrão se não existir
        if not Admin.query.first():
            admin = Admin(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('Admin padrão criado: admin/admin123')


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
