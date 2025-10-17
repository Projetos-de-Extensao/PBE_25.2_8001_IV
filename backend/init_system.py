#!/usr/bin/env python
"""
Script de Inicialização do Sistema de Gestão de Monitorias
===========================================================

Este script inicializa o sistema com dados básicos necessários:
- Tipos de usuários
- Usuários do sistema (admin, coordenador, monitor, aluno)
- Cursos
- Salas
- Dados de exemplo

Execute: python manage.py shell < init_system.py
Ou: python init_system.py
"""

import os
import sys
import django
from datetime import date, datetime, timedelta

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')
django.setup()

from django.contrib.auth import get_user_model
from gestao_monitoria.models import (
    TipoUsuario, Curso, Sala, Aluno, Funcionario, Vaga, Turma,
    ParticipacaoMonitoria, Presenca, Inscricao, HorarioDisponivel,
    AgendamentoMonitoria, SubmissaoHoras
)

User = get_user_model()

def print_section(title):
    """Imprime um título de seção"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def create_user_types():
    """Cria os tipos de usuários do sistema"""
    print_section("CRIANDO TIPOS DE USUÁRIOS")
    
    tipos = [
        {'tipo': 'Administrador', 'ativo': True},
        {'tipo': 'Coordenador', 'ativo': True},
        {'tipo': 'Professor', 'ativo': True},
        {'tipo': 'Monitor', 'ativo': True},
        {'tipo': 'Aluno', 'ativo': True},
        {'tipo': 'Funcionário', 'ativo': True},
    ]
    
    created_tipos = []
    for tipo_data in tipos:
        tipo, created = TipoUsuario.objects.get_or_create(
            tipo=tipo_data['tipo'],
            defaults={'ativo': tipo_data['ativo']}
        )
        status = "✓ Criado" if created else "→ Já existe"
        print(f"{status}: {tipo.tipo}")
        created_tipos.append(tipo)
    
    return created_tipos

def create_courses():
    """Cria cursos de exemplo"""
    print_section("CRIANDO CURSOS")
    
    cursos_data = [
        'Engenharia de Software',
        'Ciência da Computação',
        'Sistemas de Informação',
        'Análise e Desenvolvimento de Sistemas',
        'Engenharia de Computação',
        'Tecnologia da Informação',
    ]
    
    cursos = []
    for nome in cursos_data:
        curso, created = Curso.objects.get_or_create(
            nome=nome,
            defaults={'ativo': True}
        )
        status = "✓ Criado" if created else "→ Já existe"
        print(f"{status}: {curso.nome}")
        cursos.append(curso)
    
    return cursos

def create_rooms():
    """Cria salas de exemplo"""
    print_section("CRIANDO SALAS")
    
    salas_data = [
        'Sala 101', 'Sala 102', 'Sala 103', 'Sala 104', 'Sala 105',
        'Laboratório 1', 'Laboratório 2', 'Laboratório 3',
        'Auditório Principal', 'Sala de Reuniões'
    ]
    
    salas = []
    for numero in salas_data:
        sala, created = Sala.objects.get_or_create(
            numero=numero,
            defaults={'ativo': True}
        )
        status = "✓ Criado" if created else "→ Já existe"
        print(f"{status}: {sala.numero}")
        salas.append(sala)
    
    return salas

def create_admin_user(tipo_admin):
    """Cria usuário administrador"""
    print_section("CRIANDO USUÁRIO ADMINISTRADOR")
    
    username = 'admin'
    password = 'admin123'
    
    if User.objects.filter(username=username).exists():
        print(f"→ Usuário '{username}' já existe")
        user = User.objects.get(username=username)
    else:
        user = User.objects.create_superuser(
            username=username,
            email='admin@sistema.com',
            password=password,
            first_name='Administrador',
            last_name='Sistema'
        )
        print(f"✓ Criado: {username}")
        print(f"  Senha: {password}")
    
    return user

def create_coordinators(tipo_coordenador, cursos):
    """Cria coordenadores de curso"""
    print_section("CRIANDO COORDENADORES")
    
    coordenadores_data = [
        {
            'username': 'coord1',
            'password': 'coord123',
            'nome': 'Maria Silva',
            'email': 'maria.silva@sistema.com',
            'matricula': 'COORD001',
            'departamento': 'Coordenação de TI',
            'curso': cursos[0] if cursos else None
        },
        {
            'username': 'coord2',
            'password': 'coord123',
            'nome': 'João Santos',
            'email': 'joao.santos@sistema.com',
            'matricula': 'COORD002',
            'departamento': 'Coordenação de Engenharia',
            'curso': cursos[1] if len(cursos) > 1 else None
        },
    ]
    
    coordenadores = []
    for data in coordenadores_data:
        # Criar usuário Django
        user, user_created = User.objects.get_or_create(
            username=data['username'],
            defaults={
                'email': data['email'],
                'first_name': data['nome'].split()[0],
                'last_name': ' '.join(data['nome'].split()[1:]),
                'is_staff': True
            }
        )
        
        if user_created:
            user.set_password(data['password'])
            user.save()
        
        # Criar perfil de Funcionário (Coordenador)
        funcionario, func_created = Funcionario.objects.get_or_create(
            matricula=data['matricula'],
            defaults={
                'nome': data['nome'],
                'email': data['email'],
                'tipo_usuario': tipo_coordenador,
                'departamento': data['departamento'],
                'coordenador': True,
                'ativo': True
            }
        )
        
        status = "✓ Criado" if func_created else "→ Já existe"
        print(f"{status}: {data['nome']} (usuário: {data['username']}, senha: {data['password']})")
        coordenadores.append(funcionario)
    
    return coordenadores

def create_students(tipo_aluno, cursos):
    """Cria alunos de exemplo"""
    print_section("CRIANDO ALUNOS")
    
    alunos_data = [
        {
            'username': 'aluno1',
            'password': 'aluno123',
            'nome': 'Pedro Oliveira',
            'email': 'pedro.oliveira@aluno.com',
            'matricula': 'ALU001',
            'curso': cursos[0] if cursos else None,
            'periodo': 5,
            'cr_geral': 8.5
        },
        {
            'username': 'aluno2',
            'password': 'aluno123',
            'nome': 'Ana Costa',
            'email': 'ana.costa@aluno.com',
            'matricula': 'ALU002',
            'curso': cursos[0] if cursos else None,
            'periodo': 6,
            'cr_geral': 9.2
        },
        {
            'username': 'aluno3',
            'password': 'aluno123',
            'nome': 'Carlos Mendes',
            'email': 'carlos.mendes@aluno.com',
            'matricula': 'ALU003',
            'curso': cursos[1] if len(cursos) > 1 else cursos[0],
            'periodo': 4,
            'cr_geral': 7.8
        },
        {
            'username': 'monitor1',
            'password': 'monitor123',
            'nome': 'Julia Santos',
            'email': 'julia.santos@aluno.com',
            'matricula': 'MON001',
            'curso': cursos[0] if cursos else None,
            'periodo': 7,
            'cr_geral': 9.5
        },
        {
            'username': 'monitor2',
            'password': 'monitor123',
            'nome': 'Roberto Lima',
            'email': 'roberto.lima@aluno.com',
            'matricula': 'MON002',
            'curso': cursos[1] if len(cursos) > 1 else cursos[0],
            'periodo': 8,
            'cr_geral': 9.0
        },
    ]
    
    alunos = []
    for data in alunos_data:
        # Criar usuário Django
        user, user_created = User.objects.get_or_create(
            username=data['username'],
            defaults={
                'email': data['email'],
                'first_name': data['nome'].split()[0],
                'last_name': ' '.join(data['nome'].split()[1:])
            }
        )
        
        if user_created:
            user.set_password(data['password'])
            user.save()
        
        # Criar perfil de Aluno
        aluno, aluno_created = Aluno.objects.get_or_create(
            matricula=data['matricula'],
            defaults={
                'nome': data['nome'],
                'email': data['email'],
                'tipo_usuario': tipo_aluno,
                'curso': data['curso'],
                'data_ingresso': date(2020, 1, 1),
                'periodo': data['periodo'],
                'cr_geral': data['cr_geral'],
                'ativo': True
            }
        )
        
        tipo = "MONITOR" if 'monitor' in data['username'] else "ALUNO"
        status = "✓ Criado" if aluno_created else "→ Já existe"
        print(f"{status}: {data['nome']} [{tipo}] (usuário: {data['username']}, senha: {data['password']})")
        alunos.append(aluno)
    
    return alunos

def create_sample_vagas(coordenadores, cursos):
    """Cria vagas de monitoria de exemplo"""
    print_section("CRIANDO VAGAS DE MONITORIA")
    
    if not coordenadores or not cursos:
        print("⚠ Sem coordenadores ou cursos para criar vagas")
        return []
    
    vagas_data = [
        {
            'nome': 'Monitoria de Programação I',
            'curso': cursos[0],
            'coordenador': coordenadores[0],
            'descricao': 'Auxílio em programação básica e lógica',
            'requisitos': 'CR mínimo 8.0, aprovado na disciplina'
        },
        {
            'nome': 'Monitoria de Banco de Dados',
            'curso': cursos[0],
            'coordenador': coordenadores[0],
            'descricao': 'Suporte em SQL e modelagem de dados',
            'requisitos': 'CR mínimo 8.5, conhecimento em SQL'
        },
        {
            'nome': 'Monitoria de Estruturas de Dados',
            'curso': cursos[1] if len(cursos) > 1 else cursos[0],
            'coordenador': coordenadores[1] if len(coordenadores) > 1 else coordenadores[0],
            'descricao': 'Apoio em algoritmos e estruturas',
            'requisitos': 'CR mínimo 8.0, domínio de algoritmos'
        },
    ]
    
    vagas = []
    for data in vagas_data:
        vaga, created = Vaga.objects.get_or_create(
            nome=data['nome'],
            defaults={
                'curso': data['curso'],
                'coordenador': data['coordenador'],
                'descricao': data['descricao'],
                'requisitos': data['requisitos'],
                'ativo': True
            }
        )
        status = "✓ Criado" if created else "→ Já existe"
        print(f"{status}: {vaga.nome}")
        vagas.append(vaga)
    
    return vagas

def create_sample_turmas(vagas, salas, monitores):
    """Cria turmas de exemplo"""
    print_section("CRIANDO TURMAS")
    
    if not vagas or not salas or not monitores:
        print("⚠ Dados insuficientes para criar turmas")
        return []
    
    turmas_data = [
        {
            'nome': 'Turma A - Programação I',
            'vaga': vagas[0],
            'sala': salas[0],
            'monitor': monitores[0],
            'descricao': 'Horário matutino',
            'dias_da_semana': 'Segunda, Quarta, Sexta',
            'horario': '08:00 - 10:00'
        },
        {
            'nome': 'Turma B - Banco de Dados',
            'vaga': vagas[1] if len(vagas) > 1 else vagas[0],
            'sala': salas[1] if len(salas) > 1 else salas[0],
            'monitor': monitores[1] if len(monitores) > 1 else monitores[0],
            'descricao': 'Horário vespertino',
            'dias_da_semana': 'Terça, Quinta',
            'horario': '14:00 - 16:00'
        },
    ]
    
    turmas = []
    for data in turmas_data:
        turma, created = Turma.objects.get_or_create(
            nome=data['nome'],
            defaults={
                'vaga': data['vaga'],
                'sala': data['sala'],
                'monitor': data['monitor'],
                'curso': data['vaga'].curso,
                'descricao': data['descricao'],
                'data_inicio': date.today(),
                'data_fim': date.today() + timedelta(days=120),
                'dias_da_semana': data['dias_da_semana'],
                'horario': data['horario'],
                'ativo': True
            }
        )
        status = "✓ Criado" if created else "→ Já existe"
        print(f"{status}: {turma.nome}")
        turmas.append(turma)
    
    return turmas

def print_summary(tipos, cursos, salas, admin, coordenadores, alunos, vagas, turmas):
    """Imprime resumo da inicialização"""
    print_section("RESUMO DA INICIALIZAÇÃO")
    
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"  • Tipos de Usuário: {len(tipos)}")
    print(f"  • Cursos: {len(cursos)}")
    print(f"  • Salas: {len(salas)}")
    print(f"  • Coordenadores: {len(coordenadores)}")
    print(f"  • Alunos: {len(alunos)}")
    print(f"  • Vagas: {len(vagas)}")
    print(f"  • Turmas: {len(turmas)}")
    
    print(f"\n🔑 CREDENCIAIS DE ACESSO:")
    print(f"\n  ADMINISTRADOR:")
    print(f"    Usuário: admin")
    print(f"    Senha: admin123")
    
    print(f"\n  COORDENADORES:")
    print(f"    Usuário: coord1 | Senha: coord123")
    print(f"    Usuário: coord2 | Senha: coord123")
    
    print(f"\n  MONITORES:")
    print(f"    Usuário: monitor1 | Senha: monitor123")
    print(f"    Usuário: monitor2 | Senha: monitor123")
    
    print(f"\n  ALUNOS:")
    print(f"    Usuário: aluno1 | Senha: aluno123")
    print(f"    Usuário: aluno2 | Senha: aluno123")
    print(f"    Usuário: aluno3 | Senha: aluno123")
    
    print(f"\n🌐 ACESSO:")
    print(f"    Sistema: http://127.0.0.1:8000/")
    print(f"    Login: http://127.0.0.1:8000/login")
    print(f"    Admin: http://127.0.0.1:8000/admin/")
    
    print("\n" + "="*60)
    print("  ✅ SISTEMA INICIALIZADO COM SUCESSO!")
    print("="*60 + "\n")

def main():
    """Função principal de inicialização"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  🚀 INICIALIZAÇÃO DO SISTEMA DE GESTÃO DE MONITORIAS  ".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    try:
        # Criar dados básicos
        tipos = create_user_types()
        cursos = create_courses()
        salas = create_rooms()
        
        # Identificar tipos específicos
        tipo_admin = next((t for t in tipos if 'admin' in t.tipo.lower()), tipos[0])
        tipo_coordenador = next((t for t in tipos if 'coordenador' in t.tipo.lower()), tipos[0])
        tipo_aluno = next((t for t in tipos if 'aluno' in t.tipo.lower()), tipos[0])
        
        # Criar usuários
        admin = create_admin_user(tipo_admin)
        coordenadores = create_coordinators(tipo_coordenador, cursos)
        alunos = create_students(tipo_aluno, cursos)
        
        # Separar monitores dos alunos (últimos 2 da lista)
        monitores = alunos[-2:] if len(alunos) >= 2 else alunos
        
        # Criar dados de monitorias
        vagas = create_sample_vagas(coordenadores, cursos)
        turmas = create_sample_turmas(vagas, salas, monitores)
        
        # Imprimir resumo
        print_summary(tipos, cursos, salas, admin, coordenadores, alunos, vagas, turmas)
        
    except Exception as e:
        print(f"\n❌ ERRO durante a inicialização:")
        print(f"   {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
