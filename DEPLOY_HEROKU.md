# 🚀 Deploy da Plataforma Casa no Heroku

## ✅ Deploy Concluído com Sucesso!

**URL da Aplicação:** https://plataformacasa-a2a3d2abfd5e.herokuapp.com/

---

## 📋 Informações do Deploy

### Configurações do Heroku

- **Nome do App:** plataformacasa
- **Stack:** heroku-24
- **Região:** US
- **Python:** 3.12.8
- **Banco de Dados:** PostgreSQL (essential-0)

### Variáveis de Ambiente Configuradas

```bash
ALLOWED_HOSTS=plataformacasa-a2a3d2abfd5e.herokuapp.com,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://plataformacasa-a2a3d2abfd5e.herokuapp.com
DATABASE_URL=postgres://... (configurado automaticamente pelo Heroku)
DEBUG=False
SECRET_KEY=django-prod-plataformacasa-... (gerada automaticamente)
```

---

## 👥 Usuários de Demonstração Criados

O sistema foi populado com dados de teste. Use as seguintes credenciais para login:

| Papel | Usuário | Senha | Descrição |
|-------|---------|-------|-----------|
| **Aluno** | `aluno.teste` | `aluno123` | Estudante regular |
| **Monitor** | `monitor.teste` | `monitor123` | Monitor de disciplinas |
| **Professor** | `professor.teste` | `professor123` | Professor/Coordenador |
| **Admin** | `admin` | `admin123` | Administrador do sistema |

---

## 📊 Dados Populados

O banco de dados foi populado automaticamente com:

- ✅ 4 Grupos de usuários (Aluno, Monitor, Professor, Admin)
- ✅ 5 Tipos de usuário
- ✅ 5 Cursos (CC, SI, ES, ADS, RC)
- ✅ 5 Salas (Labs e Auditório)
- ✅ 4 Funcionários (Professores/Coordenadores)
- ✅ 7 Alunos
- ✅ 3 Vagas de Monitoria
- ✅ 3 Turmas de Monitoria
- ✅ Inscrições, Participações, Presenças
- ✅ Registros de Horas e Pagamentos

---

## 🔧 Comandos Úteis

### Ver logs da aplicação
```bash
heroku logs --tail -a plataformacasa
```

### Executar migrações
```bash
heroku run python meuprojeto/manage.py migrate -a plataformacasa
```

### Popular dados de teste novamente
```bash
heroku run python meuprojeto/manage.py popular_dados -a plataformacasa
```

### Abrir shell do Django
```bash
heroku run python meuprojeto/manage.py shell -a plataformacasa
```

### Criar novo superusuário
```bash
heroku run "python meuprojeto/manage.py shell -c \"
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('username', 'email@example.com', 'senha')
\"" -a plataformacasa
```

### Verificar status dos dynos
```bash
heroku ps -a plataformacasa
```

### Resetar banco de dados (CUIDADO!)
```bash
heroku pg:reset DATABASE_URL -a plataformacasa --confirm plataformacasa
heroku run python meuprojeto/manage.py migrate -a plataformacasa
heroku run python meuprojeto/manage.py popular_dados -a plataformacasa
```

---

## 🌐 Acessando a Aplicação

1. **URL Principal:** https://plataformacasa-a2a3d2abfd5e.herokuapp.com/
2. **Login:** https://plataformacasa-a2a3d2abfd5e.herokuapp.com/login/
3. **Admin Django:** https://plataformacasa-a2a3d2abfd5e.herokuapp.com/admin/

---

## 📝 Notas Importantes

1. **Banco de Dados:** O PostgreSQL está no plano `essential-0` (~$5/mês)
2. **Arquivos Estáticos:** Servidos via WhiteNoise (comprimidos e com cache)
3. **Segurança:** 
   - DEBUG=False em produção
   - SECRET_KEY gerada automaticamente
   - HTTPS forçado
   - Cookies seguros habilitados

---

## 🔄 Atualizando a Aplicação

Para fazer deploy de novas alterações:

```bash
# 1. Fazer commit das alterações
git add .
git commit -m "Descrição das alterações"

# 2. Push para o Heroku
git push heroku anderon:main

# 3. Se houver novas migrações
heroku run python meuprojeto/manage.py migrate -a plataformacasa

# 4. Verificar logs
heroku logs --tail -a plataformacasa
```

---

## 🆘 Solução de Problemas

### Aplicação não está respondendo
```bash
# Reiniciar dynos
heroku restart -a plataformacasa

# Verificar logs
heroku logs --tail -a plataformacasa
```

### Erro 500 (Internal Server Error)
```bash
# Ver logs detalhados
heroku logs --tail -a plataformacasa

# Verificar variáveis de ambiente
heroku config -a plataformacasa
```

### Erro de migração
```bash
# Resetar migrações (CUIDADO - perde dados!)
heroku pg:reset DATABASE_URL -a plataformacasa --confirm plataformacasa
heroku run python meuprojeto/manage.py migrate -a plataformacasa
```

---

## 📧 Contato

Para suporte ou dúvidas sobre o deploy, consulte:
- Documentação do Heroku: https://devcenter.heroku.com/
- Documentação do Django: https://docs.djangoproject.com/

---

**✨ Deploy realizado em:** 20 de outubro de 2025
**🎯 Status:** Ativo e funcionando
