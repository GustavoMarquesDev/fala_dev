from django.shortcuts import render
from django.views import View

# Create your views here.


class Criar(View):
    def get(self, request):
        return render(request, 'perfil/criar.html')
