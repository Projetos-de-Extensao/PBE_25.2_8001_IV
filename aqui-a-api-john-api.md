# 🏠 API Plataforma CASA - Documentação Completa

## 📋 Visão Geral

A **API Plataforma CASA** é uma API REST completa para gerenciamento de monitoria acadêmica. A API está disponível em **produção** no Heroku e permite gerenciar disciplinas, vagas, turmas, inscrições, presenças, horas trabalhadas, pagamentos e materiais de apoio.

### 🌐 URLs da API

- **Base URL (Produção):** `https://plataformacasa-a2a3d2abfd5e.herokuapp.com`
- **Documentação Swagger (Interativa):** [https://plataformacasa-a2a3d2abfd5e.herokuapp.com/restapi/](https://plataformacasa-a2a3d2abfd5e.herokuapp.com/restapi/)
- **Documentação ReDoc (Visual):** [https://plataformacasa-a2a3d2abfd5e.herokuapp.com/redoc/](https://plataformacasa-a2a3d2abfd5e.herokuapp.com/redoc/)

### 🔑 Autenticação

**Status atual:** A API está **aberta e pública** (não requer autenticação).

```
Permissão: AllowAny
```

Todos os endpoints podem ser acessados sem token ou credenciais. Para produção, recomenda-se implementar autenticação por token JWT ou OAuth2.

---

## 📚 Estrutura da API

### **Base Endpoints**
Gerenciamento de dados base do sistema

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/tipos-usuario/` | GET | Lista todos os tipos de usuário |
| `/api/tipos-usuario/` | POST | Cria novo tipo de usuário |
| `/api/tipos-usuario/{id}/` | GET | Detalhes de um tipo específico |
| `/api/tipos-usuario/{id}/` | PUT/PATCH | Atualiza tipo de usuário |
| `/api/tipos-usuario/{id}/` | DELETE | Remove tipo de usuário |
| `/api/tipos-usuario/ativos/` | GET | Lista apenas tipos ativos |

### **Cursos**
Gerenciamento de cursos acadêmicos

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/cursos/` | GET | Lista todos os cursos |
| `/api/cursos/` | POST | Cria novo curso |
| `/api/cursos/{id}/` | GET | Detalhes de um curso |
| `/api/cursos/{id}/` | PUT/PATCH | Atualiza curso |
| `/api/cursos/{id}/` | DELETE | Remove curso |
| `/api/cursos/ativos/` | GET | Lista apenas cursos ativos |
| `/api/cursos/{id}/estatisticas/` | GET | Estatísticas do curso |

### **Salas**
Gerenciamento de salas

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/salas/` | GET | Lista todas as salas |
| `/api/salas/` | POST | Cria nova sala |
| `/api/salas/{id}/` | GET | Detalhes de uma sala |
| `/api/salas/{id}/` | PUT/PATCH | Atualiza sala |
| `/api/salas/{id}/` | DELETE | Remove sala |
| `/api/salas/disponiveis/` | GET | Lista salas disponíveis |

### **Disciplinas**
Gerenciamento completo de disciplinas

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/disciplinas/` | GET | Lista todas as disciplinas |
| `/api/disciplinas/` | POST | Cria nova disciplina |
| `/api/disciplinas/{id}/` | GET | Detalhes de uma disciplina |
| `/api/disciplinas/{id}/` | PUT/PATCH | Atualiza disciplina |
| `/api/disciplinas/{id}/` | DELETE | Remove disciplina |
| `/api/disciplinas/por_curso/` | GET | Disciplinas de um curso (param: `curso_id`) |
| `/api/disciplinas/por_periodo/` | GET | Disciplinas de um período (param: `periodo`) |
| `/api/disciplinas/ativas/` | GET | Lista apenas disciplinas ativas |
| `/api/disciplinas/com_vagas/` | GET | Disciplinas com vagas abertas |
| `/api/disciplinas/{id}/pre_requisitos_recursivo/` | GET | Todos os pré-requisitos recursivamente |

### **Usuários**
Gerenciamento de usuários base

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/usuarios/` | GET | Lista todos os usuários |
| `/api/usuarios/` | POST | Cria novo usuário |
| `/api/usuarios/{id}/` | GET | Detalhes de um usuário |
| `/api/usuarios/{id}/` | PUT/PATCH | Atualiza usuário |
| `/api/usuarios/{id}/` | DELETE | Remove usuário |

### **Funcionários**
Gerenciamento de professores e coordenadores

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/funcionarios/` | GET | Lista todos os funcionários |
| `/api/funcionarios/` | POST | Cria novo funcionário |
| `/api/funcionarios/{id}/` | GET | Detalhes de um funcionário |
| `/api/funcionarios/{id}/` | PUT/PATCH | Atualiza funcionário |
| `/api/funcionarios/{id}/` | DELETE | Remove funcionário |
| `/api/funcionarios/coordenadores/` | GET | Lista apenas coordenadores |
| `/api/funcionarios/por_departamento/` | GET | Lista por departamento (param: `departamento`) |

### **Alunos**
Gerenciamento de alunos

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/alunos/` | GET | Lista todos os alunos |
| `/api/alunos/` | POST | Cria novo aluno |
| `/api/alunos/{id}/` | GET | Detalhes de um aluno |
| `/api/alunos/{id}/` | PUT/PATCH | Atualiza aluno |
| `/api/alunos/{id}/` | DELETE | Remove aluno |
| `/api/alunos/por_curso/` | GET | Alunos de um curso (param: `curso_id`) |
| `/api/alunos/por_periodo/` | GET | Alunos de um período (param: `periodo`) |
| `/api/alunos/monitores/` | GET | Lista alunos que são monitores |
| `/api/alunos/{id}/desempenho/` | GET | Desempenho acadêmico do aluno |

### **Vagas**
Gerenciamento de vagas de monitoria

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/vagas/` | GET | Lista todas as vagas |
| `/api/vagas/` | POST | Cria nova vaga |
| `/api/vagas/{id}/` | GET | Detalhes de uma vaga |
| `/api/vagas/{id}/` | PUT/PATCH | Atualiza vaga |
| `/api/vagas/{id}/` | DELETE | Remove vaga |
| `/api/vagas/ativas/` | GET | Lista vagas ativas |
| `/api/vagas/por_curso/` | GET | Vagas de um curso (param: `curso_id`) |
| `/api/vagas/com_vagas_disponiveis/` | GET | Vagas ainda disponíveis |
| `/api/vagas/{id}/inscricoes/` | GET | Inscrições da vaga |
| `/api/vagas/{id}/adicionar_coordenador/` | POST | Adiciona coordenador (body: `coordenador_id`) |
| `/api/vagas/{id}/remover_coordenador/` | POST | Remove coordenador (body: `coordenador_id`) |
| `/api/vagas/{id}/adicionar_professor/` | POST | Adiciona professor (body: `professor_id`) |
| `/api/vagas/{id}/remover_professor/` | POST | Remove professor (body: `professor_id`) |

### **Turmas**
Gerenciamento de turmas de monitoria

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/turmas/` | GET | Lista todas as turmas |
| `/api/turmas/` | POST | Cria nova turma |
| `/api/turmas/{id}/` | GET | Detalhes de uma turma |
| `/api/turmas/{id}/` | PUT/PATCH | Atualiza turma |
| `/api/turmas/{id}/` | DELETE | Remove turma |
| `/api/turmas/ativas/` | GET | Lista turmas ativas |
| `/api/turmas/por_monitor/` | GET | Turmas de um monitor (param: `monitor_id`) |
| `/api/turmas/por_periodo/` | GET | Turmas no período atual |
| `/api/turmas/{id}/participantes/` | GET | Participantes da turma |
| `/api/turmas/{id}/presencas/` | GET | Presenças da turma |
| `/api/turmas/{id}/materiais/` | GET | Materiais de apoio da turma |

### **Participações**
Gerenciamento de participação em monitorias

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/participacoes/` | GET | Lista todas as participações |
| `/api/participacoes/` | POST | Registra nova participação |
| `/api/participacoes/{id}/` | GET | Detalhes de uma participação |
| `/api/participacoes/{id}/` | PUT/PATCH | Atualiza participação |
| `/api/participacoes/{id}/` | DELETE | Remove participação |
| `/api/participacoes/por_aluno/` | GET | Participações de um aluno (param: `aluno_id`) |
| `/api/participacoes/por_turma/` | GET | Participações de uma turma (param: `turma_id`) |

### **Presenças**
Controle de frequência

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/presencas/` | GET | Lista todos os registros de presença |
| `/api/presencas/` | POST | Registra nova presença |
| `/api/presencas/{id}/` | GET | Detalhes de uma presença |
| `/api/presencas/{id}/` | PUT/PATCH | Atualiza presença |
| `/api/presencas/{id}/` | DELETE | Remove presença |
| `/api/presencas/por_aluno/` | GET | Presenças de um aluno (param: `aluno_id`) |
| `/api/presencas/por_turma/` | GET | Presenças de uma turma (param: `turma_id`) |
| `/api/presencas/por_data/` | GET | Presenças em uma data (param: `data` YYYY-MM-DD) |
| `/api/presencas/taxa_presenca/` | GET | Taxa de presença (params: `aluno_id` ou `turma_id`) |

### **Inscrições**
Gerenciamento de inscrições em vagas

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/inscricoes/` | GET | Lista todas as inscrições |
| `/api/inscricoes/` | POST | Cria nova inscrição |
| `/api/inscricoes/{id}/` | GET | Detalhes de uma inscrição |
| `/api/inscricoes/{id}/` | PUT/PATCH | Atualiza inscrição |
| `/api/inscricoes/{id}/` | DELETE | Remove inscrição |
| `/api/inscricoes/por_status/` | GET | Inscrições por status (param: `status`) |
| `/api/inscricoes/por_aluno/` | GET | Inscrições de um aluno (param: `aluno_id`) |
| `/api/inscricoes/por_vaga/` | GET | Inscrições de uma vaga (param: `vaga_id`) |
| `/api/inscricoes/{id}/aprovar/` | POST | Aprova inscrição |
| `/api/inscricoes/{id}/rejeitar/` | POST | Rejeita inscrição |

### **Documentos**
Gerenciamento de documentos de inscrição

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/documentos/` | GET | Lista todos os documentos |
| `/api/documentos/` | POST | Upload de novo documento |
| `/api/documentos/{id}/` | GET | Detalhes de um documento |
| `/api/documentos/{id}/` | PUT/PATCH | Atualiza documento |
| `/api/documentos/{id}/` | DELETE | Remove documento |
| `/api/documentos/por_inscricao/` | GET | Documentos de uma inscrição (param: `inscricao_id`) |
| `/api/documentos/por_tipo/` | GET | Documentos por tipo (param: `tipo`) |

### **Registro de Horas**
Controle de horas trabalhadas pelos monitores

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/registro-horas/` | GET | Lista todos os registros |
| `/api/registro-horas/` | POST | Cria novo registro de horas |
| `/api/registro-horas/{id}/` | GET | Detalhes de um registro |
| `/api/registro-horas/{id}/` | PUT/PATCH | Atualiza registro |
| `/api/registro-horas/{id}/` | DELETE | Remove registro |
| `/api/registro-horas/por_monitor/` | GET | Registros de um monitor (param: `monitor_id`) |
| `/api/registro-horas/por_turma/` | GET | Registros de uma turma (param: `turma_id`) |
| `/api/registro-horas/por_status/` | GET | Registros por status (param: `status`) |
| `/api/registro-horas/pendentes/` | GET | Registros pendentes de validação |
| `/api/registro-horas/{id}/aprovar/` | POST | Aprova registro de horas |
| `/api/registro-horas/{id}/rejeitar/` | POST | Rejeita registro (body: `observacao`) |
| `/api/registro-horas/total_horas_monitor/` | GET | Total de horas aprovadas (param: `monitor_id`) |

### **Pagamentos**
Gerenciamento de pagamentos

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/pagamentos/` | GET | Lista todos os pagamentos |
| `/api/pagamentos/` | POST | Cria novo pagamento |
| `/api/pagamentos/{id}/` | GET | Detalhes de um pagamento |
| `/api/pagamentos/{id}/` | PUT/PATCH | Atualiza pagamento |
| `/api/pagamentos/{id}/` | DELETE | Remove pagamento |
| `/api/pagamentos/por_monitor/` | GET | Pagamentos de um monitor (param: `monitor_id`) |
| `/api/pagamentos/por_status/` | GET | Pagamentos por status (param: `status`) |
| `/api/pagamentos/pendentes/` | GET | Pagamentos pendentes |
| `/api/pagamentos/{id}/processar/` | POST | Processa pagamento |

### **Materiais de Apoio**
Gerenciamento de materiais das turmas

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/materiais/` | GET | Lista todos os materiais |
| `/api/materiais/` | POST | Upload de novo material |
| `/api/materiais/{id}/` | GET | Detalhes de um material |
| `/api/materiais/{id}/` | PUT/PATCH | Atualiza material |
| `/api/materiais/{id}/` | DELETE | Remove material |
| `/api/materiais/por_turma/` | GET | Materiais de uma turma (param: `turma_id`) |
| `/api/materiais/por_tipo/` | GET | Materiais por tipo (param: `tipo`) |
| `/api/materiais/publicados/` | GET | Lista materiais publicados |

### **Estatísticas**
Análise e relatórios do sistema

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/estatisticas/geral/` | GET | Estatísticas gerais do sistema |

---

## 🚀 Como Usar a API

### **1. Usando o Swagger UI (Recomendado para Testes)**

Acesse: [https://plataformacasa-a2a3d2abfd5e.herokuapp.com/restapi/](https://plataformacasa-a2a3d2abfd5e.herokuapp.com/restapi/)

**Vantagens:**
- Interface interativa
- Teste endpoints diretamente no navegador
- Visualize request/response em tempo real
- Exemplos de código gerados automaticamente

**Como usar:**
1. Clique em um endpoint
2. Clique em "Try it out"
3. Preencha os parâmetros necessários
4. Clique em "Execute"
5. Veja a resposta

### **2. Usando o ReDoc (Recomendado para Documentação)**

Acesse: [https://plataformacasa-a2a3d2abfd5e.herokuapp.com/redoc/](https://plataformacasa-a2a3d2abfd5e.herokuapp.com/redoc/)

**Vantagens:**
- Documentação visual limpa e organizada
- Melhor para ler e entender a API
- Busca por endpoints
- Exemplos de código

### **3. Usando cURL (Linha de Comando)**

```bash
# Listar todos os cursos
curl -X GET "https://plataformacasa-a2a3d2abfd5e.herokuapp.com/api/cursos/"

# Buscar curso específico
curl -X GET "https://plataformacasa-a2a3d2abfd5e.herokuapp.com/api/cursos/1/"

# Criar novo curso
curl -X POST "https://plataformacasa-a2a3d2abfd5e.herokuapp.com/api/cursos/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Engenharia de Software",
    "ativo": true
  }'

# Atualizar curso
curl -X PATCH "https://plataformacasa-a2a3d2abfd5e.herokuapp.com/api/cursos/1/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Engenharia de Software - Atualizado"
  }'

# Deletar curso
curl -X DELETE "https://plataformacasa-a2a3d2abfd5e.herokuapp.com/api/cursos/1/"
```

### **4. Usando Python (Requests)**

```python
import requests

BASE_URL = "https://plataformacasa-a2a3d2abfd5e.herokuapp.com"

# Listar todos os cursos
response = requests.get(f"{BASE_URL}/api/cursos/")
cursos = response.json()
print(cursos)

# Criar novo curso
novo_curso = {
    "nome": "Ciência da Computação",
    "ativo": True
}
response = requests.post(f"{BASE_URL}/api/cursos/", json=novo_curso)
print(response.json())

# Buscar curso específico
curso_id = 1
response = requests.get(f"{BASE_URL}/api/cursos/{curso_id}/")
print(response.json())

# Atualizar curso
dados_atualizados = {
    "nome": "Ciência da Computação - Atualizado"
}
response = requests.patch(f"{BASE_URL}/api/cursos/{curso_id}/", json=dados_atualizados)
print(response.json())

# Deletar curso
response = requests.delete(f"{BASE_URL}/api/cursos/{curso_id}/")
print(response.status_code)  # 204 No Content
```

### **5. Usando JavaScript (Fetch API)**

```javascript
const BASE_URL = "https://plataformacasa-a2a3d2abfd5e.herokuapp.com";

// Listar todos os cursos
fetch(`${BASE_URL}/api/cursos/`)
  .then(response => response.json())
  .then(data => console.log(data));

// Criar novo curso
fetch(`${BASE_URL}/api/cursos/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    nome: "Engenharia de Software",
    ativo: true
  })
})
  .then(response => response.json())
  .then(data => console.log(data));

// Atualizar curso
fetch(`${BASE_URL}/api/cursos/1/`, {
  method: 'PATCH',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    nome: "Engenharia de Software - Atualizado"
  })
})
  .then(response => response.json())
  .then(data => console.log(data));

// Deletar curso
fetch(`${BASE_URL}/api/cursos/1/`, {
  method: 'DELETE'
})
  .then(response => console.log(response.status));
```

### **6. Usando Axios (JavaScript)**

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://plataformacasa-a2a3d2abfd5e.herokuapp.com/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Listar todos os cursos
api.get('/cursos/')
  .then(response => console.log(response.data))
  .catch(error => console.error(error));

// Criar novo curso
api.post('/cursos/', {
  nome: "Engenharia de Software",
  ativo: true
})
  .then(response => console.log(response.data))
  .catch(error => console.error(error));

// Atualizar curso
api.patch('/cursos/1/', {
  nome: "Engenharia de Software - Atualizado"
})
  .then(response => console.log(response.data))
  .catch(error => console.error(error));

// Deletar curso
api.delete('/cursos/1/')
  .then(response => console.log(response.status))
  .catch(error => console.error(error));
```

---

## 📊 Exemplos de Uso Completo

### **Exemplo 1: Fluxo de Criação de Vaga de Monitoria**

```python
import requests

BASE_URL = "https://plataformacasa-a2a3d2abfd5e.herokuapp.com/api"

# 1. Criar disciplina
disciplina = {
    "codigo": "ENG001",
    "nome": "Estruturas de Dados",
    "curso": 1,
    "periodo_sugerido": 3,
    "carga_horaria": 80,
    "ementa": "Introdução a estruturas de dados...",
    "ativo": True
}
resp = requests.post(f"{BASE_URL}/disciplinas/", json=disciplina)
disciplina_id = resp.json()['id']

# 2. Criar vaga de monitoria
vaga = {
    "nome": "Monitor de Estruturas de Dados",
    "curso": 1,
    "disciplina": disciplina_id,
    "tipo_vaga": "TEA",
    "valor_bolsa": 1500.00,
    "descricao": "Auxiliar alunos nas práticas...",
    "requisitos": "CR mínimo 7.0, ter cursado a disciplina",
    "numero_vagas": 2,
    "ativo": True
}
resp = requests.post(f"{BASE_URL}/vagas/", json=vaga)
vaga_id = resp.json()['id']

# 3. Adicionar coordenador à vaga
requests.post(f"{BASE_URL}/vagas/{vaga_id}/adicionar_coordenador/", json={
    "coordenador_id": 1
})

print(f"Vaga criada com sucesso! ID: {vaga_id}")
```

### **Exemplo 2: Gerenciar Inscrições**

```python
# 1. Listar inscrições pendentes de uma vaga
vaga_id = 1
resp = requests.get(f"{BASE_URL}/inscricoes/por_vaga/", params={"vaga_id": vaga_id})
inscricoes = resp.json()

# 2. Aprovar inscrição
inscricao_id = inscricoes[0]['id']
requests.post(f"{BASE_URL}/inscricoes/{inscricao_id}/aprovar/")

# 3. Rejeitar inscrição
requests.post(f"{BASE_URL}/inscricoes/{inscricao_id}/rejeitar/")
```

### **Exemplo 3: Controle de Presença**

```python
from datetime import date

# 1. Registrar presença
presenca = {
    "turma": 1,
    "aluno": 5,
    "data": str(date.today()),
    "presente": True
}
requests.post(f"{BASE_URL}/presencas/", json=presenca)

# 2. Calcular taxa de presença de um aluno
resp = requests.get(f"{BASE_URL}/presencas/taxa_presenca/", params={"aluno_id": 5})
taxa = resp.json()
print(f"Taxa de presença: {taxa['taxa_presenca']}%")
```

### **Exemplo 4: Registro e Validação de Horas**

```python
# 1. Monitor registra horas trabalhadas
registro = {
    "turma": 1,
    "monitor": 5,
    "data": "2025-10-31",
    "hora_inicio": "14:00:00",
    "hora_fim": "18:00:00",
    "total_horas": 4.0,
    "atividade": "Aula de exercícios",
    "status": "Pendente"
}
resp = requests.post(f"{BASE_URL}/registro-horas/", json=registro)
registro_id = resp.json()['id']

# 2. Professor aprova registro
requests.post(f"{BASE_URL}/registro-horas/{registro_id}/aprovar/")

# 3. Verificar total de horas do monitor
resp = requests.get(f"{BASE_URL}/registro-horas/total_horas_monitor/", params={"monitor_id": 5})
print(resp.json())
```

---

## 🔍 Busca e Filtros

A API suporta busca e filtros em endpoints de listagem:

### **Busca por texto**
```bash
# Buscar cursos por nome
curl "https://plataformacasa-a2a3d2abfd5e.herokuapp.com/api/cursos/?search=engenharia"

# Buscar alunos por nome ou email
curl "https://plataformacasa-a2a3d2abfd5e.herokuapp.com/api/alunos/?search=joao"
```

### **Ordenação**
```bash
# Ordenar cursos por nome
curl "https://plataformacasa-a2a3d2abfd5e.herokuapp.com/api/cursos/?ordering=nome"

# Ordenar em ordem decrescente
curl "https://plataformacasa-a2a3d2abfd5e.herokuapp.com/api/cursos/?ordering=-nome"
```

### **Paginação**
```bash
# Primeira página (20 itens por padrão)
curl "https://plataformacasa-a2a3d2abfd5e.herokuapp.com/api/cursos/?page=1"

# Segunda página
curl "https://plataformacasa-a2a3d2abfd5e.herokuapp.com/api/cursos/?page=2"
```

---

## 📝 Formatos de Dados

### **Status de Inscrição**
- `Pendente` - Aguardando avaliação
- `Entrevista` - Convocado para entrevista
- `Aprovado` - Aprovado como monitor
- `Não Aprovado` - Não aprovado

### **Status de Registro de Horas**
- `Pendente` - Aguardando validação
- `Aprovado` - Validado pelo professor
- `Rejeitado` - Rejeitado pelo professor

### **Tipo de Vaga**
- `TEA` - Monitoria remunerada (R$ 1.500,00)
- `Voluntaria` - Monitoria voluntária

### **Formato de Data**
- `YYYY-MM-DD` (ex: `2025-10-31`)

### **Formato de Hora**
- `HH:MM:SS` (ex: `14:30:00`)

---

## ⚠️ Notas Importantes

1. **Todos os endpoints estão abertos** - Não requer autenticação atualmente
2. **CORS habilitado** - Pode ser acessado de qualquer origem
3. **Arquivos estáticos** - Servidos via WhiteNoise
4. **Banco de dados** - PostgreSQL no Heroku
5. **Limite de requisições** - Sem limite definido atualmente

---

## 🛠️ Desenvolvimento

### **Executar localmente**

```bash
# Clone o repositório
git clone https://github.com/Projetos-de-Extensao/PBE_25.2_8001_IV.git
cd PBE_25.2_8001_IV

# Instale as dependências
pip install -r requirements.txt

# Configure o banco de dados local
cd meuprojeto
python manage.py migrate

# Execute o servidor
python manage.py runserver
```

### **Acessar localmente**

- Base URL: `http://localhost:8000`
- Swagger: `http://localhost:8000/restapi/`
- ReDoc: `http://localhost:8000/redoc/`
- Admin: `http://localhost:8000/admin/`

---

## 📞 Suporte

- **GitHub Issues:** [https://github.com/Projetos-de-Extensao/PBE_25.2_8001_IV/issues](https://github.com/Projetos-de-Extensao/PBE_25.2_8001_IV/issues)
- **Email:** suporte@plataformacasa.com.br

---

## 📜 Licença

MIT License - Livre para uso acadêmico e comercial.

---

**Última atualização:** 31 de outubro de 2025
**Versão da API:** v1.0
**Status:** ✅ Produção
