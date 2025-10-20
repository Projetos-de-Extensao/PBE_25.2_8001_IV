#!/bin/bash
# ═════════════════════════════════════════════════════════════════════════════
# 🚀 SCRIPT INICIALIZADOR - PLATAFORMA CASA
# ═════════════════════════════════════════════════════════════════════════════

PROJETO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PYTHON="$PROJETO_DIR/inicializar_sistema.py"
VENV_DIR="$PROJETO_DIR/.venv"

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# ═════════════════════════════════════════════════════════════════════════════
# FUNÇÕES
# ═════════════════════════════════════════════════════════════════════════════

print_header() {
    echo -e "${BOLD}${CYAN}"
    echo "╔════════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                            ║"
    echo "║          🚀 INICIALIZADOR SUPER DO SISTEMA - PLATAFORMA CASA 🚀           ║"
    echo "║                                                                            ║"
    echo "║                    Sistema Completo de Gestão de Monitorias                ║"
    echo "║                                                                            ║"
    echo "╚════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}\n"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# ═════════════════════════════════════════════════════════════════════════════

print_header

# Detectar Python disponível
print_info "Detectando ambiente Python..."

# Procurar Python 3.10+
for python_cmd in python3.12 python3.11 python3.10 python3; do
    if command -v "$python_cmd" &> /dev/null; then
        PYTHON_VERSION=$($python_cmd --version 2>&1)
        MAJOR=$(echo $PYTHON_VERSION | cut -d' ' -f2 | cut -d'.' -f1)
        MINOR=$(echo $PYTHON_VERSION | cut -d' ' -f2 | cut -d'.' -f2)
        
        if [ "$MAJOR" -gt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 10 ]); then
            PYTHON_BIN=$python_cmd
            print_success "Python $PYTHON_VERSION encontrado ✓"
            break
        fi
    fi
done

if [ -z "$PYTHON_BIN" ]; then
    print_error "Python 3.10 ou superior não encontrado!"
    echo "Por favor, instale Python 3.10 ou superior"
    exit 1
fi

# Verificar script
if [ ! -f "$SCRIPT_PYTHON" ]; then
    print_error "Script inicializar_sistema.py não encontrado em $PROJETO_DIR"
    exit 1
fi

print_info "Projeto: $PROJETO_DIR"
print_info "Usando Python: $PYTHON_BIN"

# Criar venv se não existir
if [ ! -d "$VENV_DIR" ]; then
    print_info "Criando ambiente virtual..."
    $PYTHON_BIN -m venv "$VENV_DIR"
    if [ $? -eq 0 ]; then
        print_success "Ambiente virtual criado ✓"
    else
        print_error "Falha ao criar ambiente virtual"
        exit 1
    fi
else
    print_success "Ambiente virtual encontrado ✓"
fi

# Executar script Python usando o venv
print_info "Executando inicializador...\n"
$PYTHON_BIN "$SCRIPT_PYTHON"

exit $?
