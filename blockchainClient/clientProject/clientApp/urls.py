from django.urls import path
from clientProject.clientApp import views
from clientProject.clientApp.forms import LoginForm
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('login', LoginView.as_view(form_class=LoginForm, redirect_authenticated_user=True), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', views.register, name='register'),
    path('vote', views.vote, name='vote'),
    path('', views.index, name='index'),
]