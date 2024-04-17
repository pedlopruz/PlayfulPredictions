from django.db import models

# Create your models here.


class PartidosEntrenamiento(models.Model):
    id = models.IntegerField(primary_key=True)
    liga = models.CharField(max_length=50)
    temporada = models.CharField(max_length=50)
    jornada = models.IntegerField(default=0)
    equipo_local = models.CharField(max_length=100)
    equipo_visitante = models.CharField(max_length=100)
    goles_local = models.IntegerField()
    goles_visitante = models.IntegerField()
    puntos_local = models.IntegerField()
    puntos_visitante = models.IntegerField()
    goles_ultimos_5_partidos_equipo_local = models.IntegerField(default = -1)
    goles_ultimos_5_partidos_equipo_visitante = models.IntegerField(default = -1)
    puntos_ultimos_5_partidos_equipo_local = models.IntegerField(default = -1)
    puntos_ultimos_5_partidos_equipo_visitante = models.IntegerField(default = -1)
    goles_ultimos_5_partidos_local_siendo_local = models.IntegerField(default = -1)
    goles_ultimos_5_partidos_visitante_siendo_visitante = models.IntegerField(default = -1)
    puntos_ultimos_5_partidos_local_siendo_local = models.IntegerField(default = -1)
    puntos_ultimos_5_partidos_visitante_siendo_visitante = models.IntegerField(default = -1)
    goles_en_contra_ultimos_5_partidos_equipo_local = models.IntegerField(default = -1)
    goles_en_contra_ultimos_5_partidos_equipo_visitante = models.IntegerField(default = -1)
    goles_en_contra_ultimos_5_partidos_local_siendo_local = models.IntegerField(default = -1)
    goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante = models.IntegerField(default = -1)
    
    goles_ultimos_3_partidos_equipo_local = models.IntegerField(default = -1)
    goles_ultimos_3_partidos_equipo_visitante = models.IntegerField(default = -1)
    puntos_ultimos_3_partidos_equipo_local = models.IntegerField(default = -1)
    puntos_ultimos_3_partidos_equipo_visitante = models.IntegerField(default = -1)
    goles_ultimos_3_partidos_local_siendo_local = models.IntegerField(default = -1)
    goles_ultimos_3_partidos_visitante_siendo_visitante = models.IntegerField(default = -1)
    puntos_ultimos_3_partidos_local_siendo_local = models.IntegerField(default = -1)
    puntos_ultimos_3_partidos_visitante_siendo_visitante = models.IntegerField(default = -1)
    goles_en_contra_ultimos_3_partidos_equipo_local = models.IntegerField(default = -1)
    goles_en_contra_ultimos_3_partidos_equipo_visitante = models.IntegerField(default = -1)
    goles_en_contra_ultimos_3_partidos_local_siendo_local = models.IntegerField(default = -1)
    goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante = models.IntegerField(default = -1)
    falta = models.BooleanField(default = False)
    winner = models.CharField(max_length = 1)
    def __str__(self):
        return str(self.jornada)
    

class PartidoReal(models.Model):
    id = models.IntegerField(primary_key=True)
    liga = models.CharField(max_length=50)
    jornada = models.IntegerField()
    temporada = models.CharField(max_length=50)
    equipo_local = models.CharField(max_length=100)
    equipo_visitante = models.CharField(max_length=100)
    goles_local = models.IntegerField(default = -1)
    goles_visitante = models.IntegerField(default = -1)
    puntos_local = models.IntegerField(default = -1)
    puntos_visitante = models.IntegerField(default = -1)
    winner = models.CharField(max_length = 1, blank = True)
    def __str__(self):
        return self.liga
    
class PartidoSinPredecir(models.Model):
    id = models.IntegerField(primary_key=True)
    liga = models.CharField(max_length=50)
    jornada = models.IntegerField()
    temporada = models.CharField(max_length=50)
    equipo_local = models.CharField(max_length=100)
    equipo_visitante = models.CharField(max_length=100)
    goles_ultimos_5_partidos_equipo_local = models.IntegerField(default = -1)
    goles_ultimos_5_partidos_equipo_visitante = models.IntegerField(default = -1)
    puntos_ultimos_5_partidos_equipo_local = models.IntegerField(default = -1)
    puntos_ultimos_5_partidos_equipo_visitante = models.IntegerField(default = -1)
    goles_ultimos_5_partidos_local_siendo_local = models.IntegerField(default = -1)
    goles_ultimos_5_partidos_visitante_siendo_visitante = models.IntegerField(default = -1)
    puntos_ultimos_5_partidos_local_siendo_local = models.IntegerField(default = -1)
    puntos_ultimos_5_partidos_visitante_siendo_visitante = models.IntegerField(default = -1)
    goles_en_contra_ultimos_5_partidos_equipo_local = models.IntegerField(default = -1)
    goles_en_contra_ultimos_5_partidos_equipo_visitante = models.IntegerField(default = -1)
    goles_en_contra_ultimos_5_partidos_local_siendo_local = models.IntegerField(default = -1)
    goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante = models.IntegerField(default = -1)
    
    goles_ultimos_3_partidos_equipo_local = models.IntegerField(default = -1)
    goles_ultimos_3_partidos_equipo_visitante = models.IntegerField(default = -1)
    puntos_ultimos_3_partidos_equipo_local = models.IntegerField(default = -1)
    puntos_ultimos_3_partidos_equipo_visitante = models.IntegerField(default = -1)
    goles_ultimos_3_partidos_local_siendo_local = models.IntegerField(default = -1)
    goles_ultimos_3_partidos_visitante_siendo_visitante = models.IntegerField(default = -1)
    puntos_ultimos_3_partidos_local_siendo_local = models.IntegerField(default = -1)
    puntos_ultimos_3_partidos_visitante_siendo_visitante = models.IntegerField(default = -1)
    goles_en_contra_ultimos_3_partidos_equipo_local = models.IntegerField(default = -1)
    goles_en_contra_ultimos_3_partidos_equipo_visitante = models.IntegerField(default = -1)
    goles_en_contra_ultimos_3_partidos_local_siendo_local = models.IntegerField(default = -1)
    goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante = models.IntegerField(default = -1)
    falta = models.BooleanField(default = False)
    def __str__(self):
        return f"Partido: {self.equipo_local} vs {self.equipo_visitante}"
    
class PartidosPredichos(models.Model):
    id = models.IntegerField(primary_key=True)
    liga = models.CharField(max_length=50)
    jornada = models.IntegerField()
    temporada = models.CharField(max_length=50)
    equipo_local = models.CharField(max_length=100)
    equipo_visitante = models.CharField(max_length=100)
    goles_ultimos_5_partidos_equipo_local = models.IntegerField(default = -1)
    goles_ultimos_5_partidos_equipo_visitante = models.IntegerField(default = -1)
    puntos_ultimos_5_partidos_equipo_local = models.IntegerField(default = -1)
    puntos_ultimos_5_partidos_equipo_visitante = models.IntegerField(default = -1)
    goles_ultimos_5_partidos_local_siendo_local = models.IntegerField(default = -1)
    goles_ultimos_5_partidos_visitante_siendo_visitante = models.IntegerField(default = -1)
    puntos_ultimos_5_partidos_local_siendo_local = models.IntegerField(default = -1)
    puntos_ultimos_5_partidos_visitante_siendo_visitante = models.IntegerField(default = -1)
    goles_en_contra_ultimos_5_partidos_equipo_local = models.IntegerField(default = -1)
    goles_en_contra_ultimos_5_partidos_equipo_visitante = models.IntegerField(default = -1)
    goles_en_contra_ultimos_5_partidos_local_siendo_local = models.IntegerField(default = -1)
    goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante = models.IntegerField(default = -1)
    
    goles_ultimos_3_partidos_equipo_local = models.IntegerField(default = -1)
    goles_ultimos_3_partidos_equipo_visitante = models.IntegerField(default = -1)
    puntos_ultimos_3_partidos_equipo_local = models.IntegerField(default = -1)
    puntos_ultimos_3_partidos_equipo_visitante = models.IntegerField(default = -1)
    goles_ultimos_3_partidos_local_siendo_local = models.IntegerField(default = -1)
    goles_ultimos_3_partidos_visitante_siendo_visitante = models.IntegerField(default = -1)
    puntos_ultimos_3_partidos_local_siendo_local = models.IntegerField(default = -1)
    puntos_ultimos_3_partidos_visitante_siendo_visitante = models.IntegerField(default = -1)
    goles_en_contra_ultimos_3_partidos_equipo_local = models.IntegerField(default = -1)
    goles_en_contra_ultimos_3_partidos_equipo_visitante = models.IntegerField(default = -1)
    goles_en_contra_ultimos_3_partidos_local_siendo_local = models.IntegerField(default = -1)
    goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante = models.IntegerField(default = -1)
    winner = models.CharField(max_length = 1, blank = True)
    def __str__(self):
        return f"Partido: {self.equipo_local} vs {self.equipo_visitante}, Jornada {self.jornada} y Liga {self.liga}"
    
class Quiniela(models.Model):
    id = models.AutoField(primary_key=True)
    primer_partido = models.ForeignKey(PartidosPredichos, on_delete=models.PROTECT, related_name='primer_partido')
    segundo_partido = models.ForeignKey(PartidosPredichos, on_delete=models.PROTECT,related_name='segundo_partido')
    tercer_partido = models.ForeignKey(PartidosPredichos, on_delete=models.PROTECT,related_name='tercer_partido')
    cuarto_partido = models.ForeignKey(PartidosPredichos, on_delete=models.PROTECT, related_name='cuarto_partido')
    quinto_partido = models.ForeignKey(PartidosPredichos, on_delete=models.PROTECT,related_name='quinto_partido')
    sexto_partido = models.ForeignKey(PartidosPredichos, on_delete=models.PROTECT,related_name='sexto_partido')
    septimo_partido = models.ForeignKey(PartidosPredichos, on_delete=models.PROTECT, related_name='septimo_partido')
    octavo_partido = models.ForeignKey(PartidosPredichos, on_delete=models.PROTECT,related_name='octavo_partido')
    noveno_partido = models.ForeignKey(PartidosPredichos, on_delete=models.PROTECT,related_name='noveno_partido')
    decimo_partido = models.ForeignKey(PartidosPredichos, on_delete=models.PROTECT, related_name='decimo_partido')
    abierta = models.BooleanField(default=True)

    def __str__(self):
        return str(self.abierta)





