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
SECRET_KEY = config('SECRET_KEY', default='django-insecure-)8e!dd5q@2&qwtt(v0qm4c2&^%t5p3kxi60x$^9(zh6att5qh8')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG deve ser False em produção
DEBUG = config('DEBUG', default=False, cast=bool)

# Permite múltiplos hosts separados por vírgula
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'plataforma_Casa',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve arquivos estáticos em produção
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'meuprojeto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'plataforma_Casa.context_processors.user_groups',  # Adiciona grupos do usuário
            ],
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

# Configurações de Segurança para Produção
# Estas configurações são ativadas apenas quando DEBUG=False

if not DEBUG:
    # Força redirecionamento HTTP para HTTPS
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    
    # Cookies de sessão apenas via HTTPS
    SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
    
    # Cookies CSRF apenas via HTTPS
    CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
    
    # Ativa HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = 31536000  # 1 ano
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Previne que o navegador detecte incorretamente o content type
    SECURE_CONTENT_TYPE_NOSNIFF = True
    
    # Ativa proteção XSS do navegador
    SECURE_BROWSER_XSS_FILTER = True
    
    # Previne que o site seja carregado em frames (clickjacking)
    X_FRAME_OPTIONS = 'DENY'
