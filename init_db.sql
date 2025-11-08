-- Script de Inicialização do Banco de Dados
-- Execute este SQL no Supabase SQL Editor

-- Criar tabela de administradores
CREATE TABLE IF NOT EXISTS admin (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

-- Criar tabela de grupos de convidados
CREATE TABLE IF NOT EXISTS guest_group (
    id SERIAL PRIMARY KEY,
    group_name VARCHAR(100) NOT NULL,
    description VARCHAR(255)
);

-- Criar tabela de convidados
CREATE TABLE IF NOT EXISTS guest (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    group_id INTEGER REFERENCES guest_group(id) ON DELETE SET NULL,
    status VARCHAR(20) DEFAULT 'pendente' CHECK (status IN ('pendente', 'confirmado', 'nao_confirmado')),
    confirmed_at TIMESTAMP,
    plus_one BOOLEAN DEFAULT FALSE,
    notes TEXT
);

-- Criar índices para melhorar performance
CREATE INDEX IF NOT EXISTS idx_guest_name ON guest(name);
CREATE INDEX IF NOT EXISTS idx_guest_status ON guest(status);
CREATE INDEX IF NOT EXISTS idx_guest_group ON guest(group_id);

-- Criar tabela de informações do local
CREATE TABLE IF NOT EXISTS venue_info (
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
CREATE TABLE IF NOT EXISTS gift_registry (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(200) NOT NULL,
    description TEXT,
    price FLOAT,
    store_link VARCHAR(500),
    store_name VARCHAR(100),
    category VARCHAR(50),
    priority VARCHAR(20) CHECK (priority IN ('alta', 'media', 'baixa')),
    reserved_by VARCHAR(100),
    reserved BOOLEAN DEFAULT FALSE
);

-- Criar índice para categoria de presentes
CREATE INDEX IF NOT EXISTS idx_gift_category ON gift_registry(category);

-- Criar tabela de corte de honra
CREATE TABLE IF NOT EXISTS court (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('dama', 'cavalheiro', 'pajem', 'dama_principal')),
    photo_url VARCHAR(500),
    bio TEXT,
    order_position INTEGER
);

-- Criar índice para ordem de entrada
CREATE INDEX IF NOT EXISTS idx_court_order ON court(order_position);

-- Inserir admin padrão
-- Senha: admin123 (MUDE DEPOIS DO PRIMEIRO LOGIN!)
INSERT INTO admin (username, password_hash) 
VALUES ('admin', 'scrypt:32768:8:1$oKGZ8PqV5GvUhZKe$6a3e0d0f5e6c0d8a7f9e0c5a7f9e0c5a7f9e0c5a7f9e0c5a7f9e0c5a7f9e0c5a7f9e0c5a7f9e0c5a7f9e0c5a')
ON CONFLICT (username) DO NOTHING;

-- Inserir dados de exemplo (opcional - remova se não quiser)

-- Exemplo de grupo
INSERT INTO guest_group (group_name, description) 
VALUES ('Família Silva', 'Família da debutante')
ON CONFLICT DO NOTHING;

-- Exemplo de convidado
INSERT INTO guest (name, phone, email, group_id, status) 
VALUES ('Maria Silva', '+5511999999999', 'maria@email.com', 1, 'pendente')
ON CONFLICT DO NOTHING;

-- Exemplo de presente
INSERT INTO gift_registry (item_name, description, price, category, priority) 
VALUES ('Jogo de Panelas', 'Conjunto completo de panelas antiaderentes', 299.90, 'Casa', 'alta')
ON CONFLICT DO NOTHING;

-- Verificar criação das tabelas
SELECT 
    table_name,
    (SELECT COUNT(*) 
     FROM information_schema.columns 
     WHERE table_name = t.table_name AND table_schema = 'public') as column_count
FROM information_schema.tables t
WHERE table_schema = 'public' 
AND table_type = 'BASE TABLE'
ORDER BY table_name;

-- Mostrar estrutura das tabelas
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position;
