from .models import Notificacao


def notificacoes_nao_lidas(request):
    """
    Context processor para adicionar o número de notificações não lidas
    em todos os templates.
    """
    if request.user.is_authenticated:
        count = Notificacao.objects.filter(
            usuario=request.user,
            lida=False
        ).count()
        return {'notificacoes_nao_lidas_count': count}
    return {'notificacoes_nao_lidas_count': 0}
