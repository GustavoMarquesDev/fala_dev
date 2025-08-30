from django.contrib import admin
from .models import Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'user',
                    'nome',
                    'sobrenome',
                    'email',
                    'profissao'
                    )
    list_display_links = ('id', 'user')
    search_fields = ('user',  'nome', 'sobrenome', 'email', 'profissao')
