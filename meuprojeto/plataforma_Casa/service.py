from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from django.db import IntegrityError, transaction


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
        self.vaga = get_object_or_404(Vaga, id=vaga_id)
        self.user = user

    def check_permission(self):
        # admins sempre têm acesso
        if self.user.is_staff or self.user.is_superuser:
            return True

        try:
            funcionario = Funcionario.objects.get(email=self.user.email)
        except Funcionario.DoesNotExist:
            raise PermissionDenied("Professor não encontrado")

        if funcionario in self.vaga.coordenadores.all() or funcionario in self.vaga.professores.all():
            return True

        raise PermissionDenied("Você não tem permissão para ver esta vaga")

    def get_inscricoes_qs(self):
        return Inscricao.objects.filter(vaga=self.vaga).select_related('aluno', 'aluno__curso').order_by('-data_inscricao')

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
        # valida permissão (lança PermissionDenied se não tiver)
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
        qs = Usuario.objects.all().select_related('tipo_usuario')
        if tipo_id:
            qs = qs.filter(tipo_usuario__id=tipo_id)
        if ativo is not None:
            qs = qs.filter(ativo=ativo)
        return qs

    def create_user(self, nome, email, tipo_usuario_id):
        tipo = get_object_or_404(TipoUsuario, id=tipo_usuario_id)
        try:
            usuario = Usuario.objects.create(
                nome=nome,
                email=email,
                tipo_usuario=tipo,
                ativo=True
            )
            return usuario
        except IntegrityError as e:
            raise

    def update_user(self, usuario_id, nome=None, email=None, ativo=None):
        usuario = get_object_or_404(Usuario, id=usuario_id)
        if nome is not None:
            usuario.nome = nome
        if email is not None:
            usuario.email = email
        if ativo is not None:
            usuario.ativo = ativo
        usuario.save()
        return usuario

    def delete_user(self, usuario_id):
        usuario = get_object_or_404(Usuario, id=usuario_id)
        nome = usuario.nome
        usuario.delete()
        return nome
    

class AlunoService:
    """Service para operações CRUD de Aluno."""

    def list_alunos(self, curso_id=None, periodo=None):
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

    def create_aluno(self, nome, email, matricula, curso_id, periodo=None, cr_geral=0.0):
        # valida curso
        curso = get_object_or_404(Curso, id=curso_id)
        # obtém ou cria tipo_usuario 'aluno'
        tipo_usuario, _ = TipoUsuario.objects.get_or_create(tipo='aluno', defaults={'ativo': True})

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
                aluno = Aluno.objects.create(
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
        aluno = get_object_or_404(Aluno, id=aluno_id)
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
        aluno = get_object_or_404(Aluno, id=aluno_id)
        nome = aluno.nome
        aluno.delete()
        return nome
    

class TurmaService:
    """Service para operações CRUD de Turma."""

    def list_turmas(self, vaga_id=None, status=None):
        qs = Turma.objects.all().select_related('vaga', 'monitor', 'sala', 'curso')
        if vaga_id:
            qs = qs.filter(vaga__id=vaga_id)
        if status is not None:
            qs = qs.filter(ativo=(status == 'ativa'))
        return qs

    def get_turma_detail(self, turma_id):
        turma = get_object_or_404(Turma, id=turma_id)
        participacoes = ParticipacaoMonitoria.objects.filter(turma=turma).select_related('aluno')
        presencas = Presenca.objects.filter(turma=turma).select_related('aluno')
        return {
            'turma': turma,
            'participacoes': participacoes,
            'presencas': presencas,
        }

    def create_turma(self, nome, vaga_id, sala_id, descricao, data_inicio, data_fim, dias_semana, horario, monitor_id, curso_id):
        try:
            with transaction.atomic():
                vaga = Vaga.objects.get(id=vaga_id)
                sala = Sala.objects.get(id=sala_id)
                monitor = Aluno.objects.get(id=monitor_id)
                curso = Curso.objects.get(id=curso_id)
                turma = Turma.objects.create(
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
        turma = get_object_or_404(Turma, id=turma_id)
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
        turma = get_object_or_404(Turma, id=turma_id)
        turma.delete()
        return True
    

class MonitoriaService:
    """Service para operações de monitorias do professor."""

    def listar_monitorias(self, user, turma_id=None):
        try:
            professor = Funcionario.objects.get(email=user.email)
            turmas = Turma.objects.filter(
                vaga__professores=professor,
                ativo=True
            ).select_related('vaga', 'monitor', 'curso', 'sala').order_by('-criado_em')
            participacoes = ParticipacaoMonitoria.objects.filter(
                turma__in=turmas
            ).select_related('aluno', 'turma')
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
        participacao = get_object_or_404(ParticipacaoMonitoria, id=participacao_id)
        participacao.ap1 = ap1 if ap1 != '' else None
        participacao.ap2 = ap2 if ap2 != '' else None
        participacao.cr = cr if cr != '' else None
        participacao.save()
        return participacao

class PresencaService:
    """Service para operações de presenças."""

    def listar_presencas(self, turma_id=None, data=None):
        presencas = Presenca.objects.all().select_related('aluno', 'turma')
        if turma_id:
            presencas = presencas.filter(turma__id=turma_id)
        if data:
            presencas = presencas.filter(data=data)
        turmas = Turma.objects.filter(ativo=True)
        return {
            'presencas': presencas,
            'turmas': turmas,
        }

    def editar_presenca(self, presenca_id, presente):
        presenca = get_object_or_404(Presenca, id=presenca_id)
        presenca.presente = presente
        presenca.save()


class RelatorioService:
    """Service para relatórios do sistema."""

    def desempenho(self):
        participacoes = ParticipacaoMonitoria.objects.all().select_related('aluno', 'turma')
        return {
            'participacoes': participacoes,
            'titulo': 'Relatório de Desempenho',
        }

    def frequencia(self):
        presencas = Presenca.objects.all().select_related('aluno', 'turma')
        return {
            'presencas': presencas,
            'titulo': 'Relatório de Frequência',
        }

    def inscricoes(self):
        inscricoes = Inscricao.objects.all().select_related('aluno', 'vaga')
        return {
            'inscricoes': inscricoes,
            'titulo': 'Relatório de Inscrições',
        }

    def geral(self):
        return {
            'total_usuarios': Usuario.objects.filter(ativo=True).count(),
            'total_alunos': Aluno.objects.filter(ativo=True).count(),
            'total_funcionarios': Funcionario.objects.filter(ativo=True).count(),
            'total_turmas': Turma.objects.filter(ativo=True).count(),
            'total_vagas': Vaga.objects.filter(ativo=True).count(),
            'total_inscricoes': Inscricao.objects.count(),
            'total_presencas': Presenca.objects.filter(presente=True).count(),
            'titulo': 'Relatório Geral',
        }

class PerfilService:
    """Service para operações de perfil do usuário."""

    def get_perfil_context(self, user):
        # Busca aluno e professor pelo email do usuário
        try:
            aluno = Aluno.objects.get(email=user.email)
        except Aluno.DoesNotExist:
            aluno = None
        try:
            professor = Funcionario.objects.get(email=user.email)
        except Funcionario.DoesNotExist:
            professor = None
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
        # Atualiza também Aluno, se existir
        try:
            aluno = Aluno.objects.get(email=user.email)
            aluno.nome = nome
            aluno.email = email
            aluno.save()
        except Aluno.DoesNotExist:
            pass


