from django.urls import path, include
from .views import cargar_Datos_Real, cargar_Datos_Sin_Predecir, cargar_Datos_Entrenamiento, eliminarPartidodeEntrenamiento, PartidoEntrenamientoExportToCsv, eliminarPartidoSinPredecir
urlpatterns = [
   path("entrenamiento/", cargar_Datos_Entrenamiento, name="Cargar_Datos_Entrenamiento"),
   path("real/", cargar_Datos_Real, name="Cargar_Datos_Real"),
   path("sin_predecir/", cargar_Datos_Sin_Predecir, name="Cargar_Datos_Sin_Predecir"),
   path("eliminar/", eliminarPartidodeEntrenamiento, name="Eliminar"),
   path("eliminar_sin_predecir/", eliminarPartidoSinPredecir, name="Eliminar Sin Predecir"),
   path("exportar/csv", PartidoEntrenamientoExportToCsv, name="Exportar"),
]