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
        title="🏠 API Plataforma CASA - Sistema de Monitoria",
        default_version='v1.0',
        description="""
# Bem-vindo à API da Plataforma CASA! 🚀

## 📚 Sobre
API REST completa para gerenciamento de monitoria acadêmica, incluindo:
- Gestão de disciplinas, vagas e turmas
- Controle de inscrições e presenças
- Registro de horas e pagamentos
- Materiais de apoio
- Relatórios e estatísticas

## 🔑 Recursos Principais
### Para Professores
- Criar e gerenciar disciplinas
- Criar vagas de monitoria
- Selecionar coordenadores responsáveis

### Para Coordenadores
- Gerenciar vagas
- Selecionar professores para as disciplinas
- Aprovar inscrições e horas

### Para Alunos
- Inscrever-se em vagas
- Registrar horas de monitoria
- Acessar materiais de apoio

## 🛠️ Como Usar
1. Explore os endpoints abaixo organizados por categoria
2. Clique em um endpoint para ver detalhes
3. Use "Try it out" para testar diretamente na interface
4. Todos os endpoints suportam busca, filtros e ordenação

## 📊 Endpoints Disponíveis
- **Base**: Tipos de usuário, Cursos, Salas, Disciplinas
- **Usuários**: Funcionários, Alunos
- **Acadêmico**: Vagas, Turmas, Inscrições
- **Controle**: Presenças, Horas, Pagamentos
- **Conteúdo**: Materiais de Apoio, Documentos
- **Análise**: Estatísticas do Sistema

---
**Suporte**: suporte@plataformacasa.com.br  
**Documentação**: [API Guide](https://github.com/Projetos-de-Extensao/PBE_25.2_8001_IV)
        """,
        terms_of_service="https://www.unifeso.edu.br/",
        contact=openapi.Contact(
            name="Equipe Plataforma CASA",
            email="suporte@plataformacasa.com.br",
            url="https://www.unifeso.edu.br"
        ),
        license=openapi.License(
            name="MIT License",
            url="https://opensource.org/licenses/MIT"
        ),
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
    # DOCUMENTAÇÃO DA API (SWAGGER UI E REDOC)
    # ---------------------------------------------------------------------------
    # Swagger UI - Documentação interativa
    path('restapi/', schema_view.with_ui('swagger', cache_timeout=0), name='api-docs'),
    
    # ReDoc - Documentação alternativa (mais bonita e limpa)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='api-redoc'),
    path('restapi/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='api-redoc-alt'),
    
    # Schema JSON/YAML
    re_path(r'^restapi/schema(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='api-schema'),
    
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
