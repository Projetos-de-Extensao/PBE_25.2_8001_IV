#!/bin/bash

# Script de Deploy Automatizado para Heroku
# Execute este script após instalar o Heroku CLI e fazer login

set -e  # Para o script se houver erro

echo "=========================================="
echo "Script de Deploy Heroku - Plataforma Casa"
echo "=========================================="
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verifica se Heroku CLI está instalado
if ! command -v heroku &> /dev/null; then
    echo -e "${RED}Erro: Heroku CLI não está instalado.${NC}"
    echo ""
    echo "Para instalar:"
    echo "1. Visite: https://devcenter.heroku.com/articles/heroku-cli"
    echo "2. Ou execute: brew tap heroku/brew && brew install heroku"
    exit 1
fi

echo -e "${GREEN}✓ Heroku CLI detectado${NC}"

# Verifica se está logado no Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo -e "${YELLOW}Você não está logado no Heroku.${NC}"
    echo "Executando login..."
    heroku login
fi

echo -e "${GREEN}✓ Autenticado no Heroku${NC}"
echo ""

# Pergunta o nome da aplicação
read -p "Digite o nome da aplicação Heroku (deixe em branco para gerar automático): " APP_NAME

# Cria aplicação
echo ""
echo "Criando aplicação na Heroku..."
if [ -z "$APP_NAME" ]; then
    heroku create
else
    heroku create "$APP_NAME"
fi

# Captura o nome da app criada
APP_NAME=$(heroku apps:info --json | grep -o '"name":"[^"]*' | cut -d'"' -f4)
echo -e "${GREEN}✓ Aplicação criada: $APP_NAME${NC}"
echo ""

# Adiciona PostgreSQL
echo "Adicionando PostgreSQL..."
echo "Escolha o plano:"
echo "1) mini (gratuito, limitado)"
echo "2) essential-0 ($5/mês - RECOMENDADO)"
read -p "Digite 1 ou 2: " DB_CHOICE

if [ "$DB_CHOICE" = "2" ]; then
    heroku addons:create heroku-postgresql:essential-0 --app "$APP_NAME"
else
    heroku addons:create heroku-postgresql:mini --app "$APP_NAME"
fi

echo -e "${GREEN}✓ PostgreSQL adicionado${NC}"
echo ""

# Gera SECRET_KEY
echo "Gerando SECRET_KEY segura..."
SECRET_KEY=$(/Users/anderson/my_folders/repositoriolocal/PBE_25.2_8001_IV/.venv/bin/python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")

# Configura variáveis de ambiente
echo "Configurando variáveis de ambiente..."
heroku config:set SECRET_KEY="$SECRET_KEY" --app "$APP_NAME"
heroku config:set DEBUG=False --app "$APP_NAME"
heroku config:set ALLOWED_HOSTS=".herokuapp.com" --app "$APP_NAME"

echo -e "${GREEN}✓ Variáveis de ambiente configuradas${NC}"
echo ""

# Adiciona remote do Heroku
echo "Configurando Git remote..."
heroku git:remote -a "$APP_NAME"

echo -e "${GREEN}✓ Git remote configurado${NC}"
echo ""

# Faz commit das alterações se houver
echo "Verificando alterações Git..."
if ! git diff-index --quiet HEAD --; then
    echo "Há alterações não commitadas. Fazendo commit..."
    git add .
    git commit -m "Configuração para deploy na Heroku com PostgreSQL"
fi

echo -e "${GREEN}✓ Código commitado${NC}"
echo ""

# Deploy
echo "=========================================="
echo "Iniciando deploy para Heroku..."
echo "=========================================="
echo ""

git push heroku anderon:main

echo ""
echo -e "${GREEN}✓ Deploy concluído${NC}"
echo ""

# Executa migrações
echo "Executando migrações do banco de dados..."
heroku run python meuprojeto/manage.py migrate --app "$APP_NAME"

echo -e "${GREEN}✓ Migrações executadas${NC}"
echo ""

# Coleta arquivos estáticos
echo "Coletando arquivos estáticos..."
heroku run python meuprojeto/manage.py collectstatic --noinput --app "$APP_NAME"

echo -e "${GREEN}✓ Arquivos estáticos coletados${NC}"
echo ""

# Cria superusuário
echo "=========================================="
echo "Criação de Superusuário"
echo "=========================================="
echo ""
read -p "Deseja criar um superusuário agora? (s/n): " CREATE_SUPER

if [ "$CREATE_SUPER" = "s" ] || [ "$CREATE_SUPER" = "S" ]; then
    heroku run python meuprojeto/manage.py createsuperuser --app "$APP_NAME"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}DEPLOY CONCLUÍDO COM SUCESSO!${NC}"
echo "=========================================="
echo ""
echo "Aplicação: $APP_NAME"
echo "URL: https://$APP_NAME.herokuapp.com"
echo ""
echo "Comandos úteis:"
echo "  Ver logs:           heroku logs --tail --app $APP_NAME"
echo "  Abrir aplicação:    heroku open --app $APP_NAME"
echo "  Console Django:     heroku run python meuprojeto/manage.py shell --app $APP_NAME"
echo "  Executar comando:   heroku run <comando> --app $APP_NAME"
echo ""

# Abre aplicação no navegador
read -p "Deseja abrir a aplicação no navegador? (s/n): " OPEN_APP
if [ "$OPEN_APP" = "s" ] || [ "$OPEN_APP" = "S" ]; then
    heroku open --app "$APP_NAME"
fi

echo ""
echo "Deploy finalizado!"
