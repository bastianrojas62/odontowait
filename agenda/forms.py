from django import forms
from django.core.exceptions import ValidationError
from datetime import date, datetime, timedelta
import uuid
import requests

from .models import Cita

DURACION_MINUTOS_DEFAULT = 30


def es_feriado_chile(fecha: date) -> bool:
    year = fecha.year
    url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/CL"

    r = requests.get(url, timeout=10)
    r.raise_for_status()
    feriados = r.json()

    objetivo = fecha.strftime("%Y-%m-%d")
    return any(f.get("date") == objetivo for f in feriados)


class CitaForm(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Fecha"
    )
    hora = forms.TimeField(
        widget=forms.TimeInput(attrs={"type": "time"}),
        label="Hora"
    )

    class Meta:
        model = Cita
        fields = ["paciente", "odontologo", "tratamiento", "fecha", "hora"]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        if request:
            paciente_id = request.GET.get("paciente")
            if paciente_id and "paciente" in self.fields:
                self.fields["paciente"].initial = paciente_id

    def clean(self):
        cleaned = super().clean()

        fecha = cleaned.get("fecha")
        hora = cleaned.get("hora")

        if not fecha or not hora:
            return cleaned

        try:
            if es_feriado_chile(fecha):
                raise ValidationError("Feriado irrenunciable, por favor marque otra fecha.")
        except requests.RequestException:
            raise ValidationError("No se pudo validar feriados en este momento. Intente nuevamente.")

        inicia_en = datetime.combine(fecha, hora)
        termina_en = inicia_en + timedelta(minutes=DURACION_MINUTOS_DEFAULT)

        cleaned["inicia_en"] = inicia_en
        cleaned["termina_en"] = termina_en

        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.inicia_en = self.cleaned_data["inicia_en"]
        instance.termina_en = self.cleaned_data["termina_en"]

        if not instance.estado:
            instance.estado = "AGENDADA"  # ajusta si tu modelo usa otro valor en choices

        if not instance.token_confirmacion:
            instance.token_confirmacion = uuid.uuid4().hex

        if commit:
            instance.save()
        return instance