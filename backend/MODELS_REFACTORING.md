# Refatoração do Models.py - Sistema de Gestão de Monitorias

## 📋 Resumo das Melhorias

Esta refatoração transforma o `models.py` original em uma estrutura moderna, escalável e aderente às melhores práticas do Django.

---

## ✨ Principais Melhorias Implementadas

### 1. **Modelos Base Abstratos**

```python
class TimeStampedModel(models.Model):
    """Timestamps automáticos em todos os modelos"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class ActiveModel(models.Model):
    """Soft delete com métodos auxiliares"""
    ativo = models.BooleanField(default=True)
    
    def desativar(self):
        self.ativo = False
        self.save(update_fields=['ativo'])
```

**Benefícios:**
- DRY (Don't Repeat Yourself)
- Auditoria automática
- Soft delete padronizado

---

### 2. **Choices como Enums (IntegerChoices/TextChoices)**

**Antes:**
```python
dias_da_semana = models.CharField(max_length=100)  # "Segunda, Quarta, Sexta"
status = models.CharField(max_length=50, default='Pendente')
```

**Depois:**
```python
class DiaSemana(models.IntegerChoices):
    SEGUNDA = 0, 'Segunda-feira'
    TERCA = 1, 'Terça-feira'
    # ...

class StatusInscricao(models.TextChoices):
    PENDENTE = 'pendente', 'Pendente'
    APROVADO = 'aprovado', 'Aprovado'
    REJEITADO = 'rejeitado', 'Rejeitado'
```

**Benefícios:**
- Type safety
- Queries mais eficientes
- Autocomplete no IDE
- Menos erros de digitação
- Internacionalização facilitada

---

### 3. **Validators e Constraints**

```python
class AlunoProfile(BaseModel):
    cr_geral = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    periodo = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
```

**Constraints no banco:**
```python
class Meta:
    constraints = [
        models.CheckConstraint(
            check=models.Q(data_fim__gte=models.F('data_inicio')),
            name='turma_data_fim_valida'
        ),
    ]
```

**Benefícios:**
- Validação no nível do banco
- Integridade garantida
- Previne dados inválidos

---

### 4. **Índices para Performance**

```python
class Meta:
    indexes = [
        models.Index(fields=['matricula', 'ativo']),
        models.Index(fields=['curso', 'periodo']),
        models.Index(fields=['status', 'created_at']),
    ]
```

**Benefícios:**
- Queries mais rápidas
- Melhor performance em filtros comuns
- Preparado para escala

---

### 5. **Relacionamentos Melhorados**

**on_delete apropriados:**
```python
# PROTECT - não permite deletar se houver referências
curso = models.ForeignKey(Curso, on_delete=models.PROTECT)

# CASCADE - deleta em cascata
aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)

# SET_NULL - mantém histórico
aprovado_por = models.ForeignKey(
    Funcionario, 
    on_delete=models.SET_NULL, 
    null=True
)
```

**related_name consistentes:**
```python
# Plural para ForeignKey reverso
curso = models.ForeignKey(..., related_name='alunos')

# Descritivo para clareza
monitor = models.ForeignKey(..., related_name='turmas_monitoria')
```

---

### 6. **Métodos de Negócio nos Modelos**

```python
class Vaga(BaseModel):
    @property
    def vagas_preenchidas(self):
        return self.inscricoes.filter(status=StatusInscricao.APROVADO).count()
    
    @property
    def tem_vagas(self):
        return self.vagas_preenchidas < self.vagas_disponiveis

class Inscricao(TimeStampedModel):
    def aprovar(self, avaliador):
        self.status = StatusInscricao.APROVADO
        self.avaliado_por = avaliador
        self.data_avaliacao = timezone.now()
        self.save()
```

**Benefícios:**
- Lógica de negócio centralizada
- Código mais legível
- Fácil de testar

---

### 7. **Validações Customizadas**

```python
def clean(self):
    super().clean()
    if self.data_ingresso > timezone.now().date():
        raise ValidationError({
            'data_ingresso': 'Data de ingresso não pode ser futura.'
        })
```

**Benefícios:**
- Validações complexas
- Mensagens de erro claras
- Validação antes de salvar

---

### 8. **Horários Estruturados**

**Antes:**
```python
dias_da_semana = models.CharField(max_length=100)  # "Segunda, Quarta"
horario = models.CharField(max_length=50)  # "18:00 - 21:00"
```

**Depois:**
```python
class Turma(BaseModel):
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

class TurmaDiaSemana(models.Model):
    """M2M para múltiplos dias"""
    turma = models.ForeignKey(Turma, ...)
    dia = models.IntegerField(choices=DiaSemana.choices)
```

**Benefícios:**
- Queries por horário facilitadas
- Validação de conflitos
- Filtros e ordenações eficientes

---

### 9. **Internacionalização (i18n)**

```python
from django.utils.translation import gettext_lazy as _

nome = models.CharField(_('nome'), max_length=100)

class Meta:
    verbose_name = _('aluno')
    verbose_name_plural = _('alunos')
```

**Benefícios:**
- Preparado para múltiplos idiomas
- Admin em português
- Mensagens traduzíveis

---

### 10. **Documentação e Type Hints**

```python
class AlunoProfile(BaseModel):
    """Perfil de aluno vinculado ao User do Django"""
    
    @property
    def nome_completo(self) -> str:
        """Retorna nome completo do usuário associado"""
        return self.user.get_full_name() or self.user.username
```

---

## 📊 Comparação: Antes vs Depois

| Aspecto | Antes | Depois |
|---------|-------|--------|
| **Linhas de código** | ~180 | ~700 (com docs) |
| **Modelos base** | 0 | 3 abstratos |
| **Validators** | 0 | 15+ |
| **Indexes** | 0 | 20+ |
| **Constraints** | 0 | 6 |
| **Choices** | Strings soltas | 4 Enums |
| **Métodos de negócio** | 0 | 8+ |
| **Campos TimeField** | 0 (strings) | 6 |
| **Documentação** | Mínima | Completa |

---

## 🚀 Como Migrar

### Passo 1: Backup
```bash
python manage.py dumpdata > backup.json
```

### Passo 2: Substituir models.py
```bash
cp models_refactored.py models.py
```

### Passo 3: Criar migrations
```bash
python manage.py makemigrations
```

### Passo 4: Revisar migrations geradas
```bash
# Verifique se há data migrations necessárias
# Ex: converter strings "Segunda" para 0 (DiaSemana.SEGUNDA)
```

### Passo 5: Aplicar
```bash
python manage.py migrate
```

### Passo 6: Atualizar serializers e views
- Atualizar `serializers.py` para novos campos
- Ajustar filtros em `views.py` para usar choices
- Atualizar testes

---

## ⚠️ Breaking Changes

### 1. Turma: campos de horário
**Antes:**
```python
turma.dias_da_semana  # "Segunda, Quarta"
turma.horario  # "18:00 - 21:00"
```

**Depois:**
```python
turma.hora_inicio  # time(18, 0)
turma.hora_fim  # time(21, 0)
turma.dias_semana.all()  # QuerySet[TurmaDiaSemana]
```

### 2. Status como Choices
**Antes:**
```python
inscricao.status = "Pendente"
```

**Depois:**
```python
from .models import StatusInscricao
inscricao.status = StatusInscricao.PENDENTE
```

### 3. Novos campos obrigatórios
- `Vaga.vagas_disponiveis`
- `Turma.hora_inicio` e `hora_fim`
- `Curso.codigo` (pode ser blank)

---

## 🎯 Próximos Passos Recomendados

1. **Criar signals** para notificações automáticas
2. **Adicionar managers customizados** para queries comuns
3. **Implementar testes** para validações e métodos
4. **Criar migrations de dados** para converter formatos antigos
5. **Documentar API** com drf-spectacular

---

## 📚 Recursos

- [Django Model Best Practices](https://docs.djangoproject.com/en/5.0/topics/db/models/)
- [Django Choices](https://docs.djangoproject.com/en/5.0/ref/models/fields/#choices)
- [Database Constraints](https://docs.djangoproject.com/en/5.0/ref/models/constraints/)
- [Model Validators](https://docs.djangoproject.com/en/5.0/ref/validators/)

---

## 💡 Dicas de Uso

### Queries otimizadas
```python
# Antes
alunos = Aluno.objects.all()
for aluno in alunos:
    print(aluno.curso.nome)  # N+1 query!

# Depois
alunos = AlunoProfile.objects.select_related('user', 'curso').all()
for aluno in alunos:
    print(aluno.nome_completo, aluno.curso.nome)  # 1 query!
```

### Filtros com Choices
```python
# Aprovados
inscricoes = Inscricao.objects.filter(status=StatusInscricao.APROVADO)

# Pendentes ou aprovados
from django.db.models import Q
inscricoes = Inscricao.objects.filter(
    Q(status=StatusInscricao.PENDENTE) | Q(status=StatusInscricao.APROVADO)
)
```

### Soft delete
```python
# Desativar
aluno.desativar()

# Reativar
aluno.ativar()

# Filtrar apenas ativos
alunos_ativos = AlunoProfile.objects.filter(ativo=True)
```

---

## ✅ Checklist de Validação

- [ ] Todos os testes passam
- [ ] Migrations aplicadas sem erros
- [ ] Admin funciona corretamente
- [ ] API REST retorna dados corretos
- [ ] Performance melhorou (usar django-debug-toolbar)
- [ ] Serializers atualizados
- [ ] Views atualizadas
- [ ] Documentação atualizada
