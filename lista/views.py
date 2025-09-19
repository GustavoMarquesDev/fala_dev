from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.views.generic import DetailView, ListView

from lista.forms import PerguntaForm
from perfil.models import FotoErro, PerguntasDoUsuario

PER_PAGE = 10


class Index(ListView):
    model = PerguntasDoUsuario
    template_name = 'lista/home.html'
    context_object_name = 'perguntas'
    paginate_by = PER_PAGE
    ordering = ['-criado_em']


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


class Perguntas(View):
    def get(self, request):
        perguntas = PerguntasDoUsuario.objects.all().order_by('-criado_em')

        return render(request, 'lista/perguntas.html', {'perguntas': perguntas})


class Detalhes(DetailView):
    model = PerguntasDoUsuario
    template_name = 'lista/detalhes.html'
    context_object_name = 'pergunta'
    slug_url_kwarg = 'pk'
