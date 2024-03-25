from django.shortcuts import render
from .populateDB import populateDatabaseEntrenamiento, populateDatabaseReal, populateDatabaseSinPredecir
from .models import PartidosEntrenamiento, PartidoReal, PartidoSinPredecir
from django.http import HttpResponse
import csv
import codecs
from django.utils.encoding import smart_str
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix
import numpy as np
from tabulate import tabulate
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


def entrenamientoModeloBayes(request):
    partidos = PartidosEntrenamiento.objects.all()
    equipos_locales = [partido.equipo_local for partido in partidos]
    equipos_visitantes = [partido.equipo_visitante for partido in partidos]

    todos_los_equipos = list(set(equipos_locales + equipos_visitantes))
    label_encoder = LabelEncoder()
    equipos_encoded = label_encoder.fit_transform(todos_los_equipos)
    equipos_dict = dict(zip(todos_los_equipos, equipos_encoded))
    X_encoded = np.array([[equipos_dict[equipo_local], equipos_dict[equipo_visitante]] for equipo_local, equipo_visitante in zip(equipos_locales, equipos_visitantes)])

    goles_ultimos_5_partidos_equipos_locales = [partido.goles_ultimos_5_partidos_equipo_local for partido in partidos]
    goles_ultimos_5_partidos_equipos_visitante = [partido.goles_ultimos_5_partidos_equipo_visitante for partido in partidos]
    puntos_ultimos_5_partidos_equipos_locales = [partido.puntos_ultimos_5_partidos_equipo_local for partido in partidos]
    puntos_ultimos_5_partidos_equipos_visitantes = [partido.puntos_ultimos_5_partidos_equipo_visitante for partido in partidos]
    goles_ultimos_5_partidos_locales_siendo_local = [partido.goles_ultimos_5_partidos_local_siendo_local for partido in partidos]
    goles_ultimos_5_partidos_visitantes_siendo_visitante = [partido.goles_ultimos_5_partidos_visitante_siendo_visitante for partido in partidos]
    puntos_ultimos_5_partidos_locales_siendo_local = [partido.puntos_ultimos_5_partidos_local_siendo_local for partido in partidos]
    puntos_ultimos_5_partidos_visitante_siendo_visitantes = [partido.puntos_ultimos_5_partidos_visitante_siendo_visitante for partido in partidos]
    goles_en_contra_ultimos_5_partidos_equipo_locales = [partido.goles_en_contra_ultimos_5_partidos_equipo_local for partido in partidos]
    goles_en_contra_ultimos_5_partidos_equipo_visitantes = [partido.goles_en_contra_ultimos_5_partidos_equipo_visitante for partido in partidos]
    goles_en_contra_ultimos_5_partidos_locales_siendo_local = [partido.goles_en_contra_ultimos_5_partidos_local_siendo_local for partido in partidos]
    goles_en_contra_ultimos_5_partidos_visitantees_siendo_visitante = [partido.goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante for partido in partidos]
    winners = [partido.winner for partido in partidos]
    

    X = np.column_stack((X_encoded,
                        goles_ultimos_5_partidos_equipos_locales, 
                        goles_ultimos_5_partidos_equipos_visitante,
                        puntos_ultimos_5_partidos_equipos_locales,
                        puntos_ultimos_5_partidos_equipos_visitantes,
                        goles_ultimos_5_partidos_locales_siendo_local,
                        goles_ultimos_5_partidos_visitantes_siendo_visitante,
                        puntos_ultimos_5_partidos_locales_siendo_local,
                        puntos_ultimos_5_partidos_visitante_siendo_visitantes,
                        goles_en_contra_ultimos_5_partidos_equipo_locales,
                        goles_en_contra_ultimos_5_partidos_equipo_visitantes,
                        goles_en_contra_ultimos_5_partidos_locales_siendo_local,
                        goles_en_contra_ultimos_5_partidos_visitantees_siendo_visitante))
    Y = np.array(winners)

    X_train, X_test, winner_train, winner_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    model_nv = MultinomialNB()
    model_nv.fit(X_train, winner_train)
    winner_pred = model_nv.predict(X_test)
    labels = ['0', "1", "2"]
    conf_mat_nv = confusion_matrix(winner_test, winner_pred, labels=labels)
    conf_matrix_table = tabulate(conf_mat_nv, headers=labels, showindex=labels, tablefmt='fancy_grid')
    accuracy = accuracy_score(winner_test, winner_pred)
    
    print(conf_matrix_table)
    print(accuracy)

    return render(request, 'predicciones/conjuntoEntrenamiento.html', {"mensaje": accuracy})

def entrenamientoModeloBayesConValidacionCruzada(request):
    partidos = PartidosEntrenamiento.objects.all()
    equipos_locales = [partido.equipo_local for partido in partidos]
    equipos_visitantes = [partido.equipo_visitante for partido in partidos]

    todos_los_equipos = list(set(equipos_locales + equipos_visitantes))
    label_encoder = LabelEncoder()
    equipos_encoded = label_encoder.fit_transform(todos_los_equipos)
    equipos_dict = dict(zip(todos_los_equipos, equipos_encoded))
    X_encoded = np.array([[equipos_dict[equipo_local], equipos_dict[equipo_visitante]] for equipo_local, equipo_visitante in zip(equipos_locales, equipos_visitantes)])

    goles_ultimos_5_partidos_equipos_locales = [partido.goles_ultimos_5_partidos_equipo_local for partido in partidos]
    goles_ultimos_5_partidos_equipos_visitante = [partido.goles_ultimos_5_partidos_equipo_visitante for partido in partidos]
    puntos_ultimos_5_partidos_equipos_locales = [partido.puntos_ultimos_5_partidos_equipo_local for partido in partidos]
    puntos_ultimos_5_partidos_equipos_visitantes = [partido.puntos_ultimos_5_partidos_equipo_visitante for partido in partidos]
    goles_ultimos_5_partidos_locales_siendo_local = [partido.goles_ultimos_5_partidos_local_siendo_local for partido in partidos]
    goles_ultimos_5_partidos_visitantes_siendo_visitante = [partido.goles_ultimos_5_partidos_visitante_siendo_visitante for partido in partidos]
    puntos_ultimos_5_partidos_locales_siendo_local = [partido.puntos_ultimos_5_partidos_local_siendo_local for partido in partidos]
    puntos_ultimos_5_partidos_visitante_siendo_visitantes = [partido.puntos_ultimos_5_partidos_visitante_siendo_visitante for partido in partidos]
    goles_en_contra_ultimos_5_partidos_equipo_locales = [partido.goles_en_contra_ultimos_5_partidos_equipo_local for partido in partidos]
    goles_en_contra_ultimos_5_partidos_equipo_visitantes = [partido.goles_en_contra_ultimos_5_partidos_equipo_visitante for partido in partidos]
    goles_en_contra_ultimos_5_partidos_locales_siendo_local = [partido.goles_en_contra_ultimos_5_partidos_local_siendo_local for partido in partidos]
    goles_en_contra_ultimos_5_partidos_visitantees_siendo_visitante = [partido.goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante for partido in partidos]
    winners = [partido.winner for partido in partidos]
    

    X = np.column_stack((X_encoded,
                        goles_ultimos_5_partidos_equipos_locales, 
                        goles_ultimos_5_partidos_equipos_visitante,
                        puntos_ultimos_5_partidos_equipos_locales,
                        puntos_ultimos_5_partidos_equipos_visitantes,
                        goles_ultimos_5_partidos_locales_siendo_local,
                        goles_ultimos_5_partidos_visitantes_siendo_visitante,
                        puntos_ultimos_5_partidos_locales_siendo_local,
                        puntos_ultimos_5_partidos_visitante_siendo_visitantes,
                        goles_en_contra_ultimos_5_partidos_equipo_locales,
                        goles_en_contra_ultimos_5_partidos_equipo_visitantes,
                        goles_en_contra_ultimos_5_partidos_locales_siendo_local,
                        goles_en_contra_ultimos_5_partidos_visitantees_siendo_visitante))
    Y = np.array(winners)

    model_nv = MultinomialNB()
    scores = cross_val_score(model_nv, X, Y, cv=5)
    
    mean_accuracy = np.mean(scores)
   

    return render(request, 'predicciones/conjuntoEntrenamiento.html', {"mensaje": mean_accuracy})
