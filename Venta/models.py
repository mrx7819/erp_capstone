from django.db import models
from Cliente.models import Cliente

# Nota: No importamos Producto directamente para evitar la importación circular.

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Relación con el modelo Cliente
    fecha_venta = models.DateField()  # Fecha de la venta
    total_venta = models.DecimalField(max_digits=10, decimal_places=2)  # Total de la venta
    impuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Impuestos aplicados
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Descuento aplicado
    METODO_PAGO_CHOICES = [
        ('Efectivo', 'Efectivo'),
        ('Tarjeta', 'Tarjeta'),
        ('Transferencia', 'Transferencia'),
        ('Otro', 'Otro'),
    ]
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)  # Método de pago
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Completada', 'Completada'),
        ('Cancelada', 'Cancelada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')  # Estado de la venta
    
    def __str__(self):
        return f"Venta {self.id} - {self.cliente.nombre} {self.cliente.apellido} - {self.fecha_venta}"

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        db_table = "venta"
        ordering = ["-fecha_venta"]  # Ordenar por fecha de venta de forma descendente


class Detalle_Venta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)  # Relación con el modelo Venta
    producto = models.ForeignKey('Inventario.Producto', on_delete=models.CASCADE)  # Referencia a Producto como cadena
    cantidad = models.PositiveIntegerField()  # Cantidad del producto vendido
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)  # Precio unitario del producto
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)  # Subtotal (cantidad * precio unitario)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Descuento aplicado

    def calcular_subtotal(self):
        """Calcula el subtotal basado en la cantidad y el precio unitario."""
        return self.cantidad * self.precio_unitario - self.descuento

    def __str__(self):
        return f"Detalle de Venta {self.id} - Producto: {self.producto.nombre} - Cantidad: {self.cantidad}"

    class Meta:
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de Ventas"
        db_table = "detalle_venta"
