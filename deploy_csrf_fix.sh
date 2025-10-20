#!/bin/bash

# 🚀 COMANDOS ESSENCIAIS - Correção CSRF 403 em Heroku
# 
# Use este arquivo como referência rápida de comandos
# Copie e adapte os comandos conforme necessário

echo "
╔════════════════════════════════════════════════════════════════╗
║    CORREÇÃO: Erro 403 CSRF - Comandos Essenciais              ║
╚════════════════════════════════════════════════════════════════╝
"

# ============================================================================
# PASSO 1: DEFINIR VARIÁVEIS
# ============================================================================

APP_NAME="plataformacasa-f820a0a16535"  # ← MUDE AQUI
APP_DOMAIN="plataformacasa-f820a0a16535.herokuapp.com"  # ← E AQUI

echo "
📝 Variáveis configuradas:
   APP_NAME: $APP_NAME
   APP_DOMAIN: $APP_DOMAIN

Se estiver errado, edite este arquivo!
"

# ============================================================================
# PASSO 2: CONFIGURAR VARIÁVEIS DE AMBIENTE
# ============================================================================

echo "
🔧 Passo 1: Configurando variáveis de ambiente no Heroku...
"

echo "  ➜ ALLOWED_HOSTS..."
heroku config:set ALLOWED_HOSTS="localhost,127.0.0.1,$APP_DOMAIN" --app "$APP_NAME"

echo "  ➜ CSRF_TRUSTED_ORIGINS..."
heroku config:set CSRF_TRUSTED_ORIGINS="https://$APP_DOMAIN" --app "$APP_NAME"

echo "  ➜ DEBUG..."
heroku config:set DEBUG=False --app "$APP_NAME"

echo "  ➜ SECURE_SSL_REDIRECT..."
heroku config:set SECURE_SSL_REDIRECT=True --app "$APP_NAME"

echo "  ➜ CSRF_COOKIE_SECURE..."
heroku config:set CSRF_COOKIE_SECURE=True --app "$APP_NAME"

echo "  ➜ SESSION_COOKIE_SECURE..."
heroku config:set SESSION_COOKIE_SECURE=True --app "$APP_NAME"

# ============================================================================
# PASSO 3: VERIFICAR CONFIGURAÇÕES
# ============================================================================

echo "
✅ Verificando configurações...
"

heroku config --app "$APP_NAME" | grep -E "ALLOWED_HOSTS|CSRF|DEBUG|SECURE|SESSION"

# ============================================================================
# PASSO 4: COMMIT E DEPLOY
# ============================================================================

echo "
📤 Passo 2: Deploy para Heroku
"

echo "  ➜ Adicionando arquivos modificados..."
git add meuprojeto/settings.py

echo "  ➜ Fazendo commit..."
git commit -m "fix: Corrigir verificação CSRF com proxy reverso Heroku"

echo "  ➜ Push para Heroku..."
git push heroku main

# ============================================================================
# PASSO 5: MONITORAR LOGS
# ============================================================================

echo "
👀 Passo 3: Monitorando logs...
(Pressione CTRL+C para parar)
"

heroku logs --tail --app "$APP_NAME"

# ============================================================================
# PASSO 6: TESTAR LOGIN
# ============================================================================

echo "
✅ Teste concluído!

🌐 Acesse: https://$APP_DOMAIN/login/

📋 Credenciais de teste:
   Professor: professor.teste / professor123
   Monitor:   monitor.teste / monitor123
   Admin:     admin / admin123
   Aluno:     aluno.teste / aluno123

Se o login funcionar, a correção foi bem-sucedida! 🎉
"
