from rest_framework.routers import DefaultRouter

from .api.viewsets import (
    CursoViewSet,
    VagaViewSet,
    TurmaViewSet,
    AlunoViewSet,
    InscricaoViewSet,
)

# Router padrão do DRF para expor endpoints de leitura na documentação
router = DefaultRouter()
router.register(r'cursos', CursoViewSet, basename='curso')
router.register(r'alunos', AlunoViewSet, basename='aluno')
router.register(r'vagas', VagaViewSet, basename='vaga')
router.register(r'turmas', TurmaViewSet, basename='turma')
router.register(r'inscricoes', InscricaoViewSet, basename='inscricao')

urlpatterns = router.urls
