from django.db import models
from django.utils import timezone
from decimal import Decimal

from pacientes.models import Paciente
from catalogo.models import TipoTratamiento


class EntradaListaEspera(models.Model):
    PRIORIDAD = (
        ('P1', 'Alta'),
        ('P2', 'Media'),
        ('P3', 'Baja'),
    )

    ESTADO = (
        ('PENDIENTE', 'Pendiente'),
        ('AGENDADO', 'Agendado'),
        ('REMOVIDO', 'Removido'),
    )

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    tratamiento = models.ForeignKey(TipoTratamiento, on_delete=models.PROTECT)

    derivado_en = models.DateField(default=timezone.localdate)

    prioridad_clinica = models.CharField(max_length=2, choices=PRIORIDAD)

  
    estado = models.CharField(max_length=10, choices=ESTADO, default='PENDIENTE')

   
    puntaje = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0'))

   
    puntaje_actualizado = models.DateTimeField(null=True, blank=True)

    observaciones = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Entrada de Lista de Espera'
        verbose_name_plural = 'Entradas de Lista de Espera'
        indexes = [
            models.Index(fields=['tratamiento', 'estado', 'puntaje', 'derivado_en']),
        ]

    def __str__(self):
        return f"{self.paciente} · {self.tratamiento} · {self.estado}"