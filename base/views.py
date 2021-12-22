import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages

# Create your views here.
from base.forms import AdicionarUsuarioForm, AdicionarFeriasForm, RevisarFeriasForm, ListagemRevisaoFeriasForm, \
    ListagemFeriasForm
from base.models import Vacancia


def adicionar_usuario(request):
    form = AdicionarUsuarioForm(data=request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/admin/base/customuser/')
    return render(request, 'adicionar_usuario.html', dict(form=form))


def listagem_ferias(request):
    form = ListagemFeriasForm(data=request.POST or None)

    vacancias = form.search(user=request.user)
    return render(request, 'listagem_ferias.html', dict(vacancias=vacancias, form=form))


def adicionar_ferias(request):
    form = AdicionarFeriasForm(data=request.POST or None, user=request.user)
    if form.is_valid():
        ferias = form.save(commit=False)
        ferias.servidor = request.user
        ferias.save()
        messages.success(request, 'Solicitação de férias cadastrada com sucesso')
        return HttpResponseRedirect('/base/listagem_ferias/')
    return render(request, 'adicionar_ferias.html', dict(form=form))


def listagem_revisao_ferias(request):
    form = ListagemRevisaoFeriasForm(data=request.POST or None)

    vacancias = form.search(user=request.user)
    return render(request, 'listagem_revisao_ferias.html', dict(vacancias=vacancias, form=form))


def revisar_ferias(request, vacation_id):
    form = RevisarFeriasForm(data=request.POST or None)
    ferias = get_object_or_404(Vacancia, pk=vacation_id)
    if form.is_valid():
        ferias.avaliador = request.user
        ferias.observacao = form.cleaned_data['observacao']
        ferias.situacao = form.cleaned_data['situacao']
        ferias.data_avaliacao = datetime.datetime.now()
        ferias.save()
        messages.success(request, 'Solicitação de Férias avaliada com sucesso')
        return HttpResponseRedirect('/base/listagem_revisao_ferias')
    return render(request, 'revisar_ferias.html', dict(form=form))
