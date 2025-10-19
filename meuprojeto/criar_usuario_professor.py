#!/usr/bin/env python
"""
Script para criar usuário Django User PROFESSOR + Funcionario para login no sistema
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto.settings')
django.setup()

from django.contrib.auth.models import User, Group
from plataforma_Casa.models import Usuario, TipoUsuario, Funcionario
from datetime import date

def criar_usuario_professor():
    """Cria um User Django PROFESSOR + Funcionario para login"""
    
    print("=" * 60)
    print("CRIANDO USUÁRIO PROFESSOR PARA LOGIN")
    print("=" * 60)
    
    # Credenciais
    username = 'professor.teste'
    email = 'professor.teste@casa.com'
    password = 'professor123'
    
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
    
    # Criar Django User PROFESSOR (sem permissões de admin)
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name='Carlos',
        last_name='Silva (Professor)',
        is_staff=False,  # Professor não é staff
        is_superuser=False  # Professor não é superuser
    )
    print(f"\n✓ Django User criado: {user.username} (PROFESSOR)")
    
    # Adicionar ao grupo Professor
    try:
        grupo_professor = Group.objects.get(name='Professor')
        user.groups.add(grupo_professor)
        print(f"✓ Usuário adicionado ao grupo 'Professor'")
    except Group.DoesNotExist:
        print("⚠ Grupo 'Professor' não encontrado. Execute 'configurar_grupos_permissoes.py' primeiro!")
    
    # Buscar/criar tipo de usuário
    try:
        tipo_funcionario = TipoUsuario.objects.get(tipo='Funcionario')
    except TipoUsuario.DoesNotExist:
        tipo_funcionario = TipoUsuario.objects.create(tipo='Funcionario', ativo=True)
        print("✓ Tipo de usuário 'Funcionario' criado")
    
    # Criar Funcionario
    funcionario = Funcionario.objects.create(
        nome='Carlos Silva (Professor)',
        email=email,
        tipo_usuario=tipo_funcionario,
        matricula='PROF2025001',  # Matrícula única do professor
        departamento='Acadêmico',
        coordenador=True,  # Professor é coordenador
        ativo=True
    )
    print(f"✓ Funcionário criado: {funcionario.nome}")
    
    # Exibir credenciais
    print("\n" + "=" * 60)
    print("✅ USUÁRIO PROFESSOR CRIADO COM SUCESSO!")
    print("=" * 60)
    print(f"\n🔐 CREDENCIAIS DE LOGIN:")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Senha: {password}")
    print(f"\n👤 DADOS DO PROFESSOR:")
    print(f"   Nome: {funcionario.nome}")
    print(f"   Matrícula: {funcionario.matricula}")
    print(f"   Departamento: {funcionario.departamento}")
    print(f"   Coordenador: {'Sim' if funcionario.coordenador else 'Não'}")
    print(f"\n🎯 PERMISSÕES:")
    print(f"   - Publicar vagas de monitoria")
    print(f"   - Avaliar candidatos")
    print(f"   - Validar horas dos monitores")
    print(f"   - Gerenciar turmas e monitorias")
    print(f"   - Gerar relatórios")
    print(f"\n🌐 COMO FAZER LOGIN:")
    print(f"   1. Acesse: http://localhost:8000/login/")
    print(f"   2. Username: {username}")
    print(f"   3. Senha: {password}")
    print("\n" + "=" * 60)
    
    return user, funcionario

if __name__ == '__main__':
    criar_usuario_professor()
