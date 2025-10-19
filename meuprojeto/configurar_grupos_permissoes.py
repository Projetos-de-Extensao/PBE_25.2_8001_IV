#!/usr/bin/env python
"""
Script para configurar grupos de permissões no sistema
Cria os 4 perfis de usuário: Aluno, Monitor, Professor, Admin
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from plataforma_Casa.models import (
    Vaga, Inscricao, RegistroHoras, Turma, ParticipacaoMonitoria,
    Presenca, StatusPagamento
)

def criar_grupos_permissoes():
    """
    Cria os 4 grupos de usuários com suas permissões específicas
    """
    print("=" * 70)
    print("CONFIGURANDO GRUPOS E PERMISSÕES DO SISTEMA")
    print("=" * 70)
    
    # ==================== GRUPO: ALUNO (Candidato) ====================
    print("\n📚 Criando grupo: ALUNO (Candidato)")
    grupo_aluno, created = Group.objects.get_or_create(name='Aluno')
    
    # Permissões do Aluno
    permissoes_aluno = [
        # Pode ver vagas
        Permission.objects.get(codename='view_vaga', content_type=ContentType.objects.get_for_model(Vaga)),
        
        # Pode criar e ver suas próprias inscrições
        Permission.objects.get(codename='add_inscricao', content_type=ContentType.objects.get_for_model(Inscricao)),
        Permission.objects.get(codename='view_inscricao', content_type=ContentType.objects.get_for_model(Inscricao)),
    ]
    
    grupo_aluno.permissions.set(permissoes_aluno)
    print(f"   ✓ Grupo 'Aluno' configurado com {len(permissoes_aluno)} permissões")
    print(f"   - Ver vagas disponíveis")
    print(f"   - Candidatar-se a vagas")
    print(f"   - Ver suas inscrições")
    
    # ==================== GRUPO: MONITOR (Aluno Selecionado) ====================
    print("\n⭐ Criando grupo: MONITOR (Aluno Selecionado)")
    grupo_monitor, created = Group.objects.get_or_create(name='Monitor')
    
    # Permissões do Monitor = Aluno + registro de horas
    permissoes_monitor = permissoes_aluno + [
        # Pode registrar horas
        Permission.objects.get(codename='add_registrohoras', content_type=ContentType.objects.get_for_model(RegistroHoras)),
        Permission.objects.get(codename='view_registrohoras', content_type=ContentType.objects.get_for_model(RegistroHoras)),
        Permission.objects.get(codename='change_registrohoras', content_type=ContentType.objects.get_for_model(RegistroHoras)),
        
        # Pode ver suas monitorias
        Permission.objects.get(codename='view_participacaomonitoria', content_type=ContentType.objects.get_for_model(ParticipacaoMonitoria)),
        
        # Pode ver presenças
        Permission.objects.get(codename='view_presenca', content_type=ContentType.objects.get_for_model(Presenca)),
    ]
    
    grupo_monitor.permissions.set(permissoes_monitor)
    print(f"   ✓ Grupo 'Monitor' configurado com {len(permissoes_monitor)} permissões")
    print(f"   - Todas as permissões de Aluno")
    print(f"   - Registrar horas trabalhadas")
    print(f"   - Ver registros de horas")
    print(f"   - Ver suas monitorias")
    
    # ==================== GRUPO: PROFESSOR/COORDENADOR ====================
    print("\n👨‍🏫 Criando grupo: PROFESSOR (Coordenador/Supervisor)")
    grupo_professor, created = Group.objects.get_or_create(name='Professor')
    
    # Permissões do Professor
    permissoes_professor = [
        # Gerenciar vagas
        Permission.objects.get(codename='add_vaga', content_type=ContentType.objects.get_for_model(Vaga)),
        Permission.objects.get(codename='view_vaga', content_type=ContentType.objects.get_for_model(Vaga)),
        Permission.objects.get(codename='change_vaga', content_type=ContentType.objects.get_for_model(Vaga)),
        
        # Avaliar candidatos
        Permission.objects.get(codename='view_inscricao', content_type=ContentType.objects.get_for_model(Inscricao)),
        Permission.objects.get(codename='change_inscricao', content_type=ContentType.objects.get_for_model(Inscricao)),
        
        # Validar horas
        Permission.objects.get(codename='view_registrohoras', content_type=ContentType.objects.get_for_model(RegistroHoras)),
        Permission.objects.get(codename='change_registrohoras', content_type=ContentType.objects.get_for_model(RegistroHoras)),
        
        # Gerenciar turmas e monitorias
        Permission.objects.get(codename='view_turma', content_type=ContentType.objects.get_for_model(Turma)),
        Permission.objects.get(codename='change_turma', content_type=ContentType.objects.get_for_model(Turma)),
        Permission.objects.get(codename='view_participacaomonitoria', content_type=ContentType.objects.get_for_model(ParticipacaoMonitoria)),
        Permission.objects.get(codename='change_participacaomonitoria', content_type=ContentType.objects.get_for_model(ParticipacaoMonitoria)),
        
        # Ver presenças
        Permission.objects.get(codename='view_presenca', content_type=ContentType.objects.get_for_model(Presenca)),
        Permission.objects.get(codename='change_presenca', content_type=ContentType.objects.get_for_model(Presenca)),
    ]
    
    grupo_professor.permissions.set(permissoes_professor)
    print(f"   ✓ Grupo 'Professor' configurado com {len(permissoes_professor)} permissões")
    print(f"   - Publicar e gerenciar vagas")
    print(f"   - Avaliar candidatos")
    print(f"   - Validar horas dos monitores")
    print(f"   - Gerenciar turmas e monitorias")
    print(f"   - Avaliar desempenho dos monitores")
    
    # ==================== GRUPO: ADMIN/DEPARTAMENTO ====================
    print("\n👨‍💼 Criando grupo: ADMIN (Departamento/Gestão)")
    grupo_admin, created = Group.objects.get_or_create(name='Administrador')
    
    # Admin tem todas as permissões via is_staff/is_superuser
    # Mas vamos documentar o que eles podem fazer
    print(f"   ✓ Grupo 'Administrador' configurado")
    print(f"   - Acesso COMPLETO ao sistema (via is_staff/is_superuser)")
    print(f"   - Dashboard de gestão")
    print(f"   - Gerenciar pagamentos")
    print(f"   - Relatórios gerais")
    print(f"   - Cadastros do sistema")
    print(f"   - Todas as funcionalidades")
    
    # ==================== RESUMO ====================
    print("\n" + "=" * 70)
    print("✅ GRUPOS CONFIGURADOS COM SUCESSO!")
    print("=" * 70)
    print("\n📋 RESUMO DOS GRUPOS:")
    print(f"   1. 👨‍🎓 Aluno (Candidato)       - {grupo_aluno.permissions.count()} permissões")
    print(f"   2. ⭐ Monitor                  - {grupo_monitor.permissions.count()} permissões")
    print(f"   3. 👨‍🏫 Professor (Coordenador) - {grupo_professor.permissions.count()} permissões")
    print(f"   4. 👨‍💼 Administrador (Gestão)  - Acesso total (is_staff)")
    
    print("\n💡 PRÓXIMOS PASSOS:")
    print("   1. Atribuir usuários aos grupos usando: atribuir_usuario_grupo.py")
    print("   2. Testar login com cada perfil")
    print("   3. Verificar menus específicos para cada grupo")
    print("\n" + "=" * 70)
    
    return {
        'aluno': grupo_aluno,
        'monitor': grupo_monitor,
        'professor': grupo_professor,
        'admin': grupo_admin
    }

if __name__ == '__main__':
    try:
        grupos = criar_grupos_permissoes()
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
