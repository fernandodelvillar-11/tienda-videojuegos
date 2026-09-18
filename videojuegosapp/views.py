from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Videojuego


def inicio(request):
    videojuego = Videojuego.objects.all()
    return render (request, 'videojuegosapp/inicio.html', {
        'videojuegos' : videojuego
    })




        