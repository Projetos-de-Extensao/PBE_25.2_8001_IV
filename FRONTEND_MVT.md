# Frontend - Plataforma Casa com Arquitetura MVT

## 📋 Visão Geral

Este é um frontend completo para a **Plataforma Casa** desenvolvido com a arquitetura **MVT (Model-View-Template)** do Django. O sistema gerencia monitorias acadêmicas com controle de usuários, alunos, vagas, turmas, presenças e relatórios.

---

## 🏗️ Arquitetura MVT

### Model (Modelo)
- **Localização**: `plataforma_Casa/models.py`
- **Responsabilidade**: Define a estrutura dos dados
- **Modelos principais**:
  - `Usuario`: Usuário base do sistema
  - `Aluno`: Herança de Usuário
  - `Funcionario`: Herança de Usuário
  - `Curso`, `Sala`, `Vaga`, `Turma`
  - `ParticipacaoMonitoria`, `Presenca`, `Inscricao`

### View (Visualização)
- **Localização**: `plataforma_Casa/views.py`
- **Responsabilidade**: Lógica de negócio e processamento de requisições
- **Principais views**:
  - `dashboard()` - Dashboard principal
  - `listar_usuarios()` - Lista de usuários
  - `criar_aluno()` - Criação de aluno
  - `listar_monitorias()` - Participações em monitorias
  - `listar_presencas()` - Controle de presenças
  - `relatorio_desempenho()` - Relatórios diversos

### Template (Modelo de Apresentação)
- **Localização**: `plataforma_Casa/templates/`
- **Responsabilidade**: Renderização da interface HTML
- **Estrutura de templates**:
  ```
  templates/
  ├── base.html              # Template base com navbar e sidebar
  ├── dashboard.html         # Dashboard principal
  ├── usuarios/
  │   ├── listar.html
  │   ├── criar.html
  │   └── editar.html
  ├── alunos/
  │   ├── listar.html
  │   ├── criar.html
  │   └── editar.html
  ├── vagas/
  │   ├── listar.html
  │   ├── criar.html
  │   ├── editar.html
  │   └── detalhe.html
  ├── turmas/
  │   ├── listar.html
  │   ├── criar.html
  │   ├── editar.html
  │   └── detalhe.html
  ├── monitorias/
  │   ├── listar.html
  │   └── editar.html
  ├── presencas/
  │   ├── listar.html
  │   └── editar.html
  ├── relatorios/
  │   ├── listar.html
  │   ├── desempenho.html
  │   ├── frequencia.html
  │   ├── inscricoes.html
  │   └── geral.html
  └── perfil.html
  ```

---

## 🛣️ Rotas (URLs)

### Dashboard
```
GET /                              -> Dashboard principal
```

### Usuários
```
GET    /usuarios/                  -> Listar usuários
POST   /usuarios/criar/            -> Criar novo usuário
GET    /usuarios/<id>/editar/      -> Exibir formulário de edição
POST   /usuarios/<id>/editar/      -> Salvar edição
GET    /usuarios/<id>/deletar/     -> Deletar usuário
```

### Alunos
```
GET    /alunos/                    -> Listar alunos
POST   /alunos/criar/              -> Criar novo aluno
GET    /alunos/<id>/editar/        -> Editar aluno
POST   /alunos/<id>/editar/        -> Salvar alteração
GET    /alunos/<id>/deletar/       -> Deletar aluno
```

### Vagas
```
GET    /vagas/                     -> Listar vagas
GET    /vagas/<id>/                -> Detalhe da vaga
POST   /vagas/criar/               -> Criar nova vaga
GET    /vagas/<id>/editar/         -> Editar vaga
GET    /vagas/<id>/deletar/        -> Deletar vaga
```

### Turmas
```
GET    /turmas/                    -> Listar turmas
GET    /turmas/<id>/               -> Detalhe da turma
POST   /turmas/criar/              -> Criar nova turma
GET    /turmas/<id>/editar/        -> Editar turma
GET    /turmas/<id>/deletar/       -> Deletar turma
```

### Monitorias
```
GET    /monitorias/                -> Listar participações
POST   /monitorias/<id>/editar/    -> Editar participação
```

### Presenças
```
GET    /presencas/                 -> Listar presenças
POST   /presencas/<id>/editar/     -> Editar presença
```

### Relatórios
```
GET    /relatorios/                -> Página de relatórios
GET    /relatorios/desempenho/     -> Relatório de desempenho
GET    /relatorios/frequencia/     -> Relatório de frequência
GET    /relatorios/inscricoes/     -> Relatório de inscrições
GET    /relatorios/geral/          -> Relatório geral
```

### Perfil
```
GET    /perfil/                    -> Exibir perfil do usuário
POST   /perfil/                    -> Editar perfil
POST   /alterar-senha/             -> Alterar senha
```

---

## 🎨 Interface e Styling

### Framework CSS
- **Bootstrap 5.3.0**: Framework responsivo
- **Font Awesome 6.4.0**: Ícones
- **Custom CSS**: Estilos personalizados no `base.html`

### Componentes principais
- **Navbar**: Barra de navegação superior com menu dropdown
- **Sidebar**: Menu lateral com links de navegação
- **Cards**: Componentes reutilizáveis
- **Tabelas**: Exibição de dados
- **Formulários**: Entrada de dados
- **Badges**: Indicadores de status

### Paleta de cores
```css
Primária: #667eea (Roxo)
Secundária: #764ba2 (Roxo escuro)
Sucesso: #d4edda (Verde claro)
Erro: #f8d7da (Vermelho claro)
Aviso: #fff3cd (Amarelo claro)
```

---

## 📝 Exemplo de Uso

### 1. Acessar Dashboard
```
http://localhost:8000/
```

### 2. Listar Usuários
```
http://localhost:8000/usuarios/
```

### 3. Criar Novo Aluno
```
POST http://localhost:8000/alunos/criar/

Dados:
- nome: "João Silva"
- email: "joao@example.com"
- matricula: "2025001"
- curso: 1
- periodo: 3
- cr_geral: 8.50
```

### 4. Editar Participação em Monitoria
```
POST http://localhost:8000/monitorias/1/editar/

Dados:
- ap1: 8.5
- ap2: 9.0
- cr: 8.75
```

---

## 🔍 Principais Features

### Dashboard
- Resumo geral com estatísticas
- Últimas monitorias criadas
- Inscrições pendentes
- Cards com contadores

### Gerenciamento de Usuários
- Criar, editar e deletar usuários
- Filtro por tipo de usuário
- Filtro por status (ativo/inativo)
- Listagem com paginação

### Gerenciamento de Alunos
- Cadastro completo de alunos
- Rastreamento de CR (Coeficiente de Rendimento)
- Período curricular
- Associação com cursos

### Gerenciamento de Vagas
- Criação de vagas de monitoria
- Requisitos e descrição
- Rastreamento de inscrições
- Associação com coordenadores

### Gerenciamento de Turmas
- Criação de turmas de monitoria
- Horários e dias da semana
- Salas de aula
- Associação com monitores

### Controle de Presenças
- Registro de presença por aluno
- Filtros por turma e data
- Visualização de ausências

### Participações em Monitorias
- Rastreamento de desempenho (AP1, AP2, CR)
- Filtro por turma
- Edição de notas

### Relatórios
- Relatório de desempenho
- Relatório de frequência
- Relatório de inscrições
- Relatório geral consolidado

### Perfil do Usuário
- Visualização e edição de perfil
- Alteração de senha
- Informações pessoais

---

## ⚙️ Configuração

### Settings do Django
```python
# Em meuprojeto/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'plataforma_Casa',  # Sua app
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,  # Procura templates em templates/ da app
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

---

## 🚀 Como Executar

1. **Ativar ambiente virtual**
```bash
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

2. **Instalar dependências**
```bash
pip install django
```

3. **Aplicar migrações**
```bash
python manage.py migrate
```

4. **Criar superusuário (admin)**
```bash
python manage.py createsuperuser
```

5. **Executar servidor**
```bash
python manage.py runserver
```

6. **Acessar aplicação**
```
http://localhost:8000/
```

---

## 📊 Fluxo de Dados MVT

```
1. Requisição HTTP
   ↓
2. URL Router (urls.py)
   ↓
3. View (views.py)
   ├─ Processa lógica de negócio
   ├─ Consulta Models (models.py)
   ├─ Prepara contexto de dados
   ↓
4. Template (templates/)
   ├─ Renderiza HTML com dados
   ├─ Aplica estilização
   ↓
5. Resposta HTTP (HTML rendered)
```

---

## 🔒 Segurança

- ✅ CSRF Protection (csrf_token em formulários)
- ✅ SQL Injection Prevention (ORM Django)
- ✅ XSS Protection (Template escaping automático)
- ✅ Validação de permissões (pode ser expandida)

---

## 📈 Próximos Passos

1. Implementar autenticação e autorização
2. Adicionar paginação nas listas
3. Implementar busca e filtros avançados
4. Adicionar exportação de relatórios (PDF/Excel)
5. Melhorar performance com caching
6. Adicionar testes unitários
7. Implementar API REST
8. Adicionar gráficos e dashboards interativos

---

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação oficial do Django:
- https://docs.djangoproject.com/

---

**Versão**: 1.0  
**Última atualização**: 18 de outubro de 2025
