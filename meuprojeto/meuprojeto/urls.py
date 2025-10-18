"""
================================================================================
CONFIGURAÇÃO DE URLS - PROJETO PLATAFORMA CASA
================================================================================

Este arquivo contém a configuração de roteamento de URLs para o projeto Django.
Define os padrões de URL que mapeiam requisições HTTP para as views apropriadas.

Documentação: https://docs.djangoproject.com/en/5.2/topics/http/urls/
================================================================================
"""

from django.contrib import admin
from django.urls import path, include

# ================================================================================
# PADRÕES DE URL - URL PATTERNS
# ================================================================================

urlpatterns = [
    # ---------------------------------------------------------------------------
    # ADMIN DO DJANGO
    # ---------------------------------------------------------------------------
    # Rota para acesso ao painel administrativo do Django
    # Acesso em: http://localhost:8000/admin/
    # Requer superusuário para autenticação
    path('admin/', admin.site.urls),
    
    # ---------------------------------------------------------------------------
    # ROTAS PRINCIPAIS DA APLICAÇÃO PLATAFORMA CASA
    # ---------------------------------------------------------------------------
    # Inclui todas as URLs definidas no arquivo urls.py da aplicação plataforma_Casa
    # Isso centraliza o roteamento da aplicação em um único lugar
    # As rotas são prefixadas com uma string vazia '', ou seja, começam na raiz
    # 
    # Exemplo de rotas incluídas:
    # - http://localhost:8000/              (dashboard)
    # - http://localhost:8000/usuarios/     (listar usuários)
    # - http://localhost:8000/alunos/       (listar alunos)
    # - http://localhost:8000/vagas/        (listar vagas)
    # - http://localhost:8000/turmas/       (listar turmas)
    # - http://localhost:8000/monitorias/   (listar monitorias)
    # - http://localhost:8000/presencas/    (listar presenças)
    # - http://localhost:8000/relatorios/   (listar relatórios)
    # - http://localhost:8000/perfil/       (perfil do usuário)
    # - http://localhost:8000/sql/          (view sql legado)
    path('', include('plataforma_Casa.urls')),
]
