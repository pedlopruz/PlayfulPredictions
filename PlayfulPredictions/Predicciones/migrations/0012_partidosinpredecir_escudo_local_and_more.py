# Generated by Django 5.0.2 on 2024-04-26 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Predicciones', '0011_porra'),
    ]

    operations = [
        migrations.AddField(
            model_name='partidosinpredecir',
            name='escudo_local',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='partidosinpredecir',
            name='escudo_visitante',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='partidospredichos',
            name='escudo_local',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='partidospredichos',
            name='escudo_visitante',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]