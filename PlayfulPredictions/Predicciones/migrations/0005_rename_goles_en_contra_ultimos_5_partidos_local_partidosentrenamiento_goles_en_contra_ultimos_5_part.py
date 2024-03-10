# Generated by Django 5.0.2 on 2024-03-10 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Predicciones', '0004_partidosentrenamiento_goles_en_contra_ultimos_5_partidos_local_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='partidosentrenamiento',
            old_name='goles_en_contra_ultimos_5_partidos_local',
            new_name='goles_en_contra_ultimos_5_partidos_equipo_local',
        ),
        migrations.RenameField(
            model_name='partidosentrenamiento',
            old_name='goles_en_contra_ultimos_5_partidos_visitante',
            new_name='goles_en_contra_ultimos_5_partidos_equipo_visitante',
        ),
        migrations.RenameField(
            model_name='partidosentrenamiento',
            old_name='goles_ultimos_5_partidos_local',
            new_name='goles_ultimos_5_partidos_equipo_local',
        ),
        migrations.RenameField(
            model_name='partidosentrenamiento',
            old_name='goles_ultimos_5_partidos_visitante',
            new_name='goles_ultimos_5_partidos_equipo_visitante',
        ),
        migrations.RenameField(
            model_name='partidosentrenamiento',
            old_name='puntos_ultimos_5_partidos_local',
            new_name='puntos_ultimos_5_partidos_equipo_local',
        ),
    ]
