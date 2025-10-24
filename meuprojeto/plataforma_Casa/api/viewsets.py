from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny

from ..models import Curso, Vaga, Turma, Aluno, Inscricao
from .serializers import (
    CursoSerializer,
    VagaSerializer,
    TurmaSerializer,
    AlunoSerializer,
    InscricaoSerializer,
)


class BaseReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet base apenas leitura, com suporte a busca e ordenação,
    para permitir navegação interativa no Swagger.
    """

    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]


class CursoViewSet(BaseReadOnlyViewSet):
    """Lista cursos ativos para uso público na documentação."""
    queryset = Curso.objects.all().order_by('nome')
    serializer_class = CursoSerializer
    search_fields = ['nome']
    ordering_fields = ['nome', 'ativo']
    ordering = ['nome']


class AlunoViewSet(BaseReadOnlyViewSet):
    """Retorna alunos com informações acadêmicas básicas."""
    queryset = Aluno.objects.select_related('curso').all().order_by('nome')
    serializer_class = AlunoSerializer
    search_fields = ['nome', 'email', 'matricula']
    ordering_fields = ['nome', 'matricula', 'periodo', 'cr_geral']
    ordering = ['nome']


class VagaViewSet(BaseReadOnlyViewSet):
    """Expõe vagas de monitoria para consulta rápida e filtros no Swagger."""
    queryset = Vaga.objects.select_related('curso', 'coordenador').all().order_by('-criado_em')
    serializer_class = VagaSerializer
    search_fields = ['nome', 'descricao', 'requisitos', 'disciplina']
    ordering_fields = ['criado_em', 'numero_vagas', 'nome']
    ordering = ['-criado_em']


class TurmaViewSet(BaseReadOnlyViewSet):
    """Lista turmas de monitoria com dados agregados de sala, curso e monitor."""
    queryset = (
        Turma.objects.select_related('vaga', 'sala', 'monitor', 'curso')
        .all()
        .order_by('nome')
    )
    serializer_class = TurmaSerializer
    search_fields = ['nome', 'descricao', 'dias_da_semana', 'horario']
    ordering_fields = ['nome', 'data_inicio', 'data_fim']
    ordering = ['nome']


class InscricaoViewSet(BaseReadOnlyViewSet):
    """Permite visualizar inscrições realizadas em cada vaga."""
    queryset = Inscricao.objects.select_related('aluno', 'vaga').all().order_by('-data_inscricao')
    serializer_class = InscricaoSerializer
    search_fields = ['aluno__nome', 'vaga__nome', 'status']
    ordering_fields = ['data_inscricao', 'status']
    ordering = ['-data_inscricao']
