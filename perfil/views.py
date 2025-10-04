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


class AtualizarPerfil(View):
    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(
                request, 'Você precisa estar logado para atualizar seu perfil.')
            return redirect('perfil:login')

        perfil = get_object_or_404(models.Perfil, user=request.user)
        form = forms.AtualizarPerfilForm(instance=perfil, user=request.user)
        return render(request, 'perfil/atualizar_perfil.html', {'form': form, 'perfil': perfil})

    def post(self, request):
        if not request.user.is_authenticated:
            messages.error(
                request, 'Você precisa estar logado para atualizar seu perfil.')
            return redirect('perfil:login')

        perfil = get_object_or_404(models.Perfil, user=request.user)
        form = forms.AtualizarPerfilForm(
            request.POST, request.FILES, instance=perfil, user=request.user)

        if form.is_valid():
            # Atualiza os dados do perfil
            form.save()

            # Atualiza os dados do usuário
            user = request.user
            user.first_name = form.cleaned_data['nome']
            user.last_name = form.cleaned_data['sobrenome']
            user.email = form.cleaned_data['email']

            # Atualiza senha se fornecida
            nova_senha = form.cleaned_data.get('nova_senha1')
            if nova_senha:
                user.set_password(nova_senha)
                messages.success(
                    request, 'Perfil e senha atualizados com sucesso!')
            else:
                messages.success(request, 'Perfil atualizado com sucesso!')

            user.save()

            return redirect('perfil:atualizarPerfil')

        messages.error(request, 'Corrija os erros abaixo.')
        return render(request, 'perfil/atualizar_perfil.html', {'form': form, 'perfil': perfil})


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
        fotos_existentes = pergunta.fotos.all()  # type: ignore
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


class Like(View):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            messages.error(
                request, 'Você precisa estar logado para avaliar respostas.')
            return redirect('perfil:login')

        resposta = get_object_or_404(models.RespostasDoUsuario, pk=pk)

        # Usuário não pode avaliar sua própria resposta
        if request.user == resposta.usuario:
            messages.error(
                request, 'Você não pode avaliar sua própria resposta.')
            return redirect('lista:detalhes', pk=resposta.post.pk)

        # Verifica se o usuário já avaliou esta resposta
        avaliacao_existente = models.AvaliacaoResposta.objects.filter(
            usuario=request.user,
            resposta=resposta
        ).first()

        if avaliacao_existente:
            if avaliacao_existente.tipo_avaliacao == models.AvaliacaoResposta.LIKE:
                # Se já deu like, remove a avaliação
                avaliacao_existente.delete()

            else:
                # Se deu dislike, muda para like
                avaliacao_existente.tipo_avaliacao = models.AvaliacaoResposta.LIKE
                avaliacao_existente.save()

        else:
            # Cria nova avaliação de like
            models.AvaliacaoResposta.objects.create(
                usuario=request.user,
                resposta=resposta,
                tipo_avaliacao=models.AvaliacaoResposta.LIKE
            )

        return redirect('lista:detalhes', pk=resposta.post.pk)


class Deslike(View):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            messages.error(
                request, 'Você precisa estar logado para avaliar respostas.')
            return redirect('perfil:login')

        resposta = get_object_or_404(models.RespostasDoUsuario, pk=pk)

        # Usuário não pode avaliar sua própria resposta
        if request.user == resposta.usuario:
            messages.error(
                request, 'Você não pode avaliar sua própria resposta.')
            return redirect('lista:detalhes', pk=resposta.post.pk)

        # Verifica se o usuário já avaliou esta resposta
        avaliacao_existente = models.AvaliacaoResposta.objects.filter(
            usuario=request.user,
            resposta=resposta
        ).first()

        if avaliacao_existente:
            if avaliacao_existente.tipo_avaliacao == models.AvaliacaoResposta.DISLIKE:
                # Se já deu dislike, remove a avaliação
                avaliacao_existente.delete()

            else:
                # Se deu like, muda para dislike
                avaliacao_existente.tipo_avaliacao = models.AvaliacaoResposta.DISLIKE
                avaliacao_existente.save()

        else:
            # Cria nova avaliação de dislike
            models.AvaliacaoResposta.objects.create(
                usuario=request.user,
                resposta=resposta,
                tipo_avaliacao=models.AvaliacaoResposta.DISLIKE
            )

        return redirect('lista:detalhes', pk=resposta.post.pk)


class LikeRespostaDaResposta(View):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            messages.error(
                request, 'Você precisa estar logado para avaliar respostas.')
            return redirect('perfil:login')

        resposta_da_resposta = get_object_or_404(
            models.RespostaDaResposta, pk=pk)

        # Usuário não pode avaliar sua própria resposta
        if request.user == resposta_da_resposta.usuario:
            messages.error(
                request, 'Você não pode avaliar sua própria resposta.')
            return redirect('lista:detalhes', pk=resposta_da_resposta.resposta.post.pk)

        # Verifica se o usuário já avaliou esta resposta
        avaliacao_existente = models.AvaliacaoRespostaDaResposta.objects.filter(
            usuario=request.user,
            resposta=resposta_da_resposta
        ).first()

        if avaliacao_existente:
            if avaliacao_existente.tipo_avaliacao == models.AvaliacaoRespostaDaResposta.LIKE:
                # Se já deu like, remove a avaliação
                avaliacao_existente.delete()

            else:
                # Se deu dislike, muda para like
                avaliacao_existente.tipo_avaliacao = models.AvaliacaoRespostaDaResposta.LIKE
                avaliacao_existente.save()

        else:
            # Cria nova avaliação de like
            models.AvaliacaoRespostaDaResposta.objects.create(
                usuario=request.user,
                resposta=resposta_da_resposta,
                tipo_avaliacao=models.AvaliacaoRespostaDaResposta.LIKE
            )

        return redirect('lista:detalhes', pk=resposta_da_resposta.resposta.post.pk)


class DeslikeRespostaDaResposta(View):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            messages.error(
                request, 'Você precisa estar logado para avaliar respostas.')
            return redirect('perfil:login')

        resposta_da_resposta = get_object_or_404(
            models.RespostaDaResposta, pk=pk)

        # Usuário não pode avaliar sua própria resposta
        if request.user == resposta_da_resposta.usuario:
            messages.error(
                request, 'Você não pode avaliar sua própria resposta.')
            return redirect('lista:detalhes', pk=resposta_da_resposta.resposta.post.pk)

        # Verifica se o usuário já avaliou esta resposta
        avaliacao_existente = models.AvaliacaoRespostaDaResposta.objects.filter(
            usuario=request.user,
            resposta=resposta_da_resposta
        ).first()

        if avaliacao_existente:
            if avaliacao_existente.tipo_avaliacao == models.AvaliacaoRespostaDaResposta.DISLIKE:
                # Se já deu dislike, remove a avaliação
                avaliacao_existente.delete()

            else:
                # Se deu like, muda para dislike
                avaliacao_existente.tipo_avaliacao = models.AvaliacaoRespostaDaResposta.DISLIKE
                avaliacao_existente.save()

        else:
            # Cria nova avaliação de dislike
            models.AvaliacaoRespostaDaResposta.objects.create(
                usuario=request.user,
                resposta=resposta_da_resposta,
                tipo_avaliacao=models.AvaliacaoRespostaDaResposta.DISLIKE
            )

        return redirect('lista:detalhes', pk=resposta_da_resposta.resposta.post.pk)
