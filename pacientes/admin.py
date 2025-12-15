from django.contrib import admin
from .models import Paciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('apellidos','nombres','correo','comuna','creado_en')
    search_fields = ('apellidos','nombres','rut','correo')