# Generated by Django 5.0.2 on 2024-04-13 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Predicciones', '0005_partidosinpredecir_goles_en_contra_ultimos_3_partidos_equipo_local_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partidos_Predichos',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('liga', models.CharField(max_length=50)),
                ('jornada', models.CharField(max_length=50)),
                ('temporada', models.CharField(max_length=50)),
                ('equipo_local', models.CharField(max_length=100)),
                ('equipo_visitante', models.CharField(max_length=100)),
                ('goles_ultimos_5_partidos_equipo_local', models.IntegerField(default=-1)),
                ('goles_ultimos_5_partidos_equipo_visitante', models.IntegerField(default=-1)),
                ('puntos_ultimos_5_partidos_equipo_local', models.IntegerField(default=-1)),
                ('puntos_ultimos_5_partidos_equipo_visitante', models.IntegerField(default=-1)),
                ('goles_ultimos_5_partidos_local_siendo_local', models.IntegerField(default=-1)),
                ('goles_ultimos_5_partidos_visitante_siendo_visitante', models.IntegerField(default=-1)),
                ('puntos_ultimos_5_partidos_local_siendo_local', models.IntegerField(default=-1)),
                ('puntos_ultimos_5_partidos_visitante_siendo_visitante', models.IntegerField(default=-1)),
                ('goles_en_contra_ultimos_5_partidos_equipo_local', models.IntegerField(default=-1)),
                ('goles_en_contra_ultimos_5_partidos_equipo_visitante', models.IntegerField(default=-1)),
                ('goles_en_contra_ultimos_5_partidos_local_siendo_local', models.IntegerField(default=-1)),
                ('goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante', models.IntegerField(default=-1)),
                ('goles_ultimos_3_partidos_equipo_local', models.IntegerField(default=-1)),
                ('goles_ultimos_3_partidos_equipo_visitante', models.IntegerField(default=-1)),
                ('puntos_ultimos_3_partidos_equipo_local', models.IntegerField(default=-1)),
                ('puntos_ultimos_3_partidos_equipo_visitante', models.IntegerField(default=-1)),
                ('goles_ultimos_3_partidos_local_siendo_local', models.IntegerField(default=-1)),
                ('goles_ultimos_3_partidos_visitante_siendo_visitante', models.IntegerField(default=-1)),
                ('puntos_ultimos_3_partidos_local_siendo_local', models.IntegerField(default=-1)),
                ('puntos_ultimos_3_partidos_visitante_siendo_visitante', models.IntegerField(default=-1)),
                ('goles_en_contra_ultimos_3_partidos_equipo_local', models.IntegerField(default=-1)),
                ('goles_en_contra_ultimos_3_partidos_equipo_visitante', models.IntegerField(default=-1)),
                ('goles_en_contra_ultimos_3_partidos_local_siendo_local', models.IntegerField(default=-1)),
                ('goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante', models.IntegerField(default=-1)),
                ('winner', models.CharField(blank=True, max_length=1)),
            ],
        ),
    ]
