from django import forms
from django.forms import NumberInput

from base.models import CustomUser


class AdicionarUsuarioForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'matricula']

    data_admissao = forms.DateField(label='Data Admissão', widget=NumberInput(attrs={'type': 'date'}), required=True)

