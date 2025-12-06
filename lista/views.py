from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages
from django.views.generic import DetailView, ListView
from django.db.models import Q

from lista.forms import PerguntaForm, RespostaForm, RespostaDaRespostaForm
from perfil.models import FotoErro, PerguntasDoUsuario, RespostasDoUsuario, RespostaDaResposta as RespostaDaRespostaModel, Notificacao

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

            messages.success(request, 'Resposta enviada com sucesso.')
            return redirect('lista:index')
        else:
            messages.error(request, 'Verifique os dados enviados.')
            return render(request, 'lista/perguntar.html', {'form': form})


class Perguntas(View):
    def get(self, request):
        perguntas = PerguntasDoUsuario.objects.all().order_by('-criado_em')

        context = {'perguntas': perguntas}

        return render(request, 'lista/perguntas.html', context)


class Detalhes(DetailView):
    model = PerguntasDoUsuario
    template_name = 'lista/detalhes.html'
    context_object_name = 'pergunta'
    slug_url_kwarg = 'pk'


class Resposta(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, 'Faça login para responder perguntas.')
            return redirect('perfil:login')

        try:
            pergunta = PerguntasDoUsuario.objects.get(
                pk=kwargs['pk'])
        except PerguntasDoUsuario.DoesNotExist:
            messages.error(request, 'Pergunta não encontrada.')
            return redirect('lista:index')

        form = RespostaForm()
        context = {
            'form': form,
            'pergunta': pergunta
        }
        return render(request, 'lista/resposta.html', context)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, 'Faça login para responder perguntas.')
            return redirect('perfil:login')

        try:
            pergunta = PerguntasDoUsuario.objects.get(
                pk=kwargs['pk'])
        except PerguntasDoUsuario.DoesNotExist:
            messages.error(request, 'Pergunta não encontrada.')
            return redirect('lista:index')

        form = RespostaForm(request.POST, request.FILES)

        if form.is_valid():
            resposta = form.save(commit=False)
            resposta.usuario = request.user
            resposta.post = pergunta
            resposta.save()  # Salvando no banco de dados

            # Criar notificação se o autor da resposta não for o autor da pergunta
            if pergunta.usuario != request.user:
                Notificacao.objects.create(
                    usuario=pergunta.usuario,
                    pergunta=pergunta,
                    resposta=resposta
                )

            messages.success(request, 'Resposta enviada com sucesso.')
            return redirect('lista:detalhes', pk=kwargs['pk'])
        else:
            messages.error(request, 'Verifique todos os dados enviados.')
            context = {
                'form': form,
                'pergunta': pergunta
            }
            return render(request, 'lista/resposta.html', context)


class RespostaDaResposta(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, 'Faça login para responder respostas.')
            return redirect('perfil:login')

        try:
            resposta = RespostasDoUsuario.objects.get(
                pk=kwargs['pk'])
        except RespostasDoUsuario.DoesNotExist:
            messages.error(request, 'Resposta não encontrada.')
            return redirect('lista:index')

        form = RespostaDaRespostaForm()
        resposta_pai_id = request.GET.get('resposta_pai_id')
        resposta_pai = None
        if resposta_pai_id:
            resposta_pai = RespostaDaRespostaModel.objects.filter(
                pk=resposta_pai_id).first()

        context = {
            'form': form,
            'resposta': resposta,
            'pergunta': resposta.post,
            'resposta_pai': resposta_pai,
            'resposta_pai_id': resposta_pai_id
        }
        return render(request, 'lista/resposta_da_resposta.html', context)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, 'Faça login para responder respostas.')
            return redirect('perfil:login')

        try:
            resposta = RespostasDoUsuario.objects.get(
                pk=kwargs['pk'])
        except RespostasDoUsuario.DoesNotExist:
            messages.error(request, 'Resposta não encontrada.')
            return redirect('lista:index')

        form = RespostaDaRespostaForm(request.POST, request.FILES)

        if form.is_valid():
            resposta_da_resposta = form.save(commit=False)
            resposta_da_resposta.usuario = request.user
            resposta_da_resposta.resposta = resposta

            # Verificar se está respondendo a uma resposta de resposta específica
            resposta_pai_id = request.POST.get(
                'resposta_pai_id') or request.GET.get('resposta_pai_id')
            if resposta_pai_id:
                resposta_pai = RespostaDaRespostaModel.objects.filter(
                    pk=resposta_pai_id).first()
                if resposta_pai:
                    resposta_da_resposta.resposta_pai = resposta_pai

            resposta_da_resposta.save()

            # Criar notificações
            usuarios_notificados = set()

            # Notificar o autor da resposta de resposta (resposta_pai) se estiver respondendo a uma
            if resposta_da_resposta.resposta_pai and resposta_da_resposta.resposta_pai.usuario != request.user:
                usuarios_notificados.add(
                    resposta_da_resposta.resposta_pai.usuario.id)
                Notificacao.objects.create(
                    usuario=resposta_da_resposta.resposta_pai.usuario,
                    pergunta=resposta.post,
                    resposta=resposta,
                    resposta_da_resposta=resposta_da_resposta
                )

            # Criar notificação para o autor da resposta original se não for o próprio usuário e ainda não foi notificado
            if resposta.usuario != request.user and resposta.usuario.id not in usuarios_notificados:
                Notificacao.objects.create(
                    usuario=resposta.usuario,
                    pergunta=resposta.post,
                    resposta=resposta,
                    resposta_da_resposta=resposta_da_resposta
                )

            messages.success(request, 'Resposta enviada com sucesso.')
            return redirect('lista:detalhes', pk=resposta.post.pk)
        else:
            messages.error(request, 'Verifique todos os dados enviados.')
            context = {
                'form': form,
                'resposta': resposta,
                'pergunta': resposta.post
            }
            return render(request, 'lista/resposta_da_resposta.html', context)


class EditarResposta(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'lista/editar_resposta.html')


class DeletarResposta(View):
    def get(self, request, *args, **kwargs):
        resposta_id = self.kwargs.get('pk')
        print(resposta_id)
        resposta = get_object_or_404(
            RespostasDoUsuario, pk=resposta_id, usuario=request.user)

        resposta.delete()
        messages.success(request, 'Resposta excluída com sucesso.')
        return redirect('lista:detalhes', pk=resposta.post.pk)


class Busca(ListView):
    model = PerguntasDoUsuario
    template_name = 'lista/home.html'
    context_object_name = 'perguntas'
    paginate_by = PER_PAGE
    ordering = ['-criado_em']

    def get(self, request, *args, **kwargs):
        termo = request.GET.get('termo')
        if termo == '' or termo is None:
            return redirect('lista:index')
        return super().get(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        termo = self.request.GET.get('termo')
        qs = super().get_queryset(*args, **kwargs)

        if not termo:
            return qs

        qs = qs.filter(
            Q(titulo__icontains=termo) | Q(
                descricao__icontains=termo) | Q(categoria__icontains=termo)
        )
        print(termo)

        return qs
