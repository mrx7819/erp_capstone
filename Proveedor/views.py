from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.contrib import messages
from .models import *
from .forms import *
import json
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

def upload_logo(request):
    if request.method == 'POST' and request.FILES.get('logo'):
        logo = request.FILES['logo']
        
        # Validación del tipo de archivo (solo imágenes)
        if not logo.content_type.startswith('image/'):
            return JsonResponse({'success': False, 'error': 'Solo se permiten imágenes.'})
        
        file_path = os.path.join('provider_logos', logo.name)
        default_storage.save(file_path, ContentFile(logo.read()))
        return JsonResponse({'success': True, 'logo_url': default_storage.url(file_path)})
    
    return JsonResponse({'success': False})


def filtrar_comunas(request):
    comuna_codigo = request.GET.get('comuna_codigo')
    if comuna_codigo:
        comuna = get_object_or_404(Comuna, codigo_comuna=comuna_codigo)
        provincia = comuna.provincia
        region = provincia.region
        return JsonResponse({
            'success': True,
            'region': {
                'codigo': region.codigo_region,
                'nombre': region.nombre
            }
        })
    return JsonResponse({'success': False})

def get_regiones(request):
    regiones = Region.objects.all()
    data = [{'id': r.codigo_region, 'nombre': r.nombre} for r in regiones]
    return JsonResponse(data, safe=False)

def get_provincias_por_region(request, region_id):
    provincias = Provincia.objects.filter(region__codigo_region=region_id)
    data = [{'id': p.codigo_provincia, 'nombre': p.nombre} for p in provincias]
    return JsonResponse(data, safe=False)

def get_comunas_por_provincia(request, provincia_id):
    comunas = Comuna.objects.filter(provincia__codigo_provincia=provincia_id)
    data = [{'id': c.codigo_comuna, 'nombre': c.nombre} for c in comunas]
    return JsonResponse(data, safe=False)

@login_required
def listarProveedor(request):
    # Filtrar proveedores por el usuario que ha iniciado sesión
    proveedores = Proveedor.objects.filter(user=request.user)
    return render(request, 'crud_proveedores/listar_proveedor.html', {'proveedores': proveedores})


@login_required
def agregarProveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST, request.FILES)
        if form.is_valid():
            proveedor = form.save(commit=False)
            proveedor.user = request.user
            
            # Asignar las instancias de Region, Provincia y Comuna
            proveedor.region = form.cleaned_data['region']
            proveedor.provincia = form.cleaned_data['provincia']
            proveedor.comuna = form.cleaned_data['comuna']
            proveedor.save()

            messages.success(request, 'Proveedor agregado exitosamente.')
            return redirect('listarProveedor')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
            print(form.errors)  # Para depuración
            print(request.POST)  # Imprimir datos enviados para depuración
    else:
        form = ProveedorForm()

    context = {
        'form': form,
        'regiones': Region.objects.all().order_by('nombre'),
        'provincias': Provincia.objects.all().order_by('nombre'),
        'comunas': Comuna.objects.select_related('provincia', 'provincia__region').order_by('provincia__region__nombre', 'nombre'),
    }

    return render(request, 'crud_proveedores/agregar_proveedor.html', context)


@login_required
def modificarProveedor(request, idProveedor):
    # Si el ID es 0, inicializa un nuevo proveedor
    if idProveedor == 0:
        proveedor = Proveedor()  # Crea una nueva instancia de Proveedor
        # Puedes inicializar otros campos si es necesario
    else:
        proveedor = get_object_or_404(Proveedor, id=idProveedor, user=request.user)

    if request.method == 'POST':
        if idProveedor == 0:
            proveedor = Proveedor()  # Crea una nueva instancia si es un nuevo proveedor
        else:
            # Actualizar los campos del proveedor existente
            proveedor = get_object_or_404(Proveedor, id=idProveedor, user=request.user)

        # Actualizar los campos del proveedor
        proveedor.nombre = request.POST.get('nombre')
        proveedor.rut = request.POST.get('rut')
        proveedor.direccion = request.POST.get('direccion')
        proveedor.telefono = request.POST.get('telefono')
        proveedor.email = request.POST.get('email')
        proveedor.logo = request.FILES.get('logo')  # Manejo del archivo correctamente

        # Obtener las instancias de Comuna, Región y Provincia
        comuna_id = request.POST.get('comuna')
        region_id = request.POST.get('region')
        provincia_id = request.POST.get('provincia')

        # Asignar las instancias correspondientes
        if comuna_id:
            proveedor.comuna = get_object_or_404(Comuna, codigo_comuna=comuna_id)
        if region_id:
            proveedor.region = get_object_or_404(Region, codigo_region=region_id)
        if provincia_id:
            proveedor.provincia = get_object_or_404(Provincia, codigo_provincia=provincia_id)

        proveedor.save()
        messages.success(request, 'Proveedor guardado exitosamente.')  # Mensaje de éxito
        return redirect('listarProveedor')
    else:
        proveedores = Proveedor.objects.filter(user=request.user)  # Filtrar por el usuario
        datos = {'proveedores': proveedores, 'proveedor': proveedor}
        return render(request, 'crud_proveedores/modificar_proveedor.html', datos)

@login_required
def eliminarProveedor(request, idProveedor):
    try:
        if request.method == 'POST':
            if request.POST.get('id'):
                id_a_borrar = request.POST.get('id')
                tupla = Proveedor.objects.get(id=id_a_borrar)
                tupla.delete()
                return redirect('listarProveedor')

        proveedores = Proveedor.objects.all()
        proveedor = Proveedor.objects.get(id=idProveedor)
        datos = {'proveedores': proveedores, 'proveedor': proveedor}
        return render(request, "crud_proveedores/eliminar_proveedor.html", datos)

    except Proveedor.DoesNotExist:
        proveedores = Proveedor.objects.all()
        proveedor = None
        datos = {'proveedores': proveedores, 'proveedor': proveedor}
        return render(request, "crud_proveedores/eliminar_proveedor.html", datos)


@login_required
def listarGiro(request):
    # Filtrar giros por el usuario que ha iniciado sesión (si es necesario)
    giros = Giro.objects.all()  # Si no hay un campo de usuario, puedes listar todos los giros
    return render(request, 'crud_giros/listar_giro.html', {'giros': giros})

@login_required
def agregarGiro(request):
    if request.method == 'POST':
        form = GiroForm(request.POST)  # No necesitas request.FILES si no hay archivos

        if form.is_valid():
            form.save()  # Guarda el giro en la base de datos
            return redirect('listarGiro')  # Redirige a la lista de giros después de agregar

    else:
        form = GiroForm()  # Crea un nuevo formulario vacío

    return render(request, 'crud_giros/agregar_giro.html', {'form': form})  # Asegúrate de que la plantilla sea correcta

def buscar_proveedores(request):
    query = request.GET.get('query', '')
    proveedores = Proveedor.objects.filter(nombre__icontains=query) | Proveedor.objects.filter(rut__icontains=query)
    
    results = []
    for p in proveedores:
        results.append({
            'id': p.id,
            'rut': p.rut,
            'nombre': p.nombre,
            'direccion': p.direccion,
            'telefono': p.telefono,
            'email': p.email,
            'giro_id': p.giro.id,  # Solo incluir el ID del giro
            'giro_nombre': p.giro.nombre if p.giro else None  # Incluir el nombre del giro si existe
        })
    
    return JsonResponse(results, safe=False)


def get_giros(request):
    giros = Giro.objects.all().values('id','codigo', 'nombre')  # Obtén los giros desde la base de datos
    return JsonResponse(list(giros), safe=False)  # Devuelve los giros como JSON