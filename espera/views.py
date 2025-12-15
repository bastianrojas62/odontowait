from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone
from decimal import Decimal
from typing import Optional
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

from .models import EntradaListaEspera


class ListaEsperaLista(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = 'login'
    permission_required = 'espera.view_entradalistaespera'
    model = EntradaListaEspera
    template_name = 'espera/espera_lista.html'
    context_object_name = 'entradas'
    ordering = ['-derivado_en']


class ListaEsperaCrear(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = 'login'
    permission_required = 'espera.add_entradalistaespera'
    model = EntradaListaEspera

    # En derivación (CESFAM): no se elige estado ni puntaje
    fields = [
        'paciente',
        'tratamiento',
        'prioridad_clinica',
        'observaciones',
    ]

    template_name = 'espera/espera_form.html'
    success_url = reverse_lazy('espera_lista')

    def form_valid(self, form):
        form.instance.estado = 'PENDIENTE'

        prioridad: Optional[str] = form.cleaned_data.get('prioridad_clinica')

        if prioridad == 'P1':
            puntaje = Decimal('10')
        elif prioridad == 'P2':
            puntaje = Decimal('6')
        elif prioridad == 'P3':
            puntaje = Decimal('3')
        else:
            puntaje = Decimal('0')

        form.instance.puntaje = puntaje
        form.instance.puntaje_actualizado = timezone.now()

        return super().form_valid(form)


class ListaEsperaEditar(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = 'login'
    permission_required = 'espera.change_entradalistaespera'
    model = EntradaListaEspera

    # Hospital/Admin puede ajustar estado y puntaje si necesita
    fields = [
        'paciente',
        'tratamiento',
        'prioridad_clinica',
        'puntaje',
        'estado',
        'observaciones',
    ]

    template_name = 'espera/espera_form.html'
    success_url = reverse_lazy('espera_lista')

    def form_valid(self, form):
        form.instance.puntaje_actualizado = timezone.now()
        return super().form_valid(form)


class ListaEsperaEliminar(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = 'login'
    permission_required = 'espera.delete_entradalistaespera'
    model = EntradaListaEspera
    template_name = 'espera/espera_confirmar_eliminar.html'
    success_url = reverse_lazy('espera_lista')


def agendar_desde_espera(request, pk):
    """
    Redirige a crear una cita con el paciente preseleccionado desde la lista de espera.
    """
    if not request.user.is_authenticated:
        return redirect('login')

    entrada = get_object_or_404(EntradaListaEspera, pk=pk)

    if entrada.estado == 'AGENDADO':
        messages.info(request, "Esta entrada ya está agendada.")
        return redirect('espera_lista')

    url = reverse('cita_crear')
    return redirect(f"{url}?paciente={entrada.paciente.pk}&espera={entrada.pk}")