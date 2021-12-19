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


pre_save.connect(pre_save_custom_user, sender=CustomUser)
post_save.connect(post_save_custom_user, sender=CustomUser)
