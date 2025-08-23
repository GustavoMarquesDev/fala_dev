from django.contrib import admin
from .models import Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'usuario',
                    'nome',
                    'sobrenome',
                    'email',
                    'profissao'
                    )
    list_display_links = ('id', 'usuario')
    search_fields = ('usuario',  'nome', 'sobrenome', 'email', 'profissao')
