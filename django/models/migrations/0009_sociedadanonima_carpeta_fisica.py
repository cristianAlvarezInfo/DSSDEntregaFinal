# Generated by Django 3.2.7 on 2021-12-07 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0008_auto_20211125_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='sociedadanonima',
            name='carpeta_fisica',
            field=models.TextField(null=True),
        ),
    ]
