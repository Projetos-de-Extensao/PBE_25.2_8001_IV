# Guia de Deploy na Heroku

## Pré-requisitos

1. Conta no Heroku (plano gratuito ou pago)
2. Heroku CLI instalado localmente
3. Git configurado

## Passos para Deploy

### 1. Login no Heroku

```bash
heroku login
```

### 2. Criar aplicação na Heroku

```bash
heroku create nome-da-sua-aplicacao
```

Ou deixe a Heroku gerar um nome automático:

```bash
heroku create
```

### 3. Adicionar PostgreSQL (plano mais barato)

O plano "Essential 0" custa $5/mês e oferece:
- 10.000 linhas
- 1GB de armazenamento
- Conexões ilimitadas

```bash
heroku addons:create heroku-postgresql:essential-0
```

Para plano gratuito (limitado):

```bash
heroku addons:create heroku-postgresql:mini
```

### 4. Configurar variáveis de ambiente

```bash
# Gerar SECRET_KEY segura
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Configurar no Heroku
heroku config:set SECRET_KEY="sua-secret-key-gerada"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=".herokuapp.com"
```

### 5. Deploy do código

```bash
git add .
git commit -m "Configuração para deploy na Heroku"
git push heroku anderon:main
```

Ou se estiver na branch main:

```bash
git push heroku main
```

### 6. Executar migrações do banco de dados

```bash
heroku run python meuprojeto/manage.py migrate
```

### 7. Criar superusuário (administrador)

```bash
heroku run python meuprojeto/manage.py createsuperuser
```

### 8. Coletar arquivos estáticos

```bash
heroku run python meuprojeto/manage.py collectstatic --noinput
```

### 9. Abrir aplicação

```bash
heroku open
```

## Comandos Úteis

### Ver logs em tempo real

```bash
heroku logs --tail
```

### Verificar status da aplicação

```bash
heroku ps
```

### Executar comandos Django remotamente

```bash
heroku run python meuprojeto/manage.py <comando>
```

### Acessar console Python remoto

```bash
heroku run python meuprojeto/manage.py shell
```

### Reiniciar aplicação

```bash
heroku restart
```

### Verificar variáveis de ambiente

```bash
heroku config
```

### Conectar ao banco PostgreSQL

```bash
heroku pg:psql
```

## Troubleshooting

### Erro ao coletar arquivos estáticos

Se houver erro com staticfiles, execute localmente primeiro:

```bash
python meuprojeto/manage.py collectstatic --noinput
```

### Erro de migração

Verifique se todas as migrações foram criadas:

```bash
python meuprojeto/manage.py makemigrations
git add .
git commit -m "Add migrations"
git push heroku anderon:main
heroku run python meuprojeto/manage.py migrate
```

### Aplicação não inicia

Verifique os logs:

```bash
heroku logs --tail
```

### Verificar DATABASE_URL

```bash
heroku config:get DATABASE_URL
```

## Configurações de Produção

O arquivo `settings.py` foi configurado para:

1. Usar PostgreSQL automaticamente na Heroku via DATABASE_URL
2. Usar SQLite localmente para desenvolvimento
3. Desabilitar DEBUG em produção
4. Configurar segurança HTTPS obrigatório
5. Servir arquivos estáticos com WhiteNoise
6. Proteger credenciais via variáveis de ambiente

## Desenvolvimento Local

Para desenvolvimento local, crie arquivo `.env` na pasta `meuprojeto/`:

```env
SECRET_KEY=sua-chave-local
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Custos Estimados

### PostgreSQL Essential 0
- **Custo:** $5/mês
- **Linhas:** 10.000
- **Armazenamento:** 1GB
- **Conexões:** Ilimitadas

### Dynos (servidores)
- **Eco Dyno:** $5/mês (sleeps após inatividade)
- **Basic Dyno:** $7/mês (não sleeps)
- **Standard 1X:** $25/mês (recursos dedicados)

### Recomendação Inicial
- PostgreSQL Essential 0: $5/mês
- Eco Dyno: $5/mês
- **Total:** $10/mês

## Monitoramento

Acesse o dashboard da Heroku para monitorar:
- Uso de recursos
- Logs de erro
- Métricas de performance
- Status do banco de dados

Dashboard: https://dashboard.heroku.com/apps/nome-da-sua-aplicacao

## Backup do Banco de Dados

### Criar backup manual

```bash
heroku pg:backups:capture
```

### Baixar backup

```bash
heroku pg:backups:download
```

### Agendar backups automáticos (planos pagos)

```bash
heroku pg:backups:schedule --at '02:00 America/Sao_Paulo'
```

## Domínio Customizado

Para adicionar domínio próprio:

```bash
heroku domains:add www.seudominio.com.br
```

Depois configure os registros DNS conforme instruções fornecidas.
