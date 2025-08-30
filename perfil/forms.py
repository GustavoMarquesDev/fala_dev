
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil


class CadastroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nome = forms.CharField(required=True)
    sobrenome = forms.CharField(required=True)
    profissao = forms.CharField(required=False)
    foto = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2",
                  "nome", "sobrenome", "profissao", "foto")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["nome"]
        user.last_name = self.cleaned_data["sobrenome"]
        if commit:
            user.save()
            profissao = self.cleaned_data.get("profissao")
            foto = self.cleaned_data.get("foto")
            nome = self.cleaned_data.get("nome")
            sobrenome = self.cleaned_data.get("sobrenome")
            email = self.cleaned_data.get("email")
            Perfil.objects.create(user=user, nome=nome, sobrenome=sobrenome,
                                  email=email, profissao=profissao, foto=foto)
        return user
