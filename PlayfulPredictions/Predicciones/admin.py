from django.contrib import admin
from .models import PartidosEntrenamiento, PartidoReal, PartidoSinPredecir, PartidosPredichos
# Register your models here.

admin.site.register(PartidosEntrenamiento)
admin.site.register(PartidoReal)
admin.site.register(PartidoSinPredecir)
admin.site.register(PartidosPredichos)