
from django.urls import path, include
from .views import cargar_Datos_Entreanmiento, cargar_Datos_Real, cargar_Datos_Sin_Predecir
urlpatterns = [
    path("entrenamiento/", cargar_Datos_Entreanmiento, name="Cargar_Datos_Entrenamiento"),
    path("real/", cargar_Datos_Real, name="Cargar_Datos_Real"),
    path("sin_predecir/", cargar_Datos_Sin_Predecir, name="Cargar_Datos_Sin_Predecir"),
]