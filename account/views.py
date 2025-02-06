from django.views.generic import FormView, TemplateView
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Habitacion, Reserva
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import ReservaForm

def index(request):
    return render(request, "index.html")

def pricing(request):
    return render(request, "pricing.html")

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True  # Redirige si el usuario ya está autenticado
    success_url = reverse_lazy('dashboard')  # URL a la que redirige tras login exitoso


class VistaReservar(LoginRequiredMixin, TemplateView, FormView):
    template_name = 'reservar.html'
    form_class = ReservaForm
    success_url = '/'
    
    def form_valid(self, form):
        reserva = form.save(commit=False)
        reserva.usuario = self.request.user
        reserva.save()
        return super().form_valid(form)
class VistaDashboard(LoginRequiredMixin, TemplateView):
    model = Reserva
    template_name = 'dashboard.html'
    context_object_name = "reservas"
    
    def get_queryset(self):
        return Reserva.objects.filter(usuario=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservas'] = Reserva.objects.filter(usuario=self.request.user)
        return context
