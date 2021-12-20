from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from base.forms import AdicionarUsuarioForm, AdicionarFeriasForm
from base.models import Vacancia


def adicionar_usuario(request):
    form = AdicionarUsuarioForm(data=request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/admin/base/customuser/')
    return render(request, 'adicionar_usuario.html', dict(form=form))


def listagem_ferias(request):
    vacancias = Vacancia.objects.filter(servidor=request.user)
    return render(request, 'listagem_ferias.html', dict(vacancias=vacancias))


def adicionar_ferias(request):
    form = AdicionarFeriasForm(data=request.POST or None)
    if form.is_valid():
        ferias = form.save(commit=False)
        ferias.servidor = request.user
        ferias.save()
        return HttpResponseRedirect('/base/listagem_ferias/')
    return render(request, 'adicionar_ferias.html', dict(form=form))
