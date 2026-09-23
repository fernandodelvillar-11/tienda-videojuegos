from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Videojuego

def inicio(request):
    videojuegos = Videojuego.objects.all()
    return render(request, 'videojuegosapp/inicio.html', {
        'videojuegos': videojuegos
    })

def crear_videojuego(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        genero = request.POST.get('genero', '').strip()
        plataformas_seleccionadas = request.POST.getlist('plataformas')
        plataforma = ', '.join(plataformas_seleccionadas)
        precio = request.POST.get('precio', '')
        stock = request.POST.get('stock', '')
        anio_lanzamiento = request.POST.get('anio_lanzamiento', '')
        descripcion = request.POST.get('descripcion', '').strip()

        errores = []

        # Validaciones requeridas
        if not titulo:
            errores.append('El título es obligatorio.')
        if not genero:
            errores.append('El género es obligatorio.')
        if not plataformas_seleccionadas:
            errores.append('Debes seleccionar al menos una plataforma.')
        if len(descripcion) > 300:
            errores.append('La descripción no puede tener más de 300 caracteres.')

        try:
            precio = float(precio)
            if precio <= 0:
                errores.append('El precio debe ser mayor que 0.')
        except ValueError:
            errores.append('El precio debe ser un número válido.')

        try:
            stock = int(stock)
            if stock < 0:
                errores.append('El stock no puede ser negativo.')
        except ValueError:
            errores.append('El stock debe ser un número entero válido.')

        try:
            anio_lanzamiento = int(anio_lanzamiento)
            if anio_lanzamiento < 1970 or anio_lanzamiento > 2100:
                errores.append('El año debe estar entre 1970 y 2100.')
        except ValueError:
            errores.append('El año debe ser un número entero válido.')

        if errores:
            return render(request, 'videojuegosapp/crear.html', {
                'errores': errores,
                'datos': request.POST,
                'plataformas_seleccionadas': plataformas_seleccionadas # ¡Agregado para persistir selecciones si hay error!
            })

        Videojuego.objects.create(
            titulo=titulo,
            genero=genero,
            plataforma=plataforma,
            precio=precio,
            stock=stock,
            anio_lanzamiento=anio_lanzamiento,
            descripcion=descripcion
        )
        return redirect('inicio')

    return render(request, 'videojuegosapp/crear.html')

def detalle_videojuego(request, id):
    videojuego = Videojuego.objects.get(id=id)
    return render(request, 'videojuegosapp/detalle.html', {
        'videojuego': videojuego
    })

def editar_videojuego(request, id):
    videojuego = Videojuego.objects.get(id=id)

    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        genero = request.POST.get('genero', '').strip()
        plataformas_seleccionadas = request.POST.getlist('plataformas')
        plataforma = ', '.join(plataformas_seleccionadas)
        precio = request.POST.get('precio', '')
        stock = request.POST.get('stock', '')
        anio_lanzamiento = request.POST.get('anio_lanzamiento', '')
        descripcion = request.POST.get('descripcion', '').strip()

        errores = []

        if not titulo:
            errores.append('El título es obligatorio.')
        if not genero:
            errores.append('El género es obligatorio.')
        if not plataformas_seleccionadas:
            errores.append('Debes seleccionar al menos una plataforma.')
        if len(descripcion) > 300:
            errores.append('La descripción no puede tener más de 300 caracteres.')

        try:
            precio = float(precio)
            if precio <= 0:
                errores.append('El precio debe ser mayor que 0.')
        except ValueError:
            errores.append('El precio debe ser un número válido.')

        try:
            stock = int(stock)
            if stock < 0:
                errores.append('El stock no puede ser negativo.')
        except ValueError:
            errores.append('El stock debe ser un número entero válido.')

        try:
            anio_lanzamiento = int(anio_lanzamiento)
            if anio_lanzamiento < 1970 or anio_lanzamiento > 2100:
                errores.append('El año debe estar entre 1970 y 2100.')
        except ValueError:
            errores.append('El año debe ser un número entero válido.')

        if errores:
            return render(request, 'videojuegosapp/editar.html', {
                'videojuego': videojuego,
                'errores': errores,
                'plataformas_seleccionadas': plataformas_seleccionadas # Mantiene los checks en caso de error
            })

        videojuego.titulo = titulo
        videojuego.genero = genero
        videojuego.plataforma = plataforma
        videojuego.precio = precio
        videojuego.stock = stock
        videojuego.anio_lanzamiento = anio_lanzamiento
        videojuego.descripcion = descripcion
        videojuego.save()
        return redirect('inicio')

    # ¡ESTA ES LA PARTE CRUCIAL PARA LA PETICIÓN GET!
    # Convertimos el string de la base de datos de vuelta a una lista
    lista_plataformas = videojuego.plataforma.split(', ') if videojuego.plataforma else []

    return render(request, 'videojuegosapp/editar.html', {
        'videojuego': videojuego,
        'plataformas_seleccionadas': lista_plataformas # Enviamos la lista al template
    })

def eliminar_videojuego(request, id):
    videojuego = Videojuego.objects.get(id=id)

    if request.method == 'POST':
        videojuego.delete()
        return redirect('inicio')

    return render(request, 'videojuegosapp/eliminar.html', {
        'videojuego': videojuego
    })