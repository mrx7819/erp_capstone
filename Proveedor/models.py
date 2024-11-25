from django.db import models
from Ubicacion.models import *
from Inventario import *
from django.utils.text import slugify  # Importar slugify para generar slugs automáticamente
from django.contrib.auth.models import User

class CategoriaGiro(models.Model):
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'categoria_giro'  # Nombre de la tabla en la base de datos
        ordering = ['nombre']  # Ordenar por nombre de forma ascendente
        verbose_name = "Categoría de Giro"
        verbose_name_plural = "Categorías de Giro"


class Giro(models.Model):
    codigo = models.CharField(max_length=10, unique=True)  # Código único para el giro
    nombre = models.CharField(max_length=100)  # Nombre del giro
    categoria = models.ForeignKey(CategoriaGiro, on_delete=models.CASCADE, null=False, default=0)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    class Meta:
        db_table = 'giro'  # Nombre de la tabla en la base de datos
        ordering = ['nombre']  # Ordenar por nombre de forma ascendente
        unique_together = ('codigo', 'nombre')  # Asegurar que la combinación de código y nombre sea única
        verbose_name = "Giro"
        verbose_name_plural = "Giros"
    
class Proveedor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proveedores', default=0)  # Agregar este campo
    rut = models.CharField(max_length=12, unique=True, default='00.000.000-0') 
    nombre = models.CharField(max_length=100)  # Campo para el nombre del proveedor
    direccion = models.TextField()              # Campo para la dirección del proveedor
    comuna = models.ForeignKey(Comuna, on_delete=models.SET_NULL, null=True, related_name='proveedores')  # Relación con el modelo Comuna
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, related_name='proveedores')  # Relación con el modelo Region
    provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True, related_name='proveedores')
    telefono = models.CharField(max_length=15)  # Campo para el teléfono del proveedor
    email = models.EmailField()                  # Campo para el correo electrónico del proveedor
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación del proveedor
    fecha_actualizacion = models.DateTimeField(auto_now=True)  # Fecha de la última actualización
    giro = models.ForeignKey(Giro, on_delete=models.SET_NULL, null=True)  # Relación con el modelo Giro
    logo = models.ImageField(upload_to='static/images/proveedores/logos/', blank=True, null=True)


    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        db_table = "proveedor"

class Pedido(models.Model):
    
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)  # Relación con el proveedor
    fecha_pedido = models.DateTimeField(auto_now_add=True)  # Fecha en que se realizó el pedido
    total = models.DecimalField(max_digits=10, decimal_places=2)  # Total del pedido
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),  # El pedido está pendiente de ser procesado
        ('En Proceso', 'En Proceso'),  # El pedido está siendo procesado
        ('Completado', 'Completado'),  # El pedido ha sido completado
        ('Cancelado', 'Cancelado'),  # El pedido ha sido cancelado
        ('Devuelto', 'Devuelto'),  # El pedido ha sido devuelto
    ]
    estado = models.CharField(max_length=50)  # Estado del pedido (ej. 'Pendiente', 'Completado')

    def __str__(self):
        return f"Pedido {self.id} - Proveedor: {self.proveedor.nombre} - Total: {self.total}"
    
    class Meta:
        db_table = 'pedido'  # Nombre de la tabla en la base de datos
        ordering = ['fecha_pedido']  # Ordenar por fecha de pedido de forma ascendente
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        indexes = [
            models.Index(fields=['fecha_pedido'], name='fecha_pedido_idx'),  # Índice en el campo fecha_pedido
        ]
