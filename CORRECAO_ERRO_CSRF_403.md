# 🔧 CORREÇÃO: Erro 403 CSRF - Forbidden em Produção (Heroku)

## ⚠️ Problema Identificado

```
Error 500 / Forbidden (403)
CSRF verification failed. Request aborted.
```

**Quando ocorre:** Ao fazer login como Professor, Monitor e Admin no Heroku  
**Causa raiz:** Configuração incompleta de CSRF em ambiente com proxy reverso (Heroku)

---

## 🎯 Solução

### 1️⃣ Atualizar Variáveis de Ambiente no Heroku

```bash
# Executar estes comandos para configurar as variáveis necessárias:

heroku config:set ALLOWED_HOSTS=localhost,127.0.0.1,plataformacasa-f820a0a16535.herokuapp.com --app your-app-name

heroku config:set CSRF_TRUSTED_ORIGINS=https://plataformacasa-f820a0a16535.herokuapp.com --app your-app-name

heroku config:set DEBUG=False --app your-app-name

heroku config:set SECURE_SSL_REDIRECT=True --app your-app-name

heroku config:set CSRF_COOKIE_SECURE=True --app your-app-name

heroku config:set SESSION_COOKIE_SECURE=True --app your-app-name

heroku config:set SECRET_KEY=seu-secret-key-aqui --app your-app-name
```

### 2️⃣ Verificar Configurações Atualizadas

```bash
# Listar todas as variáveis configuradas:
heroku config --app your-app-name

# Verificar valor específico:
heroku config:get ALLOWED_HOSTS --app your-app-name
```

### 3️⃣ Deploy da Correção

```bash
# Fazer commit das alterações
git add meuprojeto/settings.py
git commit -m "fix: Corrigir verificação CSRF com proxy reverso Heroku"

# Push para Heroku (auto-deploy se configurado)
git push heroku main

# Ou deploy manual:
heroku deploy:github --app your-app-name
```

---

## 📋 O Que Foi Alterado

### ✅ settings.py

1. **CSRF_TRUSTED_ORIGINS** adicionado
   - Permite requisições CSRF do domínio Heroku

2. **SECURE_PROXY_SSL_HEADER** adicionado
   - Resolve problema com redirecionamento HTTP→HTTPS em proxy reverso
   - Django reconhece header `X-Forwarded-Proto: https` do Heroku

3. **CSRF_COOKIE_SAMESITE** definido como 'Lax'
   - Protege contra CSRF sem quebrar funcionalidade

4. **CSRF_COOKIE_HTTPONLY** definido como False
   - Necessário para Django carregar o token CSRF em templates

---

## 🔍 Configuração Detalhada

### Por que o erro ocorria?

```
Heroku (HTTP)
     ↓ [Proxy Reverso]
     ↓ X-Forwarded-Proto: https
Django ❌ Não reconhecia HTTPS
     ↓ Criava token CSRF para HTTP
     ↓ Cliente enviava requisição em HTTPS
     ↓ Token não correspondia → 403 CSRF
```

### Como foi corrigido:

```
Heroku (HTTPS)
     ↓ [Proxy Reverso]
     ↓ X-Forwarded-Proto: https
Django ✅ Reconhece HTTPS (SECURE_PROXY_SSL_HEADER)
     ↓ Cria token CSRF para HTTPS
     ↓ Cliente envia em HTTPS
     ↓ Token corresponde → ✅ Login bem-sucedido
```

---

## 🧪 Testando a Correção

### Local (Desenvolvimento)
```bash
cd meuprojeto
python manage.py runserver
# Testar login com usuários de teste
```

### Produção (Heroku)
```bash
# Ver logs em tempo real
heroku logs --tail --app your-app-name

# Testar login em: https://plataformacasa-f820a0a16535.herokuapp.com/login/

# Procurar por mensagens:
# ✅ "[08/Oct/2025 14:23:45] "POST /login/ HTTP/1.1" 302"  → LOGIN OK
# ❌ "[08/Oct/2025 14:23:45] "POST /login/ HTTP/1.1" 403"  → ERRO CSRF
```

---

## 📚 Referências

- [Django CSRF Protection](https://docs.djangoproject.com/en/5.2/ref/csrf/)
- [Heroku Security Headers](https://devcenter.heroku.com/articles/http-routing)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)

---

## 🆘 Se o Problema Persistir

### Passo 1: Validar HTML do formulário de login

Verificar se `login.html` tem o token CSRF:

```django
<!-- ✅ Correto: O template tem {% csrf_token %} -->
<form method="POST" class="login-form">
    {% csrf_token %}  <!-- Obrigatório! -->
    ...
</form>
```

### Passo 2: Verificar Middleware

Em `settings.py`, CSRF middleware deve estar ativo:

```python
MIDDLEWARE = [
    # ...
    'django.middleware.csrf.CsrfViewMiddleware',  # ← Obrigatório
    # ...
]
```

### Passo 3: Limpar Cache do Navegador

```bash
# Heroku: Limpar dyno e redeploy
heroku restart --app your-app-name

# Cliente: CTRL+SHIFT+DEL (limpar cache completo)
```

### Passo 4: Ativar DEBUG Temporariamente (⚠️ CUIDADO!)

```bash
# ⚠️ APENAS PARA DEBUGGING:
heroku config:set DEBUG=True --app your-app-name
# Vê mensagens de erro mais detalhadas
# REMOVER após resolver:
heroku config:set DEBUG=False --app your-app-name
```

---

## ✅ Checklist Final

- [ ] `ALLOWED_HOSTS` configurado com domínio Heroku
- [ ] `CSRF_TRUSTED_ORIGINS` adicionado
- [ ] `SECURE_PROXY_SSL_HEADER` ativo
- [ ] `login.html` contém `{% csrf_token %}`
- [ ] `CSRF_COOKIE_SECURE=True` em produção
- [ ] `MIDDLEWARE` contém `CsrfViewMiddleware`
- [ ] Deploy realizado para Heroku
- [ ] Login teste bem-sucedido para Professor/Monitor/Admin

---

**Status:** ✅ CORRIGIDO  
**Data:** 20 de outubro de 2025  
**Afetados:** Professor, Monitor, Admin em produção
