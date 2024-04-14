from django.contrib import admin
from django.urls import path, include
from .views import registro, cerrar_Session, iniciar_Sesion, actualizar_Perfil, actualizar_Contraseña, listar_Usuarios_Admin, eliminar_Usuarios_Admin,buscar

urlpatterns = [
    path('register/',registro, name="register"),
    path('cerrarSesion/',cerrar_Session, name="logout"),
    path('iniciarSesion/',iniciar_Sesion, name="login"),
    path('actualizarPerfil/', actualizar_Perfil, name="perfil"),
    path('actualizarContraseña/', actualizar_Contraseña, name="pass"),
    path('gestionUsuarios/', listar_Usuarios_Admin, name="user_admin"),
    path('eliminarusuario/<int:user_id>/', eliminar_Usuarios_Admin, name="user_delete"),
    path('gestionUsuarios/buscar/', buscar),
    
]