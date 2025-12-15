from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    path('pacientes/', views.PacienteLista.as_view(), name='paciente_lista'),
    path('pacientes/nuevo/', views.PacienteCrear.as_view(), name='paciente_crear'),
    path('pacientes/<int:pk>/editar/', views.PacienteEditar.as_view(), name='paciente_editar'),
    path('pacientes/<int:pk>/eliminar/', views.PacienteEliminar.as_view(), name='paciente_eliminar'),
    path('citas/<int:pk>/estado/', views.cita_cambiar_estado, name='cita_estado'),
]