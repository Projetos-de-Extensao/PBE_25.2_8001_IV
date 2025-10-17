from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    sql_view, TipoUsuarioViewSet, CursoViewSet, SalaViewSet,
    UsuarioViewSet, FuncionarioViewSet, AlunoViewSet,
    VagaViewSet, TurmaViewSet, ParticipacaoMonitoriaViewSet,
    PresencaViewSet, InscricaoViewSet,
    HorarioDisponivelViewSet, AgendamentoMonitoriaViewSet, SubmissaoHorasViewSet,
    register, login, user_profile, dashboard_stats, exportar_relatorio
)

# Router para API REST
router = DefaultRouter()
router.register(r'tipos-usuario', TipoUsuarioViewSet)
router.register(r'cursos', CursoViewSet)
router.register(r'salas', SalaViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'funcionarios', FuncionarioViewSet)
router.register(r'alunos', AlunoViewSet)
router.register(r'vagas', VagaViewSet)
router.register(r'turmas', TurmaViewSet)
router.register(r'participacoes-monitoria', ParticipacaoMonitoriaViewSet)
router.register(r'presencas', PresencaViewSet)
router.register(r'inscricoes', InscricaoViewSet)
router.register(r'horarios-disponiveis', HorarioDisponivelViewSet)
router.register(r'agendamentos', AgendamentoMonitoriaViewSet)
router.register(r'submissoes-horas', SubmissaoHorasViewSet)

urlpatterns = [
    path('sql/', sql_view, name='sql_view'),
    # API Routes
    path('api/', include([
        path('', include(router.urls)),
        # Autenticação
        path('auth/register/', register, name='register'),
        path('auth/login/', login, name='login'),
        path('auth/profile/', user_profile, name='user_profile'),
        path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        # Dashboard
        path('dashboard/stats/', dashboard_stats, name='dashboard_stats'),
        # Relatórios
        path('relatorios/exportar/', exportar_relatorio, name='exportar_relatorio'),
    ])),
]
