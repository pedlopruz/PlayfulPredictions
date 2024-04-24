from django.urls import path, include
from .views import *
urlpatterns = [
   path("entrenamiento/", cargar_Datos_Entrenamiento, name="Cargar_Datos_Entrenamiento"),
   path("sin_predecir/", cargar_Datos_Sin_Predecir, name="Cargar_Datos_Sin_Predecir"),
   path("eliminar/", eliminarPartidodeEntrenamiento, name="Eliminar"),
   path("eliminar_sin_predecir/", eliminarPartidoSinPredecir, name="Eliminar Sin Predecir"),
   path("exportar/csv", PartidoEntrenamientoExportToCsv, name="Exportar"),
   path("predecir/bayes/5_partidos",entrenamiento_Modelo_Bayes_Para_Datos_5_Ultimos_Partidos),
   path("predecir/bayes/cruzada",entrenamiento_Modelo_Bayes_Con_Validacion_Cruzada_Para_Datos_5_Ultimos_Partidos),
   path("predecir/knn/5_partidos",entrenamiento_Modelo_KNN_Para_Datos_5_Ultimos_Partidos),
   path("predecir/randomForest/5_partidos",entrenamiento_Modelo_Random_Forest_Para_Datos_5_Ultimos_Partidos),
   path("predecir/SVM/5_partidos",entrenamiento_Modelo_SVM_Para_Datos_5_Ultimos_Partidos),
   path("predecir/LR/5_partidos",entrenamiento_Modelo_LR_Para_Datos_5_Ultimos_Partidos),
   path("predecir/GBC/5_partidos",entrenamiento_Modelo_Gradient_Boosting_Classifier_Para_Datos_5_Ultimos_Partidos),

   path("predecir/bayes/3_partidos",entrenamiento_Modelo_Bayes_Para_Datos_3_Ultimos_Partidos),
   path("predecir/knn/3_partidos",entrenamiento_Modelo_KNN_Para_Datos_3_Ultimos_Partidos),
   path("predecir/randomForest/3_partidos",entrenamiento_Modelo_Random_Forest_Para_Datos_3_Ultimos_Partidos),
   path("predecir/SVM/3_partidos",entrenamiento_Modelo_SVM_Para_Datos_3_Ultimos_Partidos),
   path("predecir/LR/3_partidos",entrenamiento_Modelo_LR_Para_Datos_3_Ultimos_Partidos),
   path("predecir/GBC/3_partidos",entrenamiento_Modelo_Gradient_Boosting_Classifier_Para_Datos_3_Ultimos_Partidos),

   path("predecir/bayes/3_y_5_partidos",entrenamiento_Modelo_Bayes_Para_Datos_3_Y_5_Ultimos_Partidos),
   path("predecir/knn/3_y_5_partidos",entrenamiento_Modelo_KNN_Para_Datos_3_Y_5_Ultimos_Partidos),
   path("predecir/randomForest/3_y_5_partidos",entrenamiento_Modelo_Random_Forest_Para_Datos_3_Y_5_Ultimos_Partidos),
   path("predecir/SVM/3_y_5_partidos",entrenamiento_Modelo_SVM_Para_Datos_3_Y_5_Ultimos_Partidos),
   path("predecir/LR/3_y_5_partidos",entrenamiento_Modelo_LR_Para_Datos_3_Y_5_Ultimos_Partidos),
   path("predecir/GBC/3_y_5_partidos",entrenamiento_Modelo_Gradient_Boosting_Classifier_Para_Datos_3_Y_5_Ultimos_Partidos),

   path("predecir/partidos_sin_predecir", prediccion_partidos_sin_predecir),
   path("mostrarPredicciones/", mostrar_predicciones, name = "Partidos_Predichos"),
   path("filtrarPredicciones/", filtrado_predicciones, name = "Filtrar_Predicciones"),
   path("compararEquipos/", comparar_equipos, name = "Comparar_Equipos"),
   path("crearQuiniela/", crear_quiniela, name = "Crear_Quiniela"),
   path("mostrarQuiniela/", mostrar_quiniela, name = "Mostrar_Quiniela"),
   path("realizarPorra/", realizar_porra, name = "Realizar_Porra"),
   path("mostrarQuinielasCreadas/", mostrar_quinielas_creadas, name = "Mostrar_Quinielas_Creadas"),
   path("mostrarUsuariosQuinielas/<int:quiniela_id>/", mostrar_usuarios_participes_quinielas, name = "Mostrar_Usuarios_Participes"),
   path("mostrarPorrasPasadas/", mostrar_porras_pasadas, name = "Mostrar_Porras_Pasadas"),
   path("cerrarPorra/", cerrar_quiniela_calcular_puntos, name = "Cerrar_Porra"),
   path("ranking/", ranking, name = "Ranking"),
   path('ranking/buscar/', buscar),
   path('estadisticas/', mostrar_tasa_de_acierto),

   
]