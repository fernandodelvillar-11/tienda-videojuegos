from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name = 'inicio'),
    path('crear/', views.crear_videojuego, name = 'crear_videojuego'),
    path('videojuego/<int:id>/', views.detalle_videojuego, name = 'detalle_videojuego'),
    path('videojuego/<int:id>/editar/', views.editar_videojuego, name='editar_videojuego'),
    path('videojuego/<int:id>/eliminar/', views.eliminar_videojuego, name='eliminar_videojuego'),
]