# ✅ Checklist de Deploy - Plataforma CASA

## 🔍 Antes do Deploy

### Configurações Essenciais
- [x] `Procfile` configurado corretamente
- [x] `runtime.txt` com versão Python correta (3.12.8)
- [x] `requirements.txt` atualizado com todas as dependências
- [x] `settings.py` configurado para produção:
  - [x] DEBUG usa variável de ambiente
  - [x] SECRET_KEY usa variável de ambiente
  - [x] ALLOWED_HOSTS configurável
  - [x] CSRF_TRUSTED_ORIGINS configurável
  - [x] CORS configurado
  - [x] WhiteNoise para arquivos estáticos
  - [x] PostgreSQL via dj-database-url

### Arquivos Estáticos
- [x] `STATIC_ROOT` configurado
- [x] `STATICFILES_STORAGE` usando WhiteNoise
- [x] `collectstatic` testado localmente

### Banco de Dados
- [x] Todas as migrações criadas
- [x] Migrações testadas localmente
- [ ] Backup do banco local (se houver dados importantes)

### Código
- [x] Código testado localmente
- [ ] Todas as mudanças commitadas no Git
- [ ] Branch main atualizada
- [ ] Sem erros de sintaxe ou imports

## 🚀 Durante o Deploy

### Opção 1: Script Automatizado (Recomendado)

```bash
# Executar o script de deploy
./deploy.sh
```

O script irá:
- ✅ Verificar Heroku CLI
- ✅ Criar/configurar app
- ✅ Configurar variáveis de ambiente
- ✅ Instalar PostgreSQL
- ✅ Fazer deploy do código
- ✅ Executar migrações
- ✅ Coletar arquivos estáticos
- ✅ Criar superusuário (opcional)
- ✅ Popular disciplinas (opcional)

### Opção 2: Manual

```bash
# 1. Login no Heroku
heroku login

# 2. Criar app
heroku create plataformacasa-ibmec

# 3. Configurar variáveis
heroku config:set SECRET_KEY='sua-chave-secreta'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS='plataformacasa-ibmec.herokuapp.com'
heroku config:set CSRF_TRUSTED_ORIGINS='https://plataformacasa-ibmec.herokuapp.com'

# 4. Adicionar PostgreSQL
heroku addons:create heroku-postgresql:essential-0

# 5. Deploy
git push heroku main

# 6. Migrações
heroku run python meuprojeto/manage.py migrate

# 7. Arquivos estáticos
heroku run python meuprojeto/manage.py collectstatic --noinput

# 8. Criar admin
heroku run python meuprojeto/manage.py createsuperuser

# 9. Popular disciplinas
heroku run python meuprojeto/popular_disciplinas.py
```

## ✅ Após o Deploy

### Verificações Básicas
- [ ] Aplicação abre sem erros
- [ ] CSS/JavaScript carregando corretamente
- [ ] Login funcionando
- [ ] Admin acessível
- [ ] API Swagger acessível

### Testes Funcionais
- [ ] Criar conta de usuário
- [ ] Login com email e senha
- [ ] Visualizar vagas
- [ ] Cadastrar disciplina (professor/admin)
- [ ] Criar vaga (coordenador/admin)
- [ ] Upload de documentos
- [ ] Modal de detalhes funcionando

### Páginas Principais
- [ ] Home/Landing Page
- [ ] Portal de Vagas
- [ ] Login/Registro
- [ ] Dashboard (usuário logado)
- [ ] Admin Django
- [ ] API Swagger: `/swagger/`
- [ ] API ReDoc: `/redoc/`

### Segurança
- [ ] HTTPS ativo (automático no Heroku)
- [ ] DEBUG=False confirmado
- [ ] SECRET_KEY única e segura
- [ ] CORS configurado corretamente
- [ ] CSRF protection ativo

## 🐛 Troubleshooting

### Se algo der errado:

```bash
# Ver logs em tempo real
heroku logs --tail

# Ver apenas erros
heroku logs --tail | grep ERROR

# Reiniciar aplicação
heroku restart

# Verificar variáveis de ambiente
heroku config

# Verificar status dos dynos
heroku ps

# Acessar console Django
heroku run python meuprojeto/manage.py shell
```

### Problemas Comuns

1. **Aplicação não abre**: Verifique logs com `heroku logs --tail`
2. **CSS não carrega**: Execute `heroku run python meuprojeto/manage.py collectstatic --noinput`
3. **Database error**: Verifique se PostgreSQL está ativo com `heroku pg:info`
4. **Secret key error**: Configure com `heroku config:set SECRET_KEY='nova-chave'`
5. **CSRF error**: Configure `CSRF_TRUSTED_ORIGINS` com domínio completo

## 📊 Monitoramento

### Métricas Importantes
- [ ] Tempo de resposta das páginas
- [ ] Uso de memória do dyno
- [ ] Número de requisições
- [ ] Taxa de erros

```bash
# Ver uso de recursos
heroku ps

# Ver métricas (requer add-on)
heroku addons:create newrelic:wayne
```

## 🔄 Atualizações Futuras

Para atualizar o código:

```bash
# 1. Fazer mudanças no código
# 2. Testar localmente
# 3. Commit
git add .
git commit -m "Descrição das mudanças"

# 4. Deploy
git push heroku main

# 5. Se houver novas migrações
heroku run python meuprojeto/manage.py migrate

# 6. Reiniciar (se necessário)
heroku restart
```

## 📝 Comandos de Manutenção

```bash
# Backup do banco de dados
heroku pg:backups:capture
heroku pg:backups:download

# Ver tamanho do banco
heroku pg:info

# Ver conexões ativas
heroku pg:psql -c "SELECT * FROM pg_stat_activity;"

# Resetar banco (CUIDADO!)
heroku pg:reset DATABASE_URL
heroku run python meuprojeto/manage.py migrate
```

## 🎉 Deploy Completo!

Quando todos os checkboxes estiverem marcados, seu deploy está completo e a aplicação está em produção!

---

📅 **Data**: 7 de novembro de 2025
🚀 **Plataforma CASA - Ibmec/RJ**
