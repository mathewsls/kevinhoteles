from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dashboard/', VistaDashboard.as_view(), name='dashboard'),
    path('reservar/', VistaReservar.as_view(), name='reservar'),
    path('logout/', LogoutView.as_view(template_name="logout.html"), name='logout'),
    path('register/', UsuarioCreateView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('eliminar/<int:id>/', eliminar_reserva, name='eliminar_reserva'),
    path('editar/<int:id>/', editar_reserva, name='editar_reserva'),
    path('pagar/', payment, name='payment'),
]