from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import CustomAuthenticationForm
from .forms import RegistroForm
from django.contrib.auth.models import User
from Cliente.models import Cliente  # Asegúrate de importar tu modelo Cliente
from Proveedor.models import Proveedor

@login_required
def index(request):
    clientes = Cliente.objects.all()  # Obtiene todos los clientes
    cantidad_clientes = clientes.count()  # Cuenta el total de clientes
    primeros_clientes = clientes[:5]  # Obtiene los primeros 5 clientes

    proveedores = Proveedor.objects.all()  # Obtiene todos los proveedores
    cantidad_proveedores = proveedores.count()  # Cuenta el total de proveedores
    primeros_proveedores = proveedores[:5]  # Obtiene los primeros 5 proveedores

    context = {
        'cantidad_clientes': cantidad_clientes,
        'clientes': primeros_clientes,  # Pasa solo los primeros 5 clientes a la plantilla
        'cantidad_proveedores': cantidad_proveedores,
        'proveedores': primeros_proveedores,  # Pasa solo los primeros 5 proveedores a la plantilla
    }
    return render(request, 'index.html', context)

@login_required
def vistasprotegidas(request):
    return render(request, 'index.html')


def forgot_password(request):
    return render(request, 'forgot_password.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Guardar el usuario sin enviar todavía el commit a la base de datos
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']  # Usar el correo como username
            user.save()  # Guardar el usuario en la base de datos
            login(request, user)  # Iniciar sesión automáticamente después del registro
            return redirect('login')  # Redirigir a la página de inicio o a la que prefieras
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # Cambia esto a la URL que prefieras después del login exitoso
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})