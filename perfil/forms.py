
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Perfil


class CadastroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nome = forms.CharField(required=True)
    sobrenome = forms.CharField(required=True)
    profissao = forms.CharField(required=False)
    foto = forms.ImageField(required=False, label="Foto de perfil")

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
            nome = self.cleaned_data.get("nome")
            sobrenome = self.cleaned_data.get("sobrenome")
            email = self.cleaned_data.get("email")
            perfil = Perfil.objects.create(user=user, nome=nome, sobrenome=sobrenome,
                                           email=email, profissao=profissao)
            foto = self.cleaned_data.get("foto")
            if foto:
                perfil.foto = foto
                perfil.save()
        return user


class AtualizarPerfilForm(forms.ModelForm):
    nova_senha1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nova senha (deixe em branco para manter a atual)'
        }),
        required=False,
        label='Nova Senha'
    )
    nova_senha2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme a nova senha'
        }),
        required=False,
        label='Confirmar Nova Senha'
    )
    senha_atual = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha atual para confirmar as alterações'
        }),
        required=True,
        label='Senha Atual'
    )

    class Meta:
        model = Perfil
        fields = ('nome', 'sobrenome', 'email', 'profissao', 'foto')
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome'
            }),
            'sobrenome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sobrenome'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'profissao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Profissão'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_nova_senha2(self):
        nova_senha1 = self.cleaned_data.get('nova_senha1')
        nova_senha2 = self.cleaned_data.get('nova_senha2')

        if nova_senha1 or nova_senha2:
            if nova_senha1 != nova_senha2:
                raise forms.ValidationError('As senhas não coincidem.')

            if len(nova_senha1) < 8:
                raise forms.ValidationError(
                    'A senha deve ter pelo menos 8 caracteres.')

        return nova_senha2

    def clean_senha_atual(self):
        senha_atual = self.cleaned_data.get('senha_atual')

        if not self.user.check_password(senha_atual):
            raise forms.ValidationError('Senha atual incorreta.')

        return senha_atual

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Verifica se o email já está sendo usado por outro usuário
        if User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError(
                'Este email já está sendo usado por outro usuário.')

        return email
