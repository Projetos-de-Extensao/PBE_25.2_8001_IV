from django.db.models import Count, Sum, Avg, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import ( 
    Documento,
    RegistroHoras,
    StatusPagamento,
    Usuario,
    Funcionario, 
    Aluno, 
    Vaga, 
    Turma, 
    Inscricao, 
    Curso, 
    TipoUsuario, 
    Sala, 
    ParticipacaoMonitoria, 
    Presenca,
    Disciplina

    )

from django.db.models.functions import TruncMonth
from django.contrib.auth import authenticate


class AuthRepository:
    @staticmethod
    def autenticar(request, username, password):
        return authenticate(request, username=username, password=password)

    @staticmethod
    def logout_usuario(request):
        from django.contrib.auth import logout
        logout(request)

class RegistroRepository:
    @staticmethod
    def email_existe(email):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return User.objects.filter(email=email).exists()

    @staticmethod
    def matricula_existe(matricula):
        return Aluno.objects.filter(matricula=matricula).exists()

    @staticmethod
    def get_curso(curso_id):
        return Curso.objects.get(id=curso_id)

    @staticmethod
    def get_cursos_ativos():
        return Curso.objects.filter(ativo=True)

    @staticmethod
    def get_tipo_usuario_aluno():
        return TipoUsuario.objects.get_or_create(tipo='aluno', defaults={'ativo': True})[0]

    @staticmethod
    def get_grupo_aluno():
        from django.contrib.auth.models import Group
        return Group.objects.get_or_create(name='Aluno')[0]

    @staticmethod
    def username_existe(username):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return User.objects.filter(username=username).exists()

    @staticmethod
    def criar_usuario(username, email, password, nome):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        first_name = nome.split()[0] if nome else ''
        last_name = ' '.join(nome.split()[1:]) if len(nome.split()) > 1 else ''
        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

    @staticmethod
    def adicionar_grupo(user, grupo):
        user.groups.add(grupo)
        user.save()

    @staticmethod
    def criar_aluno(nome, email, tipo_usuario, matricula, curso, periodo, cr_geral):
        from datetime import datetime
        return Aluno.objects.create(
            nome=nome,
            email=email,
            tipo_usuario=tipo_usuario,
            matricula=matricula,
            curso=curso,
            data_ingresso=datetime.now().date(),
            periodo=periodo,
            cr_geral=cr_geral,
            ativo=True
        )


class VagaRepository:
    @staticmethod
    def get_vaga_by_id(vaga_id):
        return Vaga.objects.get(id=vaga_id)

    @staticmethod
    def get_funcionario_by_email(email):
        return Funcionario.objects.get(email=email)

    @staticmethod
    def get_inscricoes_by_vaga(vaga):
        return Inscricao.objects.filter(vaga=vaga).select_related('aluno', 'aluno__curso').order_by('-data_inscricao')

    @staticmethod
    def get_coordenadores(vaga):
        return vaga.coordenadores.all()

    @staticmethod
    def get_professores(vaga):
        return vaga.professores.all()

class UsuarioRepository:
    @staticmethod
    def list_users(tipo_id=None, ativo=None):
        qs = Usuario.objects.all().select_related('tipo_usuario')
        if tipo_id:
            qs = qs.filter(tipo_usuario__id=tipo_id)
        if ativo is not None:
            qs = qs.filter(ativo=ativo)
        return qs

    @staticmethod
    def get_tipo_usuario_by_id(tipo_usuario_id):
        return TipoUsuario.objects.get(id=tipo_usuario_id)

    @staticmethod
    def get_usuario_by_id(usuario_id):
        return Usuario.objects.get(id=usuario_id)

    @staticmethod
    def get_usuario_by_email(email):
        return Usuario.objects.get(email=email)

class AlunoRepository:
    @staticmethod
    def list_alunos(curso_id=None, periodo=None):
        qs = Aluno.objects.all().select_related('curso', 'tipo_usuario')
        if curso_id:
            qs = qs.filter(curso__id=curso_id)
        if periodo:
            try:
                periodo_int = int(periodo)
                qs = qs.filter(periodo=periodo_int)
            except (ValueError, TypeError):
                pass
        return qs

    @staticmethod
    def get_aluno_by_id(aluno_id):
        return Aluno.objects.get(id=aluno_id)

    @staticmethod
    def get_curso_by_id(curso_id):
        return Curso.objects.get(id=curso_id)

    @staticmethod
    def get_or_create_tipo_usuario_aluno():
        return TipoUsuario.objects.get_or_create(tipo='aluno', defaults={'ativo': True})

    @staticmethod
    def create_aluno(**kwargs):
        return Aluno.objects.create(**kwargs)


class TurmaRepository:
    @staticmethod
    def list_turmas(vaga_id=None, status=None):
        qs = Turma.objects.all().select_related('vaga', 'monitor', 'sala', 'curso')
        if vaga_id:
            qs = qs.filter(vaga__id=vaga_id)
        if status is not None:
            qs = qs.filter(ativo=(status == 'ativa'))
        return qs

    @staticmethod
    def get_turma_by_id(turma_id):
        return Turma.objects.get(id=turma_id)

    @staticmethod
    def get_participacoes_by_turma(turma):
        return ParticipacaoMonitoria.objects.filter(turma=turma).select_related('aluno')

    @staticmethod
    def get_presencas_by_turma(turma):
        return Presenca.objects.filter(turma=turma).select_related('aluno')

    @staticmethod
    def get_vaga_by_id(vaga_id):
        return Vaga.objects.get(id=vaga_id)

    @staticmethod
    def get_sala_by_id(sala_id):
        return Sala.objects.get(id=sala_id)

    @staticmethod
    def get_monitor_by_id(monitor_id):
        return Aluno.objects.get(id=monitor_id)

    @staticmethod
    def get_curso_by_id(curso_id):
        return Curso.objects.get(id=curso_id)

    @staticmethod
    def create_turma(**kwargs):
        return Turma.objects.create(**kwargs)
    

class MonitoriaRepository:
    @staticmethod
    def get_professor_by_email(email):
        return Funcionario.objects.get(email=email)

    @staticmethod
    def get_turmas_by_professor(professor):
        return Turma.objects.filter(
            vaga__professores=professor,
            ativo=True
        ).select_related('vaga', 'monitor', 'curso', 'sala').order_by('-criado_em')

    @staticmethod
    def get_participacoes_by_turmas(turmas):
        return ParticipacaoMonitoria.objects.filter(
            turma__in=turmas
        ).select_related('aluno', 'turma')

    @staticmethod
    def get_participacao_by_id(participacao_id):
        return ParticipacaoMonitoria.objects.get(id=participacao_id)
    
class PresencaRepository:
    @staticmethod
    def list_presencas(turma_id=None, data=None):
        presencas = Presenca.objects.all().select_related('aluno', 'turma')
        if turma_id:
            presencas = presencas.filter(turma__id=turma_id)
        if data:
            presencas = presencas.filter(data=data)
        return presencas

    @staticmethod
    def get_turmas_ativas():
        return Turma.objects.filter(ativo=True)

    @staticmethod
    def get_presenca_by_id(presenca_id):
        return Presenca.objects.get(id=presenca_id)
    

class RelatorioRepository:
    @staticmethod
    def get_participacoes():
        return ParticipacaoMonitoria.objects.all().select_related('aluno', 'turma')

    @staticmethod
    def get_presencas():
        return Presenca.objects.all().select_related('aluno', 'turma')

    @staticmethod
    def get_inscricoes():
        return Inscricao.objects.all().select_related('aluno', 'vaga')

    @staticmethod
    def get_total_usuarios():
        return Usuario.objects.filter(ativo=True).count()

    @staticmethod
    def get_total_alunos():
        return Aluno.objects.filter(ativo=True).count()

    @staticmethod
    def get_total_funcionarios():
        return Funcionario.objects.filter(ativo=True).count()

    @staticmethod
    def get_total_turmas():
        return Turma.objects.filter(ativo=True).count()

    @staticmethod
    def get_total_vagas():
        return Vaga.objects.filter(ativo=True).count()

    @staticmethod
    def get_total_inscricoes():
        return Inscricao.objects.count()

    @staticmethod
    def get_total_presencas():
        return Presenca.objects.filter(presente=True).count()
    

class PerfilRepository:
    @staticmethod
    def get_aluno_by_email(email):
        try:
            return Aluno.objects.get(email=email)
        except Aluno.DoesNotExist:
            return None

    @staticmethod
    def get_professor_by_email(email):
        try:
            return Funcionario.objects.get(email=email)
        except Funcionario.DoesNotExist:
            return None
        
class VagaRepository:
    @staticmethod
    def get_all_vagas():
        return Vaga.objects.all().select_related('curso', 'disciplina').prefetch_related('coordenadores', 'professores', 'monitores').annotate(
            total_inscritos=Count('inscricao')
        )

    @staticmethod
    def get_vagas_by_coordenador(funcionario):
        return Vaga.objects.filter(coordenadores=funcionario).select_related('curso', 'disciplina').prefetch_related('coordenadores', 'professores', 'monitores').annotate(
            total_inscritos=Count('inscricao')
        )

    @staticmethod
    def get_vaga_by_id(vaga_id):
        return Vaga.objects.get(id=vaga_id)

    @staticmethod
    def get_inscricoes_by_vaga(vaga):
        return Inscricao.objects.filter(vaga=vaga).select_related('aluno', 'aluno__curso').order_by('-data_inscricao')

    @staticmethod
    def get_tipo_usuario_by_id(tipo_usuario_id):
        return TipoUsuario.objects.get(id=tipo_usuario_id)

    @staticmethod
    def get_curso_by_id(curso_id):
        return Curso.objects.get(id=curso_id)

    @staticmethod
    def get_disciplina_by_id(disciplina_id):
        return Disciplina.objects.get(id=disciplina_id)

    @staticmethod
    def get_funcionario_by_id(funcionario_id):
        return Funcionario.objects.get(id=funcionario_id)

    @staticmethod
    def create_vaga(**kwargs):
        vaga = Vaga.objects.create(**kwargs)
        return vaga

    @staticmethod
    def delete_vaga(vaga):
        vaga.delete()


class TurmaRepository:
    @staticmethod
    def get_all_turmas():
        return Turma.objects.all().select_related('vaga', 'monitor', 'sala', 'curso')

    @staticmethod
    def get_turma_by_id(turma_id):
        return Turma.objects.get(id=turma_id)

    @staticmethod
    def get_participacoes_by_turma(turma):
        return ParticipacaoMonitoria.objects.filter(turma=turma).select_related('aluno')

    @staticmethod
    def get_presencas_by_turma(turma):
        return Presenca.objects.filter(turma=turma).select_related('aluno')

    @staticmethod
    def create_turma(**kwargs):
        return Turma.objects.create(**kwargs)

    @staticmethod
    def delete_turma(turma):
        turma.delete()

class RelatorioRepository:
    @staticmethod
    def get_participacoes():
        return ParticipacaoMonitoria.objects.all().select_related('aluno', 'turma')

    @staticmethod
    def get_presencas():
        return Presenca.objects.all().select_related('aluno', 'turma')

    @staticmethod
    def get_inscricoes():
        return Inscricao.objects.all().select_related('aluno', 'vaga')

    @staticmethod
    def get_total_usuarios():
        return Usuario.objects.filter(ativo=True).count()

    @staticmethod
    def get_total_alunos():
        return Aluno.objects.filter(ativo=True).count()

    @staticmethod
    def get_total_funcionarios():
        return Funcionario.objects.filter(ativo=True).count()

    @staticmethod
    def get_total_turmas():
        return Turma.objects.filter(ativo=True).count()

    @staticmethod
    def get_total_vagas():
        return Vaga.objects.filter(ativo=True).count()

    @staticmethod
    def get_total_inscricoes():
        return Inscricao.objects.count()

    @staticmethod
    def get_total_presencas():
        return Presenca.objects.filter(presente=True).count()
    

class PortalVagasRepository:
    @staticmethod
    def vagas_ativas():
        return Vaga.objects.filter(ativo=True).select_related('curso', 'disciplina').prefetch_related('coordenadores', 'professores').annotate(total_inscritos=Count('inscricao'))

    @staticmethod
    def filtrar_vagas(vagas, busca=None, curso=None, tipo=None):
        if busca:
            vagas = vagas.filter(
                Q(disciplina__nome__icontains=busca) |
                Q(disciplina__codigo__icontains=busca) |
                Q(nome__icontains=busca) |
                Q(descricao__icontains=busca)
            )
        if curso:
            vagas = vagas.filter(curso__id=curso)
        if tipo:
            vagas = vagas.filter(tipo_vaga=tipo)
        return vagas

    @staticmethod
    def total_vagas():
        return Vaga.objects.filter(ativo=True).count()

    @staticmethod
    def total_cursos():
        return Vaga.objects.filter(ativo=True).values('curso').distinct().count()

    @staticmethod
    def total_disciplinas():
        return Vaga.objects.filter(ativo=True).values('disciplina').distinct().count()

    @staticmethod
    def cursos_ativos():
        return Curso.objects.filter(ativo=True).order_by('nome')

    @staticmethod
    def get_vaga(vaga_id):
        return Vaga.objects.get(id=vaga_id, ativo=True)

    @staticmethod
    def get_aluno_by_email(email):
        try:
            return Aluno.objects.get(email=email)
        except Aluno.MultipleObjectsReturned:
            return Aluno.objects.filter(email=email).first()
        except Aluno.DoesNotExist:
            return None

    @staticmethod
    def inscricao_exists(aluno, vaga):
        return Inscricao.objects.filter(aluno=aluno, vaga=vaga).exists()

    @staticmethod
    def vagas_disponiveis(vaga):
        return vaga.vagas_disponiveis()

    @staticmethod
    def criar_inscricao(aluno, vaga):
        return Inscricao.objects.create(aluno=aluno, vaga=vaga, status='Pendente')

    @staticmethod
    def criar_documento(inscricao, tipo, arquivo, nome_arquivo):
        return Documento.objects.create(inscricao=inscricao, tipo=tipo, arquivo=arquivo, nome_arquivo=nome_arquivo)
    

class RegistroHorasRepository:
    @staticmethod
    def get_turmas_do_monitor(monitor):
        return Turma.objects.filter(monitor=monitor, ativo=True)

    @staticmethod
    def criar_registro(turma, monitor, data, hora_inicio, hora_fim, descricao_atividade):
        return RegistroHoras.objects.create(
            turma=turma,
            monitor=monitor,
            data=data,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim,
            descricao_atividade=descricao_atividade,
            status='Pendente'
        )

    @staticmethod
    def get_registros_do_monitor(monitor):
        return RegistroHoras.objects.filter(monitor=monitor).select_related('turma', 'validado_por').order_by('-data')

    @staticmethod
    def get_registro_by_id_monitor(registro_id, monitor):
        return RegistroHoras.objects.get(id=registro_id, monitor=monitor)

    @staticmethod
    def get_funcionario_by_email(email):
        return Funcionario.objects.get(email=email)

    @staticmethod
    def get_registros_pendentes():
        return RegistroHoras.objects.filter(status='Pendente').select_related('monitor', 'turma')

    @staticmethod
    def get_registro_by_id(registro_id):
        return RegistroHoras.objects.get(id=registro_id)
    
    @staticmethod
    def get_monitor_by_email(email):
        return Aluno.objects.get(email=email)


    
class DashboardGestaoRepository:
    @staticmethod
    def total_monitores():
        return Aluno.objects.filter(monitorias__ativo=True).distinct().count()

    @staticmethod
    def total_alunos():
        return Aluno.objects.filter(ativo=True).count()

    @staticmethod
    def total_professores():
        from django.contrib.auth.models import Group
        try:
            grupo_professor = Group.objects.get(name='Professor')
            return grupo_professor.user_set.count()
        except:
            return 0

    @staticmethod
    def total_vagas():
        return Vaga.objects.filter(ativo=True).count()

    @staticmethod
    def total_turmas():
        return Turma.objects.filter(ativo=True).count()

    @staticmethod
    def total_inscricoes():
        return Inscricao.objects.all().count()

    @staticmethod
    def total_horas_mes():
        now = timezone.now()
        return RegistroHoras.objects.filter(
            status='Aprovado',
            data__month=now.month,
            data__year=now.year
        ).aggregate(total=Sum('total_horas'))['total'] or 0

    @staticmethod
    def valor_total_mes():
        now = timezone.now()
        return StatusPagamento.objects.filter(
            status='Pago',
            mes_referencia__month=now.month,
            mes_referencia__year=now.year
        ).aggregate(total=Sum('valor_total'))['total'] or 0

    @staticmethod
    def inscricoes_por_status():
        return list(Inscricao.objects.values('status').annotate(total=Count('id')).order_by('-total'))

    @staticmethod
    def taxa_aprovacao():
        total_avaliadas = Inscricao.objects.exclude(status='Pendente').count()
        total_aprovados = Inscricao.objects.filter(status='Aprovado').count()
        return round((total_aprovados / total_avaliadas * 100), 1) if total_avaliadas > 0 else 0

    @staticmethod
    def monitores_por_curso():
        return list(Inscricao.objects.filter(status='Aprovado').values('aluno__curso__nome').annotate(total=Count('id', distinct=True)).order_by('-total')[:10])

    @staticmethod
    def inscricoes_timeline(seis_meses_atras):
        return list(Inscricao.objects.filter(
            data_inscricao__gte=seis_meses_atras
        ).annotate(
            mes=TruncMonth('data_inscricao')
        ).values('mes').annotate(
            total=Count('id')
        ).order_by('mes'))

    @staticmethod
    def horas_timeline(seis_meses_atras):
        return list(RegistroHoras.objects.filter(
            status='Aprovado',
            data__gte=seis_meses_atras
        ).annotate(
            mes=TruncMonth('data')
        ).values('mes').annotate(
            total_horas=Sum('total_horas')
        ).order_by('mes'))

    @staticmethod
    def pagamentos_timeline(seis_meses_atras):
        return list(StatusPagamento.objects.filter(
            mes_referencia__gte=seis_meses_atras
        ).annotate(
            mes=TruncMonth('mes_referencia')
        ).values('mes').annotate(
            total_valor=Sum('valor_total')
        ).order_by('mes'))

    @staticmethod
    def horas_por_status():
        return list(RegistroHoras.objects.values('status').annotate(
            total=Count('id'),
            horas=Sum('total_horas')
        ).order_by('-total'))

    @staticmethod
    def pagamentos_pendentes():
        return StatusPagamento.objects.filter(status='Pendente').count()

    @staticmethod
    def avaliacoes_pendentes():
        return Inscricao.objects.filter(status='Pendente').count()

    @staticmethod
    def horas_pendentes():
        return RegistroHoras.objects.filter(status='Pendente').count()

    @staticmethod
    def documentos_pendentes():
        return Documento.objects.filter(inscricao__status='Pendente').count()

    @staticmethod
    def vagas_ativas():
        return Vaga.objects.filter(ativo=True).annotate(
            total_inscritos=Count('inscricao'),
            aprovados=Count('inscricao', filter=Q(inscricao__status='Aprovado'))
        ).select_related('curso', 'disciplina').prefetch_related('coordenadores').order_by('-criado_em')[:10]

    @staticmethod
    def cr_medio_monitores():
        return Inscricao.objects.filter(status='Aprovado').aggregate(media=Avg('aluno__cr_geral'))['media'] or 0

    @staticmethod
    def media_horas_monitor():
        return RegistroHoras.objects.filter(status='Aprovado').aggregate(media=Avg('total_horas'))['media'] or 0
    @staticmethod
    def total_pago_ano():
        ano_atual = timezone.now().year
        return StatusPagamento.objects.filter(
            status='Pago',
            mes_referencia__year=ano_atual
        ).aggregate(total=Sum('valor_total'))['total'] or 0

    @staticmethod
    def dados_exportacao():
        return {
            'monitores': Inscricao.objects.filter(status='Aprovado').select_related('aluno', 'vaga').values(
                'aluno__nome', 'aluno__matricula', 'aluno__curso__nome', 
                'vaga__disciplina', 'aluno__cr_geral'
            ),
            'horas': RegistroHoras.objects.filter(status='Aprovado').select_related('monitor').values(
                'monitor__nome', 'data', 'total_horas', 'descricao_atividade'
            ),
            'vagas': Vaga.objects.filter(ativo=True).select_related('curso', 'disciplina').prefetch_related('coordenadores').values(
                'disciplina__nome', 'curso__nome', 'numero_vagas'
            ),
        }
    

class DisciplinaRepository:
    @staticmethod
    def listar_disciplinas(ativo=True, curso_id=None, periodo=None, busca=None):
        qs = Disciplina.objects.select_related('curso', 'criado_por').filter(ativo=ativo)
        if curso_id:
            qs = qs.filter(curso_id=curso_id)
        if periodo:
            qs = qs.filter(periodo_sugerido=periodo)
        if busca:
            from django.db.models import Q
            qs = qs.filter(
                Q(nome__icontains=busca) |
                Q(codigo__icontains=busca) |
                Q(ementa__icontains=busca)
            )
        return qs.order_by('curso__nome', 'periodo_sugerido', 'nome')

    @staticmethod
    def get_cursos_ativos():
        return Curso.objects.filter(ativo=True).order_by('nome')

    @staticmethod
    def get_disciplina_by_id(disciplina_id):
        return Disciplina.objects.get(id=disciplina_id, ativo=True)

    @staticmethod
    def get_funcionario_by_email(email):
        try:
            return Funcionario.objects.get(email=email)
        except Funcionario.DoesNotExist:
            return None
        

class PagamentoRepository:
    """Acesso a dados para StatusPagamento."""

    def listar_pagamentos(self, status=None):
        qs = StatusPagamento.objects.all().select_related('monitor', 'turma').order_by('-mes_referencia')
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_pagamento(self, pagamento_id):
        return get_object_or_404(StatusPagamento, id=pagamento_id)

    def salvar(self, pagamento):
        pagamento.save()
        return pagamento

    def get_funcionario_por_email(self, email):
        try:
            return Funcionario.objects.get(email=email)
        except Funcionario.DoesNotExist:
            return None