# Generated by Django 3.2.7 on 2021-11-17 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0002_alter_sociosociedadanonima_sociedad'),
    ]

    operations = [
        migrations.AddField(
            model_name='sociedadanonima',
            name='estado_bonita',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='sociedadanonima',
            name='numero_expediente',
            field=models.IntegerField(null=True),
        ),
    ]
