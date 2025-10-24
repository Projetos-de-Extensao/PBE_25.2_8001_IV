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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# ================================================================================
# DOCUMENTAÇÃO SWAGGER (DRF-YASG)
# ================================================================================
api_patterns = [
    # Agrupa as rotas da API REST para reaproveitar no Swagger e no projeto
    path('api/', include('plataforma_Casa.api_urls')),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Plataforma CASA API",
        default_version='v1',
        description="Documentação interativa da API REST da Plataforma CASA.",
        terms_of_service="https://www.unifeso.edu.br/",
        contact=openapi.Contact(email="suporte@plataformacasa.com.br"),
        license=openapi.License(name="Uso interno Plataforma CASA"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=api_patterns,
)

# ================================================================================
# PADRÕES DE URL - URL PATTERNS
# ================================================================================

urlpatterns = [
    # ---------------------------------------------------------------------------
    # DOCUMENTAÇÃO DA API (SWAGGER UI)
    # ---------------------------------------------------------------------------
    path('restapi/', schema_view.with_ui('swagger', cache_timeout=0), name='api-docs'),
    re_path(r'^restapi/schema(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='api-schema'),
    path('restapi/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='api-redoc'),
    
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

# Rotas da API REST (utilizadas pelo Swagger)
urlpatterns += api_patterns

# Servir arquivos de media em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
