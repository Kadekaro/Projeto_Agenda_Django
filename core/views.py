from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth import authenticate, login, logout


# Create your views here.

# def index_redirect():       AQUI FOI SO UMA MANEIRA DE REDIRECIONAR A PÁGINA QUANDO A URL TA PURA
#    return redirect('/agenda/')

def login_user(request):
    return render(request, 'agenda/login.html')


def logout_user(request):
    logout(request)
    return redirect('/')


def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou senha inválida!")
    return redirect('/')


@login_required(login_url='/login/')
def lista_eventos(request):
    # evento = Evento.objects.get(id=1)
    # evento = Evento.objects.all()
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario)
    dados = {'eventos': evento}
    return render(request, 'agenda/agenda.html', dados)


@login_required(login_url='/login/')
def eventos(request):
    return render(request, 'agenda/eventos.html')


@login_required(login_url='/login/')
def submit_eventos(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        Evento.objects.create(titulo=titulo,
                              data_evento=data_evento,
                              descricao=descricao,
                              usuario=usuario)
    return redirect('/')
