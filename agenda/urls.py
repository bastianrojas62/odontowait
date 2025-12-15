from django.urls import path
from . import views

urlpatterns = [
    # Odontólogos
    path('odontologos/', views.OdontologoLista.as_view(), name='odontologo_lista'),
    path('odontologos/nuevo/', views.OdontologoCrear.as_view(), name='odontologo_crear'),
    path('odontologos/<int:pk>/editar/', views.OdontologoEditar.as_view(), name='odontologo_editar'),
    path('odontologos/<int:pk>/eliminar/', views.OdontologoEliminar.as_view(), name='odontologo_eliminar'),
    # Bloques
    path('bloques/', views.BloqueLista.as_view(), name='bloque_lista'),
    path('bloques/nuevo/', views.BloqueCrear.as_view(), name='bloque_crear'),
    path('citas/', views.CitaLista.as_view(), name='cita_lista'),
    path('citas/nueva/', views.CitaCrear.as_view(), name='cita_crear'),
]