from django import forms
from .models import Reserva
from django.utils import timezone
from bootstrap_datepicker_plus.widgets import DatePickerInput
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['habitacion', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'fecha_inicio': DatePickerInput(options={
                "format": "YYYY-MM-DD",
                "showClose": True,
                "showClear": True,
                "showTodayButton": True,
            }),
            'fecha_fin': DatePickerInput(options={
                "format": "YYYY-MM-DD",
                "showClose": True,
                "showClear": True,
                "showTodayButton": True,
            }),
        }
        
    
    def clean(self):
        cleaned_data = super().clean()
        habitacion = cleaned_data.get('habitacion')
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        
        if fecha_inicio < timezone.now().date():
            raise forms.ValidationError("No puedes reservar fechas pasadas.")
        
        # Verificar solapamiento de reservas
        reservas_existentes = Reserva.objects.filter(
            habitacion=habitacion,
            fecha_inicio__lte=fecha_fin,
            fecha_fin__gte=fecha_inicio
        )
        
        if reservas_existentes.exists():
            raise forms.ValidationError("Esta habitación ya está reservada en las fechas seleccionadas.")