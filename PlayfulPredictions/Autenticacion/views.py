from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
from django.core.paginator import Paginator, PageNotAnInteger
from django.http import Http404
import os
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse
from django.core.mail import EmailMessage
from django.http import request
# Create your views here.

def registro(request):
    mensaje = None
    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():

            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            user = authenticate(username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password'])
            login(request, user)

            return redirect('Home') 

    else:
        user_form = UserForm()

    return render(request, 'autenticacion/registro.html', {'user_form': user_form, 'mensaje' : mensaje})

def iniciar_Sesion(request):
    formulario = AuthenticationForm()
    if request.method=='POST':
        formulario = AuthenticationForm(request.POST)
        usuario=request.POST['username']
        clave=request.POST['password']
        acceso=authenticate(username=usuario,password=clave)
        if acceso is not None:
            if acceso.is_active:
                login(request, acceso)
                return redirect('Home')
            else:
                return render(request, 'autenticacion/ingresar.html', {'mensaje':"Usuario o Contraseña Incorrecta",'formulario':formulario})
        else:
            return render(request, 'autenticacion/ingresar.html', {'mensaje':"Usuario Incorrecto o Contraseña Incorrecta",'formulario':formulario})
                     
    return render(request, 'autenticacion/ingresar.html', {'formulario':formulario})


def cerrar_Session(request):
    logout(request)
    return redirect('Home')


def actualizar_Perfil(request):
    if  request.user.is_authenticated:

        if request.method == 'POST':
            user_form = UserFormWithoutPassword(request.POST, instance=request.user)

            if user_form.is_valid():
                user = user_form.save(commit=False)
                user.save()
                user = authenticate(username=user_form.cleaned_data['username'], password=request.user.password)
                login(request, user)
                return redirect('Home')

        else:
            user_form = UserFormWithoutPassword(instance=request.user)

        return render(request, 'autenticacion/perfil.html', {'user_form': user_form})
    else:
        return redirect('Home')

def actualizar_Contraseña(request):
    if  request.user.is_authenticated:
        if request.method == 'POST':
            user_form = UserPasswordForm(request.POST)

            if user_form.is_valid():
                password1 = user_form.cleaned_data['password']
                password2 = user_form.cleaned_data['password2']
                if password1 == password2:
                    # Cambiar la contraseña del usuario
                    request.user.set_password(password2)
                    request.user.save()
                    
                    # Autenticar al usuario con la nueva contraseña
                    user = authenticate(username=request.user.username, password=password2)
                    login(request, user)
                    
                    return redirect('Home')
                else:
                    return render(request, 'autenticacion/password.html', {'mensaje':"Contraseñas no coinciden",'user_form': user_form})

        else:
            user_form = UserPasswordForm()

        return render(request, 'autenticacion/password.html', {'user_form': user_form})
    else:
        return redirect('Home')
    
def recuperar_contraseña(request):
    if request.method == 'POST':
        user_form = EmailForm(request.POST)
        if user_form.is_valid():
            email = user_form.cleaned_data['email']
            usuario = CustomUser.objects.filter(email = email).first()
            if usuario is not None:
                url = reverse('Cambiar_Contraseña', args=[usuario.id])
                url = request.build_absolute_uri(url)
                envio_email = EmailMessage("Cambio de contraseña", "Hola, {} \n Para cambiar de contraseña acceda al siguiente enlace\n {}".format(usuario.username, url),"",[email], reply_to=["playfullpredictions@gmail.com"])
                try:
                    envio_email.send()
                except:
                    return redirect(reverse('Mostrar_Quiniela') + f'?novalido')
                    
                return redirect('Home')
            else:
                return render(request, 'autenticacion/recuperarPassword.html', {'mensaje':"Email no encontrado",'user_form': user_form})
    else:
        user_form = EmailForm()

    return render(request, 'autenticacion/recuperarPassword.html', {'user_form': user_form})
    
def cambiar_Contraseña(request, user_id):
    if request.method == 'POST':
        user_form = UserPasswordForm(request.POST)

        if user_form.is_valid():
            password1 = user_form.cleaned_data['password']
            password2 = user_form.cleaned_data['password2']
            usuario = CustomUser.objects.filter(id = user_id).first()
            if usuario is None:
                return redirect('Home')
            if password1 == password2:
                # Cambiar la contraseña del usuario
                usuario.set_password(password2)
                usuario.save() 
                return redirect('Home')
            else:
                return render(request, 'autenticacion/cambiarPassword.html', {'mensaje':"Contraseñas no coinciden",'user_form': user_form})

    else:
        user_form = UserPasswordForm()

    return render(request, 'autenticacion/cambiarPassword.html', {'user_form': user_form})
    
    
def listar_Usuarios_Admin(request):
    if request.user.is_authenticated and request.user.is_staff:
        usuarios = CustomUser.objects.all()
        page = request.GET.get('page', 1)  # Obtener el número de página de la solicitud GET
        
        try:
            paginator = Paginator(usuarios, 6)  # 6 usuarios por página
            usuarios = paginator.page(page)
        except PageNotAnInteger:
            raise Http404
        
        return render(request, 'autenticacion/usuariosAdmin.html', {"entity": usuarios, "paginator":paginator})
    else:
        return redirect('Home')
    
def eliminar_Usuarios_Admin(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_admin') 

    return render(request, 'autenticacion/eliminarUsuarios.html', {'usuarios': user})
    

def buscar(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.GET["usern"]:
            user = request.GET["usern"]
            if len(user)>20:
               return render('Home')
            else:
                usuario = CustomUser.objects.filter(username__icontains=user)
                return render(request, "autenticacion/busquedaUsuario.html", {"usuario":usuario})
        else:
            return redirect('user_admin')
    else:
        return render('Home')
    
def mostrar_terminos(request):
    ruta_pdf = os.path.join(settings.BASE_DIR, 'data', 'Términos_y_condiciones_de_Uso.pdf')
    if os.path.exists(ruta_pdf):
        with open(ruta_pdf, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="documento.pdf"'
            return response
    else:
        return HttpResponse("El archivo PDF no se encontró.", status=404)