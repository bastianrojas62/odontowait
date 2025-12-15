from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.utils import timezone

from .models import Paciente
from agenda.models import Cita, Odontologo
from espera.models import EntradaListaEspera


@login_required(login_url="login")
def inicio(request):
    # KPIs
    kpis = {
        "pacientes": Paciente.objects.count(),
        "pendientes_espera": EntradaListaEspera.objects.filter(estado="PENDIENTE").count(),
        "odontologos": Odontologo.objects.filter(activo=True).count(),
        "citas_hoy": Cita.objects.filter(inicia_en__date=timezone.localdate()).count(),
    }

    # Próximas citas (solo 10)
    proximas_citas = (
        Cita.objects
        .filter(inicia_en__gte=timezone.now())
        .order_by("inicia_en")[:10]
    )

    return render(request, "home.html", {
        "kpis": kpis,
        "proximas_citas": proximas_citas
    })


@require_POST
@login_required(login_url="login")
@permission_required("agenda.change_cita", raise_exception=True)
def cita_cambiar_estado(request, pk):
    cita = get_object_or_404(Cita, pk=pk)

    nuevo_estado = request.POST.get("estado")

    # ⚠️ Ajusta estos valores si tus choices usan otros textos
    estados_validos = {"AGENDADA", "CONFIRMADA", "NO_CONTESTA", "CANCELADA", "NO_ASISTE"}

    if nuevo_estado not in estados_validos:
        messages.error(request, "Estado inválido.")
        return redirect("inicio")

    cita.estado = nuevo_estado
    cita.save()

    messages.success(request, "Estado actualizado ✅")
    return redirect("inicio")


# ---------- CRUD PACIENTES ----------

class PacienteLista(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = "login"
    permission_required = "pacientes.view_paciente"
    model = Paciente
    template_name = "pacientes/paciente_lista.html"
    context_object_name = "pacientes"
    ordering = ["apellidos", "nombres"]


class PacienteCrear(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = "login"
    permission_required = "pacientes.add_paciente"
    model = Paciente
    fields = "__all__"
    template_name = "pacientes/paciente_form.html"
    success_url = reverse_lazy("paciente_lista")


class PacienteEditar(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = "login"
    permission_required = "pacientes.change_paciente"
    model = Paciente
    fields = "__all__"
    template_name = "pacientes/paciente_form.html"
    success_url = reverse_lazy("paciente_lista")


class PacienteEliminar(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = "login"
    permission_required = "pacientes.delete_paciente"
    model = Paciente
    template_name = "pacientes/paciente_confirmar_eliminar.html"
    success_url = reverse_lazy("paciente_lista")