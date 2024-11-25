from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Venta.models import Venta, Detalle_Venta
from Inventario.models import Producto
from Cliente.models import Cliente
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import F
# Create your views here.
@login_required
@csrf_exempt  # Permitir solicitudes AJAX
def eliminar_detalle(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        try:
            # Aquí podrías buscar el detalle por el ID del producto (o cualquier otro criterio)
            detalle = Detalle_Venta.objects.get(producto_id=producto_id)
            detalle.delete()
            return JsonResponse({'success': True})
        except Detalle_Venta.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Detalle no encontrado'})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@login_required
def get_producto_precio(request, producto_id):
    """
    Retorna el precio de venta de un producto dado su ID.
    """
    try:
        producto = Producto.objects.get(id=producto_id)
        return JsonResponse({'success': True, 'precio_venta': float(producto.precio_venta)})
    except Producto.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Producto no encontrado'})
    
@login_required
def listarVenta(request):
    # Prefetch los detalles para optimizar la consulta
    ventas = Venta.objects.filter(user=request.user).prefetch_related('detalle_venta_set__producto')

    # Calcular el total de la venta sumando los total_venta de los detalles
    for venta in ventas:
        venta.total_venta_calculado = sum(detalle.total_venta for detalle in venta.detalle_venta_set.all())

    return render(request, 'crud_ventas/listar_venta.html', {'ventas': ventas})






@login_required
def agregarVenta(request):
    if request.method == 'POST':
        print("Se recibió un POST en agregarVenta.")
        print(f"Datos recibidos: cliente_id={request.POST.get('cliente')}, metodo_pago={request.POST.get('metodo_pago')}, estado={request.POST.get('estado')}, impuesto={request.POST.get('impuesto')}")

        # Validar los campos requeridos para Venta
        if all([
            request.POST.get('cliente'),
            request.POST.get('metodo_pago'),
            request.POST.get('estado'),
            request.POST.get('impuesto')
        ]):
            try:
                with transaction.atomic():
                    # Crear la Venta
                    venta = Venta.objects.create(
                        cliente_id=request.POST.get('cliente'),
                        metodo_pago=request.POST.get('metodo_pago'),
                        estado=request.POST.get('estado'),
                        impuesto=float(request.POST.get('impuesto')),
                        user=request.user,
                    )
                    print(f"Venta guardada con ID: {venta.id}")

                    # Manejar los detalles de la venta
                    productos = request.POST.getlist('productos[]')
                    cantidades = request.POST.getlist('cantidades[]')
                    precios = request.POST.getlist('precios[]')
                    descuentos = request.POST.getlist('descuentos[]')

                    for i in range(len(productos)):
                        producto_id = productos[i]
                        cantidad_vendida = int(cantidades[i])

                        # Obtener el producto y su bodega
                        producto = get_object_or_404(Producto, pk=producto_id, user=request.user)
                        bodega = producto.bodega

                        # Verificar stock suficiente
                        if producto.cantidad < cantidad_vendida:
                            raise ValueError(f"Stock insuficiente para el producto {producto.nombre}.")

                        # Calcular subtotal, IVA y total con descuento
                        precio_unitario = float(precios[i])
                        descuento = float(descuentos[i]) if descuentos[i] else 0.0
                        subtotal = cantidad_vendida * precio_unitario
                        iva = subtotal * 0.19  # IVA fijo del 19%
                        total_con_iva = subtotal + iva
                        total_final = total_con_iva * (1 - (descuento / 100))

                        # Crear el detalle de la venta
                        detalle = Detalle_Venta.objects.create(
                            venta=venta,
                            producto=producto,
                            cantidad=cantidad_vendida,
                            precio_unitario=precio_unitario,
                            descuento=descuento,
                            total_venta=max(total_final, 0),
                            user=request.user,
                        )
                        print(f"Detalle creado para producto {producto.nombre} con cantidad {cantidad_vendida}")

                        # Actualizar cantidades directamente en la base de datos usando F()
                        Producto.objects.filter(pk=producto.pk).update(cantidad=F('cantidad') - cantidad_vendida)
                        bodega.cantidad_art -= cantidad_vendida
                        bodega.save(update_fields=['cantidad_art'])

                    print("Venta procesada con éxito.")
                    return redirect('listarVenta')

            except Exception as e:
                print(f"Error: {str(e)}")
                return render(request, 'crud_ventas/agregar_venta.html', {
                    'error': f"Error al procesar la venta: {str(e)}",
                    'clientes': Cliente.objects.filter(user=request.user),
                    'metodo_pago_choices': Venta.METODO_PAGO_CHOICES,
                    'estado_choices': Venta.ESTADO_CHOICES,
                    'productos': Producto.objects.filter(user=request.user),
                })
        else:
            print("Campos obligatorios faltantes.")
            return render(request, 'crud_ventas/agregar_venta.html', {
                'error': 'Faltan campos obligatorios',
                'clientes': Cliente.objects.filter(user=request.user),
                'metodo_pago_choices': Venta.METODO_PAGO_CHOICES,
                'estado_choices': Venta.ESTADO_CHOICES,
                'productos': Producto.objects.filter(user=request.user),
            })

    else:
        return render(request, 'crud_ventas/agregar_venta.html', {
            'clientes': Cliente.objects.filter(user=request.user),
            'metodo_pago_choices': Venta.METODO_PAGO_CHOICES,
            'estado_choices': Venta.ESTADO_CHOICES,
            'productos': Producto.objects.filter(user=request.user),
        })











@login_required
def modificarVenta(request, idVenta):
    try:
        if request.method == 'POST':
            if (
                request.POST.get('id') and
                request.POST.get('cliente') and
                request.POST.get('metodo_pago') and
                request.POST.get('estado') and
                request.POST.get('impuesto') is not None and
                request.POST.get('descuento') is not None
            ):
                # Recuperamos la venta original antes de actualizarla
                venta_id_old = request.POST.get('id')
                venta_old = Venta.objects.get(id=venta_id_old)

                # Creamos una nueva instancia de la venta con los datos actualizados
                venta = Venta()
                venta.id = request.POST.get('id')
                venta.cliente_id = request.POST.get('cliente')
                venta.metodo_pago = request.POST.get('metodo_pago')
                venta.estado = request.POST.get('estado')
                venta.impuesto = request.POST.get('impuesto')
                venta.descuento = request.POST.get('descuento')
                venta.user = request.user
                venta.fecha_creacion = venta_old.fecha_creacion  # Mantenemos la fecha original
                
                # Guardamos la venta para actualizar el total automáticamente
                venta.save()

                return redirect('listarVentas')
            else:
                # Si faltan campos en el formulario, devolver el formulario con un error
                ventas = Venta.objects.all()
                venta = Venta.objects.get(id=idVenta)
                clientes = Cliente.objects.all()
                datos = {
                    'ventas': ventas,
                    'venta': venta,
                    'clientes': clientes,
                    'metodos_pago': Venta.METODO_PAGO_CHOICES,
                    'estados': Venta.ESTADO_CHOICES,
                    'error': 'Faltan campos obligatorios',
                }
                return render(request, 'crud_ventas/modificar_venta.html', datos)

        else:
            # Si es una solicitud GET, mostrar el formulario con los datos de la venta
            ventas = Venta.objects.all()
            venta = Venta.objects.get(id=idVenta)
            clientes = Cliente.objects.all()
            datos = {
                'ventas': ventas,
                'venta': venta,
                'clientes': clientes,
                'metodos_pago': Venta.METODO_PAGO_CHOICES,
                'estados': Venta.ESTADO_CHOICES,
            }
            return render(request, 'crud_ventas/modificar_venta.html', datos)

    except Venta.DoesNotExist:
        # En caso de que no exista la venta, manejar el error y devolver la vista con venta nula
        ventas = Venta.objects.all()
        clientes = Cliente.objects.all()
        datos = {
            'ventas': ventas,
            'venta': None,
            'clientes': clientes,
            'metodos_pago': Venta.METODO_PAGO_CHOICES,
            'estados': Venta.ESTADO_CHOICES,
            'error': 'La venta solicitada no existe.',
        }
        return render(request, 'crud_ventas/modificar_venta.html', datos)

@login_required
def eliminarVenta(request, idVenta):
    try:
        if request.method == 'POST':
            if request.POST.get('id'):
                # Recuperar el ID de la venta a eliminar
                id_a_borrar = request.POST.get('id')
                venta = Venta.objects.get(id=id_a_borrar)
                venta.delete()
                return redirect('listarVentas')
            else:
                # Si faltan campos, devolvemos el formulario con un mensaje de error
                ventas = Venta.objects.all()
                venta = Venta.objects.get(id=idVenta)
                datos = {'ventas': ventas, 'venta': venta, 'error': 'Faltan campos obligatorios'}
                return render(request, 'crud_ventas/eliminar_venta.html', datos)
        else:
            # En caso de una solicitud GET, mostramos el formulario para confirmar eliminación
            ventas = Venta.objects.all()
            venta = Venta.objects.get(id=idVenta)
            datos = {'ventas': ventas, 'venta': venta}
            return render(request, 'crud_ventas/eliminar_venta.html', datos)

    except Venta.DoesNotExist:
        # Si la venta no existe, manejamos el error y mostramos las ventas existentes
        ventas = Venta.objects.all()
        datos = {'ventas': ventas, 'error': 'La venta no existe.'}
        return render(request, 'crud_ventas/eliminar_venta.html', datos)
