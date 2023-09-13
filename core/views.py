from django.shortcuts import render, redirect
from core.models import Evento


# Create your views here.

# def index_redirect():       AQUI FOI SO UMA MANEIRA DE REDIRECIONAR A PÁGINA QUANDO A URL TA PURA
#    return redirect('/agenda/')


def lista_eventos(request):
    # evento = Evento.objects.get(id=1)
    # evento = Evento.objects.all()
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario)
    dados = {'eventos': evento}
    return render(request, 'agenda/agenda.html', dados)
