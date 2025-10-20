#!/bin/zsh

# Script de Continuação do Deploy para Heroku - Plataforma Casa
# Aplicação já criada: plataformacasa

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Continuação do Deploy - Plataforma Casa"
echo "=========================================="
echo ""
echo "Aplicação: plataformacasa"
echo "URL: https://plataformacasa-f820a0a16535.herokuapp.com/"
echo ""

APP_NAME="plataformacasa"

# Define o caminho do Heroku CLI
HEROKU_PATH="/opt/homebrew/bin/heroku"

# Verifica se heroku está disponível
if [ -f "$HEROKU_PATH" ]; then
    alias heroku="$HEROKU_PATH"
    echo -e "${GREEN}✓ Heroku CLI detectado${NC}"
elif command -v heroku &> /dev/null; then
    echo -e "${GREEN}✓ Heroku CLI detectado no PATH${NC}"
else
    echo -e "${RED}✗ Heroku CLI não encontrado${NC}"
    echo "Verifique se está instalado"
    exit 1
fi

echo ""

# Passo 1: Adicionar PostgreSQL
echo "=========================================="
echo "Passo 1: Adicionar PostgreSQL"
echo "=========================================="
echo ""
echo "Escolha o plano:"
echo "1) hobby-dev (gratuito, 10.000 linhas)"
echo "2) basic ($9/mês, 10M linhas)"
echo "3) Tentar outros planos automaticamente"
read "DB_CHOICE?Digite 1, 2 ou 3: "

echo ""
if [ "$DB_CHOICE" = "1" ]; then
    echo "Adicionando PostgreSQL hobby-dev..."
    heroku addons:create heroku-postgresql:hobby-dev --app "$APP_NAME"
elif [ "$DB_CHOICE" = "2" ]; then
    echo "Adicionando PostgreSQL basic..."
    heroku addons:create heroku-postgresql:basic --app "$APP_NAME"
else
    echo "Tentando adicionar PostgreSQL..."
    if heroku addons:create heroku-postgresql:hobby-dev --app "$APP_NAME" 2>/dev/null; then
        echo -e "${GREEN}✓ PostgreSQL hobby-dev adicionado${NC}"
    elif heroku addons:create heroku-postgresql:basic --app "$APP_NAME" 2>/dev/null; then
        echo -e "${GREEN}✓ PostgreSQL basic adicionado${NC}"
    elif heroku addons:create heroku-postgresql:standard-0 --app "$APP_NAME" 2>/dev/null; then
        echo -e "${GREEN}✓ PostgreSQL standard-0 adicionado${NC}"
    else
        echo -e "${RED}✗ Erro ao adicionar PostgreSQL${NC}"
        echo "Execute manualmente: heroku addons:plans heroku-postgresql"
        exit 1
    fi
fi

echo ""
echo -e "${GREEN}✓ PostgreSQL adicionado com sucesso${NC}"
echo ""

# Aguarda o PostgreSQL ficar pronto
echo "Aguardando PostgreSQL ficar pronto..."
sleep 5

# Passo 2: Configurar variáveis de ambiente
echo "=========================================="
echo "Passo 2: Configurar Variáveis de Ambiente"
echo "=========================================="
echo ""

echo "Gerando SECRET_KEY segura..."
SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")

echo "Configurando variáveis..."
heroku config:set SECRET_KEY="$SECRET_KEY" --app "$APP_NAME"
heroku config:set DEBUG=False --app "$APP_NAME"
heroku config:set ALLOWED_HOSTS=".herokuapp.com" --app "$APP_NAME"

echo ""
echo -e "${GREEN}✓ Variáveis de ambiente configuradas${NC}"
echo ""

# Passo 3: Configurar Git Remote
echo "=========================================="
echo "Passo 3: Configurar Git Remote"
echo "=========================================="
echo ""

cd /Users/anderson/my_folders/repositoriolocal/PBE_25.2_8001_IV

if git remote | grep -q heroku; then
    echo "Remote heroku já existe, atualizando..."
    git remote set-url heroku https://git.heroku.com/plataformacasa.git
else
    echo "Adicionando remote heroku..."
    heroku git:remote -a "$APP_NAME"
fi

echo -e "${GREEN}✓ Git remote configurado${NC}"
echo ""

# Passo 4: Commit e Deploy
echo "=========================================="
echo "Passo 4: Deploy do Código"
echo "=========================================="
echo ""

# Verifica se há alterações não commitadas
if ! git diff-index --quiet HEAD --; then
    echo "Há alterações não commitadas. Fazendo commit..."
    git add .
    git commit -m "Deploy: Configuração completa para Heroku com PostgreSQL"
fi

echo "Iniciando deploy para Heroku..."
echo -e "${YELLOW}Isso pode levar alguns minutos...${NC}"
echo ""

git push heroku anderon:main

echo ""
echo -e "${GREEN}✓ Deploy concluído${NC}"
echo ""

# Passo 5: Executar Migrações
echo "=========================================="
echo "Passo 5: Executar Migrações do Banco"
echo "=========================================="
echo ""

heroku run python meuprojeto/manage.py migrate --app "$APP_NAME"

echo ""
echo -e "${GREEN}✓ Migrações executadas${NC}"
echo ""

# Passo 6: Coletar Arquivos Estáticos
echo "=========================================="
echo "Passo 6: Coletar Arquivos Estáticos"
echo "=========================================="
echo ""

heroku run python meuprojeto/manage.py collectstatic --noinput --app "$APP_NAME"

echo ""
echo -e "${GREEN}✓ Arquivos estáticos coletados${NC}"
echo ""

# Passo 7: Criar Superusuário
echo "=========================================="
echo "Passo 7: Criar Superusuário"
echo "=========================================="
echo ""
read "CREATE_SUPER?Deseja criar um superusuário agora? (s/n): "

if [[ "$CREATE_SUPER" =~ ^[sS]$ ]]; then
    heroku run python meuprojeto/manage.py createsuperuser --app "$APP_NAME"
    echo ""
    echo -e "${GREEN}✓ Superusuário criado${NC}"
else
    echo -e "${YELLOW}Você pode criar depois com:${NC}"
    echo "heroku run python meuprojeto/manage.py createsuperuser --app $APP_NAME"
fi

echo ""

# Finalização
echo "=========================================="
echo -e "${GREEN}DEPLOY CONCLUÍDO COM SUCESSO!${NC}"
echo "=========================================="
echo ""
echo -e "${BLUE}Aplicação:${NC} $APP_NAME"
echo -e "${BLUE}URL:${NC} https://plataformacasa-f820a0a16535.herokuapp.com/"
echo ""
echo "Comandos úteis:"
echo "  Ver logs:           heroku logs --tail --app $APP_NAME"
echo "  Abrir aplicação:    heroku open --app $APP_NAME"
echo "  Console Django:     heroku run python meuprojeto/manage.py shell --app $APP_NAME"
echo "  Status:             heroku ps --app $APP_NAME"
echo "  Config:             heroku config --app $APP_NAME"
echo ""

# Abre aplicação no navegador
read "OPEN_APP?Deseja abrir a aplicação no navegador? (s/n): "
if [[ "$OPEN_APP" =~ ^[sS]$ ]]; then
    heroku open --app "$APP_NAME"
fi

echo ""
echo -e "${GREEN}Deploy finalizado!${NC}"
echo ""
