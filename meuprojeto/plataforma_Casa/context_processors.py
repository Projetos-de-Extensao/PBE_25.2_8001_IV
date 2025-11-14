"""
Context processors para adicionar informações de grupo do usuário ao contexto dos templates
"""

def user_groups(request):
    """
    Adiciona informações sobre os grupos do usuário ao contexto do template
    """
    if request.user.is_authenticated:
        is_aluno = request.user.groups.filter(name='Aluno').exists()
        is_monitor = request.user.groups.filter(name='Monitor').exists()
        is_professor = request.user.groups.filter(name='Professor').exists()
        is_admin = request.user.is_staff or request.user.is_superuser

        # Fallback detection: alguns ambientes não atribuem o grupo "Monitor"
        # corretamente ao usuário. Tentamos detectar se o usuário é monitor
        # verificando registros associados (Turma.monitor) ou registros de horas.
        if not is_monitor:
            try:
                # Import aqui para evitar dependência circular em import time
                from .service import RegistroHorasService, PortalVagasService
                from .models import Turma

                # 1) Se existir um registro de monitor por email no serviço de horas
                try:
                    registro_service = RegistroHorasService()
                    mon = registro_service.get_monitor_by_email(request.user.email)
                    if mon:
                        is_monitor = True
                except Exception:
                    pass

                # 2) Se o usuário for um Aluno que aparece como monitor em qualquer Turma
                if not is_monitor:
                    try:
                        portal = PortalVagasService()
                        aluno = portal.get_aluno(request.user.email)
                        if aluno and Turma.objects.filter(monitor=aluno).exists():
                            is_monitor = True
                    except Exception:
                        pass
            except Exception:
                # Se qualquer import falhar, não interromper a renderização do template
                is_monitor = is_monitor

        return {
            'is_aluno': is_aluno,
            'is_monitor': is_monitor,
            'is_professor': is_professor,
            'is_admin': is_admin,
        }
    return {
        'is_aluno': False,
        'is_monitor': False,
        'is_professor': False,
        'is_admin': False,
    }
