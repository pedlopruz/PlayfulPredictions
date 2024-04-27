from django.shortcuts import render, redirect
from .populateDB import populateDatabaseEntrenamiento, populateDatabaseSinPredecir, cargar_Imagenes_Equipos_Entrenamiento
from .models import *
from Autenticacion.models import CustomUser
from django.http import HttpResponse
import csv
import codecs
from django.utils.encoding import smart_str
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from tabulate import tabulate
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from django.core.paginator import Paginator, PageNotAnInteger
from django.http import Http404
from .forms import *
from django.urls import reverse
from django.db.models import Q
from django.db.models import Max, Min
from django.core.mail import EmailMessage

# Create your views here.
def cargar_Datos_Entrenamiento(request):
    if populateDatabaseEntrenamiento():
        populateDatabaseEntrenamiento()
        partidos_entrenamiento = PartidosEntrenamiento.objects.all().count()
        mensaje = "Se ha creado %d partidos entrenamiento" % (partidos_entrenamiento)
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

def cargar_Partido_Entrenamiento_V2(request):
    PartidosEntrenamiento.objects.all().delete()
    path3 = "data/Partido_Entrenamiento.csv"
    with open(path3, newline='', encoding='utf-8-sig') as csvfile:
        lector_csv = csv.DictReader(csvfile, delimiter=';')
        for numero_fila, fila in enumerate(lector_csv, start=1):
            try:
                id = fila['id']
                league = fila['League']
                season = fila['Season']
                jornada = fila['Jornada']
                home_team = fila['Home Team']
                away_team = fila['Away Team']
                home_goals = fila['Home Goals']
                away_goals = fila['Away Goals']
                home_points = fila['Home Points']
                away_points = fila['Away Points']
                goles_ultimos_5_partidos_equipo_local = fila['goles_ultimos_5_partidos_equipo_local']
                goles_ultimos_5_partidos_equipo_visitante = fila['goles_ultimos_5_partidos_equipo_visitante']
                puntos_ultimos_5_partidos_equipo_local = fila['puntos_ultimos_5_partidos_equipo_local']
                puntos_ultimos_5_partidos_equipo_visitante = fila['puntos_ultimos_5_partidos_equipo_visitante']
                goles_ultimos_5_partidos_local_siendo_local = fila['goles_ultimos_5_partidos_local_siendo_local']
                goles_ultimos_5_partidos_visitante_siendo_visitante = fila['goles_ultimos_5_partidos_visitante_siendo_visitante']
                puntos_ultimos_5_partidos_local_siendo_local = fila['puntos_ultimos_5_partidos_local_siendo_local']
                puntos_ultimos_5_partidos_visitante_siendo_visitante = fila['puntos_ultimos_5_partidos_visitante_siendo_visitante']
                goles_en_contra_ultimos_5_partidos_equipo_local = fila['goles_en_contra_ultimos_5_partidos_equipo_local']
                goles_en_contra_ultimos_5_partidos_equipo_visitante = fila['goles_en_contra_ultimos_5_partidos_equipo_visitante']
                goles_en_contra_ultimos_5_partidos_local_siendo_local = fila['goles_en_contra_ultimos_5_partidos_local_siendo_local']
                goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante = fila['goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante']

                goles_ultimos_3_partidos_equipo_local = fila['goles_ultimos_3_partidos_equipo_local']
                goles_ultimos_3_partidos_equipo_visitante = fila['goles_ultimos_3_partidos_equipo_visitante']
                puntos_ultimos_3_partidos_equipo_local = fila['puntos_ultimos_3_partidos_equipo_local']
                puntos_ultimos_3_partidos_equipo_visitante = fila['puntos_ultimos_3_partidos_equipo_visitante']
                goles_ultimos_3_partidos_local_siendo_local = fila['goles_ultimos_3_partidos_local_siendo_local']
                goles_ultimos_3_partidos_visitante_siendo_visitante = fila['goles_ultimos_3_partidos_visitante_siendo_visitante']
                puntos_ultimos_3_partidos_local_siendo_local = fila['puntos_ultimos_3_partidos_local_siendo_local']
                puntos_ultimos_3_partidos_visitante_siendo_visitante = fila['puntos_ultimos_3_partidos_visitante_siendo_visitante']
                goles_en_contra_ultimos_3_partidos_equipo_local = fila['goles_en_contra_ultimos_3_partidos_equipo_local']
                goles_en_contra_ultimos_3_partidos_equipo_visitante = fila['goles_en_contra_ultimos_3_partidos_equipo_visitante']
                goles_en_contra_ultimos_3_partidos_local_siendo_local = fila['goles_en_contra_ultimos_3_partidos_local_siendo_local']
                goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante = fila['goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante']
                falta = fila['falta']
                winner = fila['Winner']
                PartidosEntrenamiento.objects.create(id = id, liga=league, temporada=season, jornada=jornada,
                                                          equipo_local=home_team, equipo_visitante=away_team, goles_local=home_goals, 
                                                          goles_visitante=away_goals, puntos_local=home_points, puntos_visitante=away_points,
                                                          goles_ultimos_5_partidos_equipo_local = goles_ultimos_5_partidos_equipo_local,
                                                          goles_ultimos_5_partidos_equipo_visitante = goles_ultimos_5_partidos_equipo_visitante,
                                                          puntos_ultimos_5_partidos_equipo_local = puntos_ultimos_5_partidos_equipo_local,
                                                          puntos_ultimos_5_partidos_equipo_visitante = puntos_ultimos_5_partidos_equipo_visitante,
                                                            goles_ultimos_5_partidos_local_siendo_local = goles_ultimos_5_partidos_local_siendo_local,
                                                            goles_ultimos_5_partidos_visitante_siendo_visitante = goles_ultimos_5_partidos_visitante_siendo_visitante,
                                                            puntos_ultimos_5_partidos_local_siendo_local = puntos_ultimos_5_partidos_local_siendo_local,
                                                            puntos_ultimos_5_partidos_visitante_siendo_visitante = puntos_ultimos_5_partidos_visitante_siendo_visitante,
                                                            goles_en_contra_ultimos_5_partidos_equipo_local = goles_en_contra_ultimos_5_partidos_equipo_local,
                                                            goles_en_contra_ultimos_5_partidos_equipo_visitante = goles_en_contra_ultimos_5_partidos_equipo_visitante,
                                                            goles_en_contra_ultimos_5_partidos_local_siendo_local = goles_en_contra_ultimos_5_partidos_local_siendo_local,
                                                            goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante = goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante,

                                                            goles_ultimos_3_partidos_equipo_local = goles_ultimos_3_partidos_equipo_local,
                                                            goles_ultimos_3_partidos_equipo_visitante = goles_ultimos_3_partidos_equipo_visitante,
                                                            puntos_ultimos_3_partidos_equipo_local = puntos_ultimos_3_partidos_equipo_local,
                                                            puntos_ultimos_3_partidos_equipo_visitante = puntos_ultimos_3_partidos_equipo_visitante,
                                                            goles_ultimos_3_partidos_local_siendo_local = goles_ultimos_3_partidos_local_siendo_local,
                                                            goles_ultimos_3_partidos_visitante_siendo_visitante = goles_ultimos_3_partidos_visitante_siendo_visitante,
                                                            puntos_ultimos_3_partidos_local_siendo_local = puntos_ultimos_3_partidos_local_siendo_local,
                                                            puntos_ultimos_3_partidos_visitante_siendo_visitante = puntos_ultimos_3_partidos_visitante_siendo_visitante,
                                                            goles_en_contra_ultimos_3_partidos_equipo_local = goles_en_contra_ultimos_3_partidos_equipo_local,
                                                            goles_en_contra_ultimos_3_partidos_equipo_visitante = goles_en_contra_ultimos_3_partidos_equipo_visitante,
                                                            goles_en_contra_ultimos_3_partidos_local_siendo_local = goles_en_contra_ultimos_3_partidos_local_siendo_local,
                                                            goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante = goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante,
                                                            falta = falta,

                                                          winner=winner)
                
                
            except Exception as e:
                print(f"Error en la fila {numero_fila}: {e}")
                # Opcional: Puedes añadir más información de la fila si es necesario
                print(f"Contenido de la fila {numero_fila}: {fila}")
        cargar_Imagenes_Equipos_Entrenamiento()
    return HttpResponse("Todo Ok")


def PartidoEntrenamientoExportToCsv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="Partido_EntrenamientoV3sineliminar.csv"'

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
            
            smart_str("goles_ultimos_3_partidos_equipo_local"),
            smart_str("goles_ultimos_3_partidos_equipo_visitante"),
            smart_str("puntos_ultimos_3_partidos_equipo_local"),
            smart_str("puntos_ultimos_3_partidos_equipo_visitante"),
            smart_str("goles_ultimos_3_partidos_local_siendo_local"),
            smart_str("goles_ultimos_3_partidos_visitante_siendo_visitante"),
            smart_str("puntos_ultimos_3_partidos_local_siendo_local"),
            smart_str("puntos_ultimos_3_partidos_visitante_siendo_visitante"),
            smart_str("goles_en_contra_ultimos_3_partidos_equipo_local"),
            smart_str("goles_en_contra_ultimos_3_partidos_equipo_visitante"),
            smart_str("goles_en_contra_ultimos_3_partidos_local_siendo_local"),
            smart_str("goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante"),
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
                smart_str(p.goles_ultimos_3_partidos_equipo_local),
                smart_str(p.goles_ultimos_3_partidos_equipo_visitante),
                smart_str(p.puntos_ultimos_3_partidos_equipo_local),
                smart_str(p.puntos_ultimos_3_partidos_equipo_visitante),
                smart_str(p.goles_ultimos_3_partidos_local_siendo_local),
                smart_str(p.goles_ultimos_3_partidos_visitante_siendo_visitante),
                smart_str(p.puntos_ultimos_3_partidos_local_siendo_local),
                smart_str(p.puntos_ultimos_3_partidos_visitante_siendo_visitante),
                smart_str(p.goles_en_contra_ultimos_3_partidos_equipo_local),
                smart_str(p.goles_en_contra_ultimos_3_partidos_equipo_visitante),
                smart_str(p.goles_en_contra_ultimos_3_partidos_local_siendo_local),
                smart_str(p.goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante),
                smart_str(p.falta),
                smart_str(p.winner)
            ]
        )

    return response

def calculo_Valores_Indp_Y_Depen_Para_Datos_5_Ultimos_Partidos():
    partidos = PartidosEntrenamiento.objects.all()

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
    

    X = np.column_stack((
                        goles_ultimos_5_partidos_equipos_locales, 
                        goles_ultimos_5_partidos_equipos_visitante,
                        puntos_ultimos_5_partidos_equipos_locales,
                        puntos_ultimos_5_partidos_equipos_visitantes,
                        goles_en_contra_ultimos_5_partidos_equipo_locales,
                        goles_en_contra_ultimos_5_partidos_equipo_visitantes,
                        goles_ultimos_5_partidos_locales_siendo_local,
                        goles_ultimos_5_partidos_visitantes_siendo_visitante,
                        puntos_ultimos_5_partidos_locales_siendo_local,
                        puntos_ultimos_5_partidos_visitante_siendo_visitantes,
                        goles_en_contra_ultimos_5_partidos_locales_siendo_local,
                        goles_en_contra_ultimos_5_partidos_visitantees_siendo_visitante))
    Y = np.array(winners)
    return X, Y


def entrenamiento_Modelo_Bayes_Para_Datos_5_Ultimos_Partidos(request):
    
    X,Y = calculo_Valores_Indp_Y_Depen_Para_Datos_5_Ultimos_Partidos()
    
    X_train, X_test, winner_train, winner_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    model_nv = MultinomialNB()
    model_nv.fit(X_train, winner_train)
    winner_pred = model_nv.predict(X_test)
    labels = ['1', "0", "2"]
    conf_mat_nv = confusion_matrix(winner_test, winner_pred, labels=labels)
    conf_matrix_table = tabulate(conf_mat_nv, headers=labels, showindex=labels, tablefmt='fancy_grid')
    accuracy = accuracy_score(winner_test, winner_pred)
    
    print(conf_matrix_table)
    print(accuracy)

    return render(request, 'predicciones/conjuntoEntrenamiento.html', {"mensaje": accuracy})

def entrenamiento_Modelo_Bayes_Con_Validacion_Cruzada_Para_Datos_5_Ultimos_Partidos(request):

    X,Y = calculo_Valores_Indp_Y_Depen_Para_Datos_5_Ultimos_Partidos()

    model_nv = MultinomialNB()
    scores = cross_val_score(model_nv, X, Y, cv=5)
    
    mean_accuracy = np.mean(scores)
   

    return render(request, 'predicciones/conjuntoEntrenamiento.html', {"mensaje": mean_accuracy})


def entrenamiento_Modelo_KNN_Para_Datos_5_Ultimos_Partidos(request):
    
    X,Y = calculo_Valores_Indp_Y_Depen_Para_Datos_5_Ultimos_Partidos()
    X_train, X_test, winner_train, winner_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    
    #model_knn = KNeighborsClassifier(n_neighbors=300, metric='manhattan', weights='uniform', algorithm='auto')
    #model_knn = KNeighborsClassifier(n_neighbors=203, metric='euclidean', weights='uniform', algorithm='auto')
    model_knn = KNeighborsClassifier(n_neighbors=203, metric='chebyshev', weights='uniform', algorithm='auto')
    #model_knn = KNeighborsClassifier(n_neighbors=203, metric='minkowski', p=1,weights='uniform', algorithm='auto')
    #model_knn = KNeighborsClassifier(n_neighbors=203, metric='minkowski', p=2,weights='distance', algorithm='brute')
    model_knn.fit(X_train, winner_train)
    winner_pred = model_knn.predict(X_test)
    labels = ['1', "0", "2"]
    conf_mat_nv = confusion_matrix(winner_test, winner_pred, labels=labels)
    conf_matrix_table = tabulate(conf_mat_nv, headers=labels, showindex=labels, tablefmt='fancy_grid')
    accuracy = accuracy_score(winner_test, winner_pred)
    from django.db.models import Q
    
    print(conf_matrix_table)
    print(accuracy)

    return render(request, 'predicciones/conjuntoEntrenamiento.html', {"mensaje": accuracy})


'''def entrenamientoModeloRandomForest(request):
    
    X,Y = calculoValoresIndpYDepen()
    X_train, X_test, winner_train, winner_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    rf = RandomForestClassifier()

# Define la distribución de los hiperparámetros que deseas explorar
    param_dist = {
    'n_estimators': randint(100, 1000),  # Número de estimadores entre 100 y 1000
    'max_depth': [None] + list(randint(3, 30).rvs(10)),  # Profundidad máxima entre 3 y 30
    'min_samples_split': randint(2, 20),  # Número mínimo de muestras para dividir un nodo
    'min_samples_leaf': randint(1, 20),  # Número mínimo de muestras en cada hoja
    'max_features': ['auto', 'sqrt']
    }

# Inicializa RandomizedSearchCV con el clasificador, la distribución de parámetros y el número de iteraciones
    random_search = RandomizedSearchCV(rf, param_distributions=param_dist, n_iter=100, cv=5, random_state=42, n_jobs=-1)

# Ajusta RandomizedSearchCV en tus datos de entrenamiento
    random_search.fit(X_train, winner_train)

# Muestra los mejores parámetros encontrados
    print("Mejores parámetros encontrados:", random_search.best_params_)

# Muestra el mejor puntaje obtenido durante la búsqueda
    print("Mejor precisión encontrada:", random_search.best_score_)

    return render(request, 'predicciones/conjuntoEntrenamiento.html', {"mensaje": random_search.best_score_}) '''

def entrenamiento_Modelo_Random_Forest_Para_Datos_5_Ultimos_Partidos(request):
    X,Y = calculo_Valores_Indp_Y_Depen_Para_Datos_5_Ultimos_Partidos()
    X_train, X_test, winner_train, winner_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    model_rf = RandomForestClassifier(n_estimators=1000, max_depth=50, max_features='sqrt', min_samples_leaf=50, min_samples_split=20)
    model_rf.fit(X_train, winner_train), 
    winner_pred = model_rf.predict(X_test)
    labels = ['1', "0", "2"]
    conf_mat_nv = confusion_matrix(winner_test, winner_pred, labels=labels)
    conf_matrix_table = tabulate(conf_mat_nv, headers=labels, showindex=labels, tablefmt='fancy_grid')
    accuracy = accuracy_score(winner_test, winner_pred)
    
    print(conf_matrix_table)
    print(accuracy)

    return render(request, 'predicciones/conjuntoEntrenamiento.html', {"mensaje": accuracy})

def entrenamiento_Modelo_SVM_Para_Datos_5_Ultimos_Partidos(request):
    X,Y = calculo_Valores_Indp_Y_Depen_Para_Datos_5_Ultimos_Partidos()
    X_train, X_test, winner_train, winner_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    model_svm = SVC(kernel='poly', C=1, random_state=42)
    model_svm.fit(X_train, winner_train), 
    winner_pred = model_svm.predict(X_test)
    labels = ['1', "0", "2"]
    conf_mat_nv = confusion_matrix(winner_test, winner_pred, labels=labels)
    conf_matrix_table = tabulate(conf_mat_nv, headers=labels, showindex=labels, tablefmt='fancy_grid')
    accuracy = accuracy_score(winner_test, winner_pred)
    
    print(conf_matrix_table)
    print(accuracy)

    return render(request, 'predicciones/conjuntoEntrenamiento.html', {"mensaje": accuracy})

def entrenamiento_Modelo_LR_Para_Datos_5_Ultimos_Partidos(request):
    X,Y = calculo_Valores_Indp_Y_Depen_Para_Datos_5_Ultimos_Partidos()
    X_train, X_test, winner_train, winner_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    model_lr = LogisticRegression(penalty="l1", C=0.1, solver="liblinear", class_weight='balanced', max_iter=10000, random_state=42)
    model_lr.fit(X_train, winner_train), 
    winner_pred = model_lr.predict(X_test)
    labels = ['1', "0", "2"]
    conf_mat_nv = confusion_matrix(winner_test, winner_pred, labels=labels)
    conf_matrix_table = tabulate(conf_mat_nv, headers=labels, showindex=labels, tablefmt='fancy_grid')
    accuracy = accuracy_score(winner_test, winner_pred)
    
    print(conf_matrix_table)
    print(accuracy)

    return render(request, 'predicciones/conjuntoEntrenamiento.html', {"mensaje": accuracy})

def entrenamiento_Modelo_Gradient_Boosting_Classifier_Para_Datos_5_Ultimos_Partidos(request):
    X,Y = calculo_Valores_Indp_Y_Depen_Para_Datos_5_Ultimos_Partidos()
    X_train, X_test, winner_train, winner_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    model_gbc =  GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, subsample=0.9, random_state=42)
    model_gbc.fit(X_train, winner_train), 
    winner_pred = model_gbc.predict(X_test)
    labels = ['1', "0", "2"]
    conf_mat_nv = confusion_matrix(winner_test, winner_pred, labels=labels)
    conf_matrix_table = tabulate(conf_mat_nv, headers=labels, showindex=labels, tablefmt='fancy_grid')
    accuracy = accuracy_score(winner_test, winner_pred)
    
    print(conf_matrix_table)
    print(accuracy)

    return render(request, 'predicciones/conjuntoEntrenamiento.html', {"mensaje": accuracy})



def calculo_Valores_Indp_Y_Depen_Para_Datos_3_Ultimos_Partidos():
    partidos = PartidosEntrenamiento.objects.all()

    goles_ultimos_3_partidos_equipos_locales = [partido.goles_ultimos_3_partidos_equipo_local for partido in partidos]
    goles_ultimos_3_partidos_equipos_visitante = [partido.goles_ultimos_3_partidos_equipo_visitante for partido in partidos]
    puntos_ultimos_3_partidos_equipos_locales = [partido.puntos_ultimos_3_partidos_equipo_local for partido in partidos]
    puntos_ultimos_3_partidos_equipos_visitantes = [partido.puntos_ultimos_3_partidos_equipo_visitante for partido in partidos]
    goles_ultimos_3_partidos_locales_siendo_local = [partido.goles_ultimos_3_partidos_local_siendo_local for partido in partidos]
    goles_ultimos_3_partidos_visitantes_siendo_visitante = [partido.goles_ultimos_3_partidos_visitante_siendo_visitante for partido in partidos]
    puntos_ultimos_3_partidos_locales_siendo_local = [partido.puntos_ultimos_3_partidos_local_siendo_local for partido in partidos]
    puntos_ultimos_3_partidos_visitante_siendo_visitantes = [partido.puntos_ultimos_3_partidos_visitante_siendo_visitante for partido in partidos]
    goles_en_contra_ultimos_3_partidos_equipo_locales = [partido.goles_en_contra_ultimos_3_partidos_equipo_local for partido in partidos]
    goles_en_contra_ultimos_3_partidos_equipo_visitantes = [partido.goles_en_contra_ultimos_3_partidos_equipo_visitante for partido in partidos]
    goles_en_contra_ultimos_3_partidos_locales_siendo_local = [partido.goles_en_contra_ultimos_3_partidos_local_siendo_local for partido in partidos]
    goles_en_contra_ultimos_3_partidos_visitantees_siendo_visitante = [partido.goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante for partido in partidos]
    winners = [partido.winner for partido in partidos]
    

    X = np.column_stack((
                        goles_ultimos_3_partidos_equipos_locales, 
                        goles_ultimos_3_partidos_equipos_visitante,
                        puntos_ultimos_3_partidos_equipos_locales,
                        puntos_ultimos_3_partidos_equipos_visitantes,
                        goles_en_contra_ultimos_3_partidos_equipo_locales,
                        goles_en_contra_ultimos_3_partidos_equipo_visitantes,
                        goles_ultimos_3_partidos_locales_siendo_local,
                        goles_ultimos_3_partidos_visitantes_siendo_visitante,
                        puntos_ultimos_3_partidos_locales_siendo_local,
                        puntos_ultimos_3_partidos_visitante_siendo_visitantes,
                        goles_en_contra_ultimos_3_partidos_locales_siendo_local,
                        goles_en_contra_ultimos_3_partidos_visitantees_siendo_visitante))
    Y = np.array(winners)
    return X, Y


def entrenamiento_Modelo_Bayes_Para_Datos_3_Ultimos_Partidos(request):
    
    X,Y = calculo_Valores_Indp_Y_Depen_Para_Datos_3_Ultimos_Partidos()
    X_train, X_test, winner_train, winner_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    model_nv = MultinomialNB()
    model_nv.fit(X_train, winner_train)
    winner_pred = model_nv.predict(X_test)
    labels = ['1', "0", "2"]
    conf_mat_nv = confusion_matrix(winner_test, winner_pred, labels=labels)
    conf_matrix_table = tabulate(conf_mat_nv, headers=labels, showindex=labels, tablefmt='fancy_grid')
    accuracy = accuracy_score(winner_test, winner_pred)
    
    print(conf_matrix_table)
    print(accuracy)

    return render(request, 'predicciones/conjuntoEntrenamiento.html', {"mensaje": accuracy})


def entrenamiento_Modelo_KNN_Para_Datos_3_Ultimos_Partidos(request):
    
    X,Y = calculo_Valores_Indp_Y_Depen_Para_Datos_3_Ultimos_Partidos()
    X_train, X_test, winner_train, winner_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    
    #model_knn = KNeighborsClassifier(n_neighbors=300, metric='manhattan', weights='uniform', algorithm='auto')
    #model_knn = KNeighborsClassifier(n_neighbors=203, metric='euclidean', weights='uniform', algorithm='auto')
    model_knn = KNeighborsClassifier(n_neighbors=203, metric='chebyshev', weights='uniform', algorithm='auto')
    #model_knn = KNeighborsClassifier(n_neighbors=203, metric='minkowski', p=1,weights='uniform', algorithm='auto')
    #model_knn = KNeighborsClassifier(n_neighbors=203, metric='minkowski', p=2,weights='distance', algorithm='brute')
    model_knn.fit(X_train, winner_train)
    winner_pred = model_knn.predict(X_test)
    labels = ['1', "0", "2"]
    conf_mat_nv = confusion_matrix(winner_test, winner_pred, labels=labels)
    conf_matrix_table = tabulate(conf_mat_nv, headers=labels, showindex=labels, tablefmt='fancy_grid')
    accuracy = accuracy_score(winner_test, winner_pred)
    
    print(conf_matrix_table)
    print(accuracy)

    return render(request, 'predicciones/conjuntoEntrenamiento.html', {"mensaje": accuracy})


def entrenamiento_Modelo_Random_Forest_Para_Datos_3_Ultimos_Partidos(request):
    X,Y = calculo_Valores_Indp_Y_Depen_Para_Datos_3_Ultimos_Partidos()
    X_train, X_test, winner_train, winner_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    model_rf = RandomForestClassifier(n_estimators=203, max_depth=50, max_features='sqrt', min_samples_leaf=50, min_samples_split=20)
    model_rf.fit(X_train, winner_train), 
    winner_pred = model_rf.predict(X_test)
    labels = ['1', "0", "2"]
    conf_mat_nv = confusion_matrix(winner_test, winner_pred, labels=labels)
    conf_matrix_table = tabulate(conf_mat_nv, headers=labels, showindex=labels, tablefmt='fancy_grid')
    accuracy = accuracy_score(winner_test, winner_pred)
    
    print(conf_matrix_table)
    print(accuracy)

    return render(request, 'predicciones/conjuntoEntrenamiento.html', {"mensaje": accuracy})

def entrenamiento_Modelo_SVM_Para_Datos_3_Ultimos_Partidos(request):
    X,Y = calculo_Valores_Indp_Y_Depen_Para_Datos_3_Ultimos_Partidos()
    X_train, X_test, winner_train, winner_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    model_svm = SVC(kernel='linear', C=1, random_state=42)
    model_svm.fit(X_train, winner_train), 
    winner_pred = model_svm.predict(X_test)
    labels = ['1', "0", "2"]
    conf_mat_nv = confusion_matrix(winner_test, winner_pred, labels=labels)
    conf_matrix_table = tabulate(conf_mat_nv, headers=labels, showindex=labels, tablefmt='fancy_grid')
    accuracy = accuracy_score(winner_test, winner_pred)
    
    print(conf_matrix_table)
    print(accuracy)

    return render(request, 'predicciones/conjuntoEntrenamiento.html', {"mensaje": accuracy})

def entrenamiento_Modelo_LR_Para_Datos_3_Ultimos_Partidos(request):
    X,Y = calculo_Valores_Indp_Y_Depen_Para_Datos_3_Ultimos_Partidos()
    X_train, X_test, winner_train, winner_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    for i in range(1,11):

        if i <= 3:
            penalty = "l1"
            solver = "liblinear"
        else:
            penalty = "l2"
            solver = "lbfgs" if i <= 6 else "saga"  # Utilizar otros solvers para las últimas combinaciones

        C_values = [0.1, 1, 10] if i <= 9 else [0.1, 1, 10, 100]

        model_lr = LogisticRegression(penalty=penalty, C=C_values[(i - 1) % len(C_values)], solver=solver, class_weight='balanced', max_iter=10000, random_state=42)
        model_lr.fit(X_train, winner_train)
        winner_pred = model_lr.predict(X_test)
        labels = ['1', "0", "2"]
        conf_mat_nv = confusion_matrix(winner_test, winner_pred, labels=labels)
        conf_matrix_table = tabulate(conf_mat_nv, headers=labels, showindex=labels, tablefmt='fancy_grid')
        accuracy = accuracy_score(winner_test, winner_pred)

        print(model_lr)
        print(conf_matrix_table)
        print(accuracy)

    return HttpResponse("Todo Ok")

def entrenamiento_Modelo_Gradient_Boosting_Classifier_Para_Datos_3_Ultimos_Partidos(request):
    X,Y = calculo_Valores_Indp_Y_Depen_Para_Datos_3_Ultimos_Partidos()
    X_train, X_test, winner_train, winner_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    for i in range(1, 12):
        if i == 1:
            model_gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
        elif i == 2:
            model_gbc = GradientBoostingClassifier(n_estimators=200, learning_rate=0.1, max_depth=3, random_state=42)
        elif i == 3:
            model_gbc = GradientBoostingClassifier(n_estimators=300, learning_rate=0.1, max_depth=3, random_state=42)
        elif i == 4:
            model_gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.01, max_depth=3, random_state=42)
        elif i == 5:
            model_gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.001, max_depth=3, random_state=42)
        elif i == 6:
            model_gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
        elif i == 7:
            model_gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=7, random_state=42)
        elif i == 8:
            model_gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, min_samples_split=2, min_samples_leaf=1, random_state=42)
        elif i == 9:
            model_gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, min_samples_split=5, min_samples_leaf=2, random_state=42)
        elif i == 10:
            model_gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, subsample=0.8, random_state=42)
        elif i == 11:
            model_gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, subsample=0.9, random_state=42)
        model_gbc.fit(X_train, winner_train), 
        winner_pred = model_gbc.predict(X_test)
        labels = ['1', "0", "2"]
        conf_mat_nv = confusion_matrix(winner_test, winner_pred, labels=labels)
        conf_matrix_table = tabulate(conf_mat_nv, headers=labels, showindex=labels, tablefmt='fancy_grid')
        accuracy = accuracy_score(winner_test, winner_pred)
    
        print(conf_matrix_table)
        print(accuracy)

    return HttpResponse("Todo OK")

def calculo_Valores_Indp_Y_Depen_Para_Datos_3_Y_5_Ultimos_Partidos():
    partidos = PartidosEntrenamiento.objects.all()
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
    

    goles_ultimos_3_partidos_equipos_locales = [partido.goles_ultimos_3_partidos_equipo_local for partido in partidos]
    goles_ultimos_3_partidos_equipos_visitante = [partido.goles_ultimos_3_partidos_equipo_visitante for partido in partidos]
    puntos_ultimos_3_partidos_equipos_locales = [partido.puntos_ultimos_3_partidos_equipo_local for partido in partidos]
    puntos_ultimos_3_partidos_equipos_visitantes = [partido.puntos_ultimos_3_partidos_equipo_visitante for partido in partidos]
    goles_ultimos_3_partidos_locales_siendo_local = [partido.goles_ultimos_3_partidos_local_siendo_local for partido in partidos]
    goles_ultimos_3_partidos_visitantes_siendo_visitante = [partido.goles_ultimos_3_partidos_visitante_siendo_visitante for partido in partidos]
    puntos_ultimos_3_partidos_locales_siendo_local = [partido.puntos_ultimos_3_partidos_local_siendo_local for partido in partidos]
    puntos_ultimos_3_partidos_visitante_siendo_visitantes = [partido.puntos_ultimos_3_partidos_visitante_siendo_visitante for partido in partidos]
    goles_en_contra_ultimos_3_partidos_equipo_locales = [partido.goles_en_contra_ultimos_3_partidos_equipo_local for partido in partidos]
    goles_en_contra_ultimos_3_partidos_equipo_visitantes = [partido.goles_en_contra_ultimos_3_partidos_equipo_visitante for partido in partidos]
    goles_en_contra_ultimos_3_partidos_locales_siendo_local = [partido.goles_en_contra_ultimos_3_partidos_local_siendo_local for partido in partidos]
    goles_en_contra_ultimos_3_partidos_visitantees_siendo_visitante = [partido.goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante for partido in partidos]
    winners = [partido.winner for partido in partidos]
    

    X = np.column_stack((
                        goles_ultimos_5_partidos_equipos_locales, 
                        goles_ultimos_5_partidos_equipos_visitante,
                        puntos_ultimos_5_partidos_equipos_locales,
                        puntos_ultimos_5_partidos_equipos_visitantes,
                        goles_en_contra_ultimos_5_partidos_equipo_locales,
                        goles_en_contra_ultimos_5_partidos_equipo_visitantes,
                        goles_ultimos_5_partidos_locales_siendo_local,
                        goles_ultimos_5_partidos_visitantes_siendo_visitante,
                        puntos_ultimos_5_partidos_locales_siendo_local,
                        puntos_ultimos_5_partidos_visitante_siendo_visitantes,
                        goles_en_contra_ultimos_5_partidos_locales_siendo_local,
                        goles_en_contra_ultimos_5_partidos_visitantees_siendo_visitante,
                        goles_ultimos_3_partidos_equipos_locales, 
                        goles_ultimos_3_partidos_equipos_visitante,
                        puntos_ultimos_3_partidos_equipos_locales,
                        puntos_ultimos_3_partidos_equipos_visitantes,
                        goles_en_contra_ultimos_3_partidos_equipo_locales,
                        goles_en_contra_ultimos_3_partidos_equipo_visitantes,
                        goles_ultimos_3_partidos_locales_siendo_local,
                        goles_ultimos_3_partidos_visitantes_siendo_visitante,
                        puntos_ultimos_3_partidos_locales_siendo_local,
                        puntos_ultimos_3_partidos_visitante_siendo_visitantes,
                        goles_en_contra_ultimos_3_partidos_locales_siendo_local,
                        goles_en_contra_ultimos_3_partidos_visitantees_siendo_visitante))
    Y = np.array(winners)
    return X, Y


def entrenamiento_Modelo_Bayes_Para_Datos_3_Y_5_Ultimos_Partidos(request):

    
    X,Y = calculo_Valores_Indp_Y_Depen_Para_Datos_3_Y_5_Ultimos_Partidos()
    X_train, X_test, winner_train, winner_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    model_nv = MultinomialNB()
    model_nv.fit(X_train, winner_train)
    winner_pred = model_nv.predict(X_test)
    labels = ['1', "0", "2"]
    conf_mat_nv = confusion_matrix(winner_test, winner_pred, labels=labels)
    conf_matrix_table = tabulate(conf_mat_nv, headers=labels, showindex=labels, tablefmt='fancy_grid')
    accuracy = accuracy_score(winner_test, winner_pred)
    
    print(conf_matrix_table)
    print(accuracy)

    return render(request, 'predicciones/conjuntoEntrenamiento.html', {"mensaje": accuracy})


def entrenamiento_Modelo_KNN_Para_Datos_3_Y_5_Ultimos_Partidos(request):
    
    X,Y = calculo_Valores_Indp_Y_Depen_Para_Datos_3_Y_5_Ultimos_Partidos()
    X_train, X_test, winner_train, winner_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    
    model_knn = KNeighborsClassifier(n_neighbors=300, metric='manhattan', weights='distance', algorithm='auto')
    #model_knn = KNeighborsClassifier(n_neighbors=203, metric='euclidean', weights='uniform', algorithm='auto')
    #model_knn = KNeighborsClassifier(n_neighbors=203, metric='chebyshev', weights='distance', algorithm='auto')
    #model_knn = KNeighborsClassifier(n_neighbors=203, metric='minkowski', p=1,weights='uniform', algorithm='auto')
    #model_knn = KNeighborsClassifier(n_neighbors=203, metric='minkowski', p=2,weights='distance', algorithm='brute')
    model_knn.fit(X_train, winner_train)
    winner_pred = model_knn.predict(X_test)
    labels = ['1', "0", "2"]
    conf_mat_nv = confusion_matrix(winner_test, winner_pred, labels=labels)
    conf_matrix_table = tabulate(conf_mat_nv, headers=labels, showindex=labels, tablefmt='fancy_grid')
    accuracy = accuracy_score(winner_test, winner_pred)
    
    print(conf_matrix_table)
    print(accuracy)

    return render(request, 'predicciones/conjuntoEntrenamiento.html', {"mensaje": accuracy})


def entrenamiento_Modelo_Random_Forest_Para_Datos_3_Y_5_Ultimos_Partidos(request):
    X,Y = calculo_Valores_Indp_Y_Depen_Para_Datos_3_Y_5_Ultimos_Partidos()
    X_train, X_test, winner_train, winner_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    model_rf = RandomForestClassifier(n_estimators=203, max_depth=20, max_features='sqrt', class_weight="balanced",min_samples_leaf=3, min_samples_split=10)
    model_rf.fit(X_train, winner_train), 
    winner_pred = model_rf.predict(X_test)
    labels = ['1', "0", "2"]
    conf_mat_nv = confusion_matrix(winner_test, winner_pred, labels=labels)
    conf_matrix_table = tabulate(conf_mat_nv, headers=labels, showindex=labels, tablefmt='fancy_grid')
    accuracy = accuracy_score(winner_test, winner_pred)
    report = classification_report(winner_test, winner_pred)
    print(conf_matrix_table)
    print(accuracy)
    print(report)

    return render(request, 'predicciones/conjuntoEntrenamiento.html', {"mensaje": accuracy})

def entrenamiento_Modelo_SVM_Para_Datos_3_Y_5_Ultimos_Partidos(request):
    X,Y = calculo_Valores_Indp_Y_Depen_Para_Datos_3_Y_5_Ultimos_Partidos()
    X_train, X_test, winner_train, winner_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    model_svm = SVC(kernel='poly', C=1, class_weight="balanced", random_state=42)
    model_svm.fit(X_train, winner_train), 
    winner_pred = model_svm.predict(X_test)
    labels = ['1', "0", "2"]
    conf_mat_nv = confusion_matrix(winner_test, winner_pred, labels=labels)
    conf_matrix_table = tabulate(conf_mat_nv, headers=labels, showindex=labels, tablefmt='fancy_grid')
    accuracy = accuracy_score(winner_test, winner_pred)
    report = classification_report(winner_test, winner_pred)
    
    print(conf_matrix_table)
    print(accuracy)
    print(report)

    return render(request, 'predicciones/conjuntoEntrenamiento.html', {"mensaje": accuracy})

def entrenamiento_Modelo_LR_Para_Datos_3_Y_5_Ultimos_Partidos(request):
    X,Y = calculo_Valores_Indp_Y_Depen_Para_Datos_3_Y_5_Ultimos_Partidos()
    X_train, X_test, winner_train, winner_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    for i in range(1,11):

        if i <= 3:
            penalty = "l1"
            solver = "liblinear"
        else:
            penalty = "l2"
            solver = "lbfgs" if i <= 6 else "saga"  # Utilizar otros solvers para las últimas combinaciones

        C_values = [0.1, 1, 10] if i <= 9 else [0.1, 1, 10, 100]

        model_lr = LogisticRegression(penalty=penalty, C=C_values[(i - 1) % len(C_values)],solver=solver, class_weight='balanced', max_iter=10000, random_state=42)
        model_lr.fit(X_train, winner_train)
        winner_pred = model_lr.predict(X_test)
        labels = ['1', "0", "2"]
        conf_mat_nv = confusion_matrix(winner_test, winner_pred, labels=labels)
        conf_matrix_table = tabulate(conf_mat_nv, headers=labels, showindex=labels, tablefmt='fancy_grid')
        accuracy = accuracy_score(winner_test, winner_pred)

        conf_mat_nv = confusion_matrix(winner_test, winner_pred, labels=labels)
        conf_matrix_table = tabulate(conf_mat_nv, headers=labels, showindex=labels, tablefmt='fancy_grid')
        accuracy = accuracy_score(winner_test, winner_pred)
        report = classification_report(winner_test, winner_pred)
    
        print(conf_matrix_table)
        print(accuracy)
        print(report)

    return HttpResponse("Todo Ok")



def entrenamiento_Modelo_Gradient_Boosting_Classifier_Para_Datos_3_Y_5_Ultimos_Partidos(request):
    X,Y = calculo_Valores_Indp_Y_Depen_Para_Datos_3_Y_5_Ultimos_Partidos()
    X_train, X_test, winner_train, winner_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    for i in range(1, 12):
        if i == 1:
            model_gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
            print( model_gbc)
        elif i == 2:
            model_gbc = GradientBoostingClassifier(n_estimators=200, learning_rate=0.1, max_depth=3, random_state=42)
            print( model_gbc)
        elif i == 3:
            model_gbc = GradientBoostingClassifier(n_estimators=300, learning_rate=0.1, max_depth=3, random_state=42)
            print( model_gbc)
        elif i == 4:
            model_gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.01, max_depth=3, random_state=42)
            print( model_gbc)
        elif i == 5:
            model_gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.001, max_depth=3, random_state=42)
            print( model_gbc)
        elif i == 6:
            model_gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
            print( model_gbc)
        elif i == 7:
            model_gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=7, random_state=42)
            print( model_gbc)
        elif i == 8:
            model_gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, min_samples_split=2, min_samples_leaf=1, random_state=42)
            print( model_gbc)
        elif i == 9:
            model_gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, min_samples_split=5, min_samples_leaf=2, random_state=42)
            print( model_gbc)
        elif i == 10:
            model_gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, subsample=0.8, random_state=42)
            print( model_gbc)
        elif i == 11:
            model_gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, subsample=0.9, random_state=42)
            print( model_gbc)
        model_gbc.fit(X_train, winner_train), 
        winner_pred = model_gbc.predict(X_test)
        labels = ['1', "0", "2"]
        conf_mat_nv = confusion_matrix(winner_test, winner_pred, labels=labels)
        conf_matrix_table = tabulate(conf_mat_nv, headers=labels, showindex=labels, tablefmt='fancy_grid')
        accuracy = accuracy_score(winner_test, winner_pred)
        report = classification_report(winner_test, winner_pred)
    
        print(conf_matrix_table)
        print(accuracy)
        print(report)

    return HttpResponse("Todo Ok")

def obtencion_valores_para_predecir_partido_sin_predecir():
    partidos = PartidoSinPredecir.objects.all()
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
    

    goles_ultimos_3_partidos_equipos_locales = [partido.goles_ultimos_3_partidos_equipo_local for partido in partidos]
    goles_ultimos_3_partidos_equipos_visitante = [partido.goles_ultimos_3_partidos_equipo_visitante for partido in partidos]
    puntos_ultimos_3_partidos_equipos_locales = [partido.puntos_ultimos_3_partidos_equipo_local for partido in partidos]
    puntos_ultimos_3_partidos_equipos_visitantes = [partido.puntos_ultimos_3_partidos_equipo_visitante for partido in partidos]
    goles_ultimos_3_partidos_locales_siendo_local = [partido.goles_ultimos_3_partidos_local_siendo_local for partido in partidos]
    goles_ultimos_3_partidos_visitantes_siendo_visitante = [partido.goles_ultimos_3_partidos_visitante_siendo_visitante for partido in partidos]
    puntos_ultimos_3_partidos_locales_siendo_local = [partido.puntos_ultimos_3_partidos_local_siendo_local for partido in partidos]
    puntos_ultimos_3_partidos_visitante_siendo_visitantes = [partido.puntos_ultimos_3_partidos_visitante_siendo_visitante for partido in partidos]
    goles_en_contra_ultimos_3_partidos_equipo_locales = [partido.goles_en_contra_ultimos_3_partidos_equipo_local for partido in partidos]
    goles_en_contra_ultimos_3_partidos_equipo_visitantes = [partido.goles_en_contra_ultimos_3_partidos_equipo_visitante for partido in partidos]
    goles_en_contra_ultimos_3_partidos_locales_siendo_local = [partido.goles_en_contra_ultimos_3_partidos_local_siendo_local for partido in partidos]
    goles_en_contra_ultimos_3_partidos_visitantees_siendo_visitante = [partido.goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante for partido in partidos]
    

    XP = np.column_stack((
                        goles_ultimos_5_partidos_equipos_locales, 
                        goles_ultimos_5_partidos_equipos_visitante,
                        puntos_ultimos_5_partidos_equipos_locales,
                        puntos_ultimos_5_partidos_equipos_visitantes,
                        goles_en_contra_ultimos_5_partidos_equipo_locales,
                        goles_en_contra_ultimos_5_partidos_equipo_visitantes,
                        goles_ultimos_5_partidos_locales_siendo_local,
                        goles_ultimos_5_partidos_visitantes_siendo_visitante,
                        puntos_ultimos_5_partidos_locales_siendo_local,
                        puntos_ultimos_5_partidos_visitante_siendo_visitantes,
                        goles_en_contra_ultimos_5_partidos_locales_siendo_local,
                        goles_en_contra_ultimos_5_partidos_visitantees_siendo_visitante,
                        goles_ultimos_3_partidos_equipos_locales, 
                        goles_ultimos_3_partidos_equipos_visitante,
                        puntos_ultimos_3_partidos_equipos_locales,
                        puntos_ultimos_3_partidos_equipos_visitantes,
                        goles_en_contra_ultimos_3_partidos_equipo_locales,
                        goles_en_contra_ultimos_3_partidos_equipo_visitantes,
                        goles_ultimos_3_partidos_locales_siendo_local,
                        goles_ultimos_3_partidos_visitantes_siendo_visitante,
                        puntos_ultimos_3_partidos_locales_siendo_local,
                        puntos_ultimos_3_partidos_visitante_siendo_visitantes,
                        goles_en_contra_ultimos_3_partidos_locales_siendo_local,
                        goles_en_contra_ultimos_3_partidos_visitantees_siendo_visitante))
    return XP
    


def prediccion_partidos_sin_predecir(request):
    PartidosPredichos.objects.all().delete()
    X,Y = calculo_Valores_Indp_Y_Depen_Para_Datos_3_Y_5_Ultimos_Partidos()
    XP = obtencion_valores_para_predecir_partido_sin_predecir()
    X_train, X_test, winner_train, winner_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    model_gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
    model_gbc.fit(X_train, winner_train),
    predicciones = model_gbc.predict(XP)
    predicciones_modificadas = ['X' if pred == '0' else pred for pred in predicciones]
    partidos = PartidoSinPredecir.objects.all()
    i = 0
    for partido in partidos:
        liga = partido.liga
        logo_liga = partido. logo_liga
        jornada = partido.jornada
        temporada = partido.temporada
        equipo_local = partido.equipo_local
        equipo_visitante = partido.equipo_visitante
        escudo_local = partido.escudo_local
        escudo_visitante = partido.escudo_visitante
        goles_ultimos_5_partidos_equipo_local = partido.goles_ultimos_5_partidos_equipo_local
        goles_ultimos_5_partidos_equipo_visitante = partido.goles_ultimos_5_partidos_equipo_visitante
        puntos_ultimos_5_partidos_equipo_local = partido.puntos_ultimos_5_partidos_equipo_local
        puntos_ultimos_5_partidos_equipo_visitante = partido.puntos_ultimos_5_partidos_equipo_visitante
        goles_ultimos_5_partidos_local_siendo_local = partido.goles_ultimos_5_partidos_local_siendo_local
        goles_ultimos_5_partidos_visitante_siendo_visitante = partido.goles_ultimos_5_partidos_visitante_siendo_visitante
        puntos_ultimos_5_partidos_local_siendo_local = partido.puntos_ultimos_5_partidos_local_siendo_local
        puntos_ultimos_5_partidos_visitante_siendo_visitante = partido.puntos_ultimos_5_partidos_visitante_siendo_visitante
        goles_en_contra_ultimos_5_partidos_equipo_local = partido.goles_en_contra_ultimos_5_partidos_equipo_local
        goles_en_contra_ultimos_5_partidos_equipo_visitante = partido.goles_en_contra_ultimos_5_partidos_equipo_visitante
        goles_en_contra_ultimos_5_partidos_local_siendo_local = partido.goles_en_contra_ultimos_5_partidos_local_siendo_local
        goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante = partido.goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante
        goles_ultimos_3_partidos_equipo_local = partido.goles_ultimos_3_partidos_equipo_local
        goles_ultimos_3_partidos_equipo_visitante = partido.goles_ultimos_3_partidos_equipo_visitante
        puntos_ultimos_3_partidos_equipo_local = partido.puntos_ultimos_3_partidos_equipo_local
        puntos_ultimos_3_partidos_equipo_visitante = partido.puntos_ultimos_3_partidos_equipo_visitante
        goles_ultimos_3_partidos_local_siendo_local = partido.goles_ultimos_3_partidos_local_siendo_local
        goles_ultimos_3_partidos_visitante_siendo_visitante = partido.goles_ultimos_3_partidos_visitante_siendo_visitante
        puntos_ultimos_3_partidos_local_siendo_local = partido.puntos_ultimos_3_partidos_local_siendo_local
        puntos_ultimos_3_partidos_visitante_siendo_visitante = partido.puntos_ultimos_3_partidos_visitante_siendo_visitante
        goles_en_contra_ultimos_3_partidos_equipo_local = partido.goles_en_contra_ultimos_3_partidos_equipo_local
        goles_en_contra_ultimos_3_partidos_equipo_visitante = partido.goles_en_contra_ultimos_3_partidos_equipo_visitante
        goles_en_contra_ultimos_3_partidos_local_siendo_local = partido.goles_en_contra_ultimos_3_partidos_local_siendo_local
        goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante = partido.goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante
        winner = predicciones_modificadas[i]

        PartidosPredichos.objects.create(
                                    id=i,
                                    liga=liga,
                                    jornada=jornada,
                                    temporada=temporada,
                                    logo_liga = logo_liga, 
                                    equipo_local = equipo_local, 
                                    equipo_visitante=equipo_visitante,
                                    escudo_local = escudo_local,
                                    escudo_visitante  = escudo_visitante, 
                                    goles_ultimos_5_partidos_equipo_local =  goles_ultimos_5_partidos_equipo_local,
                                    goles_ultimos_5_partidos_equipo_visitante = goles_ultimos_5_partidos_equipo_visitante, 
                                    puntos_ultimos_5_partidos_equipo_local = puntos_ultimos_5_partidos_equipo_local, 
                                    puntos_ultimos_5_partidos_equipo_visitante=puntos_ultimos_5_partidos_equipo_visitante, 
                                    goles_ultimos_5_partidos_local_siendo_local=goles_ultimos_5_partidos_local_siendo_local, 
                                    goles_ultimos_5_partidos_visitante_siendo_visitante = goles_ultimos_5_partidos_visitante_siendo_visitante,
                                    puntos_ultimos_5_partidos_local_siendo_local = puntos_ultimos_5_partidos_local_siendo_local,
                                    puntos_ultimos_5_partidos_visitante_siendo_visitante = puntos_ultimos_5_partidos_visitante_siendo_visitante,
                                    goles_en_contra_ultimos_5_partidos_equipo_local = goles_en_contra_ultimos_5_partidos_equipo_local,
                                    goles_en_contra_ultimos_5_partidos_equipo_visitante = goles_en_contra_ultimos_5_partidos_equipo_visitante,
                                    goles_en_contra_ultimos_5_partidos_local_siendo_local = goles_en_contra_ultimos_5_partidos_local_siendo_local,
                                    goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante = goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante,

                                    goles_ultimos_3_partidos_equipo_local =  goles_ultimos_3_partidos_equipo_local,
                                    goles_ultimos_3_partidos_equipo_visitante = goles_ultimos_3_partidos_equipo_visitante, 
                                    puntos_ultimos_3_partidos_equipo_local = puntos_ultimos_3_partidos_equipo_local, 
                                    puntos_ultimos_3_partidos_equipo_visitante=puntos_ultimos_3_partidos_equipo_visitante, 
                                    goles_ultimos_3_partidos_local_siendo_local=goles_ultimos_3_partidos_local_siendo_local, 
                                    goles_ultimos_3_partidos_visitante_siendo_visitante = goles_ultimos_3_partidos_visitante_siendo_visitante,
                                    puntos_ultimos_3_partidos_local_siendo_local = puntos_ultimos_3_partidos_local_siendo_local,
                                    puntos_ultimos_3_partidos_visitante_siendo_visitante = puntos_ultimos_3_partidos_visitante_siendo_visitante,
                                    goles_en_contra_ultimos_3_partidos_equipo_local = goles_en_contra_ultimos_3_partidos_equipo_local,
                                    goles_en_contra_ultimos_3_partidos_equipo_visitante = goles_en_contra_ultimos_3_partidos_equipo_visitante,
                                    goles_en_contra_ultimos_3_partidos_local_siendo_local = goles_en_contra_ultimos_3_partidos_local_siendo_local,
                                    goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante = goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante,
                                    winner = winner)
        i = i+1
        

    return HttpResponse("Partidos de Predichos Cargados")

def mostrar_tasa_de_acierto():
    partidos_predichos = PartidosPredichos.objects.all()
    es1siendo1 = 0
    es1siendoX = 0
    es1siendo2 = 0
    esXsiendo1 = 0
    esXsiendoX = 0
    esXsiendo2 = 0
    es2siendo1 = 0
    es2siendoX = 0
    es2siendo2 = 0

    for p in partidos_predichos:
        local = p.equipo_local
        visitante = p.equipo_visitante
        winner_predichos = p.winner

        partido_real = PartidoReal.objects.filter(equipo_local = local, equipo_visitante = visitante).first()
        winner_real = partido_real.winner

        if winner_predichos == '1' and winner_real == '1':
            es1siendo1 += 1
        elif winner_predichos == '1' and winner_real == 'X':
            es1siendoX += 1
        elif winner_predichos == '1' and winner_real == '2':
            es1siendo2 += 1
        elif winner_predichos == 'X' and winner_real == '1':
            esXsiendo1 += 1
        elif winner_predichos == 'X' and winner_real == 'X':
            esXsiendoX += 1
        elif winner_predichos == 'X' and winner_real == '2':
            esXsiendo2 += 1
        elif winner_predichos == '2' and winner_real == '1':
            es2siendo1 += 1
        elif winner_predichos == '2' and winner_real == 'X':
            es2siendoX += 1
        elif winner_predichos == '2' and winner_real == '2':
            es2siendo2 += 1
    return es1siendo1,es1siendoX,es1siendo2,esXsiendo1,esXsiendoX,esXsiendo2,es2siendo1,es2siendoX,es2siendo2

def mostrar_predicciones(request):
    partidos = None
    paginator = None
    if request.method =='POST':
        formulario = formulario_prediccion(request.POST)
        if formulario.is_valid():
            liga = formulario.cleaned_data["liga"]
            jornada =formulario.cleaned_data["jornada"]
            local = formulario.cleaned_data["local"]
            visitante = formulario.cleaned_data["visitante"]
            winner = formulario.cleaned_data["winner"]



            if liga and local and visitante:
                return redirect(reverse('Filtrar_Predicciones') + f'?liga={liga}&local={local}&visitante={visitante}')
            elif liga and winner and jornada:
                return redirect(reverse('Filtrar_Predicciones') + f'?liga={liga}&winner={winner}&jornada={jornada}')
            elif liga and winner and  local:
                return redirect(reverse('Filtrar_Predicciones') + f'?liga={liga}&winner={winner}&local={local}')
            elif liga and winner and visitante:
                return redirect(reverse('Filtrar_Predicciones') + f'?liga={liga}&winner={winner}&visitante={visitante}')
            elif liga and local:
                return redirect(reverse('Filtrar_Predicciones') + f'?liga={liga}&local={local}')
            elif liga and visitante:
                return redirect(reverse('Filtrar_Predicciones') + f'?liga={liga}&visitante={visitante}')
            elif liga and jornada:
                return redirect(reverse('Filtrar_Predicciones') + f'?liga={liga}&jornada={jornada}')
            elif liga and winner:
                return redirect(reverse('Filtrar_Predicciones') + f'?liga={liga}&winner={winner}')
            elif liga:
                return redirect(reverse('Filtrar_Predicciones') + f'?liga={liga}')
            

        
    else:
        formulario = formulario_prediccion()
        partidos = PartidosPredichos.objects.all()
        page = request.GET.get('page', 1)  # Obtener el número de página de la solicitud GET
        try:
            paginator = Paginator(partidos, 10)  # 6 predicciones por página
            partidos = paginator.page(page)
            es1siendo1, es1siendoX, es1siendo2, esXsiendo1, esXsiendoX, esXsiendo2, es2siendo1, es2siendoX, es2siendo2 = mostrar_tasa_de_acierto() 
        except PageNotAnInteger:
            raise Http404

        return render(request, 'predicciones/mostrarPredicciones.html', {"formulario": formulario, "entity": partidos, "paginator": paginator, "es1siendo1": es1siendo1,
                                                                        "es1siendoX": es1siendoX, "es1siendo2": es1siendo2, "esXsiendo1": esXsiendo1,
                                                                        "esXsiendoX": esXsiendoX, "esXsiendo2": esXsiendo2, "es2siendo1": es2siendo1,
                                                                        "es2siendoX": es2siendoX, "es2siendo2": es2siendo2})


def filtrado_predicciones(request):
    liga = request.GET.get("liga")
    jornada = request.GET.get("jornada")
    local = request.GET.get("local")
    print(local)
    visitante = request.GET.get("visitante")
    winner = request.GET.get("winner")
    if liga is None:
        liga = None
    else:
        liga = liga  
    if jornada is None:
        jornada = None
    else:
        jornada = jornada
    if local is None:
        local = None
    else:
        local = local
    if local is None:
        local = None
    else:
        local = local
    if visitante is None:
        visitante = None
    else:
        visitante = visitante
    
    if jornada is None and liga is not None and visitante is None and local is None and winner is None:
        partidos = PartidosPredichos.objects.filter(liga = liga)
        page = request.GET.get('page', 1)  # Obtener el número de página de la solicitud GET
        
        try:
            paginator = Paginator(partidos, 10)  # 6 predicciones por página
            partidos = paginator.page(page)
        except PageNotAnInteger:
            raise Http404
    elif jornada is not None and liga is not None and visitante is None and local is None and winner is None:
        partidos = PartidosPredichos.objects.filter(liga = liga, jornada = jornada)
        page = request.GET.get('page', 1)  # Obtener el número de página de la solicitud GET
        
        try:
            paginator = Paginator(partidos, 10)  # 6 predicciones por página
            partidos = paginator.page(page)
        except PageNotAnInteger:
            raise Http404
    elif jornada is None and liga is not None and visitante is None and local is not None and winner is None:
        partidos = PartidosPredichos.objects.filter(liga = liga, equipo_local = local)
        page = request.GET.get('page', 1)  # Obtener el número de página de la solicitud GET
        
        try:
            paginator = Paginator(partidos, 10)  # 6 predicciones por página
            partidos = paginator.page(page)
        except PageNotAnInteger:
                raise Http404
    elif jornada is None and liga is not None and visitante is not None and local is None and winner is None:
        partidos = PartidosPredichos.objects.filter(liga = liga, equipo_visitante = visitante)
        page = request.GET.get('page', 1)  # Obtener el número de página de la solicitud GET
        
        try:
            paginator = Paginator(partidos, 10)  # 6 predicciones por página
            partidos = paginator.page(page)
        except PageNotAnInteger:
                raise Http404
    elif jornada is None and liga is not None and visitante is not None and local is not None and winner is None:
        partidos = PartidosPredichos.objects.filter(liga = liga, equipo_local = local, equipo_visitante = visitante)
        page = request.GET.get('page', 1)  # Obtener el número de página de la solicitud GET
        
        try:
            paginator = Paginator(partidos, 10)  # 6 predicciones por página
            partidos = paginator.page(page)
        except PageNotAnInteger:
                raise Http404
    elif jornada is None and liga is not None and visitante is None and local is None and winner is not None:
        partidos = PartidosPredichos.objects.filter(liga = liga, winner = winner)
        page = request.GET.get('page', 1)  # Obtener el número de página de la solicitud GET
        
        try:
            paginator = Paginator(partidos, 10)  # 6 predicciones por página
            partidos = paginator.page(page)
        except PageNotAnInteger:
                raise Http404
    elif jornada is not None and liga is not None and visitante is None and local is None and winner is not None:
        partidos = PartidosPredichos.objects.filter(liga = liga, jornada = jornada, winner = winner)
        page = request.GET.get('page', 1)  # Obtener el número de página de la solicitud GET
        
        try:
            paginator = Paginator(partidos, 10)  # 6 predicciones por página
            partidos = paginator.page(page)
        except PageNotAnInteger:
                raise Http404
    elif jornada is None and liga is not None and visitante is None and local is not None and winner is not None:
        partidos = PartidosPredichos.objects.filter(liga = liga, equipo_local = local, winner = winner)
        page = request.GET.get('page', 1)  # Obtener el número de página de la solicitud GET
        
        try:
            paginator = Paginator(partidos, 10)  # 6 predicciones por página
            partidos = paginator.page(page)
        except PageNotAnInteger:
                raise Http404
        
    elif jornada is None and liga is not None and visitante is not None and local is None and winner is not None:
        partidos = PartidosPredichos.objects.filter(liga = liga, equipo_visitante = visitante, winner = winner)
        page = request.GET.get('page', 1)  # Obtener el número de página de la solicitud GET
        
        try:
            paginator = Paginator(partidos, 10)  # 6 predicciones por página
            partidos = paginator.page(page)
        except PageNotAnInteger:
                raise Http404
    return render(request, 'predicciones/mostrarPrediccionesFiltradas.html', {"entity": partidos, "paginator":paginator})


def comparar_equipos(request):
    partidos_local_visitante = None
    existe = True
    winner = None
    partidos_cruzados = None
    ultimos_partidos_partidos_local = None
    partidos_local_siendo_local = None
    partidos_visitante_siendo_visitante = None
    ultimos_partidos_visitante = None
    local = None
    visitante = None
    escudo_local = None
    escudo_visitante = None
    prediccion = None
    max_goles_ultimos_5_partidos_equipo_local = None
    max_goles_ultimos_5_partidos_equipo_visitante = None
    max_puntos_ultimos_5_partidos_equipo_local = None
    max_puntos_ultimos_5_partidos_equipo_visitante = None
    max_goles_ultimos_5_partidos_local_siendo_local =None
    max_goles_ultimos_5_partidos_visitante_siendo_visitante = None
    max_puntos_ultimos_5_partidos_local_siendo_local = None
    max_puntos_ultimos_5_partidos_visitante_siendo_visitante = None
    min_goles_en_contra_ultimos_5_partidos_equipo_local = None
    min_goles_en_contra_ultimos_5_partidos_equipo_visitante = None
    min_goles_en_contra_ultimos_5_partidos_local_siendo_local = None
    min_goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante = None
                    
    max_goles_ultimos_3_partidos_equipo_local = None
    max_goles_ultimos_3_partidos_equipo_visitante = None
    max_puntos_ultimos_3_partidos_equipo_local = None
    max_puntos_ultimos_3_partidos_equipo_visitante = None
    max_goles_ultimos_3_partidos_local_siendo_local = None
    max_goles_ultimos_3_partidos_visitante_siendo_visitante = None
    max_puntos_ultimos_3_partidos_local_siendo_local = None
    max_puntos_ultimos_3_partidos_visitante_siendo_visitante = None
    min_goles_en_contra_ultimos_3_partidos_equipo_local = None
    min_goles_en_contra_ultimos_3_partidos_equipo_visitante = None
    min_goles_en_contra_ultimos_3_partidos_local_siendo_local = None
    min_goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante = None
    if request.method =='POST':
        formulario = formulario_prediccion(request.POST)
        if formulario.is_valid():
            local = formulario.cleaned_data["local"]
            visitante = formulario.cleaned_data["visitante"]
            if local == visitante:
                formulario = formulario_equipos()
            else:
                partidos_local_visitante=PartidosEntrenamiento.objects.filter(equipo_local = local, equipo_visitante = visitante).order_by("-id")[:5]
                partidos_cruzados = PartidosEntrenamiento.objects.filter(Q(equipo_local=local, equipo_visitante=visitante) | Q(equipo_local=visitante, equipo_visitante=local)).order_by("-id")[:5]
                ultimos_partidos_partidos_local = PartidosEntrenamiento.objects.filter(Q(equipo_local=local) | Q(equipo_visitante=local)).order_by("-id")[:5]
                partidos_local_siendo_local = PartidosEntrenamiento.objects.filter(equipo_local = local).order_by("-id")[:5]
                partidos_visitante_siendo_visitante = PartidosEntrenamiento.objects.filter(Q(equipo_visitante=visitante) | Q(equipo_local=visitante)).order_by("-id")[:5]
                ultimos_partidos_visitante = PartidosEntrenamiento.objects.filter(equipo_visitante = visitante).order_by("-id")[:5]

                p_local = PartidosPredichos.objects.filter(equipo_local = local).first()
                escudo_local = p_local.escudo_local
                p_local = PartidosPredichos.objects.filter(equipo_visitante = visitante).first()
                escudo_visitante = p_local.escudo_visitante

                prediccion = PartidosPredichos.objects.filter(equipo_local = local, equipo_visitante = visitante).first()
                if prediccion is not None:
                    prediccion = prediccion
                    existe = True
                else:
                    existe = False
                    max_goles_ultimos_5_partidos_equipo_local = PartidosEntrenamiento.objects.filter(equipo_local=local).aggregate(max_goles_ultimos_5_partidos_equipo_local=Max('goles_ultimos_5_partidos_equipo_local'))['max_goles_ultimos_5_partidos_equipo_local']
                    max_goles_ultimos_5_partidos_equipo_visitante = PartidosEntrenamiento.objects.filter(equipo_visitante=visitante).aggregate(max_goles_ultimos_5_partidos_equipo_visitante=Max('goles_ultimos_5_partidos_equipo_visitante'))['max_goles_ultimos_5_partidos_equipo_visitante']
                    max_puntos_ultimos_5_partidos_equipo_local = PartidosEntrenamiento.objects.filter(equipo_local=local).aggregate(max_puntos_ultimos_5_partidos_equipo_local=Max('puntos_ultimos_5_partidos_equipo_local'))['max_puntos_ultimos_5_partidos_equipo_local']
                    max_puntos_ultimos_5_partidos_equipo_visitante = PartidosEntrenamiento.objects.filter(equipo_visitante=visitante).aggregate(max_puntos_ultimos_5_partidos_equipo_visitante=Max('puntos_ultimos_5_partidos_equipo_visitante'))['max_puntos_ultimos_5_partidos_equipo_visitante']
                    max_goles_ultimos_5_partidos_local_siendo_local = PartidosEntrenamiento.objects.filter(equipo_local=local).aggregate(max_goles_ultimos_5_partidos_local_siendo_local=Max('goles_ultimos_5_partidos_local_siendo_local'))['max_goles_ultimos_5_partidos_local_siendo_local']
                    max_goles_ultimos_5_partidos_visitante_siendo_visitante = PartidosEntrenamiento.objects.filter(equipo_visitante=visitante).aggregate(max_goles_ultimos_5_partidos_visitante_siendo_visitante=Max('goles_ultimos_5_partidos_visitante_siendo_visitante'))['max_goles_ultimos_5_partidos_visitante_siendo_visitante']
                    max_puntos_ultimos_5_partidos_local_siendo_local = PartidosEntrenamiento.objects.filter(equipo_local=local).aggregate(max_puntos_ultimos_5_partidos_local_siendo_local=Max('puntos_ultimos_5_partidos_local_siendo_local'))['max_puntos_ultimos_5_partidos_local_siendo_local']
                    max_puntos_ultimos_5_partidos_visitante_siendo_visitante = PartidosEntrenamiento.objects.filter(equipo_visitante=visitante).aggregate(max_puntos_ultimos_5_partidos_visitante_siendo_visitante=Max('puntos_ultimos_5_partidos_visitante_siendo_visitante'))['max_puntos_ultimos_5_partidos_visitante_siendo_visitante']
                    min_goles_en_contra_ultimos_5_partidos_equipo_local = PartidosEntrenamiento.objects.filter(equipo_local=local).aggregate(min_goles_en_contra_ultimos_5_partidos_equipo_local=Min('goles_en_contra_ultimos_5_partidos_equipo_local'))['min_goles_en_contra_ultimos_5_partidos_equipo_local']
                    min_goles_en_contra_ultimos_5_partidos_equipo_visitante = PartidosEntrenamiento.objects.filter(equipo_visitante=visitante).aggregate(min_goles_en_contra_ultimos_5_partidos_equipo_visitante=Min('goles_en_contra_ultimos_5_partidos_equipo_visitante'))['min_goles_en_contra_ultimos_5_partidos_equipo_visitante']
                    min_goles_en_contra_ultimos_5_partidos_local_siendo_local = PartidosEntrenamiento.objects.filter(equipo_local=local).aggregate(min_goles_en_contra_ultimos_5_partidos_local_siendo_local=Min('goles_en_contra_ultimos_5_partidos_local_siendo_local'))['min_goles_en_contra_ultimos_5_partidos_local_siendo_local']
                    min_goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante = PartidosEntrenamiento.objects.filter(equipo_visitante=visitante).aggregate(min_goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante=Min('goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante'))['min_goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante']
                    
                    max_goles_ultimos_3_partidos_equipo_local = PartidosEntrenamiento.objects.filter(equipo_local=local).aggregate(max_goles_ultimos_3_partidos_equipo_local=Max('goles_ultimos_3_partidos_equipo_local'))['max_goles_ultimos_3_partidos_equipo_local']
                    max_goles_ultimos_3_partidos_equipo_visitante = PartidosEntrenamiento.objects.filter(equipo_visitante=visitante).aggregate(max_goles_ultimos_3_partidos_equipo_visitante=Max('goles_ultimos_3_partidos_equipo_visitante'))['max_goles_ultimos_3_partidos_equipo_visitante']
                    max_puntos_ultimos_3_partidos_equipo_local = PartidosEntrenamiento.objects.filter(equipo_local=local).aggregate(max_puntos_ultimos_3_partidos_equipo_local=Max('puntos_ultimos_3_partidos_equipo_local'))['max_puntos_ultimos_3_partidos_equipo_local']
                    max_puntos_ultimos_3_partidos_equipo_visitante = PartidosEntrenamiento.objects.filter(equipo_visitante=visitante).aggregate(max_puntos_ultimos_3_partidos_equipo_visitante=Max('puntos_ultimos_3_partidos_equipo_visitante'))['max_puntos_ultimos_3_partidos_equipo_visitante']
                    max_goles_ultimos_3_partidos_local_siendo_local = PartidosEntrenamiento.objects.filter(equipo_local=local).aggregate(max_goles_ultimos_3_partidos_local_siendo_local=Max('goles_ultimos_3_partidos_local_siendo_local'))['max_goles_ultimos_3_partidos_local_siendo_local']
                    max_goles_ultimos_3_partidos_visitante_siendo_visitante = PartidosEntrenamiento.objects.filter(equipo_visitante=visitante).aggregate(max_goles_ultimos_3_partidos_visitante_siendo_visitante=Max('goles_ultimos_3_partidos_visitante_siendo_visitante'))['max_goles_ultimos_3_partidos_visitante_siendo_visitante']
                    max_puntos_ultimos_3_partidos_local_siendo_local = PartidosEntrenamiento.objects.filter(equipo_local=local).aggregate(max_puntos_ultimos_3_partidos_local_siendo_local=Max('puntos_ultimos_3_partidos_local_siendo_local'))['max_puntos_ultimos_3_partidos_local_siendo_local']
                    max_puntos_ultimos_3_partidos_visitante_siendo_visitante = PartidosEntrenamiento.objects.filter(equipo_visitante=visitante).aggregate(max_puntos_ultimos_3_partidos_visitante_siendo_visitante=Max('puntos_ultimos_3_partidos_visitante_siendo_visitante'))['max_puntos_ultimos_3_partidos_visitante_siendo_visitante']
                    min_goles_en_contra_ultimos_3_partidos_equipo_local = PartidosEntrenamiento.objects.filter(equipo_local=local).aggregate(min_goles_en_contra_ultimos_3_partidos_equipo_local=Min('goles_en_contra_ultimos_3_partidos_equipo_local'))['min_goles_en_contra_ultimos_3_partidos_equipo_local']
                    min_goles_en_contra_ultimos_3_partidos_equipo_visitante = PartidosEntrenamiento.objects.filter(equipo_visitante=visitante).aggregate(min_goles_en_contra_ultimos_3_partidos_equipo_visitante=Min('goles_en_contra_ultimos_3_partidos_equipo_visitante'))['min_goles_en_contra_ultimos_3_partidos_equipo_visitante']
                    min_goles_en_contra_ultimos_3_partidos_local_siendo_local = PartidosEntrenamiento.objects.filter(equipo_local=local).aggregate(min_goles_en_contra_ultimos_3_partidos_local_siendo_local=Min('goles_en_contra_ultimos_3_partidos_local_siendo_local'))['min_goles_en_contra_ultimos_3_partidos_local_siendo_local']
                    min_goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante = PartidosEntrenamiento.objects.filter(equipo_visitante=visitante).aggregate(min_goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante=Min('goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante'))['min_goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante']
                    if max_goles_ultimos_5_partidos_equipo_local is None or max_goles_ultimos_3_partidos_equipo_visitante is None:
                        max_goles_ultimos_5_partidos_equipo_local = PartidoSinPredecir.objects.filter(equipo_local=local).aggregate(max_goles_ultimos_5_partidos_equipo_local=Max('goles_ultimos_5_partidos_equipo_local'))['max_goles_ultimos_5_partidos_equipo_local']
                        max_goles_ultimos_5_partidos_equipo_visitante = PartidoSinPredecir.objects.filter(equipo_visitante=visitante).aggregate(max_goles_ultimos_5_partidos_equipo_visitante=Max('goles_ultimos_5_partidos_equipo_visitante'))['max_goles_ultimos_5_partidos_equipo_visitante']
                        max_puntos_ultimos_5_partidos_equipo_local = PartidoSinPredecir.objects.filter(equipo_local=local).aggregate(max_puntos_ultimos_5_partidos_equipo_local=Max('puntos_ultimos_5_partidos_equipo_local'))['max_puntos_ultimos_5_partidos_equipo_local']
                        max_puntos_ultimos_5_partidos_equipo_visitante = PartidoSinPredecir.objects.filter(equipo_visitante=visitante).aggregate(max_puntos_ultimos_5_partidos_equipo_visitante=Max('puntos_ultimos_5_partidos_equipo_visitante'))['max_puntos_ultimos_5_partidos_equipo_visitante']
                        max_goles_ultimos_5_partidos_local_siendo_local = PartidoSinPredecir.objects.filter(equipo_local=local).aggregate(max_goles_ultimos_5_partidos_local_siendo_local=Max('goles_ultimos_5_partidos_local_siendo_local'))['max_goles_ultimos_5_partidos_local_siendo_local']
                        max_goles_ultimos_5_partidos_visitante_siendo_visitante = PartidoSinPredecir.objects.filter(equipo_visitante=visitante).aggregate(max_goles_ultimos_5_partidos_visitante_siendo_visitante=Max('goles_ultimos_5_partidos_visitante_siendo_visitante'))['max_goles_ultimos_5_partidos_visitante_siendo_visitante']
                        max_puntos_ultimos_5_partidos_local_siendo_local = PartidoSinPredecir.objects.filter(equipo_local=local).aggregate(max_puntos_ultimos_5_partidos_local_siendo_local=Max('puntos_ultimos_5_partidos_local_siendo_local'))['max_puntos_ultimos_5_partidos_local_siendo_local']
                        max_puntos_ultimos_5_partidos_visitante_siendo_visitante = PartidoSinPredecir.objects.filter(equipo_visitante=visitante).aggregate(max_puntos_ultimos_5_partidos_visitante_siendo_visitante=Max('puntos_ultimos_5_partidos_visitante_siendo_visitante'))['max_puntos_ultimos_5_partidos_visitante_siendo_visitante']
                        min_goles_en_contra_ultimos_5_partidos_equipo_local = PartidoSinPredecir.objects.filter(equipo_local=local).aggregate(min_goles_en_contra_ultimos_5_partidos_equipo_local=Min('goles_en_contra_ultimos_5_partidos_equipo_local'))['min_goles_en_contra_ultimos_5_partidos_equipo_local']
                        min_goles_en_contra_ultimos_5_partidos_equipo_visitante = PartidoSinPredecir.objects.filter(equipo_visitante=visitante).aggregate(min_goles_en_contra_ultimos_5_partidos_equipo_visitante=Min('goles_en_contra_ultimos_5_partidos_equipo_visitante'))['min_goles_en_contra_ultimos_5_partidos_equipo_visitante']
                        min_goles_en_contra_ultimos_5_partidos_local_siendo_local = PartidoSinPredecir.objects.filter(equipo_local=local).aggregate(min_goles_en_contra_ultimos_5_partidos_local_siendo_local=Min('goles_en_contra_ultimos_5_partidos_local_siendo_local'))['min_goles_en_contra_ultimos_5_partidos_local_siendo_local']
                        min_goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante = PartidoSinPredecir.objects.filter(equipo_visitante=visitante).aggregate(min_goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante=Min('goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante'))['min_goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante']
                        
                        max_goles_ultimos_3_partidos_equipo_local = PartidoSinPredecir.objects.filter(equipo_local=local).aggregate(max_goles_ultimos_3_partidos_equipo_local=Max('goles_ultimos_3_partidos_equipo_local'))['max_goles_ultimos_3_partidos_equipo_local']
                        max_goles_ultimos_3_partidos_equipo_visitante = PartidoSinPredecir.objects.filter(equipo_visitante=visitante).aggregate(max_goles_ultimos_3_partidos_equipo_visitante=Max('goles_ultimos_3_partidos_equipo_visitante'))['max_goles_ultimos_3_partidos_equipo_visitante']
                        max_puntos_ultimos_3_partidos_equipo_local = PartidoSinPredecir.objects.filter(equipo_local=local).aggregate(max_puntos_ultimos_3_partidos_equipo_local=Max('puntos_ultimos_3_partidos_equipo_local'))['max_puntos_ultimos_3_partidos_equipo_local']
                        max_puntos_ultimos_3_partidos_equipo_visitante = PartidoSinPredecir.objects.filter(equipo_visitante=visitante).aggregate(max_puntos_ultimos_3_partidos_equipo_visitante=Max('puntos_ultimos_3_partidos_equipo_visitante'))['max_puntos_ultimos_3_partidos_equipo_visitante']
                        max_goles_ultimos_3_partidos_local_siendo_local = PartidoSinPredecir.objects.filter(equipo_local=local).aggregate(max_goles_ultimos_3_partidos_local_siendo_local=Max('goles_ultimos_3_partidos_local_siendo_local'))['max_goles_ultimos_3_partidos_local_siendo_local']
                        max_goles_ultimos_3_partidos_visitante_siendo_visitante = PartidoSinPredecir.objects.filter(equipo_visitante=visitante).aggregate(max_goles_ultimos_3_partidos_visitante_siendo_visitante=Max('goles_ultimos_3_partidos_visitante_siendo_visitante'))['max_goles_ultimos_3_partidos_visitante_siendo_visitante']
                        max_puntos_ultimos_3_partidos_local_siendo_local = PartidoSinPredecir.objects.filter(equipo_local=local).aggregate(max_puntos_ultimos_3_partidos_local_siendo_local=Max('puntos_ultimos_3_partidos_local_siendo_local'))['max_puntos_ultimos_3_partidos_local_siendo_local']
                        max_puntos_ultimos_3_partidos_visitante_siendo_visitante = PartidoSinPredecir.objects.filter(equipo_visitante=visitante).aggregate(max_puntos_ultimos_3_partidos_visitante_siendo_visitante=Max('puntos_ultimos_3_partidos_visitante_siendo_visitante'))['max_puntos_ultimos_3_partidos_visitante_siendo_visitante']
                        min_goles_en_contra_ultimos_3_partidos_equipo_local = PartidoSinPredecir.objects.filter(equipo_local=local).aggregate(min_goles_en_contra_ultimos_3_partidos_equipo_local=Min('goles_en_contra_ultimos_3_partidos_equipo_local'))['min_goles_en_contra_ultimos_3_partidos_equipo_local']
                        min_goles_en_contra_ultimos_3_partidos_equipo_visitante = PartidoSinPredecir.objects.filter(equipo_visitante=visitante).aggregate(min_goles_en_contra_ultimos_3_partidos_equipo_visitante=Min('goles_en_contra_ultimos_3_partidos_equipo_visitante'))['min_goles_en_contra_ultimos_3_partidos_equipo_visitante']
                        min_goles_en_contra_ultimos_3_partidos_local_siendo_local = PartidoSinPredecir.objects.filter(equipo_local=local).aggregate(min_goles_en_contra_ultimos_3_partidos_local_siendo_local=Min('goles_en_contra_ultimos_3_partidos_local_siendo_local'))['min_goles_en_contra_ultimos_3_partidos_local_siendo_local']
                        min_goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante = PartidoSinPredecir.objects.filter(equipo_visitante=visitante).aggregate(min_goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante=Min('goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante'))['min_goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante']

                    
                    XP = np.column_stack((
                                        max_goles_ultimos_5_partidos_equipo_local,
                                        max_goles_ultimos_5_partidos_equipo_visitante,
                                        max_puntos_ultimos_5_partidos_equipo_local,
                                        max_puntos_ultimos_5_partidos_equipo_visitante,
                                        min_goles_en_contra_ultimos_5_partidos_equipo_local,
                                        min_goles_en_contra_ultimos_5_partidos_equipo_visitante,
                                        max_goles_ultimos_5_partidos_local_siendo_local,
                                        max_goles_ultimos_5_partidos_visitante_siendo_visitante,
                                        max_puntos_ultimos_5_partidos_local_siendo_local,
                                        max_puntos_ultimos_5_partidos_visitante_siendo_visitante,
                                        min_goles_en_contra_ultimos_5_partidos_local_siendo_local,
                                        min_goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante,

                                        max_goles_ultimos_3_partidos_equipo_local,
                                        max_goles_ultimos_3_partidos_equipo_visitante,
                                        max_puntos_ultimos_3_partidos_equipo_local,
                                        max_puntos_ultimos_3_partidos_equipo_visitante,
                                        min_goles_en_contra_ultimos_3_partidos_equipo_local,
                                        min_goles_en_contra_ultimos_3_partidos_equipo_visitante,
                                        max_goles_ultimos_3_partidos_local_siendo_local,
                                        max_goles_ultimos_3_partidos_visitante_siendo_visitante,
                                        max_puntos_ultimos_3_partidos_local_siendo_local,
                                        max_puntos_ultimos_3_partidos_visitante_siendo_visitante,
                                        min_goles_en_contra_ultimos_3_partidos_local_siendo_local,
                                        min_goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante))
                    X,Y = calculo_Valores_Indp_Y_Depen_Para_Datos_3_Y_5_Ultimos_Partidos()
                    X_train, X_test, winner_train, winner_test = train_test_split(X, Y, test_size=0.2, random_state=42)
                    model_gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
                    model_gbc.fit(X_train, winner_train),
                    predicciones = model_gbc.predict(XP)
                    winner = ['X' if pred == '0' else pred for pred in predicciones]



            
    else:
        formulario = formulario_equipos()
    return render(request, 'predicciones/compararEquipos.html', {"formulario":formulario, 
                                                                 "entity": partidos_local_visitante, 
                                                                 "entity2": partidos_cruzados,
                                                                 "entity3": ultimos_partidos_partidos_local,
                                                                 "entity4": partidos_local_siendo_local,
                                                                 "entity5":partidos_visitante_siendo_visitante,
                                                                 "entity6": ultimos_partidos_visitante, 
                                                                 "local":local, 
                                                                 "visitante":visitante, 
                                                                 "prediccion":prediccion,
                                                                 "winner":winner,
                                                                 "existe":existe,
                                                                 "escudo_local":escudo_local,
                                                                 "escudo_visitante":escudo_visitante,
                                                                 "goles_ultimos_5_partidos_equipo_local":max_goles_ultimos_5_partidos_equipo_local,
                                                                 "goles_ultimos_5_partidos_equipo_visitante":max_goles_ultimos_5_partidos_equipo_visitante,
                                                                 "puntos_ultimos_5_partidos_equipo_local":max_puntos_ultimos_5_partidos_equipo_local,
                                                                 "puntos_ultimos_5_partidos_equipo_visitante":max_puntos_ultimos_5_partidos_equipo_visitante,
                                                                 "goles_ultimos_5_partidos_local_siendo_local":max_goles_ultimos_5_partidos_local_siendo_local,
                                                                 "goles_ultimos_5_partidos_visitante_siendo_visitante":max_goles_ultimos_5_partidos_visitante_siendo_visitante,
                                                                 "puntos_ultimos_5_partidos_local_siendo_local":max_puntos_ultimos_5_partidos_local_siendo_local,
                                                                 "puntos_ultimos_5_partidos_visitante_siendo_visitante":max_puntos_ultimos_5_partidos_visitante_siendo_visitante,
                                                                 "goles_en_contra_ultimos_5_partidos_equipo_local":min_goles_en_contra_ultimos_5_partidos_equipo_local,
                                                                 "goles_en_contra_ultimos_5_partidos_equipo_visitante":min_goles_en_contra_ultimos_5_partidos_equipo_visitante,
                                                                 "goles_en_contra_ultimos_5_partidos_local_siendo_local":min_goles_en_contra_ultimos_5_partidos_local_siendo_local,
                                                                 "goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante":min_goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante,

                                                                 "goles_ultimos_3_partidos_equipo_local":max_goles_ultimos_3_partidos_equipo_local,
                                                                 "goles_ultimos_3_partidos_equipo_visitante":max_goles_ultimos_3_partidos_equipo_visitante,
                                                                 "puntos_ultimos_3_partidos_equipo_local":max_puntos_ultimos_3_partidos_equipo_local,
                                                                 "puntos_ultimos_3_partidos_equipo_visitante":max_puntos_ultimos_3_partidos_equipo_visitante,
                                                                 "goles_ultimos_3_partidos_local_siendo_local":max_goles_ultimos_3_partidos_local_siendo_local,
                                                                 "goles_ultimos_3_partidos_visitante_siendo_visitante":max_goles_ultimos_3_partidos_visitante_siendo_visitante,
                                                                 "puntos_ultimos_3_partidos_local_siendo_local":max_puntos_ultimos_3_partidos_local_siendo_local,
                                                                 "puntos_ultimos_3_partidos_visitante_siendo_visitante":max_puntos_ultimos_3_partidos_visitante_siendo_visitante,
                                                                 "goles_en_contra_ultimos_3_partidos_equipo_local":min_goles_en_contra_ultimos_3_partidos_equipo_local,
                                                                 "goles_en_contra_ultimos_3_partidos_equipo_visitante":min_goles_en_contra_ultimos_3_partidos_equipo_visitante,
                                                                 "goles_en_contra_ultimos_3_partidos_local_siendo_local":min_goles_en_contra_ultimos_3_partidos_local_siendo_local,
                                                                 "goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante":min_goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante,
                                                                 })

def crear_quiniela(request):
    if  request.user.is_authenticated and request.user.is_staff:
        mensaje = None
        if request.method == 'POST':
            formulario = formulario_quiniela(request.POST)

            if formulario.is_valid():
                partido1 = formulario.cleaned_data['partido1']
                partido2 = formulario.cleaned_data['partido2']
                partido3 = formulario.cleaned_data['partido3']
                partido4 = formulario.cleaned_data['partido4']
                partido5 = formulario.cleaned_data['partido5']
                partido6 = formulario.cleaned_data['partido6']
                partido7 = formulario.cleaned_data['partido7']
                partido8 = formulario.cleaned_data['partido8']
                partido9 = formulario.cleaned_data['partido9']
                partido10 = formulario.cleaned_data['partido10']

                num_porra_abierta = Quiniela.objects.filter(abierta =True).count()
                if num_porra_abierta ==1:
                    formulario = formulario_quiniela()
                    mensaje = "Hay un porra abierta, cierrala antes de crear una nueva"
                elif partido1 == partido2 or partido1 == partido3 or partido1 == partido4 or partido1 == partido5 or partido2 == partido3 or partido2 == partido4 or partido2 == partido5 or partido3 == partido4 or partido3 == partido5 or partido4 == partido5:
                    formulario = formulario_quiniela()
                    mensaje = "Hay algun partido repetido"
                elif partido6 == partido7 or partido6 == partido8 or partido6 == partido9 or partido6 == partido10 or partido7 == partido8 or partido7 == partido9 or partido7 == partido10 or partido8 == partido9 or partido8 == partido10 or partido9 == partido10:
                    formulario = formulario_quiniela()
                    mensaje = "Hay algun partido repetido"
                else:
                    Quiniela.objects.create(primer_partido = partido1, segundo_partido = partido2, tercer_partido = partido3, cuarto_partido = partido4, quinto_partido= partido5, sexto_partido = partido6, septimo_partido = partido7, octavo_partido=partido8, noveno_partido = partido9, decimo_partido = partido10)
                    usuarios = CustomUser.objects.all()
                    for usuario in usuarios:
                        email = usuario.email
                        envio_email = EmailMessage("Nueva Porra Disponible", "Se ha abierto una nueva porra con nuevos partidos para participar, no se olvides de conseguir sus puntos y escalar en el Ranking. Mucha suerte!","",[email], reply_to=["playfullpredictions@gmail.com"])
                        try:
                            envio_email.send()
                        except:
                            return redirect(reverse('Crear_Quiniela') + f'?novalido')
                    return redirect('Home')
        else:
           formulario = formulario_quiniela()

        return render(request, 'predicciones/crearQuiniela.html', {'formulario': formulario, "mensaje": mensaje})
    else:
        return redirect('Home')

def mostrar_quiniela(request):
    if request.user.is_authenticated:
        num_quiniela = Quiniela.objects.filter(abierta = True).count()
        num_quinielas_total = Quiniela.objects.all().count()
        if num_quiniela == 0:
            return render(request, 'predicciones/noQuiniela.html', {"numero":num_quinielas_total})
        
        else:
            quiniela = Quiniela.objects.filter(abierta = True).first()
            num_porras_usuario_total = Porra.objects.filter(usuario = request.user).count()
            num_esta_porra_hechas = Porra.objects.filter(quiniela=quiniela, usuario = request.user).count()
            print(num_porras_usuario_total)
            print(num_esta_porra_hechas)
            return render(request, 'predicciones/mostrarQuiniela.html', {"quiniela": quiniela, "num_quiniela": num_quinielas_total,"num_esta_porra_hechas":num_esta_porra_hechas, "num_porras_usuario":num_porras_usuario_total})
    else:
        return render(request, 'predicciones/pedirInicio.html')
    
def realizar_porra(request):
    if  request.user.is_authenticated and not request.user.is_staff:
        quiniela = Quiniela.objects.filter(abierta = True)
        for q in quiniela:
            num_porras = Porra.objects.filter(quiniela=q, usuario = request.user).count()
        if num_porras >= 1:
            return render(request, 'predicciones/quinielaHecha.html')
        if request.method == 'POST':
            formulario = formulario_porra(request.POST)

            if formulario.is_valid():
                partido1 = formulario.cleaned_data['partido1']
                partido2 = formulario.cleaned_data['partido2']
                partido3 = formulario.cleaned_data['partido3']
                partido4 = formulario.cleaned_data['partido4']
                partido5 = formulario.cleaned_data['partido5']
                partido6 = formulario.cleaned_data['partido6']
                partido7 = formulario.cleaned_data['partido7']
                partido8 = formulario.cleaned_data['partido8']
                partido9 = formulario.cleaned_data['partido9']
                partido10 = formulario.cleaned_data['partido10']

                quiniela = Quiniela.objects.filter(abierta = True).first()
                Porra.objects.create(primer_partido = partido1, segundo_partido = partido2, tercer_partido = partido3, cuarto_partido = partido4, quinto_partido= partido5, sexto_partido = partido6, septimo_partido = partido7, octavo_partido=partido8, noveno_partido = partido9, decimo_partido = partido10, quiniela = quiniela, usuario = request.user)
                email = request.user.email
                primer_partido = quiniela.primer_partido
                segundo_partido = quiniela.segundo_partido
                tercer_partido = quiniela.tercer_partido
                cuarto_partido = quiniela.cuarto_partido
                quinto_partido = quiniela.quinto_partido
                sexto_partido = quiniela.sexto_partido
                septimo_partido = quiniela.septimo_partido
                octavo_partido = quiniela.octavo_partido
                noveno_partido = quiniela.noveno_partido
                decimo_partido = quiniela.decimo_partido
                
                envio_email = EmailMessage("Porra Realizada Correctamente", "Tu porra se ha relizado correctamete, aquí tienes tus prediciones:\n {}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}\n Gracias por participar y mucha suerte".format(primer_partido,partido1,segundo_partido,partido2,tercer_partido,partido3,cuarto_partido,partido4,quinto_partido,partido5,sexto_partido,partido6,septimo_partido,partido7,octavo_partido,partido8,noveno_partido,partido9,decimo_partido,partido10),"",[email], reply_to=["playfullpredictions@gmail.com"])
                try:
                    envio_email.send()
                except:
                    return redirect(reverse('Realizar_Porra') + f'?novalido')
                return redirect('Mostrar_Quiniela')
                

        else:
           formulario = formulario_porra()

        return render(request, 'predicciones/realizarPorra.html', {'formulario': formulario, "entity":quiniela})
    else:
        return redirect('Home')
    
def mostrar_quinielas_creadas(request):
    if request.user.is_authenticated and request.user.is_staff:
        quiniela = Quiniela.objects.all()
        page = request.GET.get('page', 1)  
        
        try:
            paginator = Paginator(quiniela, 6) 
            quinielas = paginator.page(page)
        except PageNotAnInteger:
            raise Http404
        
        return render(request, 'predicciones/mostrarQuinielasCreadas.html', {"entity": quinielas, "paginator":paginator})
    else:
        return redirect('Home')
    

def mostrar_usuarios_participes_quinielas(request, quiniela_id):
    if request.user.is_authenticated and request.user.is_staff:
        quiniela = Quiniela.objects.filter(id = quiniela_id).first()
        abierta = quiniela.abierta
        porra = Porra.objects.filter(quiniela__id = quiniela_id)
        num_usuarios = porra.count()
        page = request.GET.get('page', 1)  
        
        try:
            paginator = Paginator(porra, 6) 
            porras = paginator.page(page)
        except PageNotAnInteger:
            raise Http404
        
        return render(request, 'predicciones/mostrarUsuariosQuinielas.html', {"entity":porras, "paginator":paginator, "abierta":abierta, "num_usuarios":num_usuarios})
    else:
        return redirect('Home')
    
def mostrar_porras_pasadas(request):
    if request.user.is_authenticated and not request.user.is_staff:
        porra = Porra.objects.filter(usuario = request.user)
        page = request.GET.get('page', 1)  
        
        try:
            paginator = Paginator(porra, 6) 
            porras = paginator.page(page)
        except PageNotAnInteger:
            raise Http404
        
        return render(request, 'predicciones/mostrarPorrasPasadas.html', {"entity":porras, "paginator":paginator})
    else:
        return redirect('Home')
    
def cerrar_quiniela_calcular_puntos(request):
    if request.user.is_authenticated and request.user.is_staff:
        quiniela = Quiniela.objects.filter(abierta = True).first()
        porras = Porra.objects.filter(quiniela=quiniela, sin_puntuar = True)
        usuarios = [porra.usuario for porra in porras]
        num_porra = porras.count()
        if num_porra >=2:
            puntos = 0
            for porra in porras:
                puntos = 0
                partido1 = porra.primer_partido
                local = quiniela.primer_partido.equipo_local
                visitante = quiniela.primer_partido.equipo_visitante
                real = PartidoReal.objects.filter(equipo_local = local, equipo_visitante = visitante).first()
                if partido1 == real.winner:
                    puntos = puntos +1
                partido2 = porra.segundo_partido
                local = quiniela.segundo_partido.equipo_local
                visitante = quiniela.segundo_partido.equipo_visitante
                real = PartidoReal.objects.filter(equipo_local = local, equipo_visitante = visitante).first()
                if partido2 == real.winner:
                    puntos = puntos +1
                partido3 = porra.tercer_partido
                local = quiniela.tercer_partido.equipo_local
                visitante = quiniela.tercer_partido.equipo_visitante
                real = PartidoReal.objects.filter(equipo_local = local, equipo_visitante = visitante).first()
                if partido3 == real.winner:
                    puntos = puntos +1
                partido4 = porra.cuarto_partido
                local = quiniela.cuarto_partido.equipo_local
                visitante = quiniela.cuarto_partido.equipo_visitante
                real = PartidoReal.objects.filter(equipo_local = local, equipo_visitante = visitante).first()
                if partido4 == real.winner:
                    puntos = puntos +1
                partido5 = porra.quinto_partido
                local = quiniela.quinto_partido.equipo_local
                visitante = quiniela.quinto_partido.equipo_visitante
                real = PartidoReal.objects.filter(equipo_local = local, equipo_visitante = visitante).first()
                if partido5 == real.winner:
                    puntos = puntos +1
                partido6 = porra.sexto_partido
                local = quiniela.sexto_partido.equipo_local
                visitante = quiniela.sexto_partido.equipo_visitante
                real = PartidoReal.objects.filter(equipo_local = local, equipo_visitante = visitante).first()
                if partido6 == real.winner:
                    puntos = puntos +1
                partido7 = porra.septimo_partido
                local = quiniela.septimo_partido.equipo_local
                visitante = quiniela.septimo_partido.equipo_visitante
                real = PartidoReal.objects.filter(equipo_local = local, equipo_visitante = visitante).first()
                if partido7 == real.winner:
                    puntos = puntos +1
                partido8 = porra.octavo_partido
                local = quiniela.octavo_partido.equipo_local
                visitante = quiniela.octavo_partido.equipo_visitante
                real = PartidoReal.objects.filter(equipo_local = local, equipo_visitante = visitante).first()
                if partido8 == real.winner:
                    puntos = puntos +1
                partido9 = porra.noveno_partido
                local = quiniela.noveno_partido.equipo_local
                visitante = quiniela.noveno_partido.equipo_visitante
                real = PartidoReal.objects.filter(equipo_local = local, equipo_visitante = visitante).first()
                if partido9 == real.winner:
                    puntos = puntos +1
                partido10 = porra.decimo_partido
                local = quiniela.decimo_partido.equipo_local
                visitante = quiniela.decimo_partido.equipo_visitante
                real = PartidoReal.objects.filter(equipo_local = local, equipo_visitante = visitante).first()
                if partido10 == real.winner:
                    puntos = puntos +1
                porra.sin_puntuar = False
                porra.puntos = puntos
                porra.save()
            
            quiniela.abierta = False
            quiniela.save()
            for usuario in usuarios:
                email = usuario.email
                envio_email = EmailMessage("Puntos Repartidos", "Ya están dispoonibles los puntos conseguidos en las porras realizadas en la última quiniela. Accede a la web para ver tu posición en el Ranking","",[email], reply_to=["playfullpredictions@gmail.com"])
                try:
                    envio_email.send()
                except:
                    return redirect(reverse('Mostrar_Quiniela') + f'?novalido')
            return redirect('Mostrar_Quiniela')
        else:
            return redirect('Mostrar_Quiniela')
    else:
        return redirect('Home')
    

def ranking(request):
    usuarios = CustomUser.objects.filter(is_staff = False)
    for usuario in usuarios:
        puntos = 0
        porras = Porra.objects.filter(usuario = usuario)
        for porra in porras:
            puntos += porra.puntos
        usuario.puntos = puntos
        usuario.save()
    usuarios = CustomUser.objects.filter(is_staff = False).order_by('-puntos')
    page = request.GET.get('page', 1) 
    try:
        paginator = Paginator(usuarios, 10)
        usuarios = paginator.page(page)
    except PageNotAnInteger:
        raise Http404
    return render(request, "predicciones/ranking.html", {"entity":usuarios, "paginator":paginator })

def buscar(request):
    if request.GET["usern"]:
        user = request.GET["usern"]
        if len(user)>20:
            return render('Home')
        else:
            usuario = CustomUser.objects.filter(username__icontains=user)
            return render(request, "predicciones/busquedaUsuario.html", {"usuario":usuario})
        

def mostrar_tasa_de_acierto():
    partidos_predichos = PartidosPredichos.objects.all()
    es1siendo1 = 0
    es1siendoX = 0
    es1siendo2 = 0
    esXsiendo1 = 0
    esXsiendoX = 0
    esXsiendo2 = 0
    es2siendo1 = 0
    es2siendoX = 0
    es2siendo2 = 0

    for p in partidos_predichos:
        local = p.equipo_local
        visitante = p.equipo_visitante
        winner_predichos = p.winner

        partido_real = PartidoReal.objects.filter(equipo_local = local, equipo_visitante = visitante).first()
        winner_real = partido_real.winner

        if winner_predichos == '1' and winner_real == '1':
            es1siendo1 += 1
        elif winner_predichos == '1' and winner_real == 'X':
            es1siendoX += 1
        elif winner_predichos == '1' and winner_real == '2':
            es1siendo2 += 1
        elif winner_predichos == 'X' and winner_real == '1':
            esXsiendo1 += 1
        elif winner_predichos == 'X' and winner_real == 'X':
            esXsiendoX += 1
        elif winner_predichos == 'X' and winner_real == '2':
            esXsiendo2 += 1
        elif winner_predichos == '2' and winner_real == '1':
            es2siendo1 += 1
        elif winner_predichos == '2' and winner_real == 'X':
            es2siendoX += 1
        elif winner_predichos == '2' and winner_real == '2':
            es2siendo2 += 1
    return es1siendo1,es1siendoX,es1siendo2,esXsiendo1,esXsiendoX,esXsiendo2,es2siendo1,es2siendoX,es2siendo2

        



        



    
