from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    username = forms.CharField(label="Username")
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={'autofocus': True}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'password']

class UserFormWithoutPassword(forms.ModelForm):
    username = forms.CharField(label="Username")
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={'autofocus': True}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email']

class UserPasswordForm(forms.Form):
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

class LoginForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['username', 'password']