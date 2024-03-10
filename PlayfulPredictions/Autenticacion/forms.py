from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={'autofocus': True}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'password']