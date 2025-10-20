# Checklist Pré-Deploy - Heroku

## Arquivos Criados

- [x] Procfile - Define comando para iniciar aplicação
- [x] runtime.txt - Especifica versão do Python
- [x] requirements.txt - Atualizado com dependências de produção
- [x] .env.example - Template de variáveis de ambiente
- [x] .env - Arquivo local (não commitado)
- [x] .gitignore - Atualizado para proteger arquivos sensíveis
- [x] DEPLOY_HEROKU.md - Documentação completa de deploy

## Configurações Realizadas no settings.py

- [x] Importação de dj_database_url e python-decouple
- [x] SECRET_KEY via variável de ambiente
- [x] DEBUG via variável de ambiente
- [x] ALLOWED_HOSTS via variável de ambiente
- [x] WhiteNoise no MIDDLEWARE
- [x] Configuração dual de banco (SQLite local / PostgreSQL produção)
- [x] STATIC_ROOT configurado
- [x] STATICFILES_STORAGE com WhiteNoise
- [x] Configurações de segurança HTTPS
- [x] HSTS habilitado
- [x] Proteções XSS e Clickjacking

## Dependências Instaladas

- [x] Django==5.2
- [x] psycopg2-binary==2.9.10 (adaptador PostgreSQL)
- [x] gunicorn==23.0.0 (servidor WSGI)
- [x] whitenoise==6.8.2 (arquivos estáticos)
- [x] dj-database-url==2.2.0 (configuração DB)
- [x] python-decouple==3.8 (variáveis ambiente)

## Testes Locais Antes do Deploy

- [x] python manage.py check (sem erros)
- [ ] python manage.py makemigrations (verificar se há pendências)
- [ ] python manage.py migrate (aplicar migrações)
- [ ] python manage.py collectstatic (coletar arquivos estáticos)
- [ ] python manage.py runserver (testar localmente)

## Comandos para Executar Antes do Deploy

```bash
# Entrar na pasta do projeto
cd /Users/anderson/my_folders/repositoriolocal/PBE_25.2_8001_IV/meuprojeto

# Verificar sistema
/Users/anderson/my_folders/repositoriolocal/PBE_25.2_8001_IV/.venv/bin/python manage.py check

# Criar migrações se necessário
/Users/anderson/my_folders/repositoriolocal/PBE_25.2_8001_IV/.venv/bin/python manage.py makemigrations

# Aplicar migrações
/Users/anderson/my_folders/repositoriolocal/PBE_25.2_8001_IV/.venv/bin/python manage.py migrate

# Coletar arquivos estáticos
/Users/anderson/my_folders/repositoriolocal/PBE_25.2_8001_IV/.venv/bin/python manage.py collectstatic --noinput

# Testar servidor local
/Users/anderson/my_folders/repositoriolocal/PBE_25.2_8001_IV/.venv/bin/python manage.py runserver
```

## Antes de Fazer o Deploy na Heroku

1. [ ] Commit de todas as alterações
2. [ ] Push para repositório Git
3. [ ] Instalar Heroku CLI
4. [ ] Fazer login na Heroku
5. [ ] Criar aplicação na Heroku
6. [ ] Adicionar PostgreSQL addon
7. [ ] Configurar variáveis de ambiente
8. [ ] Fazer push para Heroku
9. [ ] Executar migrações remotas
10. [ ] Criar superusuário remoto
11. [ ] Testar aplicação em produção

## Variáveis de Ambiente para Configurar na Heroku

```bash
# Gerar nova SECRET_KEY segura
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Configurar variáveis
heroku config:set SECRET_KEY="<chave-gerada-acima>"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=".herokuapp.com"
```

## Notas Importantes

1. O arquivo .env contém SECRET_KEY de desenvolvimento e NÃO deve ser commitado
2. Em produção, gerar nova SECRET_KEY exclusiva
3. DATABASE_URL é configurada automaticamente pela Heroku ao adicionar PostgreSQL
4. WhiteNoise serve arquivos estáticos, não é necessário AWS S3 inicialmente
5. Para arquivos de media (uploads), considerar AWS S3 em produção futura

## Estrutura de Custos Inicial

- PostgreSQL Essential 0: $5/mês
- Eco Dyno: $5/mês
- **Total mínimo:** $10/mês

## Próximos Passos Após Deploy

1. Configurar domínio customizado (opcional)
2. Configurar backups automáticos do banco
3. Implementar sistema de logs e monitoramento
4. Configurar AWS S3 para arquivos de media (uploads)
5. Implementar CDN para arquivos estáticos (opcional)
6. Configurar SSL customizado se usar domínio próprio
