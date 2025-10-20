#!/usr/bin/env python
"""
================================================================================
SCRIPT DE VERIFICAÇÃO - CONFIGURAÇÃO CSRF E SEGURANÇA
================================================================================

Descrição:
Script para verificar se as configurações de CSRF e segurança estão
corretas em desenvolvimento e produção.

Uso:
    python verify_csrf_config.py
    python verify_csrf_config.py --heroku seu-app-name

Autor: Equipe de Desenvolvimento - Plataforma Casa
Data: Outubro 2025

================================================================================
"""

import os
import sys
import django
from pathlib import Path

# Adicionar diretório do projeto ao path
project_dir = Path(__file__).parent / 'meuprojeto'
sys.path.insert(0, str(project_dir.parent))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto.settings')
django.setup()

from django.conf import settings

# ============================================================================
# CORES PARA OUTPUT
# ============================================================================
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_header(title):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'═' * 70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}  {title}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'═' * 70}{Colors.END}\n")

def print_check(condition, message):
    """Exibe um item de verificação"""
    if condition:
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")
        return True
    else:
        print(f"{Colors.RED}❌ {message}{Colors.END}")
        return False

def print_value(key, value, expected=None):
    """Exibe um valor de configuração"""
    if expected is not None and value != expected:
        status = f"{Colors.YELLOW}⚠️  (esperado: {expected}){Colors.END}"
    else:
        status = ""
    
    print(f"{Colors.CYAN}  {key}:{Colors.END} {Colors.BOLD}{value}{Colors.END} {status}")

# ============================================================================
# VERIFICAÇÕES
# ============================================================================

def verify_csrf_config():
    """Verifica configurações de CSRF"""
    print_header("🔍 VERIFICAÇÃO: Configurações CSRF")
    
    checks_passed = 0
    checks_total = 0
    
    # Verificação 1: CSRF_COOKIE_SECURE
    checks_total += 1
    print(f"\n{Colors.BOLD}1. CSRF_COOKIE_SECURE{Colors.END}")
    expected = not settings.DEBUG  # True em produção, False em dev
    if print_check(
        settings.CSRF_COOKIE_SECURE == expected,
        f"CSRF_COOKIE_SECURE = {settings.CSRF_COOKIE_SECURE} (esperado: {expected})"
    ):
        checks_passed += 1
    print_value("Valor", settings.CSRF_COOKIE_SECURE)
    
    # Verificação 2: CSRF_COOKIE_HTTPONLY
    checks_total += 1
    print(f"\n{Colors.BOLD}2. CSRF_COOKIE_HTTPONLY{Colors.END}")
    if print_check(
        settings.CSRF_COOKIE_HTTPONLY == False,
        f"CSRF_COOKIE_HTTPONLY = False (Django precisa ler o token)"
    ):
        checks_passed += 1
    print_value("Valor", settings.CSRF_COOKIE_HTTPONLY)
    
    # Verificação 3: CSRF_COOKIE_SAMESITE
    checks_total += 1
    print(f"\n{Colors.BOLD}3. CSRF_COOKIE_SAMESITE{Colors.END}")
    if print_check(
        hasattr(settings, 'CSRF_COOKIE_SAMESITE') and settings.CSRF_COOKIE_SAMESITE in ['Lax', 'Strict'],
        f"CSRF_COOKIE_SAMESITE configurado ({getattr(settings, 'CSRF_COOKIE_SAMESITE', 'N/A')})"
    ):
        checks_passed += 1
    print_value("Valor", getattr(settings, 'CSRF_COOKIE_SAMESITE', 'N/A'))
    
    # Verificação 4: CSRF_TRUSTED_ORIGINS
    checks_total += 1
    print(f"\n{Colors.BOLD}4. CSRF_TRUSTED_ORIGINS{Colors.END}")
    has_trusted_origins = hasattr(settings, 'CSRF_TRUSTED_ORIGINS') and len(settings.CSRF_TRUSTED_ORIGINS) > 0
    if print_check(has_trusted_origins, "CSRF_TRUSTED_ORIGINS configurado"):
        checks_passed += 1
    trusted_origins = getattr(settings, 'CSRF_TRUSTED_ORIGINS', [])
    for origin in trusted_origins:
        print_value("  Origem", origin)
    
    # Verificação 5: Middleware CSRF ativo
    checks_total += 1
    print(f"\n{Colors.BOLD}5. Middleware CSRF{Colors.END}")
    has_csrf_middleware = 'django.middleware.csrf.CsrfViewMiddleware' in settings.MIDDLEWARE
    if print_check(has_csrf_middleware, "CsrfViewMiddleware ativo"):
        checks_passed += 1
    
    return checks_passed, checks_total

def verify_security_config():
    """Verifica configurações de segurança geral"""
    print_header("🔒 VERIFICAÇÃO: Segurança Geral")
    
    checks_passed = 0
    checks_total = 0
    
    # Verificação 1: DEBUG
    checks_total += 1
    print(f"\n{Colors.BOLD}1. DEBUG Mode{Colors.END}")
    if print_check(settings.DEBUG == False, "DEBUG = False (esperado em produção)"):
        checks_passed += 1
    print_value("Valor", settings.DEBUG)
    
    # Verificação 2: SECRET_KEY
    checks_total += 1
    print(f"\n{Colors.BOLD}2. SECRET_KEY{Colors.END}")
    secret_is_safe = 'insecure' not in settings.SECRET_KEY.lower()
    if print_check(secret_is_safe, "SECRET_KEY não é o padrão inseguro"):
        checks_passed += 1
    print_value("Comprimento", len(settings.SECRET_KEY))
    
    # Verificação 3: ALLOWED_HOSTS
    checks_total += 1
    print(f"\n{Colors.BOLD}3. ALLOWED_HOSTS{Colors.END}")
    has_hosts = len(settings.ALLOWED_HOSTS) > 0
    if print_check(has_hosts, "ALLOWED_HOSTS configurado"):
        checks_passed += 1
    for host in settings.ALLOWED_HOSTS:
        print_value("  Host", host)
    
    # Verificação 4: SECURE_SSL_REDIRECT
    checks_total += 1
    print(f"\n{Colors.BOLD}4. SECURE_SSL_REDIRECT{Colors.END}")
    expected_ssl = not settings.DEBUG
    if print_check(
        settings.SECURE_SSL_REDIRECT == expected_ssl,
        f"SECURE_SSL_REDIRECT = {settings.SECURE_SSL_REDIRECT}"
    ):
        checks_passed += 1
    print_value("Valor", settings.SECURE_SSL_REDIRECT)
    
    # Verificação 5: SECURE_PROXY_SSL_HEADER
    checks_total += 1
    print(f"\n{Colors.BOLD}5. SECURE_PROXY_SSL_HEADER (Heroku)${Colors.END}")
    has_proxy_header = hasattr(settings, 'SECURE_PROXY_SSL_HEADER') and settings.SECURE_PROXY_SSL_HEADER is not None
    if print_check(has_proxy_header, "SECURE_PROXY_SSL_HEADER configurado"):
        checks_passed += 1
    if has_proxy_header:
        print_value("Valor", str(settings.SECURE_PROXY_SSL_HEADER))
    
    # Verificação 6: SESSION_COOKIE_SECURE
    checks_total += 1
    print(f"\n{Colors.BOLD}6. SESSION_COOKIE_SECURE{Colors.END}")
    expected_session = not settings.DEBUG
    if print_check(
        settings.SESSION_COOKIE_SECURE == expected_session,
        f"SESSION_COOKIE_SECURE = {settings.SESSION_COOKIE_SECURE}"
    ):
        checks_passed += 1
    print_value("Valor", settings.SESSION_COOKIE_SECURE)
    
    # Verificação 7: X_FRAME_OPTIONS
    checks_total += 1
    print(f"\n{Colors.BOLD}7. X_FRAME_OPTIONS (Clickjacking)${Colors.END}")
    if print_check(
        settings.X_FRAME_OPTIONS == 'DENY',
        "X_FRAME_OPTIONS = 'DENY'"
    ):
        checks_passed += 1
    print_value("Valor", settings.X_FRAME_OPTIONS)
    
    return checks_passed, checks_total

def verify_template_context():
    """Verifica context processors"""
    print_header("📝 VERIFICAÇÃO: Context Processors")
    
    checks_passed = 0
    checks_total = 0
    
    context_processors = settings.TEMPLATES[0]['OPTIONS'].get('context_processors', [])
    
    # Verificação 1: CSRF context processor
    checks_total += 1
    csrf_processor = 'django.template.context_processors.csrf'
    has_csrf = csrf_processor in context_processors
    if print_check(has_csrf, "CSRF context processor ativo"):
        checks_passed += 1
    
    # Verificação 2: request context processor
    checks_total += 1
    request_processor = 'django.template.context_processors.request'
    has_request = request_processor in context_processors
    if print_check(has_request, "Request context processor ativo"):
        checks_passed += 1
    
    print(f"\n{Colors.BOLD}Context Processors Ativos:{Colors.END}")
    for processor in context_processors:
        print_value("  ", processor)
    
    return checks_passed, checks_total

def main():
    """Função principal"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║    VERIFICAÇÃO: Configuração CSRF e Segurança                  ║")
    print("║    Plataforma Casa - Monitorias                                ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    # Environment
    print(f"\n{Colors.BOLD}Environment:{Colors.END}")
    print_value("DEBUG", settings.DEBUG)
    print_value("Environment Type", "Produção (Heroku)" if 'herokuapp.com' in str(settings.ALLOWED_HOSTS) else "Desenvolvimento")
    
    # Executar verificações
    csrf_passed, csrf_total = verify_csrf_config()
    security_passed, security_total = verify_security_config()
    template_passed, template_total = verify_template_context()
    
    # Resumo
    total_checks = csrf_total + security_total + template_total
    total_passed = csrf_passed + security_passed + template_passed
    
    print_header("📊 RESUMO")
    print(f"Total de verificações: {Colors.BOLD}{total_checks}{Colors.END}")
    print(f"Aprovadas: {Colors.GREEN}{Colors.BOLD}{total_passed}{Colors.END}")
    print(f"Falhadas: {Colors.RED}{Colors.BOLD}{total_checks - total_passed}{Colors.END}")
    
    percentage = (total_passed / total_checks) * 100 if total_checks > 0 else 0
    
    if percentage == 100:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Todas as verificações passaram!{Colors.END}")
        status = 0
    elif percentage >= 80:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  {percentage:.0f}% das verificações passaram{Colors.END}")
        status = 1
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ Apenas {percentage:.0f}% das verificações passaram{Colors.END}")
        status = 2
    
    print(f"\n{Colors.BLUE}{'═' * 70}{Colors.END}\n")
    
    return status

if __name__ == '__main__':
    sys.exit(main())
