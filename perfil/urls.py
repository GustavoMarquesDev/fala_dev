from django.urls import path

from . import views

app_name = "perfil"

urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('criar/', views.Criar.as_view(), name='criar'),
    path('minhasPerguntas/', views.MinhasPerguntas.as_view(), name='minhasPerguntas'),
]
