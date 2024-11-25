from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Inventario.models import Categoria, CategoriaGiro, Producto, Bodega
from Proveedor.models import Proveedor
from Ubicacion.models import *
from django.contrib import messages  # Añadir esta importación
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver    
from django.http import HttpResponse
# Create your views here.

@login_required
def listarCategoria(request):
    # Filtrar clientes por el usuario que ha iniciado sesión
    categorias = Categoria.objects.filter(user=request.user)
    return render(request, 'crud_categorias/listar_categoria.html', {'categorias': categorias})


@login_required
def agregarCategoria(request):
    if request.method == 'POST':
        if request.POST.get('nombre') and request.POST.get('descripcion') and request.FILES.get('imagen'):
            
            
            categoria = Categoria()
            categoria.nombre = request.POST.get('nombre')
            categoria.descripcion = request.POST.get('descripcion')
            categoria.img = request.FILES.get('imagen')
            categoria.user = request.user
            categoria.save()
            return redirect('listarCategoria')
        else:
            # Si no se completaron todos los campos, podrías mostrar un mensaje de error
            return render(request, 'crud_categorias/agregar_categoria.html')
    else:
        return render(request, 'crud_categorias/agregar_categoria.html')



@login_required
def modificarCategoria(request, idCategoria):
    try:
        if request.method == 'POST':
            if request.POST.get('id') and request.POST.get('nombre') and request.POST.get('descripcion') and request.FILES.get('imagen'):

                categoria_id_old = request.POST.get('id')
                categoria_old = Categoria.objects.get(id=categoria_id_old)

                categoria = Categoria()
                categoria.id = request.POST.get('id')
                categoria.nombre = request.POST.get('nombre')
                categoria.descripcion = request.POST.get('descripcion')
                categoria.img = request.FILES.get('imagen')
                categoria.fecha_creacion = categoria_old.fecha_creacion
                categoria.user = request.user
                categoria.save()
                return redirect('listarCategoria')
            else:
                # Si faltan campos en el formulario, devolver el formulario con un error
                categorias = Categoria.objects.all()
                categoria = Categoria.objects.get(id=idCategoria)
                datos = {'categorias': categorias, 'categoria': categoria, 'error': 'Faltan campos obligatorios'}
                return render(request, 'crud_categorias/modificar_categoria.html', datos)

        else:
            # Si es una solicitud GET, mostrar el formulario con los datos de la categoría
            categorias = Categoria.objects.all()
            categoria = Categoria.objects.get(id=idCategoria)
            datos = {'categorias': categorias, 'categoria': categoria}
            return render(request, 'crud_categorias/modificar_categoria.html', datos)

    except Categoria.DoesNotExist:
        # En caso de que no exista la categoría, manejar el error y devolver la vista con categoría nula
        categorias = Categoria.objects.all()
        categoria = None
        datos = {'categorias': categorias, 'categoria': categoria}
        return render(request, 'crud_categorias/modificar_categoria.html', datos)




@login_required
def eliminarCategoria(request,idCategoria):
    try:
        if request.method=='POST':
            if request.POST.get('id'):
                id_a_borrar = request.POST.get('id')
                tupla = Categoria.objects.get(id = id_a_borrar)
                tupla.delete()
                return redirect('listarCategoria')
            else:
                # Si faltan campos en el formulario, devolver el formulario con un error
                categorias = Categoria.objects.all()
                categoria = Categoria.objects.get(id=idCategoria)
                datos = {'categorias': categorias, 'categoria': categoria, 'error': 'Faltan campos obligatorios'}
                return render(request, 'crud_categorias/eliminar_categoria.html', datos)
        else:  
            categorias = Categoria.objects.all()
            datos = {'categorias': categorias}
            return render (request, "crud_categorias/eliminar_categoria.html", datos)
    except Categoria.DoesNotExist:
        categorias = Categoria.objects.all()
        datos = {'categorias': categorias}
        return render (request, "crud_categorias/eliminar_categoria.html", datos)


##PRODUCTOS##
@login_required
def listarProducto(request):
    # Filtrar clientes por el usuario que ha iniciado sesión
    productos = Producto.objects.filter(user=request.user)
    return render(request, 'crud_productos/listar_producto.html', {'productos': productos})


@login_required
def agregarProducto(request):
    if request.method == 'POST':
        if (
            request.POST.get('sku') and 
            request.POST.get('nombre') and 
            request.POST.get('descripcion') and 
            request.POST.get('precio_compra') and
            request.POST.get('precio_venta') and
            request.POST.get('porc_ganancias') and
            request.POST.get('cantidad') and 
            request.POST.get('categoria') and
            request.POST.get('proveedor') and
            request.POST.get('bodega') and
            request.FILES.get('imagen')
        ):
            producto = Producto()
            producto.sku = request.POST.get('sku')
            producto.nombre = request.POST.get('nombre')
            producto.descripcion = request.POST.get('descripcion')
            producto.precio_compra = request.POST.get('precio_compra')
            producto.precio_venta = request.POST.get('precio_venta')
            producto.porc_ganancias = request.POST.get('porc_ganancias')
            producto.cantidad = request.POST.get('cantidad')
            producto.categoria_id = request.POST.get('categoria')
            producto.proveedor_id = request.POST.get('proveedor')
            producto.bodega_id = request.POST.get('bodega')
            producto.img = request.FILES.get('imagen')
            producto.user = request.user
            producto.save()
            return redirect('listarProducto')
        else:
            # Si no se completaron todos los campos, podrías mostrar un mensaje de error
            return render(request, 'crud_productos/agregar_producto.html', {'error': 'Faltan campos obligatorios'})
    else:
        # Pasamos las categorías, proveedores, y bodegas disponibles al formulario
        categorias = Categoria.objects.filter(user=request.user)
        proveedores = Proveedor.objects.filter(user=request.user)  # Asumiendo que tienes un modelo Proveedor
        bodegas = Bodega.objects.filter(user=request.user)  # Asumiendo que tienes un modelo Bodega
        return render(request, 'crud_productos/agregar_producto.html', {
            'categorias': categorias,
            'proveedores': proveedores,
            'bodegas': bodegas
        })



@login_required
def modificarProducto(request, idProducto):
    try:
        if request.method == 'POST':
            if (
                request.POST.get('id') and 
                request.POST.get('categoria') and 
                request.POST.get('sku') and 
                request.POST.get('nombre') and 
                request.POST.get('descripcion') and 
                request.POST.get('proveedor') and 
                request.POST.get('precio_compra') and 
                request.POST.get('precio_venta') and 
                request.POST.get('porc_ganancias') and 
                request.POST.get('cantidad') and 
                request.POST.get('bodega') and 
                request.FILES.get('imagen')
            ):
                # Recuperamos el producto original antes de actualizarlo
                producto_id_old = request.POST.get('id')
                producto_old = Producto.objects.get(id=producto_id_old)

                # Creamos una nueva instancia del producto con los datos actualizados
                producto = Producto()
                producto.id = request.POST.get('id')
                producto.categoria_id = request.POST.get('categoria')
                producto.sku = request.POST.get('sku')
                producto.nombre = request.POST.get('nombre')
                producto.descripcion = request.POST.get('descripcion')
                producto.proveedor_id = request.POST.get('proveedor')
                producto.precio_compra = request.POST.get('precio_compra')
                producto.precio_venta = request.POST.get('precio_venta')
                producto.porc_ganancias = request.POST.get('porc_ganancias')
                producto.cantidad = request.POST.get('cantidad')
                producto.bodega_id = request.POST.get('bodega')
                producto.img = request.FILES.get('imagen')
                producto.fecha_creacion = producto_old.fecha_creacion  # Mantenemos la fecha original
                producto.user = request.user
                producto.save()
                return redirect('listarProducto')
            else:
                # Si faltan campos en el formulario, devolver el formulario con un error
                productos = Producto.objects.all()
                producto = Producto.objects.get(id=idProducto)
                categorias = Categoria.objects.all()
                proveedores = Proveedor.objects.all()
                bodegas = Bodega.objects.all()
                datos = {
                    'productos': productos,
                    'producto': producto,
                    'categorias': categorias,
                    'proveedores': proveedores,
                    'bodegas': bodegas,
                    'error': 'Faltan campos obligatorios',
                }
                return render(request, 'crud_productos/modificar_producto.html', datos)

        else:
            # Si es una solicitud GET, mostrar el formulario con los datos del producto
            productos = Producto.objects.all()
            producto = Producto.objects.get(id=idProducto)
            categorias = Categoria.objects.all()
            proveedores = Proveedor.objects.all()
            bodegas = Bodega.objects.all()
            datos = {
                'productos': productos,
                'producto': producto,
                'categorias': categorias,
                'proveedores': proveedores,
                'bodegas': bodegas,
            }
            return render(request, 'crud_productos/modificar_producto.html', datos)

    except Producto.DoesNotExist:
        # En caso de que no exista el producto, manejar el error y devolver la vista con producto nulo
        productos = Producto.objects.all()
        categorias = Categoria.objects.all()
        proveedores = Proveedor.objects.all()
        bodegas = Bodega.objects.all()
        datos = {
            'productos': productos,
            'producto': None,
            'categorias': categorias,
            'proveedores': proveedores,
            'bodegas': bodegas,
            'error': 'El producto solicitado no existe.',
        }
        return render(request, 'crud_productos/modificar_producto.html', datos)




@login_required
def eliminarProducto(request, idProducto):
    try:
        if request.method == 'POST':
            if request.POST.get('id'):
                id_a_borrar = request.POST.get('id')
                producto = Producto.objects.get(id=id_a_borrar)
                producto.delete()
                return redirect('listarProducto')
            else:
                # Si faltan campos en el formulario, devolver el formulario con un error
                productos = Producto.objects.all()
                producto = Producto.objects.get(id=idProducto)
                datos = {'productos': productos, 'producto': producto, 'error': 'Faltan campos obligatorios'}   
                return render(request, 'crud_productos/eliminar_producto.html', datos)
        else:
            productos = Producto.objects.all()
            producto = Producto.objects.get(id=idProducto)
            datos = {'productos': productos, 'producto': producto}
            return render(request, 'crud_productos/eliminar_producto.html', datos)

    except Producto.DoesNotExist:
        productos = Producto.objects.all()
        datos = {'productos': productos}
        return render(request, 'crud_productos/eliminar_producto.html', datos)

##BODEGAS##

@login_required
def listarBodega(request):
    # Filtrar bodegas por el usuario que ha iniciado sesión
    bodegas = Bodega.objects.filter(user=request.user)
    return render(request, 'crud_bodegas/listar_bodega.html', {'bodegas': bodegas})


@login_required
def agregarBodega(request):
    if request.method == 'POST':
        if (
            request.POST.get('nombre') and
            request.POST.get('direccion') and
            request.POST.get('capacidad') and
            request.POST.get('comuna') and
            request.POST.get('provincia') and
            request.POST.get('region')
        ):
            try:
                bodega = Bodega()
                bodega.nombre = request.POST.get('nombre')
                bodega.direccion = request.POST.get('direccion')
                bodega.capacidad = int(request.POST.get('capacidad'))
                bodega.comuna_id = request.POST.get('comuna')
                bodega.provincia_id = request.POST.get('provincia')
                bodega.region_id = request.POST.get('region')
                bodega.user = request.user
                bodega.cantidad_art = 0  # Inicializamos en 0 ya que es una bodega nueva
                bodega.save()
                messages.success(request, 'Bodega creada exitosamente.')
                return redirect('listarBodega')
            except ValueError:
                messages.error(request, 'Por favor, ingrese valores válidos.')
            except Exception as e:
                messages.error(request, f'Error al crear la bodega: {str(e)}')
            return render(request, 'crud_bodegas/agregar_bodega.html')
        else:
            messages.error(request, 'Por favor complete todos los campos requeridos.')
            return render(request, 'crud_bodegas/agregar_bodega.html')
    else:
        # Pasamos las comunas, provincias y regiones disponibles al formulario
        comunas = Comuna.objects.all()
        provincias = Provincia.objects.all()
        regiones = Region.objects.all()
        return render(request, 'crud_bodegas/agregar_bodega.html', {
            'comunas': comunas,
            'regiones': regiones,
            'provincias': provincias,
        })

@login_required
def modificarBodega(request, idBodega):
    try:
        if request.method == 'POST':
            print("Datos POST:", request.POST)

            if (request.POST.get('id') and request.POST.get('nombre') and
                request.POST.get('direccion') and request.POST.get('producto') and
                request.POST.get('cantidad') and request.POST.get('comuna') and
                request.POST.get('region')):

                bodega_id_old = request.POST.get('id')
                bodega_old = Bodega.objects.get(id=bodega_id_old)

                bodega = Bodega()
                bodega.id = request.POST.get('id')
                bodega.nombre = request.POST.get('nombre')
                bodega.direccion = request.POST.get('direccion')
                bodega.producto_id = request.POST.get('producto')
                bodega.cantidad = request.POST.get('cantidad')
                bodega.comuna_id = request.POST.get('comuna')
                bodega.region_id = request.POST.get('region')
                bodega.fecha_creacion = bodega_old.fecha_creacion
                bodega.user = request.user
                bodega.save()
                return redirect('listarBodega')
            else:
                # Si faltan campos, mostrar un error
                bodegas = Bodega.objects.all()
                productos = Producto.objects.all()
                comunas = Comuna.objects.all()
                regiones = Region.objects.all()
                bodega = Bodega.objects.get(id=idBodega)
                return render(request, 'crud_bodegas/modificar_bodega.html', {
                    'bodegas': bodegas,
                    'bodega': bodega,
                    'productos': productos,
                    'comunas': comunas,
                    'regiones': regiones,
                    'error': 'Faltan campos obligatorios',
                })
        else:
            # En caso de GET, cargar los datos actuales de la bodega
            bodegas = Bodega.objects.all()
            productos = Producto.objects.all()
            comunas = Comuna.objects.all()
            regiones = Region.objects.all()
            bodega = Bodega.objects.get(id=idBodega)
            return render(request, 'crud_bodegas/modificar_bodega.html', {
                'bodegas': bodegas,
                'bodega': bodega,
                'productos': productos,
                'comunas': comunas,
                'regiones': regiones,
            })
    except Bodega.DoesNotExist:
        # Si no existe la bodega, manejar el error
        bodegas = Bodega.objects.all()
        productos = Producto.objects.all()
        comunas = Comuna.objects.all()
        regiones = Region.objects.all()
        bodega = None
        return render(request, 'crud_bodegas/modificar_bodega.html', {
            'bodegas': bodegas,
            'bodega': bodega,
            'productos': productos,
            'comunas': comunas,
            'regiones': regiones,
        })


@login_required
def eliminarBodega(request, idBodega):
    try:
        if request.method == 'POST':
            if request.POST.get('id'):
                id_a_borrar = request.POST.get('id')
                bodega = Bodega.objects.get(id=id_a_borrar)
                bodega.delete()
                return redirect('listarBodega')
            else:
                # Si faltan campos, mostrar un error
                bodegas = Bodega.objects.all()
                bodega = Bodega.objects.get(id=idBodega)
                return render(request, 'crud_bodegas/eliminar_bodega.html', {
                    'bodegas': bodegas,
                    'bodega': bodega,
                    'error': 'Faltan campos obligatorios',
                })
        else:
            # En caso de GET, cargar la bodega a eliminar
            bodegas = Bodega.objects.all()
            bodega = Bodega.objects.get(id=idBodega)
            return render(request, 'crud_bodegas/eliminar_bodega.html', {
                'bodegas': bodegas,
                'bodega': bodega,
            })
    except Bodega.DoesNotExist:
        # Si no existe la bodega, manejar el error
        bodegas = Bodega.objects.all()
        return render(request, 'crud_bodegas/eliminar_bodega.html', {
            'bodegas': bodegas,
        })

