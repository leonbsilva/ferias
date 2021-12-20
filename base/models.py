from datetime import date

from django.conf import settings
from django.contrib.auth.models import Group

# Create your models here.
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import AbstractUser


def pre_save_custom_user(sender, instance, **kwargs):
    if not instance.is_staff:
        instance.is_staff = True
        if not instance.pk:
            instance.set_password('123')


def post_save_custom_user(sender, instance, **kwargs):
    group = Group.objects.filter(name='Servidor')
    if group:
        instance.groups.add(group.first())


class CustomUser(AbstractUser):
    matricula = models.CharField(verbose_name='Matrícula', max_length=30, null=True)
    data_admissao = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.username + ' (' + self.matricula + ')'


pre_save.connect(pre_save_custom_user, sender=CustomUser)
post_save.connect(post_save_custom_user, sender=CustomUser)


class Vacancia(models.Model):
    servidor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vacancias')
    avaliador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='avaliacoes')
    data_inicio = models.DateField(null=False)
    data_fim = models.DateField(null=False)
    data_avaliacao = models.DateField(null=True)
    data_solicitacao = models.DateField()
    ano_base = models.IntegerField(null=False)
    observacao = models.CharField(null=True, max_length=255)
    situacao = models.CharField(null=False, max_length=255)

    class Meta:
        verbose_name = "Férias"
        verbose_name_plural = "Férias"

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.data_solicitacao = date.today()
            self.situacao = 'Aguardando avaliação'
        super().save(*args, **kwargs)
