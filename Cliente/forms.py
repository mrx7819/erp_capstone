from django import forms
from .models import Cliente, InteraccionCliente  # Asegúrate de importar el modelo InteraccionCliente
from django.core.exceptions import ValidationError
import re


class ClienteForm(forms.ModelForm):
    # Campos adicionales para la interacción
    fecha_interaccion = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    descripcion = forms.CharField(required=True, widget=forms.Textarea)
    tipo_interaccion = forms.ChoiceField(choices=[
        ('Llamada', 'Llamada'),
        ('Email', 'Email'),
        ('Reunión', 'Reunión'),
        ('Otro', 'Otro'),
    ])

    class Meta:
        model = Cliente
        fields = ['rut', 'nombre', 'apellido', 'direccion', 'telefono', 'email', 'fecha_nacimiento', 'genero', 'fecha_interaccion', 'descripcion', 'tipo_interaccion']

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        
        # Verificar que el RUT solo contenga números y un dígito verificador
        if not re.match(r'^\d{7,8}[0-9Kk]$', rut):
            raise ValidationError('El RUT debe contener entre 7 y 8 números seguidos de un dígito verificador (0-9 o K).')
        
        # Validar el dígito verificador
        if not self.validar_dv(rut):
            raise ValidationError('El RUT ingresado no es válido.')
        
        return rut

    def validar_dv(self, rut):
        # Extraer el cuerpo y el dígito verificador
        cuerpo = rut[:-1]
        dv = rut[-1].upper()
        
        # Calcular el dígito verificador
        suma = 0
        multiplicador = 2
        
        for r in reversed(cuerpo):
            suma += int(r) * multiplicador
            multiplicador = 2 if multiplicador == 7 else multiplicador + 1
            
        resto = suma % 11
        dv_calculado = '0' if resto == 0 else 'K' if resto == 1 else str(11 - resto)
        
        # Verificar que el DV sea correcto
        return dv == dv_calculado