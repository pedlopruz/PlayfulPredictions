# Generated by Django 5.0.2 on 2024-04-26 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Predicciones', '0013_partidospredichos_logo_liga'),
    ]

    operations = [
        migrations.AddField(
            model_name='partidosinpredecir',
            name='logo_liga',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
