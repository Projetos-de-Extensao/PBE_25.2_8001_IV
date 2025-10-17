#!/usr/bin/env python3
"""
Script para criar usuários de teste no sistema
Execute com: python create_test_users.py
"""

import os
import django
import sys

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')
django.setup()

from django.contrib.auth.models import User

def create_test_users():
    """Cria usuários de teste para o sistema"""
    
    users_data = [
        {
            'username': 'admin',
            'email': 'admin@sistema.com',
            'password': 'admin123',
            'first_name': 'Administrador',
            'last_name': 'Sistema',
            'is_staff': True,
            'is_superuser': True
        },
        {
            'username': 'anderson',
            'email': 'anderson@aluno.com',
            'password': '123456',
            'first_name': 'Anderson',
            'last_name': 'Aluno',
            'is_staff': False,
            'is_superuser': False
        },
        {
            'username': 'coordenador',
            'email': 'coordenador@sistema.com',
            'password': 'coord123',
            'first_name': 'João',
            'last_name': 'Coordenador',
            'is_staff': True,
            'is_superuser': False
        },
        {
            'username': 'monitor',
            'email': 'monitor@aluno.com',
            'password': 'monitor123',
            'first_name': 'Maria',
            'last_name': 'Monitor',
            'is_staff': False,
            'is_superuser': False
        },
        {
            'username': 'professor',
            'email': 'professor@sistema.com',
            'password': 'prof123',
            'first_name': 'Carlos',
            'last_name': 'Professor',
            'is_staff': True,
            'is_superuser': False
        },
    ]
    
    print("=" * 60)
    print("CRIANDO USUÁRIOS DE TESTE")
    print("=" * 60)
    
    for user_data in users_data:
        username = user_data['username']
        
        # Verificar se usuário já existe
        if User.objects.filter(username=username).exists():
            print(f"⚠️  Usuário '{username}' já existe - PULANDO")
            continue
        
        # Criar usuário
        password = user_data.pop('password')
        user = User.objects.create_user(**user_data)
        user.set_password(password)
        user.save()
        
        # Restaurar senha para exibição
        user_data['password'] = password
        
        print(f"✅ Usuário criado: {username}")
        print(f"   Email: {user_data['email']}")
        print(f"   Senha: {password}")
        print(f"   Nome: {user_data['first_name']} {user_data['last_name']}")
        print(f"   Tipo: {'Administrador' if user_data['is_superuser'] else 'Staff' if user_data['is_staff'] else 'Usuário comum'}")
        print()
    
    print("=" * 60)
    print("RESUMO DE CREDENCIAIS PARA LOGIN")
    print("=" * 60)
    print()
    print("🔐 CREDENCIAIS DISPONÍVEIS:")
    print()
    print("1. Administrador do Sistema:")
    print("   Usuário: admin")
    print("   Senha: admin123")
    print()
    print("2. Anderson (Seu usuário):")
    print("   Usuário: anderson")
    print("   Senha: 123456")
    print()
    print("3. Coordenador:")
    print("   Usuário: coordenador")
    print("   Senha: coord123")
    print()
    print("4. Monitor:")
    print("   Usuário: monitor")
    print("   Senha: monitor123")
    print()
    print("5. Professor:")
    print("   Usuário: professor")
    print("   Senha: prof123")
    print()
    print("=" * 60)
    print("✅ Script concluído!")
    print("=" * 60)
    print()
    print("Acesse: http://localhost:8000/login")
    print()

if __name__ == '__main__':
    try:
        create_test_users()
    except Exception as e:
        print(f"❌ Erro ao criar usuários: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
