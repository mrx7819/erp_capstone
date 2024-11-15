# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email", 
        widget=forms.EmailInput(attrs={
            'placeholder': 'Ingrese su Email', 
            'class': 'custom-input'})  # Asegúrate de agregar la clase 'custom-input'
    )
    password = forms.CharField(
        label="Contraseña", 
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Ingrese su Contraseña', 
            'class': 'custom-input'})  # Asegúrate de agregar la clase 'custom-input'
    )


class RegistroForm(UserCreationForm):
    """
    Formulario de registro personalizado que extiende UserCreationForm.
    
    Este formulario agrega campos adicionales al formulario de registro estándar
    de Django, incluyendo nombre, apellido, correo electrónico y empresa.

    """
    
    first_name = forms.CharField(max_length=30, required=True, help_text='Nombre')
    last_name = forms.CharField(max_length=30, required=True, help_text='Apellido')
    email = forms.EmailField(max_length=254, required=True, help_text='Correo electrónico')
    empresa = forms.CharField(max_length=100, required=True, help_text='Empresa')

    class Meta:
        """
        Clase Meta para configurar el modelo y los campos del formulario.
        """
        model = User
        fields = ['first_name', 'last_name', 'email', 'empresa', 'password1', 'password2']

