#!/usr/bin/env python3
"""
Script para gerar hash de senha para o admin
Use este script para criar uma nova senha segura
"""

from werkzeug.security import generate_password_hash
import sys

def main():
    print("=" * 60)
    print("🔐 GERADOR DE SENHA PARA ADMIN")
    print("=" * 60)
    print()
    
    if len(sys.argv) > 1:
        # Senha passada como argumento
        password = sys.argv[1]
    else:
        # Pedir senha interativamente
        password = input("Digite a nova senha: ")
    
    if len(password) < 8:
        print("❌ ERRO: A senha deve ter pelo menos 8 caracteres!")
        sys.exit(1)
    
    # Gerar hash
    password_hash = generate_password_hash(password)
    
    print()
    print("✅ Hash gerado com sucesso!")
    print()
    print("=" * 60)
    print("HASH DA SENHA:")
    print("=" * 60)
    print(password_hash)
    print()
    print("=" * 60)
    print("SQL PARA ATUALIZAR NO SUPABASE:")
    print("=" * 60)
    print(f"""
UPDATE admin 
SET password_hash = '{password_hash}' 
WHERE username = 'admin';
""")
    print("=" * 60)
    print()
    print("📝 Instruções:")
    print("1. Copie o SQL acima")
    print("2. Acesse Supabase → SQL Editor")
    print("3. Cole e execute o SQL")
    print("4. Sua nova senha estará ativa!")
    print()

if __name__ == "__main__":
    main()
