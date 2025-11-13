from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from django.db import IntegrityError, transaction

from .repository_2 import (
    AlunoRepository,
    MonitoriaRepository,
    PerfilRepository,
    PresencaRepository,
    RelatorioRepository,
    TurmaRepository,
    UsuarioRepository,
    VagaRepository

)

from .models import (
    Curso,
    ParticipacaoMonitoria, 
    Presenca, 
    Inscricao,
    Sala,
    TipoUsuario, 
    Usuario, 
    Aluno, 
    Funcionario, 
    Turma, 
    Vaga
)

class BaseService:
    @staticmethod
    def safe_count(qs):
        try:
            return qs.count()
        except Exception:
            return 0

class VagaService(BaseService):
    def __init__(self, vaga_id, user):
        self.vaga = VagaRepository.get_vaga_by_id(vaga_id)
        self.user = user

    def check_permission(self):
        if self.user.is_staff or self.user.is_superuser:
            return True

        try:
            funcionario = VagaRepository.get_funcionario_by_email(self.user.email)
        except Funcionario.DoesNotExist:
            raise PermissionDenied("Professor não encontrado")

        if funcionario in VagaRepository.get_coordenadores(self.vaga) or funcionario in VagaRepository.get_professores(self.vaga):
            return True

        raise PermissionDenied("Você não tem permissão para ver esta vaga")

    def get_inscricoes_qs(self):
        return VagaRepository.get_inscricoes_by_vaga(self.vaga)

    def get_stats(self):
        qs = self.get_inscricoes_qs()
        return {
            'total_inscricoes': self.safe_count(qs),
            'pendentes': qs.filter(status='Pendente').count(),
            'entrevista': qs.filter(status='Entrevista').count(),
            'aprovados': qs.filter(status='Aprovado').count(),
            'rejeitados': qs.filter(status='Não Aprovado').count(),
        }

    def vaga_service(self):
        self.check_permission()
        inscricoes = self.get_inscricoes_qs()
        stats = self.get_stats()
        context = {
            'vaga': self.vaga,
            'inscricoes': inscricoes,
            **stats
        }
        return context


class UsuarioService:
    """Service para operações CRUD simples sobre Usuario."""

    def list_users(self, tipo_id=None, ativo=None):
        return UsuarioRepository.list_users(tipo_id, ativo)

    def create_user(self, nome, email, tipo_usuario_id):
        tipo = UsuarioRepository.get_tipo_usuario_by_id(tipo_usuario_id)
        try:
            usuario = UsuarioRepository.create_usuario(nome, email, tipo)
            return usuario
        except IntegrityError as e:
            raise

    def update_user(self, usuario_id, nome=None, email=None, ativo=None):
        usuario = UsuarioRepository.get_usuario_by_id(usuario_id)
        if nome is not None:
            usuario.nome = nome
        if email is not None:
            usuario.email = email
        if ativo is not None:
            usuario.ativo = ativo
        usuario.save()
        return usuario

    def delete_user(self, usuario_id):
        usuario = UsuarioRepository.get_usuario_by_id(usuario_id)
        nome = usuario.nome
        usuario.delete()
        return nome
    


class AlunoService:
    """Service para operações CRUD de Aluno."""

    def list_alunos(self, curso_id=None, periodo=None):
        return AlunoRepository.list_alunos(curso_id, periodo)

    def create_aluno(self, nome, email, matricula, curso_id, periodo=None, cr_geral=0.0):
        curso = AlunoRepository.get_curso_by_id(curso_id)
        tipo_usuario, _ = AlunoRepository.get_or_create_tipo_usuario_aluno()

        try:
            periodo_val = int(periodo) if periodo is not None and periodo != '' else None
        except (ValueError, TypeError):
            periodo_val = None

        try:
            cr_val = float(cr_geral) if cr_geral not in (None, '') else 0.0
        except (ValueError, TypeError):
            cr_val = 0.0

        try:
            with transaction.atomic():
                aluno = AlunoRepository.create_aluno(
                    nome=nome,
                    email=email,
                    matricula=matricula,
                    curso=curso,
                    periodo=periodo_val,
                    cr_geral=cr_val,
                    tipo_usuario=tipo_usuario,
                    data_ingresso=timezone.now().date(),
                    ativo=True
                )
            return aluno
        except IntegrityError as e:
            raise

    def update_aluno(self, aluno_id, nome=None, email=None, periodo=None, cr_geral=None, ativo=None):
        aluno = AlunoRepository.get_aluno_by_id(aluno_id)
        if nome is not None:
            aluno.nome = nome
        if email is not None:
            aluno.email = email
        if periodo is not None and periodo != '':
            try:
                aluno.periodo = int(periodo)
            except (ValueError, TypeError):
                pass
        if cr_geral is not None and cr_geral != '':
            try:
                aluno.cr_geral = float(cr_geral)
            except (ValueError, TypeError):
                pass
        if ativo is not None:
            aluno.ativo = bool(ativo)
        aluno.save()
        return aluno

    def delete_aluno(self, aluno_id):
        aluno = AlunoRepository.get_aluno_by_id(aluno_id)
        nome = aluno.nome
        aluno.delete()
        return nome
    

class TurmaService:
    """Service para operações CRUD de Turma."""

    def list_turmas(self, vaga_id=None, status=None):
        return TurmaRepository.list_turmas(vaga_id, status)

    def get_turma_detail(self, turma_id):
        turma = TurmaRepository.get_turma_by_id(turma_id)
        participacoes = TurmaRepository.get_participacoes_by_turma(turma)
        presencas = TurmaRepository.get_presencas_by_turma(turma)
        return {
            'turma': turma,
            'participacoes': participacoes,
            'presencas': presencas,
        }

    def create_turma(self, nome, vaga_id, sala_id, descricao, data_inicio, data_fim, dias_semana, horario, monitor_id, curso_id):
        try:
            with transaction.atomic():
                vaga = TurmaRepository.get_vaga_by_id(vaga_id)
                sala = TurmaRepository.get_sala_by_id(sala_id)
                monitor = TurmaRepository.get_monitor_by_id(monitor_id)
                curso = TurmaRepository.get_curso_by_id(curso_id)
                turma = TurmaRepository.create_turma(
                    nome=nome,
                    vaga=vaga,
                    sala=sala,
                    descricao=descricao,
                    data_inicio=data_inicio,
                    data_fim=data_fim,
                    dias_da_semana=dias_semana,
                    horario=horario,
                    monitor=monitor,
                    curso=curso,
                    ativo=True
                )
            return turma
        except Exception as e:
            raise

    def update_turma(self, turma_id, nome=None, descricao=None, horario=None, ativo=None):
        turma = TurmaRepository.get_turma_by_id(turma_id)
        if nome is not None:
            turma.nome = nome
        if descricao is not None:
            turma.descricao = descricao
        if horario is not None:
            turma.horario = horario
        if ativo is not None:
            turma.ativo = ativo
        turma.save()
        return turma

    def delete_turma(self, turma_id):
        turma = TurmaRepository.get_turma_by_id(turma_id)
        turma.delete()
        return True
    

class MonitoriaService:
    """Service para operações de monitorias do professor."""

    def listar_monitorias(self, user, turma_id=None):
        try:
            professor = MonitoriaRepository.get_professor_by_email(user.email)
            turmas = MonitoriaRepository.get_turmas_by_professor(professor)
            participacoes = MonitoriaRepository.get_participacoes_by_turmas(turmas)
            if turma_id:
                participacoes = participacoes.filter(turma__id=turma_id)
                turmas = turmas.filter(id=turma_id)
        except Funcionario.DoesNotExist:
            turmas = Turma.objects.none()
            participacoes = ParticipacaoMonitoria.objects.none()
        return {
            'participacoes': participacoes,
            'turmas': turmas,
        }

    def editar_participacao(self, participacao_id, ap1=None, ap2=None, cr=None):
        participacao = MonitoriaRepository.get_participacao_by_id(participacao_id)
        participacao.ap1 = ap1 if ap1 != '' else None
        participacao.ap2 = ap2 if ap2 != '' else None
        participacao.cr = cr if cr != '' else None
        participacao.save()
        return participacao

class PresencaService:
    """Service para operações de presenças."""

    def listar_presencas(self, turma_id=None, data=None):
        presencas = PresencaRepository.list_presencas(turma_id, data)
        turmas = PresencaRepository.get_turmas_ativas()
        return {
            'presencas': presencas,
            'turmas': turmas,
        }

    def editar_presenca(self, presenca_id, presente):
        presenca = PresencaRepository.get_presenca_by_id(presenca_id)
        presenca.presente = presente
        presenca.save()

class RelatorioService:
    """Service para relatórios do sistema."""

    def desempenho(self):
        participacoes = RelatorioRepository.get_participacoes()
        return {
            'participacoes': participacoes,
            'titulo': 'Relatório de Desempenho',
        }

    def frequencia(self):
        presencas = RelatorioRepository.get_presencas()
        return {
            'presencas': presencas,
            'titulo': 'Relatório de Frequência',
        }

    def inscricoes(self):
        inscricoes = RelatorioRepository.get_inscricoes()
        return {
            'inscricoes': inscricoes,
            'titulo': 'Relatório de Inscrições',
        }

    def geral(self):
        return {
            'total_usuarios': RelatorioRepository.get_total_usuarios(),
            'total_alunos': RelatorioRepository.get_total_alunos(),
            'total_funcionarios': RelatorioRepository.get_total_funcionarios(),
            'total_turmas': RelatorioRepository.get_total_turmas(),
            'total_vagas': RelatorioRepository.get_total_vagas(),
            'total_inscricoes': RelatorioRepository.get_total_inscricoes(),
            'total_presencas': RelatorioRepository.get_total_presencas(),
            'titulo': 'Relatório Geral',
        }

class PerfilService:
    """Service para operações de perfil do usuário."""

    def get_perfil_context(self, user):
        aluno = PerfilRepository.get_aluno_by_email(user.email)
        professor = PerfilRepository.get_professor_by_email(user.email)
        return {
            'usuario': user,
            'aluno': aluno,
            'professor': professor,
        }

    def atualizar_perfil(self, user, data):
        nome = data.get('nome')
        email = data.get('email')
        user.first_name = nome
        user.email = email
        user.save()
        aluno = PerfilRepository.get_aluno_by_email(user.email)
        if aluno:
            aluno.nome = nome
            aluno.email = email
            aluno.save()


class PortalVagasService:
    """Service para lógica do portal público de vagas."""

    def get_context(self, request):
        # Buscar todas as vagas ativas
        vagas = Vaga.objects.filter(ativo=True).select_related(
            'curso', 'disciplina'
        ).prefetch_related(
            'coordenadores', 'professores'
        ).annotate(
            total_inscritos=Count('inscricao')
        )

        # Filtros
        busca = request.GET.get('busca', '').strip()
        if busca:
            vagas = vagas.filter(
                Q(disciplina__nome__icontains=busca) |
                Q(disciplina__codigo__icontains=busca) |
                Q(nome__icontains=busca) |
                Q(descricao__icontains=busca)
            )

        curso_filtro = request.GET.get('curso')
        if curso_filtro:
            vagas = vagas.filter(curso__id=curso_filtro)

        tipo_filtro = request.GET.get('tipo')
        if tipo_filtro:
            vagas = vagas.filter(tipo_vaga=tipo_filtro)

        # Estatísticas
        total_vagas = Vaga.objects.filter(ativo=True).count()
        total_cursos = Vaga.objects.filter(ativo=True).values('curso').distinct().count()
        total_disciplinas = Vaga.objects.filter(ativo=True).values('disciplina').distinct().count()
        cursos = Curso.objects.filter(ativo=True).order_by('nome')

        context = {
            'vagas': vagas,
            'cursos': cursos,
            'total_vagas': total_vagas,
            'total_cursos': total_cursos,
            'total_disciplinas': total_disciplinas,
        }

        # Dados do aluno autenticado
        if request.user.is_authenticated:
            try:
                aluno = Aluno.objects.get(email=request.user.email)
                context['aluno'] = aluno
                perfil_incompleto = request.session.pop('perfil_incompleto', None)
                vaga_tentada = request.session.pop('vaga_tentada', None)
                if perfil_incompleto:
                    context['perfil_incompleto'] = perfil_incompleto
                if vaga_tentada:
                    context['vaga_tentada'] = vaga_tentada
            except Exception:
                context['aluno'] = None

        return context
