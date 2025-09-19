from django import forms
from perfil.models import PerguntasDoUsuario


class PerguntaForm(forms.ModelForm):

    class Meta:
        model = PerguntasDoUsuario
        fields = ['titulo', 'descricao', 'categoria',]

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título da pergunta'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição da pergunta'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),

        }
