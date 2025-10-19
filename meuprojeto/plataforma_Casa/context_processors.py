"""
Context processors para adicionar informações de grupo do usuário ao contexto dos templates
"""

def user_groups(request):
    """
    Adiciona informações sobre os grupos do usuário ao contexto do template
    """
    if request.user.is_authenticated:
        return {
            'is_aluno': request.user.groups.filter(name='Aluno').exists(),
            'is_monitor': request.user.groups.filter(name='Monitor').exists(),
            'is_professor': request.user.groups.filter(name='Professor').exists(),
            'is_admin': request.user.is_staff or request.user.is_superuser,
        }
    return {
        'is_aluno': False,
        'is_monitor': False,
        'is_professor': False,
        'is_admin': False,
    }
