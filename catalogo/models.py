from django.db import models

class Especialidad(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    def __str__(self): return self.nombre

class TipoTratamiento(models.Model):
    nombre = models.CharField(max_length=120)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.PROTECT, related_name='tipos')
    class Meta:
        unique_together = ('especialidad','nombre')
        verbose_name = 'Tipo de tratamiento'
        verbose_name_plural = 'Tipos de tratamiento'
    def __str__(self): return f"{self.nombre} ({self.especialidad})"