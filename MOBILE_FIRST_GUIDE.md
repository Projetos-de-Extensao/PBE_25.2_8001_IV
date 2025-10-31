# 📱 Guia Mobile-First - Plataforma Casa

## Visão Geral

Este documento descreve a implementação de um **design Mobile-First** completo para a Plataforma Casa. A abordagem prioriza a experiência do usuário em dispositivos móveis como requisito primário.

---

## 🎯 Princípios Mobile-First

### 1. **Hierarquia de Breakpoints**

| Dispositivo | Largura | Classe | Uso |
|---|---|---|---|
| **Móvel** | < 576px | `.d-only-mobile` | Padrão (otimizado) |
| **Tablet** | 576px - 768px | `.d-none-mobile` | Tablets pequenos |
| **Desktop** | 768px - 1200px | `@media (min-width: 768px)` | Laptops |
| **Grande** | > 1200px | `@media (min-width: 1200px)` | Monitores grandes |

### 2. **Estratégia CSS**

```css
/* ✅ CORRETO - Mobile First */
.card {
    width: 100%;
    margin-bottom: 1rem;
}

@media (min-width: 768px) {
    .card {
        width: 48%;
        margin-bottom: 1.5rem;
    }
}

/* ❌ ERRADO - Desktop First */
.card {
    width: 48%;
}

@media (max-width: 768px) {
    .card {
        width: 100%;
    }
}
```

---

## 📐 Componentes Otimizados

### Navbar

**Mobile (< 576px):**
- Hamburger menu colapsável
- Altura compacta: 50px
- Sticky positioning
- Font size reduzido

**Tablet+ (≥ 576px):**
- Altura normal: 56px
- Menu expandido

**Desktop+ (≥ 768px):**
- Altura: 60px
- Logo maior
- Espaçamento melhorado

```html
<!-- Navbar responsiva -->
<nav class="navbar navbar-expand-lg">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">Casa</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse">
            <i class="fas fa-bars"></i>
        </button>
        <div class="collapse navbar-collapse">
            <!-- Menu items -->
        </div>
    </div>
</nav>
```

### Sidebar

**Mobile:**
- Oculta por padrão
- Apresentada como overlay fullscreen
- Desliza do topo ou lado

**Desktop+ (≥ 768px):**
- Sempre visível
- Layout de 2 colunas com sidebar fixa
- Largura: 250-280px

### Cards KPI

```html
<div class="kpi-card">
    <div class="kpi-label">Monitores Ativos</div>
    <div class="kpi-value">6</div>
</div>
```

**Responsividade:**
- Mobile: 100% width, text-align center
- Desktop: Side-by-side, 2-4 colunas

### Buttons

**Touch-Friendly:**
```css
.btn {
    min-height: 44px;      /* Tamanho recomendado para touch */
    min-width: 44px;
    padding: 0.75rem 1rem; /* Espaçamento confortável */
}
```

**Mobile Stack:**
```html
<!-- Botões empilhados em mobile -->
<div class="btn-group">
    <button class="btn btn-primary btn-block">Exportar</button>
    <button class="btn btn-secondary btn-block">Voltar</button>
</div>
```

---

## 📋 Tabelas Responsivas

### Mobile Strategy

**Ocultar colunas menos importantes:**
```html
<th class="d-none d-md-table-cell">Coluna Desktop</th>
```

**Scroll horizontal:**
```html
<div class="table-responsive">
    <table class="table">
        <!-- Conteúdo -->
    </table>
</div>
```

---

## 📝 Formulários

### Tamanhos Touch-Friendly

```css
.form-control {
    min-height: 44px;
    font-size: 1rem;  /* Evita zoom no iOS */
}
```

### Layout Mobile

```html
<!-- Todos os inputs 100% width em mobile -->
<div class="form-group">
    <label>Campo</label>
    <input class="form-control" type="text">
</div>
```

---

## 🎨 Utilitários CSS

### Ocultar/Mostrar por Tamanho

```html
<!-- Oculto apenas em mobile -->
<div class="d-none-mobile">
    Conteúdo desktop
</div>

<!-- Visível apenas em mobile -->
<div class="d-only-mobile">
    Conteúdo mobile
</div>

<!-- Bootstrap built-in -->
<div class="d-none d-md-block">Desktop</div>
<div class="d-md-none">Mobile</div>
```

### Safe Area Padding (iPhone Notch)

```css
@supports (padding: max(0px)) {
    body {
        padding-left: max(12px, env(safe-area-inset-left));
        padding-right: max(12px, env(safe-area-inset-right));
    }
}
```

---

## 🔍 Viewport Meta Tag

**Já configurado em `base.html`:**

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

**Adições recomendadas:**
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
```

---

## 🚀 Performance Mobile

### 1. **CSS Minificado**

Arquivos CSS são carregados em ordem:
```
1. bootstrap@5.3.0 (CDN)
2. font-awesome@6.4.0 (CDN)
3. cores-institucionais.css (variáveis)
4. cores-padrao.css (sobrescrita)
5. mobile-first.css (responsive)
```

### 2. **Lazy Loading de Imagens**

```html
<img src="imagem.jpg" loading="lazy" alt="Descrição">
```

### 3. **Print Styles**

```css
@media print {
    .navbar, .sidebar { display: none; }
}
```

---

## 📱 Teste em Dispositivos Reais

### DevTools Chrome
1. F12 → Toggle Device Toolbar (Ctrl+Shift+M)
2. Selecionar dispositivos: iPhone, iPad, Android
3. Testar orientação (portrait/landscape)

### Breakpoints para Testar
- **375px** - iPhone SE
- **390px** - iPhone 14 Pro
- **428px** - iPhone 14 Max
- **540px** - Tablet pequeno
- **768px** - iPad
- **1024px** - iPad Pro
- **1920px** - Desktop

---

## ✅ Checklist Mobile-First

- [ ] Viewport meta tag configurada
- [ ] Navbar responsiva funciona
- [ ] Sidebar se expande em desktop
- [ ] Botões têm min-height: 44px
- [ ] Inputs têm min-height: 44px
- [ ] Tabelas são scrolláveis em mobile
- [ ] Imagens responsivas
- [ ] Touch targets adequados (44x44px mínimo)
- [ ] Sem scroll horizontal em mobile
- [ ] Cores contrast accessibility (WCAG)
- [ ] Testar em orientações (portrait/landscape)
- [ ] Testar em conexão lenta (3G)

---

## 🔗 Recursos Úteis

- [MDN: Mobile Optimization](https://developer.mozilla.org/pt-BR/docs/Web/Performance/Mobile_optimization)
- [Bootstrap Responsive Design](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- [Google Mobile-Friendly Test](https://search.google.com/test/mobile-friendly)
- [WebAIM: Accessible Design](https://webaim.org/)

---

## 📞 Suporte

Para dúvidas ou melhorias, consulte:
- Documentação Bootstrap: `/docs`
- CSS Customizado: `/static/css/`
- Templates: `/templates/`

---

**Última atualização:** 31 de outubro de 2025  
**Versão:** 1.0
