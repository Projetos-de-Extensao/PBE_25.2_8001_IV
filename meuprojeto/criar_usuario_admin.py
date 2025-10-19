#!/usr/bin/env python
"""
Script para criar usuário Django User ADMIN + Funcionario para login no sistema
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto.settings')
django.setup()

from django.contrib.auth.models import User
from plataforma_Casa.models import Usuario, TipoUsuario, Funcionario
from datetime import date

def criar_usuario_admin():
    """Cria um User Django ADMIN + Funcionario para login"""
    
    print("=" * 60)
    print("CRIANDO USUÁRIO ADMIN PARA LOGIN")
    print("=" * 60)
    
    # Credenciais
    username = 'admin'
    email = 'admin@casa.com'
    password = 'admin'
    
    # Verificar se já existe
    if User.objects.filter(username=username).exists():
        print(f"\n⚠ Usuário '{username}' já existe!")
        resposta = input("Deseja recriar? (s/n): ")
        if resposta.lower() != 's':
            print("Operação cancelada.")
            return
        else:
            # Deletar existentes
            User.objects.filter(username=username).delete()
            Usuario.objects.filter(email=email).delete()
            Funcionario.objects.filter(email=email).delete()
            print("✓ Usuário anterior removido")
    
    # Criar Django User ADMIN (com permissões)
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name='Administrador',
        last_name='do Sistema',
        is_staff=True,  # ADMIN é staff
        is_superuser=True  # ADMIN é superuser
    )
    print(f"\n✓ Django User criado: {user.username} (ADMIN - com permissões completas)")
    
    # Buscar/criar tipo de usuário
    try:
        tipo_funcionario = TipoUsuario.objects.get(tipo='Funcionario')
    except TipoUsuario.DoesNotExist:
        tipo_funcionario = TipoUsuario.objects.create(tipo='Funcionario', ativo=True)
    
    # Criar Funcionario
    funcionario = Funcionario.objects.create(
        nome='Administrador do Sistema',
        email=email,
        tipo_usuario=tipo_funcionario,
        cargo='Administrador',
        setor='TI',
        data_admissao=date(2025, 1, 1),
        ativo=True
    )
    
    # Exibir credenciais
    print("\n" + "=" * 60)
    print("✅ USUÁRIO ADMIN CRIADO COM SUCESSO!")
    print("=" * 60)
    print(f"\n🔐 CREDENCIAIS DE LOGIN:")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Senha: {password}")
    print(f"\n👤 DADOS DO FUNCIONÁRIO:")
    print(f"   Nome: {funcionario.nome}")
    print(f"   Cargo: {funcionario.cargo}")
    print(f"   Setor: {funcionario.setor}")
    print(f"   Permissões: ADMIN COMPLETO")
    print(f"\n🌐 COMO FAZER LOGIN:")
    print(f"   1. Acesse: http://localhost:8000/login/")
    print(f"   2. Username: {username}")
    print(f"   3. Senha: {password}")
    print(f"\n📋 ACESSO COMPLETO A:")
    print(f"   ✅ Dashboard Principal")
    print(f"   ✅ Dashboard de Gestão")
    print(f"   ✅ Validar Horas")
    print(f"   ✅ Gerenciar Pagamentos")
    print(f"   ✅ Cadastros (Usuários, Alunos, Vagas, Turmas)")
    print(f"   ✅ Monitorias e Presenças")
    print(f"   ✅ Todos os Relatórios")
    print("\n" + "=" * 60)
    
    return user, funcionario

if __name__ == '__main__':
    criar_usuario_admin()
