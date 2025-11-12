from .models import Usuario, Funcionario, Aluno, Vaga, Turma, Inscricao, Curso, TipoUsuario, Sala, ParticipacaoMonitoria, Presenca


class DetalheVagaRepository:

    @staticmethod
    def listar_vagas_disponiveis():
        return Vaga.objects.filter(disponivel=True)
    
    

def listar_usuarios():
    return Usuario.objects.all()

def listar_funcionarios():
    return Funcionario.objects.all()

def listar_alunos():
    return Aluno.objects.all()

def listar_vagas():
    return Vaga.objects.all()

def listar_turmas():
    return Turma.objects.all()

def listar_inscricoes():
    return Inscricao.objects.all()

def listar_cursos():
    return Curso.objects.all()

def listar_tipos_usuario():
    return TipoUsuario.objects.all()

def listar_salas():
    return Sala.objects.all()

def listar_participacoes_monitoria():
    return ParticipacaoMonitoria.objects.all()

def listar_presencas():
    return Presenca.objects.all()




