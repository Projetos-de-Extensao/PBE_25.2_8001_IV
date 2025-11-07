# 🚀 Guia de Deploy - Plataforma CASA (Heroku)

## 📋 Pré-requisitos

1. ✅ Conta no Heroku (https://heroku.com)
2. ✅ Heroku CLI instalado (https://devcenter.heroku.com/articles/heroku-cli)
3. ✅ Git instalado e configurado
4. ✅ Projeto commitado no Git

## 🔧 Verificação do Ambiente Local

Antes de fazer deploy, verifique se tudo está funcionando localmente:

```bash
# No diretório meuprojeto
cd /Users/anderson/my_folders/repositoriolocal/PBE_25.2_8001_IV/meuprojeto

# Teste o servidor local
python manage.py runserver
```

## 📦 Passo 1: Login no Heroku

```bash
# Login via CLI
heroku login

# Ou via browser
heroku login -i
```

## 🆕 Passo 2: Criar Aplicação no Heroku

```bash
# No diretório raiz do projeto
cd /Users/anderson/my_folders/repositoriolocal/PBE_25.2_8001_IV

# Criar app (escolha um nome único)
heroku create plataformacasa-ibmec

# Ou deixe o Heroku gerar um nome aleatório
heroku create
```

## 🔐 Passo 3: Configurar Variáveis de Ambiente

```bash
# SECRET_KEY (gere uma nova chave secreta)
heroku config:set SECRET_KEY='sua-chave-secreta-super-segura-aqui-2025'

# DEBUG (SEMPRE False em produção)
heroku config:set DEBUG=False

# ALLOWED_HOSTS (substitua pelo domínio gerado pelo Heroku)
heroku config:set ALLOWED_HOSTS='plataformacasa-ibmec.herokuapp.com'

# CSRF_TRUSTED_ORIGINS
heroku config:set CSRF_TRUSTED_ORIGINS='https://plataformacasa-ibmec.herokuapp.com'

# CORS (opcional - já configurado como True no settings.py)
heroku config:set CORS_ALLOW_ALL_ORIGINS=True

# DATABASE_URL será configurado automaticamente quando adicionar PostgreSQL
```

## 🗄️ Passo 4: Adicionar PostgreSQL

```bash
# Adiciona PostgreSQL gratuito (Hobby Dev)
heroku addons:create heroku-postgresql:essential-0

# Verificar se foi criado
heroku config:get DATABASE_URL
```

## 📤 Passo 5: Deploy do Código

```bash
# Garantir que está no branch main
git checkout main

# Adicionar remote do Heroku (se ainda não foi adicionado)
heroku git:remote -a plataformacasa-ibmec

# Fazer commit de todas as mudanças
git add .
git commit -m "Deploy: Configurações de produção"

# Push para o Heroku
git push heroku main
```

## 🔄 Passo 6: Executar Migrações

```bash
# Rodar migrações no banco de dados
heroku run python meuprojeto/manage.py migrate

# Criar superusuário (admin)
heroku run python meuprojeto/manage.py createsuperuser

# Coletar arquivos estáticos
heroku run python meuprojeto/manage.py collectstatic --noinput
```

## 📊 Passo 7: Popular Dados Iniciais (Opcional)

```bash
# Popular disciplinas
heroku run python meuprojeto/popular_disciplinas.py

# Ou via manage.py shell
heroku run python meuprojeto/manage.py shell
```

## ✅ Passo 8: Verificar Deploy

```bash
# Abrir aplicação no browser
heroku open

# Ver logs em tempo real
heroku logs --tail

# Ver status da aplicação
heroku ps
```

## 🔍 URLs Importantes

Após o deploy, sua aplicação estará disponível em:

- **App Principal**: https://plataformacasa-ibmec.herokuapp.com/
- **Admin Django**: https://plataformacasa-ibmec.herokuapp.com/admin/
- **API Docs (Swagger)**: https://plataformacasa-ibmec.herokuapp.com/swagger/
- **API Docs (ReDoc)**: https://plataformacasa-ibmec.herokuapp.com/redoc/

## 🐛 Troubleshooting

### Erro: "Application Error"

```bash
# Ver logs detalhados
heroku logs --tail

# Reiniciar dyno
heroku restart
```

### Erro: "collectstatic failed"

```bash
# Executar manualmente
heroku run python meuprojeto/manage.py collectstatic --noinput

# Se persistir, desabilitar temporariamente
heroku config:set DISABLE_COLLECTSTATIC=1
```

### Erro: "Database connection refused"

```bash
# Verificar se PostgreSQL está ativo
heroku pg:info

# Resetar database (CUIDADO: apaga todos os dados!)
heroku pg:reset DATABASE_URL
heroku run python meuprojeto/manage.py migrate
```

### Erro: "Secret Key não configurada"

```bash
# Gerar nova SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Configurar no Heroku
heroku config:set SECRET_KEY='nova-chave-gerada'
```

## 📝 Comandos Úteis

```bash
# Ver todas as variáveis de ambiente
heroku config

# Editar variável
heroku config:set NOME_VARIAVEL=valor

# Remover variável
heroku config:unset NOME_VARIAVEL

# Ver informações do app
heroku info

# Acessar console do Django
heroku run python meuprojeto/manage.py shell

# Backup do banco de dados
heroku pg:backups:capture
heroku pg:backups:download

# Escalar dynos (aumentar capacidade)
heroku ps:scale web=1

# Ver uso de recursos
heroku ps

# Reiniciar aplicação
heroku restart
```

## 🔄 Atualizações Futuras

Para atualizar o código após mudanças:

```bash
# 1. Fazer commit das mudanças
git add .
git commit -m "Descrição das mudanças"

# 2. Push para o Heroku
git push heroku main

# 3. Se houver novas migrações
heroku run python meuprojeto/manage.py migrate

# 4. Coletar novos arquivos estáticos (se necessário)
heroku run python meuprojeto/manage.py collectstatic --noinput

# 5. Reiniciar (opcional)
heroku restart
```

## 📧 Configuração de Email (Opcional)

Para enviar emails em produção:

```bash
# Configurar servidor SMTP
heroku config:set EMAIL_HOST='smtp.gmail.com'
heroku config:set EMAIL_PORT=587
heroku config:set EMAIL_HOST_USER='seu-email@gmail.com'
heroku config:set EMAIL_HOST_PASSWORD='sua-senha-de-app'
heroku config:set EMAIL_USE_TLS=True
```

## 🔒 Segurança em Produção

Verificações importantes:

- ✅ `DEBUG=False`
- ✅ `SECRET_KEY` única e secreta
- ✅ `ALLOWED_HOSTS` configurado corretamente
- ✅ `CSRF_TRUSTED_ORIGINS` configurado
- ✅ PostgreSQL configurado (não usar SQLite em produção)
- ✅ HTTPS habilitado (automático no Heroku)
- ✅ Arquivos estáticos servidos pelo WhiteNoise

## 📊 Monitoramento

```bash
# Ver métricas de uso
heroku ps

# Ver logs de acesso
heroku logs --tail --dyno web

# Ver logs de erros
heroku logs --tail | grep ERROR
```

## 💰 Custos (Free Tier)

- **Dyno Web**: Gratuito (550-1000 horas/mês)
- **PostgreSQL Hobby Dev**: Gratuito (10.000 linhas)
- **HTTPS/SSL**: Gratuito (automático)

⚠️ **Nota**: Dynos gratuitos "dormem" após 30 minutos de inatividade. Upgrade para Hobby ($7/mês) para manter ativo 24/7.

## 🎉 Deploy Completo!

Após seguir todos os passos, sua aplicação estará online em:
**https://[seu-app].herokuapp.com**

---

📝 **Última atualização**: 7 de novembro de 2025
🚀 **Plataforma CASA - Ibmec/RJ**
