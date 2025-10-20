"""
================================================================================
SCRIPT DE POPULAÇÃO DO BANCO DE DADOS COM DADOS DE TESTE
================================================================================

Este script popula o banco de dados com dados completos de teste para:
- TipoUsuario
- Cursos
- Salas
- Funcionários (Professores/Coordenadores)
- Alunos
- Vagas de Monitoria
- Turmas
- Inscrições
- Participações em Monitoria
- Presenças
- Documentos
- Registros de Horas
- Pagamentos

Uso no Heroku:
    heroku run "python meuprojeto/manage.py shell" --app plataformacasa < popular_dados_teste.py

Uso localmente:
    cd meuprojeto
    python manage.py shell < ../popular_dados_teste.py

================================================================================
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto.settings')
django.setup()

from django.contrib.auth.models import Group
from plataforma_Casa.models import (
    TipoUsuario, Curso, Sala, Usuario, Funcionario, Aluno, 
    Vaga, Turma, ParticipacaoMonitoria, Presenca, Inscricao,
    Documento, RegistroHoras, StatusPagamento
)
from datetime import date, datetime, timedelta, time
from decimal import Decimal
import random

print("=" * 80)
print("INICIALIZANDO SISTEMA - POPULAÇÃO DE DADOS DE TESTE")
print("=" * 80)

# =============================================================================
# 1. TIPOS DE USUÁRIO
# =============================================================================
print("\n1. Criando Tipos de Usuário...")
tipos_usuario_data = [
    {'tipo': 'Admin'},
    {'tipo': 'Professor'},
    {'tipo': 'Coordenador'},
    {'tipo': 'Aluno'},
    {'tipo': 'Monitor'},
]

for tipo_data in tipos_usuario_data:
    tipo, created = TipoUsuario.objects.get_or_create(tipo=tipo_data['tipo'])
    if created:
        print(f"  ✅ Tipo '{tipo.tipo}' criado")
    else:
        print(f"  ℹ️  Tipo '{tipo.tipo}' já existe")

# =============================================================================
# 2. CURSOS
# =============================================================================
print("\n2. Criando Cursos...")
cursos_data = [
    'Análise e Desenvolvimento de Sistemas',
    'Ciência da Computação',
    'Engenharia de Software',
    'Sistemas de Informação',
    'Gestão da Tecnologia da Informação',
]

cursos = {}
for curso_nome in cursos_data:
    curso, created = Curso.objects.get_or_create(nome=curso_nome)
    cursos[curso_nome] = curso
    if created:
        print(f"  ✅ Curso '{curso_nome}' criado")
    else:
        print(f"  ℹ️  Curso '{curso_nome}' já existe")

# =============================================================================
# 3. SALAS
# =============================================================================
print("\n3. Criando Salas...")
salas_data = ['101', '102', '103', '201', '202', '203', 'Lab 1', 'Lab 2', 'Auditório']

salas = {}
for sala_numero in salas_data:
    sala, created = Sala.objects.get_or_create(numero=sala_numero)
    salas[sala_numero] = sala
    if created:
        print(f"  ✅ Sala '{sala_numero}' criada")
    else:
        print(f"  ℹ️  Sala '{sala_numero}' já existe")

# =============================================================================
# 4. FUNCIONÁRIOS (PROFESSORES/COORDENADORES)
# =============================================================================
print("\n4. Criando Funcionários (Professores/Coordenadores)...")
tipo_professor = TipoUsuario.objects.get(tipo='Professor')

funcionarios_data = [
    {
        'nome': 'Prof. Carlos Silva',
        'email': 'carlos.silva@plataformacasa.com',
        'matricula': 'PROF001',
        'departamento': 'Computação',
        'coordenador': True
    },
    {
        'nome': 'Prof. Maria Santos',
        'email': 'maria.santos@plataformacasa.com',
        'matricula': 'PROF002',
        'departamento': 'Sistemas',
        'coordenador': True
    },
    {
        'nome': 'Prof. João Oliveira',
        'email': 'joao.oliveira@plataformacasa.com',
        'matricula': 'PROF003',
        'departamento': 'Engenharia',
        'coordenador': False
    },
]

funcionarios = []
for func_data in funcionarios_data:
    func, created = Funcionario.objects.get_or_create(
        email=func_data['email'],
        defaults={
            'nome': func_data['nome'],
            'tipo_usuario': tipo_professor,
            'matricula': func_data['matricula'],
            'departamento': func_data['departamento'],
            'coordenador': func_data['coordenador']
        }
    )
    funcionarios.append(func)
    if created:
        print(f"  ✅ Funcionário '{func.nome}' criado")
    else:
        print(f"  ℹ️  Funcionário '{func.nome}' já existe")

# =============================================================================
# 5. ALUNOS
# =============================================================================
print("\n5. Criando Alunos...")
tipo_aluno = TipoUsuario.objects.get(tipo='Aluno')

alunos_data = [
    {
        'nome': 'João Pedro Souza',
        'email': 'joao.souza@aluno.com',
        'matricula': '2024001',
        'curso': cursos['Ciência da Computação'],
        'data_ingresso': date(2024, 2, 1),
        'periodo': 3,
        'cr_geral': 8.5
    },
    {
        'nome': 'Maria Eduarda Lima',
        'email': 'maria.lima@aluno.com',
        'matricula': '2024002',
        'curso': cursos['Análise e Desenvolvimento de Sistemas'],
        'data_ingresso': date(2024, 2, 1),
        'periodo': 3,
        'cr_geral': 9.2
    },
    {
        'nome': 'Pedro Henrique Costa',
        'email': 'pedro.costa@aluno.com',
        'matricula': '2023001',
        'curso': cursos['Engenharia de Software'],
        'data_ingresso': date(2023, 2, 1),
        'periodo': 5,
        'cr_geral': 8.8
    },
    {
        'nome': 'Ana Carolina Oliveira',
        'email': 'ana.oliveira@aluno.com',
        'matricula': '2023002',
        'curso': cursos['Sistemas de Informação'],
        'data_ingresso': date(2023, 2, 1),
        'periodo': 5,
        'cr_geral': 9.5
    },
    {
        'nome': 'Lucas Gabriel Santos',
        'email': 'lucas.santos@aluno.com',
        'matricula': '2022001',
        'curso': cursos['Ciência da Computação'],
        'data_ingresso': date(2022, 2, 1),
        'periodo': 7,
        'cr_geral': 8.0
    },
]

alunos = []
for aluno_data in alunos_data:
    aluno, created = Aluno.objects.get_or_create(
        email=aluno_data['email'],
        defaults={
            'nome': aluno_data['nome'],
            'tipo_usuario': tipo_aluno,
            'matricula': aluno_data['matricula'],
            'curso': aluno_data['curso'],
            'data_ingresso': aluno_data['data_ingresso'],
            'periodo': aluno_data['periodo'],
            'cr_geral': aluno_data['cr_geral']
        }
    )
    alunos.append(aluno)
    if created:
        print(f"  ✅ Aluno '{aluno.nome}' criado")
    else:
        print(f"  ℹ️  Aluno '{aluno.nome}' já existe")

# =============================================================================
# 6. VAGAS DE MONITORIA
# =============================================================================
print("\n6. Criando Vagas de Monitoria...")

vagas_data = [
    {
        'nome': 'Monitor de Algoritmos',
        'curso': cursos['Ciência da Computação'],
        'coordenador': funcionarios[0],
        'descricao': 'Auxiliar alunos com dificuldades em algoritmos e estruturas de dados',
        'requisitos': 'CR mínimo 7.0, ter cursado Algoritmos com aprovação',
        'responsabilidades': 'Tirar dúvidas, preparar material de apoio, organizar grupos de estudo',
        'numero_vagas': 2,
        'disciplina': 'Algoritmos e Estruturas de Dados'
    },
    {
        'nome': 'Monitor de Banco de Dados',
        'curso': cursos['Sistemas de Informação'],
        'coordenador': funcionarios[1],
        'descricao': 'Apoio em disciplinas de banco de dados e SQL',
        'requisitos': 'CR mínimo 7.5, conhecimento em SQL e modelagem',
        'responsabilidades': 'Auxiliar em exercícios práticos, tirar dúvidas sobre SQL',
        'numero_vagas': 1,
        'disciplina': 'Banco de Dados'
    },
    {
        'nome': 'Monitor de Programação Web',
        'curso': cursos['Análise e Desenvolvimento de Sistemas'],
        'coordenador': funcionarios[0],
        'descricao': 'Ajudar alunos com desenvolvimento web (HTML, CSS, JavaScript)',
        'requisitos': 'CR mínimo 8.0, experiência com desenvolvimento web',
        'responsabilidades': 'Resolver dúvidas sobre código, revisar projetos',
        'numero_vagas': 2,
        'disciplina': 'Desenvolvimento Web'
    },
]

vagas = []
for vaga_data in vagas_data:
    vaga, created = Vaga.objects.get_or_create(
        nome=vaga_data['nome'],
        defaults=vaga_data
    )
    vagas.append(vaga)
    if created:
        print(f"  ✅ Vaga '{vaga.nome}' criada")
    else:
        print(f"  ℹ️  Vaga '{vaga.nome}' já existe")

# =============================================================================
# 7. INSCRIÇÕES EM VAGAS
# =============================================================================
print("\n7. Criando Inscrições em Vagas...")

inscricoes_data = [
    {'aluno': alunos[2], 'vaga': vagas[0], 'status': 'Aprovado'},
    {'aluno': alunos[3], 'vaga': vagas[1], 'status': 'Aprovado'},
    {'aluno': alunos[1], 'vaga': vagas[2], 'status': 'Pendente'},
    {'aluno': alunos[4], 'vaga': vagas[0], 'status': 'Entrevista'},
]

inscricoes = []
for insc_data in inscricoes_data:
    insc, created = Inscricao.objects.get_or_create(
        aluno=insc_data['aluno'],
        vaga=insc_data['vaga'],
        defaults={'status': insc_data['status']}
    )
    inscricoes.append(insc)
    if created:
        print(f"  ✅ Inscrição '{insc.aluno.nome}' em '{insc.vaga.nome}' criada")
    else:
        print(f"  ℹ️  Inscrição já existe")

# =============================================================================
# 8. TURMAS DE MONITORIA
# =============================================================================
print("\n8. Criando Turmas de Monitoria...")

turmas_data = [
    {
        'nome': 'Monitoria Algoritmos - Turma A',
        'vaga': vagas[0],
        'sala': salas['Lab 1'],
        'descricao': 'Turma de monitoria para auxiliar em algoritmos',
        'data_inicio': date(2025, 3, 1),
        'data_fim': date(2025, 7, 15),
        'dias_da_semana': 'Segunda, Quarta',
        'horario': '18:00 - 20:00',
        'monitor': alunos[2],  # Pedro Henrique (aprovado na vaga)
        'curso': cursos['Ciência da Computação']
    },
    {
        'nome': 'Monitoria Banco de Dados - Turma A',
        'vaga': vagas[1],
        'sala': salas['Lab 2'],
        'descricao': 'Turma de monitoria para banco de dados',
        'data_inicio': date(2025, 3, 1),
        'data_fim': date(2025, 7, 15),
        'dias_da_semana': 'Terça, Quinta',
        'horario': '19:00 - 21:00',
        'monitor': alunos[3],  # Ana Carolina (aprovada na vaga)
        'curso': cursos['Sistemas de Informação']
    },
]

turmas = []
for turma_data in turmas_data:
    turma, created = Turma.objects.get_or_create(
        nome=turma_data['nome'],
        defaults=turma_data
    )
    turmas.append(turma)
    if created:
        print(f"  ✅ Turma '{turma.nome}' criada")
    else:
        print(f"  ℹ️  Turma '{turma.nome}' já existe")

# =============================================================================
# 9. PARTICIPAÇÕES EM MONITORIA
# =============================================================================
print("\n9. Criando Participações em Monitoria...")

participacoes_data = [
    {'aluno': alunos[0], 'turma': turmas[0], 'ap1': Decimal('8.5'), 'ap2': Decimal('9.0'), 'cr': Decimal('8.75')},
    {'aluno': alunos[1], 'turma': turmas[0], 'ap1': Decimal('7.0'), 'ap2': Decimal('8.5'), 'cr': Decimal('7.75')},
    {'aluno': alunos[4], 'turma': turmas[1], 'ap1': Decimal('9.0'), 'ap2': Decimal('9.5'), 'cr': Decimal('9.25')},
]

for part_data in participacoes_data:
    part, created = ParticipacaoMonitoria.objects.get_or_create(
        aluno=part_data['aluno'],
        turma=part_data['turma'],
        defaults={'ap1': part_data['ap1'], 'ap2': part_data['ap2'], 'cr': part_data['cr']}
    )
    if created:
        print(f"  ✅ Participação '{part.aluno.nome}' em '{part.turma.nome}' criada")
    else:
        print(f"  ℹ️  Participação já existe")

# =============================================================================
# 10. PRESENÇAS
# =============================================================================
print("\n10. Criando Presenças...")

# Criar presenças para as últimas 4 semanas
hoje = date.today()
presencas_criadas = 0

for turma in turmas:
    participacoes = ParticipacaoMonitoria.objects.filter(turma=turma)
    
    for i in range(8):  # 8 aulas
        data_aula = hoje - timedelta(days=i*3)
        
        for participacao in participacoes:
            presente = random.choice([True, True, True, False])  # 75% de presença
            
            presenca, created = Presenca.objects.get_or_create(
                turma=turma,
                aluno=participacao.aluno,
                data=data_aula,
                defaults={'presente': presente}
            )
            if created:
                presencas_criadas += 1

print(f"  ✅ {presencas_criadas} presenças criadas")

# =============================================================================
# 11. REGISTROS DE HORAS (MONITORES)
# =============================================================================
print("\n11. Criando Registros de Horas...")

registros_criados = 0
for turma in turmas:
    monitor = turma.monitor
    
    # Criar 10 registros de horas para cada monitor
    for i in range(10):
        data_registro = hoje - timedelta(days=i*3)
        
        registro, created = RegistroHoras.objects.get_or_create(
            turma=turma,
            monitor=monitor,
            data=data_registro,
            defaults={
                'hora_inicio': time(18, 0),
                'hora_fim': time(20, 0),
                'descricao_atividade': f'Atendimento de monitoria - dia {data_registro.strftime("%d/%m")}',
                'status': random.choice(['Pendente', 'Aprovado', 'Aprovado']),
                'validado_por': funcionarios[0] if random.random() > 0.3 else None,
            }
        )
        if created:
            registros_criados += 1

print(f"  ✅ {registros_criados} registros de horas criados")

# =============================================================================
# 12. PAGAMENTOS
# =============================================================================
print("\n12. Criando Status de Pagamentos...")

pagamentos_criados = 0
for turma in turmas:
    monitor = turma.monitor
    
    # Criar pagamento semestral
    pagamento, created = StatusPagamento.objects.get_or_create(
        monitor=monitor,
        turma=turma,
        mes_referencia=date(2025, 7, 31),  # Final do semestre
        defaults={
            'status': 'Pendente',
            'observacao': 'Pagamento do primeiro semestre de 2025'
        }
    )
    if created:
        pagamentos_criados += 1
        print(f"  ✅ Pagamento para '{monitor.nome}' criado")
    else:
        print(f"  ℹ️  Pagamento já existe")

print(f"\n  Total: {pagamentos_criados} pagamentos criados")

# =============================================================================
# RESUMO FINAL
# =============================================================================
print("\n" + "=" * 80)
print("POPULAÇÃO DE DADOS CONCLUÍDA!")
print("=" * 80)
print(f"""
📊 ESTATÍSTICAS:
   - Tipos de Usuário: {TipoUsuario.objects.count()}
   - Cursos: {Curso.objects.count()}
   - Salas: {Sala.objects.count()}
   - Funcionários: {Funcionario.objects.count()}
   - Alunos: {Aluno.objects.count()}
   - Vagas: {Vaga.objects.count()}
   - Inscrições: {Inscricao.objects.count()}
   - Turmas: {Turma.objects.count()}
   - Participações: {ParticipacaoMonitoria.objects.count()}
   - Presenças: {Presenca.objects.count()}
   - Registros de Horas: {RegistroHoras.objects.count()}
   - Pagamentos: {StatusPagamento.objects.count()}
""")
print("✅ Sistema pronto para uso!")
print("=" * 80)
