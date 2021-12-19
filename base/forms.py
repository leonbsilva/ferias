from django import forms
from base.models import CustomUser


class AdicionarUsuarioForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'matricula']
