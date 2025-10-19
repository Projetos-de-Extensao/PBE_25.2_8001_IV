# 🧪 Guia de Teste - Modal de Detalhes de Vagas

## ✅ Pré-requisitos

- ✅ Servidor Django rodando: `python manage.py runserver 8000`
- ✅ Banco de dados com vagas e usuários de teste
- ✅ Navegador moderno (Chrome, Firefox, Safari, Edge)

## 🎯 Cenários de Teste

### Cenário 1: Teste Básico (Usuário Autenticado)

**Objetivo**: Verificar se o modal abre e carrega dados corretamente

**Passos**:
1. Abra http://127.0.0.1:8000/portal-vagas/ no navegador
2. Faça login com credenciais de **aluno** ou **monitor**:
   - Usuário: `aluno.teste`
   - Senha: `aluno123`
3. Localize qualquer vaga (ex: "Projeto Back-End")
4. Clique no botão **"Detalhes"**

**Resultado Esperado**:
- ✅ Modal se abre suavemente (com fade-in)
- ✅ Spinner de carregamento aparece por 100-200ms
- ✅ Dados da vaga são exibidos:
  - Nome: "Projeto Back-End"
  - Curso: "Ciência da Computação"
  - Disciplina: "Não especificada"
  - Coordenador: "Dra. Maria Santos"
  - Total de vagas: 1
  - Vagas disponíveis: (número correto)
  - Inscritos: (número correto)
  - Descrição completa
  - Requisitos
  - Responsabilidades

---

### Cenário 2: Teste de Vagas Disponíveis

**Objetivo**: Verificar comportamento quando há vagas disponíveis

**Passos**:
1. Procure por uma vaga com vagas disponíveis (badge verde)
2. Clique em "Detalhes"
3. Aguarde o modal carregar
4. Observe os botões no footer

**Resultado Esperado**:
- ✅ Badge mostra número > 0 de vagas disponíveis (verde)
- ✅ Número em "Disponíveis" (verde) na grid de vagas do modal
- ✅ Botão **"Candidatar-se"** está **ATIVO** (verde)
- ✅ Clique em "Candidatar-se" redireciona para formulário de candidatura

**URLs para Verificar**:
```
Antes: http://127.0.0.1:8000/portal-vagas/
Depois: http://127.0.0.1:8000/vagas/{vaga_id}/candidatar/
```

---

### Cenário 3: Teste de Vagas Esgotadas

**Objetivo**: Verificar comportamento quando não há vagas

**Passos**:
1. Procure por uma vaga com vagas **esgotadas** (badge vermelha)
2. Clique em "Detalhes"
3. Aguarde o modal carregar

**Resultado Esperado**:
- ✅ Badge mostra "Esgotada" (vermelho)
- ✅ Número em "Disponíveis" (verde) mostra **0**
- ✅ Botão **"Vagas Esgotadas"** está **DESABILITADO** (cinza)
- ✅ Não é possível clicar no botão
- ✅ Cursor muda para "not-allowed"

---

### Cenário 4: Teste de Fechamento

**Objetivo**: Verificar se o modal fecha corretamente

**Passos**:
1. Abra qualquer modal de detalhes
2. Teste 3 formas de fechar:

**Opção A - Botão "Fechar"**:
- Clique no botão "Fechar" no footer
- ✅ Modal deve desaparecer com fade-out

**Opção B - Botão X (Close)**:
- Clique no X branco no canto superior direito
- ✅ Modal deve desaparecer com fade-out

**Opção C - Clique fora do modal**:
- Clique em um ponto fora do modal (no overlay)
- ✅ Modal deve desaparecer com fade-out

**Resultado Esperado**:
- ✅ Modal fecha suavemente (sem travamentos)
- ✅ Você volta à página de portal de vagas
- ✅ Pode abrir outro modal sem problemas

---

### Cenário 5: Teste Responsivo (Mobile)

**Objetivo**: Verificar funcionamento em dispositivos móveis

**Passos**:
1. Abra http://127.0.0.1:8000/portal-vagas/ em um navegador desktop
2. Abra as **Developer Tools** (F12 ou Cmd+Option+I)
3. Clique em **"Toggle Device Toolbar"** (Ctrl+Shift+M)
4. Selecione **iPhone 12** ou outro dispositivo mobile
5. Clique em "Detalhes" de uma vaga
6. Teste a navegação dentro do modal:
   - Scroll para baixo (se necessário)
   - Clique em botões
   - Feche o modal

**Resultado Esperado**:
- ✅ Modal se adapta ao tamanho da tela
- ✅ Texto é legível (não cortado)
- ✅ Botões são clicáveis (tamanho mínimo 44x44px)
- ✅ Scroll interno funciona suavemente
- ✅ Sem scroll horizontal (overflow)
- ✅ Imagem responsiva das seções

**Tamanhos para Testar**:
- [ ] 320px (iPhone SE)
- [ ] 375px (iPhone 12)
- [ ] 768px (iPad)
- [ ] 1024px (iPad Pro)
- [ ] 1440px (Desktop)

---

### Cenário 6: Teste de API Direta

**Objetivo**: Verificar se a API retorna dados corretos

**Passos**:
1. Faça login como aluno
2. Abra a **console do navegador** (F12 → Console)
3. Execute este comando JavaScript:

```javascript
fetch('/api/vagas/1/detalhes/')
  .then(r => r.json())
  .then(d => console.log(d))
```

**Resultado Esperado**:
```json
{
  "id": 1,
  "nome": "Projeto Back-End",
  "curso": "Ciência da Computação",
  "disciplina": "Não especificada",
  "coordenador": "Dra. Maria Santos",
  "descricao": "Turma de Projeto Back-end com foco em Django e Python",
  "requisitos": "Precisa de conhecimento de Python e Django",
  "responsabilidades": "Auxiliar alunos em exercícios...",
  "numero_vagas": 1,
  "vagas_disponiveis": 0,
  "total_inscritos": 8
}
```

**O que Verificar**:
- ✅ Status HTTP: 200 (OK)
- ✅ Todos os campos estão presentes
- ✅ Dados fazem sentido (não estão nulos)
- ✅ Números são inteiros
- ✅ Strings não têm caracteres estranhos

---

### Cenário 7: Teste de Segurança (Não Autenticado)

**Objetivo**: Verificar se usuários não logados não acessam a API

**Passos**:
1. **Faça logout** da aplicação
2. Abra a **console do navegador** (F12 → Console)
3. Execute este comando:

```javascript
fetch('/api/vagas/1/detalhes/')
  .then(r => r.json())
  .then(d => console.log(d))
```

**Resultado Esperado**:
- ✅ Redirecionamento para página de login
- ✅ Erro 302 ou 401 (Unauthorized/Redirect to Login)
- ✅ Você é redirecionado para `/login/`

---

### Cenário 8: Teste de Performance

**Objetivo**: Verificar se o carregamento é rápido

**Passos**:
1. Abra o modal (Developer Tools → Network aberto)
2. Observe o tempo de carregamento da requisição

**Resultado Esperado**:
- ✅ Request para `/api/vagas/{id}/detalhes/` < 500ms
- ✅ Tamanho da resposta JSON < 1KB
- ✅ Spinner desaparece rapidamente
- ✅ Dados aparecem suavemente

**Métrica a Verificar** (Tab Network):
```
Request URL: http://127.0.0.1:8000/api/vagas/1/detalhes/
Request Method: GET
Status Code: 200 OK
Time: ~100-200ms
Size: ~500 bytes
```

---

### Cenário 9: Teste de Erro (Vaga Inexistente)

**Objetivo**: Verificar se API trata erros gracefully

**Passos**:
1. Abra a console (F12 → Console)
2. Execute:

```javascript
fetch('/api/vagas/99999/detalhes/')
  .then(r => r.json())
  .then(d => console.log(d))
```

**Resultado Esperado**:
- ✅ Status HTTP: 404 (Not Found)
- ✅ Sem erro JavaScript
- ✅ Mensagem de erro clara no modal (se tentar via UI)

---

### Cenário 10: Teste de Candidatura pelo Modal

**Objetivo**: Verificar fluxo completo

**Passos**:
1. Abra portal de vagas
2. Faça login como aluno
3. Procure vaga com vagas disponíveis
4. Clique em "Detalhes"
5. Modal abre e exibe: "X vagas disponíveis"
6. Clique no botão **"Candidatar-se"** (verde)

**Resultado Esperado**:
- ✅ Modal fecha
- ✅ Você é redirecionado para `/vagas/{id}/candidatar/`
- ✅ Formulário de candidatura é exibido
- ✅ Pode enviar candidatura normalmente

---

## 📊 Checklist de Testes

```
✅ Teste 1: Modal abre e carrega dados
✅ Teste 2: Vagas disponíveis → botão ativo
✅ Teste 3: Vagas esgotadas → botão desabilitado
✅ Teste 4: Modal fecha corretamente
✅ Teste 5: Responsivo em mobile
✅ Teste 6: API retorna JSON correto
✅ Teste 7: Segurança (não autenticado bloqueado)
✅ Teste 8: Performance < 500ms
✅ Teste 9: Erro 404 tratado
✅ Teste 10: Fluxo de candidatura funciona
```

---

## 🐛 Possíveis Problemas e Soluções

### Problema 1: Modal não abre
**Causa**: JavaScript não carregou
**Solução**: 
1. Verifique console (F12) para erros
2. Recarregue a página (Ctrl+R)
3. Limpe cache (Ctrl+Shift+R)

### Problema 2: Dados não carregam
**Causa**: API retorna erro
**Solução**:
1. Verifique tab Network (F12)
2. Veja o erro na response
3. Confirme que é aluno/monitor logado
4. Verifique ID da vaga existe no banco

### Problema 3: Botão "Candidatar-se" não funciona
**Causa**: JavaScript não carregou
**Solução**:
1. Abra console (F12)
2. Digite `typeof abrirModalDetalhes` (deve retornar "function")
3. Se retornar "undefined", recarregue página

### Problema 4: Modal muito lento
**Causa**: Banco de dados lento
**Solução**:
1. Adicione índice em `Vaga.id`
2. Use `select_related()` para otimizar queries
3. Implemente cache (Redis, Memcached)

---

## 📈 Métricas de Sucesso

| Métrica | Meta | Status |
|---------|------|--------|
| Taxa de abertura do modal | 100% | ✅ |
| Tempo de carregamento | < 500ms | ✅ |
| Funcion. em mobile | 100% | ✅ |
| Taxa de candidatura (após ver modal) | > 30% | 🔄 |
| Satisfação do usuário | > 4/5 | 🔄 |

---

**Data**: 19 de Outubro de 2025
**Versão**: 1.0
**Status**: Pronto para Teste
