# Generated by Django 5.0.2 on 2024-04-09 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Predicciones', '0004_partidosentrenamiento_goles_en_contra_ultimos_3_partidos_equipo_local_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='partidosinpredecir',
            name='goles_en_contra_ultimos_3_partidos_equipo_local',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='partidosinpredecir',
            name='goles_en_contra_ultimos_3_partidos_equipo_visitante',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='partidosinpredecir',
            name='goles_en_contra_ultimos_3_partidos_local_siendo_local',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='partidosinpredecir',
            name='goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='partidosinpredecir',
            name='goles_ultimos_3_partidos_equipo_local',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='partidosinpredecir',
            name='goles_ultimos_3_partidos_equipo_visitante',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='partidosinpredecir',
            name='goles_ultimos_3_partidos_local_siendo_local',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='partidosinpredecir',
            name='goles_ultimos_3_partidos_visitante_siendo_visitante',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='partidosinpredecir',
            name='puntos_ultimos_3_partidos_equipo_local',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='partidosinpredecir',
            name='puntos_ultimos_3_partidos_equipo_visitante',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='partidosinpredecir',
            name='puntos_ultimos_3_partidos_local_siendo_local',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='partidosinpredecir',
            name='puntos_ultimos_3_partidos_visitante_siendo_visitante',
            field=models.IntegerField(default=-1),
        ),
    ]