from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cuentas/', include('cuentas.urls')),
    path('', include('pacientes.urls')),
    path('espera/', include('espera.urls')),
    path('agenda/', include('agenda.urls')),
    path('api/', include('api.urls')),
]