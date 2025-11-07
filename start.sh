#!/bin/bash
###############################################################################
# 🚀 PLATAFORMA CASA - Script de Inicialização Robusto
# Inicializa o sistema Django com verificações completas
###############################################################################

# Não sair em caso de erro - vamos tratar cada erro individualmente
# set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Contadores de erro
ERRORS=0
WARNINGS=0

# Funções de log
log_error() {
    echo -e "${RED}❌ ERRO: $1${NC}"
    ((ERRORS++))
}

log_warning() {
    echo -e "${YELLOW}⚠️  AVISO: $1${NC}"
    ((WARNINGS++))
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_step() {
    echo -e "\n${CYAN}${BOLD}▶ $1${NC}"
}

# Banner
echo -e "${BOLD}${CYAN}"
echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
echo "║                  🚀 PLATAFORMA CASA - INICIALIZAÇÃO                          ║"
echo "║                        Sistema de Gestão de Monitorias                       ║"
echo "╚═══════════════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Diretórios
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$SCRIPT_DIR/meuprojeto"
VENV_DIR="$SCRIPT_DIR/.venv"

echo -e "${BLUE}📂 Diretório do projeto: ${PROJECT_DIR}${NC}\n"

# ═════════════════════════════════════════════════════════════════════════════
# VERIFICAÇÃO 1: Estrutura do Projeto
# ═════════════════════════════════════════════════════════════════════════════
log_step "Verificando estrutura do projeto..."

if [ ! -f "$PROJECT_DIR/manage.py" ]; then
    log_error "manage.py não encontrado em $PROJECT_DIR"
    exit 1
fi
log_success "manage.py encontrado"

if [ ! -f "$SCRIPT_DIR/requirements.txt" ]; then
    log_warning "requirements.txt não encontrado"
else
    log_success "requirements.txt encontrado"
fi

# ═════════════════════════════════════════════════════════════════════════════
# VERIFICAÇÃO 2: Ambiente Virtual
# ═════════════════════════════════════════════════════════════════════════════
log_step "Verificando ambiente virtual..."

if [ ! -d "$VENV_DIR" ]; then
    log_warning "Ambiente virtual não encontrado. Criando..."
    python3 -m venv "$VENV_DIR"
    if [ $? -eq 0 ]; then
        log_success "Ambiente virtual criado"
    else
        log_error "Falha ao criar ambiente virtual"
        exit 1
    fi
else
    log_success "Ambiente virtual encontrado"
fi

# Ativar ambiente virtual
log_info "Ativando ambiente virtual..."
source "$VENV_DIR/bin/activate"

if [ -z "$VIRTUAL_ENV" ]; then
    log_error "Falha ao ativar ambiente virtual"
    exit 1
fi
log_success "Ambiente virtual ativado: $VIRTUAL_ENV"

# ═════════════════════════════════════════════════════════════════════════════
# VERIFICAÇÃO 3: Python e Pip
# ═════════════════════════════════════════════════════════════════════════════
log_step "Verificando Python e Pip..."

PYTHON_VERSION=$(python --version 2>&1)
log_success "Python: $PYTHON_VERSION"

PIP_VERSION=$(pip --version 2>&1 | awk '{print $2}')
log_info "Pip: versão $PIP_VERSION"

# Atualizar pip silenciosamente
pip install --quiet --upgrade pip 2>&1 > /dev/null
log_success "Pip atualizado"

# ═════════════════════════════════════════════════════════════════════════════
# VERIFICAÇÃO 4: Dependências
# ═════════════════════════════════════════════════════════════════════════════
log_step "Verificando/Instalando dependências..."

# Verificar Django
if ! python -c "import django" 2>/dev/null; then
    log_warning "Django não instalado. Instalando dependências..."
    
    if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
        log_info "Instalando a partir do requirements.txt..."
        pip install --quiet -r "$SCRIPT_DIR/requirements.txt"
        if [ $? -eq 0 ]; then
            log_success "Dependências instaladas com sucesso"
        else
            log_error "Falha ao instalar dependências"
            log_info "Tentando instalar pacotes essenciais individualmente..."
            pip install Django djangorestframework django-cors-headers drf-yasg python-decouple dj-database-url whitenoise gunicorn psycopg2-binary
        fi
    else
        log_info "Instalando pacotes essenciais..."
        pip install Django djangorestframework django-cors-headers drf-yasg python-decouple dj-database-url whitenoise gunicorn
        log_success "Pacotes essenciais instalados"
    fi
else
    DJANGO_VERSION=$(python -c "import django; print(django.get_version())" 2>/dev/null)
    log_success "Django $DJANGO_VERSION já instalado"
fi

# ═════════════════════════════════════════════════════════════════════════════
# VERIFICAÇÃO 5: Banco de Dados
# ═════════════════════════════════════════════════════════════════════════════
log_step "Verificando banco de dados..."

cd "$PROJECT_DIR"

DB_FILE="$PROJECT_DIR/db.sqlite3"
if [ -f "$DB_FILE" ]; then
    DB_SIZE=$(du -h "$DB_FILE" | awk '{print $1}')
    log_success "Banco de dados encontrado (${DB_SIZE})"
else
    log_info "Banco de dados será criado"
fi

# Verificar se há migrações pendentes
log_info "Verificando migrações..."
MIGRATIONS_OUTPUT=$(python manage.py showmigrations --plan 2>&1)

if echo "$MIGRATIONS_OUTPUT" | grep -q "\[ \]"; then
    log_warning "Há migrações não aplicadas"
    
    log_info "Criando migrações para plataforma_Casa..."
    python manage.py makemigrations plataforma_Casa --noinput 2>&1 | grep -v "No changes detected" || true
    
    log_info "Aplicando todas as migrações..."
    python manage.py migrate --noinput
    
    if [ $? -eq 0 ]; then
        log_success "Migrações aplicadas com sucesso"
    else
        log_error "Erro ao aplicar migrações"
        log_info "Tentando aplicar migrações com --fake-initial..."
        python manage.py migrate --fake-initial
    fi
else
    log_success "Todas as migrações estão aplicadas"
fi

# ═════════════════════════════════════════════════════════════════════════════
# VERIFICAÇÃO 6: Arquivos Estáticos
# ═════════════════════════════════════════════════════════════════════════════
log_step "Verificando arquivos estáticos..."

if [ -d "$PROJECT_DIR/staticfiles" ]; then
    STATIC_COUNT=$(find "$PROJECT_DIR/staticfiles" -type f | wc -l | tr -d ' ')
    log_success "Diretório staticfiles existe ($STATIC_COUNT arquivos)"
else
    log_info "Diretório staticfiles será criado"
fi

log_info "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear 2>&1 > /dev/null
if [ $? -eq 0 ]; then
    log_success "Arquivos estáticos coletados"
else
    log_warning "Não foi possível coletar estáticos (não crítico para desenvolvimento)"
fi

# ═════════════════════════════════════════════════════════════════════════════
# VERIFICAÇÃO 7: Superusuário
# ═════════════════════════════════════════════════════════════════════════════
log_step "Verificando usuário admin..."

python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@casa.com', 'admin')
    print('✓ Superusuário criado: admin / admin')
else:
    print('✓ Superusuário já existe')
" 2>/dev/null

# ═════════════════════════════════════════════════════════════════════════════
# VERIFICAÇÃO 8: Porta do Servidor
# ═════════════════════════════════════════════════════════════════════════════
log_step "Verificando disponibilidade da porta 8000..."

if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    log_warning "Porta 8000 já está em uso"
    log_info "Tentando liberar a porta..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    sleep 2
    if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        log_error "Não foi possível liberar a porta 8000"
        log_info "Tente executar: lsof -ti:8000 | xargs kill -9"
        exit 1
    else
        log_success "Porta 8000 liberada"
    fi
else
    log_success "Porta 8000 disponível"
fi

# ═════════════════════════════════════════════════════════════════════════════
# RESUMO PRÉ-INICIALIZAÇÃO
# ═════════════════════════════════════════════════════════════════════════════
echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                           RESUMO DA VERIFICAÇÃO                               ║${NC}"
echo -e "${CYAN}╠═══════════════════════════════════════════════════════════════════════════════╣${NC}"

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${CYAN}║${NC}  ${GREEN}✅ Sistema totalmente configurado! Nenhum problema encontrado.${NC}             ${CYAN}║${NC}"
elif [ $ERRORS -eq 0 ]; then
    echo -e "${CYAN}║${NC}  ${YELLOW}⚠️  Sistema configurado com $WARNINGS avisos (não críticos)${NC}                      ${CYAN}║${NC}"
else
    echo -e "${CYAN}║${NC}  ${RED}❌ $ERRORS erros encontrados. Verifique as mensagens acima.${NC}                  ${CYAN}║${NC}"
fi

echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

if [ $ERRORS -gt 0 ]; then
    log_error "Inicialização abortada devido a erros críticos"
    exit 1
fi

# ═════════════════════════════════════════════════════════════════════════════
# INICIAR SERVIDOR
# ═════════════════════════════════════════════════════════════════════════════
echo -e "${GREEN}${BOLD}✓ Sistema pronto para inicialização!${NC}\n"

echo -e "${CYAN}📍 URLs Disponíveis:${NC}"
echo -e "   ${BOLD}• Página Principal:${NC}  http://localhost:8000/"
echo -e "   ${BOLD}• Admin Django:${NC}      http://localhost:8000/admin/"
echo -e "   ${BOLD}• API Root:${NC}          http://localhost:8000/api/"
echo -e "   ${BOLD}• Swagger:${NC}           http://localhost:8000/restapi/"
echo -e "   ${BOLD}• ReDoc:${NC}             http://localhost:8000/restapi/redoc/"
echo ""
echo -e "${CYAN}🔑 Credenciais Padrão:${NC}"
echo -e "   ${BOLD}• Usuário:${NC}           admin"
echo -e "   ${BOLD}• Senha:${NC}             admin"
echo ""
echo -e "${YELLOW}💡 Dica: Pressione CTRL+C para parar o servidor${NC}"
echo -e "${YELLOW}💡 Se o servidor cair, execute este script novamente${NC}\n"

# Capturar CTRL+C graciosamente
trap 'echo -e "\n\n${GREEN}✓${NC} Servidor parado. Até logo!"; exit 0' INT

# Iniciar servidor com reinicialização automática em caso de erro
log_info "Iniciando servidor Django...\n"

while true; do
    python manage.py runserver 0.0.0.0:8000
    EXIT_CODE=$?
    
    if [ $EXIT_CODE -ne 0 ]; then
        echo ""
        log_error "Servidor encerrou com código de erro $EXIT_CODE"
        echo ""
        read -p "Deseja reiniciar o servidor? (s/N): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Ss]$ ]]; then
            log_info "Encerrando..."
            exit $EXIT_CODE
        fi
        log_info "Reiniciando servidor em 3 segundos..."
        sleep 3
    else
        break
    fi
done
