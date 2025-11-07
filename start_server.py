#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║              🚀 PLATAFORMA CASA - INICIALIZADOR INTELIGENTE                  ║
║                      Sistema de Gestão de Monitorias                         ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Script de inicialização robusto com suporte a HTTP/HTTPS
Autor: Sistema CASA
Versão: 2.0
"""

import os
import sys
import subprocess
import platform
import signal
import time
from pathlib import Path
from typing import Optional, Tuple

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÕES
# ══════════════════════════════════════════════════════════════════════════════

class Cores:
    """Códigos de cores ANSI para terminal"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    @staticmethod
    def desabilitar():
        """Desabilita cores no Windows se necessário"""
        if platform.system() == 'Windows':
            Cores.RED = Cores.GREEN = Cores.YELLOW = Cores.BLUE = ''
            Cores.MAGENTA = Cores.CYAN = Cores.WHITE = Cores.BOLD = ''
            Cores.UNDERLINE = Cores.END = ''

# ══════════════════════════════════════════════════════════════════════════════
# FUNÇÕES DE LOG
# ══════════════════════════════════════════════════════════════════════════════

def print_banner():
    """Exibe o banner inicial"""
    print(f"\n{Cores.BOLD}{Cores.CYAN}")
    print("╔═══════════════════════════════════════════════════════════════════════════════╗")
    print("║              🚀 PLATAFORMA CASA - INICIALIZAÇÃO INTELIGENTE                  ║")
    print("║                      Sistema de Gestão de Monitorias                         ║")
    print("╚═══════════════════════════════════════════════════════════════════════════════╝")
    print(f"{Cores.END}")

def log_step(msg: str):
    """Log de etapa/seção"""
    print(f"\n{Cores.CYAN}{Cores.BOLD}▶ {msg}{Cores.END}")

def log_success(msg: str):
    """Log de sucesso"""
    print(f"{Cores.GREEN}✅ {msg}{Cores.END}")

def log_error(msg: str):
    """Log de erro"""
    print(f"{Cores.RED}❌ ERRO: {msg}{Cores.END}")

def log_warning(msg: str):
    """Log de aviso"""
    print(f"{Cores.YELLOW}⚠️  AVISO: {msg}{Cores.END}")

def log_info(msg: str):
    """Log informativo"""
    print(f"{Cores.BLUE}ℹ️  {msg}{Cores.END}")

def print_separator():
    """Imprime uma linha separadora"""
    print(f"{Cores.CYAN}{'─' * 80}{Cores.END}")

# ══════════════════════════════════════════════════════════════════════════════
# CLASSE PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

class InicializadorPlataformaCASA:
    """Classe principal para inicialização do sistema"""
    
    def __init__(self):
        self.projeto_raiz = Path(__file__).parent.resolve()
        self.meuprojeto = self.projeto_raiz / "meuprojeto"
        self.venv_path = self.projeto_raiz / ".venv"
        self.manage_py = self.meuprojeto / "manage.py"
        self.requirements = self.projeto_raiz / "requirements.txt"
        
        self.erros = 0
        self.avisos = 0
        
        # Determinar executáveis do venv
        if platform.system() == "Windows":
            self.python_venv = str(self.venv_path / "Scripts" / "python.exe")
            self.pip_venv = str(self.venv_path / "Scripts" / "pip.exe")
        else:
            self.python_venv = str(self.venv_path / "bin" / "python")
            self.pip_venv = str(self.venv_path / "bin" / "pip")
    
    def executar_comando(self, cmd: list, timeout: int = 60, silent: bool = False) -> Tuple[bool, str]:
        """
        Executa um comando e retorna (sucesso, saída)
        
        Args:
            cmd: Lista com o comando e argumentos
            timeout: Timeout em segundos
            silent: Se True, suprime a saída
            
        Returns:
            Tupla (sucesso: bool, saída: str)
        """
        try:
            resultado = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(self.meuprojeto) if 'manage.py' in ' '.join(cmd) else None
            )
            
            saida = resultado.stdout + resultado.stderr
            sucesso = resultado.returncode == 0
            
            if not silent and not sucesso:
                log_warning(f"Comando retornou código {resultado.returncode}")
                if saida.strip():
                    print(saida)
            
            return sucesso, saida
        except subprocess.TimeoutExpired:
            log_error(f"Timeout ao executar: {' '.join(cmd)}")
            return False, "Timeout"
        except Exception as e:
            log_error(f"Erro ao executar comando: {e}")
            return False, str(e)
    
    def verificar_estrutura(self) -> bool:
        """Verifica a estrutura básica do projeto"""
        log_step("Verificando estrutura do projeto...")
        
        if not self.manage_py.exists():
            log_error(f"manage.py não encontrado em {self.meuprojeto}")
            self.erros += 1
            return False
        log_success("manage.py encontrado")
        
        if not self.requirements.exists():
            log_warning("requirements.txt não encontrado")
            self.avisos += 1
        else:
            log_success("requirements.txt encontrado")
        
        log_info(f"Diretório do projeto: {self.projeto_raiz}")
        return True
    
    def configurar_venv(self) -> bool:
        """Configura o ambiente virtual"""
        log_step("Configurando ambiente virtual...")
        
        if not self.venv_path.exists():
            log_info("Criando ambiente virtual...")
            sucesso, _ = self.executar_comando([sys.executable, "-m", "venv", str(self.venv_path)])
            
            if sucesso:
                log_success("Ambiente virtual criado")
            else:
                log_error("Falha ao criar ambiente virtual")
                self.erros += 1
                return False
        else:
            log_success("Ambiente virtual encontrado")
        
        # Verificar se o Python do venv existe
        if not Path(self.python_venv).exists():
            log_error(f"Python do venv não encontrado: {self.python_venv}")
            self.erros += 1
            return False
        
        log_success(f"Usando Python: {self.python_venv}")
        
        # Verificar versão do Python
        sucesso, saida = self.executar_comando([self.python_venv, "--version"], silent=True)
        if sucesso:
            versao = saida.strip()
            log_success(f"Versão: {versao}")
        
        return True
    
    def instalar_dependencias(self) -> bool:
        """Instala as dependências do projeto"""
        log_step("Verificando/Instalando dependências...")
        
        # Verificar se Django está instalado
        sucesso, _ = self.executar_comando(
            [self.python_venv, "-c", "import django"],
            silent=True
        )
        
        if not sucesso:
            log_info("Django não instalado. Instalando dependências...")
            
            # Atualizar pip
            log_info("Atualizando pip...")
            self.executar_comando([self.python_venv, "-m", "pip", "install", "--upgrade", "pip"], silent=True)
            
            # Instalar do requirements.txt
            if self.requirements.exists():
                log_info("Instalando a partir do requirements.txt...")
                sucesso, saida = self.executar_comando(
                    [self.pip_venv, "install", "-r", str(self.requirements)],
                    timeout=300
                )
                
                if sucesso:
                    log_success("Dependências instaladas com sucesso")
                else:
                    log_warning("Erro ao instalar do requirements.txt")
                    log_info("Tentando instalar pacotes essenciais...")
                    
                    pacotes = [
                        "Django>=5.0",
                        "djangorestframework",
                        "django-cors-headers",
                        "drf-yasg",
                        "python-decouple",
                        "dj-database-url",
                        "whitenoise",
                        "gunicorn",
                        "psycopg2-binary"
                    ]
                    
                    for pacote in pacotes:
                        log_info(f"Instalando {pacote}...")
                        self.executar_comando([self.pip_venv, "install", pacote], silent=True)
                    
                    log_success("Pacotes essenciais instalados")
            else:
                log_info("Instalando pacotes essenciais...")
                pacotes = ["Django", "djangorestframework", "django-cors-headers", "drf-yasg"]
                sucesso, _ = self.executar_comando([self.pip_venv, "install"] + pacotes, timeout=180)
                
                if sucesso:
                    log_success("Pacotes essenciais instalados")
                else:
                    log_error("Falha ao instalar dependências")
                    self.erros += 1
                    return False
        else:
            # Verificar versão do Django
            sucesso, saida = self.executar_comando(
                [self.python_venv, "-c", "import django; print(django.get_version())"],
                silent=True
            )
            if sucesso:
                versao = saida.strip()
                log_success(f"Django {versao} já instalado")
        
        return True
    
    def verificar_banco_dados(self) -> bool:
        """Verifica e configura o banco de dados"""
        log_step("Verificando banco de dados...")
        
        db_file = self.meuprojeto / "db.sqlite3"
        
        if db_file.exists():
            tamanho = db_file.stat().st_size / 1024  # KB
            if tamanho < 1024:
                log_success(f"Banco de dados encontrado ({tamanho:.1f} KB)")
            else:
                log_success(f"Banco de dados encontrado ({tamanho/1024:.1f} MB)")
        else:
            log_info("Banco de dados será criado")
        
        # Verificar migrações pendentes
        log_info("Verificando migrações...")
        
        # Criar migrações
        log_info("Criando migrações...")
        self.executar_comando(
            [self.python_venv, str(self.manage_py), "makemigrations", "--noinput"],
            silent=True
        )
        
        # Aplicar migrações
        log_info("Aplicando migrações...")
        sucesso, saida = self.executar_comando(
            [self.python_venv, str(self.manage_py), "migrate", "--noinput"],
            timeout=120
        )
        
        if sucesso:
            log_success("Migrações aplicadas com sucesso")
        else:
            log_warning("Erro ao aplicar migrações")
            log_info("Tentando com --fake-initial...")
            sucesso, _ = self.executar_comando(
                [self.python_venv, str(self.manage_py), "migrate", "--fake-initial"],
                timeout=120
            )
            if sucesso:
                log_success("Migrações aplicadas com --fake-initial")
            else:
                log_error("Não foi possível aplicar migrações")
                self.avisos += 1
        
        return True
    
    def coletar_estaticos(self) -> bool:
        """Coleta arquivos estáticos"""
        log_step("Coletando arquivos estáticos...")
        
        sucesso, _ = self.executar_comando(
            [self.python_venv, str(self.manage_py), "collectstatic", "--noinput", "--clear"],
            timeout=60,
            silent=True
        )
        
        if sucesso:
            log_success("Arquivos estáticos coletados")
        else:
            log_warning("Não foi possível coletar estáticos (não crítico)")
            self.avisos += 1
        
        return True
    
    def criar_superusuario(self) -> bool:
        """Cria superusuário se não existir"""
        log_step("Verificando usuário admin...")
        
        script = """
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@casa.com', 'admin')
    print('CRIADO')
else:
    print('EXISTE')
"""
        
        sucesso, saida = self.executar_comando(
            [self.python_venv, str(self.manage_py), "shell", "-c", script],
            silent=True
        )
        
        if sucesso:
            if 'CRIADO' in saida:
                log_success("Superusuário criado: admin / admin")
            else:
                log_success("Superusuário já existe")
        else:
            log_warning("Não foi possível verificar/criar superusuário")
            self.avisos += 1
        
        return True
    
    def verificar_porta(self, porta: int = 8000) -> bool:
        """Verifica se a porta está disponível"""
        log_step(f"Verificando porta {porta}...")
        
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        resultado = sock.connect_ex(('127.0.0.1', porta))
        sock.close()
        
        if resultado == 0:
            log_warning(f"Porta {porta} já está em uso")
            
            resposta = input(f"\n{Cores.YELLOW}Deseja tentar liberar a porta? (s/N): {Cores.END}").strip().lower()
            
            if resposta == 's':
                log_info("Tentando liberar a porta...")
                if platform.system() != 'Windows':
                    os.system(f"lsof -ti:{porta} | xargs kill -9 2>/dev/null")
                    time.sleep(2)
                    
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    resultado = sock.connect_ex(('127.0.0.1', porta))
                    sock.close()
                    
                    if resultado != 0:
                        log_success(f"Porta {porta} liberada")
                        return True
                    else:
                        log_error(f"Não foi possível liberar a porta {porta}")
                        return False
                else:
                    log_warning("Liberação automática não disponível no Windows")
                    return False
            else:
                return False
        else:
            log_success(f"Porta {porta} disponível")
            return True
    
    def exibir_resumo(self):
        """Exibe resumo da verificação"""
        print(f"\n{Cores.CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗{Cores.END}")
        print(f"{Cores.CYAN}║                           RESUMO DA VERIFICAÇÃO                               ║{Cores.END}")
        print(f"{Cores.CYAN}╠═══════════════════════════════════════════════════════════════════════════════╣{Cores.END}")
        
        if self.erros == 0 and self.avisos == 0:
            print(f"{Cores.CYAN}║{Cores.END}  {Cores.GREEN}✅ Sistema totalmente configurado! Nenhum problema encontrado.{Cores.END}             {Cores.CYAN}║{Cores.END}")
        elif self.erros == 0:
            print(f"{Cores.CYAN}║{Cores.END}  {Cores.YELLOW}⚠️  Sistema configurado com {self.avisos} avisos (não críticos){Cores.END}                      {Cores.CYAN}║{Cores.END}")
        else:
            print(f"{Cores.CYAN}║{Cores.END}  {Cores.RED}❌ {self.erros} erros encontrados. Verifique as mensagens acima.{Cores.END}                  {Cores.CYAN}║{Cores.END}")
        
        print(f"{Cores.CYAN}╚═══════════════════════════════════════════════════════════════════════════════╝{Cores.END}\n")
    
    def escolher_modo_servidor(self) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Permite ao usuário escolher entre HTTP e HTTPS
        
        Returns:
            Tupla (usar_https, cert_file, key_file)
        """
        print(f"\n{Cores.BOLD}{Cores.CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗{Cores.END}")
        print(f"{Cores.BOLD}{Cores.CYAN}║                     ESCOLHA O MODO DE EXECUÇÃO                               ║{Cores.END}")
        print(f"{Cores.BOLD}{Cores.CYAN}╚═══════════════════════════════════════════════════════════════════════════════╝{Cores.END}\n")
        
        print(f"{Cores.BOLD}Selecione uma opção:{Cores.END}\n")
        print(f"  {Cores.GREEN}1{Cores.END}) {Cores.BOLD}HTTP{Cores.END} - Desenvolvimento local (Recomendado)")
        print(f"     {Cores.BLUE}• Mais rápido e simples{Cores.END}")
        print(f"     {Cores.BLUE}• Ideal para desenvolvimento{Cores.END}")
        print(f"     {Cores.BLUE}• URL: http://localhost:8000{Cores.END}\n")
        
        print(f"  {Cores.YELLOW}2{Cores.END}) {Cores.BOLD}HTTPS{Cores.END} - Configuração automática completa")
        print(f"     {Cores.BLUE}• Cria certificados SSL automaticamente{Cores.END}")
        print(f"     {Cores.BLUE}• Instala todas as dependências necessárias{Cores.END}")
        print(f"     {Cores.BLUE}• URL: https://localhost:8000{Cores.END}")
        print(f"     {Cores.YELLOW}• Navegador mostrará aviso de segurança (normal){Cores.END}\n")
        
        while True:
            escolha = input(f"{Cores.BOLD}Digite sua escolha (1-2) [1]: {Cores.END}").strip() or "1"
            
            if escolha == "1":
                log_success("Modo HTTP selecionado")
                return False, None, None
            
            elif escolha == "2":
                # Instalar suporte para HTTPS automaticamente
                log_step("Preparando ambiente para HTTPS...")
                self.instalar_suporte_https()
                
                log_info("Criando certificados SSL automaticamente...")
                cert_file, key_file = self.criar_certificados_autoassinados()
                
                if cert_file and key_file:
                    log_success("Certificados SSL criados com sucesso")
                    log_info(f"Certificado: {cert_file}")
                    log_info(f"Chave: {key_file}")
                    
                    # Verificar se django_extensions está disponível
                    sucesso, _ = self.executar_comando(
                        [self.python_venv, "-c", "import django_extensions"],
                        silent=True
                    )
                    
                    if sucesso:
                        log_info("Usando django-extensions runserver_plus para HTTPS")
                        return True, cert_file, key_file
                    else:
                        log_warning("django-extensions não disponível")
                        log_info("Usando servidor padrão do Django")
                        return True, cert_file, key_file
                else:
                    log_error("Falha ao criar certificados SSL")
                    
                    resposta = input(f"\n{Cores.YELLOW}Deseja tentar o modo HTTP? (S/n): {Cores.END}").strip().lower()
                    if resposta != 'n':
                        log_info("Voltando para modo HTTP...")
                        return False, None, None
                    else:
                        log_error("Não é possível continuar sem certificados")
                        sys.exit(1)
            
            else:
                log_warning("Opção inválida. Digite 1 ou 2.")
    
    def instalar_suporte_https(self) -> bool:
        """
        Instala pacotes necessários para HTTPS com django-extensions
        
        Returns:
            bool: True se instalação foi bem-sucedida
        """
        log_info("Instalando suporte para HTTPS...")
        
        # Pacotes necessários para HTTPS
        pacotes = [
            "django-extensions",  # Fornece runserver_plus com HTTPS
            "werkzeug",           # Servidor WSGI com suporte SSL
            "pyopenssl"          # OpenSSL para Python
        ]
        
        for pacote in pacotes:
            log_info(f"Instalando {pacote}...")
            sucesso, _ = self.executar_comando(
                [self.pip_venv, "install", "-q", pacote],
                timeout=120,
                silent=True
            )
            if not sucesso:
                log_warning(f"Falha ao instalar {pacote}")
        
        # Adicionar django_extensions ao INSTALLED_APPS se não estiver
        settings_file = self.meuprojeto / "meuprojeto" / "settings.py"
        
        if settings_file.exists():
            with open(settings_file, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            if 'django_extensions' not in conteudo:
                log_info("Adicionando django_extensions ao INSTALLED_APPS...")
                
                # Procurar INSTALLED_APPS e adicionar django_extensions
                if 'INSTALLED_APPS = [' in conteudo:
                    conteudo = conteudo.replace(
                        "INSTALLED_APPS = [",
                        "INSTALLED_APPS = [\n    'django_extensions',"
                    )
                    
                    with open(settings_file, 'w', encoding='utf-8') as f:
                        f.write(conteudo)
                    
                    log_success("django_extensions adicionado ao INSTALLED_APPS")
        
        log_success("Suporte para HTTPS instalado")
        return True
    
    def criar_certificados_autoassinados(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Cria certificados SSL auto-assinados usando múltiplos métodos
        
        Returns:
            Tupla (cert_file, key_file) ou (None, None) em caso de erro
        """
        try:
            cert_dir = self.projeto_raiz / "ssl_certs"
            cert_dir.mkdir(exist_ok=True)
            
            cert_file = cert_dir / "cert.pem"
            key_file = cert_dir / "key.pem"
            
            # Verificar se certificados já existem
            if cert_file.exists() and key_file.exists():
                log_info("Certificados existentes encontrados")
                
                # Verificar se ainda são válidos (não expirados)
                sucesso, saida = self.executar_comando(
                    ["openssl", "x509", "-in", str(cert_file), "-noout", "-enddate"],
                    silent=True
                )
                
                if sucesso:
                    log_success("Certificados válidos encontrados")
                    log_info(f"Certificado: {cert_file}")
                    log_info(f"Chave: {key_file}")
                    return str(cert_file), str(key_file)
                else:
                    log_warning("Certificados existentes podem estar corrompidos")
            
            log_info("Criando novos certificados SSL auto-assinados...")
            
            # Método 1: Tentar com OpenSSL via linha de comando
            sucesso, _ = self.executar_comando(["openssl", "version"], silent=True)
            
            if sucesso:
                log_info("Usando OpenSSL para criar certificados...")
                
                # Criar chave privada
                cmd_key = [
                    "openssl", "genrsa", "-out", str(key_file), "2048"
                ]
                sucesso_key, _ = self.executar_comando(cmd_key, silent=True)
                
                if sucesso_key:
                    # Criar certificado
                    cmd_cert = [
                        "openssl", "req", "-new", "-x509",
                        "-key", str(key_file),
                        "-out", str(cert_file),
                        "-days", "365",
                        "-subj", "/C=BR/ST=Estado/L=Cidade/O=Plataforma CASA/CN=localhost"
                    ]
                    sucesso_cert, _ = self.executar_comando(cmd_cert, silent=True)
                    
                    if sucesso_cert:
                        log_success(f"✓ Certificado criado: {cert_file}")
                        log_success(f"✓ Chave criada: {key_file}")
                        log_info("Válido por 365 dias")
                        return str(cert_file), str(key_file)
            
            # Método 2: Tentar com Python pyOpenSSL
            log_info("Tentando criar certificados com Python...")
            
            try:
                from OpenSSL import crypto
                
                # Criar par de chaves
                k = crypto.PKey()
                k.generate_key(crypto.TYPE_RSA, 2048)
                
                # Criar certificado
                cert = crypto.X509()
                cert.get_subject().C = "BR"
                cert.get_subject().ST = "Estado"
                cert.get_subject().L = "Cidade"
                cert.get_subject().O = "Plataforma CASA"
                cert.get_subject().CN = "localhost"
                
                cert.set_serial_number(1000)
                cert.gmtime_adj_notBefore(0)
                cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)  # 1 ano
                cert.set_issuer(cert.get_subject())
                cert.set_pubkey(k)
                cert.sign(k, 'sha256')
                
                # Salvar arquivos
                with open(cert_file, "wb") as f:
                    f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
                
                with open(key_file, "wb") as f:
                    f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
                
                log_success(f"✓ Certificado criado com Python: {cert_file}")
                log_success(f"✓ Chave criada: {key_file}")
                return str(cert_file), str(key_file)
                
            except ImportError:
                log_warning("pyOpenSSL não está instalado")
                log_info("Instalando pyOpenSSL...")
                self.executar_comando([self.pip_venv, "install", "-q", "pyopenssl"], silent=True)
                
                # Tentar novamente
                try:
                    from OpenSSL import crypto
                    
                    k = crypto.PKey()
                    k.generate_key(crypto.TYPE_RSA, 2048)
                    
                    cert = crypto.X509()
                    cert.get_subject().CN = "localhost"
                    cert.set_serial_number(1000)
                    cert.gmtime_adj_notBefore(0)
                    cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)
                    cert.set_issuer(cert.get_subject())
                    cert.set_pubkey(k)
                    cert.sign(k, 'sha256')
                    
                    with open(cert_file, "wb") as f:
                        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
                    
                    with open(key_file, "wb") as f:
                        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
                    
                    log_success(f"✓ Certificado criado: {cert_file}")
                    log_success(f"✓ Chave criada: {key_file}")
                    return str(cert_file), str(key_file)
                    
                except Exception as e2:
                    log_error(f"Erro ao criar certificados com Python: {e2}")
            
            log_error("Não foi possível criar certificados SSL")
            log_info("Sugestões:")
            log_info("1. Instale OpenSSL: brew install openssl (macOS)")
            log_info("2. Ou use o modo HTTP (opção 1)")
            return None, None
                
        except Exception as e:
            log_error(f"Erro ao criar certificados: {e}")
            return None, None
    
    def iniciar_servidor(self, usar_https: bool = False, cert_file: str = None, key_file: str = None):
        """Inicia o servidor Django"""
        print(f"\n{Cores.GREEN}{Cores.BOLD}✓ Sistema pronto para inicialização!{Cores.END}\n")
        
        protocolo = "https" if usar_https else "http"
        
        print(f"{Cores.CYAN}📍 URLs Disponíveis:{Cores.END}")
        print(f"   {Cores.BOLD}• Página Principal:{Cores.END}  {protocolo}://localhost:8000/")
        print(f"   {Cores.BOLD}• Admin Django:{Cores.END}      {protocolo}://localhost:8000/admin/")
        print(f"   {Cores.BOLD}• API Root:{Cores.END}          {protocolo}://localhost:8000/api/")
        print(f"   {Cores.BOLD}• Swagger:{Cores.END}           {protocolo}://localhost:8000/restapi/")
        print(f"   {Cores.BOLD}• ReDoc:{Cores.END}             {protocolo}://localhost:8000/restapi/redoc/")
        print("")
        print(f"{Cores.CYAN}🔑 Credenciais Padrão:{Cores.END}")
        print(f"   {Cores.BOLD}• Usuário:{Cores.END}           admin")
        print(f"   {Cores.BOLD}• Senha:{Cores.END}             admin")
        print("")
        
        if usar_https:
            print(f"{Cores.YELLOW}⚠️  AVISO: Usando HTTPS{Cores.END}")
            if cert_file and "cert.pem" in cert_file:
                print(f"{Cores.YELLOW}   Certificado auto-assinado - seu navegador mostrará um aviso{Cores.END}")
                print(f"{Cores.YELLOW}   Para aceitar: clique em 'Avançado' → 'Prosseguir para localhost'{Cores.END}")
            print("")
        
        print(f"{Cores.YELLOW}💡 Dica: Pressione CTRL+C para parar o servidor{Cores.END}\n")
        
        # Montar comando
        if usar_https and cert_file and key_file:
            # Verificar se django_extensions está disponível
            sucesso, _ = self.executar_comando(
                [self.python_venv, "-c", "import django_extensions"],
                silent=True
            )
            
            if sucesso:
                log_info("Usando runserver_plus (django-extensions) com SSL")
                # Usar django-extensions runserver_plus que tem suporte SSL nativo
                cmd = [
                    self.python_venv, str(self.manage_py), 
                    "runserver_plus", 
                    "0.0.0.0:8000",
                    "--cert-file", cert_file,
                    "--key-file", key_file
                ]
            else:
                log_warning("django-extensions não disponível")
                log_warning("Django runserver padrão não suporta HTTPS")
                log_info("Continuando com HTTP...")
                
                usar_https = False
                protocolo = "http"
                cmd = [self.python_venv, str(self.manage_py), "runserver", "0.0.0.0:8000"]
        else:
            # Usar runserver padrão para HTTP
            cmd = [self.python_venv, str(self.manage_py), "runserver", "0.0.0.0:8000"]
        
        # Configurar handler para CTRL+C
        def signal_handler(sig, frame):
            print(f"\n\n{Cores.GREEN}✓{Cores.END} Servidor parado. Até logo!\n")
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        
        log_info("Iniciando servidor Django...\n")
        print_separator()
        
        # Loop de reinicialização em caso de erro
        tentativas = 0
        max_tentativas = 3
        
        while tentativas < max_tentativas:
            try:
                processo = subprocess.Popen(
                    cmd,
                    cwd=str(self.meuprojeto),
                    stdout=sys.stdout,
                    stderr=sys.stderr
                )
                
                processo.wait()
                
                if processo.returncode != 0:
                    print("")
                    log_error(f"Servidor encerrou com código {processo.returncode}")
                    tentativas += 1
                    
                    if tentativas < max_tentativas:
                        resposta = input(f"\n{Cores.YELLOW}Deseja reiniciar o servidor? (s/N): {Cores.END}").strip().lower()
                        if resposta != 's':
                            break
                        
                        log_info("Reiniciando servidor em 3 segundos...")
                        time.sleep(3)
                    else:
                        log_error(f"Máximo de {max_tentativas} tentativas atingido")
                        break
                else:
                    break
                    
            except KeyboardInterrupt:
                print(f"\n\n{Cores.GREEN}✓{Cores.END} Servidor parado. Até logo!\n")
                break
            except Exception as e:
                log_error(f"Erro ao iniciar servidor: {e}")
                tentativas += 1
                if tentativas < max_tentativas:
                    time.sleep(3)
                else:
                    break
    
    def executar(self):
        """Executa o processo completo de inicialização"""
        print_banner()
        
        # Verificações
        if not self.verificar_estrutura():
            return 1
        
        if not self.configurar_venv():
            return 1
        
        if not self.instalar_dependencias():
            return 1
        
        if not self.verificar_banco_dados():
            return 1
        
        self.coletar_estaticos()
        self.criar_superusuario()
        
        if not self.verificar_porta(8000):
            return 1
        
        self.exibir_resumo()
        
        if self.erros > 0:
            log_error("Inicialização abortada devido a erros críticos")
            return 1
        
        # Escolher modo de execução
        usar_https, cert_file, key_file = self.escolher_modo_servidor()
        
        # Iniciar servidor
        self.iniciar_servidor(usar_https, cert_file, key_file)
        
        return 0

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    """Função principal"""
    try:
        inicializador = InicializadorPlataformaCASA()
        codigo_saida = inicializador.executar()
        sys.exit(codigo_saida)
    except KeyboardInterrupt:
        print(f"\n\n{Cores.YELLOW}Operação cancelada pelo usuário{Cores.END}\n")
        sys.exit(0)
    except Exception as e:
        log_error(f"Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
