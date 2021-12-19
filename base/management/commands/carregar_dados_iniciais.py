from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('CARREGANDO DADOS INICIAIS')
        Group.objects.get_or_create(name='Servidor')
        Group.objects.get_or_create(name='Avaliador')
        print('FEITO!')
