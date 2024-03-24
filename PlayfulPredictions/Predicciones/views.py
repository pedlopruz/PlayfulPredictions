from django.shortcuts import render
from .populateDB import populateDatabaseEntrenamiento, populateDatabaseReal, populateDatabaseSinPredecir
from .models import PartidosEntrenamiento, PartidoReal, PartidoSinPredecir
from django.http import HttpResponse
import csv
import codecs
from django.utils.encoding import smart_str
# Create your views here.
def cargar_Datos_Entrenamiento(request):
    if populateDatabaseEntrenamiento():
        populateDatabaseEntrenamiento()
        partidos_entrenamiento = PartidosEntrenamiento.objects.all().count()
        mensaje = "Se ha creado %d partidos entrenamiento" % (partidos_entrenamiento)
    else: 
        mensaje = "No funciona"
    return render(request, 'predicciones/conjuntoEntrenamiento.html', {"mensaje": mensaje})

def cargar_Datos_Real(request):
    if populateDatabaseReal():
        populateDatabaseReal()
        partidos_real = PartidoReal.objects.all().count()
        mensaje = "Se ha creado %d partidos real" % (partidos_real)
    else: 
        mensaje = "No funciona"
    return render(request, 'predicciones/conjuntoEntrenamiento.html', {"mensaje": mensaje})

def cargar_Datos_Sin_Predecir(request):
    if populateDatabaseSinPredecir():
        populateDatabaseSinPredecir()
        partidos_real = PartidoSinPredecir.objects.all().count()
        mensaje = "Se ha creado %d partidos sin predecir" % (partidos_real)
    else: 
        mensaje = "No funciona"
    return render(request, 'predicciones/conjuntoEntrenamiento.html', {"mensaje": mensaje})

def eliminarPartidodeEntrenamiento(request):
    partidos_con_falta = PartidosEntrenamiento.objects.filter(falta=True)
    
    # Eliminar los partidos con falta=True
    for partido in partidos_con_falta:
        partido.delete()
    
    return HttpResponse("Partidos Incorrectos Eliminados")

def eliminarPartidoSinPredecir(request):
    partidos_con_falta = PartidoSinPredecir.objects.filter(falta=True)
    
    # Eliminar los partidos con falta=True
    for partido in partidos_con_falta:
        partido.delete()
    
    return HttpResponse("Partidos Sin Predecir Incorrectos Eliminados")


def PartidoEntrenamientoExportToCsv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="Partido_EntrenamientoV2.csv"'

    # Open the CSV file with UTF-8 encoding
    response.write(codecs.BOM_UTF8)

    # Create a CSV writer object
    writer = csv.writer(response, csv.excel)

    # Write the header row
    writer.writerow(
        [
            smart_str("id"),
            smart_str("League"),
            smart_str("Season"),
            smart_str("Jornada"),
            smart_str("Home Team"),
            smart_str("Away Team"),
            smart_str("Home Goals"),
            smart_str("Away Goals"),
            smart_str("Home Points"),
            smart_str("Away Points"),
            smart_str("goles_ultimos_5_partidos_equipo_local"),
            smart_str("goles_ultimos_5_partidos_equipo_visitante"),
            smart_str("puntos_ultimos_5_partidos_equipo_local"),
            smart_str("puntos_ultimos_5_partidos_equipo_visitante"),
            smart_str("goles_ultimos_5_partidos_local_siendo_local"),
            smart_str("goles_ultimos_5_partidos_visitante_siendo_visitante"),
            smart_str("puntos_ultimos_5_partidos_local_siendo_local"),
            smart_str("puntos_ultimos_5_partidos_visitante_siendo_visitante"),
            smart_str("goles_en_contra_ultimos_5_partidos_equipo_local"),
            smart_str("goles_en_contra_ultimos_5_partidos_equipo_visitante"),
            smart_str("goles_en_contra_ultimos_5_partidos_local_siendo_local"),
            smart_str("goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante"),
            smart_str("falta"),
            smart_str("Winner")
        ]
    )

    # Retrieve data from your model
    queryset = PartidosEntrenamiento.objects.all()

    # Write data rows
    for p in queryset:
        writer.writerow(
            [
                smart_str(p.id),
                smart_str(p.liga),
                smart_str(p.temporada),
                smart_str(p.jornada),
                smart_str(p.equipo_local),
                smart_str(p.equipo_visitante),
                smart_str(p.goles_local),
                smart_str(p.goles_visitante),
                smart_str(p.puntos_local),
                smart_str(p.puntos_visitante),
                smart_str(p.goles_ultimos_5_partidos_equipo_local),
                smart_str(p.goles_ultimos_5_partidos_equipo_visitante),
                smart_str(p.puntos_ultimos_5_partidos_equipo_local),
                smart_str(p.puntos_ultimos_5_partidos_equipo_visitante),
                smart_str(p.goles_ultimos_5_partidos_local_siendo_local),
                smart_str(p.goles_ultimos_5_partidos_visitante_siendo_visitante),
                smart_str(p.puntos_ultimos_5_partidos_local_siendo_local),
                smart_str(p.puntos_ultimos_5_partidos_visitante_siendo_visitante),
                smart_str(p.goles_en_contra_ultimos_5_partidos_equipo_local),
                smart_str(p.goles_en_contra_ultimos_5_partidos_equipo_visitante),
                smart_str(p.goles_en_contra_ultimos_5_partidos_local_siendo_local),
                smart_str(p.goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante),
                smart_str(p.falta),
                smart_str(p.winner)
            ]
        )

    return response
