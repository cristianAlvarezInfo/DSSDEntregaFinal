# Generated by Django 3.2.7 on 2021-11-16 01:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sociosociedadanonima',
            name='sociedad',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='socios', to='models.sociedadanonima'),
        ),
    ]
