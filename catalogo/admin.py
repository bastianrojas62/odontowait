from django.contrib import admin
from .models import Especialidad, TipoTratamiento

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)

@admin.register(TipoTratamiento)
class TipoTratamientoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especialidad')
    list_filter = ('especialidad',)
    search_fields = ('nombre',)