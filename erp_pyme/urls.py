from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from Home import views as home_views
from django.contrib.auth import views as auth_views
from Cliente import views as cliente_views
from Inventario.views import *
from Proveedor import views as proveedor_views

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('', home_views.index, name='index'),  # Vista no protegida
    path('vistasprotegidas/', home_views.vistasprotegidas, name='vistasprotegidas'),  # Vista protegida
    path('login/', home_views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('forgot-password/', home_views.forgot_password, name='forgot_password'),
    path('registro/', home_views.registro, name='registro'),
    #Clientes
    path('listarCliente/', cliente_views.listarCliente, name='listarCliente'),
    path('agregarCliente/', cliente_views.agregarCliente, name='agregarCliente'),
    path('modificarCliente/<int:idCliente>', cliente_views.modificarCliente, name='modificarCliente'),
    path('eliminarCliente/<int:idCliente>', cliente_views.eliminarCliente, name='eliminarCliente'),
    #Proveedores
    path('agregarProveedor/', proveedor_views.agregarProveedor, name='agregarProveedor'),
    path('listarProveedor/', proveedor_views.listarProveedor, name='listarProveedor'),
    path('modificarProveedor/<int:idProveedor>', proveedor_views.modificarProveedor, name='modificarProveedor'),
    path('eliminarProveedor/<int:idProveedor>', proveedor_views.eliminarProveedor, name='eliminarProveedor'),
    #Categorías
    path('listarCategoria/', listarCategoria, name='listarCategoria'),
    path('agregarCategoria/', agregarCategoria, name='agregarCategoria'),
    path('modificarCategoria/<int:idCategoria>/', modificarCategoria, name='modificarCategoria'),
    path('eliminarCategoria/<int:idCategoria>/', eliminarCategoria, name='eliminarCategoria'),
    #Productos
    path('listarProducto/', listarProducto, name='listarProducto'),
    path('agregarProducto/', agregarProducto, name='agregarProducto'),
    path('modificarProducto/<int:idProducto>/', modificarProducto, name='modificarProducto'),
    path('eliminarProducto/<int:idProducto>/', eliminarProducto, name='eliminarProducto'),
    #Bodegas
    path('listarBodega/', listarBodega, name='listarBodega'),
    path('agregarBodega/', agregarBodega, name='agregarBodega'),
    path('modificarBodega/<int:idBodega>/', modificarBodega, name='modificarBodega'),
    path('eliminarBodega/<int:idBodega>/', eliminarBodega, name='eliminarBodega'),
    # Otras URLs...
    path('filtrar_comunas/', proveedor_views.filtrar_comunas, name='filtrar_comunas'),
    path('get_regiones/', proveedor_views.get_regiones, name='get_regiones'),
    path('get_provincias_por_region/<str:region_id>/', proveedor_views.get_provincias_por_region, name='get_provincias_por_region'),
    path('get_comunas_por_provincia/<str:provincia_id>/', proveedor_views.get_comunas_por_provincia, name='get_comunas_por_provincia'),
    path('get_giros/', proveedor_views.get_giros, name='get_giros'),  # Añade la URL para obtener giros
    path('upload_logo/', proveedor_views.upload_logo, name='upload_logo'),
    path('buscarProveedores/', proveedor_views.buscar_proveedores, name='buscar_proveedores'),



    
]
