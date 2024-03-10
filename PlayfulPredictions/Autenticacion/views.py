from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
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
                return messages.error(request, "Usuario no encontrado")
        else:
            return messages.error(request, "Información Incorrecta")
                     
    return render(request, 'autenticacion/ingresar.html', {'formulario':formulario})


def cerrar_Session(request):
    logout(request)
    return redirect('Home')