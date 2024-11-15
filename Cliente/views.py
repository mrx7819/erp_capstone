from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
# Create your views here.

@login_required
def listarCliente(request):
    # Filtrar clientes por el usuario que ha iniciado sesión
    clientes = Cliente.objects.filter(user=request.user)
    return render(request, 'crud_clientes/listar_cliente.html', {'clientes': clientes})

# views.py

@login_required
def agregarCliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)

        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.user = request.user  # Asocia el cliente con el usuario actual
            cliente.save()

            # Guarda la interacción
            interaccion = InteraccionCliente(
                cliente=cliente,
                fecha=form.cleaned_data['fecha_interaccion'],
                descripcion=form.cleaned_data['descripcion'],
                tipo_interaccion=form.cleaned_data['tipo_interaccion']
            )
            interaccion.save()

            return redirect('listarCliente')
    else:
        form = ClienteForm()

    return render(request, 'crud_clientes/agregar_cliente.html', {'form': form})


@login_required
def modificarCliente(request, idCliente):
    try:
        if request.method == 'POST':
            cliente_id = request.POST.get('id')
            if cliente_id:
                cliente = get_object_or_404(Cliente, id=cliente_id, user=request.user)
                # Actualizar los campos del cliente
                cliente.nombre = request.POST.get('nombre')
                cliente.apellido = request.POST.get('apellido')
                cliente.direccion = request.POST.get('direccion')
                cliente.telefono = request.POST.get('telefono')
                cliente.email = request.POST.get('email')
                cliente.fecha_nacimiento = request.POST.get('fecha_nacimiento')
                cliente.genero = request.POST.get('genero')
                cliente.save()
                return redirect('listarCliente')
        else:
            clientes = Cliente.objects.all()
            cliente = Cliente.objects.get(id=idCliente)
            datos = {'clientes' : clientes, 'cliente' : cliente}
            return render(request, 'crud_clientes/modificar_cliente.html', datos)
    except Cliente.DoesNotExist:
        clientes = Cliente.objects.all()
        cliente = None
        datos = {'clientes' : clientes, 'cliente' : cliente}
        return render(request, 'crud_clientes/modificar_cliente.html', datos)



@login_required
def eliminarCliente(request, idCliente):
    # Si el ID es 0, muestra un mensaje y redirige a la lista de clientes
    if idCliente == 0:
        messages.warning(request, "No hay clientes para eliminar.")  # Mensaje de advertencia
        return redirect('listarCliente')  # Redirige a la lista de clientes

    # Intentamos obtener el cliente o retornamos un 404 si no existe
    cliente = get_object_or_404(Cliente, id=idCliente)
    
    if request.method == 'POST':
        # Elimina el cliente y redirige
        cliente.delete()
        messages.success(request, "Cliente eliminado con éxito.")  # Mensaje de éxito
        return redirect('listarCliente')
    
    # Si la solicitud es GET, muestra la página de confirmación
    clientes = Cliente.objects.all()
    datos = {'clientes': clientes, 'cliente': cliente}
    return render(request, "crud_clientes/eliminar_cliente.html", datos)
