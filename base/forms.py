from django import forms
from django.forms import NumberInput

from base.models import CustomUser, Vacancia


class AdicionarUsuarioForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'matricula']

    data_admissao = forms.DateField(label='Data Admissão', widget=NumberInput(attrs={'type': 'date'}), required=True)


class AdicionarFeriasForm(forms.ModelForm):
    data_inicio = forms.DateField(label='Início', widget=NumberInput(attrs={'type': 'date'}), required=True)
    data_fim = forms.DateField(label='Fim', widget=NumberInput(attrs={'type': 'date'}), required=True)

    class Meta:
        model = Vacancia
        fields = ['ano_base', 'data_inicio', 'data_fim']


class RevisarFeriasForm(forms.ModelForm):
    situacao = forms.ChoiceField(choices=[
        ('', ''),
        ('Deferido', 'Deferido'),
        ('Indeferido', 'Indeferido'),
    ])

    class Meta:
        model = Vacancia
        fields = ['situacao', 'observacao']


class ListagemFeriasForm(forms.Form):
    situacao = forms.ChoiceField(label='Situação', choices=[
        ('', ''),
        ('Deferido', 'Deferido'),
        ('Indeferido', 'Indeferido'),
    ], required=False)

    def search(self, user):
        query = Vacancia.objects.filter(servidor=user).order_by("data_solicitacao")
        if self.is_valid():
            situacao = self.cleaned_data['situacao']

            if situacao:
                query = query.filter(situacao=situacao)
        return query.order_by("-data_solicitacao")


class ListagemRevisaoFeriasForm(forms.Form):
    servidor = forms.CharField(label='Pesquisar Servidor', required=False)

    def search(self, user):
        query = Vacancia.objects.filter(avaliador__isnull=True, situacao='Aguardando avaliação').exclude(servidor=user)
        # query = Vacancia.objects.all()
        if self.is_valid():
            servidor = self.cleaned_data['servidor']

            if servidor:
                query = query.filter(servidor__username__icontains=servidor)

        return query.order_by("-data_solicitacao")
