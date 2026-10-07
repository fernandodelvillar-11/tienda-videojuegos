from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import LoginAPIView, VideojuegoAPIView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='videojuegosapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.inicio, name = 'inicio'),
    path('crear/', views.crear_videojuego, name = 'crear_videojuego'),
    path('videojuego/<int:id>/', views.detalle_videojuego, name = 'detalle_videojuego'),
    path('videojuego/<int:id>/editar/', views.editar_videojuego, name='editar_videojuego'),
    path('videojuego/<int:id>/eliminar/', views.eliminar_videojuego, name='eliminar_videojuego'),
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
    path('api/videojuegos/', VideojuegoAPIView.as_view(), name='api_videojuegos'),
]