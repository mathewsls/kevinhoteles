from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dashboard/', VistaDashboard.as_view(), name='dashboard'),
    path('reservar/', VistaReservar.as_view(), name='reservar'),
    path('logout/', LogoutView.as_view(template_name="logout.html"), name='logout'),
]