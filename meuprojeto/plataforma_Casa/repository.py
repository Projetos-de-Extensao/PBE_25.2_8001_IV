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



