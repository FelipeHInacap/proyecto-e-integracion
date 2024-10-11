from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Usuario
from django.contrib.auth.hashers import make_password
import logging

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'Agenda/index.html')

def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Bienvenido, {username}!")
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'Agenda/login.html')

def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        tipo = request.POST['tipo']
        telefono = request.POST.get('telefono', '')

        print(f"Intento de registro: username={username}, email={email}")

        try:
            if Usuario.objects.filter(username=username).exists():
                error_message = 'El nombre de usuario ya existe'
                messages.error(request, error_message)
                logger.error(f"Error de registro: {error_message}")
                print(f"Error: {error_message}")
            elif Usuario.objects.filter(email=email).exists():
                error_message = 'El email ya está registrado'
                messages.error(request, error_message)
                logger.error(f"Error de registro: {error_message}")
                print(f"Error: {error_message}")
            else:
                user = Usuario.objects.create(
                    username=username,
                    email=email,
                    password=make_password(password),
                    tipo=tipo,
                    telefono=telefono
                )
                auth_login(request, user)
                success_message = f"Usuario {username} registrado exitosamente"
                messages.success(request, success_message)
                logger.info(success_message)
                print(f"Éxito: {success_message}")
                return redirect('dashboard')
        except Exception as e:
            error_message = f"Error inesperado durante el registro: {str(e)}"
            messages.error(request, "Ocurrió un error durante el registro. Por favor, inténtelo de nuevo.")
            logger.error(error_message)
            print(f"Error: {error_message}")

    messages.info(request, "Este es un mensaje de prueba")
    return render(request, 'Agenda/registro.html')

@login_required
def dashboard(request):
    return render(request, 'Agenda/dashboard.html')

def cerrar_sesion(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('index')