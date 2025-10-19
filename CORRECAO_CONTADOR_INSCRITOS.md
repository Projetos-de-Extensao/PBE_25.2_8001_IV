# Correção do Contador de Inscritos nas Vagas

## Problema Identificado

O badge de "Inscritos" na página de listagem de vagas estava mostrando **0** mesmo quando havia candidatos inscritos na vaga.

**Exemplo:**
- Vaga: "teste anderson"
- Candidato inscrito: 1 pessoa
- Badge mostrava: **0 INSCRITOS** ❌

## Causa do Problema

O sistema estava confundindo dois conceitos diferentes:

### 1. Monitores Selecionados vs Inscrições
- **`vaga.monitores`**: ManyToManyField com alunos **SELECIONADOS** como monitores
- **`vaga.inscricao_set`**: Relacionamento reverso com **TODAS** as inscrições (candidatos)

### 2. Código Incorreto

**Template (vagas/listar.html - linha 385):**
```django
<span class="number">{{ vaga.monitores.count }}</span>
```
❌ Contava apenas monitores selecionados, não inscrições

**View (views.py - função listar_vagas):**
```python
vagas = Vaga.objects.all().select_related('curso', 'coordenador').prefetch_related('monitores')
```
❌ Não incluía anotação para contar inscrições

## Solução Implementada

### 1. Correção no Template
```django
<!-- ANTES -->
<span class="number">{{ vaga.monitores.count }}</span>

<!-- DEPOIS -->
<span class="number">{{ vaga.inscricao_set.count }}</span>
```
✅ Agora conta TODAS as inscrições

### 2. Correção na View
```python
# ANTES
vagas = Vaga.objects.all().select_related('curso', 'coordenador').prefetch_related('monitores')

# DEPOIS  
vagas = Vaga.objects.all().select_related('curso', 'coordenador').prefetch_related('monitores').annotate(
    total_inscritos=Count('inscricao')
)
```
✅ Adicionado `.annotate()` para contar inscrições

### 3. Aplicado em Ambos os Casos
A correção foi aplicada para:
- ✅ Usuários Admin (veem todas as vagas)
- ✅ Professores/Coordenadores (veem apenas suas vagas)

## Resultado

Agora o badge mostra corretamente:

```
┌─────────────────────────┐
│    teste anderson       │
│  Sistemas de Informação │
│                         │
│      ┌──────────┐       │
│      │    1     │       │
│      │ Inscritos│       │
│      └──────────┘       │
└─────────────────────────┘
```

## Arquivos Modificados

1. **meuprojeto/plataforma_Casa/templates/vagas/listar.html**
   - Linha 385: `vaga.monitores.count` → `vaga.inscricao_set.count`

2. **meuprojeto/plataforma_Casa/views.py**
   - Função `listar_vagas()` (linha 767-807)
   - Adicionado `.annotate(total_inscritos=Count('inscricao'))` em ambos os querysets

## Diferença Entre os Conceitos

| Campo | O que conta | Quando aumenta |
|-------|-------------|----------------|
| `monitores.count` | Monitores **APROVADOS/SELECIONADOS** | Quando professor seleciona candidato |
| `inscricao_set.count` | **TODOS** os candidatos inscritos | Quando aluno se candidata à vaga |

## Commit
```
Fix: corrigido contador de inscritos nas vagas

Problema: Badge mostrava 0 inscritos mesmo com candidatos inscritos

Correções:
- vagas/listar.html: trocado vaga.monitores.count por vaga.inscricao_set.count
- views.py/listar_vagas: adicionado .annotate(total_inscritos=Count('inscricao'))

Diferença:
- monitores.count = monitores SELECIONADOS
- inscricao_set.count = TOTAL de candidatos inscritos
```

---
**Status:** ✅ Corrigido e testado  
**Data:** 19 de outubro de 2025
