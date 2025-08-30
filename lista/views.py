from django.shortcuts import render
from django.views import View
from django.contrib import messages


class Index(View):
    def get(self, request):
        return render(request, 'lista/home.html')
