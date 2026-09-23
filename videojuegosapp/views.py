from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Videojuego

def inicio(request):
    videojuegos = Videojuego.objects.all()
    
    # EL TRUCO PROFESIONAL: Dividimos el texto en listas para iterarlas en el HTML
    for juego in videojuegos:
        juego.lista_generos = juego.genero.split(', ') if juego.genero else []
        juego.lista_plataformas = juego.plataforma.split(', ') if juego.plataforma else []

    return render(request, 'videojuegosapp/inicio.html', {
        'videojuegos': videojuegos
    })

def crear_videojuego(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        
        # Capturamos múltiples géneros y plataformas
        generos_seleccionados = request.POST.getlist('generos')
        genero = ', '.join(generos_seleccionados)
        
        plataformas_seleccionadas = request.POST.getlist('plataformas')
        plataforma = ', '.join(plataformas_seleccionadas)
        
        precio = request.POST.get('precio', '')
        stock = request.POST.get('stock', '')
        anio_lanzamiento = request.POST.get('anio_lanzamiento', '')
        descripcion = request.POST.get('descripcion', '').strip()

        errores = []

        if not titulo:
            errores.append('El título es obligatorio.')
        if not generos_seleccionados:
            errores.append('Debes seleccionar al menos un género.')
        if not plataformas_seleccionadas:
            errores.append('Debes seleccionar al menos una plataforma.')
        if len(descripcion) > 300:
            errores.append('La descripción no puede exceder los 300 caracteres.')

        try:
            precio = float(precio)
            if precio < 0: # Permitimos 0 para juegos Gratis
                errores.append('El precio no puede ser negativo.')
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
                'plataformas_seleccionadas': plataformas_seleccionadas,
                'generos_seleccionados': generos_seleccionados
            })

        Videojuego.objects.create(
            titulo=titulo, genero=genero, plataforma=plataforma,
            precio=precio, stock=stock, anio_lanzamiento=anio_lanzamiento, descripcion=descripcion
        )
        return redirect('inicio')

    return render(request, 'videojuegosapp/crear.html')

def detalle_videojuego(request, id):
    videojuego = Videojuego.objects.get(id=id)
    # Dividimos para el detalle también
    videojuego.lista_generos = videojuego.genero.split(', ') if videojuego.genero else []
    videojuego.lista_plataformas = videojuego.plataforma.split(', ') if videojuego.plataforma else []
    
    return render(request, 'videojuegosapp/detalle.html', {
        'videojuego': videojuego
    })

def editar_videojuego(request, id):
    videojuego = Videojuego.objects.get(id=id)

    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        
        generos_seleccionados = request.POST.getlist('generos')
        genero = ', '.join(generos_seleccionados)
        
        plataformas_seleccionadas = request.POST.getlist('plataformas')
        plataforma = ', '.join(plataformas_seleccionadas)
        
        precio = request.POST.get('precio', '')
        stock = request.POST.get('stock', '')
        anio_lanzamiento = request.POST.get('anio_lanzamiento', '')
        descripcion = request.POST.get('descripcion', '').strip()

        errores = []

        if not titulo:
            errores.append('El título es obligatorio.')
        if not generos_seleccionados:
            errores.append('Debes seleccionar al menos un género.')
        if not plataformas_seleccionadas:
            errores.append('Debes seleccionar al menos una plataforma.')

        try:
            precio = float(precio)
            if precio < 0:
                errores.append('El precio no puede ser negativo.')
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
                'videojuego': videojuego, 'errores': errores,
                'plataformas_seleccionadas': plataformas_seleccionadas,
                'generos_seleccionados': generos_seleccionados
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

    # Convertimos los strings a listas para el GET
    lista_plataformas = videojuego.plataforma.split(', ') if videojuego.plataforma else []
    lista_generos = videojuego.genero.split(', ') if videojuego.genero else []

    return render(request, 'videojuegosapp/editar.html', {
        'videojuego': videojuego,
        'plataformas_seleccionadas': lista_plataformas,
        'generos_seleccionados': lista_generos
    })

def eliminar_videojuego(request, id):
    videojuego = Videojuego.objects.get(id=id)
    if request.method == 'POST':
        videojuego.delete()
        return redirect('inicio')
    return render(request, 'videojuegosapp/eliminar.html', {'videojuego': videojuego})