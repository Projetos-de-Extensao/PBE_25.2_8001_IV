#!/usr/bin/env python3
"""
Script de Inicialização Rápida - Plataforma CASA
Versão sem HTTPS para desenvolvimento local
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

class Cores:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_sucesso(msg):
    print(f"{Cores.GREEN}✓{Cores.END} {msg}")

def print_erro(msg):
    print(f"{Cores.RED}✗{Cores.END} {msg}")

def print_info(msg):
    print(f"{Cores.BLUE}ℹ{Cores.END} {msg}")

def print_titulo(msg):
    print(f"\n{Cores.BOLD}{Cores.CYAN}{'─' * 80}{Cores.END}")
    print(f"{Cores.BOLD}{Cores.CYAN}{msg}{Cores.END}")
    print(f"{Cores.BOLD}{Cores.CYAN}{'─' * 80}{Cores.END}\n")

def main():
    """Inicialização rápida do sistema"""
    
    # Banner
    print(f"\n{Cores.BOLD}{Cores.CYAN}")
    print("╔═══════════════════════════════════════════════════════════════════════════════╗")
    print("║                  🚀 PLATAFORMA CASA - INICIALIZAÇÃO RÁPIDA                   ║")
    print("║                        Sistema de Gestão de Monitorias                       ║")
    print("╚═══════════════════════════════════════════════════════════════════════════════╝")
    print(f"{Cores.END}\n")
    
    # Caminhos
    projeto_raiz = Path(__file__).parent
    meuprojeto = projeto_raiz / "meuprojeto"
    venv_path = projeto_raiz / ".venv"
    
    # Determinar Python do venv
    if platform.system() == "Windows":
        python_venv = str(venv_path / "Scripts" / "python.exe")
        pip_venv = str(venv_path / "Scripts" / "pip")
    else:
        python_venv = str(venv_path / "bin" / "python")
        pip_venv = str(venv_path / "bin" / "pip")
    
    manage_py = meuprojeto / "manage.py"
    
    # Verificações
    print_titulo("VERIFICANDO AMBIENTE")
    
    if not venv_path.exists():
        print_erro("Ambiente virtual não encontrado!")
        print_info("Criando ambiente virtual...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        print_sucesso("Ambiente virtual criado")
    else:
        print_sucesso("Ambiente virtual encontrado")
    
    if not manage_py.exists():
        print_erro(f"manage.py não encontrado em {meuprojeto}")
        sys.exit(1)
    
    print_sucesso(f"Python {sys.version_info.major}.{sys.version_info.minor}")
    print_sucesso(f"Sistema: {platform.system()}")
    
    # Instalar dependências básicas
    print_titulo("INSTALANDO/VERIFICANDO DEPENDÊNCIAS")
    
    pacotes_essenciais = [
        "Django>=5.0",
        "djangorestframework>=3.15",
        "django-cors-headers>=4.0",
        "drf-yasg>=1.21",
        "Pillow",
        "python-dotenv"
    ]
    
    print_info("Instalando pacotes essenciais...")
    try:
        subprocess.run(
            [pip_venv, "install", "-q"] + pacotes_essenciais,
            timeout=120,
            check=True
        )
        print_sucesso("Dependências instaladas")
    except subprocess.TimeoutExpired:
        print_erro("Timeout ao instalar dependências")
    except Exception as e:
        print_erro(f"Erro ao instalar: {e}")
    
    # Migrações
    print_titulo("APLICANDO MIGRAÇÕES")
    
    try:
        print_info("Criando migrações...")
        subprocess.run(
            [python_venv, str(manage_py), "makemigrations"],
            cwd=str(meuprojeto),
            timeout=30
        )
        
        print_info("Aplicando migrações...")
        subprocess.run(
            [python_venv, str(manage_py), "migrate"],
            cwd=str(meuprojeto),
            timeout=60,
            check=True
        )
        print_sucesso("Migrações aplicadas")
    except Exception as e:
        print_erro(f"Erro nas migrações: {e}")
    
    # Coletar arquivos estáticos
    print_titulo("COLETANDO ARQUIVOS ESTÁTICOS")
    
    try:
        subprocess.run(
            [python_venv, str(manage_py), "collectstatic", "--noinput"],
            cwd=str(meuprojeto),
            timeout=30,
            capture_output=True
        )
        print_sucesso("Arquivos estáticos coletados")
    except:
        print_info("Pulando coleta de estáticos (não crítico)")
    
    # Criar superusuário se necessário
    print_titulo("VERIFICANDO USUÁRIO ADMIN")
    
    script_criar_admin = """
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@casa.com', 'admin')
    print('✓ Superusuário criado: admin / admin')
else:
    print('✓ Superusuário já existe')
"""
    
    try:
        subprocess.run(
            [python_venv, str(manage_py), "shell", "-c", script_criar_admin],
            cwd=str(meuprojeto),
            timeout=10
        )
    except:
        print_info("Admin pode já existir ou não foi possível criar")
    
    # Iniciar servidor
    print_titulo("INICIANDO SERVIDOR")
    
    print_sucesso("Sistema pronto!")
    print(f"\n{Cores.CYAN}📍 URLs Disponíveis:{Cores.END}")
    print(f"   • API Root:       {Cores.BOLD}http://localhost:8000/api/{Cores.END}")
    print(f"   • Swagger:        {Cores.BOLD}http://localhost:8000/restapi/{Cores.END}")
    print(f"   • ReDoc:          {Cores.BOLD}http://localhost:8000/restapi/redoc/{Cores.END}")
    print(f"   • Admin Django:   {Cores.BOLD}http://localhost:8000/admin/{Cores.END}")
    
    print(f"\n{Cores.CYAN}🔑 Credenciais:{Cores.END}")
    print(f"   • Admin:          {Cores.BOLD}admin / admin{Cores.END}")
    
    print(f"\n{Cores.YELLOW}Pressione CTRL+C para parar o servidor{Cores.END}\n")
    
    try:
        subprocess.run(
            [python_venv, str(manage_py), "runserver", "0.0.0.0:8000"],
            cwd=str(meuprojeto)
        )
    except KeyboardInterrupt:
        print(f"\n\n{Cores.GREEN}✓{Cores.END} Servidor parado com sucesso")
        print(f"{Cores.CYAN}Até logo!{Cores.END}\n")

if __name__ == "__main__":
    main()
