# Generated by Django 3.2.7 on 2021-11-25 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0007_alter_sociedadanonima_numero_expediente'),
    ]

    operations = [
        migrations.AddField(
            model_name='sociedadanonima',
            name='hash_estampilla',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='sociedadanonima',
            name='short_hash_estampilla',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='sociedadanonima',
            name='url_qr',
            field=models.TextField(null=True),
        ),
    ]
