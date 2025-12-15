from django.contrib import admin
from .models import EntradaListaEspera

@admin.register(EntradaListaEspera)
class EntradaListaEsperaAdmin(admin.ModelAdmin):
    list_display = ('paciente','tratamiento','prioridad_clinica','estado','puntaje','derivado_en')
    list_filter = ('estado','prioridad_clinica','tratamiento__especialidad')
    search_fields = ('paciente__apellidos','paciente__nombres')