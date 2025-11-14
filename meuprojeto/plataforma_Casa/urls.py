"""
================================================================================
CONFIGURAÇÃO DE URLS - APLICAÇÃO PLATAFORMA CASA
================================================================================

Este arquivo define todas as rotas (padrões de URL) da aplicação plataforma_Casa.
Cada rota mapeia um caminho de URL para uma view específica que processa a requisição.

A aplicação segue o padrão REST com operações CRUD (Create, Read, Update, Delete):
- GET:  Recuperar dados
- POST: Criar ou atualizar dados
- DELETE: Remover dados (implementado como GET com confirmação)

Documentação: https://docs.djangoproject.com/en/5.2/topics/http/urls/
================================================================================
"""

from django.urls import path
from . import views

urlpatterns = [
    
    # 1. AUTENTICAÇÃO E PÁGINAS PRINCIPAIS
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('', views.portal_vagas, name='home'),
 

    # 2. MÓDULO DE USUÁRIOS (ADMIN)
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/criar/', views.criar_usuario, name='criar_usuario'),
    path('usuarios/<int:usuario_id>/editar/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:usuario_id>/deletar/', views.deletar_usuario, name='deletar_usuario'),
    
    # 3. MÓDULO DE ALUNOS (ADMIN)
    path('alunos/', views.listar_alunos, name='listar_alunos'),
    path('alunos/criar/', views.criar_aluno, name='criar_aluno'),
    path('alunos/<int:aluno_id>/editar/', views.editar_aluno, name='editar_aluno'),
    path('alunos/<int:aluno_id>/deletar/', views.deletar_aluno, name='deletar_aluno'),
    
    # 4. MÓDULO DE VAGAS (PROFESSOR/COORDENADOR)
    path('vagas/', views.listar_vagas_monitoria, name='listar_vagas_monitoria'),
    path('vagas/criar/', views.criar_vaga_monitoria, name='criar_vaga_monitoria'),
    path('vagas/gerenciar/', views.listar_vagas_monitoria, name='listar_vagas'),
    path('vagas/<int:vaga_id>/', views.detalhe_vaga_monitoria, name='detalhe_vaga_monitoria'),
    path('vagas/<int:vaga_id>/editar/', views.editar_vaga_monitoria, name='editar_vaga_monitoria'),
    path('vagas/<int:vaga_id>/deletar/', views.deletar_vaga_monitoria, name='deletar_vaga_monitoria'),

    # 5. MÓDULO DE TURMAS (ADMIN/MONITOR)
    path('turmas/', views.listar_turmas, name='listar_turmas'),
    path('turmas/criar/', views.criar_turma, name='criar_turma'),
    path('turmas/<int:turma_id>/', views.detalhe_turma, name='detalhe_turma'),
    path('turmas/<int:turma_id>/editar/', views.editar_turma, name='editar_turma'),
    path('turmas/<int:turma_id>/deletar/', views.deletar_turma, name='deletar_turma'),
    
    # 8. MÓDULO DE RELATÓRIOS (ADMIN)
    path('relatorios/', views.listar_relatorios, name='listar_relatorios'),
    path('relatorios/desempenho/', views.relatorio_desempenho, name='relatorio_desempenho'),
    path('relatorios/frequencia/', views.relatorio_frequencia, name='relatorio_frequencia'),
    path('relatorios/inscricoes/', views.relatorio_inscricoes, name='relatorio_inscricoes'),
    path('relatorios/geral/', views.relatorio_geral, name='relatorio_geral'),
    
    # 11. PORTAL DE VAGAS E CANDIDATURAS (ALUNO)
    path('portal-vagas/', views.portal_vagas, name='portal_vagas'),
    path('vagas/<int:vaga_id>/candidatar/', views.candidatar_vaga, name='candidatar_vaga'),
    # path('minhas-inscricoes/', views.minhas_inscricoes, name='minhas_inscricoes'), # Adicionar se a view existir

    # 13. REGISTRO E VALIDAÇÃO DE HORAS (MONITOR/PROFESSOR)
    path('horas/registrar/', views.registrar_horas, name='registrar_horas'),
    path('horas/meus-registros/', views.meus_registros_horas, name='meus_registros_horas'),
    path('horas/detalhes/<int:registro_id>/', views.detalhes_registro, name='detalhes_registro'),
    path('horas/validar/', views.validar_horas, name='validar_horas'),
    path('horas/<int:registro_id>/aprovar/', views.aprovar_horas, name='aprovar_horas'),
    
    # 14. DASHBOARD DE GESTÃO (ADMIN)
    path('gestao/dashboard/', views.dashboard_gestao, name='dashboard_gestao'),
    
    # 16. GERENCIAMENTO DE DISCIPLINAS (PROFESSOR)
    path('professor/disciplinas/', views.listar_disciplinas, name='listar_disciplinas'),
    path('professor/disciplinas/nova/', views.criar_disciplina, name='criar_disciplina'),
    path('professor/disciplinas/<int:disciplina_id>/', views.detalhes_disciplina, name='detalhes_disciplina'),
    path('professor/disciplinas/<int:disciplina_id>/editar/', views.editar_disciplina, name='editar_disciplina'),

    # 14. DASHBOARD DE GESTÃO 
    path('gestao/dashboard/', views.dashboard_gestao, name='dashboard_gestao'),

    # Pagamentos - Gestão
    path('gestao/pagamentos/', views.gerenciar_pagamentos, name='gerenciar_pagamentos'),
    path('gestao/pagamentos/<int:pagamento_id>/processar/', views.processar_pagamento, name='processar_pagamento'),

    # 15. DASHBOARD DO PROFESSOR (NOVO)
    path('professor/dashboard/', views.dashboard_professor, name='dashboard_professor'),

    path('monitorias/', views.listar_monitorias, name='listar_monitorias'),


    path('presencas/', views.listar_presencas, name='listar_presencas'),

    path('perfil/', views.perfil, name='perfil'),
    path('perfil/atualizar/', views.atualizar_perfil_rapido, name='atualizar_perfil_rapido'),


]