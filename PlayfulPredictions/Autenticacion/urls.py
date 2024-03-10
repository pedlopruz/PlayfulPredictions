from django.contrib import admin
from django.urls import path, include
from .views import registro, cerrar_Session, iniciar_Sesion

urlpatterns = [
     path('register/',registro, name="register"),
    path('cerrarSesion/',cerrar_Session, name="logout"),
    path('iniciarSesion/',iniciar_Sesion, name="login"),
    
]