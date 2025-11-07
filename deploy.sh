#!/bin/bash

# 🚀 Script de Deploy Automatizado - Plataforma CASA
# Autor: Sistema CASA - Ibmec/RJ
# Data: 7 de novembro de 2025

echo "🚀 =========================================="
echo "   DEPLOY - PLATAFORMA CASA (Heroku)"
echo "=========================================="
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para printar com cor
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Verificar se está no diretório correto
if [ ! -f "Procfile" ]; then
    print_error "Procfile não encontrado! Execute este script no diretório raiz do projeto."
    exit 1
fi

print_success "Procfile encontrado!"

# Verificar se Heroku CLI está instalado
if ! command -v heroku &> /dev/null; then
    print_error "Heroku CLI não está instalado!"
    print_info "Instale em: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

print_success "Heroku CLI detectado!"

# Verificar se está logado no Heroku
if ! heroku auth:whoami &> /dev/null; then
    print_warning "Você não está logado no Heroku. Fazendo login..."
    heroku login
fi

print_success "Autenticado no Heroku!"

# Perguntar o nome do app
echo ""
print_info "Digite o nome do app Heroku (ou pressione ENTER para criar um novo):"
read -p "Nome do app: " APP_NAME

if [ -z "$APP_NAME" ]; then
    print_warning "Criando novo app com nome aleatório..."
    heroku create
    APP_NAME=$(heroku apps:info -j | python -c "import sys, json; print(json.load(sys.stdin)['app']['name'])")
    print_success "App criado: $APP_NAME"
else
    # Verificar se o app existe
    if heroku apps:info -a "$APP_NAME" &> /dev/null; then
        print_info "App '$APP_NAME' já existe. Usando este app."
    else
        print_warning "App '$APP_NAME' não existe. Criando..."
        heroku create "$APP_NAME"
        print_success "App criado: $APP_NAME"
    fi
fi

# Adicionar remote do Heroku
heroku git:remote -a "$APP_NAME"
print_success "Remote do Heroku configurado!"

# Configurar variáveis de ambiente
echo ""
print_info "Configurando variáveis de ambiente..."

# Gerar SECRET_KEY se não existir
if ! heroku config:get SECRET_KEY -a "$APP_NAME" &> /dev/null; then
    print_warning "Gerando SECRET_KEY..."
    SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
    heroku config:set SECRET_KEY="$SECRET_KEY" -a "$APP_NAME"
    print_success "SECRET_KEY configurada!"
fi

# Configurar DEBUG=False
heroku config:set DEBUG=False -a "$APP_NAME"
print_success "DEBUG=False configurado!"

# Configurar ALLOWED_HOSTS
heroku config:set ALLOWED_HOSTS="$APP_NAME.herokuapp.com" -a "$APP_NAME"
print_success "ALLOWED_HOSTS configurado!"

# Configurar CSRF_TRUSTED_ORIGINS
heroku config:set CSRF_TRUSTED_ORIGINS="https://$APP_NAME.herokuapp.com" -a "$APP_NAME"
print_success "CSRF_TRUSTED_ORIGINS configurado!"

# Configurar CORS
heroku config:set CORS_ALLOW_ALL_ORIGINS=True -a "$APP_NAME"
print_success "CORS configurado!"

# Verificar se PostgreSQL está instalado
echo ""
print_info "Verificando PostgreSQL..."
if ! heroku addons -a "$APP_NAME" | grep -q "heroku-postgresql"; then
    print_warning "PostgreSQL não encontrado. Instalando..."
    heroku addons:create heroku-postgresql:essential-0 -a "$APP_NAME"
    print_success "PostgreSQL instalado!"
else
    print_success "PostgreSQL já está instalado!"
fi

# Garantir que todas as mudanças estão commitadas
echo ""
print_info "Verificando git status..."
if [[ -n $(git status -s) ]]; then
    print_warning "Existem mudanças não commitadas."
    echo ""
    print_info "Deseja commitar todas as mudanças? (s/n)"
    read -p "Resposta: " COMMIT_CHANGES
    
    if [ "$COMMIT_CHANGES" = "s" ] || [ "$COMMIT_CHANGES" = "S" ]; then
        git add .
        git commit -m "Deploy: Atualizações $(date '+%Y-%m-%d %H:%M:%S')"
        print_success "Mudanças commitadas!"
    else
        print_error "Deploy cancelado. Commit as mudanças manualmente e tente novamente."
        exit 1
    fi
else
    print_success "Repositório limpo!"
fi

# Deploy
echo ""
print_info "=========================================="
print_info "   INICIANDO DEPLOY..."
print_info "=========================================="
echo ""

git push heroku main

if [ $? -eq 0 ]; then
    print_success "Deploy realizado com sucesso!"
else
    print_error "Erro no deploy. Verifique os logs acima."
    exit 1
fi

# Executar migrações
echo ""
print_info "Executando migrações..."
heroku run python meuprojeto/manage.py migrate -a "$APP_NAME"
print_success "Migrações concluídas!"

# Coletar arquivos estáticos
echo ""
print_info "Coletando arquivos estáticos..."
heroku run python meuprojeto/manage.py collectstatic --noinput -a "$APP_NAME"
print_success "Arquivos estáticos coletados!"

# Perguntar se deseja criar superusuário
echo ""
print_info "Deseja criar um superusuário (admin)? (s/n)"
read -p "Resposta: " CREATE_SUPERUSER

if [ "$CREATE_SUPERUSER" = "s" ] || [ "$CREATE_SUPERUSER" = "S" ]; then
    heroku run python meuprojeto/manage.py createsuperuser -a "$APP_NAME"
    print_success "Superusuário criado!"
fi

# Perguntar se deseja popular disciplinas
echo ""
print_info "Deseja popular disciplinas iniciais? (s/n)"
read -p "Resposta: " POPULATE_DISCIPLINES

if [ "$POPULATE_DISCIPLINES" = "s" ] || [ "$POPULATE_DISCIPLINES" = "S" ]; then
    heroku run python meuprojeto/popular_disciplinas.py -a "$APP_NAME"
    print_success "Disciplinas populadas!"
fi

# Finalização
echo ""
print_success "=========================================="
print_success "   DEPLOY CONCLUÍDO COM SUCESSO!"
print_success "=========================================="
echo ""
print_info "📱 URL da aplicação: https://$APP_NAME.herokuapp.com"
print_info "🔧 Admin Django: https://$APP_NAME.herokuapp.com/admin/"
print_info "📚 API Docs (Swagger): https://$APP_NAME.herokuapp.com/swagger/"
print_info "📖 API Docs (ReDoc): https://$APP_NAME.herokuapp.com/redoc/"
echo ""
print_info "Comandos úteis:"
print_info "  heroku logs --tail -a $APP_NAME       # Ver logs em tempo real"
print_info "  heroku open -a $APP_NAME              # Abrir no navegador"
print_info "  heroku ps -a $APP_NAME                # Ver status dos dynos"
print_info "  heroku restart -a $APP_NAME           # Reiniciar aplicação"
echo ""

# Perguntar se deseja abrir no navegador
print_info "Deseja abrir a aplicação no navegador? (s/n)"
read -p "Resposta: " OPEN_BROWSER

if [ "$OPEN_BROWSER" = "s" ] || [ "$OPEN_BROWSER" = "S" ]; then
    heroku open -a "$APP_NAME"
fi

print_success "🎉 Deploy finalizado!"
