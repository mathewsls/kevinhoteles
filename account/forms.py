from django import forms
from .models import Reserva
from django.utils import timezone
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.core.exceptions import ValidationError

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


class PaymentForm(forms.Form):
    card_number = forms.CharField(
        label='Número de Tarjeta',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'cardNumber', 'placeholder': '1234 5678 9101 1121'})
    )
    expiration_date = forms.CharField(
        label='Fecha de Expiración',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'expiryDate', 'placeholder': 'MM/AA'})
    )
    cvv = forms.CharField(
        label='CVV',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'cvv', 'placeholder': '123'})
    )

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']
        if not card_number.replace(' ', '').isdigit():
            raise ValidationError('El número de tarjeta debe ser numérico')
        if len(card_number.replace(' ', '')) != 16:
            raise ValidationError('El número de tarjeta debe tener 16 dígitos')
        return card_number

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data['expiration_date']
        if not expiration_date.replace('/', '').isdigit():
            raise ValidationError('La fecha de expiración debe ser numérica')
        if len(expiration_date.split('/')) != 2:
            raise ValidationError('La fecha de expiración debe tener el formato MM/AA')
        month, year = map(int, expiration_date.split('/'))
        if month < 1 or month > 12:
            raise ValidationError('El mes de expiración debe ser entre 1 y 12')
        if year < 2023:
            raise ValidationError('El año de expiración debe ser mayor o igual a 2023')
        return expiration_date

    def clean_cvv(self):
        cvv = self.cleaned_data['cvv']
        if not cvv.isdigit():
            raise ValidationError('El CVV debe ser numérico')
        if len(cvv) != 3:
            raise ValidationError('El CVV debe tener 3 dígitos')
        return cvv