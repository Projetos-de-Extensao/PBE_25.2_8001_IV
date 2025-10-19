#!/usr/bin/env python
"""
Script: criar_professor_com_permissoes.py

Cria um novo Professor com todos os grupos e Funcionario necessários

Uso:
    python criar_professor_com_permissoes.py

Interativo:
    O script pedirá pelos dados do novo professor
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.contrib.auth.models import User, Group
from plataforma_Casa.models import Funcionario, TipoUsuario, Curso


def input_custom(prompt):
    """Input que funciona melhor em diferentes ambientes"""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\n\n❌ Operação cancelada pelo usuário")
        sys.exit(1)


def criar_professor():
    print("\n" + "="*60)
    print("🆕 CRIAR NOVO PROFESSOR COM PERMISSÕES")
    print("="*60 + "\n")
    
    # Coletar dados
    print("📋 Digite as informações do professor:\n")
    
    username = input_custom("Username (ex: joao.silva): ").strip()
    email = input_custom("Email (ex: joao.silva@casa.com): ").strip()
    primeiro_nome = input_custom("Primeiro Nome: ").strip()
    sobrenome = input_custom("Sobrenome: ").strip()
    matricula = input_custom("Matrícula (ex: PROF_001): ").strip()
    departamento = input_custom("Departamento: ").strip()
    
    print("\n" + "-"*60)
    print("📊 Resumo dos dados:")
    print(f"  Username: {username}")
    print(f"  Email: {email}")
    print(f"  Nome: {primeiro_nome} {sobrenome}")
    print(f"  Matrícula: {matricula}")
    print(f"  Departamento: {departamento}")
    print("-"*60 + "\n")
    
    # Confirmar
    confirmacao = input_custom("Confirmar criação? (s/n): ").strip().lower()
    if confirmacao != 's':
        print("❌ Operação cancelada\n")
        return False
    
    try:
        # Verificar se usuário já existe
        if User.objects.filter(username=username).exists():
            print(f"\n❌ ERRO: Usuário '{username}' já existe!")
            return False
        
        if User.objects.filter(email=email).exists():
            print(f"\n❌ ERRO: Email '{email}' já está em uso!")
            return False
        
        # Obter ou criar grupos
        grupo_professor, _ = Group.objects.get_or_create(name='Professor')
        grupo_coordenador, _ = Group.objects.get_or_create(name='Coordenador')
        
        # Obter tipo de usuário
        tipo_usuario, _ = TipoUsuario.objects.get_or_create(
            tipo='Professor',
            defaults={'ativo': True}
        )
        
        # Criar Django User
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=primeiro_nome,
            last_name=sobrenome,
            password='DefaultPassword123!'  # Usuario deve mudar na primeira vez
        )
        
        # Adicionar grupos
        user.groups.add(grupo_professor)
        user.groups.add(grupo_coordenador)
        
        # Criar Funcionario
        funcionario = Funcionario.objects.create(
            nome=f"{primeiro_nome} {sobrenome}",
            email=email,
            tipo_usuario=tipo_usuario,
            matricula=matricula,
            departamento=departamento,
            coordenador=True,
            ativo=True
        )
        
        print("\n✅ PROFESSOR CRIADO COM SUCESSO!\n")
        print("📋 Detalhes do novo professor:\n")
        print(f"  Django User ID: {user.id}")
        print(f"  Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Grupos: {', '.join(user.groups.values_list('name', flat=True))}")
        print(f"\n  Funcionario ID: {funcionario.id}")
        print(f"  Nome: {funcionario.nome}")
        print(f"  Matrícula: {funcionario.matricula}")
        print(f"  Departamento: {funcionario.departamento}")
        
        print("\n⚠️  ATENÇÃO: Senha temporária: DefaultPassword123!")
        print("   O professor deve mudar na primeira vez que entrar.\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO ao criar professor: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def listar_professores():
    """Lista todos os professores existentes"""
    print("\n" + "="*60)
    print("📋 PROFESSORES EXISTENTES")
    print("="*60 + "\n")
    
    grupo_professor = Group.objects.get_or_create(name='Professor')[0]
    usuarios = User.objects.filter(groups=grupo_professor).order_by('username')
    
    if not usuarios.exists():
        print("Nenhum professor encontrado.\n")
        return
    
    for user in usuarios:
        func = Funcionario.objects.filter(email=user.email).first()
        groups = ', '.join(user.groups.values_list('name', flat=True))
        
        print(f"👤 {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Grupos: {groups}")
        if func:
            print(f"   Funcionario: {func.nome} ({func.matricula})")
        else:
            print(f"   ⚠️  Funcionario: NÃO ENCONTRADO")
        print()


def menu_principal():
    """Menu principal do script"""
    while True:
        print("\n" + "="*60)
        print("🎯 MENU PRINCIPAL - GERENCIAMENTO DE PROFESSORES")
        print("="*60)
        print("\n1. Criar novo professor")
        print("2. Listar professores existentes")
        print("3. Sincronizar grupos (Professor ↔ Coordenador)")
        print("4. Sair\n")
        
        opcao = input_custom("Escolha uma opção (1-4): ").strip()
        
        if opcao == '1':
            criar_professor()
        elif opcao == '2':
            listar_professores()
        elif opcao == '3':
            print("\nExecutando: python manage.py sincronizar_grupos\n")
            os.system('python manage.py sincronizar_grupos')
        elif opcao == '4':
            print("\n👋 Até logo!\n")
            break
        else:
            print("\n❌ Opção inválida. Tente novamente.")


if __name__ == '__main__':
    menu_principal()
