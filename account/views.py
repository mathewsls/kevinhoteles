from django.views.generic import FormView, TemplateView
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    return render(request, "index.html")


class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True  # Redirige si el usuario ya está autenticado
    success_url = reverse_lazy('dashboard')  # URL a la que redirige tras login exitoso


class VistaDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'