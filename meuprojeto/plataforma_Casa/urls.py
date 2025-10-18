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

# ================================================================================
# PADRÕES DE URL - URL PATTERNS
# ================================================================================

urlpatterns = [
    
    # ============================================================================
    # 1. DASHBOARD - PÁGINA INICIAL
    # ============================================================================
    # Rota raiz da aplicação - exibe o dashboard com resumo geral
    # Método HTTP: GET
    # URL: http://localhost:8000/
    # Nome: 'dashboard' (usado em templates com {% url 'dashboard' %})
    path('', views.dashboard, name='dashboard'),
    
    # ============================================================================
    # 2. MÓDULO DE USUÁRIOS - CRUD COMPLETO
    # ============================================================================
    
    # --- Listar Usuários ---
    # Exibe tabela com todos os usuários cadastrados no sistema
    # Método HTTP: GET
    # URL: http://localhost:8000/usuarios/
    # Suporta filtros: ?tipo=1&status=ativo
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    
    # --- Criar Novo Usuário ---
    # Exibe formulário para criação de novo usuário
    # POST: Processa e salva novo usuário no banco de dados
    # Método HTTP: GET (formulário) / POST (submissão)
    # URL: http://localhost:8000/usuarios/criar/
    path('usuarios/criar/', views.criar_usuario, name='criar_usuario'),
    
    # --- Editar Usuário ---
    # Exibe formulário com dados do usuário para edição
    # <int:usuario_id>: ID inteiro do usuário (ex: 1, 2, 3...)
    # POST: Salva alterações no banco de dados
    # Método HTTP: GET (formulário) / POST (submissão)
    # URL: http://localhost:8000/usuarios/5/editar/
    path('usuarios/<int:usuario_id>/editar/', views.editar_usuario, name='editar_usuario'),
    
    # --- Deletar Usuário ---
    # Remove o usuário do banco de dados
    # <int:usuario_id>: ID inteiro do usuário
    # Requer confirmação do usuário
    # Método HTTP: GET (com confirmação)
    # URL: http://localhost:8000/usuarios/5/deletar/
    path('usuarios/<int:usuario_id>/deletar/', views.deletar_usuario, name='deletar_usuario'),
    
    # ============================================================================
    # 3. MÓDULO DE ALUNOS - CRUD COMPLETO
    # ============================================================================
    
    # --- Listar Alunos ---
    # Exibe tabela com todos os alunos cadastrados
    # Inclui informações: nome, matrícula, email, curso, período, CR, status
    # Método HTTP: GET
    # URL: http://localhost:8000/alunos/
    # Suporta filtros: ?curso=1&periodo=3
    path('alunos/', views.listar_alunos, name='listar_alunos'),
    
    # --- Criar Novo Aluno ---
    # Formulário para cadastro de novo aluno
    # Coleta dados: nome, email, matrícula, curso, período, CR geral
    # Método HTTP: GET (formulário) / POST (submissão)
    # URL: http://localhost:8000/alunos/criar/
    path('alunos/criar/', views.criar_aluno, name='criar_aluno'),
    
    # --- Editar Aluno ---
    # Permite atualizar dados do aluno (período, CR, status)
    # Matrícula é imutável (somente leitura)
    # Método HTTP: GET (formulário) / POST (submissão)
    # URL: http://localhost:8000/alunos/3/editar/
    path('alunos/<int:aluno_id>/editar/', views.editar_aluno, name='editar_aluno'),
    
    # --- Deletar Aluno ---
    # Remove aluno do banco de dados (com confirmação)
    # Método HTTP: GET (com confirmação)
    # URL: http://localhost:8000/alunos/3/deletar/
    path('alunos/<int:aluno_id>/deletar/', views.deletar_aluno, name='deletar_aluno'),
    
    # ============================================================================
    # 4. MÓDULO DE VAGAS - CRUD + DETALHE
    # ============================================================================
    
    # --- Listar Vagas ---
    # Exibe cards com todas as vagas de monitoria disponíveis
    # Mostra: nome, curso, descrição, requisitos, inscritos, coordenador
    # Método HTTP: GET
    # URL: http://localhost:8000/vagas/
    # Suporta filtros: ?curso=1&status=ativa
    path('vagas/', views.listar_vagas, name='listar_vagas'),
    
    # --- Detalhe da Vaga ---
    # Exibe informações detalhadas de uma vaga específica
    # Inclui lista de alunos inscritos
    # Método HTTP: GET
    # URL: http://localhost:8000/vagas/2/
    path('vagas/<int:vaga_id>/', views.detalhe_vaga, name='detalhe_vaga'),
    
    # --- Criar Nova Vaga ---
    # Formulário para criação de vaga de monitoria
    # Coleta: nome, curso, coordenador, descrição, requisitos
    # Método HTTP: GET (formulário) / POST (submissão)
    # URL: http://localhost:8000/vagas/criar/
    path('vagas/criar/', views.criar_vaga, name='criar_vaga'),
    
    # --- Editar Vaga ---
    # Permite editar informações da vaga
    # Método HTTP: GET (formulário) / POST (submissão)
    # URL: http://localhost:8000/vagas/2/editar/
    path('vagas/<int:vaga_id>/editar/', views.editar_vaga, name='editar_vaga'),
    
    # --- Deletar Vaga ---
    # Remove vaga do sistema (com confirmação)
    # Método HTTP: GET (com confirmação)
    # URL: http://localhost:8000/vagas/2/deletar/
    path('vagas/<int:vaga_id>/deletar/', views.deletar_vaga, name='deletar_vaga'),
    
    # ============================================================================
    # 5. MÓDULO DE TURMAS - CRUD + DETALHE
    # ============================================================================
    
    # --- Listar Turmas ---
    # Exibe tabela com todas as turmas de monitoria
    # Mostra: nome, vaga, monitor, sala, período, horário, status
    # Método HTTP: GET
    # URL: http://localhost:8000/turmas/
    # Suporta filtros: ?vaga=1&status=ativa
    path('turmas/', views.listar_turmas, name='listar_turmas'),
    
    # --- Detalhe da Turma ---
    # Exibe informações completas da turma
    # Inclui: participações, presenças, schedule
    # Método HTTP: GET
    # URL: http://localhost:8000/turmas/1/
    path('turmas/<int:turma_id>/', views.detalhe_turma, name='detalhe_turma'),
    
    # --- Criar Nova Turma ---
    # Formulário para criação de turma
    # Coleta: nome, vaga, sala, descrição, datas, horários, monitor, curso
    # Método HTTP: GET (formulário) / POST (submissão)
    # URL: http://localhost:8000/turmas/criar/
    path('turmas/criar/', views.criar_turma, name='criar_turma'),
    
    # --- Editar Turma ---
    # Permite atualizar dados da turma
    # Método HTTP: GET (formulário) / POST (submissão)
    # URL: http://localhost:8000/turmas/1/editar/
    path('turmas/<int:turma_id>/editar/', views.editar_turma, name='editar_turma'),
    
    # --- Deletar Turma ---
    # Remove turma do sistema (com confirmação)
    # Método HTTP: GET (com confirmação)
    # URL: http://localhost:8000/turmas/1/deletar/
    path('turmas/<int:turma_id>/deletar/', views.deletar_turma, name='deletar_turma'),
    
    # ============================================================================
    # 6. MÓDULO DE MONITORIAS - GERENCIAMENTO DE PARTICIPAÇÕES
    # ============================================================================
    
    # --- Listar Participações em Monitorias ---
    # Exibe tabela com desempenho de alunos nas monitorias
    # Mostra: aluno, turma, AP1, AP2, CR (Coeficiente de Rendimento)
    # Método HTTP: GET
    # URL: http://localhost:8000/monitorias/
    # Suporta filtro: ?turma=1 (filtrar por turma específica)
    path('monitorias/', views.listar_monitorias, name='listar_monitorias'),
    
    # --- Editar Participação em Monitoria ---
    # Formulário para atualizar notas (AP1, AP2, CR) do aluno
    # AP1: Primeira Avaliação Parcial
    # AP2: Segunda Avaliação Parcial
    # CR: Coeficiente de Rendimento (calculado automaticamente)
    # Método HTTP: GET (formulário) / POST (submissão)
    # URL: http://localhost:8000/monitorias/5/editar/
    path('monitorias/<int:participacao_id>/editar/', views.editar_participacao, name='editar_participacao'),
    
    # ============================================================================
    # 7. MÓDULO DE PRESENÇAS - CONTROLE DE FREQUÊNCIA
    # ============================================================================
    
    # --- Listar Presenças ---
    # Exibe tabela com registro de presenças/ausências dos alunos
    # Inclui: aluno, turma, data, status (presente/ausente)
    # Método HTTP: GET
    # URL: http://localhost:8000/presencas/
    # Suporta filtros: ?turma=1&data=2025-10-18
    path('presencas/', views.listar_presencas, name='listar_presencas'),
    
    # --- Editar Presença ---
    # Permite atualizar o status de presença de um aluno
    # Método HTTP: GET (formulário) / POST (submissão)
    # URL: http://localhost:8000/presencas/10/editar/
    path('presencas/<int:presenca_id>/editar/', views.editar_presenca, name='editar_presenca'),
    
    # ============================================================================
    # 8. MÓDULO DE RELATÓRIOS - ANÁLISE E CONSULTORIA
    # ============================================================================
    
    # --- Página Principal de Relatórios ---
    # Menu central com links para diferentes tipos de relatórios
    # Método HTTP: GET
    # URL: http://localhost:8000/relatorios/
    path('relatorios/', views.listar_relatorios, name='listar_relatorios'),
    
    # --- Relatório de Desempenho ---
    # Análise do desempenho geral dos alunos nas monitorias
    # Mostra: notas (AP1, AP2), CR, média geral
    # Método HTTP: GET
    # URL: http://localhost:8000/relatorios/desempenho/
    path('relatorios/desempenho/', views.relatorio_desempenho, name='relatorio_desempenho'),
    
    # --- Relatório de Frequência ---
    # Análise da frequência/assiduidade dos alunos
    # Mostra: presença total, ausências, taxa de frequência
    # Método HTTP: GET
    # URL: http://localhost:8000/relatorios/frequencia/
    path('relatorios/frequencia/', views.relatorio_frequencia, name='relatorio_frequencia'),
    
    # --- Relatório de Inscrições ---
    # Análise das inscrições nas vagas de monitoria
    # Mostra: status das inscrições (pendente, aprovado, rejeitado)
    # Método HTTP: GET
    # URL: http://localhost:8000/relatorios/inscricoes/
    path('relatorios/inscricoes/', views.relatorio_inscricoes, name='relatorio_inscricoes'),
    
    # --- Relatório Geral ---
    # Consolidação de todos os dados do sistema em um único relatório
    # Mostra estatísticas gerais e resumidas
    # Método HTTP: GET
    # URL: http://localhost:8000/relatorios/geral/
    path('relatorios/geral/', views.relatorio_geral, name='relatorio_geral'),
    
    # ============================================================================
    # 9. MÓDULO DE PERFIL - DADOS PESSOAIS DO USUÁRIO
    # ============================================================================
    
    # --- Visualizar/Editar Perfil ---
    # Exibe dados pessoais do usuário logado
    # Permite editar: nome, email
    # Método HTTP: GET (exibir) / POST (atualizar)
    # URL: http://localhost:8000/perfil/
    path('perfil/', views.perfil, name='perfil'),
    
    # --- Alterar Senha ---
    # Endereço para processamento da alteração de senha
    # Requer validação de senha antiga
    # Método HTTP: POST
    # URL: http://localhost:8000/alterar-senha/
    path('alterar-senha/', views.alterar_senha, name='alterar_senha'),
    
    # ============================================================================
    # 10. MÓDULO LEGADO - VIEW SQL
    # ============================================================================
    
    # --- View SQL Legada ---
    # Endpoint legado que exibe dados brutos em formato SQL
    # Utilizado para debugging e análise de dados
    # Método HTTP: GET
    # URL: http://localhost:8000/sql/
    # Nota: Este é um endpoint de desenvolvimento, não deve ser exposto em produção
    path('sql/', views.sql_view, name='sql_view'),
]

# ================================================================================
# RESUMO DAS ROTAS
# ================================================================================
#
# ESTATÍSTICAS:
# - Total de rotas: 34
# - Operações CRUD: 16 (4 módulos completos)
# - Relatórios: 4
# - Páginas especiais: 3 (Dashboard, Perfil, SQL)
#
# PADRÃO DE NOMENCLATURA:
# - URLs nomeadas facilitam referência em templates e redirects
# - Estrutura hierárquica clara (módulo/ação)
# - Parâmetros inteiros com validação automática do Django
#
# ================================================================================
