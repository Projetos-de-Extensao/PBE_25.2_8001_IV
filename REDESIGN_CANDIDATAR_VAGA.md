# 🎨 Redesign - Página Candidatar-se à Vaga

## 📋 **O Que Foi Feito**

Aplicado o **design minimalista e profissional** na página de **"Candidatar-se à Vaga"**, seguindo o padrão visual do sistema.

---

## ✨ **Melhorias Implementadas**

### 🎨 **1. Header Redesenhado**
- ✅ Background: **verde** `#28a745` (cor de sucesso)
- ✅ Título em **off-white** `#fafaf8`
- ✅ Borda esquerda em **amarelo accent** `#F5AC00`
- ✅ Ícone de user-plus integrado
- ✅ Destaque visual apropriado para ação de candidatura

### 📊 **2. Vaga Info Box (Destaque)**
- ✅ **Box especial com gradiente:**
  - Background: gradiente azul/verde claro
  - Borda: 2px azul primária `#1245FF`
  - Cantos arredondados (8px)
  
- ✅ **Informações organizadas:**
  - Nome da vaga em destaque (h4, 1.5rem)
  - Info rows com ícones coloridos
  - Layout flexível e alinhado
  - Ícones azul primário + labels bold

### 📝 **3. Seção de Informações**
- ✅ Section title com ícone e borda inferior
- ✅ Info blocks bem espaçados
- ✅ Labels em negrito azul escuro
- ✅ Textos com line-height confortável
- ✅ Hierarquia visual clara

### 📤 **4. Seção de Documentos**
- ✅ **Background cinza claro** `#f8f9fa`
- ✅ **Upload info box:**
  - Background azul claro
  - Borda esquerda azul primária (4px)
  - Ícone de informação

- ✅ **Form groups individuais:**
  - Box branco por documento
  - Borda 2px cinza
  - Padding generoso
  - **Hover effect:** borda azul + sombra sutil
  - **Feedback visual:** borda verde ao selecionar arquivo

### 🔲 **5. Labels dos Documentos**
- ✅ Ícones contextuais:
  - 🎓 Histórico Escolar
  - 📄 Currículo
  - ✉️ Carta de Motivação
- ✅ Asterisco vermelho para obrigatórios
- ✅ Form-text descritivo em cinza

### ✅ **6. Termo de Aceite**
- ✅ **Box destacado:**
  - Background verde claro `rgba(40, 167, 69, 0.08)`
  - Borda verde (2px)
  - Padding generoso

- ✅ **Checkbox customizado:**
  - Maior (1.25rem)
  - Borda verde
  - Check verde ao marcar
  - Cursor pointer

- ✅ Label clicável e legível

### 🎯 **7. Botões de Ação**
- ✅ **Enviar Candidatura:**
  - Background verde `#28a745`
  - Full-width
  - Hover: verde escuro com elevação
  - Sombra verde no hover
  - Ícone de paper-plane

- ✅ **Voltar ao Portal:**
  - Background off-white `#fafaf8`
  - Texto azul escuro
  - Hover: inverte (azul escuro + texto off-white)
  - Elevação e sombra no hover

### 📍 **8. Breadcrumb**
- ✅ Navegação clara: Home > Portal de Vagas > Candidatar-se
- ✅ Links azul primário com hover
- ✅ Item ativo em negrito

### 🔄 **9. JavaScript Aprimorado**
- ✅ **Validação melhorada:**
  - Lista arquivos faltantes no alert
  - Valida termo de aceite
  - Mensagens mais descritivas

- ✅ **Feedback visual:**
  - Borda verde ao selecionar arquivo
  - Background verde claro
  - Estado visual clear

---

## 🎨 **Paleta de Cores Utilizada**

```css
--color-primary-dark: #002555   /* Azul escuro institucional */
--color-primary-light: #1245FF  /* Azul claro institucional */
--color-accent: #F5AC00          /* Amarelo accent */
--color-off-white: #fafaf8       /* Off-white para textos */
--color-success: #28a745         /* Verde para ações positivas */
--color-gray-light: #f8f9fa      /* Cinza claro para backgrounds */
--color-gray-border: #e9ecef     /* Cinza para bordas */
--color-text-muted: #6c757d      /* Cinza para textos secundários */
```

---

## 📱 **Visual da Página**

```
╔════════════════════════════════════════════╗
║ 🟢 CANDIDATAR-SE À VAGA (verde)           ║
╠════════════════════════════════════════════╣
║ ┌────────────────────────────────────────┐ ║
║ │ 📘 teste anderson (Box Destacado)      │ ║
║ │ 🎓 Curso: Engenharia de Software       │ ║
║ │ 📚 Disciplina: Algoritmos              │ ║
║ │ 👥 Vagas: 3 de 5                       │ ║
║ └────────────────────────────────────────┘ ║
╠════════════════════════════════════════════╣
║ ℹ️ INFORMAÇÕES DA VAGA                    ║
║ Descrição: asdfasf                         ║
║ Requisitos: asfsaf                         ║
╠════════════════════════════════════════════╣
║ 📤 DOCUMENTOS OBRIGATÓRIOS                ║
║ ℹ️ Formatos: PDF, DOC, DOCX               ║
║                                            ║
║ ┌──────────────────────────────────────┐  ║
║ │ 🎓 Histórico Escolar *               │  ║
║ │ [Escolher arquivo]                   │  ║
║ │ Envie seu histórico escolar...       │  ║
║ └──────────────────────────────────────┘  ║
║                                            ║
║ ┌──────────────────────────────────────┐  ║
║ │ 📄 Currículo *                       │  ║
║ │ [Escolher arquivo]                   │  ║
║ │ Envie seu currículo...               │  ║
║ └──────────────────────────────────────┘  ║
║                                            ║
║ ┌──────────────────────────────────────┐  ║
║ │ ✉️ Carta de Motivação *              │  ║
║ │ [Escolher arquivo]                   │  ║
║ │ Explique sua motivação...            │  ║
║ └──────────────────────────────────────┘  ║
╠════════════════════════════════════════════╣
║ ┌────────────────────────────────────────┐ ║
║ │ ☑️ Declaro que li e estou de acordo   │ ║
║ │    com os requisitos... *             │ ║
║ └────────────────────────────────────────┘ ║
╠════════════════════════════════════════════╣
║ [🟢 ✈️ Enviar Candidatura          ]      ║
║ [⚪ ⬅️ Voltar ao Portal             ]      ║
╚════════════════════════════════════════════╝
```

---

## 🔍 **Detalhes de Design**

### ✅ **Vaga Info Box (Especial)**
```css
background: linear-gradient(135deg, 
    rgba(18, 69, 255, 0.08) 0%, 
    rgba(40, 167, 69, 0.08) 100%);
border: 2px solid #1245FF;
padding: 1.5rem;
border-radius: 8px;
```

- Gradiente sutil azul→verde
- Borda azul primária destacada
- Info rows com ícones alinhados
- Hierarquia visual clara

### ✅ **Form Group Upload**
```css
background: white;
padding: 1.25rem;
border: 2px solid #e9ecef;
border-radius: 8px;
transition: all 0.3s ease;
```

**Hover:**
```css
border-color: #1245FF;
box-shadow: 0 2px 8px rgba(18, 69, 255, 0.1);
```

**Com arquivo selecionado (JavaScript):**
```css
border-color: #28a745;
background-color: rgba(40, 167, 69, 0.05);
```

### ✅ **Termo de Aceite**
```css
background: rgba(40, 167, 69, 0.08);
border: 2px solid #28a745;
padding: 1.25rem;
border-radius: 8px;
```

- Background verde claro
- Borda verde
- Checkbox grande e clicável
- Label user-friendly

---

## 🎯 **Interatividade JavaScript**

### **1. Validação Aprimorada**
```javascript
// Lista arquivos faltantes
let missingFiles = [];
fileInputs.forEach(input => {
    if (!input.files.length) {
        const label = input.previousElementSibling.textContent.trim();
        missingFiles.push(label);
    }
});

// Alert descritivo
alert('Envie os documentos:\n\n' + missingFiles.join('\n'));
```

### **2. Feedback Visual**
```javascript
input.addEventListener('change', function() {
    const parent = this.closest('.form-group-upload');
    if (this.files.length > 0) {
        parent.style.borderColor = '#28a745';
        parent.style.backgroundColor = 'rgba(40, 167, 69, 0.05)';
    }
});
```

- Borda verde ao selecionar
- Background verde claro
- Feedback imediato ao usuário

### **3. Validação do Termo**
```javascript
const termo = document.getElementById('termo');
if (!termo.checked) {
    alert('Aceite os termos e responsabilidades!');
}
```

---

## 📊 **Estrutura Visual**

### **Hierarquia:**
1. 🥇 Header verde (máximo destaque)
2. 🥈 Vaga Info Box (box especial)
3. 🥉 Seções de conteúdo
4. 📤 Área de documentos (destaque secundário)
5. ✅ Termo de aceite (atenção)
6. 🎯 Botões de ação (call-to-action)

### **Espaçamentos:**
- Padding header: 2rem
- Padding card body: 1.5rem (p-4)
- Margin entre seções: 1.5rem - 2rem
- Gap entre botões: 0.75rem

### **Bordas:**
- Info box: 2px sólida azul
- Form groups: 2px sólida cinza
- Termo: 2px sólida verde
- Border-radius: 6px - 8px

---

## ✅ **Checklist de Implementação**

- ✅ Header verde com off-white
- ✅ Vaga info box destacado
- ✅ Section titles consistentes
- ✅ Form groups individuais
- ✅ Hover effects nos uploads
- ✅ Feedback visual ao selecionar arquivo
- ✅ Termo de aceite destacado
- ✅ Botões full-width com hover
- ✅ Breadcrumb funcional
- ✅ JavaScript aprimorado
- ✅ Validações completas
- ✅ Responsivo

---

## 🚀 **Como Testar**

1. **Acesse:** `http://127.0.0.1:8000/vagas/14/candidatar/`
2. **Observe:**
   - Header verde com título off-white
   - Box de informações da vaga destacado
   - Form groups com hover effect
   - Selecione arquivo → borda verde
   - Termo de aceite verde claro
   - Botões com hover effects

---

## 📝 **Commit Realizado**

```bash
git commit -m "Design: aplicado layout minimalista na página Candidatar-se à Vaga"
```

---

## 🎯 **Resultado Final**

✅ **Design limpo e profissional**
✅ **Cores institucionais aplicadas**
✅ **Vaga info destacada apropriadamente**
✅ **Uploads organizados e intuitivos**
✅ **Feedback visual claro**
✅ **Validações robustas**
✅ **Totalmente responsivo**
✅ **Consistente com o sistema**

---

**A página agora está alinhada perfeitamente com o design minimalista do sistema!** 🎉
