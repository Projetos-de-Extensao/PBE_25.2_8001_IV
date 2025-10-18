from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Usuários
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/criar/', views.criar_usuario, name='criar_usuario'),
    path('usuarios/<int:usuario_id>/editar/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:usuario_id>/deletar/', views.deletar_usuario, name='deletar_usuario'),
    
    # Alunos
    path('alunos/', views.listar_alunos, name='listar_alunos'),
    path('alunos/criar/', views.criar_aluno, name='criar_aluno'),
    path('alunos/<int:aluno_id>/editar/', views.editar_aluno, name='editar_aluno'),
    path('alunos/<int:aluno_id>/deletar/', views.deletar_aluno, name='deletar_aluno'),
    
    # Vagas
    path('vagas/', views.listar_vagas, name='listar_vagas'),
    path('vagas/<int:vaga_id>/', views.detalhe_vaga, name='detalhe_vaga'),
    path('vagas/criar/', views.criar_vaga, name='criar_vaga'),
    path('vagas/<int:vaga_id>/editar/', views.editar_vaga, name='editar_vaga'),
    path('vagas/<int:vaga_id>/deletar/', views.deletar_vaga, name='deletar_vaga'),
    
    # Turmas
    path('turmas/', views.listar_turmas, name='listar_turmas'),
    path('turmas/<int:turma_id>/', views.detalhe_turma, name='detalhe_turma'),
    path('turmas/criar/', views.criar_turma, name='criar_turma'),
    path('turmas/<int:turma_id>/editar/', views.editar_turma, name='editar_turma'),
    path('turmas/<int:turma_id>/deletar/', views.deletar_turma, name='deletar_turma'),
    
    # Monitorias
    path('monitorias/', views.listar_monitorias, name='listar_monitorias'),
    path('monitorias/<int:participacao_id>/editar/', views.editar_participacao, name='editar_participacao'),
    
    # Presenças
    path('presencas/', views.listar_presencas, name='listar_presencas'),
    path('presencas/<int:presenca_id>/editar/', views.editar_presenca, name='editar_presenca'),
    
    # Relatórios
    path('relatorios/', views.listar_relatorios, name='listar_relatorios'),
    path('relatorios/desempenho/', views.relatorio_desempenho, name='relatorio_desempenho'),
    path('relatorios/frequencia/', views.relatorio_frequencia, name='relatorio_frequencia'),
    path('relatorios/inscricoes/', views.relatorio_inscricoes, name='relatorio_inscricoes'),
    path('relatorios/geral/', views.relatorio_geral, name='relatorio_geral'),
    
    # Perfil
    path('perfil/', views.perfil, name='perfil'),
    path('alterar-senha/', views.alterar_senha, name='alterar_senha'),
    
    # SQL View (original)
    path('sql/', views.sql_view, name='sql_view'),
]