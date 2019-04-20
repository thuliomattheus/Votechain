from django.urls import path
from clientProject.clientApp import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('index', views.index, name='index')
]