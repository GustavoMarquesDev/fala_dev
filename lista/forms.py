from django import forms
from perfil.models import PerguntasDoUsuario, RespostasDoUsuario


class PerguntaForm(forms.ModelForm):

    class Meta:
        model = PerguntasDoUsuario
        fields = ['titulo', 'descricao', 'categoria',]

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título da pergunta'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição da pergunta'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),

        }


class RespostaForm(forms.ModelForm):

    class Meta:
        model = RespostasDoUsuario
        fields = ['resposta', 'imagem']

        widgets = {

            'resposta': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Digite sua resposta aqui...'}),
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
        }
