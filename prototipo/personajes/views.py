from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import Personaje

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            request.session['role'] = role
            messages.success(request, f'Bienvenido, {user.username} ({role})!')
            if role == 'Jugador':
                return redirect('panel_jugador')
            else:
                return redirect('panel_gm')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'personajes/login.html')


def registro_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')

        if password != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('registro')

        try:
            validate_password(password)
        except ValidationError as e:
            for error in e:
                messages.error(request, error)
            return redirect('registro')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe.')
            return redirect('registro')

        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, 'Usuario creado correctamente. Inicia sesión.')
        return redirect('login_view')

    return render(request, 'personajes/registro.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión.')
    return redirect('login_view')


@login_required
def panel_jugador(request):
    role = request.session.get('role')
    if role != 'Jugador':
        return redirect('login_view')

    personajes = Personaje.objects.filter(owner=request.user)
    return render(request, 'personajes/panel_jugador.html', {'personajes': personajes})


@login_required
def create_character(request):
    role = request.session.get('role')
    if role != 'Jugador':
        return redirect('login_view')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        raza = request.POST.get('raza')
        estado = request.POST.get('estado')
        nivel = int(request.POST.get('nivel'))
        poder = request.POST.get('poder')
        equipo = request.POST.get('equipo')

        Personaje.objects.create(
            nombre=nombre,
            raza=raza,
            estado=estado,
            nivel=nivel,
            poder=poder,
            equipo=equipo,
            owner=request.user
        )
        messages.success(request, f'Personaje {nombre} creado con éxito.')
        return redirect('panel_jugador')

    return render(request, 'personajes/create_character.html')


@login_required
def eliminar_personaje(request, pk):
    personaje = get_object_or_404(Personaje, pk=pk, owner=request.user)
    personaje.delete()
    messages.success(request, f'Personaje {personaje.nombre} eliminado.')
    return redirect('panel_jugador')

@login_required
def panel_gm(request):
    personajes = Personaje.objects.all().select_related('owner').order_by('nombre')
    return render(request, 'personajes/panel_gm.html', {'personajes': personajes})


@login_required
def editar_personaje(request, pk):
    personaje = get_object_or_404(Personaje, pk=pk)

    role = request.session.get('role')
    if role != 'GM' and personaje.owner != request.user:
        messages.error(request, 'No puedes editar este personaje.')
        return redirect('panel_jugador')

    if request.method == 'POST':
        personaje.nombre = request.POST.get('nombre')
        personaje.raza = request.POST.get('raza')
        personaje.estado = request.POST.get('estado')
        personaje.nivel = request.POST.get('nivel')
        personaje.poder = request.POST.get('poder')
        personaje.equipo = request.POST.get('equipo')
        personaje.save()
        messages.success(request, f'Personaje {personaje.nombre} actualizado con éxito.')
        if role == 'GM':
            return redirect('panel_gm')
        else:
            return redirect('panel_jugador')

    return render(request, 'personajes/editar_personaje.html', {'personaje': personaje})
