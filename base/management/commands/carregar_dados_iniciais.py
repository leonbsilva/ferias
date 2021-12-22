from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('CARREGANDO DADOS INICIAIS')
        grupo_servidor = Group.objects.get_or_create(name='Servidor')
        permission1 = Permission.objects.get(codename='add_vacancia')
        permission2 = Permission.objects.get(codename='view_vacancia')
        grupo_servidor[0].permissions.add(permission1)
        grupo_servidor[0].permissions.add(permission2)
        Group.objects.get_or_create(name='Avaliador')
        print('FEITO!')
