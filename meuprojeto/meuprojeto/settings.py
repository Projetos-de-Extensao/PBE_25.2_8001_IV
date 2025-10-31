from pathlib import Path
import os
import dj_database_url
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Utiliza variável de ambiente ou fallback para desenvolvimento local
SECRET_KEY = config('SECRET_KEY', default='django-insecure-CHANGE-THIS-IN-PRODUCTION-f820a0a16535-secure-key-2025')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG deve ser False em produção (só True localmente para desenvolvimento)
DEBUG = config('DEBUG', default=False, cast=bool)

# Permite múltiplos hosts separados por vírgula
# Em produção (Heroku), inclua o domínio: plataformacasa-f820a0a16535.herokuapp.com
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# ============================================================================
# CONFIGURAÇÃO DE CORS E HOSTS CONFIÁVEIS - PRODUÇÃO
# ============================================================================
# Para Heroku em produção, adicionar na variável de ambiente:
# ALLOWED_HOSTS=localhost,127.0.0.1,plataformacasa-a2a3d2abfd5e.herokuapp.com
# 
# Ou definir aqui diretamente (menos recomendado por segurança):
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='https://plataformacasa-a2a3d2abfd5e.herokuapp.com',
    cast=Csv()
)

# Configurações de CORS - controlam quais origens podem acessar a API
DEFAULT_CORS_ORIGINS = 'http://localhost:3000,http://127.0.0.1:3000'
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default=DEFAULT_CORS_ORIGINS,
    cast=Csv()
)
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=DEBUG, cast=bool)
CORS_ALLOW_CREDENTIALS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'drf_yasg',
    'plataforma_Casa',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'meuprojeto.urls'

# Configuração de templates com cache desabilitado em DEBUG mode
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': DEBUG,  # APP_DIRS só quando DEBUG=True e sem loaders customizado
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'plataforma_Casa.context_processors.user_groups',  # Adiciona grupos do usuário
            ],
            # Desabilita cache de templates em DEBUG mode para forçar reload
            # Só define loaders quando APP_DIRS=False (produção)
            **(
                {} if DEBUG else {
                    'loaders': [
                        ('django.template.loaders.cached.Loader', [
                            'django.template.loaders.app_directories.Loader',
                            'django.template.loaders.filesystem.Loader',
                        ]),
                    ],
                }
            ),
        },
    },
]

WSGI_APPLICATION = 'meuprojeto.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Configuração do banco de dados com suporte a PostgreSQL (Heroku) e SQLite (desenvolvimento)
# A Heroku define automaticamente a variável DATABASE_URL com as credenciais do PostgreSQL
database_url = config('DATABASE_URL', default=None)

if database_url:
    # Produção: usa PostgreSQL via DATABASE_URL (Heroku)
    DATABASES = {
        'default': dj_database_url.config(
            default=database_url,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Desenvolvimento: usa SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

# Authentication Backends - permite login com email ou username
AUTHENTICATION_BACKENDS = [
    'plataforma_Casa.backends.EmailOrUsernameModelBackend',  # Backend customizado
    'django.contrib.auth.backends.ModelBackend',  # Backend padrão (fallback)
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'

# Diretório onde collectstatic irá coletar todos os arquivos estáticos
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Diretórios adicionais onde Django procura por arquivos estáticos
STATICFILES_DIRS = []

# Configuração do WhiteNoise para compressão e cache de arquivos estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    # Padrão mais aberto para facilitar visualização via Swagger em ambiente interno
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    # Faz o DRF gerar esquema OpenAPI automaticamente
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.openapi.AutoSchema',
    # Paginação configurada
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    # Filtros padrão
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    # Formato de data/hora mais legível
    'DATETIME_FORMAT': '%d/%m/%Y %H:%M:%S',
    'DATE_FORMAT': '%d/%m/%Y',
    'TIME_FORMAT': '%H:%M:%S',
}

SWAGGER_SETTINGS = {
    # Permite testar endpoints autenticados usando sessão do Django
    'USE_SESSION_AUTH': True,
    'LOGIN_URL': 'login',
    'LOGOUT_URL': 'logout',
    
    # Expansão padrão - 'none' deixa tudo colapsado inicialmente (melhor UX)
    'DOC_EXPANSION': 'none',
    
    # Exibe exemplos reais em vez de estruturas vazias
    'DEFAULT_MODEL_RENDERING': 'example',
    
    # Profundidade dos modelos aninhados
    'DEFAULT_MODEL_DEPTH': 2,
    
    # Recarrega o schema quando as credenciais mudarem
    'REFETCH_SCHEMA_WITH_AUTH': True,
    
    # Mostra operationId para facilitar cópia em integrações futuras
    'DISPLAY_OPERATION_ID': False,
    
    # Configuração de filtros
    'OPERATIONS_SORTER': 'alpha',  # Ordena alfabeticamente
    'TAGS_SORTER': 'alpha',         # Ordena tags alfabeticamente
    
    # Deep linking - permite compartilhar links diretos para endpoints
    'DEEP_LINKING': True,
    
    # Mostra extensões da spec OpenAPI
    'SHOW_EXTENSIONS': True,
    
    # Mostra common parameters
    'SHOW_COMMON_EXTENSIONS': True,
    
    # Validação de requisições
    'VALIDATOR_URL': None,  # Desabilita validação externa
    
    # JSON Editor
    'JSON_EDITOR': True,
    
    # Configurações visuais
    'DEFAULT_AUTO_SCHEMA_CLASS': 'drf_yasg.inspectors.SwaggerAutoSchema',
    
    # Permite testar tanto autenticação básica quanto Bearer token
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic',
            'description': 'Autenticação básica HTTP'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Token de autenticação. Formato: Bearer {token}'
        },
    },
    
    # Configurações de persistência
    'PERSIST_AUTH': True,
    
    # Suporte a CORS
    'SUPPORTED_SUBMIT_METHODS': [
        'get',
        'post',
        'put',
        'delete',
        'patch',
        'options'
    ],
}

REDOC_SETTINGS = {
    # Otimiza o carregamento e navegação da documentação alternativa (Redoc)
    'LAZY_RENDERING': False,  # Renderiza tudo de uma vez (melhor para navegação)
    
    # Usa scrollbar nativo do navegador
    'NATIVE_SCROLLBARS': True,
    
    # Exibe caminho no meio da tela
    'PATH_IN_MIDDLE': True,
    
    # Expande respostas por padrão
    'EXPAND_RESPONSES': 'all',
    
    # Expande navegação lateral
    'EXPAND_DEFAULT_SERVER_VARIABLES': True,
    
    # Configurações visuais
    'HIDE_HOSTNAME': False,
    'HIDE_LOADING': False,
    
    # Menu lateral fixo
    'MENU_TOGGLE': True,
    
    # Mostra logo se configurado
    'NO_AUTO_AUTH': False,
    
    # Configurações de requisição
    'REQUIRED_PROPS_FIRST': True,
    
    # Scrollbar position
    'SCROLL_Y_OFFSET': 0,
    
    # Theme customization (você pode adicionar depois)
    'THEME': {
        'colors': {
            'primary': {
                'main': '#2196F3'  # Azul Material
            }
        },
        'typography': {
            'fontSize': '16px',
            'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            'headings': {
                'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                'fontWeight': '600'
            }
        },
        'sidebar': {
            'backgroundColor': '#fafafa',
            'textColor': '#333'
        }
    }
}

# ============================================================================
# CONFIGURAÇÕES DE SEGURANÇA PARA PRODUÇÃO
# ============================================================================
# Ativadas apenas quando DEBUG=False (em produção no Heroku)

# ============================================================================
# CONFIGURAÇÕES DE SEGURANÇA SEMPRE ATIVAS
# ============================================================================
# Essas configurações são essenciais mesmo em desenvolvimento

# Configurações de HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000 if not DEBUG else 0, cast=int)  # 1 ano em prod
SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=not DEBUG, cast=bool)
SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=not DEBUG, cast=bool)

# Proteções de conteúdo
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

if not DEBUG:
    # ---------- REDIRECIONAMENTO E TRANSPORTE ----------
    # Força redirecionamento HTTP para HTTPS
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    
    # ⚠️ IMPORTANTE: Em Heroku com proxy reverso, usar X-Forwarded-Proto
    # Evita redirecionamento infinito HTTP->HTTPS
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # ---------- COOKIES SEGUROS ----------
    # Cookies de sessão apenas via HTTPS
    SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
    
    # Cookies CSRF apenas via HTTPS
    CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
    
    # ⚠️ IMPORTANTE: HttpOnly previne acesso via JavaScript
    CSRF_COOKIE_HTTPONLY = False  # Deve ser False para Django carregar o token
    SESSION_COOKIE_HTTPONLY = True  # Protege o cookie de sessão
    
    # SameSite cookie attribute (proteção contra CSRF)
    CSRF_COOKIE_SAMESITE = 'Lax'  # 'Lax' é mais permissivo que 'Strict'
    SESSION_COOKIE_SAMESITE = 'Lax'

# ============================================================================
# CONFIGURAÇÕES CSRF (CROSS-SITE REQUEST FORGERY)
# ============================================================================
# Essas configurações funcionam em DEV e PRODUÇÃO

# Tempo de vida do token CSRF (em segundos)
# 31449600 = 1 ano
CSRF_COOKIE_AGE = config('CSRF_COOKIE_AGE', default=31449600, cast=int)

# Usar valor seguro para nome do campo de cookie CSRF
CSRF_COOKIE_NAME = 'csrftoken'

# Nome do campo do formulário para token CSRF
CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'

# Verificador de token CSRF (importante para AJAX e POST)
# CSRF_FAILURE_VIEW = 'plataforma_Casa.views.csrf_failure_view'  # View customizada (opcional)
