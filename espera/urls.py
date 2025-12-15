from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListaEsperaLista.as_view(), name='espera_lista'),
    path('nueva/', views.ListaEsperaCrear.as_view(), name='espera_crear'),
    path('editar/<int:pk>/', views.ListaEsperaEditar.as_view(), name='espera_editar'),
    path('eliminar/<int:pk>/', views.ListaEsperaEliminar.as_view(), name='espera_eliminar'),
    path('agendar/<int:pk>/', views.agendar_desde_espera, name='espera_agendar'),
]