# Novas Funcionalidades - Sistema de Monitoria

## 📋 Resumo das Novas Funcionalidades

Este documento descreve as novas funcionalidades implementadas no sistema de monitoria, focadas em resolver os desafios do processo de contratação, centralizando a divulgação de vagas e a recepção de candidaturas.

---

## 🎯 Funcionalidades Implementadas

### 1. Portal de Vagas Aprimorado ✅

**Descrição**: Interface pública para que coordenadores publiquem vagas de monitoria com informações detalhadas.

**Recursos**:
- ✅ Publicação de vagas com disciplina, pré-requisitos e responsabilidades
- ✅ Definição do número de vagas disponíveis
- ✅ Contagem automática de vagas preenchidas/disponíveis
- ✅ Filtros por curso e status
- ✅ Visualização pública do portal

**URLs**:
- Portal público: `/portal-vagas/`
- Criar vaga: `/vagas/criar/`
- Editar vaga: `/vagas/<id>/editar/`

**Campos Novos no Modelo Vaga**:
- `responsabilidades`: Descrição das responsabilidades do monitor
- `numero_vagas`: Quantidade total de vagas
- `disciplina`: Nome da disciplina relacionada

---

### 2. Cadastro e Candidatura de Alunos ✅

**Descrição**: Sistema completo para alunos se candidatarem às vagas, com upload de documentos.

**Recursos**:
- ✅ Perfil do candidato vinculado ao usuário Aluno
- ✅ Upload de documentos:
  - Histórico Escolar
  - Currículo
  - Carta de Motivação
- ✅ Sistema de candidatura com validação
- ✅ Acompanhamento de status da candidatura
- ✅ Prevenção de candidaturas duplicadas

**URLs**:
- Candidatar-se: `/vagas/<vaga_id>/candidatar/`
- Minhas inscrições: `/minhas-inscricoes/`

**Novo Modelo**: `Documento`
- Armazena arquivos enviados pelos candidatos
- Vinculado à inscrição
- Suporte a múltiplos tipos de documento

---

### 3. Seleção e Comunicação de Resultados ✅

**Descrição**: Ferramentas para professores e coordenadores avaliarem candidatos e comunicarem resultados.

**Recursos**:
- ✅ Painel de avaliação de candidatos por vaga
- ✅ Sistema de notas e comentários
- ✅ Status de aprovação:
  - Pendente
  - Aprovado
  - Lista de Espera
  - Rejeitado
- ✅ Registro de quem avaliou e quando
- ✅ Comunicação padronizada de resultados
- ✅ Controle de comunicação enviada

**URLs**:
- Avaliar candidatos: `/vagas/<vaga_id>/avaliar/`
- Avaliar inscrição: `/inscricoes/<inscricao_id>/avaliar/`
- Comunicar resultado: `/inscricoes/<inscricao_id>/comunicar/`

**Campos Novos no Modelo Inscricao**:
- `STATUS_CHOICES`: Opções padronizadas de status
- `nota_avaliacao`: Nota atribuída ao candidato
- `comentario_avaliacao`: Feedback do avaliador
- `avaliado_por`: Funcionário que realizou a avaliação
- `data_avaliacao`: Data/hora da avaliação
- `resultado_comunicado`: Se o resultado foi enviado
- `data_comunicacao`: Quando foi comunicado

---

### 4. Geração de Relatórios Básicos ✅

**Descrição**: Relatórios especializados para gestão do programa de monitoria.

**Relatórios Disponíveis**:

#### 4.1 Relatório de Candidatos por Vaga
- Lista de todos os candidatos inscritos em cada vaga
- Filtro por vaga específica
- Status de cada candidatura
- URL: `/relatorios/candidatos-vaga/`

#### 4.2 Relatório de Monitores Selecionados
- Monitores aprovados por disciplina
- Agrupamento por departamento/curso
- Contagem de monitores por área
- URL: `/relatorios/monitores-selecionados/`

#### 4.3 Relatório de Horas Trabalhadas
- Total de horas por monitor
- Filtro por período (mês/ano)
- Apenas horas aprovadas
- URL: `/relatorios/horas-trabalhadas/`

---

### 5. Registro de Frequência e Horas ✅

**Descrição**: Sistema completo para registro e validação de horas trabalhadas pelos monitores.

**Recursos para Monitores**:
- ✅ Registro de horas com data e horário
- ✅ Descrição das atividades realizadas
- ✅ Cálculo automático do total de horas
- ✅ Visualização do histórico de registros
- ✅ Status de validação (Pendente/Aprovado/Rejeitado)

**Recursos para Professores/Supervisores**:
- ✅ Validação de horas registradas
- ✅ Aprovação ou rejeição com observações
- ✅ Registro de quem validou e quando
- ✅ Controle de horas pendentes

**URLs**:
- Registrar horas (Monitor): `/horas/registrar/`
- Meus registros (Monitor): `/horas/meus-registros/`
- Validar horas (Professor): `/horas/validar/`
- Aprovar horas: `/horas/<registro_id>/aprovar/`

**Novo Modelo**: `RegistroHoras`
- Cálculo automático de total de horas
- Validação por funcionário
- Múltiplos status de aprovação
- Observações do validador

**Preparação para App Móvel**:
- API-ready (views podem ser convertidas para REST API)
- Estrutura de dados otimizada para mobile
- Sistema de status para sincronização

---

### 6. Dashboard de Gestão Departamental ✅

**Descrição**: Painel de controle centralizado para gestão do departamento.

**Métricas Exibidas**:
- ✅ **Número de monitores por curso**
  - Visualização por departamento
  - Contagem distinta de monitores
  - Gráfico de distribuição

- ✅ **Horas trabalhadas no mês**
  - Total de horas aprovadas
  - Filtro por período
  - Comparação mensal

- ✅ **Status de pagamentos**
  - Pagamentos pendentes
  - Pagamentos processados
  - Total a pagar

- ✅ **Avaliações pendentes**
  - Inscrições não avaliadas
  - Horas pendentes de validação
  - Alerta de prazos

- ✅ **Vagas ativas**
  - Total de vagas abertas
  - Número de inscritos por vaga
  - Taxa de preenchimento

**URLs**:
- Dashboard de gestão: `/gestao/dashboard/`
- Gerenciar pagamentos: `/gestao/pagamentos/`
- Processar pagamento: `/gestao/pagamentos/<id>/processar/`

**Novos Modelos**:

#### `StatusPagamento`
- Controle de pagamentos mensais
- Cálculo automático de valores
- Rastreamento de processamento
- Status: Pendente/Processando/Pago/Cancelado

#### `AvaliacaoMonitor`
- Avaliação de desempenho do monitor
- Notas em 4 categorias:
  - Desempenho
  - Assiduidade
  - Didática
  - Relacionamento
- Cálculo automático de média
- Comentários e feedback

---

## 👥 Tipos de Login e Permissões

### 1. **Aluno** 👨‍🎓

**Tipo de Usuário**: `aluno`

**Permissões e Funcionalidades**:
- ✅ Visualizar portal de vagas
- ✅ Candidatar-se a vagas
- ✅ Upload de documentos (histórico, currículo, carta)
- ✅ Acompanhar status de candidaturas
- ✅ Registrar horas trabalhadas (se for monitor)
- ✅ Visualizar próprio histórico de horas
- ✅ Ver relatórios de frequência própria

**Como Identificar**: Campo `tipo_usuario` = TipoUsuario.objects.get(tipo='aluno')

**Modelo**: `Aluno` (herda de `Usuario`)

---

### 2. **Professor/Supervisor** 👨‍🏫

**Tipo de Usuário**: `funcionario` (sem flag coordenador)

**Permissões e Funcionalidades**:
- ✅ Validar horas dos monitores
- ✅ Aprovar/rejeitar registros de horas
- ✅ Avaliar desempenho de monitores
- ✅ Ver relatórios de frequência
- ✅ Acompanhar turmas que supervisiona

**Como Identificar**: 
```python
funcionario = Funcionario.objects.get(email=request.user.email, coordenador=False)
```

**Modelo**: `Funcionario` (herda de `Usuario`)

---

### 3. **Coordenador** 👔

**Tipo de Usuário**: `funcionario` (com flag coordenador=True)

**Permissões e Funcionalidades**:
- ✅ Criar e publicar vagas
- ✅ Editar informações de vagas
- ✅ Avaliar candidatos
- ✅ Registrar notas de avaliação
- ✅ Comunicar resultados
- ✅ Ver todos os relatórios
- ✅ Gerenciar turmas e monitores
- ✅ Todas as permissões de Professor

**Como Identificar**:
```python
coordenador = Funcionario.objects.get(email=request.user.email, coordenador=True)
```

**Modelo**: `Funcionario` (campo `coordenador=True`)

---

### 4. **Departamento/Gestão** 🏢

**Tipo de Usuário**: `admin` ou `funcionario` com permissões elevadas

**Permissões e Funcionalidades**:
- ✅ Acesso ao Dashboard de Gestão
- ✅ Visualizar métricas gerais
- ✅ Gerenciar pagamentos
- ✅ Processar pagamentos dos monitores
- ✅ Ver todos os relatórios consolidados
- ✅ Acompanhar avaliações pendentes
- ✅ Monitorar horas trabalhadas
- ✅ Visualizar distribuição por curso

**Como Identificar**:
```python
# Usuário admin do Django ou funcionário com departamento
user.is_staff or user.is_superuser
# OU
funcionario = Funcionario.objects.get(email=request.user.email)
# Verificar departamento específico
```

---

## 📊 Modelos de Dados Criados/Atualizados

### Novos Modelos

1. **Documento**
   - `inscricao`: FK para Inscricao
   - `tipo`: Escolha entre tipos de documento
   - `arquivo`: FileField para upload
   - `nome_arquivo`: Nome original
   - `enviado_em`: Timestamp
   - `observacao`: Texto opcional

2. **RegistroHoras**
   - `turma`: FK para Turma
   - `monitor`: FK para Aluno
   - `data`: Data do registro
   - `hora_inicio`: Horário inicial
   - `hora_fim`: Horário final
   - `total_horas`: Calculado automaticamente
   - `descricao_atividade`: Texto
   - `status`: Pendente/Aprovado/Rejeitado
   - `validado_por`: FK para Funcionario
   - `data_validacao`: Timestamp
   - `observacao_validador`: Feedback

3. **StatusPagamento**
   - `monitor`: FK para Aluno
   - `turma`: FK para Turma
   - `mes_referencia`: Data (mês/ano)
   - `total_horas`: Decimal
   - `valor_hora`: Decimal
   - `valor_total`: Calculado automaticamente
   - `status`: Pendente/Processando/Pago/Cancelado
   - `processado_por`: FK para Funcionario
   - `data_processamento`: Timestamp
   - `observacao`: Texto

4. **AvaliacaoMonitor**
   - `turma`: FK para Turma
   - `monitor`: FK para Aluno
   - `avaliador`: FK para Funcionario
   - `data_avaliacao`: Data
   - `nota_desempenho`: Decimal (0-10)
   - `nota_assiduidade`: Decimal (0-10)
   - `nota_didatica`: Decimal (0-10)
   - `nota_relacionamento`: Decimal (0-10)
   - `comentarios`: Texto
   - `pontos_positivos`: Texto
   - `pontos_melhorar`: Texto
   - Método `nota_media()`: Calcula média

### Modelos Atualizados

1. **Vaga**
   - ➕ `responsabilidades`: TextField
   - ➕ `numero_vagas`: IntegerField
   - ➕ `disciplina`: CharField
   - ➕ Método `vagas_disponiveis()`: Calcula vagas restantes

2. **Inscricao**
   - ➕ `STATUS_CHOICES`: Lista de opções
   - ➕ `nota_avaliacao`: DecimalField
   - ➕ `comentario_avaliacao`: TextField
   - ➕ `avaliado_por`: FK para Funcionario
   - ➕ `data_avaliacao`: DateTimeField
   - ➕ `resultado_comunicado`: BooleanField
   - ➕ `data_comunicacao`: DateTimeField

---

## 🔧 Configurações Adicionais

### Upload de Arquivos

**settings.py**:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**urls.py (principal)**:
```python
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Estrutura de Pastas para Uploads

```
media/
└── documentos/
    └── 2025/
        └── 10/
            └── 18/
                ├── historico_joao.pdf
                ├── curriculo_maria.pdf
                └── carta_motivacao_pedro.pdf
```

---

## 🚀 Como Usar

### Para Alunos

1. **Candidatar-se a uma vaga**:
   ```
   1. Acesse /portal-vagas/
   2. Encontre a vaga desejada
   3. Clique em "Candidatar-se"
   4. Preencha o formulário
   5. Faça upload dos documentos
   6. Submeta a candidatura
   ```

2. **Acompanhar candidatura**:
   ```
   1. Acesse /minhas-inscricoes/
   2. Veja o status de cada candidatura
   3. Visualize documentos enviados
   ```

3. **Registrar horas (se for monitor)**:
   ```
   1. Acesse /horas/registrar/
   2. Selecione a turma
   3. Informe data e horários
   4. Descreva as atividades
   5. Submeta o registro
   ```

### Para Coordenadores

1. **Publicar vaga**:
   ```
   1. Acesse /vagas/criar/
   2. Preencha todos os campos
   3. Defina número de vagas
   4. Liste requisitos e responsabilidades
   5. Publique a vaga
   ```

2. **Avaliar candidatos**:
   ```
   1. Acesse /vagas/<id>/avaliar/
   2. Visualize lista de candidatos
   3. Clique em "Avaliar" para cada um
   4. Atribua nota e comentários
   5. Defina status (Aprovado/Rejeitado/Lista de Espera)
   6. Comunique o resultado
   ```

### Para Professores

1. **Validar horas**:
   ```
   1. Acesse /horas/validar/
   2. Veja registros pendentes
   3. Clique em "Validar"
   4. Aprove ou rejeite
   5. Adicione observações se necessário
   ```

### Para Gestão

1. **Acessar dashboard**:
   ```
   1. Acesse /gestao/dashboard/
   2. Visualize métricas em tempo real
   3. Identifique pendências
   4. Tome decisões baseadas em dados
   ```

2. **Gerenciar pagamentos**:
   ```
   1. Acesse /gestao/pagamentos/
   2. Veja lista de pagamentos
   3. Filtre por status
   4. Processe pagamentos pendentes
   ```

---

## 📈 Relatórios Disponíveis

### 1. Candidatos por Vaga
- **URL**: `/relatorios/candidatos-vaga/`
- **Filtros**: Vaga específica
- **Dados**: Lista completa de inscritos, status, documentos

### 2. Monitores Selecionados
- **URL**: `/relatorios/monitores-selecionados/`
- **Filtros**: Curso, departamento
- **Dados**: Monitores aprovados, distribuição por área

### 3. Horas Trabalhadas
- **URL**: `/relatorios/horas-trabalhadas/`
- **Filtros**: Mês, ano
- **Dados**: Total de horas por monitor, apenas aprovadas

### 4. Relatórios Existentes (mantidos)
- Desempenho: `/relatorios/desempenho/`
- Frequência: `/relatorios/frequencia/`
- Inscrições: `/relatorios/inscricoes/`
- Geral: `/relatorios/geral/`

---

## 🔐 Segurança e Validações

### Validações Implementadas

1. **Candidatura**:
   - ✅ Verificar se usuário é aluno
   - ✅ Prevenir candidaturas duplicadas
   - ✅ Validar se vaga está ativa

2. **Registro de Horas**:
   - ✅ Verificar se usuário é monitor
   - ✅ Calcular horas automaticamente
   - ✅ Validar datas e horários

3. **Upload de Arquivos**:
   - ✅ Organização por data
   - ✅ Nome único para evitar sobrescrita
   - ✅ Vinculação à inscrição

### Permissões

- Decorador `@login_required` em views sensíveis
- Verificação de tipo de usuário nas views
- Controle de acesso baseado em perfil

---

## 📱 Preparação para App Móvel

As seguintes views estão prontas para serem convertidas em API REST:

1. `registrar_horas` - POST para registro móvel
2. `meus_registros_horas` - GET para listar
3. `portal_vagas` - GET para visualização
4. `minhas_inscricoes` - GET para acompanhamento

**Próximos Passos**:
- Instalar Django REST Framework
- Criar serializers
- Criar endpoints API
- Implementar autenticação por token

---

## ✅ Checklist de Implementação

- [x] Modelos criados e migrados
- [x] Views implementadas
- [x] URLs configuradas
- [x] Admin registrado
- [x] Upload de arquivos configurado
- [ ] Templates HTML criados (próxima etapa)
- [ ] Testes implementados
- [ ] Documentação de API para mobile

---

## 🎨 Próximos Passos

1. **Criar Templates HTML**:
   - Portal de vagas
   - Formulário de candidatura
   - Dashboard de gestão
   - Formulário de avaliação
   - Registro de horas

2. **Melhorias**:
   - Sistema de notificações por email
   - Gráficos no dashboard
   - Exportação de relatórios em PDF/Excel
   - API REST para mobile

3. **Testes**:
   - Testes unitários para models
   - Testes de integração para views
   - Testes de upload de arquivos

---

## 📞 Suporte

Para dúvidas sobre as novas funcionalidades, consulte:
- Este documento
- Código comentado em `views.py`
- Modelos em `models.py`
- URLs em `urls.py`

---

**Data de Implementação**: 18 de outubro de 2025
**Versão**: 2.0
**Status**: ✅ Backend completo - Templates pendentes
