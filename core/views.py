from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse
from django.contrib.auth.models import User


# Create your views here.

# def index_redirect():   AQUI FOI SO UMA MANEIRA DE REDIRECIONAR A PÁGINA QUANDO A URL TA PURA
#    return redirect('/agenda/')

def login_user(request):
    return render(request, 'agenda/login.html')


def logout_user(request):
    logout(request)
    return redirect('/')


def submit_login(request):
    if request.POST:
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            usuario = authenticate(username=username, password=password)
        except Exception:
            raise Http404
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
    try:
        usuario = request.user
        data_atual = datetime.now() - timedelta(hours=1)
        evento = Evento.objects.filter(usuario=usuario,
                                       data_evento__gt=data_atual)
        dados = {'eventos': evento}
    except Exception:
        raise Http404
    return render(request, 'agenda/agenda.html', dados)


@login_required(login_url='/login/')
def eventos(request):
    try:
        id_evento = request.GET.get('id')
        dados = {}
    except Exception:
        raise Http404
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'agenda/eventos.html', dados)


@login_required(login_url='/login/')
def submit_eventos(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        local = request.POST.get('local')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento')
        if id_evento:
            try:
                evento = Evento.objects.get(id=id_evento)
            except Exception:
                raise Http404
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.save()
            # Evento.objects.filter(id=id_evento).update(titulo=titulo,
            #                                            local=local,
            #  Outro jeito de fazer                      data_evento=data_evento,
            #                                            descricao=descricao)
            else:
                raise Http404
        else:
            Evento.objects.create(titulo=titulo,
                                  local=local,
                                  data_evento=data_evento,
                                  descricao=descricao,
                                  usuario=usuario)
    return redirect('/')


@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()
    return redirect('/')


# @login_required(login_url='/login/')
# def json_lista_eventos(request):
#     usuario = request.user
#     evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo')
#     return JsonResponse(list(evento), safe=False, json_dumps_params={'ensure_ascii': False})


def json_lista_eventos(request, id_usuario):  # O id_usuario está vindo da url agenda/evento/
    try:
        usuario = User.objects.get(id=id_usuario)
        evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo')
    except Exception:
        raise Http404
    return JsonResponse(list(evento), safe=False, json_dumps_params={'ensure_ascii': False})


@login_required(login_url='/login/')
def historico_eventos(request):
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario)
    dados = {'eventos': evento}
    return render(request, 'agenda/historico.html', dados)
