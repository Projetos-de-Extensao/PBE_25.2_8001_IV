from django import forms

from .models import MaterialApoio, Disciplina, Curso


class MaterialApoioForm(forms.ModelForm):
    """Formulário usado pelos monitores para cadastrar materiais de apoio."""

    class Meta:
        model = MaterialApoio
        fields = ['titulo', 'tipo', 'descricao', 'arquivo']
        widgets = {
            # Campo de título com placeholder guiando o padrão de nome
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Lista 3 - Integrais Duplas',
            }),
            # Seletor com as categorias definidas no modelo
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            # Área de texto opcional para contextualizar o conteúdo
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descreva brevemente o conteúdo do material.',
                'rows': 3,
            }),
            # Componente padrão do Django que permite trocar/remover arquivo
            'arquivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'titulo': 'Título do material',
            'tipo': 'Tipo do material',
            'descricao': 'Descrição (opcional)',
            'arquivo': 'Arquivo',
        }


class DisciplinaForm(forms.ModelForm):
    """Formulário para professores criarem novas disciplinas."""

    class Meta:
        model = Disciplina
        fields = ['codigo', 'nome', 'curso', 'carga_horaria', 'periodo_sugerido', 'ementa', 'pre_requisitos']
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: CC101, MAT001, ENG102',
                'maxlength': 20,
            }),
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Cálculo I, Programação Orientada a Objetos',
                'maxlength': 100,
            }),
            'curso': forms.Select(attrs={
                'class': 'form-select',
            }),
            'carga_horaria': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '60',
                'min': 1,
                'max': 300,
            }),
            'periodo_sugerido': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '1',
                'min': 1,
                'max': 10,
            }),
            'ementa': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descreva os principais tópicos abordados na disciplina...',
                'rows': 4,
            }),
            'pre_requisitos': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': 5,
            }),
        }
        labels = {
            'codigo': 'Código da disciplina',
            'nome': 'Nome da disciplina',
            'curso': 'Curso',
            'carga_horaria': 'Carga horária (horas)',
            'periodo_sugerido': 'Período sugerido',
            'ementa': 'Ementa',
            'pre_requisitos': 'Pré-requisitos (opcional)',
        }
        help_texts = {
            'codigo': 'Código único da disciplina (ex: CC101)',
            'carga_horaria': 'Total de horas da disciplina no semestre',
            'periodo_sugerido': 'Em qual período é recomendado cursar',
            'pre_requisitos': 'Ctrl+clique para selecionar múltiplas disciplinas',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar cursos ativos
        self.fields['curso'].queryset = Curso.objects.filter(ativo=True).order_by('nome')
        # Filtrar disciplinas ativas para pré-requisitos
        self.fields['pre_requisitos'].queryset = Disciplina.objects.filter(ativo=True).order_by('curso__nome', 'periodo_sugerido', 'nome')
        # Definir pré-requisitos como não obrigatório
        self.fields['pre_requisitos'].required = False
    
    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo', '').upper()
        # Verificar se já existe uma disciplina com esse código
        if Disciplina.objects.filter(codigo=codigo).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError('Já existe uma disciplina com este código.')
        return codigo
