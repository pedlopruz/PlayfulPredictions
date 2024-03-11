from django.contrib import admin
from django.urls import path, include
from .views import registro, cerrar_Session, iniciar_Sesion, actualizar_Perfil, actualizar_Contraseña

urlpatterns = [
    path('register/',registro, name="register"),
    path('cerrarSesion/',cerrar_Session, name="logout"),
    path('iniciarSesion/',iniciar_Sesion, name="login"),
    path('actualizarPerfil/', actualizar_Perfil, name="perfil"),
    path('actualizarContraseña/', actualizar_Contraseña, name="pass")
    
]