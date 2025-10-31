"""
Comando Django para popular o banco de dados com dados de teste completos
Uso: python manage.py popular_dados
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User
from plataforma_Casa.models import (
    TipoUsuario, Curso, Sala, Usuario, Funcionario, Aluno, 
    Vaga, Turma, ParticipacaoMonitoria, Presenca, Inscricao,
    Documento, RegistroHoras, StatusPagamento
)
from datetime import date, datetime, timedelta, time
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de teste completos'

    def handle(self, *args, **kwargs):
        self.stdout.write("=" * 80)
        self.stdout.write("INICIALIZANDO POPULAÇÃO DE DADOS DE TESTE")
        self.stdout.write("=" * 80)

        # Criar grupos se não existirem
        self.criar_grupos()
        
        # Criar usuários de demonstração
        self.criar_usuarios_demo()
        
        # Criar dados básicos
        self.criar_tipos_usuario()
        self.criar_cursos()
        self.criar_salas()
        
        # Criar funcionários e alunos
        self.criar_funcionarios()
        self.criar_alunos()
        
        # Criar vagas e turmas
        self.criar_vagas()
        self.criar_turmas()
        
        # Criar inscrições
        self.criar_inscricoes()
        
        # Criar participações em monitoria
        self.criar_participacoes()
        
        # Criar presenças
        self.criar_presencas()
        
        # Criar registros de horas
        self.criar_registros_horas()
        
        # Criar pagamentos
        self.criar_pagamentos()
        
        self.stdout.write(self.style.SUCCESS("\n" + "=" * 80))
        self.stdout.write(self.style.SUCCESS("POPULAÇÃO CONCLUÍDA COM SUCESSO!"))
        self.stdout.write(self.style.SUCCESS("=" * 80))
        self.stdout.write("\n📋 USUÁRIOS DE DEMONSTRAÇÃO CRIADOS:\n")
        self.stdout.write("  🎓 Aluno: aluno.teste / aluno123")
        self.stdout.write("  👨‍🏫 Monitor: monitor.teste / monitor123")
        self.stdout.write("  👨‍🔬 Professor: professor.teste / professor123")
        self.stdout.write("  👑 Admin: admin / admin123")
        self.stdout.write("\n")

    def criar_grupos(self):
        """Cria os grupos de usuários se não existirem"""
        self.stdout.write("\n📁 Criando grupos de usuários...")
        grupos = ['Aluno', 'Monitor', 'Professor', 'Admin']
        for nome in grupos:
            grupo, created = Group.objects.get_or_create(name=nome)
            if created:
                self.stdout.write(f"  ✅ Grupo '{nome}' criado")
            else:
                self.stdout.write(f"  ℹ️  Grupo '{nome}' já existe")

    def criar_usuarios_demo(self):
        """Cria os usuários de demonstração conforme especificado"""
        self.stdout.write("\n👥 Criando usuários de demonstração...")
        
        # 1. ALUNO
        if not User.objects.filter(username='aluno.teste').exists():
            user_aluno = User.objects.create_user(
                username='aluno.teste',
                email='aluno.teste@faculdade.edu.br',
                password='aluno123',
                first_name='João',
                last_name='Silva'
            )
            user_aluno.groups.add(Group.objects.get(name='Aluno'))
            self.stdout.write("  ✅ Aluno: aluno.teste / aluno123")
        else:
            user_aluno = User.objects.get(username='aluno.teste')
            user_aluno.set_password('aluno123')
            user_aluno.save()
            self.stdout.write("  ✅ Senha do aluno.teste atualizada")
        
        # 2. MONITOR
        if not User.objects.filter(username='monitor.teste').exists():
            user_monitor = User.objects.create_user(
                username='monitor.teste',
                email='monitor.teste@faculdade.edu.br',
                password='monitor123',
                first_name='Maria',
                last_name='Santos'
            )
            user_monitor.groups.add(Group.objects.get(name='Monitor'))
            self.stdout.write("  ✅ Monitor: monitor.teste / monitor123")
        else:
            user_monitor = User.objects.get(username='monitor.teste')
            user_monitor.set_password('monitor123')
            user_monitor.save()
            self.stdout.write("  ✅ Senha do monitor.teste atualizada")
        
        # 3. PROFESSOR
        if not User.objects.filter(username='professor.teste').exists():
            user_professor = User.objects.create_user(
                username='professor.teste',
                email='professor.teste@faculdade.edu.br',
                password='professor123',
                first_name='Dr. Carlos',
                last_name='Oliveira',
                is_staff=True
            )
            user_professor.groups.add(Group.objects.get(name='Professor'))
            self.stdout.write("  ✅ Professor: professor.teste / professor123")
        else:
            user_professor = User.objects.get(username='professor.teste')
            user_professor.set_password('professor123')
            user_professor.is_staff = True
            user_professor.save()
            self.stdout.write("  ✅ Senha do professor.teste atualizada")
        
        # 4. ADMIN
        if not User.objects.filter(username='admin').exists():
            user_admin = User.objects.create_superuser(
                username='admin',
                email='admin@faculdade.edu.br',
                password='admin123',
                first_name='Administrador',
                last_name='Sistema'
            )
            self.stdout.write("  ✅ Admin: admin / admin123")
        else:
            user_admin = User.objects.get(username='admin')
            user_admin.set_password('admin123')
            user_admin.is_superuser = True
            user_admin.is_staff = True
            user_admin.save()
            self.stdout.write("  ✅ Senha do admin atualizada")

    def criar_tipos_usuario(self):
        """Cria os tipos de usuário"""
        self.stdout.write("\n📋 Criando tipos de usuário...")
        tipos = ['Aluno', 'Monitor', 'Professor', 'Coordenador', 'Administrador']
        for tipo in tipos:
            obj, created = TipoUsuario.objects.get_or_create(tipo=tipo)
            if created:
                self.stdout.write(f"  ✅ Tipo '{tipo}' criado")

    def criar_cursos(self):
        """Cria cursos"""
        self.stdout.write("\n🎓 Criando cursos...")
        cursos = [
            'Ciência da Computação',
            'Sistemas de Informação',
            'Engenharia de Software',
            'Análise e Desenvolvimento de Sistemas',
            'Redes de Computadores',
        ]
        for nome_curso in cursos:
            obj, created = Curso.objects.get_or_create(nome=nome_curso)
            if created:
                self.stdout.write(f"  ✅ Curso '{nome_curso}' criado")

    def criar_salas(self):
        """Cria salas"""
        self.stdout.write("\n🏢 Criando salas...")
        salas = ['Lab 101', 'Lab 102', 'Sala 201', 'Sala 202', 'Auditório']
        for numero_sala in salas:
            obj, created = Sala.objects.get_or_create(numero=numero_sala)
            if created:
                self.stdout.write(f"  ✅ Sala '{numero_sala}' criada")

    def criar_funcionarios(self):
        """Cria funcionários (professores)"""
        self.stdout.write("\n👨‍🏫 Criando funcionários...")
        
        # Buscar tipo_usuario Professor
        tipo_professor, _ = TipoUsuario.objects.get_or_create(tipo='Professor')
        tipo_coordenador, _ = TipoUsuario.objects.get_or_create(tipo='Coordenador')
        
        # Professor de demonstração
        if not Funcionario.objects.filter(email='professor.teste@faculdade.edu.br').exists():
            Funcionario.objects.create(
                nome='Dr. Carlos Oliveira',
                email='professor.teste@faculdade.edu.br',
                tipo_usuario=tipo_professor,
                matricula='PROF001',
                departamento='Ciência da Computação',
                funcao='Professor Adjunto',  # ✅ Adicionado
                coordenador=False
            )
            self.stdout.write("  ✅ Professor de teste criado")
        
        # Outros professores
        professores = [
            {'nome': 'Prof. Ana Silva', 'email': 'ana.silva@faculdade.edu.br', 'matricula': 'PROF002', 'dept': 'Sistemas de Informação', 'funcao': 'Coordenadora', 'coord': True},
            {'nome': 'Prof. João Santos', 'email': 'joao.santos@faculdade.edu.br', 'matricula': 'PROF003', 'dept': 'Engenharia de Software', 'funcao': 'Professor Titular', 'coord': False},
            {'nome': 'Prof. Maria Costa', 'email': 'maria.costa@faculdade.edu.br', 'matricula': 'PROF004', 'dept': 'Análise e Desenvolvimento de Sistemas', 'funcao': 'Professora Assistente', 'coord': False},
        ]
        
        for prof in professores:
            if not Funcionario.objects.filter(email=prof['email']).exists():
                Funcionario.objects.create(
                    nome=prof['nome'],
                    email=prof['email'],
                    tipo_usuario=tipo_coordenador if prof['coord'] else tipo_professor,
                    matricula=prof['matricula'],
                    departamento=prof['dept'],
                    funcao=prof['funcao'],  # ✅ Adicionado
                    coordenador=prof['coord']
                )
                self.stdout.write(f"  ✅ {prof['nome']} criado")

    def criar_alunos(self):
        """Cria alunos"""
        self.stdout.write("\n🎓 Criando alunos...")
        
        cursos = list(Curso.objects.all())
        if not cursos:
            self.stdout.write("  ⚠️  Nenhum curso disponível")
            return
        
        # Buscar tipo_usuario Aluno e Monitor
        tipo_aluno, _ = TipoUsuario.objects.get_or_create(tipo='Aluno')
        tipo_monitor, _ = TipoUsuario.objects.get_or_create(tipo='Monitor')
        
        # Aluno de demonstração
        if not Aluno.objects.filter(email='aluno.teste@faculdade.edu.br').exists():
            Aluno.objects.create(
                nome='João Silva',
                email='aluno.teste@faculdade.edu.br',
                tipo_usuario=tipo_aluno,
                matricula='2024001',
                curso=cursos[0],
                data_ingresso=date.today() - timedelta(days=730),  # 2 anos atrás
                periodo=4,
                cr_geral=8.5
            )
            self.stdout.write("  ✅ Aluno de teste criado")
        
        # Monitor de demonstração
        if not Aluno.objects.filter(email='monitor.teste@faculdade.edu.br').exists():
            Aluno.objects.create(
                nome='Maria Santos',
                email='monitor.teste@faculdade.edu.br',
                tipo_usuario=tipo_monitor,
                matricula='2023001',
                curso=cursos[0],
                data_ingresso=date.today() - timedelta(days=1095),  # 3 anos atrás
                periodo=6,
                cr_geral=9.2
            )
            self.stdout.write("  ✅ Monitor de teste criado")
        
        # Criar mais alunos
        alunos_data = [
            {'nome': 'Pedro Almeida', 'email': 'pedro.almeida@faculdade.edu.br', 'matricula': '2024002', 'periodo': 3, 'cr': 7.8},
            {'nome': 'Ana Paula', 'email': 'ana.paula@faculdade.edu.br', 'matricula': '2024003', 'periodo': 5, 'cr': 8.9},
            {'nome': 'Lucas Ferreira', 'email': 'lucas.ferreira@faculdade.edu.br', 'matricula': '2023002', 'periodo': 7, 'cr': 9.5},
            {'nome': 'Juliana Costa', 'email': 'juliana.costa@faculdade.edu.br', 'matricula': '2023003', 'periodo': 6, 'cr': 8.7},
            {'nome': 'Rafael Lima', 'email': 'rafael.lima@faculdade.edu.br', 'matricula': '2024004', 'periodo': 2, 'cr': 7.5},
        ]
        
        for aluno_data in alunos_data:
            if not Aluno.objects.filter(email=aluno_data['email']).exists():
                periodo_anos = aluno_data['periodo'] / 2
                Aluno.objects.create(
                    nome=aluno_data['nome'],
                    email=aluno_data['email'],
                    tipo_usuario=tipo_aluno,
                    matricula=aluno_data['matricula'],
                    curso=random.choice(cursos),
                    data_ingresso=date.today() - timedelta(days=int(365 * periodo_anos)),
                    periodo=aluno_data['periodo'],
                    cr_geral=aluno_data['cr']
                )
                self.stdout.write(f"  ✅ {aluno_data['nome']} criado")

    def criar_vagas(self):
        """Cria vagas de monitoria"""
        self.stdout.write("\n📢 Criando vagas de monitoria...")
        
        from plataforma_Casa.models import Disciplina
        
        cursos = list(Curso.objects.all())
        coordenadores = list(Funcionario.objects.all())
        
        if not coordenadores:
            self.stdout.write("  ⚠️  Nenhum coordenador disponível")
            return
        
        if not cursos:
            self.stdout.write("  ⚠️  Nenhum curso disponível")
            return
        
        # Primeiro, criar as disciplinas
        disciplinas_data = [
            {
                'codigo': 'CC101',
                'nome': 'Programação I',
                'carga_horaria': 80,
                'periodo_sugerido': 1,
                'ementa': 'Introdução à lógica de programação e algoritmos'
            },
            {
                'codigo': 'CC201',
                'nome': 'Estruturas de Dados',
                'carga_horaria': 80,
                'periodo_sugerido': 3,
                'ementa': 'Estruturas de dados lineares e não-lineares'
            },
            {
                'codigo': 'CC301',
                'nome': 'Banco de Dados',
                'carga_horaria': 60,
                'periodo_sugerido': 4,
                'ementa': 'Modelagem e implementação de bancos de dados'
            },
            {
                'codigo': 'CC102',
                'nome': 'Cálculo I',
                'carga_horaria': 80,
                'periodo_sugerido': 1,
                'ementa': 'Limites, derivadas e aplicações'
            },
            {
                'codigo': 'CC103',
                'nome': 'Física I',
                'carga_horaria': 80,
                'periodo_sugerido': 2,
                'ementa': 'Mecânica clássica e cinemática'
            },
        ]
        
        for disc_data in disciplinas_data:
            curso = random.choice(cursos)
            disciplina, created = Disciplina.objects.get_or_create(
                codigo=disc_data['codigo'],
                defaults={
                    'nome': disc_data['nome'],
                    'curso': curso,
                    'carga_horaria': disc_data['carga_horaria'],
                    'periodo_sugerido': disc_data['periodo_sugerido'],
                    'ementa': disc_data['ementa'],
                }
            )
            if created:
                self.stdout.write(f"  ✅ Disciplina '{disc_data['nome']}' criada")
        
        # Agora criar as vagas usando as disciplinas
        vagas_data = [
            {
                'nome': 'Monitor de Programação I',
                'disciplina_codigo': 'CC101',
                'descricao': 'Auxiliar alunos em exercícios de lógica de programação',
                'requisitos': 'CR mínimo 8.0, ter cursado a disciplina',
                'numero_vagas': 2,
                'tipo_vaga': 'TEA',
                'valor_bolsa': 1500.00,
            },
            {
                'nome': 'Monitor de Estruturas de Dados',
                'disciplina_codigo': 'CC201',
                'descricao': 'Apoio em listas, árvores, grafos e algoritmos',
                'requisitos': 'CR mínimo 8.5',
                'numero_vagas': 1,
                'tipo_vaga': 'TEA',
                'valor_bolsa': 1500.00,
            },
            {
                'nome': 'Monitor de Banco de Dados',
                'disciplina_codigo': 'CC301',
                'descricao': 'Ajuda com SQL, modelagem e normalização',
                'requisitos': 'CR mínimo 7.5',
                'numero_vagas': 2,
                'tipo_vaga': 'Voluntaria',
            },
            {
                'nome': 'Monitor de Cálculo I',
                'disciplina_codigo': 'CC102',
                'descricao': 'Apoio em exercícios de derivadas e limites',
                'requisitos': 'CR mínimo 8.0',
                'numero_vagas': 2,
                'tipo_vaga': 'Voluntaria',
            },
            {
                'nome': 'Monitor de Física I',
                'disciplina_codigo': 'CC103',
                'descricao': 'Auxílio em problemas de mecânica e cinemática',
                'requisitos': 'CR mínimo 7.5',
                'numero_vagas': 1,
                'tipo_vaga': 'TEA',
                'valor_bolsa': 1500.00,
            },
        ]
        
        for vaga_data in vagas_data:
            try:
                disciplina = Disciplina.objects.get(codigo=vaga_data['disciplina_codigo'])
                
                if not Vaga.objects.filter(disciplina=disciplina, nome=vaga_data['nome']).exists():
                    vaga_params = {
                        'nome': vaga_data['nome'],
                        'disciplina': disciplina,
                        'descricao': vaga_data['descricao'],
                        'requisitos': vaga_data['requisitos'],
                        'responsabilidades': vaga_data['descricao'],
                        'numero_vagas': vaga_data['numero_vagas'],
                        'curso': disciplina.curso,
                    }
                    
                    # Adicionar coordenadores
                    coordenador = random.choice(coordenadores)
                    
                    # Adicionar tipo de vaga e valor da bolsa se TEA
                    if 'tipo_vaga' in vaga_data:
                        vaga_params['tipo_vaga'] = vaga_data['tipo_vaga']
                    if 'valor_bolsa' in vaga_data:
                        vaga_params['valor_bolsa'] = vaga_data['valor_bolsa']
                    
                    vaga = Vaga.objects.create(**vaga_params)
                    vaga.coordenadores.add(coordenador)
                    
                    self.stdout.write(f"  ✅ Vaga '{vaga_data['nome']}' criada")
            except Disciplina.DoesNotExist:
                self.stdout.write(f"  ⚠️  Disciplina {vaga_data['disciplina_codigo']} não encontrada")

    def criar_turmas(self):
        """Cria turmas de monitoria"""
        self.stdout.write("\n🏫 Criando turmas...")
        
        vagas = list(Vaga.objects.all())
        salas = list(Sala.objects.all())
        
        # Usar o monitor de teste
        try:
            monitor = Aluno.objects.get(email='monitor.teste@faculdade.edu.br')
        except Aluno.DoesNotExist:
            self.stdout.write("  ⚠️  Monitor de teste não encontrado")
            return
        
        if not vagas or not salas:
            self.stdout.write("  ⚠️  Vagas ou salas não disponíveis")
            return
        
        for i, vaga in enumerate(vagas[:3]):
            if not Turma.objects.filter(vaga=vaga).exists():
                Turma.objects.create(
                    nome=f'Turma {vaga.disciplina.nome} - 2024.2',
                    vaga=vaga,
                    monitor=monitor,
                    sala=salas[i % len(salas)],
                    curso=vaga.curso,
                    descricao=f'Monitoria de {vaga.disciplina.nome}',
                    data_inicio=date.today() - timedelta(days=30),
                    data_fim=date.today() + timedelta(days=90),
                    dias_da_semana='Segunda e Quarta',
                    horario='14:00 - 16:00'
                )
                self.stdout.write(f"  ✅ Turma de '{vaga.disciplina.nome}' criada")

    def criar_inscricoes(self):
        """Cria inscrições em vagas"""
        self.stdout.write("\n📝 Criando inscrições...")
        
        vagas = list(Vaga.objects.all())
        alunos = list(Aluno.objects.exclude(email='monitor.teste@faculdade.edu.br'))
        
        if not vagas or not alunos:
            self.stdout.write("  ⚠️  Vagas ou alunos não disponíveis")
            return
        
        status_opcoes = ['Pendente', 'Aprovado', 'Não Aprovado', 'Entrevista']
        
        for vaga in vagas:
            # 2-3 inscrições por vaga
            num_inscricoes = random.randint(2, min(3, len(alunos)))
            alunos_selecionados = random.sample(alunos, num_inscricoes)
            
            for aluno in alunos_selecionados:
                if not Inscricao.objects.filter(vaga=vaga, aluno=aluno).exists():
                    Inscricao.objects.create(
                        vaga=vaga,
                        aluno=aluno,
                        status=random.choice(status_opcoes),
                        data_inscricao=date.today() - timedelta(days=random.randint(5, 30))
                    )
        
        total = Inscricao.objects.count()
        self.stdout.write(f"  ✅ {total} inscrições criadas")

    def criar_participacoes(self):
        """Cria participações em monitorias"""
        self.stdout.write("\n👥 Criando participações em monitorias...")
        
        turmas = list(Turma.objects.all())
        alunos = list(Aluno.objects.exclude(email='monitor.teste@faculdade.edu.br'))
        
        if not turmas or not alunos:
            self.stdout.write("  ⚠️  Turmas ou alunos não disponíveis")
            return
        
        for turma in turmas:
            # 3-5 alunos por turma
            num_participantes = random.randint(3, min(5, len(alunos)))
            alunos_selecionados = random.sample(alunos, num_participantes)
            
            for aluno in alunos_selecionados:
                if not ParticipacaoMonitoria.objects.filter(turma=turma, aluno=aluno).exists():
                    ParticipacaoMonitoria.objects.create(
                        turma=turma,
                        aluno=aluno,
                        ap1=Decimal(str(random.uniform(6.0, 10.0))),
                        ap2=Decimal(str(random.uniform(6.0, 10.0))),
                        cr=Decimal(str(random.uniform(7.0, 10.0)))
                    )
        
        total = ParticipacaoMonitoria.objects.count()
        self.stdout.write(f"  ✅ {total} participações criadas")

    def criar_presencas(self):
        """Cria registros de presença"""
        self.stdout.write("\n✅ Criando presenças...")
        
        participacoes = list(ParticipacaoMonitoria.objects.all())
        
        if not participacoes:
            self.stdout.write("  ⚠️  Nenhuma participação disponível")
            return
        
        # Últimos 14 dias
        for i in range(14):
            data_presenca = date.today() - timedelta(days=i)
            
            for participacao in participacoes:
                # 80% de chance de presença
                if random.random() < 0.8:
                    if not Presenca.objects.filter(
                        turma=participacao.turma,
                        aluno=participacao.aluno,
                        data=data_presenca
                    ).exists():
                        Presenca.objects.create(
                            turma=participacao.turma,
                            aluno=participacao.aluno,
                            data=data_presenca,
                            presente=random.choice([True, True, True, False])  # 75% presente
                        )
        
        total = Presenca.objects.count()
        self.stdout.write(f"  ✅ {total} presenças registradas")

    def criar_registros_horas(self):
        """Cria registros de horas de monitoria"""
        self.stdout.write("\n⏰ Criando registros de horas...")
        
        turmas = list(Turma.objects.all())
        
        if not turmas:
            self.stdout.write("  ⚠️  Nenhuma turma disponível")
            return
        
        status_opcoes = ['Pendente', 'Aprovado', 'Rejeitado']
        
        # Últimos 30 dias
        for i in range(30):
            data_registro = date.today() - timedelta(days=i)
            
            for turma in turmas:
                # 50% de chance de ter registro nesse dia
                if random.random() < 0.5:
                    hora_inicio = time(14, 0)
                    hora_fim = time(16, 0)
                    
                    if not RegistroHoras.objects.filter(
                        turma=turma,
                        monitor=turma.monitor,
                        data=data_registro
                    ).exists():
                        RegistroHoras.objects.create(
                            turma=turma,
                            monitor=turma.monitor,
                            data=data_registro,
                            hora_inicio=hora_inicio,
                            hora_fim=hora_fim,
                            descricao_atividade=f'Monitoria de {turma.vaga.disciplina}',
                            status=random.choice(status_opcoes)
                        )
        
        total = RegistroHoras.objects.count()
        self.stdout.write(f"  ✅ {total} registros de horas criados")

    def criar_pagamentos(self):
        """Cria registros de pagamentos"""
        self.stdout.write("\n💰 Criando pagamentos...")
        
        turmas = list(Turma.objects.all())
        
        if not turmas:
            self.stdout.write("  ⚠️  Nenhuma turma disponível")
            return
        
        # Últimos 3 meses
        for mes_offset in range(3):
            mes_ref = date.today() - timedelta(days=30 * mes_offset)
            
            for turma in turmas:
                if not StatusPagamento.objects.filter(
                    turma=turma,
                    monitor=turma.monitor,
                    mes_referencia=mes_ref
                ).exists():
                    StatusPagamento.objects.create(
                        turma=turma,
                        monitor=turma.monitor,
                        mes_referencia=mes_ref,
                        status=random.choice(['Pendente', 'Processando', 'Pago'])
                    )
        
        total = StatusPagamento.objects.count()
        self.stdout.write(f"  ✅ {total} pagamentos criados")
