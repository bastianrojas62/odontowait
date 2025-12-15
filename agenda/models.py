from django.db import models
from catalogo.models import Especialidad, TipoTratamiento
from pacientes.models import Paciente

class Odontologo(models.Model):
    nombre_completo = models.CharField(max_length=120)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.PROTECT)
    capacidad_diaria = models.PositiveIntegerField(default=12)
    activo = models.BooleanField(default=True)
    def __str__(self): return f"{self.nombre_completo} · {self.especialidad}"

class Bloque(models.Model):
    ESTADO = (('LIBRE','Libre'),('RESERVADO','Reservado'),('AGENDADO','Agendado'))
    odontologo = models.ForeignKey(Odontologo, on_delete=models.CASCADE)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.PROTECT)
    inicia_en = models.DateTimeField()
    termina_en = models.DateTimeField()
    estado = models.CharField(max_length=9, choices=ESTADO, default='LIBRE')
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(termina_en__gt=models.F('inicia_en')),
                                   name='bloque_fin_despues_inicio'),
            models.UniqueConstraint(fields=['odontologo','inicia_en'], name='uniq_bloque_odontologo_inicio')
        ]
        indexes = [models.Index(fields=['odontologo','inicia_en','estado'])]
    def __str__(self): return f"{self.odontologo} {self.inicia_en:%d-%m %H:%M}"

class Cita(models.Model):
    ESTADO = (('AGENDADA','Agendada'),('CANCELADA','Cancelada'),('NO_SHOW','No Asiste'),('ATENDIDA','Atendida'))
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    odontologo = models.ForeignKey(Odontologo, on_delete=models.PROTECT)
    tratamiento = models.ForeignKey(TipoTratamiento, on_delete=models.PROTECT)
    inicia_en = models.DateTimeField()
    termina_en = models.DateTimeField()
    estado = models.CharField(max_length=10, choices=ESTADO, default='AGENDADA')
    token_confirmacion = models.CharField(max_length=64, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(termina_en__gt=models.F('inicia_en')),
                                   name='cita_fin_despues_inicio'),
            models.UniqueConstraint(fields=['odontologo','inicia_en'], name='uniq_cita_odontologo_inicio')
        ]
        indexes = [models.Index(fields=['paciente','inicia_en'])]
    def __str__(self): return f"{self.paciente} @ {self.inicia_en:%d-%m %H:%M}"