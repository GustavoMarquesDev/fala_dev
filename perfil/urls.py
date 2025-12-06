from django.urls import path

from . import views

app_name = "perfil"

urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('criar/', views.Criar.as_view(), name='criar'),
    path('minhasPerguntas/', views.MinhasPerguntas.as_view(), name='minhasPerguntas'),
    path('minhasRespostas/<int:pk>',
         views.MinhasRespostas.as_view(), name='minhasRespostas'),
    path('removerPergunta/<int:pk>',
         views.RemoverPergunta.as_view(), name='removerPergunta'),
    path('editar/<int:pk>', views.Editar.as_view(), name='editar'),
    path('remover-foto/<int:pk>/', views.RemoverFoto.as_view(), name='remover_foto'),
    path('editarResposta/<int:pk>',
         views.EditarResposta.as_view(), name='editarResposta'),
    path('like/<int:pk>/', views.Like.as_view(), name='like'),
    path('deslike/<int:pk>/', views.Deslike.as_view(), name='deslike'),
    path('like-resposta-da-resposta/<int:pk>/',
         views.LikeRespostaDaResposta.as_view(), name='like_resposta_da_resposta'),
    path('deslike-resposta-da-resposta/<int:pk>/',
         views.DeslikeRespostaDaResposta.as_view(), name='deslike_resposta_da_resposta'),
    path('atualizarPerfil/', views.AtualizarPerfil.as_view(), name='atualizarPerfil'),
    path('minhasRespostasAosOutros/', views.MinhasRespostasAosOutros.as_view(),
         name='minhasRespostasAosOutros'),
    path('notificacoes/', views.ListarNotificacoes.as_view(), name='notificacoes'),
    path('notificacoes/marcar-lida/<int:pk>/',
         views.MarcarNotificacaoLida.as_view(), name='marcar_notificacao_lida'),
    path('notificacoes/marcar-todas-lidas/', views.MarcarTodasNotificacoesLidas.as_view(),
         name='marcar_todas_notificacoes_lidas'),
    path('ver-perfil/<int:pk>/', views.VerPerfil.as_view(), name='ver_perfil'),
]
