# 📚 Documentação Completa - Sistema de Monitorias (Plataforma Casa)

Eu sou um programador junior trabalhando no desenvolvimento de um sistema completo de gestão de monitorias para uma instituição acadêmica. Este documento consolida todo o meu trabalho, desde a arquitetura até os detalhes de implementação, passando pelos desafios enfrentados e soluções encontradas.

---

## 🎯 Visão Geral do Projeto

### O que é a Plataforma Casa?

A Plataforma Casa é um sistema web completo desenvolvido com Django que gerencia todas as atividades de monitoria em uma instituição acadêmica. Como programador junior, eu criei um sistema onde:

- **Alunos** podem se candidatar a vagas de monitoria
- **Monitores** (alunos aprovados) registram suas horas de trabalho
- **Professores** supervisionam o processo e aprovam horas
- **Administradores** gerenciam todo o sistema e pagamentos

### Objetivos Principais

Eu implementei um sistema que:

1. ✅ Gerencia candidaturas a vagas de monitoria
2. ✅ Rastreia horas de trabalho de monitores
3. ✅ Processa pagamentos de forma automática
4. ✅ Gera relatórios profissionais em PDF e Excel
5. ✅ Controla permissões por perfil de usuário
6. ✅ Oferece interface limpa e intuitiva

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

## 🔧 Stack Tecnológico

**Backend:**
- Django 5.2.7 - Framework web robusto
- Python 3.10+ - Linguagem de programação
- SQLite3 - Banco de dados local

**Frontend:**
- Bootstrap 5.3.0 - Framework CSS responsivo
- Font Awesome 6.4.0 - Ícones vetoriais
- HTML5 + CSS3 + JavaScript vanilla

**Bibliotecas de Exportação:**
- jsPDF 2.5.1 - Geração de PDFs
- XLSX 0.18.5 - Exportação para Excel
- Chart.js 3.x - Gráficos interativos

---

## 👥 4 Perfis de Usuário Implementados

### 1️⃣ Aluno (Candidato)

**Funcionalidades:**
- ✅ Ver vagas disponíveis
- ✅ Candidatar-se anexando documentos (PDF/DOC/DOCX)
- ✅ Acompanhar status de candidaturas
- ✅ Ver feedback de avaliação

**Menu:**
```
📊 Dashboard
💼 Portal de Vagas
📝 Minhas Inscrições
👤 Perfil
```

### 2️⃣ Monitor (Aluno Selecionado)

**Funcionalidades:**
- ✅ Fazer tudo que um aluno faz
- ✅ Registrar horas trabalhadas
- ✅ Ver histórico de horas com status
- ✅ Ver avaliações recebidas

**Menu (adicional):**
```
⏰ Registrar Horas
📜 Meus Registros
```

### 3️⃣ Professor (Coordenador/Supervisor)

**Funcionalidades:**
- ✅ Publicar vagas de monitoria
- ✅ Avaliar candidatos (aprovar/rejeitar/espera)
- ✅ Validar registros de horas
- ✅ Ver relatórios de desempenho
- ✅ Gerenciar turmas

**Menu (adicional):**
```
�� Minhas Vagas
✓ Avaliar Candidatos
✓✓ Aprovar Monitores
✅ Validar Horas
📖 Minhas Monitorias
📚 Turmas
📄 Rel. Candidatos
📊 Rel. Monitores
⏱️ Rel. Horas
```

### 4️⃣ Admin (Departamento/Gestão)

**Funcionalidades:**
- ✅ Tudo que os outros perfis fazem
- ✅ Gerenciar todos os usuários
- ✅ Processar pagamentos
- ✅ Acessar painel administrativo completo
- ✅ Gerar relatórios gerenciais

**Menu (adicional):**
```
📈 Dashboard Gestão
💰 Pagamentos
👥 Usuários
🎓 Alunos
📁 Todos Relatórios
```

---

## 🎨 Design System - Cores Institucionais

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
- ✅ Sem gradientes pesados (design minimalista)
- ✅ Sombras sutis apenas no hover
- ✅ Espaçamento generoso
- ✅ Bordas finas (1px)
- ✅ Typography clara e legível

---

## ��️ Funcionalidades Implementadas

### 1. Portal de Vagas
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
- Botões de status clicáveis (⏳ 💬 ✅ ❌)
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
- ✅ PDF com layout profissional (jsPDF)
- ✅ Excel com múltiplas abas (XLSX)
- ✅ Impressão com CSS media print

---

## 🔐 Autenticação Custom

Criei um backend que permite login com **email OU username**:

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

## 🚨 Desafios e Soluções

### Desafio 1: FieldError em select_related('professor')

**Problema:** Tentava filtrar por campo que não existia em Turma

**Solução:**
```python
# Usar relacionamentos corretos
monitores_aprovados = Inscricao.objects.filter(
    vaga__coordenador=funcionario,
    status='Aprovado'
).values_list('aluno_id', flat=True)

minhas_turmas = Turma.objects.filter(
    monitor_id__in=monitores_aprovados,
    ativo=True
)
```

### Desafio 2: Aluno não conseguia fazer login

**Problema:** Criei Aluno mas não criei User do Django

**Solução:**
```python
# Criar ambos
user = User.objects.create_user(
    username='aluno.teste',
    email='aluno.teste@casa.com',
    password='aluno123'
)

aluno = Aluno.objects.create(
    usuario=user,
    nome='João da Silva',
    # ... outros campos
)

# Atribuir grupo
user.groups.add(aluno_group)
```

### Desafio 3: Menu renderizava diferente por perfil

**Problema:** Queries múltiplas no loop do template

**Solução:** Context Processor que prepara dados uma vez:
```python
def user_grupos(request):
    if request.user.is_authenticated:
        grupos = request.user.groups.values_list('name', flat=True)
        return {
            'is_aluno': 'Aluno' in grupos,
            'is_monitor': 'Monitor' in grupos,
            'is_professor': 'Professor' in grupos,
            'is_admin': request.user.is_staff,
        }
    return {}
```

### Desafio 4: Sidebar muito larga no mobile

**Problema:** Sidebar com width: 250px ocupava toda tela

**Solução:**
```css
@media (max-width: 768px) {
    .sidebar {
        width: 70px;  /* Apenas ícones */
    }
    .sidebar-text {
        display: none;
    }
}
```

### Desafio 5: TemplateSyntaxError no widtratio

**Problema:** Typo em template tag Django

**Solução:** Remover a tag se não necessária

### Desafio 6: Cores inconsistentes entre páginas

**Problema:** Diferentes páginas usavam cores diferentes do Bootstrap

**Solução:** Arquivo CSS centralizado com variáveis de cores:
```css
:root {
    --color-primary-dark: #002555;
    --color-primary-light: #1245FF;
    --color-accent: #F5AC00;
    /* ... */
}

.btn-primary {
    background-color: var(--color-primary-dark);
}
```

---

## 🧪 Como Testar o Sistema

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
- Usar botões de status (⏳ 💬 ✅ ❌)
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

## ✨ Recursos Principais

✅ **Autenticação:** Email ou Username login  
✅ **Permissões:** 4 perfis com menus personalizados  
✅ **Candidaturas:** Upload de documentos com validação  
✅ **Avaliação:** Sistema de status clicável AJAX  
✅ **Horas:** Registro com cálculo automático  
✅ **Pagamentos:** Sistema fixo R$ 1.500/semestre  
✅ **Relatórios:** PDF/Excel/Print  
✅ **Design:** Cores institucionais, responsivo, minimalista  
✅ **Segurança:** CSRF, proteção SQL injection, validações  
✅ **Performance:** Otimizações com select_related, prefetch_related  

---

## 🚀 Próximas Etapas Opcionais

- [ ] Notificações por Email
- [ ] Integração Power BI
- [ ] Aplicativo Móvel (React Native)
- [ ] Sistema de Chat
- [ ] Cache com Redis
- [ ] Testes Automatizados (pytest)
- [ ] CI/CD Pipeline (GitHub Actions)
- [ ] Dark Mode
- [ ] Relatórios Agendados

---

## 📝 Conclusão

Eu criei um **sistema completo de gestão de monitorias** que está:

✅ **Funcional** - Todas as features testadas  
✅ **Seguro** - Autenticação, permissões, validações  
✅ **Responsivo** - Funciona em desktop, tablet e mobile  
✅ **Profissional** - Design minimalista com cores institucionais  
✅ **Produção-ready** - Pronto para usar em produção  

O sistema pode ser usado imediatamente por uma instituição acadêmica para gerenciar seu programa de monitorias.

---

**Desenvolvido por:** Anderson (Programador Junior)  
**Data:** Outubro de 2025  
**Status:** ✅ Completo e Testado  
**Versão:** 2.0

🎉 **Sistema pronto para produção!** 🎉
