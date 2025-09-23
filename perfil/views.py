from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


from lista.forms import PerguntaForm, RespostaForm
from . import models
from . import forms

PER_PAGE = 10


class Criar(View):
    def get(self, request):
        form = forms.CadastroForm()
        return render(request, 'perfil/criar.html', {'form': form})

    def post(self, request):
        form = forms.CadastroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('perfil:login')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
        return render(request, 'perfil/criar.html', {'form': form})


class Login(View):
    def get(self, request):
        return render(request, 'perfil/login.html')

    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            messages.error(self.request, 'Preencha todos os campos')
            return redirect('lista:index')

        user = authenticate(self.request, username=username, password=password)

        if not user:
            messages.error(self.request, 'Usuário ou senha incorretos')
            return redirect('perfil:login')

        login(self.request, user=user)

        messages.success(self.request, f'Bem vindo {user.first_name}!!!')

        return redirect('lista:index')


class Logout(View):
    def get(self, *args, **kwargs):
        logout(self.request)
        messages.success(self.request, 'Sessão encerrada')
        return redirect('lista:index')


class MinhasPerguntas(View):

    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(request, 'Faça login para ver suas perguntas.')
            return redirect('perfil:login')

        perguntas = models.PerguntasDoUsuario.objects.filter(
            usuario=request.user).order_by('-criado_em')

        context = {'perguntas': perguntas}
        return render(request, 'perfil/minhas_perguntas.html', context)


class MinhasRespostas(View):
    def get(self, request, pk):
        pergunta = get_object_or_404(models.PerguntasDoUsuario, pk=pk)

        respostas = models.RespostasDoUsuario.objects.filter(
            post=pergunta
        ).order_by('-data_de_criacao')

        context = {
            'pergunta': pergunta,
            'respostas': respostas
        }

        return render(request, 'perfil/minhas_respostas.html', context)


class ListaRespostas(View):
    def get(self, request):
        respostas = models.RespostasDoUsuario.objects.filter(
            usuario=request.user
        ).order_by('-data_de_criacao')
        context = {'respostas': respostas}
        return render(request, 'perfil/lista_respostas.html', context)


class RemoverPergunta(View):
    def get(self, request, pk):
        pergunta = get_object_or_404(models.PerguntasDoUsuario, pk=pk)
        if request.user == pergunta.usuario:
            pergunta.delete()
            messages.success(request, 'Pergunta removida com sucesso!')
            return redirect('perfil:minhasPerguntas')


class Editar(View):
    def get(self, request, pk):
        pergunta = get_object_or_404(models.PerguntasDoUsuario, pk=pk)
        if request.user != pergunta.usuario:
            messages.error(request, 'Você não pode editar essa pergunta.')
            return redirect('perfil:minhasPerguntas')

        form = PerguntaForm(instance=pergunta)
        fotos_existentes = pergunta.fotos.all()
        return render(request, 'perfil/editar_pergunta.html', {
            'form': form,
            'fotos_existentes': fotos_existentes,
            'pergunta': pergunta,
        })

    def post(self, request, pk):
        pergunta = get_object_or_404(models.PerguntasDoUsuario, pk=pk)
        if request.user != pergunta.usuario:
            messages.error(request, 'Você não pode editar essa pergunta.')
            return redirect('perfil:minhasPerguntas')

        form = PerguntaForm(request.POST, request.FILES, instance=pergunta)

        fotos = request.FILES.getlist('fotos')
        if form.is_valid():
            pergunta = form.save(commit=False)
            pergunta.usuario = request.user
            pergunta.save()
            foto = form.cleaned_data.get('foto')

            for foto in fotos:
                models.FotoErro.objects.update_or_create(
                    post=pergunta, foto=foto)

        if form.is_valid():
            form.save()
            messages.success(request, 'Pergunta editada com sucesso!')
            return redirect('perfil:minhasPerguntas')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
        return render(request, 'perfil/editar_pergunta.html', {'form': form})


class RemoverFoto(View):
    def post(self, request, pk):
        foto = get_object_or_404(models.FotoErro, pk=pk)
        pergunta = foto.post
        if request.user != pergunta.usuario:
            messages.error(request, 'Você não pode remover esta imagem.')
            return redirect('perfil:minhasPerguntas')

        foto.delete()
        messages.success(request, 'Imagem removida com sucesso!')
        return redirect('perfil:editar', pk=pergunta.pk)


class EditarResposta(View):
    def get(self, request, pk):
        resposta = get_object_or_404(models.RespostasDoUsuario, pk=pk)
        if request.user != resposta.usuario:
            messages.error(request, 'Você não pode editar essa resposta.')
            return redirect('perfil:minhasRespostas', pk=resposta.post.pk)
        form = RespostaForm(instance=resposta)
        return render(request, 'perfil/editar_resposta.html', {'form': form})

    def post(self, request, pk):
        resposta = get_object_or_404(models.RespostasDoUsuario, pk=pk)
        if request.user != resposta.usuario:
            messages.error(request, 'Você não pode editar essa resposta.')
            return redirect('perfil:minhasRespostas', pk=resposta.post.pk)
        form = RespostaForm(request.POST, request.FILES, instance=resposta)

        if form.is_valid():
            form.save()
            messages.success(request, 'Resposta editada com sucesso!')
            return redirect('perfil:minhasRespostas', pk=resposta.post.pk)
        else:
            messages.error(request, 'Corrija os erros abaixo.')
        return render(request, 'perfil/editar_resposta.html', {'form': form})
