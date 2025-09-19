from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages

from lista.forms import PerguntaForm
from perfil.models import FotoErro


class Index(View):
    def get(self, request):
        return render(request, 'lista/home.html')


class Perguntar(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, 'Faça login para fazer perguntas.')
            return redirect('perfil:login')

        form = PerguntaForm()
        return render(request, 'lista/perguntar.html', {'form': form})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, 'Faça login para fazer perguntas.')
            return redirect('perfil:login')

        form = PerguntaForm(request.POST, request.FILES)

        fotos = request.FILES.getlist('fotos')
        if form.is_valid():
            pergunta = form.save(commit=False)
            pergunta.usuario = request.user
            pergunta.save()
            foto = form.cleaned_data.get('foto')

            for foto in fotos:
                FotoErro.objects.create(post=pergunta, foto=foto)

            messages.success(request, 'Pergunta enviada com sucesso.')
            return redirect('lista:index')
        else:
            messages.error(request, 'Verifique os dados enviados.')
            return render(request, 'lista/perguntar.html', {'form': form})
