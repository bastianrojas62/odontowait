from django.contrib import admin
from .models import Odontologo, Bloque, Cita

admin.site.register(Odontologo)

@admin.register(Bloque)
class BloqueAdmin(admin.ModelAdmin):
    list_display = ('odontologo','inicia_en','termina_en','estado')
    list_filter = ('estado','odontologo')
    search_fields = ('odontologo__nombre_completo',)

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente','odontologo','inicia_en','estado')
    list_filter = ('estado','odontologo')
    search_fields = ('paciente__apellidos','paciente__nombres')