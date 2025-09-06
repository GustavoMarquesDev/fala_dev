from django.urls import path
from . import views

app_name = "lista"

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('perguntar/', views.Perguntar.as_view(), name='perguntar'),
]
