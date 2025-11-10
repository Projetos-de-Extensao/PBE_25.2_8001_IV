from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Vaga, Inscricao, Curso, Aluno, Funcionario, Turma, RegistroHoras, Documento, StatusPagamento

class BaseService:
    """Classe base para services — coloque helpers comuns aqui."""
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

