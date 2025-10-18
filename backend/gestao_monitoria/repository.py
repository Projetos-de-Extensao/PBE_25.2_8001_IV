from django.contrib.auth.models import User

from .models import (AgendamentoMonitoria, AlunoProfile, Curso,
                     FuncionarioProfile, HorarioDisponivel, Inscricao,
                     ParticipacaoMonitoria, Presenca, Sala, SubmissaoHoras,
                     Turma, Vaga)


class VagaRepository:
    
    @staticmethod
    def listar_vagas_ativas():
        return Vaga.objects.filter(ativo=True).select_related('curso', 'coordenador__user')

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
        return Inscricao.objects.all().select_related('aluno__user', 'vaga')

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


# Funções auxiliares para compatibilidade
def listar_funcionarios():
    return FuncionarioProfile.objects.all().select_related('user')


def listar_alunos():
    return AlunoProfile.objects.all().select_related('user', 'curso')


def listar_vagas():
    return Vaga.objects.all().select_related('curso', 'coordenador')


def listar_turmas():
    return Turma.objects.all().select_related('vaga', 'sala', 'monitor', 'curso')


def listar_inscricoes():
    return Inscricao.objects.all().select_related('aluno', 'vaga')


def listar_cursos():
    return Curso.objects.all()


def listar_salas():
    return Sala.objects.all()


def listar_participacoes_monitoria():
    return ParticipacaoMonitoria.objects.all().select_related('aluno', 'turma')


def listar_presencas():
    return Presenca.objects.all().select_related('turma', 'aluno')


def listar_horarios_disponiveis():
    return HorarioDisponivel.objects.all().select_related('monitor', 'turma')


def listar_agendamentos():
    return AgendamentoMonitoria.objects.all().select_related('aluno', 'turma', 'monitor')


def listar_submissoes_horas():
    return SubmissaoHoras.objects.all().select_related('monitor', 'turma', 'aprovado_por')





