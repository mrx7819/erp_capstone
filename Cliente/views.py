from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
# Create your views here.

@login_required
def listarCliente(request):
    # Filtrar clientes por el usuario que ha iniciado sesión
    clientes = Cliente.objects.filter(user=request.user)
    return render(request, 'crud_clientes/listar_cliente.html', {'clientes': clientes})

# views.py

import datetime

@login_required
def agregarCliente(request):
    if request.method == 'POST':
        if (
            request.POST.get('rut') and
            request.POST.get('nombre') and
            request.POST.get('apellido') and
            request.POST.get('telefono') and
            request.POST.get('email') and
            request.POST.get('fecha_nacimiento') and
            request.POST.get('genero') and
            request.POST.get('interaccion_fecha') and
            request.POST.get('interaccion_descripcion') and
            request.POST.get('interaccion_tipo')
        ):
            try:
                # Crear el cliente
                cliente = Cliente()
                cliente.rut = request.POST.get('rut')
                cliente.nombre = request.POST.get('nombre')
                cliente.apellido = request.POST.get('apellido')
                cliente.direccion = request.POST.get('direccion')  # Puede ser opcional
                cliente.telefono = request.POST.get('telefono')
                cliente.email = request.POST.get('email')
                cliente.fecha_nacimiento = request.POST.get('fecha_nacimiento')
                cliente.genero = request.POST.get('genero')
                cliente.user = request.user  # Relacionamos el cliente con el usuario logueado
                
                # Validar y guardar cliente
                cliente.full_clean()
                cliente.save()

                # Crear la interacción asociada
                interaccion = InteraccionCliente()
                interaccion.cliente = cliente
                interaccion.fecha = request.POST.get('interaccion_fecha')
                interaccion.descripcion = request.POST.get('interaccion_descripcion')
                interaccion.tipo_interaccion = request.POST.get('interaccion_tipo')

                # Validar y guardar interacción
                interaccion.full_clean()
                interaccion.save()

                messages.success(request, 'Cliente e interacción agregados exitosamente.')
                return redirect('listarCliente')  # Cambiar por el nombre de la URL que lista los clientes
            except ValidationError as e:
                messages.error(request, f'Error de validación: {e.message_dict}')
            except Exception as e:
                messages.error(request, f'Error al crear el cliente o la interacción: {str(e)}')
            return render(request, 'crud_clientes/agregar_cliente.html')
        else:
            messages.error(request, 'Por favor complete todos los campos requeridos.')
            return render(request, 'crud_clientes/agregar_cliente.html')
    else:
        # Renderizamos el formulario
        return render(request, 'crud_clientes/agregar_cliente.html')



@login_required
def modificarCliente(request, idCliente):
    try:
        if request.method == 'POST':
            if (
                request.POST.get('id') and 
                request.POST.get('nombre') and 
                request.POST.get('apellido') and 
                request.POST.get('telefono') and 
                request.POST.get('email') and 
                request.POST.get('fecha_nacimiento') and 
                request.POST.get('genero')
            ):
                cliente_id_old = request.POST.get('id')
                cliente_old = Cliente.objects.get(id=cliente_id_old)

                cliente = Cliente()
                cliente.id = request.POST.get('id')
                cliente.nombre = request.POST.get('nombre')
                cliente.apellido = request.POST.get('apellido')
                cliente.direccion = request.POST.get('direccion')  # Puede ser opcional
                cliente.telefono = request.POST.get('telefono')
                cliente.email = request.POST.get('email')
                cliente.fecha_nacimiento = request.POST.get('fecha_nacimiento')
                cliente.genero = request.POST.get('genero')
                cliente.fecha_creacion = cliente_old.fecha_creacion  # Conservamos la fecha original
                cliente.user = request.user  # Asociamos al usuario actual

                cliente.save()
                messages.success(request, 'Cliente modificado exitosamente.')
                return redirect('listarCliente')
            else:
                # Si faltan campos en el formulario, devolver el formulario con un error
                clientes = Cliente.objects.all()
                cliente = Cliente.objects.get(id=idCliente)
                datos = {
                    'clientes': clientes, 
                    'cliente': cliente, 
                    'error': 'Faltan campos obligatorios'
                }
                return render(request, 'crud_clientes/modificar_cliente.html', datos)

        else:
            # Si es una solicitud GET, mostrar el formulario con los datos del cliente
            clientes = Cliente.objects.all()
            cliente = Cliente.objects.get(id=idCliente)
            datos = {'clientes': clientes, 'cliente': cliente}
            return render(request, 'crud_clientes/modificar_cliente.html', datos)

    except Cliente.DoesNotExist:
        # En caso de que no exista el cliente, manejar el error y devolver la vista con cliente nulo
        clientes = Cliente.objects.all()
        cliente = None
        datos = {'clientes': clientes, 'cliente': cliente}
        return render(request, 'crud_clientes/modificar_cliente.html', datos)




@login_required
def eliminarCliente(request, idCliente):
    try:
        if request.method == 'POST':
            if request.POST.get('id'):
                id_a_borrar = request.POST.get('id')
                cliente = Cliente.objects.get(id=id_a_borrar)
                cliente.delete()
                messages.success(request, 'Cliente eliminado exitosamente.')
                return redirect('listarCliente')  # Cambiar por el nombre de la vista que lista los clientes
            else:
                # Si faltan campos, mostrar un error
                cliente = Cliente.objects.get(id=idCliente)
                return render(request, 'crud_clientes/eliminar_cliente.html', {
                    'cliente': cliente,
                    'error': 'Faltan campos obligatorios',
                })
        else:
            # En caso de GET, cargar el cliente a eliminar
            cliente = Cliente.objects.get(id=idCliente)
            return render(request, 'crud_clientes/eliminar_cliente.html', {
                'cliente': cliente,
            })
    except Cliente.DoesNotExist:
        # Si no existe el cliente, manejar el error
        messages.error(request, 'El cliente solicitado no existe.')
        return redirect('listarCliente')  # Redirige a la lista de clientes