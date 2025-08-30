from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

from utils import resize_image


class Perfil(models.Model):

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Usuário'
    )
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome',
        blank=False,
        null=False
    )
    sobrenome = models.CharField(
        max_length=100,
        verbose_name='Sobrenome',
        blank=True,
        null=True
    )
    email = models.EmailField(
        verbose_name='Email',
        blank=False,
        null=False
    )
    profissao = models.CharField(
        max_length=100,
        verbose_name='Profissão',
        blank=False,
        null=False
    )
    foto = models.ImageField(
        upload_to='perfil/fotos/%Y/%m/%d',
        verbose_name='Foto de Perfil',
        blank=True, null=True,
        help_text='Foto de perfil a ser exibida para todos os usuários ')

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        if self.foto:
            resize_image(self.foto)

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'
