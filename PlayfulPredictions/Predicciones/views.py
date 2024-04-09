from django.shortcuts import render
from .populateDB import populateDatabaseEntrenamiento, populateDatabaseReal, populateDatabaseSinPredecir
from .models import PartidosEntrenamiento, PartidoReal, PartidoSinPredecir
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
from scipy.stats import randint
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, roc_auc_score, roc_curve, precision_recall_curve, auc
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from imblearn.over_sampling import SMOTE

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



