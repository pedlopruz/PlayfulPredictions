# Generated by Django 5.0.2 on 2024-04-26 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Predicciones', '0014_partidosinpredecir_logo_liga'),
    ]

    operations = [
        migrations.AddField(
            model_name='partidosentrenamiento',
            name='escudo_local',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='partidosentrenamiento',
            name='escudo_visitante',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='partidosentrenamiento',
            name='logo_liga',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]