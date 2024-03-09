from django.shortcuts import render
from .populateDB import populateDatabase
from .models import PartidosEntrenamiento
# Create your views here.
def cargar_Datos(request):
    if populateDatabase():
        populateDatabase()
        partidos_entrenamiento = PartidosEntrenamiento.objects.all().count()
        mensaje = "Se ha creado %d partidos entrenamiento" % (partidos_entrenamiento)
    else: 
        mensaje = "No funciona"
    return render(request, 'predicciones/conjuntoEntrenamiento.html', {"mensaje": mensaje})