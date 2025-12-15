from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PacienteViewSet, FeriadosChileView

router = DefaultRouter()
router.register(r'pacientes', PacienteViewSet, basename='pacientes')

urlpatterns = [
    path('', include(router.urls)),
    path('feriados/', FeriadosChileView.as_view(), name='api_feriados'),
]