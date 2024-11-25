from django.db import models
from Proveedor.models import *
from Ubicacion.models import Comuna, Region  # Asegúrate de importar las clases necesarias
from django.contrib.auth.models import User
from django.utils import timezone


class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now) 
    img = models.ImageField(upload_to='static/images/categorias/img/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categorias', null=False)




    def __str__(self):
        return f"{self.id} - {self.nombre}"

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        db_table = "categoria"

class Bodega(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bodegas', default=0)  # Agregar este campo
    nombre = models.CharField(max_length=100)  # Campo para el nombre de la bodega
    direccion = models.CharField(max_length=100)  # Campo para la dirección de la bodega
    capacidad = models.IntegerField(blank=False, null=False, default=0)
    cantidad_art = models.IntegerField(blank=True, null=True)  # Ahora puede ser nulo
    comuna = models.ForeignKey(Comuna, on_delete=models.SET_NULL, null=True, related_name='bodegas')  # Relación con el modelo Comuna
    provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True, related_name='bodegas')  # Relación con el modelo Provincia
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, related_name='bodegas')  # Relación con el modelo Region
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Bodega"
        verbose_name_plural = "Bodegas"
        db_table = "bodega"

    def calcular_cantidad_articulos(self):
        # Como ya no tenemos relación directa con productos, 
        # simplemente retornamos el valor de cantidad_art
        return self.cantidad_art if self.cantidad_art is not None else 0


class Producto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='productos', default=0)  # Agregar este campo
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos', default=0)
    sku = models.CharField(max_length=50, unique=True)  # Código único para cada producto
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    proveedor = models.ForeignKey('Proveedor.Proveedor', on_delete=models.SET_NULL, null=True, related_name='productos')  # Usar cadena para evitar importación circular
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    porc_ganancias = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField(blank=False, null=False, default=0)
    fecha_creacion = models.DateTimeField(default=timezone.now) 
    bodega = models.ForeignKey('Bodega', on_delete=models.CASCADE)
    img = models.ImageField(blank=True, upload_to='static/images/productos/')

    def __str__(self):
            return f"{self.nombre} - {self.sku}"

    class Meta:
            verbose_name = "Producto"
            verbose_name_plural = "Productos"
            db_table = "producto"


class Detalle_Pedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')  # Relación con el modelo Pedido
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='detalles', default=0)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)  # Usar cadena para evitar importación circular
    cantidad = models.PositiveIntegerField()  # Cantidad del producto en el pedido
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)  # Precio unitario del producto
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)  # Subtotal (cantidad * precio unitario)
    fecha_creacion = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f"Detalle de Pedido {self.id} - Producto: {self.producto.nombre} - Cantidad: {self.cantidad}"

    class Meta:
        verbose_name = "Detalle de Pedido"
        verbose_name_plural = "Detalles de Pedidos"
        db_table = "detalle_pedido"