from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Odontologo, Bloque, Cita
from .forms import CitaForm


# ----- ODONTÓLOGOS -----

class OdontologoLista(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = 'login'
    permission_required = 'agenda.view_odontologo'
    model = Odontologo
    template_name = 'agenda/odontologo_lista.html'
    context_object_name = 'odontologos'
    ordering = ['nombre_completo']


class OdontologoCrear(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = 'login'
    permission_required = 'agenda.add_odontologo'
    model = Odontologo
    fields = ['nombre_completo', 'especialidad', 'capacidad_diaria', 'activo']
    template_name = 'agenda/odontologo_form.html'
    success_url = reverse_lazy('odontologo_lista')


class OdontologoEditar(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = 'login'
    permission_required = 'agenda.change_odontologo'
    model = Odontologo
    fields = ['nombre_completo', 'especialidad', 'capacidad_diaria', 'activo']
    template_name = 'agenda/odontologo_form.html'
    success_url = reverse_lazy('odontologo_lista')


class OdontologoEliminar(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = 'login'
    permission_required = 'agenda.delete_odontologo'
    model = Odontologo
    template_name = 'agenda/odontologo_confirmar_eliminar.html'
    success_url = reverse_lazy('odontologo_lista')


# ----- BLOQUES -----

class BloqueLista(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = 'login'
    permission_required = 'agenda.view_bloque'
    model = Bloque
    template_name = 'agenda/bloque_lista.html'
    context_object_name = 'bloques'
    ordering = ['odontologo', 'inicia_en']


class BloqueCrear(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = 'login'
    permission_required = 'agenda.add_bloque'
    model = Bloque
    fields = ['odontologo', 'especialidad', 'inicia_en', 'termina_en', 'estado']
    template_name = 'agenda/bloque_form.html'
    success_url = reverse_lazy('bloque_lista')


# ----- CITAS -----

class CitaLista(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = 'login'
    permission_required = 'agenda.view_cita'
    model = Cita
    template_name = 'agenda/cita_lista.html'
    context_object_name = 'citas'
    ordering = ['-inicia_en']


class CitaCrear(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = 'login'
    permission_required = 'agenda.add_cita'
    model = Cita
    form_class = CitaForm
    template_name = 'agenda/cita_form.html'
    success_url = reverse_lazy('cita_lista')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs