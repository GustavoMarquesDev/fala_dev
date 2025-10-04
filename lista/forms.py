from django import forms
from perfil.models import PerguntasDoUsuario, RespostasDoUsuario, RespostaDaResposta


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

    def clean_resposta(self):
        resposta = self.cleaned_data.get('resposta', '').strip()
        if len(resposta) < 10:
            raise forms.ValidationError(
                'A resposta deve ter pelo menos 10 caracteres.')
        return resposta


class RespostaDaRespostaForm(forms.ModelForm):
    class Meta:
        model = RespostaDaResposta
        fields = ['texto_resposta', 'imagem']

        widgets = {
            'texto_resposta': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Digite sua resposta aqui...'}),
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_texto_resposta(self):
        texto_resposta = self.cleaned_data.get('texto_resposta', '').strip()
        if len(texto_resposta) < 10:
            raise forms.ValidationError(
                'A resposta deve ter pelo menos 10 caracteres.')
        return texto_resposta
