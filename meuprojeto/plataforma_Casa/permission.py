
def _user_groups_lower(user):
    try:
        return {g.name.lower() for g in user.groups.all()}
    except Exception:
        return set()


def is_adm(user):
    groups = _user_groups_lower(user)
    return 'admin' in groups or 'adm' in groups


def is_admin_user(user):
    groups = _user_groups_lower(user)
    return 'admin_user' in groups or 'adminuser' in groups


def is_aluno_access(user):
    groups = _user_groups_lower(user)
    return bool(groups & {'admin', 'dev', 'user_aluno', 'aluno'})


def is_monitor_access(user):
    groups = _user_groups_lower(user)
    return bool(groups & {'admin', 'dev', 'user_monitor', 'monitor'})


def is_professor_access(user):
    groups = _user_groups_lower(user)
    return bool(groups & {'admin', 'dev', 'user_professor', 'user_coordenador', 'professor', 'coordenador'})


def is_funcionairo_access(user):
    groups = _user_groups_lower(user)
    return bool(groups & {'admin', 'dev', 'user_funcionairo', 'user_professor', 'user_coordenador', 'funcionario'})