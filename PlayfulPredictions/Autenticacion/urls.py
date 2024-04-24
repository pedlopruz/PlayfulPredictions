from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('register/',registro, name="register"),
    path('cerrarSesion/',cerrar_Session, name="logout"),
    path('iniciarSesion/',iniciar_Sesion, name="login"),
    path('actualizarPerfil/', actualizar_Perfil, name="perfil"),
    path('actualizarContraseña/', actualizar_Contraseña, name="pass"),
    path('gestionUsuarios/', listar_Usuarios_Admin, name="user_admin"),
    path('eliminarusuario/<int:user_id>/', eliminar_Usuarios_Admin, name="user_delete"),
    path('gestionUsuarios/buscar/', buscar),
    path('mostrarTerminos/', mostrar_terminos, name='mostrar_terminos'),
    path('recuperarContraseña/', recuperar_contraseña, name="Recuperar_Contraseña"),
    path('cambiarContraseña/<int:user_id>/', cambiar_Contraseña, name="Cambiar_Contraseña"),
    
]