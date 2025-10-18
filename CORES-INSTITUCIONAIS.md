# 🎨 Paleta de Cores Institucionais - Plataforma Casa

## Visão Geral

A Plataforma Casa utiliza uma paleta de cores institucionais oficial, padronizada e consistente em toda a aplicação. Essas cores foram selecionadas para garantir identidade visual forte e boa experiência de usuário.

---

## 📋 Cores Oficiais

### Cores Primárias

#### 🟨 Amarelo Institucional
```
Hexadecimal: #F5AC00
Pantone: 1235 C
RGB: 245, 172, 0
Uso: Destaque, acentos, botões importantes, borders de foco
```

#### 🔵 Azul Escuro Principal
```
Hexadecimal: #002555
Pantone: 655 C
RGB: 0, 37, 85
Uso: Navbar, sidebar, headers, textos principais, links
```

---

### Cores Auxiliares

#### 🔷 Azul Auxiliar
```
Hexadecimal: #1245FF
Pantone: 2387 C
RGB: 18, 69, 255
Uso: Gradientes, links secundários, efeitos hover
```

---

### Cores de Apoio (Escala de Cinzas)

#### 🟤 Cinza Escuro
```
Hexadecimal: #6d6e71
Uso: Texto principal, labels, descrições
```

#### ⚪ Cinza Médio
```
Hexadecimal: #a7a9ab
Uso: Texto secundário, placeholders, elementos desativados
```

#### 🩶 Cinza Claro
```
Hexadecimal: #d1d3d4
Uso: Bordas, divisores, backgrounds alternativos
```

#### ⚫ Branco
```
Hexadecimal: #ffffff
Uso: Fundo principal, texto sobre cores escuras
```

---

### Cores de Status (Complementares)

#### ✅ Sucesso
```
Hexadecimal: #27ae60
Uso: Mensagens de sucesso, badges positivas, confirmações
```

#### ❌ Erro
```
Hexadecimal: #e74c3c
Uso: Mensagens de erro, alertas críticos, validações
```

#### ⚠️ Aviso
```
Hexadecimal: #f39c12
Uso: Avisos, atenção, confirmações necessárias
```

#### ℹ️ Informação
```
Hexadecimal: #3498db
Uso: Informações, dicas, tooltips
```

---

## 🎯 Guia de Uso

### Navbar
- **Fundo**: Gradiente azul escuro (#002555) para azul auxiliar (#1245FF)
- **Border inferior**: Amarelo institucional (#F5AC00)
- **Texto**: Branco (#ffffff)
- **Hover**: Amarelo institucional com transição suave

### Sidebar
- **Fundo**: Azul escuro principal (#002555)
- **Border direito**: Amarelo institucional (#F5AC00)
- **Itens ativos**: Fundo amarelo, texto azul
- **Texto**: Branco (#ffffff)

### Cards
- **Border superior**: Azul escuro (#002555) - 4px
- **Header**: Gradiente azul escuro para auxiliar
- **Border header**: Amarelo institucional (#F5AC00)

### Botões
- **Primário**: Azul escuro (#002555)
- **Hover**: Azul auxiliar (#1245FF)
- **Ativo**: Amarelo institucional (#F5AC00)

### Tabelas
- **Header**: Gradiente azul (background)
- **Header border**: Amarelo institucional (#F5AC00)
- **Linhas alternadas**: Amarelo com 2% opacidade
- **Hover**: Azul com 5% opacidade

### Formulários
- **Label**: Cinza escuro (#6d6e71)
- **Border focus**: Azul escuro (#002555)
- **Placeholder**: Cinza médio (#a7a9ab)

### Mensagens
- **Alert Success**: Verde (#27ae60)
- **Alert Danger**: Vermelho (#e74c3c)
- **Alert Warning**: Laranja (#f39c12)
- **Alert Info**: Azul (#3498db)

---

## 🖌️ Implementação em CSS

### Variáveis CSS (em uso)

```css
:root {
    --cor-amarelo-institucional: #F5AC00;
    --cor-azul-escuro-principal: #002555;
    --cor-azul-auxiliar: #1245FF;
    --cor-cinza-escuro: #6d6e71;
    --cor-cinza-medio: #a7a9ab;
    --cor-cinza-claro: #d1d3d4;
    --cor-branco: #ffffff;
    --cor-preto: #000000;
    --cor-sucesso: #27ae60;
    --cor-erro: #e74c3c;
    --cor-aviso: #f39c12;
    --cor-info: #3498db;
}
```

### Utilizando as Variáveis

```html
<!-- Em HTML -->
<div class="bg-accent">Fundo amarelo institucional</div>
<div class="text-accent">Texto amarelo institucional</div>
<div class="bg-primary-dark">Fundo azul escuro</div>
<div class="text-primary-dark">Texto azul escuro</div>
<div class="border-accent">Border amarela</div>
```

---

## 📚 Classes Utilitárias Disponíveis

### Background
- `.bg-primary-dark` - Fundo azul escuro
- `.bg-primary-light` - Fundo azul claro (10% opacidade)
- `.bg-accent` - Fundo amarelo institucional
- `.bg-accent-dark` - Fundo azul escuro

### Texto
- `.text-primary-dark` - Texto azul escuro
- `.text-accent` - Texto amarelo institucional
- `.text-muted` - Texto cinza médio

### Borders
- `.border-accent` - Border amarela
- `.border-primary-dark` - Border azul escuro

### Dividers
- `.divider-accent` - Linha divisória amarela (3px)
- `.divider-primary` - Linha divisória azul (2px)

---

## 🎬 Gradientes Utilizados

### Gradiente Primário (Navbar e Headers)
```css
background: linear-gradient(135deg, #002555 0%, #1245FF 100%);
```

### Gradiente Inverso
```css
background: linear-gradient(135deg, #1245FF 0%, #002555 100%);
```

---

## ✨ Efeitos e Transições

### Sombras
- **Leve**: `rgba(0, 37, 85, 0.1)` - Efeito sutil
- **Média**: `rgba(0, 37, 85, 0.2)` - Elevação moderada
- **Forte**: `rgba(0, 37, 85, 0.3)` - Destaque forte

### Transições Padrão
```css
transition: all 0.3s ease;
```

### Hover Effects
- Cor muda para amarelo institucional
- Sombra aumenta
- Elemento sobe 2px (translateY)

---

## 🔄 Compatibilidade

### Navegadores Suportados
- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Mobile browsers

### Responsividade
As cores foram testadas e são consistentes em todos os tamanhos de tela:
- 📱 Mobile (320px+)
- 📱 Tablet (768px+)
- 🖥️ Desktop (1024px+)

---

## 📄 Arquivo CSS

O arquivo principal com todas as cores está em:
```
plataforma_Casa/templates/css/cores-institucionais.css
```

Ele é automaticamente carregado em todos os templates através de:
```html
<link rel="stylesheet" href="{% static 'css/cores-institucionais.css' %}">
```

---

## 🎓 Mudanças Recentes

### Versão 1.0 (18 de outubro de 2025)
- ✅ Implementação da paleta institucional
- ✅ Criação de arquivo CSS centralizado
- ✅ Definição de variáveis CSS
- ✅ Classe utilitárias adicionadas
- ✅ Atualização de todos os componentes
- ✅ Gradientes e efeitos visuais

---

## 📝 Notas de Design

### Princípios de Cor
1. **Hierarquia Visual**: Amarelo (#F5AC00) para elementos importantes
2. **Contraste**: Azul escuro (#002555) fornece bom contraste
3. **Acessibilidade**: Atendimento a WCAG AA para ratios de contraste
4. **Consistência**: Uso repetido de cores em toda a interface

### Recomendações
- Nunca use cores fora da paleta oficial
- Mantenha o contraste entre texto e fundo
- Use opacidade para variações (em vez de cores diferentes)
- Aplique transições suaves entre estados

---

## 📞 Suporte

Para dúvidas sobre uso de cores, consulte:
- Este arquivo: `CORES-INSTITUCIONAIS.md`
- Arquivo CSS: `cores-institucionais.css`
- Documentação MVT: `FRONTEND_MVT.md`

---

**Desenvolvido em**: 18 de outubro de 2025  
**Versão**: 1.0  
**Status**: ✅ Implementado

