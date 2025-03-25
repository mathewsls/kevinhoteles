from django.views.generic import FormView, TemplateView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Habitacion, Reserva
from django.http import JsonResponse
from .forms import ReservaForm, PaymentForm

@login_required
def payment(request):
    if request.method == 'POST':
        print("Formulario enviado")
        form = PaymentForm(request.POST)
        if form.is_valid():
            print("Formulario válido")
            print('Pago procesado con éxito')
            Reserva.objects.filter(usuario=request.user).update(pagado=True)
            return redirect('dashboard')
        else:
            print("Formulario no válido")
            print(form.errors)
    else:
        form = PaymentForm()
    return render(request, 'payment.html', {'form': form})

@login_required
def eliminar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id, usuario=request.user)

    if request.method == 'POST':
        reserva.delete()
        return redirect('dashboard')

    # Si es GET, mostrar confirmación
    return render(request, 'confirmar_eliminacion.html', {'reserva': reserva})


@login_required
def editar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id, usuario=request.user)

    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ReservaForm(instance=reserva)

    return render(request, 'editar_reserva.html', {'form': form, 'reserva': reserva})


def index(request):
    return render(request, "index.html")


def pricing(request):
    return render(request, "pricing.html")

def support(request):
    return render(request, "support.html")

class UsuarioCreateView(CreateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password']
    template_name = 'Register.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True  # Redirige si el usuario ya está autenticado
    # URL a la que redirige tras login exitoso
    success_url = reverse_lazy('dashboard')


class VistaReservar(LoginRequiredMixin, TemplateView, FormView):
    template_name = 'reservar.html'
    form_class = ReservaForm
    success_url = '/app/dashboard/'

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
