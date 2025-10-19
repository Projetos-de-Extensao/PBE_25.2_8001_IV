#!/usr/bin/env python
"""
Script para atribuir usuários aos grupos de permissão
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto.settings')
django.setup()

from django.contrib.auth.models import User, Group

def atribuir_grupos():
    """Atribui os usuários existentes aos seus respectivos grupos"""
    
    print("=" * 70)
    print("ATRIBUINDO USUÁRIOS AOS GRUPOS")
    print("=" * 70)
    
    # Buscar grupos
    grupo_aluno = Group.objects.get(name='Aluno')
    grupo_monitor = Group.objects.get(name='Monitor')
    grupo_professor = Group.objects.get(name='Professor')
    
    # ==================== ALUNO ====================
    print("\n👨‍🎓 Configurando usuário ALUNO...")
    try:
        user_aluno = User.objects.get(username='aluno.teste')
        user_aluno.groups.clear()  # Remove grupos antigos
        user_aluno.groups.add(grupo_aluno)  # Adiciona ao grupo Aluno
        user_aluno.is_staff = False
        user_aluno.is_superuser = False
        user_aluno.save()
        print(f"   ✓ {user_aluno.username} → Grupo: Aluno")
        print(f"   - Portal de Vagas (visualizar)")
        print(f"   - Candidatar-se a vagas")
        print(f"   - Ver suas inscrições")
    except User.DoesNotExist:
        print("   ⚠ Usuário 'aluno.teste' não encontrado")
    
    # ==================== MONITOR ====================
    print("\n⭐ Criando usuário MONITOR...")
    user_monitor, created = User.objects.get_or_create(
        username='monitor.teste',
        defaults={
            'email': 'monitor.teste@casa.com',
            'first_name': 'Maria',
            'last_name': 'Santos (Monitor)',
            'is_staff': False,
            'is_superuser': False
        }
    )
    if created:
        user_monitor.set_password('monitor123')
        user_monitor.save()
        print(f"   ✓ Usuário criado: {user_monitor.username}")
    else:
        print(f"   ✓ Usuário encontrado: {user_monitor.username}")
    
    user_monitor.groups.clear()
    user_monitor.groups.add(grupo_monitor)
    user_monitor.is_staff = False
    user_monitor.is_superuser = False
    user_monitor.save()
    print(f"   ✓ {user_monitor.username} → Grupo: Monitor")
    print(f"   - Todas as funcionalidades de Aluno")
    print(f"   - Registrar horas trabalhadas")
    print(f"   - Ver dashboard do monitor")
    
    # ==================== PROFESSOR ====================
    print("\n👨‍🏫 Criando usuário PROFESSOR...")
    user_professor, created = User.objects.get_or_create(
        username='professor.teste',
        defaults={
            'email': 'professor.teste@casa.com',
            'first_name': 'Carlos',
            'last_name': 'Silva (Professor)',
            'is_staff': False,
            'is_superuser': False
        }
    )
    if created:
        user_professor.set_password('professor123')
        user_professor.save()
        print(f"   ✓ Usuário criado: {user_professor.username}")
    else:
        print(f"   ✓ Usuário encontrado: {user_professor.username}")
    
    user_professor.groups.clear()
    user_professor.groups.add(grupo_professor)
    user_professor.is_staff = False
    user_professor.is_superuser = False
    user_professor.save()
    print(f"   ✓ {user_professor.username} → Grupo: Professor")
    print(f"   - Publicar vagas")
    print(f"   - Avaliar candidatos")
    print(f"   - Validar horas dos monitores")
    print(f"   - Gerenciar turmas e monitorias")
    
    # ==================== ADMIN ====================
    print("\n👨‍💼 Configurando usuário ADMIN...")
    try:
        user_admin = User.objects.get(username='admin')
        user_admin.is_staff = True
        user_admin.is_superuser = True
        user_admin.save()
        print(f"   ✓ {user_admin.username} → is_staff=True, is_superuser=True")
        print(f"   - Acesso COMPLETO ao sistema")
    except User.DoesNotExist:
        print("   ⚠ Usuário 'admin' não encontrado")
    
    # ==================== RESUMO ====================
    print("\n" + "=" * 70)
    print("✅ USUÁRIOS CONFIGURADOS COM SUCESSO!")
    print("=" * 70)
    print("\n🔑 CREDENCIAIS DE ACESSO:")
    print("\n1. 👨‍🎓 ALUNO (Candidato):")
    print("   Username: aluno.teste")
    print("   Senha: aluno123")
    print("   Menu: Portal de Vagas")
    
    print("\n2. ⭐ MONITOR (Aluno Selecionado):")
    print("   Username: monitor.teste")
    print("   Senha: monitor123")
    print("   Menu: Portal + Registro de Horas + Dashboard Monitor")
    
    print("\n3. 👨‍🏫 PROFESSOR (Coordenador):")
    print("   Username: professor.teste")
    print("   Senha: professor123")
    print("   Menu: Vagas + Avaliar + Validar Horas + Relatórios")
    
    print("\n4. 👨‍💼 ADMIN (Departamento):")
    print("   Username: admin")
    print("   Senha: admin")
    print("   Menu: TUDO")
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    try:
        atribuir_grupos()
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
