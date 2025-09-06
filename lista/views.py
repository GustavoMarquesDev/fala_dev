from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages


class Index(View):
    def get(self, request):
        return render(request, 'lista/home.html')


class Perguntar(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, 'Faça login para fazer perguntas.')
            return redirect('perfil:login')

        return render(request, 'lista/perguntar.html')
