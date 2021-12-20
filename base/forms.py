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


