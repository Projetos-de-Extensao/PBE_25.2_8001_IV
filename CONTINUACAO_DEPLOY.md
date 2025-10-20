# Continuação do Deploy - Plataforma Casa

## Situação Atual

- Aplicação criada: **plataformacasa**
- URL: https://plataformacasa-f820a0a16535.herokuapp.com/
- Git remote: https://git.heroku.com/plataformacasa.git
- PostgreSQL: ERRO ao adicionar (plano não encontrado)

## Solução: Adicionar PostgreSQL Manualmente

### Opção 1: Hobby-dev (Gratuito, até 10.000 linhas)

```bash
heroku addons:create heroku-postgresql:hobby-dev --app plataformacasa
```

### Opção 2: Verificar planos disponíveis

```bash
heroku addons:plans heroku-postgresql --app plataformacasa
```

Depois escolha um plano disponível:

```bash
heroku addons:create heroku-postgresql:<PLANO> --app plataformacasa
```

### Opção 3: Usar interface web

1. Acesse: https://dashboard.heroku.com/apps/plataformacasa
2. Vá em "Resources"
3. Clique em "Find more add-ons"
4. Procure por "Heroku Postgres"
5. Selecione um plano e adicione

## Após Adicionar o PostgreSQL

### 1. Gerar e Configurar SECRET_KEY

```bash
# Gerar SECRET_KEY
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Configurar variáveis (substitua <SECRET_KEY> pela chave gerada)
heroku config:set SECRET_KEY="<SECRET_KEY>" --app plataformacasa
heroku config:set DEBUG=False --app plataformacasa
heroku config:set ALLOWED_HOSTS=".herokuapp.com" --app plataformacasa
```

### 2. Verificar DATABASE_URL

```bash
heroku config:get DATABASE_URL --app plataformacasa
```

Deve retornar uma URL do PostgreSQL. Se sim, está tudo certo!

### 3. Adicionar Git Remote (se necessário)

```bash
cd /Users/anderson/my_folders/repositoriolocal/PBE_25.2_8001_IV
heroku git:remote -a plataformacasa
```

### 4. Fazer Deploy

```bash
# Verificar branch atual
git branch

# Se estiver na branch anderon, usar:
git push heroku anderon:main

# Se estiver na branch main, usar:
git push heroku main
```

### 5. Executar Migrações

```bash
heroku run python meuprojeto/manage.py migrate --app plataformacasa
```

### 6. Coletar Arquivos Estáticos

```bash
heroku run python meuprojeto/manage.py collectstatic --noinput --app plataformacasa
```

### 7. Criar Superusuário

```bash
heroku run python meuprojeto/manage.py createsuperuser --app plataformacasa
```

### 8. Abrir Aplicação

```bash
heroku open --app plataformacasa
```

Ou acesse diretamente: https://plataformacasa-f820a0a16535.herokuapp.com/

## Comandos Úteis

```bash
# Ver logs em tempo real
heroku logs --tail --app plataformacasa

# Verificar status
heroku ps --app plataformacasa

# Verificar addons instalados
heroku addons --app plataformacasa

# Verificar variáveis de ambiente
heroku config --app plataformacasa

# Reiniciar aplicação
heroku restart --app plataformacasa

# Acessar console Django
heroku run python meuprojeto/manage.py shell --app plataformacasa

# Acessar banco PostgreSQL
heroku pg:psql --app plataformacasa
```

## Troubleshooting

### Se o PostgreSQL não adicionar

Os planos da Heroku mudaram. Tente estes comandos na ordem:

```bash
# 1. Hobby-dev (gratuito)
heroku addons:create heroku-postgresql:hobby-dev --app plataformacasa

# 2. Se hobby-dev não funcionar, listar planos disponíveis
heroku addons:plans heroku-postgresql

# 3. Basic (pago)
heroku addons:create heroku-postgresql:basic --app plataformacasa

# 4. Standard-0 (pago)
heroku addons:create heroku-postgresql:standard-0 --app plataformacasa
```

### Se o push falhar

```bash
# Verificar se há alterações não commitadas
git status

# Commitar se necessário
git add .
git commit -m "Configuração para Heroku"

# Tentar push novamente
git push heroku anderon:main
```

### Se as migrações falharem

```bash
# Verificar logs
heroku logs --tail --app plataformacasa

# Tentar novamente
heroku run python meuprojeto/manage.py migrate --app plataformacasa

# Se persistir, criar migrações manualmente
heroku run python meuprojeto/manage.py makemigrations --app plataformacasa
heroku run python meuprojeto/manage.py migrate --app plataformacasa
```

## Planos PostgreSQL Atualizados (2025)

A Heroku mudou os nomes dos planos recentemente:

| Plano Antigo | Plano Novo | Custo | Linhas |
|--------------|------------|-------|--------|
| hobby-dev | hobby-dev | Gratuito | 10.000 |
| hobby-basic | basic | $9/mês | 10M |
| standard-0 | standard-0 | $50/mês | Ilimitado |
| premium-0 | premium-0 | $200/mês | Ilimitado |

**Recomendação:** Comece com **hobby-dev** (gratuito) para testes, depois migre para **basic** quando for para produção.

## Próximos Passos

1. ✅ Aplicação criada
2. ⏳ Adicionar PostgreSQL (usar comando acima)
3. ⏳ Configurar variáveis de ambiente
4. ⏳ Fazer deploy do código
5. ⏳ Executar migrações
6. ⏳ Criar superusuário
7. ⏳ Testar aplicação

Execute os comandos acima na ordem para completar o deploy!
