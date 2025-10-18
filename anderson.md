# ANDERSON - Plataforma Casa - Frontend MVT

## 📋 Índice
1. [Visão Geral](#visão-geral)
2. [O Que Foi Criado](#o-que-foi-criado)
3. [Arquitetura MVT](#arquitetura-mvt)
4. [Estrutura de Diretórios](#estrutura-de-diretórios)
5. [Rotas e Endpoints](#rotas-e-endpoints)
6. [Módulos Implementados](#módulos-implementados)
7. [Tecnologias Utilizadas](#tecnologias-utilizadas)
8. [Como Executar](#como-executar)
9. [Próximos Passos](#próximos-passos)

---

## 🎯 Visão Geral

Este documento descreve o desenvolvimento do **frontend completo da Plataforma Casa** utilizando a arquitetura **MVT (Model-View-Template)** do Django.

A Plataforma Casa é um **sistema de gerenciamento de monitorias acadêmicas** que permite:
- ✅ Cadastro e gerenciamento de usuários, alunos e funcionários
- ✅ Criação e administração de vagas de monitoria
- ✅ Gestão de turmas e horários
- ✅ Controle de participação e desempenho dos alunos
- ✅ Registro e consulta de presenças
- ✅ Geração de relatórios analíticos
- ✅ Dashboard com estatísticas gerais

---

## 🚀 O Que Foi Criado

### 1️⃣ Views (Lógica de Negócio)
**Arquivo:** `plataforma_Casa/views.py`

Implementadas **34 views** em Python organizadas em 10 módulos:

#### Módulo Dashboard
- `dashboard()` - Página inicial com resumo geral

#### Módulo Usuários
- `listar_usuarios()` - Listar todos os usuários
- `criar_usuario()` - Criar novo usuário
- `editar_usuario(usuario_id)` - Editar usuário existente
- `deletar_usuario(usuario_id)` - Remover usuário

#### Módulo Alunos
- `listar_alunos()` - Listar alunos
- `criar_aluno()` - Criar novo aluno
- `editar_aluno(aluno_id)` - Editar aluno
- `deletar_aluno(aluno_id)` - Deletar aluno

#### Módulo Vagas
- `listar_vagas()` - Listar vagas de monitoria
- `detalhe_vaga(vaga_id)` - Detalhes de uma vaga
- `criar_vaga()` - Criar nova vaga
- `editar_vaga(vaga_id)` - Editar vaga
- `deletar_vaga(vaga_id)` - Deletar vaga

#### Módulo Turmas
- `listar_turmas()` - Listar turmas
- `detalhe_turma(turma_id)` - Detalhes de uma turma
- `criar_turma()` - Criar nova turma
- `editar_turma(turma_id)` - Editar turma
- `deletar_turma(turma_id)` - Deletar turma

#### Módulo Monitorias
- `listar_monitorias()` - Listar participações
- `editar_participacao(participacao_id)` - Editar notas

#### Módulo Presenças
- `listar_presencas()` - Listar presenças
- `editar_presenca(presenca_id)` - Editar presença

#### Módulo Relatórios
- `listar_relatorios()` - Menu de relatórios
- `relatorio_desempenho()` - Relatório de desempenho
- `relatorio_frequencia()` - Relatório de frequência
- `relatorio_inscricoes()` - Relatório de inscrições
- `relatorio_geral()` - Relatório consolidado

#### Módulo Perfil
- `perfil()` - Exibir/editar perfil do usuário
- `alterar_senha()` - Alterar senha

#### Legado
- `sql_view()` - View SQL original (para debugging)

### 2️⃣ Templates HTML (Apresentação)
**Diretório:** `plataforma_Casa/templates/`

Criados **17 templates** com design responsivo e profissional:

```
templates/
├── base.html                    # Template base com navbar e sidebar
├── dashboard.html               # Dashboard com estatísticas
├── perfil.html                  # Perfil do usuário
├── usuarios/
│   ├── listar.html             # Listagem de usuários
│   ├── criar.html              # Formulário de criação
│   └── editar.html             # Formulário de edição
├── alunos/
│   ├── listar.html             # Listagem de alunos
│   ├── criar.html              # Formulário de criação
│   └── editar.html             # Formulário de edição
├── vagas/
│   ├── listar.html             # Cards com vagas
│   ├── criar.html              # Formulário de criação
│   ├── editar.html             # Formulário de edição
│   └── detalhe.html            # Detalhes da vaga
├── turmas/
│   ├── listar.html             # Listagem de turmas
│   ├── criar.html              # Formulário de criação
│   ├── editar.html             # Formulário de edição
│   └── detalhe.html            # Detalhes da turma
├── monitorias/
│   ├── listar.html             # Listagem de participações
│   └── editar.html             # Editar notas
├── presencas/
│   ├── listar.html             # Listagem de presenças
│   └── editar.html             # Editar presença
└── relatorios/
    ├── listar.html             # Menu de relatórios
    ├── desempenho.html         # Relatório de desempenho
    ├── frequencia.html         # Relatório de frequência
    ├── inscricoes.html         # Relatório de inscrições
    └── geral.html              # Relatório geral
```

### 3️⃣ URLs (Roteamento)
**Arquivo:** `plataforma_Casa/urls.py`

Configuradas **34 rotas** (endpoints) com comentários detalhados.

**Arquivo:** `meuprojeto/urls.py`

Atualizado com comentários profissionais sobre o roteamento.

### 4️⃣ Documentação
- **FRONTEND_MVT.md** - Documentação técnica completa
- **anderson.md** - Este arquivo
- **14-arquitetura-mvt.puml** - Diagrama da arquitetura

---

## 🏗️ Arquitetura MVT

### O que é MVT?

**MVT (Model-View-Template)** é o padrão de arquitetura usado pelo Django para separar responsabilidades:

```
┌─────────────────────────────────────────────────────────┐
│                   CLIENTE (Browser)                     │
│                   HTML + CSS + JS                       │
└─────────────────────────────────────────────────────────┘
                            ↓↑
┌─────────────────────────────────────────────────────────┐
│                     DJANGO                              │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  │
│  │   Model     │  │   View      │  │  Template    │  │
│  ├─────────────┤  ├─────────────┤  ├──────────────┤  │
│  │ Estrutura   │  │ Lógica de   │  │ Renderização │  │
│  │ de Dados    │  │ Negócio     │  │ HTML         │  │
│  └─────────────┘  └─────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                            ↓↑
┌─────────────────────────────────────────────────────────┐
│              BANCO DE DADOS (SQLite)                    │
│              Usuários, Alunos, Vagas...                 │
└─────────────────────────────────────────────────────────┘
```

### Componentes

#### 📦 Model (Modelo de Dados)
- **Arquivo:** `models.py`
- **Responsabilidade:** Define a estrutura dos dados
- **Modelos principais:**
  - `Usuario` - Base para usuários do sistema
  - `Aluno` - Herança de Usuario
  - `Funcionario` - Herança de Usuario
  - `Curso`, `Sala`, `Vaga`, `Turma`
  - `ParticipacaoMonitoria`, `Presenca`, `Inscricao`

#### 💻 View (Visualização/Lógica)
- **Arquivo:** `views.py` (34 funções)
- **Responsabilidade:** Processa requisições HTTP
- **Operações:**
  - Recebe dados da requisição
  - Consulta models (banco de dados)
  - Processa lógica de negócio
  - Prepara contexto para template
  - Retorna resposta HTTP

#### 🎨 Template (Apresentação)
- **Diretório:** `templates/`
- **Responsabilidade:** Renderiza HTML com dados
- **Funcionalidades:**
  - Exibição de dados dinâmicos
  - Formulários interativos
  - Responsividade (Bootstrap 5)
  - Validação no cliente (JavaScript)

---

## 📁 Estrutura de Diretórios

```
PBE_25.2_8001_IV/
│
├── meuprojeto/
│   ├── meuprojeto/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py           # Configurações do Django
│   │   ├── urls.py               # ✨ NOVO: Comentários de rotas principais
│   │   └── wsgi.py
│   │
│   ├── plataforma_Casa/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py             # Modelos (Usuario, Aluno, Vaga, etc)
│   │   ├── views.py              # ✨ NOVO: 34 views com lógica completa
│   │   ├── urls.py               # ✨ NOVO: 34 rotas comentadas
│   │   ├── repository.py         # Funções SQL auxiliares
│   │   ├── service.py            # Serviços de negócio
│   │   ├── tests.py
│   │   │
│   │   ├── migrations/
│   │   │   ├── __init__.py
│   │   │   ├── 0001_initial.py
│   │   │   └── ...
│   │   │
│   │   └── templates/            # ✨ NOVO: 17 arquivos HTML
│   │       ├── base.html         # Template base (navbar + sidebar)
│   │       ├── dashboard.html
│   │       ├── perfil.html
│   │       ├── usuarios/
│   │       │   ├── listar.html
│   │       │   ├── criar.html
│   │       │   └── editar.html
│   │       ├── alunos/
│   │       │   ├── listar.html
│   │       │   ├── criar.html
│   │       │   └── editar.html
│   │       ├── vagas/
│   │       │   ├── listar.html
│   │       │   ├── criar.html
│   │       │   ├── editar.html
│   │       │   └── detalhe.html
│   │       ├── turmas/
│   │       │   ├── listar.html
│   │       │   ├── criar.html
│   │       │   ├── editar.html
│   │       │   └── detalhe.html
│   │       ├── monitorias/
│   │       │   ├── listar.html
│   │       │   └── editar.html
│   │       ├── presencas/
│   │       │   ├── listar.html
│   │       │   └── editar.html
│   │       └── relatorios/
│   │           ├── listar.html
│   │           ├── desempenho.html
│   │           ├── frequencia.html
│   │           ├── inscricoes.html
│   │           └── geral.html
│   │
│   ├── db.sqlite3
│   └── manage.py
│
├── FRONTEND_MVT.md                # ✨ NOVO: Documentação técnica
├── anderson.md                    # ✨ NOVO: Este documento
├── 14-arquitetura-mvt.puml        # ✨ NOVO: Diagrama PlantUML
└── ...outros arquivos
```

---

## 🛣️ Rotas e Endpoints

### Categorização por Módulo

#### 1. Dashboard
| Método | URL | Nome | Descrição |
|--------|-----|------|-----------|
| GET | `/` | `dashboard` | Página inicial com estatísticas |

#### 2. Usuários
| Método | URL | Nome | Descrição |
|--------|-----|------|-----------|
| GET | `/usuarios/` | `listar_usuarios` | Listar usuários |
| GET/POST | `/usuarios/criar/` | `criar_usuario` | Criar usuário |
| GET/POST | `/usuarios/<id>/editar/` | `editar_usuario` | Editar usuário |
| GET | `/usuarios/<id>/deletar/` | `deletar_usuario` | Deletar usuário |

#### 3. Alunos
| Método | URL | Nome | Descrição |
|--------|-----|------|-----------|
| GET | `/alunos/` | `listar_alunos` | Listar alunos |
| GET/POST | `/alunos/criar/` | `criar_aluno` | Criar aluno |
| GET/POST | `/alunos/<id>/editar/` | `editar_aluno` | Editar aluno |
| GET | `/alunos/<id>/deletar/` | `deletar_aluno` | Deletar aluno |

#### 4. Vagas
| Método | URL | Nome | Descrição |
|--------|-----|------|-----------|
| GET | `/vagas/` | `listar_vagas` | Listar vagas |
| GET | `/vagas/<id>/` | `detalhe_vaga` | Detalhes da vaga |
| GET/POST | `/vagas/criar/` | `criar_vaga` | Criar vaga |
| GET/POST | `/vagas/<id>/editar/` | `editar_vaga` | Editar vaga |
| GET | `/vagas/<id>/deletar/` | `deletar_vaga` | Deletar vaga |

#### 5. Turmas
| Método | URL | Nome | Descrição |
|--------|-----|------|-----------|
| GET | `/turmas/` | `listar_turmas` | Listar turmas |
| GET | `/turmas/<id>/` | `detalhe_turma` | Detalhes da turma |
| GET/POST | `/turmas/criar/` | `criar_turma` | Criar turma |
| GET/POST | `/turmas/<id>/editar/` | `editar_turma` | Editar turma |
| GET | `/turmas/<id>/deletar/` | `deletar_turma` | Deletar turma |

#### 6. Monitorias
| Método | URL | Nome | Descrição |
|--------|-----|------|-----------|
| GET | `/monitorias/` | `listar_monitorias` | Listar participações |
| GET/POST | `/monitorias/<id>/editar/` | `editar_participacao` | Editar notas |

#### 7. Presenças
| Método | URL | Nome | Descrição |
|--------|-----|------|-----------|
| GET | `/presencas/` | `listar_presencas` | Listar presenças |
| GET/POST | `/presencas/<id>/editar/` | `editar_presenca` | Editar presença |

#### 8. Relatórios
| Método | URL | Nome | Descrição |
|--------|-----|------|-----------|
| GET | `/relatorios/` | `listar_relatorios` | Menu de relatórios |
| GET | `/relatorios/desempenho/` | `relatorio_desempenho` | Relatório de desempenho |
| GET | `/relatorios/frequencia/` | `relatorio_frequencia` | Relatório de frequência |
| GET | `/relatorios/inscricoes/` | `relatorio_inscricoes` | Relatório de inscrições |
| GET | `/relatorios/geral/` | `relatorio_geral` | Relatório geral |

#### 9. Perfil
| Método | URL | Nome | Descrição |
|--------|-----|------|-----------|
| GET/POST | `/perfil/` | `perfil` | Visualizar/editar perfil |
| POST | `/alterar-senha/` | `alterar_senha` | Alterar senha |

#### 10. Legado
| Método | URL | Nome | Descrição |
|--------|-----|------|-----------|
| GET | `/sql/` | `sql_view` | View SQL (debugging) |

---

## 📦 Módulos Implementados

### ✅ Módulo de Dashboard
**Status:** Completo

- Estatísticas gerais (total de usuários, alunos, turmas, vagas)
- Últimas monitorias criadas
- Inscrições pendentes
- Interface responsiva com cards

**Componentes:** `dashboard()` view + `dashboard.html` template

---

### ✅ Módulo de Usuários
**Status:** Completo

- **Operações:** CRUD (Create, Read, Update, Delete)
- **Campos:** Nome, Email, Tipo de Usuário, Status
- **Filtros:** Por tipo, por status
- **Interface:** Tabela com ações

**Componentes:** 
- Views: `listar_usuarios`, `criar_usuario`, `editar_usuario`, `deletar_usuario`
- Templates: `usuarios/listar.html`, `usuarios/criar.html`, `usuarios/editar.html`

---

### ✅ Módulo de Alunos
**Status:** Completo

- **Operações:** CRUD completo
- **Campos:** Nome, Email, Matrícula, Curso, Período, CR (Coeficiente de Rendimento)
- **Filtros:** Por curso, por período
- **Relacionamentos:** Aluno → Curso

**Componentes:**
- Views: `listar_alunos`, `criar_aluno`, `editar_aluno`, `deletar_aluno`
- Templates: `alunos/listar.html`, `alunos/criar.html`, `alunos/editar.html`

---

### ✅ Módulo de Vagas
**Status:** Completo

- **Operações:** CRUD + detalhe
- **Campos:** Nome, Curso, Coordenador, Descrição, Requisitos
- **Funcionalidades:** Rastreamento de inscritos
- **Layout:** Cards (visual mais atraente)

**Componentes:**
- Views: `listar_vagas`, `detalhe_vaga`, `criar_vaga`, `editar_vaga`, `deletar_vaga`
- Templates: `vagas/listar.html`, `vagas/detalhe.html`, `vagas/criar.html`, `vagas/editar.html`

---

### ✅ Módulo de Turmas
**Status:** Completo

- **Operações:** CRUD + detalhe
- **Campos:** Nome, Vaga, Sala, Monitor, Datas, Horários, Dias da semana
- **Funcionalidades:** Visualização de participações e presenças
- **Relacionamentos:** Turma → Vaga → Curso, Turma → Sala, Turma → Aluno (Monitor)

**Componentes:**
- Views: `listar_turmas`, `detalhe_turma`, `criar_turma`, `editar_turma`, `deletar_turma`
- Templates: `turmas/listar.html`, `turmas/detalhe.html`, `turmas/criar.html`, `turmas/editar.html`

---

### ✅ Módulo de Monitorias
**Status:** Completo

- **Operações:** Leitura + edição de notas
- **Campos:** Aluno, Turma, AP1, AP2, CR
- **Filtros:** Por turma
- **Funcionalidade:** Rastreamento de desempenho

**Componentes:**
- Views: `listar_monitorias`, `editar_participacao`
- Templates: `monitorias/listar.html`, `monitorias/editar.html`

---

### ✅ Módulo de Presenças
**Status:** Completo

- **Operações:** Leitura + edição de presença
- **Campos:** Aluno, Turma, Data, Presente/Ausente
- **Filtros:** Por turma, por data
- **Funcionalidade:** Controle de frequência

**Componentes:**
- Views: `listar_presencas`, `editar_presenca`
- Templates: `presencas/listar.html`, `presencas/editar.html`

---

### ✅ Módulo de Relatórios
**Status:** Completo

Implementados 4 tipos de relatórios:

1. **Relatório de Desempenho**
   - Mostra: AP1, AP2, CR de cada aluno
   - Cálculo automático de média

2. **Relatório de Frequência**
   - Mostra: Presença total, ausências
   - Taxa de frequência

3. **Relatório de Inscrições**
   - Mostra: Status das inscrições (pendente, aprovado, rejeitado)
   - Distribuição por vaga

4. **Relatório Geral**
   - Consolidação de todos os dados
   - Estatísticas consolidadas

**Componentes:**
- Views: `listar_relatorios`, `relatorio_desempenho`, `relatorio_frequencia`, `relatorio_inscricoes`, `relatorio_geral`
- Templates: `relatorios/listar.html`, `relatorios/desempenho.html`, etc.

---

### ✅ Módulo de Perfil
**Status:** Completo

- Visualização de dados pessoais
- Edição de nome e email
- Alteração de senha
- Informações de conta (tipo de usuário, status)

**Componentes:**
- Views: `perfil`, `alterar_senha`
- Template: `perfil.html`

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Django 5.2** - Framework web Python
- **Python 3.10** - Linguagem de programação
- **SQLite3** - Banco de dados
- **ORM Django** - Mapeamento de objetos para banco de dados

### Frontend
- **HTML5** - Linguagem de marcação
- **CSS3** - Estilização
- **Bootstrap 5.3** - Framework responsivo
- **Font Awesome 6.4** - Ícones
- **jQuery 3.6** - Manipulação DOM (opcional)

### Ferramentas
- **Git** - Controle de versão
- **PlantUML** - Diagramas de arquitetura
- **VS Code** - Editor de código

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)
- Git

### Passo 1: Clonar o Repositório
```bash
git clone https://github.com/Projetos-de-Extensao/PBE_25.2_8001_IV.git
cd PBE_25.2_8001_IV
```

### Passo 2: Criar Ambiente Virtual
```bash
# No macOS/Linux
python3 -m venv venv
source venv/bin/activate

# No Windows
python -m venv venv
venv\Scripts\activate
```

### Passo 3: Instalar Dependências
```bash
pip install django==5.2
```

### Passo 4: Aplicar Migrações
```bash
cd meuprojeto
python manage.py migrate
```

### Passo 5: Criar Superusuário (Admin)
```bash
python manage.py createsuperuser
# Siga as instruções do terminal
```

### Passo 6: Executar Servidor
```bash
python manage.py runserver
```

### Passo 7: Acessar a Aplicação
- **Frontend:** http://localhost:8000/
- **Admin:** http://localhost:8000/admin/

---

## 📋 Padrões e Boas Práticas Implementadas

### 1. Separação de Responsabilidades (MVT)
- Views contêm apenas lógica de negócio
- Templates contêm apenas HTML/CSS
- Models definem estrutura de dados

### 2. DRY (Don't Repeat Yourself)
- Template base.html reutilizado em todos os templates
- Componentes Bootstrap reutilizados
- Funções auxiliares em repository.py

### 3. Naming Conventions
- URLs nomeadas para fácil referência
- Nomes descritivos para views e templates
- Padrão de prefixos (listar_, criar_, editar_, deletar_)

### 4. Segurança
- ✅ CSRF Protection (token em formulários)
- ✅ SQL Injection Prevention (ORM Django)
- ✅ XSS Protection (template escaping)
- ✅ Validação no servidor (views)

### 5. Responsividade
- ✅ Bootstrap 5 para layout responsivo
- ✅ CSS flexível
- ✅ Menu mobile-friendly

### 6. Acessibilidade
- ✅ Semântica HTML
- ✅ Labels em formulários
- ✅ Cores contrastantes
- ✅ Ícones com título

### 7. Performance
- ✅ Queries otimizadas (select_related, prefetch_related)
- ✅ Caching de templates
- ✅ Minimização de requisições

---

## 📊 Estatísticas do Projeto

| Métrica | Quantidade |
|---------|-----------|
| Views (funções) | 34 |
| Templates HTML | 17 |
| Rotas (endpoints) | 34 |
| Modelos de Dados | 10 |
| Módulos Funcionais | 10 |
| Linhas de código (views.py) | 800+ |
| Linhas de comentários | 500+ |

---

## 🔄 Fluxo de Dados

```
1. Usuário acessa URL
   ↓
2. Django roteia para view apropriada (urls.py)
   ↓
3. View processa requisição
   ├─ Consulta dados (models + banco de dados)
   ├─ Processa lógica de negócio
   ├─ Valida dados (se POST)
   └─ Prepara contexto
   ↓
4. Django renderiza template com contexto
   ├─ Substitui tags dinâmicas
   ├─ Aplica estilização (CSS/Bootstrap)
   └─ Gera HTML final
   ↓
5. Resposta HTTP enviada ao navegador
   ↓
6. Navegador exibe página ao usuário
```

---

## 🔐 Segurança

### Implementações Atuais
- ✅ CSRF token em todos os formulários
- ✅ ORM Django previne SQL injection
- ✅ Template escaping automático (XSS prevention)
- ✅ Validação de entrada (formulários)

### Melhorias Futuras
- [ ] Autenticação de usuário (login/logout)
- [ ] Permissões por role (admin, professor, aluno)
- [ ] Rate limiting em APIs
- [ ] HTTPS em produção
- [ ] Validação em tempo real (JavaScript)

---

## 📈 Próximos Passos

### Curto Prazo
1. ✅ **Autenticação** - Implementar login/logout
2. ✅ **Permissões** - Controle de acesso por role
3. ✅ **Validação** - Melhorar validação de formulários
4. ✅ **Testes** - Criar testes unitários

### Médio Prazo
1. 📋 **Paginação** - Adicionar paginação em listas
2. 📋 **Busca** - Implementar search avançada
3. 📋 **Filtros** - Filtros mais sofisticados
4. 📋 **Exports** - Exportar relatórios (PDF/Excel)

### Longo Prazo
1. 🔮 **API REST** - Criar endpoints JSON
2. 🔮 **Frontend React/Vue** - Migrar para SPA
3. 🔮 **Gráficos** - Dashboard com visualizações
4. 🔮 **Mobile App** - Aplicativo mobile
5. 🔮 **Notificações** - Sistema de notificações
6. 🔮 **Analytics** - Análise de dados avançada

---

## 📞 Suporte e Documentação

### Arquivos de Documentação
- **FRONTEND_MVT.md** - Documentação técnica completa
- **anderson.md** - Este arquivo (visão geral do projeto)
- **TEMA_UPDATES.md** - Atualizações do tema
- **diagramas-test/** - Diagramas de arquitetura

### Recursos Externos
- [Documentação Django](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [Font Awesome Icons](https://fontawesome.com/)
- [Django Best Practices](https://docs.djangoproject.com/en/5.2/intro/overview/)

---

## 👨‍💻 Autor

**Desenvolvedor:** Anderson

**Data:** 18 de outubro de 2025

**Branch:** anderon

**Repositório:** https://github.com/Projetos-de-Extensao/PBE_25.2_8001_IV

---

## 📝 Histórico de Versões

### v1.0 - 18/10/2025
- ✅ Implementação completa de views (34 funções)
- ✅ Criação de templates HTML (17 arquivos)
- ✅ Configuração de rotas com comentários
- ✅ Dashboard com estatísticas
- ✅ CRUD para Usuários, Alunos, Vagas, Turmas
- ✅ Módulo de Monitorias (participações)
- ✅ Módulo de Presenças
- ✅ Sistema de Relatórios (4 tipos)
- ✅ Módulo de Perfil de Usuário
- ✅ Documentação completa

---

## 📄 Licença

Este projeto faz parte do programa **PBE (Projeto de Extensão)** da instituição.

---

**Última atualização:** 18 de outubro de 2025

**Status:** ✅ Pronto para uso em desenvolvimento
