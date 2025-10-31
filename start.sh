#!/bin/bash
###############################################################################
# 🚀 PLATAFORMA CASA - Script de Inicialização
# Inicializa o sistema Django sem necessidade de HTTPS
###############################################################################

set -e  # Sair em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

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

echo -e "${BLUE}📂 Diretório do projeto: ${PROJECT_DIR}${NC}"
echo ""

# Verificar se manage.py existe
if [ ! -f "$PROJECT_DIR/manage.py" ]; then
    echo -e "${RED}❌ Erro: manage.py não encontrado em $PROJECT_DIR${NC}"
    exit 1
fi

# Verificar/criar ambiente virtual
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}📦 Criando ambiente virtual...${NC}"
    python3 -m venv "$VENV_DIR"
    echo -e "${GREEN}✓ Ambiente virtual criado${NC}"
else
    echo -e "${GREEN}✓ Ambiente virtual encontrado${NC}"
fi

# Ativar ambiente virtual
echo -e "${CYAN}🔧 Ativando ambiente virtual...${NC}"
source "$VENV_DIR/bin/activate"

# Atualizar pip
echo -e "${CYAN}📦 Atualizando pip...${NC}"
pip install --quiet --upgrade pip

# Instalar dependências
echo -e "${CYAN}📦 Instalando dependências...${NC}"
if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
    pip install --quiet -r "$SCRIPT_DIR/requirements.txt"
else
    # Instalar pacotes essenciais
    pip install --quiet Django>=5.0 \
        djangorestframework>=3.15 \
        django-cors-headers>=4.0 \
        drf-yasg>=1.21 \
        Pillow \
        python-dotenv \
        whitenoise
fi
echo -e "${GREEN}✓ Dependências instaladas${NC}"

# Aplicar migrações
echo -e "${CYAN}🔄 Aplicando migrações...${NC}"
cd "$PROJECT_DIR"
python manage.py makemigrations plataforma_Casa --noinput 2>/dev/null || true
python manage.py migrate --noinput
echo -e "${GREEN}✓ Migrações aplicadas${NC}"

# Coletar arquivos estáticos
echo -e "${CYAN}📁 Coletando arquivos estáticos...${NC}"
python manage.py collectstatic --noinput --clear 2>/dev/null || echo -e "${YELLOW}⚠ Não foi possível coletar estáticos (não crítico)${NC}"

# Criar superusuário se não existir
echo -e "${CYAN}👤 Verificando usuário admin...${NC}"
python manage.py shell <<EOF 2>/dev/null || true
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@casa.com', 'admin')
    print('✓ Superusuário criado: admin / admin')
else:
    print('✓ Superusuário já existe')
EOF

# Popular disciplinas se necessário
if [ -f "$PROJECT_DIR/popular_disciplinas.py" ]; then
    echo -e "${CYAN}📚 Verificando disciplinas...${NC}"
    python popular_disciplinas.py 2>/dev/null || echo -e "${YELLOW}⚠ Disciplinas não populadas${NC}"
fi

echo ""
echo -e "${GREEN}${BOLD}✓ Sistema pronto!${NC}"
echo ""
echo -e "${CYAN}📍 URLs Disponíveis:${NC}"
echo -e "   ${BOLD}• API Root:${NC}       http://localhost:8000/api/"
echo -e "   ${BOLD}• Swagger:${NC}        http://localhost:8000/restapi/"
echo -e "   ${BOLD}• ReDoc:${NC}          http://localhost:8000/restapi/redoc/"
echo -e "   ${BOLD}• Admin Django:${NC}   http://localhost:8000/admin/"
echo ""
echo -e "${CYAN}🔑 Credenciais:${NC}"
echo -e "   ${BOLD}• Admin:${NC}          admin / admin"
echo ""
echo -e "${YELLOW}Pressione CTRL+C para parar o servidor${NC}"
echo ""

# Iniciar servidor
python manage.py runserver 0.0.0.0:8000
