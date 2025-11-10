from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from django.db import IntegrityError, transaction


from .models import Vaga, Inscricao, Curso, Usuario, TipoUsuario, Aluno, Funcionario, Turma, RegistroHoras, Documento, StatusPagamento

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