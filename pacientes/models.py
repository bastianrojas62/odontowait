from django.db import models

class Paciente(models.Model):
    rut = models.CharField(max_length=12, unique=True, null=True, blank=True)
    nombres = models.CharField(max_length=80)
    apellidos = models.CharField(max_length=80)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    comuna = models.CharField(max_length=80, blank=True)
    # Contacto alternativo
    contacto_alt_nombre = models.CharField(max_length=120, blank=True)
    contacto_alt_parentesco = models.CharField(max_length=40, blank=True)
    contacto_alt_telefono = models.CharField(max_length=20, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['apellidos', 'nombres'])]
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

    def __str__(self):
        return f"{self.apellidos}, {self.nombres}"