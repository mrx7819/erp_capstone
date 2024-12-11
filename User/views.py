from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm
from .forms import RegistroForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model

User = get_user_model()  # Obtén el modelo de usuario personalizado

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            # Busca al usuario por email en el modelo personalizado
            user = User.objects.get(email=email)
            # Genera un token de recuperación
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(
                f'/reset-password/{uid}/{token}/'
            )
            # Enviar el email de recuperación
            send_mail(
                'Recuperación de contraseña',
                f'Usa el siguiente enlace para restablecer tu contraseña: {reset_link}',
                'vi.fraile@duocuc.cl',  # Cambia a tu correo
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Hemos enviado un enlace de recuperación a tu correo.')
            return redirect('login')  # Redirige a la página de login
        except User.DoesNotExist:
            messages.error(request, 'No se encontró un usuario con ese email.')
    return render(request, 'forgot_password.html')

def reset_password(request, uidb64, token):
    try:
        # Decodifica el ID del usuario
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, '¡Tu contraseña se ha actualizado con éxito!')
                return redirect('login')  # Redirige al login después de restablecer
        else:
            form = SetPasswordForm(user)
        return render(request, 'reset_password.html', {'form': form})
    else:
        messages.error(request, 'El enlace de restablecimiento no es válido o ha expirado.')
        return redirect('forgot_password')


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            print("Formulario válido")  # Debug
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']  # Usar el correo como username
            user.save()
            print(f"Usuario creado: {user.username}")  # Debug
            login(request, user)
            return redirect('login')
        else:
            print(f"Errores en el formulario: {form.errors}")  # Debug
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


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def ver_reporte(request):
    """
    Vista para renderizar la página de reportes con las cards.
    """
    return render(request, 'reportes/ver_reporte.html')
