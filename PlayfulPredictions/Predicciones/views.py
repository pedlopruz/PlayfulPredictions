from django.shortcuts import render
from .populateDB import populateDatabaseEntrenamiento, populateDatabaseReal, populateDatabaseSinPredecir
from .models import PartidosEntrenamiento, PartidoReal, PartidoSinPredecir
# Create your views here.
def cargar_Datos_Entreanmiento(request):
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
        mensaje = "Se ha creado %d partidos real" % (partidos_real)
    else: 
        mensaje = "No funciona"
    return render(request, 'predicciones/conjuntoEntrenamiento.html', {"mensaje": mensaje})