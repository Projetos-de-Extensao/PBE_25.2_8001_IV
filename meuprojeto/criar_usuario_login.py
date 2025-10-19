#!/usr/bin/env python
"""
Script para criar usuário Django User + Aluno para login no sistema
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto.settings')
django.setup()

from django.contrib.auth.models import User
from plataforma_Casa.models import Usuario, TipoUsuario, Aluno, Curso
from datetime import date

def criar_usuario_aluno():
    """Cria um User Django + Aluno para login"""
    
    print("=" * 60)
    print("CRIANDO USUÁRIO ALUNO PARA LOGIN")
    print("=" * 60)
    
    # Credenciais
    username = 'aluno.teste'
    email = 'aluno.teste@casa.com'
    password = 'aluno123'
    
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
            Aluno.objects.filter(email=email).delete()
            print("✓ Usuário anterior removido")
    
    # Criar Django User (ALUNO - sem permissões de staff)
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name='João',
        last_name='da Silva (Teste)',
        is_staff=False,  # Aluno NÃO é staff
        is_superuser=False  # Aluno NÃO é superuser
    )
    print(f"\n✓ Django User criado: {user.username} (ALUNO - sem permissões admin)")
    
    # Buscar/criar tipo de usuário
    try:
        tipo_aluno = TipoUsuario.objects.get(tipo='Aluno')
    except TipoUsuario.DoesNotExist:
        tipo_aluno = TipoUsuario.objects.create(tipo='Aluno', ativo=True)
    
    # Buscar curso
    try:
        curso = Curso.objects.filter(ativo=True).first()
        if not curso:
            curso = Curso.objects.create(
                nome='Análise e Desenvolvimento de Sistemas',
                ativo=True
            )
    except:
        curso = Curso.objects.create(
            nome='Análise e Desenvolvimento de Sistemas',
            ativo=True
        )
    
    # Criar Aluno
    aluno = Aluno.objects.create(
        nome='João da Silva (Teste)',
        email=email,
        tipo_usuario=tipo_aluno,
        matricula='20250001',
        curso=curso,
        data_ingresso=date(2025, 1, 1),
        periodo=2,
        cr_geral=8.5,
        ativo=True
    )
    
    # Exibir credenciais
    print("\n" + "=" * 60)
    print("✅ USUÁRIO CRIADO COM SUCESSO!")
    print("=" * 60)
    print(f"\n🔐 CREDENCIAIS DE LOGIN:")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Senha: {password}")
    print(f"\n👤 DADOS DO ALUNO:")
    print(f"   Nome: {aluno.nome}")
    print(f"   Matrícula: {aluno.matricula}")
    print(f"   Curso: {aluno.curso.nome}")
    print(f"   Período: {aluno.periodo}º")
    print(f"   CR: {aluno.cr_geral}")
    print(f"\n🌐 COMO FAZER LOGIN:")
    print(f"   1. Acesse: http://localhost:8000/login/")
    print(f"   2. Username: {username}")
    print(f"   3. Senha: {password}")
    print("\n" + "=" * 60)
    
    return user, aluno

if __name__ == '__main__':
    criar_usuario_aluno()
