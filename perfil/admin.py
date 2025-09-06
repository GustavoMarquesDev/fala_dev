from django.contrib import admin


from perfil.models import PerguntasDoUsuario, FotoErro, Votos
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


class VotosInline(admin.TabularInline):
    model = Votos
    extra = 1


class FotosDerroInline(admin.TabularInline):
    model = FotoErro
    extra = 1


class PerguntasDoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'categoria', 'criado_em')
    list_display_links = ('titulo',)
    search_fields = ('titulo', 'usuario')
    inlines = [FotosDerroInline, VotosInline]


admin.site.register(PerguntasDoUsuario, PerguntasDoUsuarioAdmin)
admin.site.site_header = "Administração do Fala Dev"
