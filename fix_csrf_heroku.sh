#!/bin/bash

################################################################################
#                    SCRIPT DE CORREÇÃO CSRF - HEROKU                         #
################################################################################
# 
# Descrição:
# Script automatizado para configurar variáveis de ambiente necessárias
# para corrigir o erro 403 CSRF em produção (Heroku)
#
# Uso:
#   chmod +x fix_csrf_heroku.sh
#   ./fix_csrf_heroku.sh
#
# Autor: Equipe de Desenvolvimento - Plataforma Casa
# Data: Outubro 2025
#
################################################################################

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         CORREÇÃO: Erro 403 CSRF - Heroku Setup                 ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo

# 1. Solicitar informações
echo -e "${YELLOW}📝 Informações Necessárias:${NC}"
echo
read -p "Nome da aplicação no Heroku (ex: plataformacasa-f820a0a16535): " APP_NAME

if [ -z "$APP_NAME" ]; then
    echo -e "${RED}❌ Nome da aplicação não fornecido!${NC}"
    exit 1
fi

read -p "Domínio da aplicação (ex: plataformacasa-f820a0a16535.herokuapp.com): " APP_DOMAIN

if [ -z "$APP_DOMAIN" ]; then
    echo -e "${RED}❌ Domínio não fornecido!${NC}"
    exit 1
fi

read -p "SECRET_KEY (deixe em branco para usar existente): " SECRET_KEY

echo
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}🔧 Configurando variáveis de ambiente no Heroku...${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo

# 2. Configurar variáveis de ambiente
echo -e "${YELLOW}1️⃣  Configurando ALLOWED_HOSTS...${NC}"
heroku config:set ALLOWED_HOSTS="localhost,127.0.0.1,$APP_DOMAIN" --app "$APP_NAME"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ ALLOWED_HOSTS configurado${NC}"
else
    echo -e "${RED}❌ Erro ao configurar ALLOWED_HOSTS${NC}"
    exit 1
fi

echo
echo -e "${YELLOW}2️⃣  Configurando CSRF_TRUSTED_ORIGINS...${NC}"
heroku config:set CSRF_TRUSTED_ORIGINS="https://$APP_DOMAIN" --app "$APP_NAME"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ CSRF_TRUSTED_ORIGINS configurado${NC}"
else
    echo -e "${RED}❌ Erro ao configurar CSRF_TRUSTED_ORIGINS${NC}"
    exit 1
fi

echo
echo -e "${YELLOW}3️⃣  Configurando DEBUG=False...${NC}"
heroku config:set DEBUG=False --app "$APP_NAME"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ DEBUG desativado${NC}"
else
    echo -e "${RED}❌ Erro ao configurar DEBUG${NC}"
    exit 1
fi

echo
echo -e "${YELLOW}4️⃣  Configurando SECURE_SSL_REDIRECT=True...${NC}"
heroku config:set SECURE_SSL_REDIRECT=True --app "$APP_NAME"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ SECURE_SSL_REDIRECT ativado${NC}"
else
    echo -e "${RED}❌ Erro ao configurar SECURE_SSL_REDIRECT${NC}"
    exit 1
fi

echo
echo -e "${YELLOW}5️⃣  Configurando CSRF_COOKIE_SECURE=True...${NC}"
heroku config:set CSRF_COOKIE_SECURE=True --app "$APP_NAME"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ CSRF_COOKIE_SECURE ativado${NC}"
else
    echo -e "${RED}❌ Erro ao configurar CSRF_COOKIE_SECURE${NC}"
    exit 1
fi

echo
echo -e "${YELLOW}6️⃣  Configurando SESSION_COOKIE_SECURE=True...${NC}"
heroku config:set SESSION_COOKIE_SECURE=True --app "$APP_NAME"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ SESSION_COOKIE_SECURE ativado${NC}"
else
    echo -e "${RED}❌ Erro ao configurar SESSION_COOKIE_SECURE${NC}"
    exit 1
fi

if [ -n "$SECRET_KEY" ]; then
    echo
    echo -e "${YELLOW}7️⃣  Configurando SECRET_KEY...${NC}"
    heroku config:set SECRET_KEY="$SECRET_KEY" --app "$APP_NAME"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ SECRET_KEY configurado${NC}"
    else
        echo -e "${RED}❌ Erro ao configurar SECRET_KEY${NC}"
        exit 1
    fi
fi

# 3. Verificar configurações
echo
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}📋 Verificando configurações...${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo

heroku config --app "$APP_NAME" | grep -E "ALLOWED_HOSTS|CSRF|DEBUG|SECURE|SESSION"

# 4. Deploy
echo
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}🚀 Próximas etapas:${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo
echo "1. Fazer commit das alterações:"
echo -e "${GREEN}   git add meuprojeto/settings.py${NC}"
echo -e "${GREEN}   git commit -m \"fix: Corrigir verificação CSRF com proxy reverso Heroku\"${NC}"
echo
echo "2. Deploy para Heroku:"
echo -e "${GREEN}   git push heroku main${NC}"
echo
echo "3. Teste de login:"
echo -e "${GREEN}   https://$APP_DOMAIN/login/${NC}"
echo
echo "4. Monitorar logs (se houver problemas):"
echo -e "${GREEN}   heroku logs --tail --app $APP_NAME${NC}"
echo
echo -e "${GREEN}✅ Configuração concluída!${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
