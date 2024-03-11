from django.shortcuts import render, redirect
from .forms import UserForm, UserFormWithoutPassword, UserPasswordForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
# Create your views here.

def registro(request):
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

    return render(request, 'autenticacion/registro.html', {'user_form': user_form})

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
    
def listar_Usuarios_Admin(request):
    if request.user.is_authenticated and request.user.is_staff:
        usuarios = CustomUser.objects.all()
        return render(request, 'autenticacion/usuariosAdmin.html', {"usuarios": usuarios})
    else:
        return redirect('Home')