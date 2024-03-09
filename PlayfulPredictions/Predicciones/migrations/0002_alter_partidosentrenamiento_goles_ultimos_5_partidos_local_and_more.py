# Generated by Django 5.0.2 on 2024-03-09 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Predicciones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partidosentrenamiento',
            name='goles_ultimos_5_partidos_local',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='partidosentrenamiento',
            name='goles_ultimos_5_partidos_local_siendo_local',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='partidosentrenamiento',
            name='goles_ultimos_5_partidos_visitante',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='partidosentrenamiento',
            name='goles_ultimos_5_partidos_visitante_siendo_visitante',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='partidosentrenamiento',
            name='puntos_ultimos_5_partidos_local',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='partidosentrenamiento',
            name='puntos_ultimos_5_partidos_local_siendo_local',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='partidosentrenamiento',
            name='puntos_ultimos_5_partidos_visitante',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='partidosentrenamiento',
            name='puntos_ultimos_5_partidos_visitante_siendo_visitante',
            field=models.IntegerField(default=-1),
        ),
    ]
