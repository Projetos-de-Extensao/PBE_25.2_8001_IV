# 📋 Modal de Atualização de Status - Documentação

## ✅ Implementação Concluída

Um modal interativo foi criado no arquivo `detalhe.html` para permitir que coordenadores e administradores atualizem o status dos candidatos às vagas de monitoria.

---

## 🎯 Funcionalidades

### 1. **Badge de Status Clicável**
- ✨ O badge de status de cada candidato é agora um botão clicável
- 🎨 Mantém os estilos de cor por status (Pendente, Entrevista, Aprovado, Não Aprovado)
- 🖱️ Efeito hover com elevação e sombra
- 📱 Responsivo em mobile

### 2. **Modal Interativo**
O modal possui a mesma estrutura e styling do `portal_logged.html`:

#### **Header**
- Ícone de edição
- Título: "Atualizar Status do Candidato"
- Botão de fechar (X)

#### **Body**
- **Informações do Candidato**: Nome e status atual
- **Seleção de Status**: 4 opções com radio buttons
  - 🟡 **Pendente**: Aguardando avaliação
  - 🔵 **Entrevista**: Agendado para entrevista
  - 🟢 **Aprovado**: Candidato selecionado
  - 🔴 **Não Aprovado**: Candidato rejeitado
- **Feedback Visual**: Opções selecionáveis com estilo destacado
- **Mensagem de Status**: Feedback de sucesso ou erro

#### **Footer**
- Botão "Cancelar" (cinza)
- Botão "Atualizar Status" (azul) com ícone de loading

---

## 🎨 Estilos CSS Adicionados

```css
/* Modal Container */
.modal-content {
    border-radius: 14px;
    border: none;
    overflow: hidden;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

/* Posicionamento do Modal */
#modalAtualizarStatus.modal.show {
    padding-top: 1rem !important;
}

#modalAtualizarStatus .modal-dialog {
    margin-top: 1rem !important;
    max-height: calc(100vh - 2rem);
}

/* Opções de Status */
.status-option {
    display: flex;
    align-items: center;
    padding: 0.875rem;
    border: 2px solid #e9ecef;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.status-option.selected {
    border-color: #002555;
    background: rgba(0, 37, 85, 0.05);
}

/* Botões */
.btn-atualizar {
    background: #002555;
    color: white;
    /* ... estilos adicionais ... */
}

.btn-atualizar.loading {
    pointer-events: none;
    opacity: 0.7;
}

.btn-atualizar.loading i {
    animation: spin 1s linear infinite;
}
```

---

## 🔧 Funcionalidade JavaScript

### **Abertura do Modal**
```javascript
// Evento disparado quando o modal é aberto
document.getElementById('modalAtualizarStatus').addEventListener('show.bs.modal', function(event) {
    // Busca dados do botão clicado
    const inscricaoId = button.getAttribute('data-inscricao-id');
    const alunoNome = button.getAttribute('data-aluno-nome');
    const statusAtual = button.getAttribute('data-status-atual');
    
    // Popula o modal com informações
    // Marca o status atual como selecionado
    
    // 🎯 SCROLL AUTOMÁTICO: Leva o modal para visão do usuário
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});
```

### **Seleção de Status**
- Radio buttons com event listeners
- Classe `.selected` adicionada visualmente
- Validação se novo status é diferente do atual

### **Atualizar Status (AJAX)**
```javascript
async function atualizarStatusCandidato() {
    // Validações
    // Requisição POST para: /inscricoes/{id}/atualizar-status/
    // Atualiza badge de status na página
    // Recarrega a página para atualizar estatísticas
}
```

---

## 📡 API Endpoint Utilizado

**Endpoint Existente**: `/inscricoes/<inscricao_id>/atualizar-status/`

### Request (POST)
```json
{
    "status": "Aprovado"  // ou "Pendente", "Entrevista", "Não Aprovado"
}
```

### Response
```json
{
    "success": true,
    "message": "Status atualizado de 'Pendente' para 'Aprovado'",
    "novo_status": "Aprovado"
}
```

---

## 🔐 Segurança

✅ **Verificações de Permissão** (no backend):
- Apenas admin ou coordenador da vaga pode atualizar
- CSRF token obrigatório

✅ **Validações no Frontend**:
- Verifica se novo status é diferente do atual
- Validação de seleção obrigatória

---

## 📱 Responsividade

| Dispositivo | Comportamento |
|---|---|
| **Desktop** | 2 colunas de opções, padding normal |
| **Tablet** | 1-2 colunas, padding reduzido |
| **Mobile** | 1 coluna, botões 100% de largura, modal otimizado |

---

## 🚀 Como Usar

### **Para Usuários Finais**:
1. Acesse a página de detalhes de uma vaga (`/vagas/<id>/`)
2. Clique no badge de status de um candidato
3. Selecione o novo status desejado
4. Clique em "Atualizar Status"
5. Aguarde a confirmação e a página será recarregada

### **Para Desenvolvedores**:
- Modal está em `templates/vagas/detalhe.html`
- Scripts também no mesmo arquivo
- Endpoint em `views.py` → `atualizar_status_inscricao()`

---

## 📝 Alterações no Arquivo

### **detalhe.html**

1. **CSS Adicional** (linhas ~640-730):
   - Estilos do modal e suas variações
   - Animações e transições
   - Responsividade

2. **HTML - Badge Clicável** (linhas ~945-955):
   ```html
   <button type="button" 
       class="candidato-status ..."
       data-bs-toggle="modal" 
       data-bs-target="#modalAtualizarStatus"
       data-inscricao-id="{{ inscricao.id }}"
       data-aluno-nome="{{ inscricao.aluno.nome }}"
       data-status-atual="{{ inscricao.status }}"
   >
   ```

3. **Modal HTML** (linhas ~1000-1090):
   - Estrutura completa do modal
   - Opções de status
   - Área de mensagens

4. **JavaScript** (linhas ~1093-1250):
   - Event listeners
   - Função de atualização
   - Tratamento de erros

---

## ✨ Melhorias Futuras

- [ ] Adicionar campo de comentário ao atualizar status
- [ ] Histórico de mudanças de status
- [ ] Notificações por email ao candidato
- [ ] Logs de quem atualizou o status
- [ ] Filtros por status na lista de candidatos

---

## 🐛 Troubleshooting

### Modal não abre?
- Verifique se Bootstrap 5+ está carregado
- Verifique o console do navegador para erros

### Status não atualiza?
- Verifique permissões do usuário
- Verifique se o token CSRF está correto
- Verifique o endpoint `/inscricoes/<id>/atualizar-status/`

### Estilos não aparecem?
- Limpe o cache do navegador
- Verifique se o CSS foi carregado corretamente

---

## 📞 Suporte

Para dúvidas ou bugs, abra uma issue no repositório com tag `[modal-status]`.

**Desenvolvedor**: Implementação em 07/11/2025
