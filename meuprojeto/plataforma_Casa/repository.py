from .models import Usuario, Funcionario, Aluno, Vaga, Turma, Inscricao, Curso, TipoUsuario, Sala, ParticipacaoMonitoria, Presenca


class VagaRepository:
    @staticmethod
    def get_vaga_by_id(vaga_id):
        return Vaga.objects.get(id=vaga_id)

    @staticmethod
    def get_funcionario_by_email(email):
        return Funcionario.objects.get(email=email)

    @staticmethod
    def get_inscricoes_by_vaga(vaga):
        return Inscricao.objects.filter(vaga=vaga).select_related('aluno', 'aluno__curso').order_by('-data_inscricao')

    @staticmethod
    def get_coordenadores(vaga):
        return vaga.coordenadores.all()

    @staticmethod
    def get_professores(vaga):
        return vaga.professores.all()

class UsuarioRepository:
    @staticmethod
    def list_users(tipo_id=None, ativo=None):
        qs = Usuario.objects.all().select_related('tipo_usuario')
        if tipo_id:
            qs = qs.filter(tipo_usuario__id=tipo_id)
        if ativo is not None:
            qs = qs.filter(ativo=ativo)
        return qs

    @staticmethod
    def get_tipo_usuario_by_id(tipo_usuario_id):
        return TipoUsuario.objects.get(id=tipo_usuario_id)

    @staticmethod
    def get_usuario_by_id(usuario_id):
        return Usuario.objects.get(id=usuario_id)

    @staticmethod
    def get_usuario_by_email(email):
        return Usuario.objects.get(email=email)

class AlunoRepository:
    @staticmethod
    def list_alunos(curso_id=None, periodo=None):
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

    @staticmethod
    def get_aluno_by_id(aluno_id):
        return Aluno.objects.get(id=aluno_id)

    @staticmethod
    def get_curso_by_id(curso_id):
        return Curso.objects.get(id=curso_id)

    @staticmethod
    def get_or_create_tipo_usuario_aluno():
        return TipoUsuario.objects.get_or_create(tipo='aluno', defaults={'ativo': True})

    @staticmethod
    def create_aluno(**kwargs):
        return Aluno.objects.create(**kwargs)


class TurmaRepository:
    @staticmethod
    def list_turmas(vaga_id=None, status=None):
        qs = Turma.objects.all().select_related('vaga', 'monitor', 'sala', 'curso')
        if vaga_id:
            qs = qs.filter(vaga__id=vaga_id)
        if status is not None:
            qs = qs.filter(ativo=(status == 'ativa'))
        return qs

    @staticmethod
    def get_turma_by_id(turma_id):
        return Turma.objects.get(id=turma_id)

    @staticmethod
    def get_participacoes_by_turma(turma):
        return ParticipacaoMonitoria.objects.filter(turma=turma).select_related('aluno')

    @staticmethod
    def get_presencas_by_turma(turma):
        return Presenca.objects.filter(turma=turma).select_related('aluno')

    @staticmethod
    def get_vaga_by_id(vaga_id):
        return Vaga.objects.get(id=vaga_id)

    @staticmethod
    def get_sala_by_id(sala_id):
        return Sala.objects.get(id=sala_id)

    @staticmethod
    def get_monitor_by_id(monitor_id):
        return Aluno.objects.get(id=monitor_id)

    @staticmethod
    def get_curso_by_id(curso_id):
        return Curso.objects.get(id=curso_id)

    @staticmethod
    def create_turma(**kwargs):
        return Turma.objects.create(**kwargs)
    

class MonitoriaRepository:
    @staticmethod
    def get_professor_by_email(email):
        return Funcionario.objects.get(email=email)

    @staticmethod
    def get_turmas_by_professor(professor):
        return Turma.objects.filter(
            vaga__professores=professor,
            ativo=True
        ).select_related('vaga', 'monitor', 'curso', 'sala').order_by('-criado_em')

    @staticmethod
    def get_participacoes_by_turmas(turmas):
        return ParticipacaoMonitoria.objects.filter(
            turma__in=turmas
        ).select_related('aluno', 'turma')

    @staticmethod
    def get_participacao_by_id(participacao_id):
        return ParticipacaoMonitoria.objects.get(id=participacao_id)
    
class PresencaRepository:
    @staticmethod
    def list_presencas(turma_id=None, data=None):
        presencas = Presenca.objects.all().select_related('aluno', 'turma')
        if turma_id:
            presencas = presencas.filter(turma__id=turma_id)
        if data:
            presencas = presencas.filter(data=data)
        return presencas

    @staticmethod
    def get_turmas_ativas():
        return Turma.objects.filter(ativo=True)

    @staticmethod
    def get_presenca_by_id(presenca_id):
        return Presenca.objects.get(id=presenca_id)