# Generated by Django 2.2 on 2021-03-18 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='footwork',
        ),
        migrations.RemoveField(
            model_name='player',
            name='freethrow',
        ),
        migrations.RemoveField(
            model_name='player',
            name='ic',
        ),
        migrations.RemoveField(
            model_name='player',
            name='imc',
        ),
        migrations.RemoveField(
            model_name='player',
            name='passing',
        ),
        migrations.RemoveField(
            model_name='player',
            name='rebond',
        ),
        migrations.RemoveField(
            model_name='player',
            name='threepts',
        ),
        migrations.RemoveField(
            model_name='player',
            name='twopts',
        ),
        migrations.AddField(
            model_name='player',
            name='postmove',
            field=models.IntegerField(null=True, verbose_name='Mouvement de Poste '),
        ),
        migrations.AddField(
            model_name='player',
            name='shot',
            field=models.IntegerField(null=True, verbose_name='Tir '),
        ),
        migrations.AddField(
            model_name='player',
            name='stars',
            field=models.IntegerField(null=True, verbose_name='Etoiles '),
        ),
        migrations.AddField(
            model_name='player',
            name='straight',
            field=models.IntegerField(null=True, verbose_name='Force '),
        ),
    ]