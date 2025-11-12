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

