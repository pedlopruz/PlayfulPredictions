# Generated by Django 5.0.2 on 2024-04-17 09:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Predicciones', '0009_porra'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiniela',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('abierta', models.BooleanField(default=True)),
                ('cuarto_partido', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cuarto_partido', to='Predicciones.partidospredichos')),
                ('decimo_partido', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='decimo_partido', to='Predicciones.partidospredichos')),
                ('noveno_partido', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='noveno_partido', to='Predicciones.partidospredichos')),
                ('octavo_partido', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='octavo_partido', to='Predicciones.partidospredichos')),
                ('primer_partido', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='primer_partido', to='Predicciones.partidospredichos')),
                ('quinto_partido', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='quinto_partido', to='Predicciones.partidospredichos')),
                ('segundo_partido', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='segundo_partido', to='Predicciones.partidospredichos')),
                ('septimo_partido', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='septimo_partido', to='Predicciones.partidospredichos')),
                ('sexto_partido', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sexto_partido', to='Predicciones.partidospredichos')),
                ('tercer_partido', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tercer_partido', to='Predicciones.partidospredichos')),
            ],
        ),
        migrations.DeleteModel(
            name='Porra',
        ),
    ]
