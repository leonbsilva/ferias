# Generated by Django 3.2.9 on 2021-12-23 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_vacancia_observacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='data_admissao',
            field=models.DateField(verbose_name='Data de Admissão'),
        ),
    ]
