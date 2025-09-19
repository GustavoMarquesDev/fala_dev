from django.contrib import admin


from perfil.models import PerguntasDoUsuario, FotoErro, RespostasDoUsuario
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


class RespostasDoUsuarioInline(admin.TabularInline):
    model = RespostasDoUsuario
    extra = 1


class FotosDerroInline(admin.TabularInline):
    model = FotoErro
    extra = 0


class PerguntasDoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'categoria', 'criado_em')
    list_display_links = ('titulo',)
    search_fields = ('titulo', 'usuario')
    inlines = [FotosDerroInline, RespostasDoUsuarioInline]


admin.site.register(PerguntasDoUsuario, PerguntasDoUsuarioAdmin)
admin.site.site_header = "Administração do Fala Dev"
