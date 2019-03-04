from django.urls import path
from . import views

urlpatterns = [
    path('', views.listarUsuarios, name='listarUsuarios'),
    path('usuario/<int:idUsuario>/', views.detalharUsuario, name='verAmigos'),
]