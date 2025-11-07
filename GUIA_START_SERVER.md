# 🚀 START SERVER - Guia Definitivo

## ✨ Opções Simplificadas

O script agora tem apenas **2 opções** simples:

### Opção 1: HTTP (Desenvolvimento) ⚡
```
✅ Rápido e simples
✅ Zero configuração
✅ Ideal para desenvolvimento diário
❌ Sem criptografia
```

### Opção 2: HTTPS (Automático) 🔒
```
✅ Configuração 100% automática
✅ Cria certificados SSL sozinho
✅ Instala todas as dependências
✅ Usa runserver_plus com SSL nativo
⚠️  Navegador mostra aviso (normal em dev)
```

---

## 📖 Como Usar

### Passo 1: Execute o script
```bash
python3 start_server.py
```

### Passo 2: Escolha uma opção

#### Para desenvolvimento normal:
```
Digite sua escolha (1-2) [1]: 1  # ou apenas Enter
```

#### Para testes HTTPS:
```
Digite sua escolha (1-2) [1]: 2
```

---

## 🤖 O que Acontece Automaticamente (Opção 2)

Quando você escolhe a opção 2 (HTTPS), o script faz TUDO automaticamente:

### 1️⃣ Instala Dependências
```
✓ django-extensions  # Servidor com SSL
✓ werkzeug          # WSGI com SSL
✓ pyopenssl         # OpenSSL para Python
```

### 2️⃣ Cria Certificados SSL
```
✓ Tenta usar OpenSSL nativo (mais rápido)
✓ Se não tiver, usa Python puro
✓ Salva em ssl_certs/cert.pem e ssl_certs/key.pem
✓ Válidos por 365 dias
```

### 3️⃣ Configura Django
```
✓ Adiciona django_extensions ao INSTALLED_APPS
✓ Configura runserver_plus
```

### 4️⃣ Inicia Servidor HTTPS
```
✓ https://localhost:8000/
✓ SSL nativo via runserver_plus
```

---

## 🎯 Exemplo de Execução

### HTTP (Desenvolvimento)
```bash
$ python3 start_server.py

╔═══════════════════════════════════════════════════════════╗
║    🚀 PLATAFORMA CASA - INICIALIZAÇÃO INTELIGENTE        ║
╚═══════════════════════════════════════════════════════════╝

▶ Verificando estrutura do projeto...
✅ manage.py encontrado
✅ requirements.txt encontrado

▶ Configurando ambiente virtual...
✅ Ambiente virtual encontrado
✅ Versão: Python 3.13.7

▶ Verificando/Instalando dependências...
✅ Django 5.2.7 já instalado

▶ Verificando banco de dados...
✅ Banco de dados encontrado (524K)
✅ Migrações aplicadas com sucesso

▶ Verificando porta 8000...
✅ Porta 8000 disponível

╔═══════════════════════════════════════════════════════════╗
║                 RESUMO DA VERIFICAÇÃO                     ║
╠═══════════════════════════════════════════════════════════╣
║  ✅ Sistema totalmente configurado!                      ║
╚═══════════════════════════════════════════════════════════╝

Selecione uma opção:

  1) HTTP - Desenvolvimento local (Recomendado)
     • Mais rápido e simples
     • Ideal para desenvolvimento
     • URL: http://localhost:8000

  2) HTTPS - Configuração automática completa
     • Cria certificados SSL automaticamente
     • Instala todas as dependências necessárias
     • URL: https://localhost:8000
     • Navegador mostrará aviso de segurança (normal)

Digite sua escolha (1-2) [1]: 1

✅ Modo HTTP selecionado

✓ Sistema pronto para inicialização!

📍 URLs Disponíveis:
   • Página Principal:  http://localhost:8000/
   • Admin Django:      http://localhost:8000/admin/
   • API Root:          http://localhost:8000/api/
   • Swagger:           http://localhost:8000/restapi/
   • ReDoc:             http://localhost:8000/restapi/redoc/

🔑 Credenciais Padrão:
   • Usuário:           admin
   • Senha:             admin

💡 Dica: Pressione CTRL+C para parar o servidor

ℹ️  Iniciando servidor Django...

Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
November 05, 2025 - 20:30:00
Django version 5.2.7, using settings 'meuprojeto.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
```

### HTTPS (Automático)
```bash
$ python3 start_server.py

[... mesmas verificações ...]

Digite sua escolha (1-2) [1]: 2

▶ Preparando ambiente para HTTPS...
ℹ️  Instalando suporte para HTTPS...
ℹ️  Instalando django-extensions...
ℹ️  Instalando werkzeug...
ℹ️  Instalando pyopenssl...
✅ Suporte para HTTPS instalado

ℹ️  Criando certificados SSL automaticamente...
ℹ️  Usando OpenSSL para criar certificados...
✅ ✓ Certificado criado: /path/to/ssl_certs/cert.pem
✅ ✓ Chave criada: /path/to/ssl_certs/key.pem
ℹ️  Válido por 365 dias

✅ Certificados SSL criados com sucesso
ℹ️  Certificado: /path/to/ssl_certs/cert.pem
ℹ️  Chave: /path/to/ssl_certs/key.pem
ℹ️  Usando django-extensions runserver_plus para HTTPS

✓ Sistema pronto para inicialização!

📍 URLs Disponíveis:
   • Página Principal:  https://localhost:8000/
   • Admin Django:      https://localhost:8000/admin/
   • API Root:          https://localhost:8000/api/
   • Swagger:           https://localhost:8000/restapi/
   • ReDoc:             https://localhost:8000/restapi/redoc/

🔑 Credenciais Padrão:
   • Usuário:           admin
   • Senha:             admin

⚠️  AVISO: Usando HTTPS
   Certificado auto-assinado - seu navegador mostrará um aviso
   Para aceitar: clique em 'Avançado' → 'Prosseguir para localhost'

💡 Dica: Pressione CTRL+C para parar o servidor

ℹ️  Usando runserver_plus (django-extensions) com SSL
ℹ️  Iniciando servidor Django...

Performing system checks...

System check identified no issues (0 silenced).
November 05, 2025 - 20:30:00
Django version 5.2.7, using settings 'meuprojeto.settings'
Starting development server at https://0.0.0.0:8000/
Using Werkzeug 3.0.4
Quit the server with CONTROL-C.

 * Running on https://0.0.0.0:8000
```

---

## 🌐 Acessando o Servidor

### HTTP
Abra o navegador e acesse:
```
http://localhost:8000/
```

### HTTPS
Abra o navegador e acesse:
```
https://localhost:8000/
```

**Você verá um aviso:**
```
⚠️ Sua conexão não é particular
   NET::ERR_CERT_AUTHORITY_INVALID
```

**É normal! Para continuar:**
1. Clique em **"Avançado"**
2. Clique em **"Prosseguir para localhost (não seguro)"**
3. ✅ Pronto!

---

## 🔍 Verificando se HTTPS está Funcionando

### No Navegador
1. Veja o cadeado 🔒 na barra de endereço
2. Clique no cadeado → "A conexão não é segura"
3. Isso é normal para certificados auto-assinados

### No Terminal
```bash
# Testar conexão
curl -k https://localhost:8000/

# Ver certificado
openssl s_client -connect localhost:8000 -showcerts
```

### Verificar Arquivos
```bash
# Listar certificados
ls -lh ssl_certs/

# Ver detalhes do certificado
openssl x509 -in ssl_certs/cert.pem -text -noout
```

---

## 🛠️ Solução de Problemas

### Problema: HTTPS não funciona

**Sintoma:** Servidor inicia mas não consegue acessar HTTPS

**Soluções:**

1. **Verificar se django-extensions está instalado:**
```bash
source .venv/bin/activate
python -c "import django_extensions; print('OK')"
```

2. **Reinstalar dependências:**
```bash
source .venv/bin/activate
pip install django-extensions werkzeug pyopenssl
```

3. **Verificar certificados:**
```bash
ls -lh ssl_certs/
openssl x509 -in ssl_certs/cert.pem -noout -dates
```

4. **Limpar e recriar:**
```bash
rm -rf ssl_certs/
python3 start_server.py  # Escolha opção 2
```

---

### Problema: "django-extensions não disponível"

**Sintoma:**
```
⚠️  django-extensions não disponível
⚠️  Django runserver padrão não suporta HTTPS
ℹ️  Continuando com HTTP...
```

**Solução:**
```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Instalar manualmente
pip install django-extensions werkzeug pyopenssl

# Executar novamente
python3 start_server.py
```

---

### Problema: Porta 8000 em uso

**O script perguntará automaticamente:**
```
⚠️  AVISO: Porta 8000 já está em uso
Deseja tentar liberar a porta? (s/N): s
```

**Ou faça manualmente:**
```bash
# macOS/Linux
lsof -ti:8000 | xargs kill -9

# Ou use outra porta
cd meuprojeto
source ../.venv/bin/activate
python manage.py runserver 8001
```

---

## 📊 Comparação Final

| Característica | HTTP (Opção 1) | HTTPS (Opção 2) |
|----------------|----------------|-----------------|
| **Configuração** | Zero | Automática |
| **Velocidade** | ⚡⚡⚡ | ⚡⚡ |
| **Criptografia** | ❌ | ✅ |
| **Certificados** | Não precisa | Cria sozinho |
| **Avisos** | Nenhum | Aviso no navegador |
| **Melhor para** | Dev diário | Testes HTTPS |
| **Dependências extras** | Não | Sim (auto) |

---

## 💡 Recomendações

### 90% do tempo → Use Opção 1 (HTTP)
- Desenvolvimento local
- Testes rápidos
- Não precisa de SSL

### 10% do tempo → Use Opção 2 (HTTPS)
- Testar Service Workers
- Testar recursos que exigem HTTPS
- PWA development
- Integração com APIs HTTPS
- Testes de cookies seguros

---

## 📁 Estrutura de Arquivos

Após usar HTTPS (opção 2):

```
PBE_25.2_8001_IV/
├── .venv/                          # Ambiente virtual
│   └── lib/python3.13/site-packages/
│       ├── django_extensions/      # ✓ Instalado
│       ├── werkzeug/               # ✓ Instalado
│       └── OpenSSL/                # ✓ Instalado
│
├── ssl_certs/                      # ✓ Criado automaticamente
│   ├── cert.pem                   # Certificado SSL
│   └── key.pem                    # Chave privada
│
├── meuprojeto/
│   ├── meuprojeto/
│   │   └── settings.py            # ✓ django_extensions adicionado
│   └── manage.py
│
└── start_server.py                # ✓ Script principal
```

---

## 🎓 Conclusão

**Agora é simples:**
- Quer velocidade? → **Opção 1** (HTTP)
- Quer HTTPS? → **Opção 2** (Automático)

**Nenhuma configuração manual necessária!** 🎉

---

## 🆘 Suporte

Se ainda tiver problemas:

1. Execute com HTTP primeiro (opção 1) para verificar se o servidor funciona
2. Verifique se tem Python 3.10+
3. Verifique se o ambiente virtual está criado (`.venv/`)
4. Delete `ssl_certs/` e tente novamente
5. Reinstale dependências: `pip install -r requirements.txt`

---

**Desenvolvido pela equipe Plataforma CASA** 🏠🚀
