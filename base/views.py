from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from base.forms import AdicionarUsuarioForm


def adicionar_usuario(request):
    form = AdicionarUsuarioForm(data=request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/admin/base/customuser/')
    return render(request, 'adicionar_usuario.html', dict(form=form))
