from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError


class Perfil(models.Model):

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Usuário')
    nome = models.CharField(
        max_length=100, verbose_name='Nome', blank=False, null=False)
    sobrenome = models.CharField(
        max_length=100, verbose_name='Sobrenome', blank=True, null=True)
    email = models.EmailField(verbose_name='Email', blank=False, null=False)
    profissao = models.CharField(
        max_length=100, verbose_name='Profissão', blank=False, null=False)

    def __str__(self):
        return f'{self.usuario}'
