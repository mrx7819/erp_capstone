from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Producto, Bodega

@receiver(post_save, sender=Producto)
def actualizar_cantidad_bodega_al_guardar(sender, instance, created, **kwargs):
    """
    Suma o actualiza la cantidad de productos en la bodega cuando un producto se crea o se actualiza.
    """
    bodega = instance.bodega

    # Asegúrate de convertir `instance.cantidad` a entero
    cantidad_producto = int(instance.cantidad)

    if created:
        # Si es un producto nuevo, incrementamos la cantidad de artículos de la bodega
        nueva_cantidad = (bodega.cantidad_art or 0) + cantidad_producto
        bodega.cantidad_art = max(nueva_cantidad, 0)  # Asegurarse de no ser negativa
        bodega.save()
    else:
        # Si el producto ya existía, calculamos el cambio en la cantidad y actualizamos
        producto_original = Producto.objects.filter(pk=instance.pk).values('cantidad', 'bodega_id').first()
        cantidad_original = int(producto_original['cantidad'])
        diferencia = cantidad_producto - cantidad_original

        # Si la bodega del producto cambió, restamos de la bodega anterior y sumamos a la nueva
        if producto_original['bodega_id'] != instance.bodega_id:
            bodega_anterior = Bodega.objects.get(pk=producto_original['bodega_id'])
            nueva_cantidad_anterior = (bodega_anterior.cantidad_art or 0) - cantidad_original
            bodega_anterior.cantidad_art = max(nueva_cantidad_anterior, 0)  # Asegurarse de no ser negativa
            bodega_anterior.save()

            # Sumamos la cantidad actual a la nueva bodega
            nueva_cantidad_actual = (bodega.cantidad_art or 0) + cantidad_producto
            bodega.cantidad_art = max(nueva_cantidad_actual, 0)  # Asegurarse de no ser negativa
            bodega.save()
        else:
            # Si la bodega no cambió, solo ajustamos la cantidad en la misma bodega
            nueva_cantidad = (bodega.cantidad_art or 0) + diferencia
            bodega.cantidad_art = max(nueva_cantidad, 0)  # Asegurarse de no ser negativa
            bodega.save()


@receiver(post_delete, sender=Producto)
def actualizar_cantidad_bodega_al_eliminar(sender, instance, **kwargs):
    """
    Resta la cantidad de productos de la bodega cuando se elimina un producto.
    """
    bodega = instance.bodega
    nueva_cantidad = (bodega.cantidad_art or 0) - instance.cantidad
    bodega.cantidad_art = max(nueva_cantidad, 0)  # Asegurarse de no ser negativa
    bodega.save()
