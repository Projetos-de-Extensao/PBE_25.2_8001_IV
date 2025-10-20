#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║            INICIALIZADOR DO SISTEMA - PLATAFORMA CASA                      ║
║                                                                            ║
║                    Sistema Completo de Gestão de Monitorias                ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

Este script automatiza COMPLETAMENTE a inicialização do sistema:

- Verifica Python e dependências
- Configura ambiente virtual
- Instala pacotes necessários
- Aplica migrações do banco
- Cria usuários de teste
- Popula dados iniciais
- Inicia o servidor Django

Autor: Anderson
Data: 19 de outubro de 2025
Versão: 1.0
Status:  Pronto para produção
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path
from datetime import datetime

# ═════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÕES DE CORES PARA TERMINAL
# ═════════════════════════════════════════════════════════════════════════════

class Cores:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# ═════════════════════════════════════════════════════════════════════════════
# CLASSE PRINCIPAL
# ═════════════════════════════════════════════════════════════════════════════

class InicializadorSistema:
    """
    Classe principal que gerencia toda a inicialização do sistema.
    """
    
    def __init__(self):
        self.projeto_raiz = Path(__file__).parent
        self.meuprojeto = self.projeto_raiz / "meuprojeto"
        self.venv_path = self.projeto_raiz / ".venv"
        self.python_venv = self._get_python_venv()
        self.logs = []
        self.erros = []
    
    def _get_python_venv(self):
        """Retorna o caminho do Python do venv"""
        if platform.system() == "Windows":
            return str(self.venv_path / "Scripts" / "python.exe")
        else:
            return str(self.venv_path / "bin" / "python")
        
    # ═════════════════════════════════════════════════════════════════════════
    # MÉTODOS DE FORMATAÇÃO
    # ═════════════════════════════════════════════════════════════════════════
    
    def print_titulo(self, texto):
        """Imprime um título destacado"""
        print(f"\n{Cores.BOLD}{Cores.CYAN}{'='*80}{Cores.END}")
        print(f"{Cores.BOLD}{Cores.CYAN}  {texto}{Cores.END}")
        print(f"{Cores.BOLD}{Cores.CYAN}{'='*80}{Cores.END}\n")
    
    def print_sucesso(self, texto):
        """Imprime mensagem de sucesso"""
        print(f"{Cores.GREEN}[OK] {texto}{Cores.END}")
        self.logs.append(f"[OK] {texto}")
    
    def print_erro(self, texto):
        """Imprime mensagem de erro"""
        print(f"{Cores.RED}[ERRO] {texto}{Cores.END}")
        self.erros.append(f"[ERRO] {texto}")
    
    def print_info(self, texto):
        """Imprime informação"""
        print(f"{Cores.BLUE}[INFO] {texto}{Cores.END}")
        self.logs.append(f"[INFO] {texto}")
    
    def print_aviso(self, texto):
        """Imprime aviso"""
        print(f"{Cores.YELLOW}[AVISO] {texto}{Cores.END}")
        self.logs.append(f"[AVISO] {texto}")
    
    # ═════════════════════════════════════════════════════════════════════════
    # 1. VERIFICAÇÃO DE PRÉ-REQUISITOS
    # ═════════════════════════════════════════════════════════════════════════
    
    def verificar_prerequisites(self):
        """Verifica se todos os pré-requisitos estão atendidos"""
        self.print_titulo("1. VERIFICANDO PRÉ-REQUISITOS")
        
        # Verificar Python
        versao_python = f"{sys.version_info.major}.{sys.version_info.minor}"
        if sys.version_info >= (3, 10):
            self.print_sucesso(f"Python {versao_python} ✓")
        else:
            self.print_erro(f"Python {versao_python} ✗ (Requer 3.10+)")
            return False
        
        # Verificar Sistema Operacional
        so = platform.system()
        self.print_info(f"Sistema Operacional: {so}")
        
        # Verificar pasta do projeto
        if self.meuprojeto.exists():
            self.print_sucesso(f"Pasta do projeto encontrada: {self.meuprojeto}")
        else:
            self.print_erro(f"Pasta do projeto não encontrada: {self.meuprojeto}")
            return False
        
        # Verificar manage.py
        manage_py = self.meuprojeto / "manage.py"
        if manage_py.exists():
            self.print_sucesso(f"manage.py encontrado ✓")
        else:
            self.print_erro(f"manage.py não encontrado ✗")
            return False
        
        # Verificar requirements.txt
        requirements = self.projeto_raiz / "requirements.txt"
        if requirements.exists():
            self.print_sucesso(f"requirements.txt encontrado ✓")
        else:
            self.print_aviso(f"requirements.txt não encontrado - tentando instalar basics")
        
        return True
    
    # ═════════════════════════════════════════════════════════════════════════
    # 2. CONFIGURAR AMBIENTE VIRTUAL
    # ═════════════════════════════════════════════════════════════════════════
    
    def setup_venv(self):
        """Configura e ativa ambiente virtual se necessário"""
        self.print_titulo("2. CONFIGURANDO AMBIENTE VIRTUAL")
        
        venv_path = self.projeto_raiz / ".venv"
        
        if venv_path.exists():
            self.print_sucesso("Ambiente virtual já existe ✓")
        else:
            self.print_info("Criando ambiente virtual...")
            try:
                subprocess.run(
                    [sys.executable, "-m", "venv", str(venv_path)],
                    check=True,
                    cwd=str(self.projeto_raiz)
                )
                self.print_sucesso("Ambiente virtual criado ✓")
            except subprocess.CalledProcessError as e:
                self.print_erro(f"Erro ao criar venv: {e}")
                return False
        
        # Verificar se pip precisa de atualização
        self.print_info("Atualizando pip...")
        try:
            if platform.system() == "Windows":
                pip_cmd = str(venv_path / "Scripts" / "pip")
            else:
                pip_cmd = str(venv_path / "bin" / "pip")
            
            subprocess.run(
                [pip_cmd, "install", "--upgrade", "pip"],
                check=True,
                capture_output=True
            )
            self.print_sucesso("pip atualizado ✓")
        except subprocess.CalledProcessError:
            self.print_aviso("Não foi possível atualizar pip (continuando...)")
        
        return True
    
    # ═════════════════════════════════════════════════════════════════════════
    # 3. INSTALAR DEPENDÊNCIAS
    # ═════════════════════════════════════════════════════════════════════════
    
    def instalar_dependencias(self):
        """Instala todas as dependências necessárias"""
        self.print_titulo("3. INSTALANDO DEPENDÊNCIAS")
        
        # Dependências mínimas
        dependencias = [
            "Django==5.2.7",
            "python-dotenv",
            "Pillow",
            "openpyxl",
            "reportlab",
            "PyPDF2",
        ]
        
        self.print_info("Instalando pacotes necessários...")
        
        for pacote in dependencias:
            try:
                self.print_info(f"Instalando {pacote}...")
                subprocess.run(
                    [self.python_venv, "-m", "pip", "install", pacote],
                    check=True,
                    capture_output=True,
                    timeout=60
                )
                self.print_sucesso(f"{pacote} instalado ✓")
            except subprocess.CalledProcessError:
                self.print_aviso(f"Erro ao instalar {pacote} (continuando...)")
            except subprocess.TimeoutExpired:
                self.print_aviso(f"Timeout ao instalar {pacote} (continuando...)")
        
        return True
    
    # ═════════════════════════════════════════════════════════════════════════
    # 4. APLICAR MIGRAÇÕES
    # ═════════════════════════════════════════════════════════════════════════
    
    def aplicar_migracoes(self):
        """Aplica as migrações do banco de dados"""
        self.print_titulo("4. APLICANDO MIGRAÇÕES DO BANCO DE DADOS")
        
        manage_py = self.meuprojeto / "manage.py"
        
        # Check migrations
        self.print_info("Verificando migrações...")
        try:
            resultado = subprocess.run(
                [self.python_venv, str(manage_py), "makemigrations"],
                cwd=str(self.meuprojeto),
                capture_output=True,
                text=True,
                timeout=30
            )
            if "No changes detected" in resultado.stdout or resultado.returncode == 0:
                self.print_sucesso("Migrações verificadas ✓")
            else:
                self.print_info(resultado.stdout)
        except subprocess.TimeoutExpired:
            self.print_aviso("Timeout ao verificar migrações")
        except Exception as e:
            self.print_aviso(f"Erro ao verificar migrações: {e}")
        
        # Apply migrations
        self.print_info("Aplicando migrações...")
        try:
            resultado = subprocess.run(
                [self.python_venv, str(manage_py), "migrate"],
                cwd=str(self.meuprojeto),
                capture_output=True,
                text=True,
                timeout=60
            )
            if resultado.returncode == 0:
                self.print_sucesso("Migrações aplicadas ✓")
            else:
                self.print_aviso(f"Resultado: {resultado.stdout}")
        except subprocess.TimeoutExpired:
            self.print_erro("Timeout ao aplicar migrações")
            return False
        except Exception as e:
            self.print_erro(f"Erro ao aplicar migrações: {e}")
            return False
        
        return True
    
    # ═════════════════════════════════════════════════════════════════════════
    # 5. CRIAR USUÁRIOS DE TESTE
    # ═════════════════════════════════════════════════════════════════════════
    
    def criar_usuarios_teste(self):
        """Cria usuários de teste para demonstração"""
        self.print_titulo("5. CRIANDO USUÁRIOS DE TESTE")
        
        manage_py = self.meuprojeto / "manage.py"
        
        # Script inline para criar usuários
        script = """
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto.settings')
django.setup()

from django.contrib.auth.models import User, Group

usuarios = [
    {
        'username': 'admin',
        'email': 'admin@casa.com',
        'password': 'admin',
        'is_staff': True,
        'is_superuser': True,
        'grupos': []
    },
    {
        'username': 'aluno.teste',
        'email': 'aluno.teste@casa.com',
        'password': 'aluno123',
        'grupos': ['Aluno']
    },
    {
        'username': 'monitor.teste',
        'email': 'monitor.teste@casa.com',
        'password': 'monitor123',
        'grupos': ['Monitor', 'Aluno']
    },
    {
        'username': 'professor.teste',
        'email': 'professor.teste@casa.com',
        'password': 'professor123',
        'grupos': ['Professor']
    },
]

for user_data in usuarios:
    grupos = user_data.pop('grupos', [])
    
    user, criado = User.objects.update_or_create(
        username=user_data['username'],
        defaults={
            'email': user_data['email'],
            'is_staff': user_data.get('is_staff', False),
            'is_superuser': user_data.get('is_superuser', False),
        }
    )
    
    # Atualizar senha
    user.set_password(user_data['password'])
    user.save()
    
    # Atribuir grupos
    for nome_grupo in grupos:
        try:
            grupo = Group.objects.get(name=nome_grupo)
            user.groups.add(grupo)
        except Group.DoesNotExist:
            pass
    
    status = "criado" if criado else "atualizado"
    print(f"[OK] Usuário '{user_data['username']}' {status}")

print("[OK] Todos os usuários de teste configurados!")
"""
        
        try:
            resultado = subprocess.run(
                [self.python_venv, str(manage_py), "shell"],
                input=script,
                cwd=str(self.meuprojeto),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if resultado.returncode == 0:
                self.print_sucesso("Usuários de teste criados ✓")
                self.print_info("Credenciais disponíveis:")
                self.print_info("  Aluno:     aluno.teste / aluno123")
                self.print_info("  Monitor:   monitor.teste / monitor123")
                self.print_info("  Professor: professor.teste / professor123")
                self.print_info("  Admin:     admin / admin")
            else:
                self.print_aviso(f"Aviso ao criar usuários: {resultado.stderr}")
        except subprocess.TimeoutExpired:
            self.print_aviso("Timeout ao criar usuários")
        except Exception as e:
            self.print_aviso(f"Erro ao criar usuários: {e}")
        
        return True
    
    # ═════════════════════════════════════════════════════════════════════════
    # 6. EXECUTAR TESTES BÁSICOS
    # ═════════════════════════════════════════════════════════════════════════
    
    def executar_testes_basicos(self):
        """Executa testes básicos do Django"""
        self.print_titulo("6. EXECUTANDO TESTES BÁSICOS")
        
        manage_py = self.meuprojeto / "manage.py"
        
        # Django check
        self.print_info("Executando Django check...")
        try:
            resultado = subprocess.run(
                [self.python_venv, str(manage_py), "check"],
                cwd=str(self.meuprojeto),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if resultado.returncode == 0:
                self.print_sucesso("Nenhum problema encontrado ✓")
            else:
                self.print_aviso(f"Avisos: {resultado.stdout}")
        except subprocess.TimeoutExpired:
            self.print_aviso("Timeout ao executar check")
        except Exception as e:
            self.print_aviso(f"Erro ao executar check: {e}")
        
        return True
    
    # ═════════════════════════════════════════════════════════════════════════
    # 7. INICIAR SERVIDOR
    # ═════════════════════════════════════════════════════════════════════════
    
    def iniciar_servidor(self):
        """Inicia o servidor Django"""
        self.print_titulo("7. INICIANDO SERVIDOR DJANGO")
        
        manage_py = self.meuprojeto / "manage.py"
        
        self.print_sucesso("Sistema inicializado com sucesso!")
        self.print_info("\nAcesse o sistema em:")
        self.print_info(f"  Login:     http://localhost:8000/login/")
        self.print_info(f"  Admin:     http://localhost:8000/admin/")
        self.print_info(f"  Dashboard: http://localhost:8000/dashboard/")
        
        self.print_info("\nCredenciais de teste:")
        self.print_info("  Aluno:     aluno.teste / aluno123")
        self.print_info("  Monitor:   monitor.teste / monitor123")
        self.print_info("  Professor: professor.teste / professor123")
        self.print_info("  Admin:     admin / admin")
        
        self.print_info("\nPressione CTRL+C para parar o servidor")
        
        try:
            subprocess.run(
                [self.python_venv, str(manage_py), "runserver"],
                cwd=str(self.meuprojeto),
                check=False
            )
        except KeyboardInterrupt:
            self.print_info("\n\nServidor parado.")
        except Exception as e:
            self.print_erro(f"Erro ao iniciar servidor: {e}")
            return False
        
        return True
    
    # ═════════════════════════════════════════════════════════════════════════
    # EXECUTAR TUDO
    # ═════════════════════════════════════════════════════════════════════════
    
    def executar_completo(self):
        """Executa o fluxo completo de inicialização"""
        
        # Cabeçalho
        print(f"\n{Cores.BOLD}{Cores.CYAN}")
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 78 + "║")
        print("║" + "  INICIALIZADOR SUPER DO SISTEMA - PLATAFORMA CASA".center(78) + "║")
        print("║" + "  Sistema Completo de Gestão de Monitorias".center(78) + "║")
        print("║" + " " * 78 + "║")
        print("╚" + "═" * 78 + "╝")
        print(f"{Cores.END}\n")
        
        # Executar steps
        steps = [
            ("Verificando pré-requisitos", self.verificar_prerequisites),
            ("Configurando ambiente virtual", self.setup_venv),
            ("Instalando dependências", self.instalar_dependencias),
            ("Aplicando migrações", self.aplicar_migracoes),
            ("Criando usuários de teste", self.criar_usuarios_teste),
            ("Executando testes básicos", self.executar_testes_basicos),
        ]
        
        for i, (nome, funcao) in enumerate(steps, 1):
            try:
                if not funcao():
                    self.print_erro(f"Falha em: {nome}")
                    if input("\nContinuar mesmo assim? (s/n): ").lower() != 's':
                        return False
            except Exception as e:
                self.print_erro(f"Exceção em {nome}: {e}")
                if input("\nContinuar mesmo assim? (s/n): ").lower() != 's':
                    return False
        
        # Iniciar servidor
        self.iniciar_servidor()
        
        return True


# ═════════════════════════════════════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════════════════════════════════════

def main():
    """Função principal"""
    try:
        inicializador = InicializadorSistema()
        sucesso = inicializador.executar_completo()
        
        if sucesso:
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{Cores.YELLOW}[AVISO] Operação cancelada pelo usuário.{Cores.END}")
        sys.exit(1)
    except Exception as e:
        print(f"{Cores.RED}[ERRO] Erro fatal: {e}{Cores.END}")
        sys.exit(1)


if __name__ == "__main__":
    main()
