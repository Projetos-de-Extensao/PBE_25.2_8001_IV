#!/bin/bash
# ═════════════════════════════════════════════════════════════════════════════
# 🐍 VERIFICADOR DE PYTHON - Plataforma Casa
# ═════════════════════════════════════════════════════════════════════════════

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

print_header() {
    echo -e "${BOLD}${CYAN}"
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo "                      🐍 VERIFICADOR DE PYTHON 3.10+"
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo -e "${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_header

# Tentar encontrar Python 3.10+
echo -e "${BOLD}Procurando Python 3.10+...${NC}\n"

found=0

for python_cmd in python3.12 python3.11 python3.10 python3; do
    if command -v "$python_cmd" &> /dev/null; then
        PYTHON_VERSION=$($python_cmd --version 2>&1)
        MAJOR=$(echo $PYTHON_VERSION | cut -d' ' -f2 | cut -d'.' -f1)
        MINOR=$(echo $PYTHON_VERSION | cut -d' ' -f2 | cut -d'.' -f2)
        
        echo "$python_cmd: $PYTHON_VERSION"
        
        if [ "$MAJOR" -gt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 10 ]); then
            print_success "$python_cmd é Python $MAJOR.$MINOR (✓ Compatível)"
            found=1
            PYTHON_BIN=$python_cmd
            break
        else
            print_warning "$python_cmd é Python $MAJOR.$MINOR (✗ Requer 3.10+)"
        fi
    fi
done

echo ""

if [ $found -eq 1 ]; then
    print_success "Python adequado encontrado: $PYTHON_BIN"
    print_info "\nVocê pode usar:"
    echo "  $PYTHON_BIN inicializar_sistema.py"
    echo "  ou"
    echo "  ./inicializar.sh"
    exit 0
else
    print_error "Python 3.10 ou superior não encontrado no sistema!"
    echo ""
    print_warning "Opções de instalação:\n"
    
    OS=$(uname)
    
    if [[ "$OS" == "Darwin" ]]; then
        echo -e "${CYAN}macOS (com Homebrew):${NC}"
        echo "  brew install python@3.11"
        echo ""
        echo -e "${CYAN}ou descarregue de: https://www.python.org/downloads/${NC}"
        
    elif [[ "$OS" == "Linux" ]]; then
        echo -e "${CYAN}Ubuntu/Debian:${NC}"
        echo "  sudo apt-get update"
        echo "  sudo apt-get install python3.11"
        echo ""
        echo -e "${CYAN}Fedora/RHEL:${NC}"
        echo "  sudo dnf install python3.11"
        echo ""
        echo -e "${CYAN}ou descarregue de: https://www.python.org/downloads/${NC}"
        
    elif [[ "$OS" == "MINGW64_NT" ]] || [[ "$OS" == "MSYS_NT" ]]; then
        echo -e "${CYAN}Windows:${NC}"
        echo "  Descarregue de: https://www.python.org/downloads/"
        echo "  Certifique-se de marcar 'Add Python to PATH' na instalação"
        
    else
        echo -e "${CYAN}Descarregue de: https://www.python.org/downloads/${NC}"
    fi
    
    echo ""
    print_warning "Após instalar Python 3.10+, execute novamente: ./inicializar.sh"
    exit 1
fi
