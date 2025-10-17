from .repository import VagaRepository
from .models import Curso, Funcionario

class VagasService:
    def __init__(self):
        self.vagas_repository = VagaRepository()
        self.cursos = Curso.objects.filter(ativo=True)
        self.coordenadores = Funcionario.objects.filter(coordenador=True, ativo=True)

    def listar_vagas_ativas(self):
        return self.vagas_repository.listar_vagas_ativas()
    
    def criar_vaga(self, dados_vaga):
        return self.vagas_repository.criar_vaga(dados_vaga)
    
    def processar_criacao_vaga(self, request):
        mensagem = None
        if request.method == 'POST':
            nome = request.POST.get('nome')
            curso_id = request.POST.get('curso')
            coordenador_id = request.POST.get('coordenador')
            descricao = request.POST.get('descricao')
            requisitos = request.POST.get('requisitos')
            ativo = bool(request.POST.get('ativo'))

            curso = Curso.objects.get(id=curso_id)
            coordenador = Funcionario.objects.get(id=coordenador_id)

            dados_vaga = {
                'nome': nome,
                'curso': curso,
                'coordenador': coordenador,
                'descricao': descricao,
                'requisitos': requisitos,
                'ativo': ativo
            }
            self.criar_vaga(dados_vaga)
            mensagem = 'Vaga registrada com sucesso!'
        return mensagem

    def vagas_service(self, request=None):
        contexto = {
            'cursos': self.cursos,
            'coordenadores': self.coordenadores,
        }
        if request:
            mensagem = self.processar_criacao_vaga(request)
            if mensagem:
                contexto['mensagem'] = mensagem
        return contexto