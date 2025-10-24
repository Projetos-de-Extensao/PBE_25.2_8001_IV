from django import forms

from .models import MaterialApoio


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
