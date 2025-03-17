from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Habitacion(models.Model):
    numero = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=50)
    precio_por_noche = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Habitación {self.numero} - {self.tipo}"

class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    pagado = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Reserva de {self.usuario.username} - Habitación {self.habitacion.numero}"
    
    class Meta:
        
        constraints = [
            models.UniqueConstraint(
                fields=['habitacion', 'fecha_inicio', 'fecha_fin'],
                name='reserva_unica_por_habitacion_y_fecha'
            )
        ]
    
    def clean(self):
        # Valida que la fecha de inicio no sea mayor que la de fin
        if self.fecha_inicio > self.fecha_fin:
            raise ValidationError("La fecha de inicio no puede ser posterior a la de fin.")

class Pago(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=99.9)
    fecha_pago = models.DateTimeField(auto_now_add=True)