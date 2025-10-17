# 🎓 Sistema de Gestão de Monitorias

Sistema completo para gestão de monitorias acadêmicas com Django REST Framework e React.

## ✨ Funcionalidades Implementadas

### 🔐 Sistema de Autenticação
- ✅ Tela de login profissional e centralizada
- ✅ Sistema de registro de novos usuários
- ✅ Autenticação JWT (JSON Web Tokens)
- ✅ Proteção de rotas no frontend
- ✅ Múltiplos tipos de usuários

### 📊 Dashboard Interativo
- ✅ Gráficos de frequência em tempo real
- ✅ Estatísticas de inscrições por mês
- ✅ Análise de presenças e faltas por turma
- ✅ Ranking de vagas mais procuradas
- ✅ Cards com totais (alunos, monitores, turmas, vagas)

### 👥 Gestão de Usuários
- ✅ **Administradores**: Controle total do sistema
- ✅ **Coordenadores**: Gestão de vagas, turmas e aprovações
- ✅ **Professores**: Indicação de alunos e aprovação de candidaturas
- ✅ **Monitores**: Gestão de disponibilidade e submissão de horas
- ✅ **Alunos**: Busca e agendamento de monitorias

### 📅 Sistema de Agendamento
- ✅ Calendário visual para agendar monitorias
- ✅ Definição de horários disponíveis pelos monitores
- ✅ Sistema de confirmação/cancelamento
- ✅ Histórico de agendamentos

### ⏰ Gestão de Horas
- ✅ Submissão automática de horas pelos monitores
- ✅ Aprovação/rejeição por coordenadores
- ✅ Controle de horas mensais
- ✅ Observações e feedback

### 📑 Relatórios e Exportação
- ✅ Exportação para Excel (XLSX)
- ✅ Relatórios de frequência
- ✅ Relatórios de presenças
- ✅ Dados para stakeholders (ex: Equipe CASAS)

### 🎨 Interface Moderna
- ✅ Design profissional com paleta #002555
- ✅ Componentes reutilizáveis
- ✅ Responsivo para mobile e desktop
- ✅ Animações e transições suaves
- ✅ Ícones intuitivos (React Icons)

## 🚀 Como Usar

### 1. Iniciar o Sistema

```bash
# Navegar para a pasta do backend
cd backend

# Criar usuários do sistema
python create_users.py

# Iniciar o servidor
python manage.py runserver
```

### 2. Acessar o Sistema

Abra seu navegador em: **http://127.0.0.1:8000/login**

### 3. Credenciais de Acesso

| Tipo | Usuário | Senha | Descrição |
|------|---------|-------|-----------|
| **Administrador** | `admin` | `admin123` | Acesso total ao sistema |
| **Seu Usuário** | `anderson` | `1234` | Seu acesso pessoal |
| **Coordenador** | `coord1` | `coord123` | Gestão e aprovações |
| **Monitor** | `monitor1` | `monitor123` | Gerenciar monitorias |
| **Aluno** | `aluno1` | `aluno123` | Agendar monitorias |

## 📂 Estrutura do Projeto

```
PBE_25.2_8001_IV/
├── backend/                      # Django Backend
│   ├── gestao_monitoria/        # App principal
│   │   ├── models.py           # Modelos de dados
│   │   ├── views.py            # Views e APIs
│   │   ├── serializers.py      # Serializers DRF
│   │   └── urls.py             # Rotas da API
│   ├── configs/                # Configurações
│   │   ├── settings.py         # Settings Django
│   │   └── urls.py             # URLs principais
│   ├── create_users.py         # Script criar usuários
│   ├── init_system.py          # Script inicialização completa
│   └── db.sqlite3              # Banco de dados
│
└── frontend/                    # React Frontend
    ├── src/
    │   ├── components/         # Componentes reutilizáveis
    │   │   ├── Header.js      # Cabeçalho das páginas
    │   │   └── Sidebar.js     # Menu lateral
    │   ├── pages/             # Páginas da aplicação
    │   │   ├── Login.js       # Tela de login
    │   │   ├── Dashboard.js   # Dashboard com gráficos
    │   │   ├── Alunos.js      # Gestão de alunos
    │   │   ├── Turmas.js      # Gestão de turmas
    │   │   ├── Vagas.js       # Gestão de vagas
    │   │   ├── Cursos.js      # Gestão de cursos
    │   │   └── Presencas.js   # Controle de presença
    │   ├── services/
    │   │   └── api.js         # Configuração do Axios
    │   └── App.js             # App principal
    └── build/                  # Build de produção
```

## 🛠️ Tecnologias Utilizadas

### Backend
- **Django 4.2.7** - Framework web Python
- **Django REST Framework 3.16.1** - API REST
- **Simple JWT** - Autenticação JWT
- **django-cors-headers** - CORS
- **django-filter** - Filtros avançados
- **openpyxl** - Exportação Excel
- **SQLite** - Banco de dados

### Frontend
- **React 18** - Framework JavaScript
- **React Router** - Roteamento
- **Axios** - Requisições HTTP
- **Recharts** - Gráficos interativos
- **React Icons** - Ícones
- **Framer Motion** - Animações

## 📋 Modelos de Dados

### Principais Entidades

1. **TipoUsuario**: Tipos de usuários do sistema
2. **Curso**: Cursos disponíveis
3. **Sala**: Salas para monitorias
4. **Usuario**: Usuários base (herança)
5. **Aluno**: Estudantes e monitores
6. **Funcionario**: Coordenadores e professores
7. **Vaga**: Vagas de monitoria
8. **Turma**: Turmas de monitoria
9. **HorarioDisponivel**: Horários dos monitores
10. **AgendamentoMonitoria**: Agendamentos de alunos
11. **SubmissaoHoras**: Submissão de horas dos monitores
12. **Presenca**: Controle de frequência
13. **Inscricao**: Inscrições em vagas

## 🔗 Endpoints da API

### Autenticação
- `POST /api/auth/register/` - Registrar novo usuário
- `POST /api/auth/login/` - Fazer login
- `GET /api/auth/profile/` - Perfil do usuário
- `POST /api/auth/token/refresh/` - Renovar token

### Dashboard
- `GET /api/dashboard/stats/` - Estatísticas gerais

### CRUD Completo
- `/api/alunos/` - Gestão de alunos
- `/api/turmas/` - Gestão de turmas
- `/api/vagas/` - Gestão de vagas
- `/api/cursos/` - Gestão de cursos
- `/api/presencas/` - Controle de presenças
- `/api/horarios-disponiveis/` - Horários dos monitores
- `/api/agendamentos/` - Agendamentos de monitorias
- `/api/submissoes-horas/` - Submissão de horas

### Relatórios
- `GET /api/relatorios/exportar/?tipo=geral` - Exportar Excel

## 🎯 Próximos Passos

### Para Produção
1. Configurar variáveis de ambiente
2. Usar PostgreSQL em vez de SQLite
3. Configurar HTTPS
4. Implementar cache (Redis)
5. Adicionar logs estruturados
6. Configurar backup automático

### Funcionalidades Futuras
- [ ] Sistema de notificações em tempo real
- [ ] Chat entre aluno e monitor
- [ ] Avaliação de monitorias
- [ ] Certificados automáticos
- [ ] Integração com calendário (Google/Outlook)
- [ ] App mobile (React Native)

## 📸 Screenshots

### Tela de Login
- Design limpo e profissional
- Fundo neutro (#f5f5f5)
- Formulário centralizado
- Validação em tempo real

### Dashboard
- Gráficos interativos com Recharts
- Cards com estatísticas principais
- Exportação de relatórios
- Responsivo e animado

## 🐛 Solução de Problemas

### Erro de CORS
Se encontrar erros de CORS, verifique:
```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:8000",
]
```

### Erro 404 nas Rotas da API
Verifique se as URLs estão corretas:
- Backend: `http://127.0.0.1:8000/api/`
- Frontend: Configurado em `src/services/api.js`

### Problemas com Migrations
```bash
# Limpar cache
find . -type d -name "__pycache__" -exec rm -rf {} +

# Recriar migrations
python manage.py makemigrations
python manage.py migrate
```

## 📝 Licença

Este projeto foi desenvolvido para fins acadêmicos.

## 👨‍💻 Desenvolvimento

Desenvolvido com ❤️ para o projeto PBE 25.2 - 8001_IV

---

**Acesse agora:** http://127.0.0.1:8000/login

**Usuário:** `anderson` | **Senha:** `1234`
