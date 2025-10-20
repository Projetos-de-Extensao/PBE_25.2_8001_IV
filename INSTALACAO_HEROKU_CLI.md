# Instalação do Heroku CLI e Deploy

## Passo 1: Instalar Heroku CLI

### Opção A: Instalação via Homebrew (Recomendado para macOS)

Se você não tem Homebrew instalado, primeiro instale-o:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Depois instale o Heroku CLI:

```bash
brew tap heroku/brew && brew install heroku
```

### Opção B: Instalação via instalador standalone

Baixe e execute o instalador:

```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

Depois adicione ao PATH no arquivo `~/.bash_profile` ou `~/.zshrc`:

```bash
export PATH="/usr/local/bin:$PATH"
```

Recarregue o terminal:

```bash
source ~/.bash_profile  # ou source ~/.zshrc
```

### Opção C: Download direto

Visite: https://devcenter.heroku.com/articles/heroku-cli#download-and-install

## Passo 2: Verificar instalação

```bash
heroku --version
```

Deve exibir algo como: `heroku/8.x.x darwin-x64 node-v18.x.x`

## Passo 3: Fazer login no Heroku

```bash
heroku login
```

Isso abrirá seu navegador para fazer login. Após o login, volte ao terminal.

## Passo 4: Executar o script de deploy

Volte para o diretório do projeto:

```bash
cd /Users/anderson/my_folders/repositoriolocal/PBE_25.2_8001_IV
```

Execute o script automatizado:

```bash
./deploy_heroku.sh
```

O script fará automaticamente:
- Verificação de login
- Criação da aplicação
- Adição do PostgreSQL
- Configuração de variáveis de ambiente
- Deploy do código
- Execução de migrações
- Coleta de arquivos estáticos
- Criação de superusuário (opcional)

## Passo 5: Verificar deploy

Após o deploy, você pode:

```bash
# Ver logs em tempo real
heroku logs --tail

# Abrir aplicação no navegador
heroku open

# Verificar status
heroku ps

# Ver variáveis de ambiente
heroku config
```

## Alternativa: Deploy Manual (sem script)

Se preferir fazer manualmente:

### 1. Login
```bash
heroku login
```

### 2. Criar aplicação
```bash
heroku create nome-da-aplicacao
# ou deixe a Heroku gerar o nome
heroku create
```

### 3. Adicionar PostgreSQL
```bash
# Plano gratuito (limitado)
heroku addons:create heroku-postgresql:mini

# OU plano pago recomendado ($5/mês)
heroku addons:create heroku-postgresql:essential-0
```

### 4. Gerar e configurar SECRET_KEY
```bash
# Gerar SECRET_KEY
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Configurar variáveis (substitua <SECRET_KEY> pela chave gerada acima)
heroku config:set SECRET_KEY="<SECRET_KEY>"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=".herokuapp.com"
```

### 5. Deploy
```bash
git add .
git commit -m "Configuração para deploy na Heroku"
git push heroku anderon:main
```

### 6. Migrações e Setup
```bash
# Executar migrações
heroku run python meuprojeto/manage.py migrate

# Coletar arquivos estáticos
heroku run python meuprojeto/manage.py collectstatic --noinput

# Criar superusuário
heroku run python meuprojeto/manage.py createsuperuser
```

### 7. Abrir aplicação
```bash
heroku open
```

## Troubleshooting

### Erro: "heroku: command not found"
- Certifique-se de ter instalado o Heroku CLI
- Verifique se /usr/local/bin está no seu PATH
- Reinicie o terminal após a instalação

### Erro: "Permission denied"
- Execute: `chmod +x deploy_heroku.sh`

### Erro ao fazer push
- Certifique-se de estar na branch correta: `git branch`
- Use: `git push heroku anderon:main` se estiver na branch anderon

### Erro de migração
- Verifique os logs: `heroku logs --tail`
- Execute novamente: `heroku run python meuprojeto/manage.py migrate`

### Aplicação não carrega
- Verifique logs: `heroku logs --tail`
- Verifique variáveis: `heroku config`
- Reinicie: `heroku restart`

## Custos

### Configuração Mínima
- **PostgreSQL Essential-0:** $5/mês
- **Eco Dyno:** $5/mês
- **Total:** $10/mês

### Plano Gratuito (Limitado)
- **PostgreSQL Mini:** Gratuito (limitações severas)
- **Eco Dyno:** $5/mês
- **Total:** $5/mês

## Após o Deploy

1. Acesse a aplicação: https://seu-app.herokuapp.com
2. Faça login no admin: https://seu-app.herokuapp.com/admin
3. Configure os dados necessários
4. Monitore os logs regularmente

## Atualizações Futuras

Sempre que fizer alterações no código:

```bash
git add .
git commit -m "Descrição das alterações"
git push heroku anderon:main
```

Se houver novas migrações:

```bash
heroku run python meuprojeto/manage.py migrate
```

Se houver novos arquivos estáticos:

```bash
heroku run python meuprojeto/manage.py collectstatic --noinput
```
