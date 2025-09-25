from django.shortcuts import render
from .repository import listar_usuarios, listar_alunos, listar_cursos, listar_funcionarios, listar_inscricoes, listar_turmas, listar_participacoes_monitoria, listar_presencas, listar_salas, listar_tipos_usuario


# Create your views here.
def sql_view(request):
    usuarios = listar_usuarios()
    alunos = listar_alunos()
    cursos = listar_cursos()
    funcionarios = listar_funcionarios()
    inscricoes = listar_inscricoes()
    turmas = listar_turmas()
    participacoes_monitoria = listar_participacoes_monitoria()
    presencas = listar_presencas()
    salas = listar_salas()
    tipos_usuario = listar_tipos_usuario()
    
    return render(request, 'sql_template.html', {'usuarios': usuarios, 
                                                 'alunos': alunos, 
                                                'cursos': cursos, 
                                                'funcionarios': funcionarios, 
                                                'inscricoes': inscricoes, 
                                                'turmas': turmas, 
                                                'participacoes_monitoria': participacoes_monitoria, 
                                                'presencas': presencas, 
                                                'salas': salas, 
                                                'tipos_usuario': tipos_usuario})
