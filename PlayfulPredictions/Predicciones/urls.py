
from django.urls import path, include
from .views import cargar_Datos
urlpatterns = [
    path("entrenamiento/", cargar_Datos, name="CargarDatos"),
]