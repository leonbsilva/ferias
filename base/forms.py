from django import forms
from django.forms import NumberInput

from base.models import CustomUser, Vacancia


class CustomUserChangeForm(forms.ModelForm):
    data_admissao = forms.DateField(label='Data Admissão', widget=NumberInput(attrs={'type': 'date'}),
                                    required=True)

    matricula = forms.CharField(label="Matrícula", max_length=75, required=True)

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)


class AdicionarUsuarioForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'matricula']

    data_admissao = forms.DateField(label='Data Admissão', widget=NumberInput(attrs={'type': 'date'}), required=True)


class AdicionarFeriasForm(forms.ModelForm):
    data_inicio = forms.DateField(label='Início', widget=NumberInput(attrs={'type': 'date'}), required=True)
    data_fim = forms.DateField(label='Fim', widget=NumberInput(attrs={'type': 'date'}), required=True)

    class Meta:
        model = Vacancia
        fields = ['ano_base', 'data_inicio', 'data_fim']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AdicionarFeriasForm, self).__init__(*args, **kwargs)

    def clean(self):
        data_inicio = self.cleaned_data['data_inicio']
        data_fim = self.cleaned_data['data_fim']
        ano_base = self.cleaned_data['ano_base']
        error_dict = {}
        periodo = (data_fim - data_inicio).days
        if data_inicio > data_fim:
            error_dict['data_inicio'] = forms.ValidationError('Data inicial não pode ser superior a data final.')
        if data_fim < data_inicio:
            error_dict['data_fim'] = forms.ValidationError('Data final não pode ser inferior a data inicial.')
        if periodo < 5:
            if '__all__' not in error_dict:
                error_dict['__all__'] = []
            error_dict['__all__'].append(forms.ValidationError('Período de férias deve ser no mínimo de 5 dias.'))

        ferias = Vacancia.objects.filter(servidor=self.user, ano_base=ano_base, situacao='Deferido')
        dias = 0
        for vacancia in ferias:
            dias += (vacancia.data_fim - vacancia.data_inicio).days

        if dias + periodo > 30:
            if '__all__' not in error_dict:
                error_dict['__all__'] = []
            error_dict['__all__'].append(
                forms.ValidationError('Esse pedido excede o máximo de dias de férias em um mesmo ano base.')
            )

        if error_dict:
            raise forms.ValidationError(error_dict)
        return self.cleaned_data

    def clean_ano_base(self):
        ano_base = self.cleaned_data['ano_base']
        if Vacancia.objects.filter(servidor=self.user, ano_base=ano_base, situacao='Deferido').count() > 2:
            raise forms.ValidationError('Só é permitido três pedidos de férias deferidos em um mesmo ano base.')
        return ano_base


class RevisarFeriasForm(forms.ModelForm):
    situacao = forms.ChoiceField(choices=[
        ('', ''),
        ('Deferido', 'Deferido'),
        ('Indeferido', 'Indeferido'),
    ])
    observacao = forms.CharField(label='Observação', required=False)

    class Meta:
        model = Vacancia
        fields = ['situacao', 'observacao']

    def clean_observacao(self):
        observacao = self.cleaned_data['observacao']
        situacao = self.cleaned_data['situacao']
        if situacao == 'Indeferido' and not observacao:
            raise forms.ValidationError('Observação precisa ser preenchido.')
        return observacao


class ListagemFeriasForm(forms.Form):
    situacao = forms.ChoiceField(label='Situação', choices=[
        ('', ''),
        ('Aguardando avaliação', 'Aguardando avaliação'),
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
    situacao = forms.ChoiceField(label='Situação', choices=[
        ('', ''),
        ('Avaliadas', 'Avaliadas'),
        ('Não avaliadas', 'Não avaliadas'),
        ('Deferido', 'Deferido'),
        ('Indeferido', 'Indeferido'),
    ], required=False, initial='Não avaliadas')

    def search(self, user):
        query = Vacancia.objects.exclude(servidor=user)
        # query = Vacancia.objects.all()
        if self.is_valid():
            servidor = self.cleaned_data['servidor']
            situacao = self.cleaned_data['situacao']

            if situacao:
                if situacao == 'Avaliadas':
                    query = query.filter(situacao__in=['Deferido', 'Indeferido'])
                elif situacao == 'Não avaliadas':
                    query = query.filter(situacao='Aguardando avaliação')
                else:
                    query = query.filter(situacao=situacao)
            if servidor:
                query = query.filter(servidor__username__icontains=servidor)
        if not self.data:
            query = query.filter(situacao='Aguardando avaliação')
        return query.order_by("-data_solicitacao")
