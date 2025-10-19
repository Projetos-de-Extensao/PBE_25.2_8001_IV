"""
Script para popular o banco de dados com dados de teste
Execute: python manage.py shell < popular_dados_teste.py
"""

import os
import django
import random
from datetime import date, datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto.settings')
django.setup()

from plataforma_Casa.models import (
    TipoUsuario, Usuario, Curso, Aluno, Funcionario, 
    Sala, Vaga, Turma, ParticipacaoMonitoria, Presenca, Inscricao
)

print("🚀 Iniciando população do banco de dados...")

# Limpar dados existentes (cuidado em produção!)
print("🗑️  Limpando dados antigos...")
Presenca.objects.all().delete()
ParticipacaoMonitoria.objects.all().delete()
Inscricao.objects.all().delete()
Turma.objects.all().delete()
Vaga.objects.all().delete()
Aluno.objects.all().delete()
Funcionario.objects.all().delete()
Sala.objects.all().delete()
Curso.objects.all().delete()

# Criar Tipos de Usuário
print("👥 Criando tipos de usuário...")
tipo_aluno, _ = TipoUsuario.objects.get_or_create(
    tipo='aluno',
    defaults={'ativo': True}
)
tipo_funcionario, _ = TipoUsuario.objects.get_or_create(
    tipo='funcionario',
    defaults={'ativo': True}
)
tipo_coordenador, _ = TipoUsuario.objects.get_or_create(
    tipo='coordenador',
    defaults={'ativo': True}
)

# Criar Cursos
print("📚 Criando cursos...")
cursos_data = [
    {'nome': 'Ciência da Computação'},
    {'nome': 'Sistemas de Informação'},
    {'nome': 'Engenharia de Software'},
    {'nome': 'Análise e Desenvolvimento de Sistemas'},
    {'nome': 'Redes de Computadores'},
]

cursos = []
for curso_data in cursos_data:
    curso = Curso.objects.create(
        nome=curso_data['nome'],
        ativo=True
    )
    cursos.append(curso)
    print(f"  ✅ Curso criado: {curso.nome}")

# Criar Salas
print("🚪 Criando salas...")
salas_data = [
    {'numero': 'Sala 101'},
    {'numero': 'Sala 102'},
    {'numero': 'Sala 201'},
    {'numero': 'Sala 202'},
    {'numero': 'Sala 301'},
    {'numero': 'Lab 01'},
    {'numero': 'Lab 02'},
]

salas = []
for sala_data in salas_data:
    sala = Sala.objects.create(
        numero=sala_data['numero'],
        ativo=True
    )
    salas.append(sala)
    print(f"  ✅ Sala criada: {sala.numero}")

# Criar Coordenadores (Funcionários)
print("👔 Criando coordenadores...")
coordenadores_data = [
    {'nome': 'Dr. João Silva', 'email': 'joao.silva@plataforma.com', 'matricula': 'FUNC001'},
    {'nome': 'Dra. Maria Santos', 'email': 'maria.santos@plataforma.com', 'matricula': 'FUNC002'},
    {'nome': 'Prof. Carlos Oliveira', 'email': 'carlos.oliveira@plataforma.com', 'matricula': 'FUNC003'},
    {'nome': 'Profa. Ana Costa', 'email': 'ana.costa@plataforma.com', 'matricula': 'FUNC004'},
]

coordenadores = []
for coord_data in coordenadores_data:
    funcionario = Funcionario.objects.create(
        nome=coord_data['nome'],
        email=coord_data['email'],
        matricula=coord_data['matricula'],
        tipo_usuario=tipo_coordenador,
        departamento='Coordenação',
        coordenador=True,
        ativo=True
    )
    coordenadores.append(funcionario)
    print(f"  ✅ Coordenador criado: {funcionario.nome}")

# Criar Alunos
print("🎓 Criando alunos...")
nomes_alunos = [
    'Pedro', 'Lucas', 'Gabriel', 'Rafael', 'Bruno',
    'Ana', 'Julia', 'Mariana', 'Beatriz', 'Camila',
    'Fernando', 'Ricardo', 'Gustavo', 'Diego', 'Thiago',
    'Carolina', 'Larissa', 'Fernanda', 'Patricia', 'Amanda'
]

sobrenomes = ['Silva', 'Santos', 'Oliveira', 'Costa', 'Souza', 'Lima', 'Pereira', 'Rodrigues']

alunos = []
for i, nome in enumerate(nomes_alunos, start=1):
    sobrenome = random.choice(sobrenomes)
    aluno = Aluno.objects.create(
        nome=f'{nome} {sobrenome}',
        email=f'{nome.lower()}.{sobrenome.lower()}@aluno.com',
        matricula=f'2024{i:04d}',
        tipo_usuario=tipo_aluno,
        curso=random.choice(cursos),
        periodo=random.randint(1, 8),
        cr_geral=round(random.uniform(6.0, 9.5), 2),
        data_ingresso=date(2024, random.randint(1, 12), 1),
        ativo=True
    )
    alunos.append(aluno)
    print(f"  ✅ Aluno criado: {aluno.nome} - {aluno.matricula}")

# Criar Vagas de Monitoria
print("💼 Criando vagas de monitoria...")
vagas_data = [
    {
        'nome': 'Projeto Back-End',
        'descricao': 'Turma de Projeto Back-end com foco em Django e Python',
        'requisitos': 'Precisa de conhecimento de Python e Django',
    },
    {
        'nome': 'Algoritmos e Estruturas de Dados',
        'descricao': 'Monitoria para auxiliar em exercícios de algoritmos e estruturas de dados',
        'requisitos': 'Conhecimento em Python ou Java, lógica de programação',
    },
    {
        'nome': 'Banco de Dados',
        'descricao': 'Monitoria de Banco de Dados com SQL, PostgreSQL e MySQL',
        'requisitos': 'Conhecimento em SQL e modelagem de dados',
    },
    {
        'nome': 'Programação Orientada a Objetos',
        'descricao': 'Auxílio em POO com Java e C++',
        'requisitos': 'Conhecimento em Java ou C++, paradigma OO',
    },
    {
        'nome': 'Desenvolvimento Web Front-End',
        'descricao': 'Monitoria de HTML, CSS, JavaScript e React',
        'requisitos': 'HTML, CSS, JavaScript básico',
    },
    {
        'nome': 'Redes de Computadores',
        'descricao': 'Monitoria de Redes, protocolos e configuração',
        'requisitos': 'Conhecimento em TCP/IP, roteamento',
    },
    {
        'nome': 'Inteligência Artificial',
        'descricao': 'Machine Learning e Deep Learning com Python',
        'requisitos': 'Python, NumPy, pandas, scikit-learn',
    },
    {
        'nome': 'Engenharia de Software',
        'descricao': 'Metodologias ágeis, UML e padrões de projeto',
        'requisitos': 'Conhecimento em Scrum, diagramas UML',
    },
]

vagas = []
for vaga_data in vagas_data:
    vaga = Vaga.objects.create(
        nome=vaga_data['nome'],
        curso=random.choice(cursos),
        coordenador=random.choice(coordenadores),
        descricao=vaga_data['descricao'],
        requisitos=vaga_data['requisitos'],
        ativo=random.choice([True, True, True, False])  # 75% ativas
    )
    # Adicionar monitores (alunos inscritos)
    num_inscritos = random.randint(0, 5)
    monitores = random.sample(alunos, min(num_inscritos, len(alunos)))
    vaga.monitores.set(monitores)
    vagas.append(vaga)
    print(f"  ✅ Vaga criada: {vaga.nome} ({vaga.monitores.count()} inscritos)")

# Criar Turmas
print("📖 Criando turmas...")
dias_semana_opcoes = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
horarios = ['08:00-10:00', '10:00-12:00', '14:00-16:00', '16:00-18:00', '18:00-20:00']

turmas = []
for i, vaga in enumerate(vagas[:6], start=1):  # Criar turmas para as 6 primeiras vagas
    if vaga.ativo:
        monitor = random.choice(alunos)
        turma = Turma.objects.create(
            nome=f'Turma {i} - {vaga.nome[:20]}',
            vaga=vaga,
            sala=random.choice(salas),
            descricao=f'Turma de monitoria para {vaga.nome}',
            data_inicio=date(2025, 9, 1),
            data_fim=date(2025, 12, 15),
            dias_da_semana=random.choice(dias_semana_opcoes),
            horario=random.choice(horarios),
            monitor=monitor,
            curso=vaga.curso,
            ativo=True
        )
        turmas.append(turma)
        print(f"  ✅ Turma criada: {turma.nome}")

# Criar Participações em Monitorias
print("📝 Criando participações em monitorias...")
for turma in turmas:
    num_participantes = random.randint(3, 8)
    participantes = random.sample(alunos, min(num_participantes, len(alunos)))
    
    for aluno in participantes:
        participacao = ParticipacaoMonitoria.objects.create(
            aluno=aluno,
            turma=turma,
            ap1=round(random.uniform(5.0, 10.0), 1) if random.choice([True, False]) else None,
            ap2=round(random.uniform(5.0, 10.0), 1) if random.choice([True, False]) else None,
            cr=round(random.uniform(5.0, 10.0), 1) if random.choice([True, False]) else None,
        )
    print(f"  ✅ {num_participantes} participações criadas para {turma.nome}")

# Criar Presenças
print("✅ Criando presenças...")
for turma in turmas:
    participacoes = ParticipacaoMonitoria.objects.filter(turma=turma)
    
    # Criar 10 datas de aula
    data_inicial = turma.data_inicio
    for semana in range(10):
        data_aula = data_inicial + timedelta(weeks=semana)
        
        for participacao in participacoes:
            presenca = Presenca.objects.create(
                aluno=participacao.aluno,
                turma=turma,
                data=data_aula,
                presente=random.choice([True, True, True, False])  # 75% de presença
            )
    print(f"  ✅ Presenças criadas para {turma.nome}")

# Criar Inscrições
print("📋 Criando inscrições...")
status_opcoes = ['Pendente', 'Aprovado', 'Rejeitado']
for vaga in vagas:
    num_inscricoes = random.randint(1, 8)
    inscritos = random.sample(alunos, min(num_inscricoes, len(alunos)))
    
    for aluno in inscritos:
        inscricao = Inscricao.objects.create(
            aluno=aluno,
            vaga=vaga,
            status=random.choice(status_opcoes),
            data_inscricao=datetime.now()
        )
    print(f"  ✅ {num_inscricoes} inscrições criadas para {vaga.nome}")

print("\n" + "="*60)
print("✅ Banco de dados populado com sucesso!")
print("="*60)
print(f"📊 Resumo:")
print(f"  • {len(cursos)} Cursos")
print(f"  • {len(salas)} Salas")
print(f"  • {len(coordenadores)} Coordenadores")
print(f"  • {len(alunos)} Alunos")
print(f"  • {len(vagas)} Vagas")
print(f"  • {len(turmas)} Turmas")
print(f"  • {ParticipacaoMonitoria.objects.count()} Participações em Monitorias")
print(f"  • {Presenca.objects.count()} Presenças registradas")
print(f"  • {Inscricao.objects.count()} Inscrições")
print("="*60)
