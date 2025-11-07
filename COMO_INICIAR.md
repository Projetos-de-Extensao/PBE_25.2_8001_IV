# 🚀 Como Iniciar a Plataforma CASA

## 📋 Resumo Rápido

```bash
# Opção 1: Script Python (Recomendado) - Com menu HTTP/HTTPS
python3 start_server.py

# Opção 2: Script Bash
./start.sh

# Opção 3: Script Python antigo
python3 iniciar.py
```

---

## ✨ Novo Script `start_server.py` (Recomendado)

### 🎯 Características

- ✅ **Verificação completa** do ambiente
- ✅ **Instalação automática** de dependências
- ✅ **Menu interativo** para escolher HTTP ou HTTPS
- ✅ **Criação automática** de certificados SSL
- ✅ **Tratamento de erros** robusto
- ✅ **Reinicialização automática** em caso de falha
- ✅ **Relatório detalhado** de status

### 📝 Como Usar

#### 1. Iniciar o Sistema

```bash
python3 start_server.py
```

#### 2. Escolher Modo de Execução

O script apresentará um menu:

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                     ESCOLHA O MODO DE EXECUÇÃO                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Selecione uma opção:

  1) HTTP - Desenvolvimento local (Recomendado)
     • Mais rápido e simples
     • Ideal para desenvolvimento
     • URL: http://localhost:8000

  2) HTTPS - Conexão segura
     • Requer certificados SSL
     • Para produção ou testes de segurança
     • URL: https://localhost:8000

  3) HTTPS com certificados auto-assinados
     • Cria certificados automaticamente
     • Útil para testes HTTPS
     • Navegador mostrará aviso de segurança

Digite sua escolha (1-3) [1]:
```

#### 3. Opções Detalhadas

##### Opção 1: HTTP (Padrão)
- Apenas pressione Enter ou digite `1`
- Servidor inicia imediatamente em HTTP
- **Melhor para desenvolvimento local**

##### Opção 2: HTTPS com Certificados Próprios
- Digite `2`
- Forneça os caminhos para:
  - Arquivo de certificado (`.crt` ou `.pem`)
  - Arquivo de chave privada (`.key`)
- **Para ambiente de produção**

##### Opção 3: HTTPS Auto-assinado (Recomendado para testes HTTPS)
- Digite `3`
- O script **configura tudo automaticamente**:
  - ✅ Instala `django-extensions` e `werkzeug`
  - ✅ Instala `pyopenssl` para criação de certificados
  - ✅ Cria certificados SSL válidos por 1 ano
  - ✅ Salva em `ssl_certs/cert.pem` e `ssl_certs/key.pem`
  - ✅ Configura o servidor com suporte SSL nativo
- **Para testes de HTTPS localmente**

⚠️ **Nota sobre certificados auto-assinados:**
- Seu navegador mostrará um aviso de segurança (normal)
- Clique em "Avançado" → "Prosseguir para localhost"
- Isso é seguro para desenvolvimento local
- Os certificados são válidos por 365 dias

🔧 **Configuração Automática:**
O script verifica e instala automaticamente:
1. OpenSSL (se disponível no sistema)
2. pyOpenSSL (para Python)
3. django-extensions (servidor HTTPS melhorado)
4. werkzeug (servidor WSGI com SSL)

Se algum componente falhar, o script oferece voltar para HTTP.

---

## 🔍 O que o Script Verifica

### 1. ✅ Estrutura do Projeto
- Verifica se `manage.py` existe
- Verifica se `requirements.txt` existe

### 2. ✅ Ambiente Virtual
- Cria ambiente virtual se não existir
- Ativa o ambiente automaticamente
- Verifica versão do Python

### 3. ✅ Dependências
- Verifica se Django está instalado
- Instala dependências do `requirements.txt`
- Instala pacotes essenciais se necessário

### 4. ✅ Banco de Dados
- Verifica existência do banco SQLite
- Cria migrações pendentes
- Aplica todas as migrações

### 5. ✅ Arquivos Estáticos
- Coleta arquivos estáticos
- Prepara CSS, JavaScript e imagens

### 6. ✅ Superusuário
- Cria usuário `admin` se não existir
- Senha padrão: `admin`

### 7. ✅ Porta do Servidor
- Verifica se porta 8000 está livre
- Oferece liberação automática se ocupada

---

## 🌐 URLs Disponíveis

Após inicialização bem-sucedida:

| Recurso | URL |
|---------|-----|
| **Página Principal** | http://localhost:8000/ |
| **Admin Django** | http://localhost:8000/admin/ |
| **API Root** | http://localhost:8000/api/ |
| **Swagger UI** | http://localhost:8000/restapi/ |
| **ReDoc** | http://localhost:8000/restapi/redoc/ |

### 🔑 Credenciais Padrão

```
Usuário: admin
Senha: admin
```

---

## 🛠️ Solução de Problemas

### Problema: Django não instalado

**Sintoma:**
```
ModuleNotFoundError: No module named 'django'
```

**Solução:**
O script `start_server.py` resolve automaticamente. Apenas execute:
```bash
python3 start_server.py
```

---

### Problema: Porta 8000 em uso

**Sintoma:**
```
⚠️  AVISO: Porta 8000 já está em uso
```

**Solução automática:**
O script oferece liberar a porta automaticamente. Digite `s` quando solicitado.

**Solução manual:**
```bash
# macOS/Linux
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

### Problema: Erro nas migrações

**Sintoma:**
```
❌ ERRO: Não foi possível aplicar migrações
```

**Solução:**
```bash
# Ativar ambiente virtual
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Resetar migrações (cuidado: perde dados!)
cd meuprojeto
python manage.py migrate --fake-initial

# Ou recriar banco (desenvolvimento apenas)
rm db.sqlite3
python manage.py migrate
```

---

### Problema: Certificados SSL inválidos

**Sintoma:**
```
❌ ERRO: Arquivo de certificado não encontrado
```

**Solução:**
1. Use a opção 1 (HTTP) para desenvolvimento
2. Ou use a opção 3 (certificados auto-assinados)
3. Para produção, obtenha certificados válidos (Let's Encrypt, etc.)

---

## 🔄 Reinicialização em Caso de Erro

Se o servidor cair, o script oferece reinicialização automática:

```
❌ ERRO: Servidor encerrou com código 1

Deseja reiniciar o servidor? (s/N):
```

Digite `s` para reiniciar ou `N` para sair.

---

## 💡 Dicas e Boas Práticas

### Desenvolvimento Local
```bash
# Use sempre HTTP para desenvolvimento
python3 start_server.py
# Escolha opção 1
```

### Testes de HTTPS
```bash
# Use certificados auto-assinados
python3 start_server.py
# Escolha opção 3
```

### Produção
- **Não use** `runserver` em produção
- Use Gunicorn + Nginx
- Obtenha certificados SSL válidos (Let's Encrypt)
- Configure variáveis de ambiente
- Use PostgreSQL ao invés de SQLite

---

## 📊 Resumo da Verificação

Ao final das verificações, o script exibe um resumo:

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                           RESUMO DA VERIFICAÇÃO                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  ✅ Sistema totalmente configurado! Nenhum problema encontrado.             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

**Status possíveis:**
- ✅ **Totalmente configurado** - Sem erros ou avisos
- ⚠️ **Configurado com avisos** - Funcional, mas com avisos não críticos
- ❌ **Erros encontrados** - Requer correção antes de iniciar

---

## 🚨 Quando o Servidor Cai Constantemente

Se você está tendo problemas recorrentes:

### 1. Verifique os Logs
```bash
# Os logs aparecem no terminal
# Procure por linhas com ERROR ou CRITICAL
```

### 2. Verifique Configurações
```bash
# Arquivo: meuprojeto/meuprojeto/settings.py
# Verifique:
DEBUG = True  # Deve ser True em desenvolvimento
ALLOWED_HOSTS = ['*']  # Ou inclua localhost
```

### 3. Verifique Memória/Recursos
```bash
# macOS/Linux
top
htop  # se instalado

# Windows
Task Manager (Ctrl+Shift+Esc)
```

### 4. Recrie o Ambiente Virtual
```bash
# Remover ambiente antigo
rm -rf .venv

# Executar script (ele cria novo ambiente)
python3 start_server.py
```

---

## 📚 Arquivos de Script Disponíveis

| Arquivo | Tipo | Descrição |
|---------|------|-----------|
| **start_server.py** | Python | ⭐ Recomendado - Menu HTTP/HTTPS, verificações completas |
| **start.sh** | Bash | Script shell robusto com verificações |
| **iniciar.py** | Python | Script Python simples |
| **inicializar.sh** | Bash | Script wrapper para inicializar_sistema.py |

---

## 🆘 Precisa de Ajuda?

1. **Verifique os logs** no terminal
2. **Leia as mensagens de erro** - o script é verboso
3. **Execute novamente** - muitos problemas são temporários
4. **Verifique a documentação** nos arquivos `.md`
5. **Consulte o arquivo** `SOLUCAO_ERRO_DETALHES_VAGA.md`

---

## 📝 Notas Adicionais

### Ambiente Virtual
- **Sempre ativado automaticamente** pelo script
- Localização: `.venv/` na raiz do projeto
- Python 3.10+ requerido

### Dependências
- Instaladas automaticamente do `requirements.txt`
- Inclui Django, DRF, CORS, Swagger, etc.

### Banco de Dados
- SQLite para desenvolvimento (`db.sqlite3`)
- PostgreSQL para produção (via Heroku)

---

**Desenvolvido pela equipe Plataforma CASA** 🏠
