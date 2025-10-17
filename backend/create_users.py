#!/usr/bin/env python
"""
Script simplificado de inicialização - Cria apenas usuários de login
"""

import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_users():
    """Cria usuários básicos do sistema"""
    
    users_data = [
        {'username': 'admin', 'password': 'admin123', 'email': 'admin@sistema.com', 
         'first_name': 'Admin', 'last_name': 'Sistema', 'is_superuser': True, 'is_staff': True},
        
        {'username': 'anderson', 'password': '1234', 'email': 'anderson@sistema.com', 
         'first_name': 'Anderson', 'last_name': 'User', 'is_superuser': False, 'is_staff': False},
         
        {'username': 'coord1', 'password': 'coord123', 'email': 'coord1@sistema.com', 
         'first_name': 'Maria', 'last_name': 'Coordenadora', 'is_superuser': False, 'is_staff': True},
         
        {'username': 'monitor1', 'password': 'monitor123', 'email': 'monitor1@sistema.com', 
         'first_name': 'Julia', 'last_name': 'Monitora', 'is_superuser': False, 'is_staff': False},
         
        {'username': 'aluno1', 'password': 'aluno123', 'email': 'aluno1@sistema.com', 
         'first_name': 'Pedro', 'last_name': 'Aluno', 'is_superuser': False, 'is_staff': False},
    ]
    
    print("\n🔑 CRIANDO USUÁRIOS DO SISTEMA\n" + "="*50)
    
    for data in users_data:
        username = data['username']
        if User.objects.filter(username=username).exists():
            print(f"→ Usuário '{username}' já existe")
        else:
            if data['is_superuser']:
                user = User.objects.create_superuser(
                    username=data['username'],
                    email=data['email'],
                    password=data['password'],
                    first_name=data['first_name'],
                    last_name=data['last_name']
                )
            else:
                user = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password=data['password'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    is_staff=data['is_staff']
                )
            print(f"✓ Criado: {username} (senha: {data['password']})")
    
    print("\n" + "="*50)
    print("✅ USUÁRIOS CRIADOS COM SUCESSO!")
    print("="*50)
    print("\n🌐 ACESSE:")
    print("   URL: http://127.0.0.1:8000/login")
    print("\n👤 CREDENCIAIS:")
    print("   admin / admin123 (Administrador)")
    print("   anderson / 1234 (Seu usuário)")
    print("   coord1 / coord123 (Coordenador)")
    print("   monitor1 / monitor123 (Monitor)")
    print("   aluno1 / aluno123 (Aluno)")
    print("\n")

if __name__ == '__main__':
    create_users()
