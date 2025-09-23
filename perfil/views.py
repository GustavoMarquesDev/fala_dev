from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import copy

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
            usuario=request.user,
            post=pergunta
        )

        context = {
            'pergunta': pergunta,
            'respostas': respostas
        }
        return render(request, 'perfil/minhas_respostas.html', context)
