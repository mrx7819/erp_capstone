from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Proveedor, Giro
from Ubicacion.models import Region, Comuna, Provincia  # Asegúrate de importar Provincia


class ProveedorForm(forms.ModelForm):
    rut = forms.CharField(required=True, max_length=12, widget=forms.TextInput(attrs={'placeholder': 'Ej: 12345678K'}))
    telefono = forms.CharField(required=True, max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Ej: +56912345678'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Ej: proveedor@example.com'}))
    direccion = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': 'Ingrese la dirección del proveedor'}))
    
    # Campos actualizados para manejar los códigos correctamente
    region = forms.ModelChoiceField(
        queryset=Region.objects.all().order_by('nombre'),
        required=True,
        empty_label="Seleccione una región",
        to_field_name="codigo_region"
    )
    
    provincia = forms.ModelChoiceField(  # Añadir campo para la provincia
        queryset=Provincia.objects.all().order_by('nombre'),
        required=True,
        empty_label="Seleccione una provincia",
        to_field_name="codigo_provincia"
    )
    
    comuna = forms.ModelChoiceField(
        queryset=Comuna.objects.all().order_by('nombre'),
        required=True,
        empty_label="Seleccione una comuna",
        to_field_name="codigo_comuna"
    )
    
    # Campos restantes sin cambios
    giro = forms.ModelChoiceField(queryset=Giro.objects.all(), required=True, empty_label="Seleccione un giro")
    logo = forms.ImageField(required=False)

    class Meta:
        model = Proveedor
        fields = ['rut', 'nombre', 'direccion', 'comuna', 'provincia', 'region', 'telefono', 'email', 'giro', 'logo']  # Eliminar 'slug'

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

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        
        # Verificar que el teléfono solo contenga números y tenga un formato válido
        if not re.match(r'^\+?\d{7,15}$', telefono):
            raise ValidationError('El teléfono debe contener entre 7 y 15 dígitos, con un posible prefijo de país.')
        
        return telefono

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicializar los campos con sus clases CSS y configuración inicial
        self.fields['region'].widget.attrs.update({'class': 'form-control'})
        self.fields['provincia'].widget.attrs.update({'class': 'form-control'})  # Añadir clase CSS para provincia
        self.fields['comuna'].widget.attrs.update({'class': 'form-control'})
        
        # Si hay una región seleccionada, filtrar las provincias
        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['provincia'].queryset = Provincia.objects.filter(region__codigo_region=region_id).order_by('nombre')
                self.fields['comuna'].queryset = Comuna.objects.none()  # Limpiar comunas
            except (ValueError, TypeError):
                self.fields['provincia'].queryset = Provincia.objects.none()
                self.fields['comuna'].queryset = Comuna.objects.none()
        elif self.instance.pk and self.instance.region:
            # Si el formulario se usa para edición, muestra las provincias y comunas de la región existente
            self.fields['provincia'].queryset = Provincia.objects.filter(region=self.instance.region).order_by('nombre')
            self.fields['comuna'].queryset = Comuna.objects.filter(provincia=self.instance.provincia).order_by('nombre')

        # Si hay una provincia seleccionada, filtrar las comunas
        if 'provincia' in self.data:
            try:
                provincia_id = int(self.data.get('provincia'))
                self.fields['comuna'].queryset = Comuna.objects.filter(provincia_id=provincia_id).order_by('nombre')
            except (ValueError, TypeError):
                self.fields['comuna'].queryset = Comuna.objects.none()
        elif self.instance.pk and self.instance.provincia:
            # Si el formulario se usa para edición, muestra las comunas de la provincia existente
            self.fields['comuna'].queryset = Comuna.objects.filter(provincia=self.instance.provincia).order_by('nombre')


class GiroForm(forms.ModelForm):
    class Meta:
        model = Giro
        fields = ['codigo', 'nombre'] 

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        
        # Verificar que el código no esté vacío
        if not codigo:
            raise ValidationError('El código no puede estar vacío.')
        
        return codigo

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        
        # Verificar que el nombre no esté vacío
        if not nombre:
            raise ValidationError('El nombre no puede estar vacío.')
        
        return nombre