from .models import Usuario, Funcionario, Aluno, Vaga, Turma, Inscricao, Curso, TipoUsuario, Sala, ParticipacaoMonitoria, Presenca



class VagaRepository:
    
    @staticmethod
    def listar_vagas_ativas():
        return Vaga.objects.filter(ativo=True)

    @staticmethod
    def criar_vaga(dados_vaga):
        vaga = Vaga.objects.create(**dados_vaga)
        return vaga
    
    @staticmethod
    def atualizar_vaga(id_vaga, dados_atualizados):
        Vaga.objects.filter(id=id_vaga).update(**dados_atualizados)
        return Vaga.objects.get(id=id_vaga)
    
    @staticmethod
    def deletar_vaga(id_vaga):
        Vaga.objects.filter(id=id_vaga).delete()


class InscricaoRepository:
    @staticmethod
    def listar_inscricoes():
        return Inscricao.objects.all()

    @staticmethod
    def criar_inscricao(dados_inscricao):
        inscricao = Inscricao.objects.create(**dados_inscricao)
        return inscricao
    
    @staticmethod
    def atualizar_inscricao(id_inscricao, dados_atualizados):
        Inscricao.objects.filter(id=id_inscricao).update(**dados_atualizados)
        return Inscricao.objects.get(id=id_inscricao)
    
    @staticmethod
    def deletar_inscricao(id_inscricao):
        Inscricao.objects.filter(id=id_inscricao).delete()

        


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




