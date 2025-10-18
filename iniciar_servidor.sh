#!/bin/bash

# Script para iniciar a Plataforma Casa

echo "🚀 Iniciando Plataforma Casa..."
echo ""

# Navegar para o diretório correto
cd /Users/anderson/my_folders/repositoriolocal/PBE_25.2_8001_IV/meuprojeto

echo "📁 Diretório: $(pwd)"
echo ""

# Verificar se manage.py existe
if [ -f "manage.py" ]; then
    echo "✅ manage.py encontrado"
else
    echo "❌ manage.py não encontrado!"
    exit 1
fi

# Ativar ambiente virtual se necessário
if [ -d "venv" ]; then
    echo "🔧 Ativando ambiente virtual..."
    source venv/bin/activate
fi

echo ""
echo "🌐 Iniciando servidor em http://localhost:8000/"
echo ""

# Iniciar servidor Django
python manage.py runserver 0.0.0.0:8000
