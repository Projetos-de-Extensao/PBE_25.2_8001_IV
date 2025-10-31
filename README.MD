# 🏠 Plataforma CASA - Sistema de Gestão de Monitorias

**Código da Disciplina**: IBM8936  
**Status**: ✅ Em Produção

---

## 📋 Sobre o Projeto

A **Plataforma CASA** é um sistema completo de gerenciamento de monitoria acadêmica desenvolvido com Django 5.2 e Django REST Framework. O sistema oferece uma solução integrada para gerenciar todo o ciclo de vida da monitoria, desde a publicação de vagas até o controle de pagamentos.

### 🎯 Problema Resolvido

Antes da Plataforma CASA, o processo de monitoria era manual, demorado e propenso a erros:
- Candidaturas em papel ou email desorganizados
- Controle de horas em planilhas Excel
- Pagamentos processados manualmente
- Falta de rastreabilidade e relatórios

### ✨ Solução Oferecida

Sistema web completo que digitaliza e automatiza todo o processo de monitoria acadêmica.

---

## 👥 Integrantes

| Nome | Função | GitHub |
|------|--------|--------|
| Anderson Lima | Backend, DevOps, FrontEnd | [@anderson](https://github.com/anderson) |
| João Pedro Campos | Full Stack, API | [@joao](https://github.com/joao) |
| Bernardo Casanovas | Frontend, UX, analista de dados | [@bernardo](https://github.com/bernardo) |
| Gabriel Caruzo | Database, Reports, DevOps, Scrum Master | [@gabriel](https://github.com/gabriel) |

---

## 🚀 Stack Tecnológica

### Backend
- **Django 5.2.7** - Framework web principal
- **Django REST Framework 3.15.2** - API REST
- **Python 3.10+** - Linguagem de programação
- **PostgreSQL** - Banco de dados (produção)
- **SQLite3** - Banco de dados (desenvolvimento)

### API & Documentação
- **drf-yasg 1.21.7** - Documentação Swagger/ReDoc
- **django-cors-headers 4.0+** - CORS para frontend
- **WhiteNoise 6.8.2** - Servir arquivos estáticos

### Frontend
- **Bootstrap 5.3.0** - Framework CSS responsivo
- **Font Awesome 6.4.0** - Ícones vetoriais
- **Chart.js 3.x** - Gráficos interativos
- **jsPDF 2.5.1** - Geração de PDFs
- **XLSX 0.18.5** - Exportação para Excel

### Deploy & Infraestrutura
- **Heroku** - Cloud Platform (PaaS)
- **AWS RDS PostgreSQL** - Banco de dados em produção
- **Git/GitHub** - Controle de versão
- **GitHub Actions** - CI/CD (opcional)

---

## 🎭 Perfis de Usuário

O sistema possui 4 perfis distintos com permissões e funcionalidades específicas:

### 1️⃣ Aluno (Candidato)
**Funcionalidades:**
- ✅ Visualizar vagas disponíveis no portal
- ✅ Candidatar-se às vagas com upload de documentos
- ✅ Acompanhar status das candidaturas em tempo real
- ✅ Receber feedback de avaliações

**Menu de Acesso:**
```
📊 Dashboard
📢 Portal de Vagas
📝 Minhas Inscrições
👤 Perfil
```

### 2️⃣ Monitor (Aluno Selecionado)
**Funcionalidades:**
- ✅ Todas as funcionalidades de Aluno
- ✅ Registrar horas trabalhadas com data/hora/atividade
- ✅ Visualizar histórico completo de horas
- ✅ Acompanhar status de aprovação de horas
- ✅ Receber avaliações de desempenho

**Menu Adicional:**
```
⏰ Registrar Horas
📋 Meus Registros de Horas
⭐ Minhas Avaliações
```

### 3️⃣ Professor (Coordenador/Supervisor)
**Funcionalidades:**
- ✅ Publicar e gerenciar vagas de monitoria
- ✅ Avaliar candidatos (aprovar/rejeitar/entrevista)
- ✅ Validar registros de horas dos monitores
- ✅ Avaliar desempenho de monitores
- ✅ Gerar relatórios de candidatos e monitores
- ✅ Gerenciar turmas de monitoria

**Menu Adicional:**
```
📢 Minhas Vagas
✅ Avaliar Candidatos
👥 Aprovar Monitores
⏱️ Validar Horas
📚 Minhas Monitorias
🎓 Turmas
📊 Relatório de Candidatos
📈 Relatório de Monitores
```

### 4️⃣ Admin (Departamento/Gestão)
**Funcionalidades:**
- ✅ Acesso completo a todas as funcionalidades
- ✅ Gerenciar todos os usuários do sistema
- ✅ Processar pagamentos de monitores
- ✅ Acessar painel administrativo Django
- ✅ Gerar relatórios gerenciais completos
- ✅ Configurar cursos, disciplinas e salas
- ✅ Visualizar estatísticas gerais do sistema

**Menu Completo:**
```
🏢 Dashboard Gestão
💰 Pagamentos
👥 Gerenciar Usuários
🎓 Gerenciar Alunos
📚 Cursos e Disciplinas
📊 Todos os Relatórios
⚙️ Configurações
```

---

## 🔑 Credenciais de Teste

### Login como Aluno

```
Username: aluno.teste
Email: aluno.teste@casa.com
Senha: aluno123
Grupo: Aluno
```

### Login como Monitor

```
Username: monitor.teste
Email: monitor.teste@casa.com
Senha: monitor123
Grupo: Monitor
```

### Login como Professor

```
Username: professor.teste
Email: professor.teste@casa.com
Senha: professor123
Grupo: Professor
```

### Login como Admin

```
Username: admin
Email: admin@casa.com
Senha: admin
is_staff: True
is_superuser: True
```

---

## �️ Instalação e Configuração

### Pré-requisitos

- **Python 3.10+** instalado
- **Git** instalado
- **pip** (gerenciador de pacotes Python)
- **PostgreSQL** (opcional, para produção)
- Conta no **Heroku** (para deploy em produção)

### 📦 Instalação Local - Método 1 (Script Automático)

O método mais rápido e fácil para iniciar o sistema localmente:

```bash
# 1. Clone o repositório
git clone https://github.com/Projetos-de-Extensao/PBE_25.2_8001_IV.git
cd PBE_25.2_8001_IV

# 2. Execute o script de inicialização
python3 iniciar.py
```

**O que o script faz automaticamente:**
- ✅ Cria ambiente virtual Python
- ✅ Instala todas as dependências necessárias
- ✅ Aplica migrações do banco de dados
- ✅ Coleta arquivos estáticos
- ✅ Cria superusuário admin (admin/admin)
- ✅ Inicia servidor em http://localhost:8000

### 📦 Instalação Local - Método 2 (Manual)

Se preferir controle total sobre cada etapa:

```bash
# 1. Clone o repositório
git clone https://github.com/Projetos-de-Extensao/PBE_25.2_8001_IV.git
cd PBE_25.2_8001_IV

# 2. Crie e ative o ambiente virtual
python3 -m venv .venv

# No Linux/Mac:
source .venv/bin/activate

# No Windows:
.venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Entre na pasta do projeto Django
cd meuprojeto

# 5. Configure variáveis de ambiente (opcional para local)
cp .env.example .env
# Edite o arquivo .env se necessário

# 6. Execute as migrações
python manage.py makemigrations
python manage.py migrate

# 7. Crie superusuário
python manage.py createsuperuser
# Username: admin
# Email: admin@casa.com
# Password: admin

# 8. Colete arquivos estáticos
python manage.py collectstatic --noinput

# 9. Popule dados de teste (opcional)
python popular_dados_teste.py

# 10. Inicie o servidor
python manage.py runserver
```

### 🌐 URLs Locais Disponíveis

Após iniciar o servidor, acesse:

| URL | Descrição |
|-----|-----------|
| http://localhost:8000/ | Página inicial |
| http://localhost:8000/login/ | Login no sistema |
| http://localhost:8000/admin/ | Painel administrativo Django |
| http://localhost:8000/api/ | API Root (DRF) |
| http://localhost:8000/restapi/ | Documentação Swagger (interativa) |
| http://localhost:8000/redoc/ | Documentação ReDoc (visual) |
| http://localhost:8000/portal-vagas/ | Portal de vagas público |

---

## 🚀 Deploy no Heroku

### Passo 1: Preparar o Projeto

```bash
# 1. Instale a CLI do Heroku
# Mac: brew install heroku/brew/heroku
# Windows/Linux: https://devcenter.heroku.com/articles/heroku-cli

# 2. Faça login no Heroku
heroku login

# 3. Crie um novo app no Heroku
heroku create plataformacasa
# Ou use um nome personalizado: heroku create seu-nome-app
```

### Passo 2: Configurar PostgreSQL

```bash
# Adicione PostgreSQL ao app Heroku
heroku addons:create heroku-postgresql:mini --app plataformacasa

# Verifique a variável DATABASE_URL criada
heroku config --app plataformacasa
```

### Passo 3: Configurar Variáveis de Ambiente

```bash
# Configure as variáveis de ambiente essenciais
heroku config:set SECRET_KEY="sua-chave-secreta-super-segura-aqui" --app plataformacasa
heroku config:set DEBUG=False --app plataformacasa
heroku config:set ALLOWED_HOSTS=plataformacasa-a2a3d2abfd5e.herokuapp.com --app plataformacasa
heroku config:set CSRF_TRUSTED_ORIGINS=https://plataformacasa-a2a3d2abfd5e.herokuapp.com --app plataformacasa
heroku config:set CORS_ALLOWED_ORIGINS=https://plataformacasa-a2a3d2abfd5e.herokuapp.com --app plataformacasa

# Para permitir requisições de qualquer origem (API pública)
heroku config:set CORS_ALLOW_ALL_ORIGINS=True --app plataformacasa

# Outras configurações opcionais
heroku config:set DJANGO_SETTINGS_MODULE=meuprojeto.settings --app plataformacasa
heroku config:set WEB_CONCURRENCY=2 --app plataformacasa
```

### Passo 4: Adicionar Remote do Heroku

```bash
# Adicione o Heroku como remote Git
heroku git:remote --app plataformacasa

# Verifique os remotes configurados
git remote -v
# Deve mostrar:
# heroku  https://git.heroku.com/plataformacasa.git (fetch)
# heroku  https://git.heroku.com/plataformacasa.git (push)
# origin  https://github.com/Projetos-de-Extensao/PBE_25.2_8001_IV.git (fetch)
# origin  https://github.com/Projetos-de-Extensao/PBE_25.2_8001_IV.git (push)
```

### Passo 5: Deploy

```bash
# 1. Commit todas as mudanças
git add .
git commit -m "Deploy inicial no Heroku"

# 2. Push para o Heroku
git push heroku main

# Ou se estiver em outra branch:
git push heroku sua-branch:main
```

### Passo 6: Executar Migrações e Criar Superusuário

```bash
# 1. Execute as migrações no Heroku
heroku run "cd meuprojeto && python manage.py migrate" --app plataformacasa

# 2. Crie o superusuário (modo interativo)
heroku run "cd meuprojeto && python manage.py createsuperuser" --app plataformacasa

# Ou use variáveis de ambiente para criar automaticamente
heroku run "cd meuprojeto && python manage.py shell -c \"
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@casa.com', 'admin123')
    print('Superusuário criado')
\"" --app plataformacasa

# 3. Colete arquivos estáticos (já é feito automaticamente no build)
heroku run "cd meuprojeto && python manage.py collectstatic --noinput" --app plataformacasa

# 4. Popule dados de teste (opcional)
heroku run "cd meuprojeto && python popular_dados_teste.py" --app plataformacasa
```

### Passo 7: Verificar Deploy

```bash
# Abra o app no navegador
heroku open --app plataformacasa

# Verifique os logs em tempo real
heroku logs --tail --app plataformacasa

# Verifique o status do app
heroku ps --app plataformacasa

# Verifique variáveis de ambiente
heroku config --app plataformacasa
```

### 🔧 Configurações Importantes no Heroku

#### Arquivo `Procfile` (na raiz do projeto)
```
web: cd meuprojeto && gunicorn meuprojeto.wsgi --log-file -
```

#### Arquivo `runtime.txt` (na raiz do projeto)
```
python-3.10.12
```

#### Arquivo `requirements.txt` (principais dependências)
```txt
Django>=5.0
djangorestframework>=3.15
django-cors-headers>=4.0
drf-yasg>=1.21
gunicorn>=20.1
whitenoise>=6.8
psycopg2-binary>=2.9
python-decouple>=3.8
dj-database-url>=2.0
Pillow>=10.0
```

### 🛠️ Comandos Úteis do Heroku

```bash
# Ver logs do app
heroku logs --tail --app plataformacasa

# Reiniciar o app
heroku restart --app plataformacasa

# Executar comandos no Heroku
heroku run bash --app plataformacasa
heroku run "cd meuprojeto && python manage.py shell" --app plataformacasa

# Verificar status das migrações
heroku run "cd meuprojeto && python manage.py showmigrations" --app plataformacasa

# Escalar dynos (workers)
heroku ps:scale web=1 --app plataformacasa

# Abrir console do PostgreSQL
heroku pg:psql --app plataformacasa

# Backup do banco de dados
heroku pg:backups:capture --app plataformacasa
heroku pg:backups:download --app plataformacasa
```

### 🔄 Atualizações Após o Deploy Inicial

```bash
# 1. Faça suas mudanças no código
# 2. Commit
git add .
git commit -m "Descrição das mudanças"

# 3. Push para GitHub
git push origin main

# 4. Push para Heroku
git push heroku main

# 5. Se houver novas migrações
heroku run "cd meuprojeto && python manage.py migrate" --app plataformacasa

# 6. Reinicie se necessário
heroku restart --app plataformacasa
```

### 🌐 URLs em Produção (Heroku)

Após o deploy bem-sucedido, seu sistema estará disponível em:

| URL | Descrição |
|-----|-----------|
| https://plataformacasa-a2a3d2abfd5e.herokuapp.com/ | Página inicial |
| https://plataformacasa-a2a3d2abfd5e.herokuapp.com/admin/ | Painel administrativo |
| https://plataformacasa-a2a3d2abfd5e.herokuapp.com/api/ | API Root |
| https://plataformacasa-a2a3d2abfd5e.herokuapp.com/restapi/ | Swagger UI |
| https://plataformacasa-a2a3d2abfd5e.herokuapp.com/redoc/ | ReDoc |

---

## 4️⃣ API REST Completa

### 📡 Visão Geral da API

A Plataforma CASA oferece uma **API REST completa e documentada** que permite integração com sistemas externos, desenvolvimento de aplicativos mobile, e automação de processos.

**Características da API:**
- ✅ **RESTful** - Seguindo padrões REST
- ✅ **Documentação Interativa** - Swagger UI e ReDoc
- ✅ **Pública** - Sem autenticação necessária (configurável)
- ✅ **CORS Habilitado** - Acessível de qualquer origem
- ✅ **Paginação** - Resultados paginados automaticamente
- ✅ **Filtros e Busca** - Endpoints com filtros avançados
- ✅ **Versionada** - Suporte para múltiplas versões

### 🌐 URLs da API

#### Local (Desenvolvimento)
```
Base URL:        http://localhost:8000
API Root:        http://localhost:8000/api/
Swagger UI:      http://localhost:8000/restapi/
ReDoc:           http://localhost:8000/redoc/
```

#### Produção (Heroku)
```
Base URL:        https://plataformacasa-a2a3d2abfd5e.herokuapp.com
API Root:        https://plataformacasa-a2a3d2abfd5e.herokuapp.com/api/
Swagger UI:      https://plataformacasa-a2a3d2abfd5e.herokuapp.com/restapi/
ReDoc:           https://plataformacasa-a2a3d2abfd5e.herokuapp.com/redoc/
```

### 📚 Endpoints Principais

#### **Gestão de Usuários**
- `GET /api/tipos-usuario/` - Listar tipos de usuário
- `GET /api/usuarios/` - Listar usuários
- `GET /api/funcionarios/` - Listar funcionários (professores)
- `GET /api/alunos/` - Listar alunos
- `GET /api/alunos/monitores/` - Listar apenas monitores

#### **Gestão Acadêmica**
- `GET /api/cursos/` - Listar cursos
- `GET /api/disciplinas/` - Listar disciplinas
- `GET /api/disciplinas/por_curso/?curso_id=1` - Disciplinas por curso
- `GET /api/salas/` - Listar salas

#### **Vagas de Monitoria**
- `GET /api/vagas/` - Listar todas as vagas
- `GET /api/vagas/ativas/` - Listar vagas ativas
- `GET /api/vagas/por_curso/?curso_id=1` - Vagas por curso
- `POST /api/vagas/` - Criar nova vaga
- `GET /api/vagas/{id}/inscricoes/` - Inscrições de uma vaga
- `POST /api/vagas/{id}/adicionar_coordenador/` - Adicionar coordenador

#### **Inscrições**
- `GET /api/inscricoes/` - Listar inscrições
- `POST /api/inscricoes/` - Criar inscrição
- `GET /api/inscricoes/por_status/?status=Pendente` - Filtrar por status
- `POST /api/inscricoes/{id}/aprovar/` - Aprovar inscrição
- `POST /api/inscricoes/{id}/rejeitar/` - Rejeitar inscrição

#### **Turmas e Participações**
- `GET /api/turmas/` - Listar turmas
- `GET /api/turmas/ativas/` - Turmas ativas
- `GET /api/participacoes/` - Listar participações
- `GET /api/participacoes/por_aluno/?aluno_id=1` - Participações por aluno

#### **Controle de Frequência**
- `GET /api/presencas/` - Listar presenças
- `POST /api/presencas/` - Registrar presença
- `GET /api/presencas/por_turma/?turma_id=1` - Presenças por turma
- `GET /api/presencas/taxa_presenca/?aluno_id=1` - Taxa de presença

#### **Registro de Horas**
- `GET /api/registro-horas/` - Listar registros
- `POST /api/registro-horas/` - Criar registro
- `GET /api/registro-horas/pendentes/` - Registros pendentes
- `POST /api/registro-horas/{id}/aprovar/` - Aprovar horas
- `GET /api/registro-horas/total_horas_monitor/?monitor_id=1` - Total de horas

#### **Pagamentos**
- `GET /api/pagamentos/` - Listar pagamentos
- `POST /api/pagamentos/` - Criar pagamento
- `GET /api/pagamentos/pendentes/` - Pagamentos pendentes
- `POST /api/pagamentos/{id}/processar/` - Processar pagamento

#### **Materiais e Documentos**
- `GET /api/materiais/` - Listar materiais de apoio
- `POST /api/materiais/` - Upload de material
- `GET /api/documentos/` - Listar documentos
- `POST /api/documentos/` - Upload de documento

#### **Estatísticas**
- `GET /api/estatisticas/geral/` - Estatísticas gerais do sistema

### 💻 Exemplos de Uso da API

#### **Usando cURL**

```bash
# Listar todas as vagas
curl -X GET "https://plataformacasa-a2a3d2abfd5e.herokuapp.com/api/vagas/"

# Buscar vaga específica
curl -X GET "https://plataformacasa-a2a3d2abfd5e.herokuapp.com/api/vagas/1/"

# Criar nova vaga
curl -X POST "https://plataformacasa-a2a3d2abfd5e.herokuapp.com/api/vagas/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Monitor de Python",
    "curso": 1,
    "disciplina": 1,
    "tipo_vaga": "TEA",
    "valor_bolsa": 1500.00,
    "numero_vagas": 2,
    "ativo": true
  }'

# Aprovar inscrição
curl -X POST "https://plataformacasa-a2a3d2abfd5e.herokuapp.com/api/inscricoes/1/aprovar/"
```

#### **Usando Python (requests)**

```python
import requests

BASE_URL = "https://plataformacasa-a2a3d2abfd5e.herokuapp.com/api"

# Listar todas as vagas
response = requests.get(f"{BASE_URL}/vagas/")
vagas = response.json()
print(f"Total de vagas: {len(vagas)}")

# Buscar vagas ativas
response = requests.get(f"{BASE_URL}/vagas/ativas/")
vagas_ativas = response.json()

# Criar nova inscrição
nova_inscricao = {
    "vaga": 1,
    "aluno": 5,
    "status": "Pendente"
}
response = requests.post(f"{BASE_URL}/inscricoes/", json=nova_inscricao)
print(response.json())

# Registrar horas trabalhadas
registro_horas = {
    "turma": 1,
    "monitor": 5,
    "data": "2025-10-31",
    "hora_inicio": "14:00:00",
    "hora_fim": "18:00:00",
    "total_horas": 4.0,
    "atividade": "Monitoria de exercícios",
    "status": "Pendente"
}
response = requests.post(f"{BASE_URL}/registro-horas/", json=registro_horas)
```

#### **Usando JavaScript (Fetch)**

```javascript
const BASE_URL = "https://plataformacasa-a2a3d2abfd5e.herokuapp.com/api";

// Listar vagas
fetch(`${BASE_URL}/vagas/`)
  .then(response => response.json())
  .then(data => console.log(data));

// Criar inscrição
fetch(`${BASE_URL}/inscricoes/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    vaga: 1,
    aluno: 5,
    status: "Pendente"
  })
})
  .then(response => response.json())
  .then(data => console.log(data));

// Aprovar inscrição
fetch(`${BASE_URL}/inscricoes/1/aprovar/`, {
  method: 'POST'
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### 📖 Documentação Completa da API

Para documentação detalhada de todos os endpoints, parâmetros, exemplos e schemas:

- **Swagger UI (Interativo):** [https://plataformacasa-a2a3d2abfd5e.herokuapp.com/restapi/](https://plataformacasa-a2a3d2abfd5e.herokuapp.com/restapi/)
  - Permite testar endpoints diretamente no navegador
  - Exemplos de requisições e respostas
  - Download de especificação OpenAPI

- **ReDoc (Visual):** [https://plataformacasa-a2a3d2abfd5e.herokuapp.com/redoc/](https://plataformacasa-a2a3d2abfd5e.herokuapp.com/redoc/)
  - Documentação visual limpa e organizada
  - Busca por endpoints
  - Melhor para leitura e compreensão

- **Arquivo de Documentação:** `aqui-a-api-john-api.md`
  - Documentação completa em Markdown
  - Exemplos de uso em múltiplas linguagens
  - Casos de uso práticos

---

## ⚙️ Funcionalidades Implementadas

---

## Design System - Cores Institucionais

Eu implementei um sistema de cores baseado em cores institucionais:

```css
--color-primary-dark: #002555      /* Azul escuro */
--color-primary-light: #1245FF     /* Azul claro */
--color-accent: #F5AC00            /* Amarelo */
--color-success: #28a745           /* Verde */
--color-danger: #dc3545            /* Vermelho */
--color-warning: #ffc107           /* Amarelo de aviso */
--color-gray-light: #f8f9fa        /* Cinza claro */
--color-gray-border: #e9ecef       /* Cinza de borda */
--color-text-muted: #6c757d        /* Cinza de texto */
```

**Características do Design:**

- Sem gradientes pesados (design minimalista)
- Sombras sutis apenas no hover
- Espaçamento generoso
- Bordas finas (1px)
- Typography clara e legível

---

## ⚙️ Funcionalidades Principais do Sistema

### 1. 🎯 Portal de Vagas

- Grid responsivo de cards com vagas
- Modal de detalhes quando clica "Detalhes"
- Botão "Candidatar-se" funcional
- Indicador visual de vagas disponíveis/esgotadas

### 2. Formulário de Candidatura

- Upload de 3 documentos (Histórico, Currículo, Carta)
- Validação de extensões (PDF, DOC, DOCX)
- Aceitação de termos obrigatória
- Proteção CSRF automática

### 3. Sistema de Avaliação de Candidatos

- Lista de candidatos por vaga com estatísticas
- Perfil completo do candidato com documentos
- Botões de status clicáveis
- Formulário de avaliação com nota e comentário

### 4. Registro e Validação de Horas

- Formulário para registrar horas com data/hora
- Cálculo automático de duração
- Status: Pendente → Aprovado/Rejeitado
- Validação por professor

### 5. Sistema de Pagamentos

- Valor fixo: R$ 1.500 por semestre
- 4 status: Pendente, Processando, Pago, Cancelado
- Interface de gerenciamento de pagamentos
- Histórico de processamentos

### 6. Relatórios Profissionais

- **Candidatos por Vaga**: Tabela com status, documentos, CR
- **Monitores Selecionados**: KPI cards, gráficos, distribuição por curso
- **Horas Trabalhadas**: KPI cards, gráficos, timeline

**Exportações:**

- PDF com layout profissional (jsPDF)
- Excel com múltiplas abas (XLSX)
- Impressão com CSS media print

---

## Autenticação Custom

backend que permite login com **email OU username**:

```python
class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
      
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
```

---

## Como Testar o Sistema

### 1. Iniciar Servidor

```bash
cd /Users/anderson/my_folders/repositoriolocal/PBE_25.2_8001_IV/meuprojeto
python manage.py runserver
```

Acesse: **http://localhost:8000/login/**

### 2. Testar como Aluno

```
Username: aluno.teste
Senha: aluno123
```

**Ações:**

- Ver Portal de Vagas
- Clicar "Detalhes" para ver modal
- Candidatar-se a uma vaga (upload documentos)
- Ver "Minhas Inscrições" (status)

### 3. Testar como Professor

```
Username: professor.teste
Senha: professor123
```

**Ações:**

- Ver "Minhas Vagas"
- Clicar numa vaga para ver candidatos
- Usar botões de status
- Avaliar candidato com nota e comentário
- Validar horas de monitores

### 4. Testar como Monitor

```
Username: monitor.teste
Senha: monitor123
```

**Ações:**

- "Registrar Horas" (data, hora, atividade)
- "Meus Registros" (ver histórico)
- Ver status dos registros

### 5. Testar como Admin

```
Username: admin
Senha: admin
```

**Ações:**

- http://localhost:8000/admin/ (painel administrativo)
- "Dashboard Gestão" (métricas)
- "Pagamentos" (processar)
- Gerar relatórios em PDF/Excel

### 6. Testar Relatórios

```
http://localhost:8000/relatorios/candidatos-vaga/
http://localhost:8000/relatorios/monitores-selecionados/
http://localhost:8000/relatorios/horas-trabalhadas/
```

**Ações:**

- Exportar PDF
- Exportar Excel
- Imprimir

---

## 📊 Dados de Teste Inclusos

**Usuários:**

- 1 Admin (superuser)
- 1 Aluno de teste
- 1 Professor de teste
- 1 Monitor de teste

**Vagas:**

- 11 vagas com diferentes disciplinas
- Mix de vagas com vagas disponíveis e esgotadas

**Inscrições:**

- 81 inscrições testando diferentes status
- Alguns aprovados, alguns pendentes, alguns rejeitados

**Horas:**

- 20 registros de horas
- Mix de status (pendente, aprovado, rejeitado)

**Pagamentos:**

- 4 pagamentos processados
- Diferentes status (pendente, pago, cancelado)

**Avaliações:**

- 8 avaliações de monitores
- Diferentes notas e comentários

---

## Recursos Principais

**Autenticação:** Email ou Username login
**Permissões:** 4 perfis com menus personalizados
**Candidaturas:** Upload de documentos com validação
**Avaliação:** Sistema de status clicável AJAX
**Horas:** Registro com cálculo automático
**Pagamentos:** Sistema fixo R$ 1.500/semestre
**Relatórios:** PDF/Excel/Print
**Design:** Cores institucionais, responsivo, minimalista
**Segurança:** CSRF, proteção SQL injection, validações
**Performance:** Otimizações com select_related, prefetch_related

---

## 🎨 Design System

### Paleta de Cores Institucionais

```css
/* Cores Primárias */
--color-primary-dark: #002555      /* Azul escuro IBMEC */
--color-primary-light: #1245FF     /* Azul claro institucional */
--color-accent: #F5AC00            /* Amarelo destaque */

/* Cores de Status */
--color-success: #28a745           /* Verde - Aprovado */
--color-danger: #dc3545            /* Vermelho - Rejeitado */
--color-warning: #ffc107           /* Amarelo - Pendente */
--color-info: #17a2b8              /* Azul claro - Informação */

/* Cores Neutras */
--color-gray-light: #f8f9fa        /* Cinza claro - Background */
--color-gray-border: #e9ecef       /* Cinza - Bordas */
--color-text-muted: #6c757d        /* Cinza - Texto secundário */
```

### Princípios de Design

- ✅ **Minimalista** - Design limpo sem elementos desnecessários
- ✅ **Responsivo** - Funciona em desktop, tablet e mobile
- ✅ **Acessível** - Contraste adequado e navegação por teclado
- ✅ **Consistente** - Padrões visuais uniformes
- ✅ **Intuitivo** - Interface clara e fácil de usar

---

## 🔐 Segurança

### Medidas Implementadas

1. **Autenticação**
   - Login com email ou username
   - Senhas hasheadas com PBKDF2
   - Proteção contra força bruta

2. **Autorização**
   - Sistema de permissões por perfil
   - Controle de acesso baseado em grupos
   - Verificação de propriedade de recursos

3. **Proteção CSRF**
   - Tokens CSRF em todos os formulários
   - Validação automática pelo Django

4. **Proteção SQL Injection**
   - ORM do Django para queries
   - Validação de entrada de dados

5. **Headers de Segurança**
   - X-Frame-Options
   - X-Content-Type-Options
   - Strict-Transport-Security (HTTPS)

6. **Validações**
   - Validação de tipos de arquivo (upload)
   - Sanitização de entrada de usuário
   - Limitação de tamanho de arquivos

---

## 📊 Dados de Teste

O sistema inclui dados de teste populados automaticamente:

### Usuários de Teste
- **1 Admin** - Acesso completo ao sistema
- **3 Professores** - Podem criar vagas e avaliar
- **10 Alunos** - Podem se candidatar
- **5 Monitores** - Alunos aprovados que registram horas

### Dados Acadêmicos
- **5 Cursos** - Engenharia, Ciências, etc.
- **20 Disciplinas** - Distribuídas pelos cursos
- **11 Vagas** - Mix de ativas e preenchidas
- **5 Salas** - Locais de monitoria

### Registros
- **81 Inscrições** - Diferentes status
- **20 Registros de Horas** - Aprovados e pendentes
- **4 Pagamentos** - Histórico de pagamentos
- **8 Avaliações** - Feedback de monitores

---

## 🧪 Testes

### Como Testar o Sistema

#### 1. **Testar como Aluno**
```bash
# Login: aluno.teste / aluno123
```
- [ ] Ver portal de vagas
- [ ] Abrir modal de detalhes da vaga
- [ ] Candidatar-se com upload de documentos
- [ ] Ver minhas inscrições e status

#### 2. **Testar como Professor**
```bash
# Login: professor.teste / professor123
```
- [ ] Criar nova vaga de monitoria
- [ ] Ver candidatos de uma vaga
- [ ] Aprovar/Rejeitar candidatos
- [ ] Validar horas registradas
- [ ] Gerar relatórios

#### 3. **Testar como Monitor**
```bash
# Login: monitor.teste / monitor123
```
- [ ] Registrar horas trabalhadas
- [ ] Ver histórico de registros
- [ ] Verificar status de aprovação
- [ ] Ver avaliações recebidas

#### 4. **Testar como Admin**
```bash
# Login: admin / admin
```
- [ ] Acessar painel administrativo (/admin/)
- [ ] Gerenciar usuários
- [ ] Processar pagamentos
- [ ] Ver dashboard de gestão
- [ ] Exportar relatórios (PDF/Excel)

#### 5. **Testar API**
```bash
# Acesse o Swagger UI
http://localhost:8000/restapi/
```
- [ ] Testar endpoints GET
- [ ] Testar criação de recursos (POST)
- [ ] Testar atualização (PUT/PATCH)
- [ ] Verificar filtros e busca

---

## 📈 Performance

### Otimizações Implementadas

1. **Database Queries**
   - `select_related()` para ForeignKeys
   - `prefetch_related()` para ManyToMany
   - Índices em campos frequentemente consultados

2. **Arquivos Estáticos**
   - WhiteNoise para servir estáticos
   - Compressão de arquivos CSS/JS
   - Cache de arquivos estáticos

3. **Caching**
   - Cache de sessão no banco
   - Cache de templates compilados

4. **Frontend**
   - Minificação de CSS/JS
   - Lazy loading de imagens
   - Carregamento assíncrono

---

## 📱 Responsividade

O sistema é totalmente responsivo e funciona em:

- 💻 **Desktop** (1920x1080 e acima)
- 💻 **Laptop** (1366x768)
- 📱 **Tablet** (768x1024)
- 📱 **Mobile** (375x667 e acima)

### Breakpoints

```css
/* Mobile First */
@media (min-width: 576px) { /* SM */ }
@media (min-width: 768px) { /* MD */ }
@media (min-width: 992px) { /* LG */ }
@media (min-width: 1200px) { /* XL */ }
@media (min-width: 1400px) { /* XXL */ }
```

---

## 🐛 Troubleshooting

### Problemas Comuns e Soluções

#### 1. **Erro ao instalar dependências**
```bash
# Atualize o pip
pip install --upgrade pip

# Instale com --no-cache
pip install --no-cache-dir -r requirements.txt
```

#### 2. **Erro de migração**
```bash
# Delete o banco local e recrie
rm meuprojeto/db.sqlite3
python meuprojeto/manage.py migrate
```

#### 3. **Arquivos estáticos não carregam**
```bash
# Colete novamente
python meuprojeto/manage.py collectstatic --noinput --clear
```

#### 4. **Erro no Heroku "Application Error"**
```bash
# Veja os logs
heroku logs --tail --app plataformacasa

# Verifique variáveis de ambiente
heroku config --app plataformacasa

# Reinicie o app
heroku restart --app plataformacasa
```

#### 5. **CORS Error na API**
```bash
# Verifique se CORS está habilitado
heroku config:get CORS_ALLOW_ALL_ORIGINS --app plataformacasa

# Se não estiver, configure
heroku config:set CORS_ALLOW_ALL_ORIGINS=True --app plataformacasa
```

#### 6. **CSS do Admin Django quebrado**
```bash
# Verifique WhiteNoise no settings.py
# Deve estar em MIDDLEWARE logo após SecurityMiddleware

# Colete estáticos novamente
heroku run "cd meuprojeto && python manage.py collectstatic --noinput" --app plataformacasa
```

---

## 🔄 Roadmap e Próximas Etapas

### ✅ Implementado (v1.0)

- [x] Sistema de autenticação completo
- [x] 4 perfis de usuário com permissões
- [x] Portal de vagas e inscrições
- [x] Registro e validação de horas
- [x] Sistema de pagamentos
- [x] Relatórios em PDF e Excel
- [x] API REST completa
- [x] Documentação Swagger/ReDoc
- [x] Deploy no Heroku
- [x] Banco PostgreSQL em produção

### 🚧 Em Desenvolvimento (v1.1)

- [ ] Dashboard com gráficos avançados

### 🔮 Futuro (v2.0)

- [ ] Aplicativo mobile (React Native)
- [ ] Integração com Power BI
- [ ] Cache com Redis
- [ ] Testes automatizados (pytest)
- [ ] CI/CD com GitHub Actions
- [ ] Dark Mode
- [ ] Relatórios agendados
- [ ] Sistema de gamificação
- [ ] Integração com sistemas acadêmicos
- [ ] Machine Learning para matching

---

## 📞 Suporte e Contato

### Reportar Bugs
- **GitHub Issues:** [https://github.com/Projetos-de-Extensao/PBE_25.2_8001_IV/issues](https://github.com/Projetos-de-Extensao/PBE_25.2_8001_IV/issues)

### Documentação Adicional
- **API Completa:** `aqui-a-api-john-api.md`
- **Swagger UI:** [https://plataformacasa-a2a3d2abfd5e.herokuapp.com/restapi/](https://plataformacasa-a2a3d2abfd5e.herokuapp.com/restapi/)
- **ReDoc:** [https://plataformacasa-a2a3d2abfd5e.herokuapp.com/redoc/](https://plataformacasa-a2a3d2abfd5e.herokuapp.com/redoc/)

---


**Status:** ✅ Em Produção  
**Deploy:** [https://plataformacasa-a2a3d2abfd5e.herokuapp.com](https://plataformacasa-a2a3d2abfd5e.herokuapp.com)

---
