# 🚀 Guia de Início Rápido - Sistema de Monitoria

## Como Começar a Usar o Sistema

### 📋 Pré-requisitos

Certifique-se de que você tem:
- ✅ Python instalado
- ✅ Django instalado
- ✅ Banco de dados migrado
- ✅ Dados de teste populados

---

## 🎬 Passo a Passo

### 1. Parar o Servidor (se estiver rodando)

```bash
# No terminal onde o servidor está rodando, pressione:
Ctrl + C

# OU execute este comando para matar processos na porta 8000:
lsof -ti:8000 | xargs kill -9
```

### 2. Navegar para o Diretório do Projeto

```bash
cd /Users/anderson/my_folders/repositoriolocal/PBE_25.2_8001_IV/meuprojeto
```

### 3. Popular o Banco com as Novas Funcionalidades

```bash
python popular_novas_funcionalidades.py
```

**Resultado esperado:**
```
✅ 11 vagas no sistema
✅ 81 inscrições criadas
✅ 20 registros de horas criados
✅ 4 pagamentos criados
✅ 8 avaliações criadas
```

### 4. Iniciar o Servidor Django

```bash
python manage.py runserver
```

**Você verá:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

---

## 🌐 Acessar as Funcionalidades

### 🏠 Portal Público de Vagas

**URL:** http://localhost:8000/portal-vagas/

**O que você verá:**
- Lista de todas as vagas ativas
- Número de vagas disponíveis
- Botão "Candidatar-se"
- Filtros por curso

**Como testar:**
1. Acesse a URL
2. Escolha uma vaga
3. Clique em "Ver Detalhes" ou "Candidatar-se"

---

### 👤 Minhas Inscrições (Aluno)

**URL:** http://localhost:8000/minhas-inscricoes/

**O que você verá:**
- Todas as suas candidaturas
- Status de cada uma:
  - ⏳ Pendente
  - ✅ Aprovado
  - ❌ Rejeitado
  - 📋 Lista de Espera
- Documentos enviados

**Como testar:**
1. Faça login como aluno
2. Acesse a URL
3. Veja suas inscrições

---

### 📝 Candidatar-se a uma Vaga

**URL:** http://localhost:8000/vagas/1/candidatar/
(Substitua `1` pelo ID da vaga)

**O que você fará:**
1. Preencher formulário
2. Fazer upload de:
   - Histórico Escolar (PDF)
   - Currículo (PDF)
   - Carta de Motivação (PDF)
3. Submeter candidatura

**Exemplo de teste:**
```bash
# 1. Acesse http://localhost:8000/portal-vagas/
# 2. Clique em uma vaga
# 3. Clique em "Candidatar-se"
# 4. Preencha e envie os documentos
```

---

### 📊 Dashboard de Gestão

**URL:** http://localhost:8000/gestao/dashboard/

**O que você verá:**
- 📈 Total de monitores ativos
- ⏱️ Horas trabalhadas no mês
- 💰 Pagamentos pendentes
- 📝 Avaliações pendentes
- 📊 Monitores por curso (gráfico)
- 📋 Vagas ativas com inscritos

**Como testar:**
1. Faça login como coordenador ou admin
2. Acesse a URL
3. Explore as métricas

---

### 🎓 Avaliar Candidatos (Coordenador)

**URL:** http://localhost:8000/vagas/1/avaliar/

**O que você fará:**
1. Ver lista de candidatos
2. Clicar em "Avaliar"
3. Atribuir nota (0-10)
4. Escrever comentários
5. Definir status:
   - ✅ Aprovado
   - ❌ Rejeitado
   - 📋 Lista de Espera
6. Comunicar resultado

**Exemplo de teste:**
```bash
# 1. Acesse http://localhost:8000/vagas/
# 2. Escolha uma vaga
# 3. Clique em "Avaliar Candidatos"
# 4. Avalie cada candidato
```

---

### ⏰ Registrar Horas (Monitor)

**URL:** http://localhost:8000/horas/registrar/

**O que você fará:**
1. Selecionar turma
2. Informar data
3. Hora de início e fim
4. Descrever atividades realizadas
5. Submeter registro

**Sistema calcula automaticamente:**
- Total de horas trabalhadas
- Status: Pendente de validação

**Exemplo de teste:**
```bash
# 1. Faça login como aluno/monitor
# 2. Acesse /horas/registrar/
# 3. Preencha o formulário
# 4. Veja em /horas/meus-registros/
```

---

### ✅ Validar Horas (Professor)

**URL:** http://localhost:8000/horas/validar/

**O que você verá:**
- Lista de registros pendentes
- Informações de cada registro:
  - Monitor
  - Data
  - Horários
  - Total de horas
  - Atividades realizadas

**O que você fará:**
1. Revisar registro
2. Aprovar ou Rejeitar
3. Adicionar observações (opcional)
4. Salvar validação

---

### 💰 Gerenciar Pagamentos (Gestão)

**URL:** http://localhost:8000/gestao/pagamentos/

**O que você verá:**
- Lista de todos os pagamentos
- Por cada pagamento:
  - Monitor
  - Mês de referência
  - Total de horas
  - Valor a pagar
  - Status

**Status possíveis:**
- ⏳ Pendente
- 🔄 Processando
- ✅ Pago
- ❌ Cancelado

**Como processar:**
```bash
# 1. Acesse /gestao/pagamentos/
# 2. Clique em "Processar" em um pagamento
# 3. Confirme ou rejeite
# 4. Adicione observações
```

---

### 📊 Relatórios Especializados

#### 1. Candidatos por Vaga
**URL:** http://localhost:8000/relatorios/candidatos-vaga/

**Mostra:**
- Todos os candidatos de cada vaga
- Status de cada candidatura
- Documentos enviados
- Filtro por vaga específica

#### 2. Monitores Selecionados
**URL:** http://localhost:8000/relatorios/monitores-selecionados/

**Mostra:**
- Monitores aprovados
- Agrupados por curso
- Total de monitores por departamento
- Filtro por curso

#### 3. Horas Trabalhadas
**URL:** http://localhost:8000/relatorios/horas-trabalhadas/

**Mostra:**
- Total de horas por monitor
- Apenas horas aprovadas
- Filtro por mês/ano
- Ranking de monitores

---

## 🔑 Usuários de Teste

### Para testar diferentes perfis, você precisará:

#### 1. Criar Usuário Admin (se não tiver)

```bash
python manage.py createsuperuser
```

- Username: `admin`
- Email: `admin@example.com`
- Password: `admin123`

#### 2. Acessar o Admin

**URL:** http://localhost:8000/admin/

**Login:**
- Username: `admin`
- Password: `admin123`

#### 3. Verificar Dados Existentes

No admin, você pode:
- Ver todos os alunos
- Ver todos os funcionários
- Ver coordenadores
- Criar novos usuários

---

## 🧪 Cenários de Teste

### Cenário 1: Fluxo Completo de Candidatura

```
1. ALUNO acessa /portal-vagas/
2. ALUNO clica em uma vaga
3. ALUNO clica em "Candidatar-se"
4. ALUNO faz upload de documentos
5. ALUNO submete candidatura
6. ALUNO acessa /minhas-inscricoes/ e vê status "Pendente"

7. COORDENADOR acessa /vagas/1/avaliar/
8. COORDENADOR clica em "Avaliar" no candidato
9. COORDENADOR atribui nota e comentários
10. COORDENADOR define status "Aprovado"
11. COORDENADOR clica em "Comunicar Resultado"

12. ALUNO acessa /minhas-inscricoes/ e vê status "Aprovado"
```

### Cenário 2: Fluxo de Registro de Horas

```
1. MONITOR acessa /horas/registrar/
2. MONITOR preenche:
   - Turma: Programação Web
   - Data: 18/10/2025
   - Início: 14:00
   - Fim: 16:00
   - Atividades: "Auxiliei alunos com exercícios de React"
3. MONITOR submete registro
4. MONITOR acessa /horas/meus-registros/ e vê status "Pendente"

5. PROFESSOR acessa /horas/validar/
6. PROFESSOR vê o registro pendente
7. PROFESSOR clica em "Validar"
8. PROFESSOR aprova com observação "Horas aprovadas"

9. MONITOR acessa /horas/meus-registros/ e vê status "Aprovado"
```

### Cenário 3: Gestão e Relatórios

```
1. GESTOR acessa /gestao/dashboard/
2. GESTOR vê:
   - 4 monitores ativos
   - 8 horas trabalhadas no mês
   - 4 pagamentos pendentes
   - 23 avaliações pendentes

3. GESTOR acessa /gestao/pagamentos/
4. GESTOR processa um pagamento
5. GESTOR acessa /relatorios/horas-trabalhadas/
6. GESTOR vê ranking de monitores por horas
```

---

## 🐛 Troubleshooting

### Problema: "Nenhum dado aparece"

**Solução:**
```bash
# Execute o script de dados de teste
python popular_novas_funcionalidades.py
```

### Problema: "Erro 404 Not Found"

**Solução:**
```bash
# Verifique se as URLs estão corretas
# Verifique se o servidor está rodando
python manage.py runserver
```

### Problema: "Erro de permissão"

**Solução:**
```bash
# Faça login com um usuário apropriado
# Aluno: para candidaturas e registro de horas
# Professor: para validação de horas
# Coordenador: para avaliação de candidatos
# Admin: para gestão completa
```

### Problema: "Erro ao fazer upload"

**Solução:**
```bash
# Crie a pasta media se não existir
mkdir -p media/documentos
```

---

## 📱 Preparação para Mobile

Para converter em API REST (futuro):

```bash
# 1. Instalar Django REST Framework
pip install djangorestframework

# 2. Adicionar ao INSTALLED_APPS
INSTALLED_APPS = [
    ...
    'rest_framework',
]

# 3. Criar serializers para os modelos
# 4. Criar ViewSets para as APIs
# 5. Configurar autenticação por token
```

---

## 📚 Recursos Adicionais

### Documentação
- `NOVAS_FUNCIONALIDADES.md` - Guia completo
- `IMPLEMENTACAO_COMPLETA.md` - Resumo técnico
- `README.md` - Visão geral do projeto

### Scripts
- `popular_dados_teste.py` - Dados básicos
- `popular_novas_funcionalidades.py` - Novas features

### Django Admin
- Acesse todos os modelos
- Edite dados diretamente
- Veja relacionamentos

---

## 🎯 Checklist de Testes

- [ ] Acessar portal de vagas
- [ ] Candidatar-se a uma vaga
- [ ] Upload de documentos
- [ ] Ver minhas inscrições
- [ ] Avaliar candidatos
- [ ] Comunicar resultado
- [ ] Registrar horas
- [ ] Validar horas
- [ ] Dashboard de gestão
- [ ] Gerenciar pagamentos
- [ ] Gerar relatórios

---

## ✅ Tudo Pronto!

O sistema está 100% funcional para testes. Explore todas as funcionalidades e veja como elas se integram!

**Dúvidas?** Consulte a documentação em `NOVAS_FUNCIONALIDADES.md`

**Bons testes! 🚀**
