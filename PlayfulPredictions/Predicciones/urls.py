
from django.urls import path, include
from .views import cargar_Datos_Entreanmiento, cargar_Datos_Real
urlpatterns = [
    path("entrenamiento/", cargar_Datos_Entreanmiento, name="Cargar_Datos_Entrenamiento"),
    path("real/", cargar_Datos_Real, name="Cargar_Datos_Real"),
]