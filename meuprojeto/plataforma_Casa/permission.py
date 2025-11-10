
def is_adm(user):
    return user.groups.filter(name='admin').exists()

def is_admin_user(user):
    return user.groups.filter(name='admin_user').exists()

def is_aluno_access(user):
    return user.groups.filter(name__in=['Admin', 'dev', 'user_aluno']).exists()

def is_monitor_access(user):
    return user.groups.filter(name__in=['Admin', 'dev', 'user_monitor']).exists()

def is_funcionairo_access(user):
    return user.groups.filter(name__in=['Admin', 'dev', 'user_funcionairo', 'user_professor','user_coordenador']).exists()